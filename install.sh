#!/bin/sh

sudo apt-get update
sudo apt-get install -y build-essential yasm pkg-config libvpx1 libpq-dev libjpeg-dev unzip autoconf libtool

wget http://download.videolan.org/pub/x264/snapshots/last_x264.tar.bz2 -O - | tar -xjf -
cd x264-snapshot*
./configure --enable-static --disable-opencl
make
sudo make install
cd ..

wget -O fdk-aac.zip https://github.com/mstorsjo/fdk-aac/zipball/master
unzip fdk-aac.zip
cd mstorsjo-fdk-aac*
autoreconf -fiv
./configure --enable-static
make
sudo make install
cd ..

wget https://www.ffmpeg.org/releases/ffmpeg-snapshot-git.tar.bz2 -O - | tar -xjf -
cd ffmpeg
./configure --disable-doc --disable-ffserver --enable-nonfree --enable-gpl --enable-libfdk_aac --enable-libx264
make
sudo make install
make clean
cd ..

sudo ldconfig
