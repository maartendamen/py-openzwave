cdef extern from "<string>" namespace "std":
    cdef cppclass string:
        string()
        string(char *)
        char * c_str()

ctypedef unsigned int uint32
ctypedef unsigned char uint8

cdef extern from "Options.h" namespace "OpenZWave":
    cdef cppclass Options:
        bint Lock()

cdef extern from "Python.h":
    void PyEval_InitThreads()

cdef extern from "Options.h" namespace "OpenZWave::Options":
    Options* Create(string a, string b, string c)

cdef extern from *:
    ctypedef char* const_notification "OpenZWave::Notification const*"

cdef extern from "Notification.h" namespace "OpenZWave::Notification":

    cdef enum NotificationType:
        Type_ValueAdded = 0
        Type_ValueRemoved = 1
        Type_ValueChanged = 2
        Type_Group = 3
        Type_NodeNew = 4
        Type_NodeAdded = 5
        Type_NodeRemoved = 6
        Type_NodeProtocolInfo = 7
        Type_NodeNaming = 8
        Type_NodeEvent = 9
        Type_PollingDisabled = 10
        Type_PollingEnabled = 11
        Type_DriverReady = 12
        Type_DriverReset = 13
        Type_MsgComplete = 14
        Type_NodeQueriesComplete = 15
        Type_AwakeNodesQueried = 16
        Type_AllNodesQueried = 17

cdef extern from "ValueID.h" namespace "OpenZWave":

    cdef cppclass ValueID:
        uint8 GetCommandClassId()
        uint8 GetIndex()

cdef extern from "Notification.h" namespace "OpenZWave":

    cdef cppclass Notification:
        NotificationType GetType()
        uint32 GetHomeId()
        uint8 GetNodeId()
        ValueID& GetValueID()

ctypedef void (*pfnOnNotification_t)(const_notification _pNotification, void* _context )

