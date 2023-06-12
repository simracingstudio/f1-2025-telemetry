#! /bin/sh

set -e

if [ -n $LOCAL_PYTHON3_BIN ] ; then
    export PATH=$LOCAL_PYTHON3_BIN:$PATH
fi


pip3 uninstall -y f1-2023-telemetry

pip3 install dist/*.whl
