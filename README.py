conda create -n eventcamera python=3.10
pip install dv_processing
pip install numpy==1.26.4

sudo gedit /etc/udev/rules.d/davis-camera.rules

SUBSYSTEM=="usb", ATTR{idVendor}=="152a", ATTR{idProduct}=="841a", MODE="0666"

Bus 002 Device 003: ID 152a:841a Thesycon Systemsoftware & Consulting GmbH INI DAViS FX3
Bus 002 Device 002: ID 152a:841a Thesycon Systemsoftware & Consulting GmbH INI DAViS FX3

reboot

左眼：DAVIS346_00001055
右眼：DAVIS346_00001054