cdef extern from "Manager.h" namespace "OpenZWave":

    cdef cppclass Manager:
        # // Configuration
        void WriteConfig(uint32 homeid)
        # Options* GetOptions()
        # // Drivers
        bint AddDriver(string serialport)
        bint RemoveDriver(string controllerPath)
        uint8 GetControllerNodeId(uint32 homeid)
        bint IsPrimaryController(uint32 homeid)
        bint IsStaticUpdateController(uint32 homeid)
        bint IsBridgeController(uint32 homeid)
        string GetLibraryVersion(uint32 homeid)
        string GetLibraryTypeName(uint32 homeid)
        # // Polling
        uint32 GetPollInterval()
        void SetPollInterval(uint8 seconds)
        bint EnablePoll(ValueID& valueId)
        bint DisablePoll(ValueID& valueId)
        bint isPolled(ValueID& valueId)
        # // Node Information
        bint RefreshNodeInfo(uint32 homeid, uint8 nodeid)
        void RequestNodeState(uint32 homeid, uint8 nodeid)
        bint IsNodeListeningDevice(uint32 homeid, uint8 nodeid)
        bint IsNodeRoutingDevice(uint32 homeid, uint8 nodeid)
        uint32 GetNodeMaxBaudRate(uint32 homeid, uint8 nodeid)
        uint8 GetNodeVersion(uint32 homeid, uint8 nodeid)
        uint8 GetNodeSecurity(uint32 homeid, uint8 nodeid)
        uint8 GetNodeBasic(uint32 homeid, uint8 nodeid)
        uint8 GetNodeGeneric(uint32 homeid, uint8 nodeid)
        uint8 GetNodeSpecific(uint32 homeid, uint8 nodeid)
        string GetNodeType(uint32 homeid, uint8 nodeid)
        # uint32 GetNodeNeighbors(uint32 homeid, uint8 nodeid, uint8** nodeNeighbors)
        string GetNodeManufacturerName(uint32 homeid, uint8 nodeid)
        string GetNodeProductName(uint32 homeid, uint8 nodeid)
        string GetNodeName(uint32 homeid, uint8 nodeid)
        string GetNodeLocation(uint32 homeid, uint8 nodeid)
        string GetNodeManufacturerId(uint32 homeid, uint8 nodeid)
        string GetNodeProductType(uint32 homeid, uint8 nodeid)
        string GetNodeProductId(uint32 homeid, uint8 nodeid)
        void SetNodeManufacturerName(uint32 homeid, uint8 nodeid, string manufacturerName)
        void SetNodeProductName(uint32 homeid, uint8 nodeid, string productName)
        void SetNodeName(uint32 homeid, uint8 nodeid, string productName)
        void SetNodeLocation(uint32 homeid, uint8 nodeid, string location)
        void SetNodeOn(uint32 homeid, uint8 nodeid)
        void SetNodeOff(uint32 homeid, uint8 nodeid)
        void SetNodeLevel(uint32 homeid, uint8 nodeid, uint8 level)
        bint IsNodeInfoReceived(uint32 homeid, uint8 nodeid)
        # bool GetNodeClassInformation(uint32 homeid, uint8 nodeid, uint8 commandClassId, string className = NULL, uint8 *classVersion = NULL)
        # // Values
        string GetValueLabel(ValueID& valueid)
        void SetValueLabel(ValueID& valueid, string value)
        string GetValueUnits(ValueID& valueid)
        void SetValueUnits(ValueID& valueid, string value)
        string GetValueHelp(ValueID& valueid)
        void SetValueHelp(ValueID& valueid, string value)
        uint32 GetValueMin(ValueID& valueid)
        uint32 GetValueMax(ValueID& valueid)
        bint IsValueReadOnly(ValueID& valueid)
        bint IsValueSet(ValueID& valueid)
        bint GetValueAsBool(ValueID& valueid, bint* o_value)
        bint GetValueAsByte(ValueID& valueid, uint8* o_value)
        bint GetValueAsFloat(ValueID& valueid, float* o_value)
        bint GetValueAsInt(ValueID& valueid, uint32* o_value)
        bint GetValueAsShort(ValueID& valueid, uint32* o_value)
        bint GetValueAsString(ValueID& valueid, string* o_value)
        bint GetValueListSelection(ValueID& valueid, string* o_value)
        bint GetValueListSelection(ValueID& valueid, uint32* o_value)
        #bint GetValueListItems(ValueID& valueid, vector<string>* o_value)
        bint SetValue(ValueID& valueid, uint8 value)
        bint SetValue(ValueID& valueid, float value)
        bint SetValue(ValueID& valueid, uint32 value)
        bint SetValue(ValueID& valueid, uint32 value)
        bint SetValue(ValueID& valueid, string value)
        bint SetValueListSelection(ValueID& valueid, string selecteditem)
        bint PressButton(ValueID& valueid)
        bint ReleaseButton(ValueID& valueid)
        uint8 GetNumSwitchPoints(ValueID& valueid)
        # // Climate Control
        bint SetSwitchPoint(ValueID& valueid, uint8 hours, uint8 minutes, uint8 setback)
        bint RemoveSwitchPoint(ValueID& valueid, uint8 hours, uint8 minutes)
        bint ClearSwitchPoints(ValueID& valueid)
        bint GetSwitchPoint(ValueID& valueid, uint8 idx, uint8* o_hours, uint8* o_minutes, uint8* o_setback)
        # // SwitchAll
        void SwitchAllOn(uint32 homeid)
        void SwitchAllOff(uint32 homeid)
        # // Configuration Parameters
        bint SetConfigParam(uint32 homeid, uint8 nodeid, uint8 param, uint32 value)
        void RequestConfigParam(uint32 homeid, uint8 nodeid, uint8 aram)
        void RequestAllConfigParams(uint32 homeid, uint8 nodeid)
        # // Groups
        uint8 GetNumGroups(uint32 homeid, uint8 nodeid)
        #uint32 GetAssociations(uint32 homeid, uint8 nodeid, uint8 groupidx, uint8** o_associations)
        uint8 GetMaxAssociations(uint32 homeid, uint8 nodeid, uint8 groupidx)
        string GetGroupLabel(uint32 homeid, uint8 nodeid, uint8 groupidx)
        void AddAssociation(uint32 homeid, uint8 nodeid, uint8 groupidx, uint8 targetnodeid)
        void RemoveAssociation(uint32 homeid, uint8 nodeid, uint8 groupidx, uint8 targetnodeid)
        bint AddWatcher(pfnOnNotification_t notification, void* context)
        bint RemoveWatcher(pfnOnNotification_t notification, void* context)
        # // Controller Commands
        void ResetController(uint32 homeid)
        void SoftReset(uint32 homeid)
        #bint BeginControllerCommand(uint32 homeid, Driver::ControllerCommand _command, Driver::pfnControllerCallback_t _callback = NULL, void* _context = NULL, bool _highPower = false, uint8 _nodeId = 0xff )
        bint CancelControllerCommand(uint32 homeid)

