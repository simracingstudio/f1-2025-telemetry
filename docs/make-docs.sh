#! /bin/sh

set -e

if [ -n $LOCAL_PYTHON3_BIN ] ; then
    export PATH=$LOCAL_PYTHON3_BIN:$PATH
fi


# Start afresh
rm -rf source/generated build

# We won't use autodoc.
# Its documentation isn't really helpful, compared to just reading the sources.

#sphinx-apidoc --separate --no-toc --module-first -o source/generated ../f1_2020_telemetry

make html
