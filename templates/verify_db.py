import sys
import importlib

print('Python executable:', sys.executable)
print('Working dir:', __file__)

# show import paths
print('sys.path (first 5):', sys.path[:5])

# Try importing the root ext and models
try:
    import ext
    from ext import db as db_root
    import models
    print('imported ext from:', ext.__file__)
    print('id(db_root):', id(db_root))
    print('models module:', models.__file__)
    # if models imported ext.db, show that id too
    try:
        print('models.db id:', id(models.db))
    except Exception as e:
        print('could not read models.db id:', e)
except Exception as e:
    print('Failed to import root ext/models:', repr(e))
    raise


    import importlib.util, os
 
    try:
        import templates.ext as templ_ext
        print('imported templates.ext from:', templ_ext.__file__)
        print('templates.ext.db id:', id(templ_ext.db))
        print('root == templates.ext?', id(db_root) == id(templ_ext.db))
    except Exception as e:
       
        templ_path = os.path.join(os.path.dirname(__file__), 'templates', 'ext.py')
        if os.path.exists(templ_path):
            spec = importlib.util.spec_from_file_location('templates_ext_from_path', templ_path)
            templ_ext2 = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(templ_ext2)
            print('loaded templates/ext.py by path:', templ_path)
            print('templates_ext_from_path.db id:', id(templ_ext2.db))
            print('root == templates_ext_from_path?', id(db_root) == id(templ_ext2.db))
        else:
            print('templates/ext.py not found on disk at', templ_path)
except Exception as e:
    print('templates.ext import/load attempt failed:', repr(e))