#Can be used for precision lighting later on.
class LightData():
    def __init__(self):
        red = 0
        blue = 0
        green = 0
        alpha = 0
        brightness = 0


# The LightPlan dict object contains data about how to turn lights on and off.
# It is limited to keys defined in the _keys variable
class LightPlan(dict):
    
    ###############--PLEASE NOTE--###############
    #
    # ALL VALID LIGHT SCHEME KEYS MUST BE INCLUDED IN THE STATIC ARRAY BELOW
    #
    #############################################    
    _keys = ["OVERHEAD_1", "OVERHEAD_2", "DOOR_COLN1", "DOOR_MARS1"]
    
    #LightPlan constructor
    def __init__(self):
        for key in LightPlan._keys:
            self[key] = "Undefined"
            
    #Modifies default dict element assignment to ensure the specified key is valid
    def __setitem__(self, key, val):
        if key not in LightPlan._keys:
            raise KeyError("LightPlan key " + str(key) + " is unregistered, so it couldn't be used.")
        dict.__setitem__(self, key, val)
    
    def __getitem__(self, key):
        if key not in LightPlan._keys:
            raise KeyError("LightPlan key " + str(key) + " is unregistered, so it couldn't be used.")
        return dict.__getitem__(self, val)
	
    
    #Returns the index associated with the key, or raises an error if the key is invalid
    @staticmethod
    def get_gpio(self, key):
        if key not in LightPlan._keys:
            raise KeyError("LightPlan key " + str(key) + " is unregistered, so it couldn't be used.")
        return LightPlan._keys.index(key)
	
    #Return the list of valid keys
    @staticmethod
    def get_keys(self):
        return LightPlan._keys        