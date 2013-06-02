#!/bin/bash -xe

if [ $# -lt 2 ]; then
    echo 'Usage : jenkins_tests.sh <workspace> <python version>'
    exit 1
fi

WORKSPACE=$1
version=$2
PYENV_HOME=${WORKSPACE}/virtualenv

if [ -d ${PYENV_HOME} ]; then
    rm -rf ${PYENV_HOME}
fi

virtualenv --no-site-packages -p python${version} ${PYENV_HOME}
source ${PYENV_HOME}/bin/activate
pip install --quiet -r ${WORKSPACE}/requirements.txt
case "${version}" in
    2*) libraries='nosexcover unittest2';;
    3*) libraries='unittest2py3k git+https://github.com/cmheisel/nose-xcover.git';;
esac
pip install --quiet nose pylint mock ${libraries}
python ${WORKSPACE}/setup.py install
pylint -f parseable elohim | tee pylint.out
nosetests --with-xcoverage --with-xunit --cover-package=elohim --cover-erase --with-doctest
deactivate
