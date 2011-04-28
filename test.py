import openzwave

options = openzwave.PyOptions()

# Specify the open-zwave config path here
options.create("py-openzwave/openzwave/config/","","")
options.lock()
manager = openzwave.PyManager()
manager.create()

cbstrs=['value added','value removed','value changed','groups changed','new node','node added',
'node removed','node protocol info','node naming','node event','polling disabled',
'polling enabled','driver ready','driver reset','message complete','node queries complete',
'awake nodes queried','all nodes queried']

def callback(type, *args):
    print('\n%s\n[%s]: type=%d\n' % ('-'*20, cbstrs[type], type))
    if args:
        print('homeId: %x' % args[0])
        print('nodeId: %d' % args[1])
        i = 2
        for arg in args[2:]:
            print('arg[%d]: %d (0x%.2x)' % (i, arg, arg))
            i += 1
    print('%s\n' % ('-'*20,))

manager.addWatcher(callback)
manager.addDriver('/dev/ttyUSB6')
