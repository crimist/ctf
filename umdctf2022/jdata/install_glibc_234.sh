# GLIBC version (2.34) is so bleeding edge even my Debian testing was out of date (2.33).

wget http://mirrors.ocf.berkeley.edu/gnu/libc/glibc-2.34.tar.gz
tar zxvf glibc-2.34.tar.gz
cd glibc-2.34
mkdir build
cd build
../configure --prefix=/opt/glibc-2.34
make -j 12
sudo make install

gdb --args /opt/glibc-2.34/lib/ld-linux-x86-64.so.2 --library-path /opt/glibc-2.34/lib/ ./jdata.zip
