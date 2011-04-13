import openzwave

options = openzwave.PyOptions()

# Specify the open-zwave config path here
options.create("c:/workspace/py-openzwave/openzwave/config/","","")
options.lock()
manager = openzwave.PyManager()
manager.create()

def callback(type, *args):
    
    if type == 5:
        # Test callback of Type_NodeAdded, called after a node has been added to open-zwave.
        homeid = args[0]
        nodeid = args[1]
        
    elif type == 0:
        print "value added"
        print "type is:", type
        print "args is:", args
        
    elif type == 2:
        print "value changed"
        print "type is:", type
        print "args is:", args

manager.add_watcher(callback)
manager.add_driver("\\\\.\\COM16")