#! /bin/sh

set -e

if [ -n $LOCAL_PYTHON3_BIN ] ; then
    export PATH=$LOCAL_PYTHON3_BIN:$PATH
fi

exec f1-2022-telemetry-recorder
