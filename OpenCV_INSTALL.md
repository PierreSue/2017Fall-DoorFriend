# Installing OpenCV
Here we describe our method of installing OpenCV on RPi. You need at least 16GB of SD Card.
Note: if you only want to install the Python binding for either Python 2.7 or Python 3, edit the following commands and remove the versions you dont't want.

Reference: <https://www.pyimagesearch.com/2017/09/04/raspbian-stretch-install-opencv-3-python-on-your-raspberry-pi/>

The swap file size is too small to compile OpenCV. We need to expand it first.

    sudo nano /etc/dphys-swapfile
    
Set

    CONF_SWAPSIZE=1024
    
Then, restart the swap file service.

    sudo /etc/init.d/dphys-swapfile restart

Now, update the existing softwares.

    sudo apt update
    sudo apt upgrade
    
Install the required packages.

    sudo apt-get install build-essential cmake pkg-config libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev
    sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev
    sudo apt-get install libatlas-base-dev gfortran python2.7-dev python3-dev
    sudo apt-get install python-numpy python3-numpy
    
Download and extract OpenCV packages. You can change the URLs to the latest version.

    wget -O opencv.tar.gz https://github.com/opencv/opencv/archive/3.4.0.tar.gz
    wget -O opencv_contrib.tar.gz https://github.com/opencv/opencv_contrib/archive/3.4.0.tar.gz
    tar xvf opencv.tar.gz
    tar xvf opencv_contrib.tar.gz
    
Create a temporary build directory under OpenCV source code.

    cd opencv-3.4.0
    mkdir build
    cd build
    
Run configuration script.

    cmake -D CMAKE_BUILD_TYPE=RELEASE \
          -D CMAKE_INSTALL_PREFIX=/usr/local \
          -D INSTALL_PYTHON_EXAMPLES=ON \
          -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib-3.4.0/modules \
          -D BUILD_EXAMPLES=ON ..

After the configuration has finished, check the output of the script, making sure that the Python and numpy pathes are recognized correctly.
Now compile OpenCV. This takes about 2 hours.

    make -j4
    
Install OpenCV.

    sudo make install
    sudo ldconfig
    
Test your OpenCV installation.

    python
    import cv2
    print(cv2.__version__)

Reset your swap file size.

    sudo nano /etc/dphys-swapfile
    
Set

    CONF_SWAPSIZE=100
    
Restart the service.

    /etc/init.d/dphys-swapfile restart
