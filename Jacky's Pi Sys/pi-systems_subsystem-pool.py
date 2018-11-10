import importlib
subsystem = importlib.import_module('pi-systems_subsystem-base')


# This variable is a dictionary that contains all subsystems.
# Subsystems are automatically placed in here upon creation
# unless otherwise specified (See subsystem-base for the code).
subsys_pool = {}

print('Just got created ')

def add(subsys, overwrite=False):
    if subsys.name in subsys_pool and overwrite is False:
        raise KeyError('Subsystem with key %s already exists in the pool!' % (subsys.name))

    subsys_pool[subsys.name] = subsys
    print('Subsystem added to pool: %s' % (subsys.name))


def remove(subsys):
    if isinstance(subsys, subsystem.Subsystem):
        subsys = subsys.name
    
    if not isinstance(subsys, str):
        raise TypeError("Provided subsystem removal key is an invalid type!")

    if subsys in subsys_pool:
        print(repr(subsys_pool))
        subsys_pool.pop(subsys)
    else:
        raise KeyError("Subsystem removal key not found in the pool!")
    

def get_all():
    return subsys_pool

        
def stop_all():
    print("Closing all subsystems.")
    for subsys in subsys_pool.values():
        subsys.stop()