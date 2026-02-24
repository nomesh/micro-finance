# Fix Django 1.11 compatibility with Python 3.8+
# This must be applied before Django is imported

import sys
import importlib.abc
import importlib.machinery

class DjangoPatcher(importlib.abc.MetaPathFinder, importlib.abc.Loader):
    def find_module(self, fullname, path=None):
        if fullname == 'django.contrib.admin.widgets':
            return self
        return None
    
    def load_module(self, fullname):
        if fullname in sys.modules:
            return sys.modules[fullname]
        
        # Load the module normally first
        spec = importlib.machinery.PathFinder.find_spec(fullname)
        module = importlib.util.module_from_spec(spec)
        sys.modules[fullname] = module
        
        # Patch the source code before execution
        import types
        original_exec = spec.loader.exec_module
        
        def patched_exec(mod):
            # Get the source and patch it
            source = spec.loader.get_source(fullname)
            if source and "'%s=%s' % (k, v) for k, v in params.items()," in source:
                source = source.replace(
                    "'%s=%s' % (k, v) for k, v in params.items(),",
                    "('%s=%s' % (k, v) for k, v in params.items()),"
                )
                code = compile(source, spec.origin, 'exec')
                exec(code, mod.__dict__)
            else:
                original_exec(mod)
        
        spec.loader.exec_module = patched_exec
        spec.loader.exec_module(module)
        
        return module

# Install the patcher
sys.meta_path.insert(0, DjangoPatcher())
