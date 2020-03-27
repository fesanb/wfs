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

printf  '\e[93m - Install mariaDB \n'
apt install mariadb-server
printf  '\e[93m - Setting up the database \n'
# If /root/.my.cnf exists then it won't ask for root password
if [ -f /root/.my.cnf ]; then
	mysql -e "CREATE DATABASE wfs /*\!40100 DEFAULT CHARACTER SET utf8 */;"
	mysql -e "show databases;"
	mysql -e "CREATE USER wfs@localhost IDENTIFIED BY 'wfs22';"
	mysql -e "GRANT ALL PRIVILEGES ON wfs.* TO 'wfs'@'localhost';"
	mysql -e "FLUSH PRIVILEGES;"
	mysql wfs < wfs_dump.sql

printf  '\e[92m - Database set up done. \n'
printf  '\e[93m - Install PIP \n'
apt install pip3
printf  '\e[92m - Done. \n'

printf  '\e[93m - Install needed Python3 packages \n'
pip3 install bme680
pip3 install mysql-connector-python
pip3 install numpy
pip3 install pynmea2
pip3 install pyqt5
pip3 install pyqtgraph
pip3 install rpi.gpio
pip3 install psutil
pip3 install threading
pip3 install pyserial

printf  '\e[92m - Installation successful \n'
