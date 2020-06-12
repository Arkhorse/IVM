# Python bytecode 2.7 (decompiled from Python 2.7)
# Embedded file name: scripts/client/gui/mods/vehicle_exp/config.py
# Compiled at: 2019-12-08 12:17:10
import codecs
import json
import os
import re
__all__ = ('ConfigProperty', 'AbstractConfig')

class ConfigProperty(object):

    def __init__(self, key, attribute='config', processerGet=None, processerSet=None):
        super(ConfigProperty, self).__init__()
        self.key = key
        self.attribute = attribute
        self.processerGet = processerGet
        self.processerSet = processerSet

    def __set__(self, instance, value):
        if self.processerSet:
            value = self.processerSet(value)
        getattr(instance, self.attribute)[self.key] = value
        instance.saveConfig()

    def __get__(self, instance, objtype=None):
        value = getattr(instance, self.attribute)[self.key]
        if self.processerGet:
            value = self.processerGet(value)
        return value


class AbstractConfig(object):

    def __init__(self, folder, filename):
        object.__init__(self)
        self.__folder = folder
        self.__filename = filename
        self.loadConfig()

    def getConfig(self):
        return {}

    def getConfigPath(self):
        path = os.path.join('mods', 'configs', self.__folder)
        if not os.path.exists(path):
            os.makedirs(path)
        return os.path.join(path, self.__filename + '.json')

    def saveConfig(self):
        with codecs.open(self.getConfigPath(), 'w', encoding='utf-8-sig') as file:
            data = jsonDump(self.getConfig(), True)
            file.write(data)

    def loadConfig(self):
        path = self.getConfigPath()
        if os.path.isfile(path):
            with codecs.open(path, 'r', encoding='utf-8-sig') as file:
                self.getConfig().update(jsonLoad(file))
        else:
            self.saveConfig()


def jsonDump(obj, needFmt=False):
    """Serializes an object into a string
    :param obj: Object
    :param needFmt: Indicates that the result should be formatted for human reading"""
    return json.dumps(obj, ensure_ascii=False, indent=4, separators=(',', ': '), sort_keys=True, encoding='utf-8') if needFmt else json.dumps(obj)


def jsonLoad(src):
    """Returns json data from source
    It supports comments in json
    :param src: Data source (file handler or string)"""
    if not isinstance(src, (str, unicode)):
        src = src.read()
    return jsonParse(src)


def jsonParse(data):
    """Pareses json string into dict
    It supports comments in json
    :param data: JSON string"""

    def comments(text):
        regex = '\\s*(#|\\/{2}).*$'
        regex_inline = '(:?(?:\\s)*([A-Za-z\\d\\.{}]*)|((?<=\\").*\\"),?)(?:\\s)*(((#|(\\/{2})).*)|)$'
        lines = text.split('\n')
        excluded = []
        for index, line in enumerate(lines):
            if re.search(regex, line):
                if re.search('^' + regex, line, re.IGNORECASE):
                    excluded.append(lines[index])
                elif re.search(regex_inline, line):
                    lines[index] = re.sub(regex_inline, '\\1', line)

        for line in excluded:
            lines.remove(line)

        return '\n'.join(lines)

    return byteify(json.loads(comments(data), encoding='utf-8'))


def byteify(data):
    """Encodes data with UTF-8
    :param data: Data to encode"""
    if isinstance(data, dict):
        return {byteify(key):byteify(data) for key, data in data.iteritems()}
    elif isinstance(data, list):
        return [ byteify(element) for element in data ]
    elif isinstance(data, unicode):
        return data.encode('utf-8')
    else:
        return data
