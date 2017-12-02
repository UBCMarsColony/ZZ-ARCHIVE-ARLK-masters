# The LightScheme dict object contains data about how to turn lights on and off.
# It is limited to keys defined in the _keys variable
class LightScheme(dict):

    # ALL VALID LIGHT SCHEME KEYS MUST BE INCLUDED IN THE ARRAY BELOW
    _keys = ["OVERHEAD_1", "OVERHEAD_2", "DOOR_COLN1", "DOOR_MARS1"]

    #LightScheme constructor
    def __init__(self, val_type=int):
        for key in LightScheme._keys:
            self[key] = val_type()

    #Modifies default dict element assignment to ensure the specified key is valud
    def __setitem__(self, key, val):
        if key not in LightScheme._keys:
            raise KeyError
        dict.__setitem__(self, key, val)
	
    #Returns the index associated with the key, assuming it is valid
    def get_gpio(self, key):
        if key not in LightScheme._keys:
            raise KeyError
        return LightScheme._keys.index(key)
	
    #Return the list of valid keys
    def get_keys(self):
        return LightScheme._keys