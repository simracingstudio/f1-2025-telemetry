#! /bin/sh

set -e

if [ -n $LOCAL_PYTHON3_BIN ] ; then
    export PATH=$LOCAL_PYTHON3_BIN:$PATH
fi

# Clean up
rm -rf build dist f1_2020_telemetry.egg-info

python3 setup.py sdist bdist_wheel

# Clean up everything except wheel file
rm -rf build f1_2020_telemetry.egg-info

# Show contents of wheel file
unzip -v dist/*.whl
