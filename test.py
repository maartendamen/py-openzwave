import openzwave

options = openzwave.PyOptions()

# Specify the open-zwave config path here
options.create("../../../openzwave/config/","","")
options.lock()
manager = openzwave.PyManager()
manager.create()

def callback(type, *args):
    
    if type == 5:
        # Test callback of Type_NodeAdded, called after a node has been added to open-zwave.
        homeid = args[0]
        nodeid = args[1]

manager.add_watcher(callback)
manager.add_driver("\\\\.\\COM16")