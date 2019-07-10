        # self.sensFrame2 = QFrame(self)
        # self.sensDataContainer = QVBoxLayout(self.sensFrame2)
        #
        # self.sensorG = QGridLayout()
        #
        # self.sensorG.addWidget(QLabel("NOW"), 0, 1)
        # self.sensorG.addWidget(QLabel("30min"), 0, 2)
        # self.sensorG.addWidget(QLabel("1hr"), 0, 3)
        # self.sensorG.addWidget(QLabel("2hr"), 0, 4)
        #
        # self.sensorG.addWidget(QLabel("Temp: "), 1, 0)
        # self.sensorG.addWidget(QLabel("Hum: "), 2, 0)
        # self.sensorG.addWidget(QLabel("ATP: "), 3, 0)
        #
        # try:
        #     self.sensdataT = QLabel(fetch_sens.temp)
        #     # self.sensdataT.setAlignment(Qt.AlignHCenter)
        #     self.sensorG.addWidget(self.sensdataT, 1, 1)
        #
        #     self.sensdataH = QLabel(fetch_sens.hum)
        #     self.sensorG.addWidget(self.sensdataH, 2, 1)
        #
        #     self.sensdataA = QLabel(fetch_sens.atp)
        #     self.sensorG.addWidget(self.sensdataA, 3, 1)
        #
        #     self.sensgridTemp30 = QLabel(fetch_sens.max30temp)
        #     self.sensorG.addWidget(self.sensgridTemp30, 1, 2)
        #
        #     self.sensgridTemp60 = QLabel(fetch_sens.max60temp)
        #     self.sensorG.addWidget(self.sensgridTemp60, 1, 3)
        #
        #     self.sensgridTemp120 = QLabel(fetch_sens.max120temp)
        #     self.sensorG.addWidget(self.sensgridTemp120, 1, 4)
        #
        #     self.sensgridHum30 = QLabel(fetch_sens.max30hum)
        #     self.sensorG.addWidget(self.sensgridHum30, 2, 2)
        #
        #     self.sensgridHum60 = QLabel(fetch_sens.max60hum)
        #     self.sensorG.addWidget(self.sensgridHum60, 2, 3)
        #
        #     self.sensgridHum120 = QLabel(fetch_sens.max120hum)
        #     self.sensorG.addWidget(self.sensgridHum120, 2, 4)
        #
        #     self.sensgridatp30 = QLabel(fetch_sens.max30atp)
        #     self.sensorG.addWidget(self.sensgridatp30, 3, 2)
        #
        #     self.sensgridatp60 = QLabel(fetch_sens.max60atp)
        #     self.sensorG.addWidget(self.sensgridatp60, 3, 3)
        #
        #     self.sensgridatp120 = QLabel(fetch_sens.max120atp)
        #     self.sensorG.addWidget(self.sensgridatp120, 3, 4)
        #
        #     gps = "Lat: " + fetch_gps.lat + " Lon: " + fetch_gps.long
        #     self.sensgridgps = QLabel(gps)
        #     self.sensorG.addWidget(self.sensgridgps, 5, 0, 1, 4)
        #
        #     gps2 = "Alt: " + fetch_gps.alt + " Time: " + fetch_gps.gps_timestamp
        #     self.sensgridgps2 = QLabel(gps2)
        #     self.sensorG.addWidget(self.sensgridgps2, 6, 0, 1, 4)
        #
        # except Exception as e:
        #     print(repr(e))
        #
        # self.sensDataContainer.addLayout(self.sensorG)
        # self.windContainer.addWidget(self.sensFrame2)
