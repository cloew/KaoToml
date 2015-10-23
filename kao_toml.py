from kao_decorators import lazy_property
import pytoml

class KaoToml(object):
    """ Represents a Toml file """
    INSTANCE_ATTRS = {'_filename', '___toml'}
    
    def __init__(self, filename):
        """ Initialize with the TOML file to wrap """
        self._filename = filename
        
    @lazy_property
    def _toml(self):
        """ Return the toml dictionary from the file """
        data = {}
        with open(self._filename, 'rb') as f:
            data = pytoml.load(f)
        return data
        
    def save(self):
        """ Save the TOML file """
        with open(self._filename, 'w') as f:
            pytoml.dump(f, self._toml)
            
    def __getattr__(self, attr):
        """ Return the value for the given attr """
        if attr in self.INSTANCE_ATTRS:
            raise AttributeError(attr)
        return self._toml[attr]
        
    def __setattr__(self, attr, value):
        """ Return the value for the given attr """
        if attr in self.INSTANCE_ATTRS:
            object.__setattr__(self, attr, value)
        else:
            self._toml[attr] = value
            