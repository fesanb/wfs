def mysql_fetch(self):
    while True:
        cnx = mysql.connector.connect(user='wfs', database='wfs', password='wfs22')
        cursor = cnx.cursor()

        get_wind = "SELECT * FROM wind WHERE id=(SELECT MAX(id) FROM wind)"
        cursor.execute(get_wind)
        db_wind = cursor.fetchone()
        self.wind = str(db_wind[1])
        self.wind_timestamp = str(db_wind[2])

        get_sens = "SELECT * FROM sens WHERE id=(SELECT MAX(id) FROM sens)"
        cursor.execute(get_sens)
        db_sens = cursor.fetchone()
        self.temp = str(db_sens[1])
        self.hum = str(round(db_sens[2]))
        self.atp = str(db_sens[3])
        self.sens_timestamp = str(db_sens[4])

        get_gps = "SELECT * FROM gps WHERE id=(SELECT MAX(id) FROM gps)"
        cursor.execute(get_gps)
        db_gps = cursor.fetchone()
        self.lat = str(db_gps[1])
        self.long = str(db_gps[2])
        self.alt = str(db_gps[3])
        self.gps_timestamp = str(db_gps[4])

        # TEMP
        get_max_wind_12 = "SELECT MAX(wind) FROM wind  WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL 12 HOUR)"
        get_max_wind_24 = "SELECT MAX(wind) FROM wind  WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL 24 HOUR)"
        get_max_wind = "SELECT MAX(wind) FROM wind"

        get_min_wind_12 = "SELECT MIN(wind) FROM wind  WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL 12 HOUR)"
        get_min_wind_24 = "SELECT MIN(wind) FROM wind  WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL 24 HOUR)"

        get_mean_wind = "SELECT AVG(wind) FROM wind  WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL 10 MINUTE)"

        # TEMP
        get_max_temp_12 = "SELECT MAX(temp) FROM sens  WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL 12 HOUR)"
        get_max_temp_24 = "SELECT MAX(temp) FROM sens  WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL 24 HOUR)"
        get_max_temp = "SELECT MAX(wind) FROM sens"

        get_min_temp_12 = "SELECT MIN(temp) FROM sens  WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL 12 HOUR)"
        get_min_temp_24 = "SELECT MIN(temp) FROM sens  WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL 24 HOUR)"
        get_min_temp = "SELECT MIN(temp) FROM sens"

        # HUM
        get_max_hum_12 = "SELECT MAX(hum) FROM sens  WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL 12 HOUR)"
        get_max_hum_24 = "SELECT MAX(hum) FROM sens  WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL 24 HOUR)"
        get_max_hum = "SELECT MAX(hum) FROM sens"

        get_min_hum_12 = "SELECT MIN(hum) FROM sens  WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL 12 HOUR)"
        get_min_hum_24 = "SELECT MIN(hum) FROM sens  WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL 24 HOUR)"
        get_min_hum = "SELECT MIN(hum) FROM sens"

        # ATP
        get_max_atp_12 = "SELECT MAX(atp) FROM sens  WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL 12 HOUR)"
        get_max_atp_24 = "SELECT MAX(atp) FROM sens  WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL 24 HOUR)"
        get_max_atp = "SELECT MAX(atp) FROM sens"

        get_min_atp_12 = "SELECT MIN(atp) FROM sens  WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL 12 HOUR)"
        get_min_atp_24 = "SELECT MIN(atp) FROM sens  WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL 24 HOUR)"
        get_min_atp = "SELECT MIN(atp) FROM sens"

        cursor.execute(get_mean_wind)
        db_mean_wind = cursor.fetchone()
        try:
            self.meanwind = str(round(db_mean_wind[0], 1))
        except:
            self.meanwind = "0"

        # print("Thread Running")