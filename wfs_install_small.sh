#!/bin/bash

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
cp /install/splash.png /usr/share/plymouth/themes/pix/
printf  '\e[92m - Done! \e[0m \n'

printf  '\e[93m Enabling Services \e[0m \n'
systemctl enable /lib/systemd/system/wfs.mean.timer
systemctl enable /lib/systemd/system/wfs.log.anemo.service
systemctl enable /lib/systemd/system/wfs.log.bme680.timer
systemctl enable /lib/systemd/system/wfs.log.gps.timer
systemctl enable /lib/systemd/system/wfs.service
systemctl enable /lib/systemd/system/wfs.clean.timer
printf  '\e[92m - Done! \e[0m \n'
