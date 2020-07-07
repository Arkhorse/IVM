from utils import CORE, overrideMethod
#####################################################################
# imports

import traceback

import base64
import debug_utils
from account_helpers.CustomFilesCache import CustomFilesCache


@overrideMethod(CustomFilesCache, '_CustomFilesCache__onReadLocalFile')
def _CustomFilesCache__onReadLocalFile(base, self, url, showImmediately):
    try:
        base(self, url, showImmediately)
    except EOFError:
        print('CustomFilesCache.__onReadLocalFile: url="{0}"'.format(url))
        print(traceback.format_exc())
        try:
            print('Attempt to reload url: {0}'.format(url))
            del(self._CustomFilesCache__db[base64.b32encode(url)])
            base(self, url, showImmediately)
        except Exception:
            print(traceback.format_exc())
