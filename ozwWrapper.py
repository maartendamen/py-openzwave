#!/usr/bin/env python
# -*- coding: utf-8 -*-

import openzwave
from collections import namedtuple
from openzwave import PyManager
import time
from louie import dispatcher, All
import logging

NamedPair = namedtuple('NamedPair', ['id', 'name'])
NodeInfo = namedtuple('NodeInfo', ['generic','basic','specific','security','version'])
GroupInfo = namedtuple('GroupInfo', ['index','label','maxAssociations','members'])

class ZWaveWrapperException(Exception):
    '''Exception class for ZWave Wrapper'''
    def __init__(self, value):
        Exception.__init__(self)
        self.value = value

    def __str__(self):
        return repr(self.value)

# TODO: allow value identification by device/index/instance
class ZWaveValueNode:
    '''Represents a single value for an OZW node element'''
    def __init__(self, homeId, nodeId, valueData):
        '''
        Initialize value node
        @param homeid: ID of home/driver
        @param nodeid: ID of node
        @param valueData: valueId dict (see openzwave.pyx)
        '''
        self._homeId = homeId
        self._nodeId = nodeId
        self._valueData = valueData
        self._lastUpdate = None

    def update(self, args):
        '''Update node value from callback arguments'''
        self._valueData = args['valueId']
        self._lastUpdate = time.time()

class ZWaveNode:
    '''Represents a single device within the Z-Wave Network'''

    def __init__(self, homeId, nodeId):
        '''
        Initialize zwave node
        @param homeId: ID of home/driver
        @param nodeId: ID of node
        '''
        self._lastUpdate = None
        self._homeId = homeId
        self._nodeId = nodeId
        self._capabilities = set()
        self._commandClasses = set()
        self._neighbors = set()
        self._values = dict()
        self._name = None
        self._location = None
        self._manufacturer = None
        self._product = None
        self._productType = None
        self._groups = list()

    id = property(lambda self: self._nodeId)
    name = property(lambda self: self._name)
    location = property(lambda self: self._location)
    type = property(lambda self: self._productType.name)

        # decorator?
        #self._batteryLevel = None # if COMMAND_CLASS_BATTERY
        #self._level = None # if COMMAND_CLASS_SWITCH_MULTILEVEL - maybe state? off - ramped - on?
        #self._powerLevel = None # hmm...
        # sensor multilevel?  instance/index
        # meter?
        # sensor binary?

class NullHandler(logging.Handler):
    '''A Null Logging Handler'''
    def emit(self, record):
        pass

