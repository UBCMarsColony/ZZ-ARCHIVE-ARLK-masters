
subsys_pool = {}
    
def add(subsys, overwrite=False):
    if subsys.name not in subsys_pool or overwrite is True:
        subsys_pool[subsys.name] = subsys
    else:
        print("WARNING: Key <" + subsys.name + "> already exists in the subsystem pool. Entry skipped.")

def stop_all():
    print("Closing all subsystems.")
    for subsys in subsys_pool.values():
        subsys.join()