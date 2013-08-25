#!/bin/bash

MY_PATH="`dirname \"$0\"`"              # relative
MY_PATH="`( cd \"$MY_PATH\" && pwd )`"  # absolutized and normalized

VENV="$MY_PATH/venv"

cd $VENV

rm -rf src
mkdir src
cd src

wget http://oligarchy.co.uk/xapian/1.2.15/xapian-core-1.2.15.tar.gz
wget http://oligarchy.co.uk/xapian/1.2.15/xapian-bindings-1.2.15.tar.gz

tar -xzvf xapian-core-*
tar -xzvf xapian-bindings-*


export LD_LIBRARY_PATH=$VENV/lib

cd xapian-core-*
./configure --prefix=$VENV
make
make install

cd ../xapian-bindings-*
./configure --prefix=$VENV XAPIAN_CONFIG=$VENV/bin/xapian-config PYTHON=$VENV/bin/python PYTHON_LIB=$VENV/lib/python2.7 --with-python --without-ruby --without-php --without-tcl 
make
make install

# PIP version is 1.5, we need minimum 2.0.0 for XAPIAN 2
cd $VENV
wget https://raw.github.com/notanumber/xapian-haystack/master/xapian_backend.py
rm lib/python2.7/site-packages/xapian_backend.py
mv xapian_backend.py lib/python2.7/site-packages/xapian_backend.py