class ZWaveWrapper:
    '''
        The purpose of this wrapper is to eliminate some of the tedium of working with
        the underlying API, which is extremely fine-grained.

        Wrapper provides a single, cohesive set of python objects representing the
        current state of the underlying ZWave network.  It is kept in sync with OZW and
        the network via callback hooks.

        Note: This version only handles a single Driver/Controller.  Modifications will
        be required in order to support more complex ZWave deployments.
    '''
    SIGNAL_DRIVER_READY = 'driverReady'
    SIGNAL_NODE_ADDED = 'nodeAdded'
    SIGNAL_NODE_READY = 'nodeReady'
    SIGNAL_SYSTEM_READY = 'systemReady'
    SIGNAL_VALUE_CHANGED = 'valueChanged'

    def __init__(self, device, config, log=None):
        self._log = log
        if self._log is None:
            self._log = logging.getLogger(__name__)
            self._log.addHandler(NullHandler())
        self._initialized = False
        self._homeId = None
        self._controllerNodeId = None
        self._controller = None
        self._nodes = dict()
        options = openzwave.PyOptions()
        options.create(config, '', '--logging false')
        options.lock()
        self._manager = openzwave.PyManager()
        self._manager.create()
        self._manager.addWatcher(self.zwcallback)
        self._manager.addDriver(device)

    controllerDescription = property(lambda self: self._getControllerDescription())
    nodeCount = property(lambda self: len(self._nodes))
    sleepingNodeCount = property(lambda self: self._getSleepingNodeCount())
    homeId = property(lambda self: self._homeId)
    controllerNode = property(lambda self: self._getNode(self._homeId, self._controllerNodeId))
    libraryTypeName = property(lambda self: self._libraryTypeName)
    libraryVersion = property(lambda self: self._libraryVersion)
    initialized = property(lambda self: self._initialized)

    def _getSleepingNodeCount(self):
        return 0
        # TODO: get actual sleeping node count

    def _getControllerDescription(self):
        if self._controllerNodeId:
            node = self._getNode(self._homeId, self._controllerNodeId)
            if node and node._product:
                return node._product.name
        return 'Unknown Controller'
    
    def zwcallback(self, args):
        '''
        Callback Handler

        @param args: callback dict
        '''
        notifyType = args['notificationType']
        self._log.debug('\n%s\n%s (node %s)\n%s', '-' * 30, notifyType, args['nodeId'], '-' * 30)
        if notifyType == 'DriverReady':
            self._handleDriverReady(args)
        elif notifyType in ('NodeAdded', 'NodeNew'):
            self._handleNodeChanged(args)
        elif notifyType in ('ValueAdded', 'ValueChanged'):
            self._handleValueChanged(args)
        elif notifyType == 'NodeQueriesComplete':
            self._handleNodeQueryComplete(args)
        elif notifyType in ('AwakeNodesQueried', 'AllNodesQueried'):
            self._handleInitializationComplete(args)
        else:
            self._log.debug('Skipping unhandled notification type [%s]', notifyType)

        # TODO: handle event
        # TODO: handle group change
        # TODO: handle value removed
        # TODO: handle node removed
        # TODO: handle config params

    def _handleDriverReady(self, args):
        '''
        Called once OZW has queried capabilities and determined startup values.  HomeID
        and NodeID of controller are known at this point.
        '''
        self._homeId = args['homeId']
        self._controllerNodeId = args['nodeId']
        self._controller = self._fetchNode(self._homeId, self._controllerNodeId)
        self._libraryVersion = self._manager.getLibraryVersion(self._homeId)
        self._libraryTypeName = self._manager.getLibraryTypeName(self._homeId)
        self._log.debug('Driver ready.  homeId is 0x%0.8x, controller node id is %d, using %s library version %s', self._homeId, self._controllerNodeId, self._libraryTypeName, self._libraryVersion)
        dispatcher.send(self.SIGNAL_DRIVER_READY, **{'homeId': self._homeId, 'nodeId': self._controllerNodeId})

    def _handleNodeQueryComplete(self, args):
        dispatcher.send(self.SIGNAL_NODE_READY, **{'homeId': self._homeId, 'nodeId': args['nodeId']})

    def _getNode(self, homeId, nodeId):
        return self._nodes[nodeId] if self._nodes.has_key(nodeId) else None

    def _fetchNode(self, homeId, nodeId):
        '''
        Build a new node and store it in nodes dict
        '''
        retval = self._getNode(homeId, nodeId)
        if retval is None:
            retval = ZWaveNode(homeId, nodeId)
            self._log.debug('Created new node with homeId 0x%0.8x, nodeId %d', homeId, nodeId)
            self._nodes[nodeId] = retval
        return retval

    def _handleNodeChanged(self, args):
        node = self._fetchNode(args['homeId'], args['nodeId'])
        node._lastUpdate = time.time()
        dispatcher.send(self.SIGNAL_NODE_ADDED, **{'homeId': args['homeId'], 'nodeId': args['nodeId']})

    def _getValueNode(self, homeId, nodeId, valueId):
        node = self._getNode(homeId, nodeId)
        if node is None:
            raise ZWaveWrapperException('Value notification received before node creation (homeId %.8x, nodeId %d)' % (homeId, nodeId))
        vid = valueId['id']
        if node._values.has_key(vid):
            retval = node._values[vid]
        else:
            retval = ZWaveValueNode(homeId, nodeId, valueId)
            self._log.debug('Created new value node with homeId %0.8x, nodeId %d, valueId %s', homeId, nodeId, valueId)
            node._values[vid] = retval
        return retval

    def _handleValueChanged(self, args):
        homeId = args['homeId']
        controllerNodeId = args['nodeId']
        valueId = args['valueId']
        node = self._fetchNode(homeId, controllerNodeId)
        node._lastUpdate = time.time()
        valueNode = self._getValueNode(homeId, controllerNodeId, valueId)
        valueNode.update(args)
        if self._initialized:
            #TODO: check valueid syntax - should be oK
            dispatcher.send(self.SIGNAL_VALUE_CHANGED, **{'homeId': homeId, 'nodeId': nodeId, 'valueId': valueId})


    def _updateNodeCapabilities(self, node):
        '''Update node's capabilities set'''
        nodecaps = set()
        if self._manager.isNodeListeningDevice(node._homeId, node._nodeId): nodecaps.add('listening')
        if self._manager.isNodeRoutingDevice(node._homeId, node._nodeId): nodecaps.add('routing')

        node._capabilities = nodecaps
        self._log.debug('Node [%d] capabilities are: %s', node._nodeId, node._capabilities)

    def _updateNodeCommandClasses(self, node):
        '''Update node's command classes'''
        classSet = set()
        for cls in PyManager.COMMAND_CLASS_DESC:
            if self._manager.getNodeClassInformation(node._homeId, node._nodeId, cls):
                classSet.add(cls)
        node._commandClasses = classSet
        self._log.debug('Node [%d] command classes are: %s', node._nodeId, node._commandClasses)
        # TODO: add command classes as string

    def _updateNodeNeighbors(self, node):
        '''Update node's neighbor list'''
        # TODO: I believe this is an OZW bug, but sleeping nodes report very odd (and long) neighbor lists
        node._neighbors = self._manager.getNodeNeighbors(node._homeId, node._nodeId)
        self._log.debug('Node [%d] neighbors are: %s', node._nodeId, node._neighbors)

    def _updateNodeInfo(self, node):
        '''Update general node information'''
        node._name = self._manager.getNodeName(node._homeId, node._nodeId)
        node._location = self._manager.getNodeLocation(node._homeId, node._nodeId)
        node._manufacturer = NamedPair(id=self._manager.getNodeManufacturerId(node._homeId, node._nodeId), name=self._manager.getNodeManufacturerName(node._homeId, node._nodeId))
        node._product = NamedPair(id=self._manager.getNodeProductId(node._homeId, node._nodeId), name=self._manager.getNodeProductName(node._homeId, node._nodeId))
        node._productType = NamedPair(id=self._manager.getNodeProductType(node._homeId, node._nodeId), name=self._manager.getNodeType(node._homeId, node._nodeId))
        node._nodeInfo = NodeInfo(
            generic = self._manager.getNodeGeneric(node._homeId, node._nodeId),
            basic = self._manager.getNodeBasic(node._homeId, node._nodeId),
            specific = self._manager.getNodeSpecific(node._homeId, node._nodeId),
            security = self._manager.getNodeSecurity(node._homeId, node._nodeId),
            version = self._manager.getNodeVersion(node._homeId, node._nodeId)
        )

    def _updateNodeGroups(self, node):
        '''Update node group/association information'''
        groups = list()
        for i in range(0, self._manager.getNumGroups(node._homeId, node._nodeId)):
            groups.append(GroupInfo(
                index = i,
                label = self._manager.getGroupLabel(node._homeId, node._nodeId, i),
                maxAssociations = self._manager.getMaxAssociations(node._homeId, node._nodeId, i),
                members = self._manager.getAssociations(node._homeId, node._nodeId, i)
            ))
        node._groups = groups
        self._log.debug('Node [%d] groups are: %s', node._nodeId, node._groups)

    def _handleInitializationComplete(self, args):
        controllercaps = set()
        if self._manager.isPrimaryController(self._homeId): controllercaps.add('primaryController')
        if self._manager.isStaticUpdateController(self._homeId): controllercaps.add('staticUpdateController')
        if self._manager.isBridgeController(self._homeId): controllercaps.add('bridgeController')
        self._controllerCaps = controllercaps
        self._log.debug('Controller capabilities are: %s', controllercaps)
        for node in self._nodes.values():
            self._updateNodeCapabilities(node)
            self._updateNodeCommandClasses(node)
            self._updateNodeNeighbors(node)
            self._updateNodeInfo(node)
            self._updateNodeGroups(node)
        self._initialized = True
        dispatcher.send(self.SIGNAL_SYSTEM_READY, **{'homeId': self._homeId})