cdef extern from "Manager.h" namespace "OpenZWave::Manager":
    Manager* Create()
    Manager* Get()

cdef class PyOptions:
    cdef Options *options

    def create(self, char *a, char *b, char *c):
        self.options = Create(string(a), string(b), string(c))

    def lock(self):
        return self.options.Lock()

cdef void value_callback(int homeid, int nodeid, ValueID _valueid, void* _context, int type):
    cdef uint8 bytevalue
    cdef Manager *manager = Get()

    manager.GetValueAsByte( _valueid, &bytevalue)
    commandclassid = _valueid.GetCommandClassId()
    index = _valueid.GetIndex()

    # Add polling // Dirty hack
    if nodeid != 1 and commandclassid == 32:
        manager.SetPollInterval(60)
        manager.EnablePoll(_valueid)

    (<object>_context)(type, homeid, nodeid, commandclassid, index, bytevalue)

cdef void callback(const_notification _notification, void* _context) with gil:

    cdef Notification* notification = <Notification*>_notification
    type = notification.GetType()

    if type == Type_DriverReady:
        g_homeid = notification.GetHomeId()
        print g_homeid
        (<object>_context)(type, g_homeid)

    elif type == Type_ValueAdded:
        homeid = notification.GetHomeId()
        nodeid = notification.GetNodeId()
        value_callback(homeid, nodeid, notification.GetValueID(), _context, Type_ValueAdded)

    elif type == Type_ValueChanged:
        homeid = notification.GetHomeId()
        nodeid = notification.GetNodeId()
        value_callback(homeid, nodeid, notification.GetValueID(), _context, Type_ValueChanged)

    elif type == Type_AllNodesQueried:
        (<object>_context)(type)

    elif type == Type_NodeAdded:
        homeid = notification.GetHomeId()
        nodeid = notification.GetNodeId()
        (<object>_context)(type, homeid, nodeid)

cdef class PyManager:
    cdef Manager *manager

    def create(self):
        self.manager = Create()
        PyEval_InitThreads()

    def writeConfig(self, homeid):
        self.manager.WriteConfig(homeid)

    def addDriver(self, char *serialport):
        self.manager.AddDriver( string(serialport) )

    def removeDriver(self, char *serialport):
        self.manager.RemoveDriver( string(serialport) )

    def getControllerNodeId(self, homeid):
        return self.manager.GetControllerNodeId(homeid)

    def isPrimaryController(self, homeid):
        return self.manager.IsPrimaryController(homeid)

    def isStaticUpdateController(self, homeid):
        return self.manager.IsStaticUpdateController(homeid)

    def isBridgeController(self, homeid):
        return self.manager.IsBridgeController(homeid)

    def getLibraryVersion(self, homeid):
        cdef string library_string = self.manager.GetLibraryVersion(homeid)
        return library_string.c_str()

    def getLibraryVersion(self, homeid):
        cdef string library_type_string = self.manager.GetLibraryTypeName(homeid)
        return library_type_string.c_str()

    def getPollInterval(self):
        return self.manager.GetPollInterval()

    def setPollInterval(self, seconds):
        self.manager.SetPollInterval(seconds)

