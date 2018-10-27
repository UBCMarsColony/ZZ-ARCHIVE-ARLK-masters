import importlib
subsystem = importlib.import_module('pi-systems_subsystem-base')


# This variable is a dictionary that contains all subsystems.
# Subsystems are automatically placed in here upon creation
# unless otherwise specified (See subsystem-base for the code).
subsys_pool = {}
    
def add(subsys, overwrite=False):
    if subsys.name not in subsys_pool or overwrite is True:
        subsys_pool[subsys.name] = subsys
    else:
        print("WARNING: Key <" + subsys.name + "> already exists in the subsystem pool. Entry skipped.")


def remove(subsys):
    if isinstance(subsys, subsystem.Subsystem):
        subsys_pool.pop(subsys.name)
    elif str(subsys) == subsys:
        subsys_pool.pop(subsys)
    else:
        raise ValueError("Invalid key parameter for subsystem retrieval!")


def get_all():
    return subsys_pool

        
def stop_all():
    print("Closing all subsystems.")
    for subsys in subsys_pool.values():
        subsys.join()