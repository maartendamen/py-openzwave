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
		bint AddDriver(string serialport)
		bint AddWatcher(pfnOnNotification_t notification, void* context)
		void SetNodeOff(uint32 homeid, uint8 nodeid)
		void SetNodeOn(uint32 homeid, uint8 nodeid)
		void WriteConfig(uint32 homeid)
		string GetNodeManufacturerName(uint32 homeid, uint8 nodeid)
		string GetNodeProductName(uint32 homeid, uint8 nodeid)
		string GetNodeProductId(uint32 homeid, uint8 nodeid)
		bint IsNodeListeningDevice(uint32 homeid, uint8 nodeid)
		uint32 GetNodeMaxBaudRate(uint32 homeid, uint8 nodeid)
		uint8 GetNodeBasic(uint32 homeid, uint8 nodeid)
		uint8 GetNodeGeneric(uint32 homeid, uint8 nodeid)
		bint GetValueAsByte(ValueID& id, uint8* o_value)
		bint EnablePoll(ValueID valueid)
		void SetPollInterval(int seconds)

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
	
	def add_driver(self, char *serialport):
		self.manager.AddDriver( string(serialport) )
		
	def add_watcher(self, pythonfunc):
		self.manager.AddWatcher(callback, <void*>pythonfunc)
		
	def setnodeoff(self, homeid, nodeid):		
		self.manager.SetNodeOff(homeid, nodeid)
		
	def setnodeon(self, homeid, nodeid):
		self.manager.SetNodeOn(homeid, nodeid)
		
	def get_manufacturer(self, homeid, nodeid):
		cdef string manufacturer_string = self.manager.GetNodeManufacturerName(homeid, nodeid)
		return manufacturer_string.c_str()
		
	def get_producttype(self, homeid, nodeid):
		cdef string producttype_string = self.manager.GetNodeProductName(homeid, nodeid)
		return producttype_string.c_str()
	
	def get_productid(self, homeid, nodeid):
		cdef string productid_string = self.manager.GetNodeProductId(homeid, nodeid)
		return productid_string.c_str()	
	
	def get_listening(self, homeid, nodeid):
		return self.manager.IsNodeListeningDevice(homeid, nodeid)
		
	def get_maxbaudrate(self, homeid, nodeid):
		return self.manager.GetNodeMaxBaudRate(homeid, nodeid)
		
	def writeconfig(self, homeid):
		self.manager.WriteConfig(homeid)