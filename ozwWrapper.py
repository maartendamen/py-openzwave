#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import namedtuple
import openzwave
from openzwave import PyManager

NamedPair = namedtuple('NamedPair', ['id','name'])
class ZWaveNode:
    def __init__(self, homeid, nodeid):
        self._lastUpdate = None
        self._homeid = homeid
        self._nodeid = nodeid
        self._capabilities = set() # bridge controller, listening device, routing device, primary controoler, etc
        self._commandclasses = set()
        self._neighbors = set()
        self._values = dict() # id -> PyValueID object
        self._location = None
        self._manufacturer = None # id, name: namedTuple
        self._product = None # id, name: namedTuple
        self._productType = None # id, name: namedTuple
        self._nodeType = None # descriptive
        self._name = None
        self._batteryLevel = None # if COMMAND_CLASS_BATTERY
        self._level = None # if COMMAND_CLASS_SWITCH_MULTILEVEL - maybe state? off - ramped - on?
        # sensor multilevel?  instance/index
        # meter?
        # sensor binary?
        # state: awake, asleep, etc

class ZWaveWrapper:
    '''This is a work in progress.  Nothing to see here, please move along.'''
    def __init__(self):
        self._homeid = None
        self._controllerNodeId = None
        self._controller = None
        self._nodes = dict()
        options = openzwave.PyOptions()
        # TODO locate this...
        options.create("/home/steve/py-openzwave/openzwave/config/","","")
        options.lock()
        self._manager = openzwave.PyManager()
        self._manager.create()
        self._manager.addWatcher(self.zwcallback)

    def open(self, device):
        self._manager.addDriver(device)

    # library: type name, version - this is in controller
    # hack, hack, copy, paste - use the right reference.  I'm tired.  Delete it before commit.
    Notify_Type_ValueAdded = 0
    Notify_Type_ValueRemoved = 1
    Notify_Type_ValueChanged = 2
    Notify_Type_Group = 3
    Notify_Type_NodeNew = 4
    Notify_Type_NodeAdded = 5
    Notify_Type_NodeRemoved = 6
    Notify_Type_NodeProtocolInfo = 7
    Notify_Type_NodeNaming = 8
    Notify_Type_NodeEvent = 9
    Notify_Type_PollingDisabled = 10
    Notify_Type_PollingEnabled = 11
    Notify_Type_DriverReady = 12
    Notify_Type_DriverReset = 13
    Notify_Type_MsgComplete = 14
    Notify_Type_NodeQueriesComplete = 15
    Notify_Type_AwakeNodesQueried = 16
    Notify_Type_AllNodesQueried = 17

    # callback param order: (notificationtype, homeid, nodeid, vid, groupidx, event, itemValue, itemLabel, itemUnits)
    def zwcallback(self, type, *args):
        if type == self.Notify_Type_DriverReady:
            self._handleDriverReady(args)
        elif type == self.Notify_Type_NodeAdded or type == self.Notify_Type_NodeNew:
            self._handleNodeAdded(args)
        elif type == self.Notify_Type_ValueAdded or type == self.Notify_Type_ValueChanged:
            self._handleValueChanged(args)
        elif type >= self.Notify_Type_AwakeNodesQueried:
            self._handleInitializationComplete()
        else:
            print('Skipping [%s]' % PyManager.CALLBACK_DESC[type])

        # TODO: handle event
        # TODO: handle group change
        # TODO: handle value removed
        # TODO: handle node removed

    def _handleDriverReady(self, *args):
        '''
        Called once OZW has queried capabilities and determined startup values.  HomeID
        and NodeID of controller are known at this point.
        '''
        self._homeid = args[0]
        self._controllerNodeId = args[1]
        self._controller = self._makeNewNode(self._homeid, self._controllerNodeId)
        print("Driver ready.  homeid is %0.2x, controller node id is %d" % (self._homeid, self._controllerNodeId))
    
    def _makeNewNode(self, homeid, nodeid):
        '''
        Build a new node and store it in nodes dict
        '''
        retval = None
        if self._nodes.has_key(nodeid):
            retval = self._nodes[nodeid]
        else:
            retval = ZWaveNode(homeid, nodeid)
            print("Created new node with homeid %0.2x, nodeid %d" % (homeid, nodeid))
            self._nodes[nodeid] = retval
        return retval

    def _handleNodeAdded(self, *args):
        self._makeNewNode(args[0], args[1])

    def _handleValueChanged(self, *args):
        # value wrapper: added value, label, units
        pass

    def _handleInitializationComplete(self, *args):
        pass

# groups: node's numgroups determines size; group home, node, label, max associations,
# nodebasic, nodegeneric, nodespecific, max baud rate,
# node caps: isBridgeController, isListeningDevice, isRoutingDevice, isPrimaryController, isStaticUpdateController,
# isNodeInfoReceived
# TODO how to handle config params?

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

# need label, units for values


'''
driver ready (reports homeid and controller node id)

    node added - genre basic (is callback missing data here?)
    node protocol info - genre basic (is callback missing data here?)
    node naming - genre basic (is callback missing data here?)
    value added (for each value) - initial value is bogus ? - Genre basic/user/system
    groups changed
    value changed
    node queries complete (with associated node)

    [awake nodes queried] or [all nodes queried] with nodeid 255... some data trickles in later
    
'''