#        bint EnablePoll(ValueID& valueId)
#        bint DisablePoll(ValueID& valueId)
#        bint isPolled(ValueID& valueId)

    def refreshNodeInfo(self, homeid, nodeid):
        return self.manager.RefreshNodeInfo(homeid, nodeid)

    def requestNodeState(self, homeid, nodeid):
        self.manager.RequestNodeState(homeid, nodeid)

    def isNodeListeningDevice(self, homeid, nodeid):
        return self.manager.IsNodeListeningDevice(homeid, nodeid)

    def isNodeRoutingDevice(self, homeid, nodeid):
        return self.manager.IsNodeRoutingDevice(homeid, nodeid)

    def getNodeMaxBaudRate(self, homeid, nodeid):
        return self.manager.GetNodeMaxBaudRate(homeid, nodeid)

    def getNodeVersion(self, homeid, nodeid):
        return self.manager.GetNodeVersion(homeid, nodeid)

    def getNodeSecurity(self, homeid, nodeid):
        return self.manager.GetNodeSecurity(homeid, nodeid)

    def getNodeBasic(self, homeid, nodeid):
        return self.manager.GetNodeBasic(homeid, nodeid)

    def getNodeGeneric(self, homeid, nodeid):
        return self.manager.GetNodeGeneric(homeid, nodeid)

    def getNodeSpecific(self, homeid, nodeid):
        return self.manager.GetNodeSpecific(homeid, nodeid)

    def getNodeType(self, homeid, nodeid):
        cdef string node_type_str = self.manager.GetNodeType(homeid, nodeid)
        return node_type_str.c_str()

    # uint32 GetNodeNeighbors(uint32 homeid, uint8 nodeid, uint8** nodeNeighbors)

    def getNodeManufacturerName(self, homeid, nodeid):
         cdef string manufacturer_string = self.manager.GetNodeManufacturerName(homeid, nodeid)
         return manufacturer_string.c_str()

    def getNodeProductName(self, homeid, nodeid):
        cdef string productname_string = self.manager.GetNodeProductName(homeid, nodeid)
        return productname_string.c_str()

    def getNodeName(self, homeid, nodeid):
        cdef string c_string = self.manager.GetNodeName(homeid, nodeid)
        return c_string.c_str()

    def getNodeLocation(self, homeid, nodeid):
        cdef string c_string = self.manager.GetNodeLocation(homeid, nodeid)
        return c_string.c_str()

    def getNodeManufacturerId(self, homeid, nodeid):
        cdef string c_string = self.manager.GetNodeManufacturerId(homeid, nodeid)
        return c_string.c_str()

    def getNodeProductType(self, homeid, nodeid):
        cdef string producttype_string = self.manager.GetNodeProductType(homeid, nodeid)
        return producttype_string.c_str()

    def getNodeProductId(self, homeid, nodeid):
        cdef string productid_string = self.manager.GetNodeProductId(homeid, nodeid)
        return productid_string.c_str()

#        void SetNodeManufacturerName(uint32 homeid, uint8 nodeid, string manufacturerName)
#        void SetNodeProductName(uint32 homeid, uint8 nodeid, string productName)
#        void SetNodeName(uint32 homeid, uint8 nodeid, string productName)
#        void SetNodeLocation(uint32 homeid, uint8 nodeid, string location)

    def setNodeOn(self, homeid, nodeid):
        self.manager.SetNodeOn(homeid, nodeid)

    def setNodeOff(self, homeid, nodeid):
        self.manager.SetNodeOff(homeid, nodeid)

    def setNodeLevel(self, homeid, nodeid, level):
        self.manager.SetNodeLevel(homeid, nodeid, level)

    def isNodeInfoReceived(self, homeid, nodeid):
        return self.manager.IsNodeInfoReceived(homeid, nodeid)
