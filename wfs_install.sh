#!/bin/bash
echo "dtoverlay=pi3-disable-bt" | sudo tee -a /boot/config.txt # Disable Bluetooth
echo "disable_splash=1" | sudo tee -a /boot/config.txt # Disable Bluetooth
systemctl disable hciuart # Free up UART to allow serial communication with GPS.

printf  '\e[93m Copying service files to /lib/systemd/system/ \e[0m \n'
cp service-timer/wfs.mean.service /lib/systemd/system/
cp service-timer/wfs.mean.timer /lib/systemd/system/
cp service-timer/wfs.log.anemo.service /lib/systemd/system/
cp service-timer/wfs.log.bme680.service /lib/systemd/system/
cp service-timer/wfs.log.bme680.timer /lib/systemd/system/
cp service-timer/wfs.log.gps.service /lib/systemd/system/
cp service-timer/wfs.log.gps.timer /lib/systemd/system/
cp service-timer/wfs.service /lib/systemd/system/
cp service-timer/wfs.clean.service /lib/systemd/system/
cp service-timer/wfs.clean.timer /lib/systemd/system/
printf  '\e[92m - Done! \e[0m \n'

printf  '\e[93m Setting a new splash image \e[0m \n' # Better way is to change plymouth theme with custom one.
cp install/splash.png /usr/share/plymouth/themes/pix/
printf  '\e[92m - Done! \e[0m \n'

printf  '\e[93m Enabling Services \e[0m \n'
systemctl enable /lib/systemd/system/wfs.mean.timer
systemctl enable /lib/systemd/system/wfs.log.anemo.service
systemctl enable /lib/systemd/system/wfs.log.bme680.timer
systemctl enable /lib/systemd/system/wfs.log.gps.timer
systemctl enable /lib/systemd/system/wfs.service
systemctl enable /lib/systemd/system/wfs.clean.timer
printf  '\e[92m - Done! \e[0m \n'

printf  '\e[93m - Install mariaDB \e[0m \n'
apt install mariadb-server
printf  '\e[93m - Setting up the database \e[0m \n'
mysql -e "CREATE DATABASE IF NOT EXISTS wfs /*\!40100 DEFAULT CHARACTER SET utf8 */;"
mysql -e "show databases;"
mysql -e "CREATE USER IF NOT EXISTS wfs@localhost IDENTIFIED BY 'wfs22';"
mysql -e "GRANT ALL PRIVILEGES ON wfs.* TO 'wfs'@'localhost';"
mysql -e "FLUSH PRIVILEGES;"
mysql wfs < wfs_dump.sql
mysql -e "SHOW TABLES FROM wfs;"
read -r
printf  '\e[92m - Database set up done. \e[0m \n'

printf  '\e[93m - Install PyQT6 \e[0m \n'
pip install pythpyqt6 -y
printf  '\e[92m - Done. \e[0m \n'


printf  '\e[93m - Install needed Python3 packages \e[0m \n'
pip3 install bme680
pip3 install mysql-connector-python
pip3 install numpy
pip3 install pynmea2
pip3 install pyqtgraph
pip3 install rpi.gpio
pip3 install psutil
pip3 install pyserial

printf  '\e[92m - Installation successful \e[0m \n'
