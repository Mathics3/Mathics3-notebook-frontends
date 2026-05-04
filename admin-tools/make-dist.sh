#!/bin/bash
PACKAGE=mathics3_notebook_frontends

# FIXME put some of the below in a common routine
function finish {
  cd $mathics3_notebook_frontends_owd
}

cd $(dirname ${BASH_SOURCE[0]})
mathics3_notebook_frontends_owd=$(pwd)
trap finish EXIT

if ! source ./pyenv-versions ; then
    exit $?
fi

cd ..
source mathics3_kernel/frontend/version.py

echo $__version__

pyversion=3.14
if ! pyenv local $pyversion ; then
    exit $?
fi
rm -fr build
python -m build --wheel
python -m build --sdist
finish