# commands:
# - refresh node
# - request node state
# - request config param/request all config params
# - set node level
# - set node on/off
# - switch all on/off
# - add node, remove node (needs command support)

# editing:
# - add association, remove association
# - set config param
# - set node manufacturer name
# - set node name
# - set node location
# - set node product name
# - set poll interval
# - set wake up interval (needs command support)

# questions:
# - can powerlevel be queried directly? See PowerLevel.cpp in command classes
# - need more detail about notification events!
# - what is COMMAND_CLASS_HAIL used for?
# - what is COMMAND_CLASS_INDICATOR used for?
# - wake up duration sent via COMMAND_CLASS_WAKE_UP

#   initialization callback sequence:
#
#   [driverReady]
#
#   [nodeAdded] <-------------------------+ This cycle is extremely quick, well under one second.
#       [nodeProtocolInfo]                |
#       [nodeNaming]                      |
#       [valueAdded] <---------------+    |
#                                    |    |
#       {REPEATS FOR EACH VALUE} ----+    |
#                                         |
#       [group] <--------------------+    |
#                                    |    |
#       {REPEATS FOR EACH GROUP} ----+    |
#                                         |
#   {REPEATS FOR EACH NODE} --------------+
#
#   [? (no notification)] <---------------+ (no notification announces the beginning of this cycle)
#                                         |
#       [valueChanged] <-------------+    | This cycle can take some time, especially if some nodes
#                                    |    | are sleeping or slow to respond.
#       {REPEATS FOR EACH VALUE} ----+    |
#                                         |
#       [group] <--------------------+    |
#                                    |    |
#       {REPEATS FOR EACH GROUP} ----+    |
#                                         |
#   [nodeQueriesComplete]                 |
#                                         |
#   {REPEATS FOR EACH NODE} --------------+
#
#   [awakeNodesQueried] or [allNodesQueried] (with nodeId 255)
