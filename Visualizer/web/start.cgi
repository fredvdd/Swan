#!/bin/sh
echo Content-type: text/plain
echo

set $PWD pwd
export PYTHONPATH=$PYTHONPATH:$PWD
/usr/bin/python start.py