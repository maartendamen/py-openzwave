import openzwave
from openzwave import PyManager

options = openzwave.PyOptions()

# Specify the open-zwave config path here
options.create("/home/steve/py-openzwave/openzwave/config/","","")
options.lock()
manager = openzwave.PyManager()
manager.create()

# callback order: (notificationtype, homeid, nodeid, ValueID, groupidx, event)
def callback(type, *args):
    print('\n%s\n[%s]:\n' % ('-'*20, PyManager.CALLBACK_DESC[type]))
    if args:
        print('homeId: 0x%.8x' % args[0])
        print('nodeId: %d' % args[1])
        print('valueID: %s' % args[2])
        if (args[3] != 0xff): print('GroupIndex: %d' % args[3])
        if (args[4] != 0xff): print('Event: %d' % args[4])
    print('%s\n' % ('-'*20,))

manager.addWatcher(callback)
manager.addDriver('/dev/keyspan-1')
