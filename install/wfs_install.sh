#!/bin/bash
printf  '\e[93m Copying service files to /lib/systemd/system/'

cp wfs.log.anemo.service /lib/systemd/system/
cp wfs.log.bme680.service /lib/systemd/system/
cp wfs.log.gps.service /lib/systemd/system/
cp wfs.service /lib/systemd/system/

printf  '\e[92m - Done! \n'
printf  '\e[93m Enabling Services'

systemctl enable /lib/systemd/system/wfs.log.anemo.service
systemctl enable /lib/systemd/system/wfs.log.bme680.service
systemctl enable /lib/systemd/system/wfs.log.gps.service
systemctl enable /lib/systemd/system/wfs.service

printf  '\e[92m - Done! \n'

#printf  '\e[93m - Install mariaDB-Server \n'
#apt install mariadb-server
#printf  '\e[92m - Done! \n'
#
#printf  '\e[93m - Install pip3 \n'
#apt install pip3
#printf  '\e[92m - Done! \n'
#
#pip3 install bme680
#pip3 install mysql-connector-python
#pip3 install numpy
#pip3 install pynmea2
#pip3 install pyqt5
#pip3 install pyqtgraph
#pip3 install rpi.gpio

printf  '\e[92m - Installation successful \n'