#        # bool GetNodeClassInformation(uint32 homeid, uint8 nodeid, uint8 commandClassId, string className = NULL, uint8 *classVersion = NULL)
#        string GetValueLabel(ValueID& valueid)
#        void SetValueLabel(ValueID& valueid, string value)
#        string GetValueUnits(ValueID& valueid)
#        void SetValueUnits(ValueID& valueid, string value)
#        string GetValueHelp(ValueID& valueid)
#        void SetValueHelp(ValueID& valueid, string value)
#        uint32 GetValueMin(ValueID& valueid)
#        uint32 GetValueMax(ValueID& valueid)
#        bint IsValueReadOnly(ValueID& valueid)
#        bint IsValueSet(ValueID& valueid)
#        bint GetValueAsBool(ValueID& valueid, bint* o_value)
#        bint GetValueAsByte(ValueID& valueid, uint8* o_value)
#        bint GetValueAsFloat(ValueID& valueid, float* o_value)
#        bint GetValueAsInt(ValueID& valueid, uint32* o_value)
#        bint GetValueAsShort(ValueID& valueid, uint32* o_value)
#        bint GetValueAsString(ValueID& valueid, string* o_value)
#        bint GetValueListSelection(ValueID& valueid, string* o_value)
#        bint GetValueListSelection(ValueID& valueid, uint32* o_value)
#        #bint GetValueListItems(ValueID& valueid, vector<string>* o_value)
#        bint SetValue(ValueID& valueid, uint8 value)
#        bint SetValue(ValueID& valueid, float value)
#        bint SetValue(ValueID& valueid, uint32 value)
#        bint SetValue(ValueID& valueid, uint32 value)
#        bint SetValue(ValueID& valueid, string value)
#        bint SetValueListSelection(ValueID& valueid, string selecteditem)
#        bint PressButton(ValueID& valueid)
#        bint ReleaseButton(ValueID& valueid)
#        uint8 GetNumSwitchPoints(ValueID& valueid)
#        # // Climate Control
#        bint SetSwitchPoint(ValueID& valueid, uint8 hours, uint8 minutes, uint8 setback)
#        bint RemoveSwitchPoint(ValueID& valueid, uint8 hours, uint8 minutes)
#        bint ClearSwitchPoints(ValueID& valueid)
#        bint GetSwitchPoint(ValueID& valueid, uint8 idx, uint8* o_hours, uint8* o_minutes, uint8* o_setback)
#        # // SwitchAll
#        void SwitchAllOn(uint32 homeid)
#        void SwitchAllOff(uint32 homeid)
#        # // Configuration Parameters
#        bint SetConfigParam(uint32 homeid, uint8 nodeid, uint8 param, uint32 value)
#        void RequestConfigParam(uint32 homeid, uint8 nodeid, uint8 aram)
#        void RequestAllConfigParams(uint32 homeid, uint8 nodeid)
#        # // Groups
#        uint8 GetNumGroups(uint32 homeid, uint8 nodeid)
#        #uint32 GetAssociations(uint32 homeid, uint8 nodeid, uint8 groupidx, uint8** o_associations)
#        uint8 GetMaxAssociations(uint32 homeid, uint8 nodeid, uint8 groupidx)
#        string GetGroupLabel(uint32 homeid, uint8 nodeid, uint8 groupidx)
#        void AddAssociation(uint32 homeid, uint8 nodeid, uint8 groupidx, uint8 targetnodeid)
#        void RemoveAssociation(uint32 homeid, uint8 nodeid, uint8 groupidx, uint8 targetnodeid)

    def add_watcher(self, pythonfunc):
        self.manager.AddWatcher(callback, <void*>pythonfunc)

#        bint RemoveWatcher(pfnOnNotification_t notification, void* context)
#        # // Controller Commands
#        void ResetController(uint32 homeid)
#        void SoftReset(uint32 homeid)
#        #bint BeginControllerCommand(uint32 homeid, Driver::ControllerCommand _command, Driver::pfnControllerCallback_t _callback = NULL, void* _context = NULL, bool _highPower = false, uint8 _nodeId = 0xff )
#        bint CancelControllerCommand(uint32 homeid)
