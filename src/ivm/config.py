#Global Imports
from json import dump as jsonDump, dumps as jsonDumps, load as jsonLoad
import os
from os import path
from debug_utils import LOG_CURRENT_EXCEPTION

class _Config(object):
    
    def __init__(self):
        self.enabled = True
        self.debug = True
        self.Cdebug = False
        self.confdata = {'enabled': True,
         'debug': False}
        self.cdata = jsonDumps(self.confdata, indent=4, sort_keys=True)

_config = _Config()

def _makeconfig():
    data = {}
    if _config.confdata:
        if _config.Cdebug:
            print '[IVM] _config.confdata found'
        try:
            os.makedirs('./mods/configs/IVM')
        except:
            pass
        with open(_FILE_, 'w') as json_file:
            jsonDump(_config.confdata, json_file, separators=(',', ': '), indent=4, sort_keys=True)
            json_file.write('\n')
            if _config.debug:
                print '[IVM] New Config file created from default settings!'
                print '[IVM] IVM config file can be found at {default wot folder}\\mods\\configs\\IVM\\fire.json'
    else:
        if _config.Cdebug:
            print '[IVM] _config.confdata not found'
        if _config.debug:
            print '[IVM] Python file corrupted REDOWNLOAD MOD!!!!!'

def _chkfile():
    if path.exists(_FILE_):
        if _config.Cdebug:
            print '[IVM] config file found'
        with open(_FILE_) as f:
            data = jsonLoad(f)
            _config.enabled = data['enabled']
            if data['debug']:
                _config.debug = True
            else:
                _config.debug = False
    else:
        if _config.debug:
            print '[IVM] config file not found creating one...'
        _makeconfig()

_chkfile()