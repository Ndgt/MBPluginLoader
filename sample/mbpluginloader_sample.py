# Make Sure this file is in the PythonStartup Path

import os

# import mbpluginloader
from mbpluginloader import load_plugins, log

try:
    # sample directory structure
    project_path = os.path.dirname(os.path.abspath(__file__))
    plugins_directory = os.path.join(project_path, "plugins")

    if os.path.exists(plugins_directory):
        # Example 1: Load all DLLs in the specified directory
        load_plugins(plugins_directory)

        # Example 2: Load a specific DLL file (uncomment to use)
        # my_specific_plugin = os.path.join(plugins_directory, "custom_plugin.dll")
        # load_plugins(my_specific_plugin)

    else:
        log("Warning", "Plugins directory not found at '{}'", plugins_directory)

except ImportError:
    log("Error", "Could not import 'mbpluginloader'. Check sys.path and file locations.")
except Exception as e:
    log("Error", "An error occurred: {}", e)