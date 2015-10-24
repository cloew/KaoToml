from kao_dict import KaoDict
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
        return self._wrap(data)
        
    def save(self):
        """ Save the TOML file """
        with open(self._filename, 'w') as f:
            pytoml.dump(f, self._collapse(self._toml))
            
    def __getattr__(self, attr):
        """ Return the value for the given attr """
        if attr in self.INSTANCE_ATTRS:
            raise AttributeError(attr)
        return getattr(self._toml, attr)
        
    def __setattr__(self, attr, value):
        """ Return the value for the given attr """
        if attr in self.INSTANCE_ATTRS:
            object.__setattr__(self, attr, value)
        else:
            setattr(self._toml, attr, value)
            
    def _wrap(self, d):
        """ Wrap the given dictionary in a KaoDict """
        wrappedDict = {}
        for key, value in d.items():
            if type(value) is dict:
                wrappedDict[key] = self._wrap(value)
            else:
                wrappedDict[key] = value
        
        return KaoDict(wrappedDict)
            
    def _collapse(self, d):
        """ Wrap the given dictionary in a KaoDict """
        collapsedDict = {}
        for key, value in d.items():
            if type(value) is KaoDict:
                collapsedDict[key] = self._collapse(value)
            else:
                collapsedDict[key] = value
        
        return collapsedDict