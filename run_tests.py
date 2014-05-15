import sys, os
CUR_DIR_PATH = os.getcwd()
sys.path.insert(0, CUR_DIR_PATH)
sys.path.insert(0, os.path.join(CUR_DIR_PATH, 'hamam'))

import unittest
from werkzeug.utils import import_string


MODULES = ['session']
suite = unittest.TestSuite()


if __name__ == '__main__':
    sys.argv, modules = sys.argv[:1], sys.argv[1:] or MODULES
    suite = unittest.TestSuite()
    for module in modules:
        if module not in MODULES:
            print 'Module %s is not registered, skipping.' % module
        else:
            mod = import_string('hamam.%s.tests' % module)
            suite.addTest(mod.suite())
    unittest.main(defaultTest='suite')
