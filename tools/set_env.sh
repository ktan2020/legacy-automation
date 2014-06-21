#!/bin/sh

# export TOOLCHAIN
export TOOLCHAIN=/opt/auto

# set PATH
export PATH=/usr/lib64/qt-3.3/bin:/usr/local/bin:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin

# export extern libs path
export PATH=$PATH

# export tools and interpreters path
export PATH=$TOOLCHAIN/tools:/usr/local/bin/java/bin:$PATH

# export PYTHONLIB path
export PYTHONPATH=$TOOLCHAIN/libs/py

# export JAVA_HOME
export JAVA_HOME=/usr/local/bin/java

# Oracle InstantClient
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH

echo PATH:$PATH