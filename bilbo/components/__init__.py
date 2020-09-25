import os, os.path
import importlib
import warnings

def load_components():
    d = os.path.join(os.getcwd(), 'bilbo/components')
    components = dict()
    for f in os.listdir(d):
        if f.startswith('__'):
            continue
        mode_dir = os.path.join(d, f)
        if os.path.isdir(mode_dir):
            pkg = importlib.import_module('bilbo.components.%s' % f)
            mode_info = {'pkg': pkg,
                         'run':lambda : importlib.import_module('.__main__',
                                                                pkg.__name__)}
            components[f] = mode_info
    return components
