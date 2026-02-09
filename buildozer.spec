[app]

# (str) Title of your application
title = Sudoku 3D

# (str) Package name
package.name = sudoku3d

# (str) Package domain (needed for android/ios packaging)
package.domain = com.sudoku

# (str) Source code where the main.py live
source.dir = .

# (str) Entry point (main file)
# This specifies main_mobile.py as the entry point for mobile version
# It will default to Chinese language
# For English version, run: python main_mobile.py en
source.main_py = main_mobile.py

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,txt,md

# (str) Application versioning (method 1)
version = 2.1

# (str) Presplash of the application
#presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
#icon.filename = %(source.dir)s/data/icon.png

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3==3.9.13,pygame==2.1.0,cython==0.29.33

# (str) Supported orientation (landscape, sensorLandscape, portrait or sensorPortrait)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 1

# (list) Permissions
android.permissions = INTERNET,WAKE_LOCK

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (bool) Use --private data storage (True) or --dir public storage (False)
android.private_storage = True

# (str) Android SDK build-tools version to use
android.build_tools_version = 33.0.2

# (bool) If True, then automatically accept SDK license
android.accept_sdk_license = True

# (str) Android logcat filters to use
android.logcat_filters = *:S python:D

# (bool) Copy library instead of making a libpymodules.so
android.copy_libs = 1

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.archs = arm64-v8a,armeabi-v7a

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1






