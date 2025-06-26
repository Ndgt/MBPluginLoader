import os
import sys
import importlib
from pyfbsdk import FBSystem, FBTrace

def log(level, format_string, *args):
    """
    A helper function to format and print log messages.
    """
    message = format_string.format(*args)
    FBTrace("[mbpluginloader] {}: {}\n".format(level, message))

def _get_pyd_module():
    """
    Loads and caches the version-specific mbpluginloader.pyd module.
    It finds the module in a version-named directory.
    """
    if hasattr(_get_pyd_module, "cached_module"):
        return _get_pyd_module.cached_module

    pyd_module = None
    try:
        # --- Determine version directory ---
        version_str = ""
        try:
            # Get version string like "22000", "23000", etc.
            version_str = str(int(FBSystem().Version))
        except (ValueError, TypeError):
            pass # Fails silently, version_str remains empty

        if not version_str:
            log("Error", "Could not determine a valid MotionBuilder version.")
        else:
            # --- Find and import the module from the version-specific directory ---
            module_path = os.path.dirname(os.path.abspath(__file__))
            pyd_root_path = os.path.join(module_path, "pyd")
            version_specific_path = os.path.join(pyd_root_path, version_str)

            if not os.path.isdir(version_specific_path):
                log("Error", "Version-specific directory not found: {}", version_specific_path)
            else:
                if version_specific_path not in sys.path:
                    sys.path.insert(0, version_specific_path)
                
                # Import the module with a fixed name
                pyd_module = importlib.import_module("mbpluginload")

    except Exception as e:
        log("Error", "Failed to initialize the loader. {}", e)
        pyd_module = None # Ensure module is None on unexpected exception
    
    # Cache the result (module or None)
    _get_pyd_module.cached_module = pyd_module
    return pyd_module

def _load_single_dll(pyd_module, full_path):
    """
    Loads a single DLL file and logs the outcome.
    """
    filename = os.path.basename(full_path)
    log("Info", "Attempting to load: {}", filename)
    try:
        if pyd_module.load(full_path):
            log("Info", "Successfully loaded: {}", filename)
        else:
            log("Error", "Failed to load: {}", filename)
    except Exception as e:
        log("Error", "loading {}: {}", filename, e)

def load_plugins(path_or_dir):
    """
    Loads plugins from a specified path or directory.
    """
    pyd_module = _get_pyd_module()
    if not pyd_module:
        log("Error", "Cannot load plugins, the core module is not available.")
        return

    path_or_dir = os.path.abspath(path_or_dir)
    if not os.path.exists(path_or_dir):
        log("Error", "The specified path does not exist: {}", path_or_dir)
        return

    # if path specified
    if os.path.isfile(path_or_dir):
        filename = os.path.basename(path_or_dir)
        if path_or_dir.lower().endswith(".dll"):
            _load_single_dll(pyd_module, path_or_dir)
        else:
            log("Warning", "Specified file is not a .dll, skipping: {}", filename)

    # if directory specified
    elif os.path.isdir(path_or_dir):
        dll_files = [f for f in os.listdir(path_or_dir) if f.lower().endswith(".dll")]
        if not dll_files:
            log("Info", "No .dll files found in directory: {}", path_or_dir)
            return
        
        for filename in dll_files:
            full_path = os.path.join(path_or_dir, filename)
            _load_single_dll(pyd_module, full_path)
            
    else:
        log("Error", "The specified path is not a valid file or directory: {}", path_or_dir)