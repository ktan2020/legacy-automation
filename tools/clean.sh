#!/bin/sh
find . -name *.pyc -o -name __pycache__ | xargs rm -rf
