# MBPluginLoader
Load C++ Plugins from a Python Project at MotionBuilder Startup.

<br>

## Platform
- Motionbuilder : 2020 or above
- OS : Windows

<br>

## Installation
### Method 1: Install via mobupy & pip

1. Open a terminal as an administrator.

2. Run the following command, replacing the path with your MotionBuilder installation directory:

    ```
    path/to/MotionBuilder<version>/bin/x64/mobupy.exe -m pip install mbpluginloader
    ```

**Note:** Only works with MotionBuilder 2022 and later.

<br>

### Method 2: Manual Install
This method is mainly intended for developers who want to bundle mbpluginloader directly within their own projects or tools (i.e., as a third-party library).

1. Go to the [GitHub Releases page](https://github.com/Ndgt/MBPluginLoader/releases).

2. Download the source code `.zip` file for the latest release.

3. Extract the archive. You will find a `src/mbpluginloader` directory inside.

4. Copy the `mbpluginloader` directory into your own project's source tree.

5. You can now import it in your project using `from mbpluginloader import ...`.

    ```
    Project directory
    ├── your modules 
    ├── ...
    └── mbpluginloader  <- downloaded from Git Release
    ```

<br>

## Reference

#### `load_plugins(path_or_dir)`
Loads a C++ plugin (`.dll`) from a specified file path or all plugins within a directory.

* **path_or_dir** (`str`): The absolute or relative path to a single `.dll` file or a directory containing `.dll` files.

<br>

#### `log(level, format_string, *args)`
Prints a formatted log message to the MotionBuilder console.

* **level** (`str`): The log level (e.g., "Info", "Error").
* **format_string** (`str`): A message template containing `{}` placeholders.
* **\*args**: Values to be inserted into the placeholders in `format_string`.

<br>

## Development
### Requirements
- **Visual Studio Build Tools & "Desktop development with C++" workload**

    - MSVC v143 - VS 2022 C++ x64/x86 build tool : MotionBuilder 2024 ~
    - MSVC v142 - VS 2019 C++ x64/x86 build tool : MotionBuilder 2022, 2023
    - MSVC v141 - VS 2017 C++ x64/x86 build tool : MotionBuilder 2020

<br>

### Building from source
1. Open a terminal as an administrator.

    Set the Visual Studio environment variables using **`vcvarsall.bat`**, which is typically located at:
    `C:/Program Files (x86)/Microsoft Visual Studio/2022/BuildTools/VC/Auxiliary/Build`.

    ```cmd
    path/to/vcvarsall.bat x64 [-vcvars_ver=<version>]
    ```

    Use `-vcvars_ver=14.29` for VS2019 or `-vcvars_ver=14.16` for VS2017.
    See the [Microsoft documentation](https://learn.microsoft.com/en-us/cpp/build/building-on-the-command-line?view=msvc-170#vcvarsall) for more details.


<br>

2. Clone this repository.

    ```cmd
    git clone https://github.com/Ndgt/MBPyPluginLoader.git
    cd MBPyPluginLoader
    ```

<br>

3. Edit the user-specific variables in `CMakeLists.txt` according to your environment.

    ```CMake
    # === Environment-specific user configuration ===
    set(PRODUCT_VERSION 2026)
    set(MOBU_ROOT "C:/Program Files/Autodesk/MotionBuilder ${PRODUCT_VERSION}")
    ```

<br>

4. Build.

    ```
    cd src
    cmake -S . -B build -G "Ninja" -DCMAKE_BUILD_TYPE=Release
    cmake --build build
    ```

<br>

### Notes
- `FBSystem().Version` returns float version value formatted as `xx000.0`

    For example, in MotionBuilder 2024, this returns  `24000.0`.

<br>

- This module uses Boost.Python to call the `FBSystem::LibraryLoad()` function from the C++ SDK, which is not exposed in the Python SDK.

