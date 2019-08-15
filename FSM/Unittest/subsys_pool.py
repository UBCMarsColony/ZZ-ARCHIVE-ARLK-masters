import importlib
subsystem = importlib.import_module('FSM.Unittest.subsys_base')


# This variable is a dictionary that contains all subsystems.
# Subsystems are automatically placed in here upon creation
# unless otherwise specified (See subsystem-base for the code).
subsystem_pool = {}


def add(subsys, overwrite=False):
    if subsys.name in subsystem_pool and overwrite is False:
        raise KeyError(
            'Subsystem with key %s already exists in the pool!'
            % (subsys.name))

    subsystem_pool[subsys.name] = subsys
    print('Subsystem added to pool: %s' % (subsys.name))


def remove(subsys):
    if isinstance(subsys, subsystem.Subsystem):
        subsys = subsys.name

    if not isinstance(subsys, str):
        raise TypeError("Provided subsystem removal key is an invalid type!")

    if subsys in subsystem_pool:
        subsystem_pool.pop(subsys)
    else:
        raise KeyError("Subsystem removal key not found in the pool!")


def get(name):
    if name in subsystem_pool.keys():
        return subsystem_pool[name]
    else:
        raise KeyError("No key %s found in subsystem pool!" % (name))


def get_all():
    return subsystem_pool


def stop_all():
    print("Closing all subsystems.")
    for subsys in subsystem_pool.values():
        if subsys.running:
            subsys.stop()
