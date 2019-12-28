#!/bin/bash
echo copying service files to /lib/systemd/system/

cp wfs.log.anemo.service /lib/systemd/system/
cp wfs.log.bme680.service /lib/systemd/system/
cp wfs.log.gps.service /lib/systemd/system/
cp wfs.service /lib/systemd/system/

echo Copying done
echo Enabling services:

systemctl enable /lib/systemd/system/wfs.log.anemo.service
systemctl enable /lib/systemd/system/wfs.log.bme680.service
systemctl enable /lib/systemd/system/wfs.log.gps.service
systemctl enable /lib/systemd/system/wfs.service

echo Services enabled
echo install mysql
apt install mariadb-server

