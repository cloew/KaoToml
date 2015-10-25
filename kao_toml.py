from kao_dict import KaoDict
from kao_decorators import lazy_property, proxy_for

from collections.abc import Mapping, Sequence
import pytoml

@proxy_for('_toml', ['__iter__', '__contains__', '__len__', '__getitem__', '__setitem__', '__delitem__'])
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
            
    def _wrap(self, value):
        """ Wrap the value """
        if isinstance(value, Mapping):
            return self._wrapDict(value)
        elif isinstance(value, Sequence) and not isinstance(value, str) and not isinstance(value, bytes):
            return self._wrapList(value)
        else:
            return value
        
    def _wrapDict(self, d):
        """ Wrap the dictionary """
        return KaoDict({key:self._wrap(value) for key, value in d.items()})
        
    def _wrapList(self, l):
        """ Wrap the list """
        return [self._wrap(v) for v in l]
            
    def _collapse(self, value):
        """ Collapse the value """
        if isinstance(value, Mapping):
            return self._collapseDict(value)
        elif isinstance(value, Sequence) and not isinstance(value, str) and not isinstance(value, bytes):
            return self._collapseList(value)
        else:
            return value
        
    def _collapseDict(self, d):
        """ Wrap the dictionary """
        return {key:self._collapse(value) for key, value in d.items()}
        
    def _collapseList(self, l):
        """ Wrap the list """
        return [self._collapse(v) for v in l]
            
            
            
        collapsedDict = {}
        for key, value in d.items():
            if type(value) is KaoDict:
                collapsedDict[key] = self._collapse(value)
            else:
                collapsedDict[key] = value
        
        return collapsedDict