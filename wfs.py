import sys
import os
import time
import platform
from datetime import datetime, timedelta
from pathlib import Path

import mysql.connector
import psutil
from PyQt5.QtWidgets import (QWidget, QLabel, QApplication, QHBoxLayout, QVBoxLayout, QPushButton, QFrame, QGridLayout, QSizePolicy)
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtCore import Qt, QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.ticker import MaxNLocator

from wfs_forecast import fc
from wfs_error_handling import error_handle


class DatabaseFetcher:
    def __init__(self):
        self.connection_params = {'user': 'wfs', 'database': 'wfs', 'password': 'wfs22'}

    def fetch_data(self, query):
        try:
            cnx = mysql.connector.connect(**self.connection_params)
            cursor = cnx.cursor(buffered=True)
            cursor.execute(query)
            data = cursor.fetchall() if cursor.rowcount > 0 else None
            cursor.close()
            cnx.close()
            return data
        except Exception as e:
            filename = Path(__file__).name
            error_handle(e, filename)


class WeatherFetcher(DatabaseFetcher):
    def fetch_wind(self):
        data = self.fetch_data("SELECT * FROM wind WHERE id=(SELECT MAX(id) FROM wind)")
        if data:
            wind, timestamp = data[0][1], data[0][2]
            if timestamp >= datetime.now() - timedelta(minutes=0.25):
                return str(wind), timestamp
        return "-.-", None

    def fetch_mean(self):
        data = self.fetch_data(
            "SELECT mean FROM mean WHERE id=(SELECT MAX(id) FROM mean) AND tmestmp >= DATE_SUB(NOW(), INTERVAL 11 MINUTE)")
        if data:
            mean_wind = round(float(data[0][0]), 1)
            return mean_wind, self.get_beaufort_scale(mean_wind)
        return "-.-", "no data last 10 min..."

    @staticmethod
    def get_beaufort_scale(mean_wind):
        beaufort_scale = [
            (32.7, "Beaufort 12 - Hurricane"),
            (28.5, "Beaufort 11 - Violent Storm"),
            (24.5, "Beaufort 10 - Storm"),
            (20.8, "Beaufort 9 - Strong Gale"),
            (17.2, "Beaufort 8 - Fresh Gale"),
            (13.9, "Beaufort 7 - Moderate gale"),
            (10.8, "Beaufort 6 - Strong breeze"),
            (8.0, "Beaufort 5 - Fresh breeze"),
            (5.5, "Beaufort 4 - Moderate breeze"),
            (3.4, "Beaufort 3 - Gentle breeze"),
            (1.6, "Beaufort 2 - Light breeze"),
            (0.3, "Beaufort 1 - Light Air"),
            (0.0, "Beaufort 0 - Calm")
        ]
        for speed, description in beaufort_scale:
            if mean_wind > speed:
                return description
        return "Beaufort 0 - Calm"

    def fetch_peaks(self):
        try:
            periods = ['24 HOUR', '12 HOUR', '6 HOUR', '3 HOUR', '1 HOUR', '10 MINUTE']
            statistics = {}
            for period in periods:
                query = f"SELECT MAX(wind) FROM wind WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL {period})"
                data = self.fetch_data(query)
                statistics[period] = str(round(data[0][0], 1)) if data and data[0][0] is not None else "0.0"
            return statistics
        except Exception as e:
            filename = Path(__file__).name
            error_handle(e, filename)

    def fetch_sens(self):
        data = self.fetch_data("SELECT * FROM sens WHERE id=(SELECT MAX(id) FROM sens)")
        if data:
            return {'temp': str(data[0][1]), 'hum': str(data[0][2]), 'atp': str(data[0][3]),
                    'timestamp': str(data[0][5])}
        return {'temp': "0", 'hum': "0", 'atp': "0", 'timestamp': "0"}

    def fetch_gps(self):
        data = self.fetch_data(
            "SELECT * FROM gps WHERE id=(SELECT MAX(id)) AND tmestmp >= DATE_SUB(NOW(), INTERVAL 65 MINUTE)")
        if data:
            return {'lat': str(data[0][1]), 'long': str(data[0][2]), 'alt': str(data[0][3]),
                    'timestamp': str(data[0][4])}
        return {'lat': "No gps signal", 'long': "No gps signal", 'alt': "No gps signal", 'timestamp': "-"}

    def fetch_graph(self, interval):
        queries = {
            'wind': f"SELECT mean, UNIX_TIMESTAMP(tmestmp) FROM mean WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL {interval} HOUR)",
            'atp': f"SELECT atp, UNIX_TIMESTAMP(tmestmp) FROM sens WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL {interval} HOUR)",
            'temp': f"SELECT temp, UNIX_TIMESTAMP(tmestmp) FROM sens WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL {interval} HOUR)",
            'hum': f"SELECT hum, UNIX_TIMESTAMP(tmestmp) FROM sens WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL {interval} HOUR)"
        }
        graph_data = {}
        for key, query in queries.items():
            data = self.fetch_data(query)
            if data:
                graph_data[key] = {'x': [time.strftime('%H:%M', time.localtime(item[1])) for item in data],
                                   'y': [item[0] for item in data]}
            else:
                current_hour = int(time.strftime('%H', time.localtime(time.time())))
                graph_data[key] = {'x': [current_hour], 'y': [0]}
        return graph_data

    def fetch_error_light(self):
        data = self.fetch_data("SELECT * FROM error WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL 10 MINUTE)")
        return "error-red.png" if data else "error-green.png"

    def fetch_sens_arrow(self, sens_type):
        data = self.fetch_data("SELECT * FROM sens ORDER BY id DESC LIMIT 3")
        if data:
            sens_col = [list(item) for item in zip(*data)]
            t = (sum(sens_col[sens_type]) / len(sens_col[sens_type])) - sens_col[sens_type][2]
            if t > 0:
                return "arrow_down.png"
            if t < 0:
                return "arrow_up.png"
        return "arrow_flat.png"


weather_fetcher = WeatherFetcher()


class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=8, height=1, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        fig.patch.set_alpha(0.0)
        self.axes = fig.add_subplot(111)

        self.axes.set_facecolor('black')
        self.set_axis_colors()

        super(MplCanvas, self).__init__(fig)
        self.setStyleSheet("background: transparent;")
        self.setAttribute(Qt.WA_OpaquePaintEvent, False)

    def set_axis_colors(self):
        self.axes.tick_params(axis='x', colors='white')
        self.axes.tick_params(axis='y', colors='white')
        for spine in self.axes.spines.values():
            spine.set_color('white')


class QHLine(QFrame):
    def __init__(self):
        super(QHLine, self).__init__()
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)


class QVLine(QFrame):
    def __init__(self):
        super(QVLine, self).__init__()
        self.setFrameShape(QFrame.VLine)
        self.setFrameShadow(QFrame.Sunken)


class App(QWidget):
    def __init__(self, parent=None):
        super(App, self).__init__(parent=parent)
        self.title = "WFS - Weather Forecast Station"
        self.setWindowIcon(QIcon("img/drawing.svg.png"))
        self.setWindowTitle(self.title)

        # Use full screen or windowed mode
        if platform.system() == 'Windows':
            self.full_screen = False # Change this to True for full-screen mode
        else:
            self.full_screen = True

        self.img_path = str(Path(__file__).parent.absolute() / "img" / "main_BG.png")

        self.initUI()
        self.setup_timers()

        if self.full_screen:
            self.showFullScreen()

    def initUI(self):
        self.BGframe = QFrame(self)
        self.BGframe.setMinimumSize(800, 480)
        self.BGframe.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.BGframe.setObjectName("MFrame")

        self.applyBackground()

        self.O1 = QVBoxLayout(self.BGframe)
        self.mainContainer = QHBoxLayout()
        self.windContainer = QVBoxLayout()
        self.sensContainer = QVBoxLayout()

        path = str(Path(__file__).parent.absolute())
        self.setup_wind_box(path)
        self.setup_graph_container()
        self.setup_sens_container(path)
        self.setup_footer(path)

        self.mainContainer.addLayout(self.windContainer)
        self.mainContainer.addWidget(QVLine())
        self.mainContainer.addLayout(self.sensContainer)
        self.O1.addLayout(self.mainContainer)
        self.O1.addWidget(QHLine())
        self.O1.addLayout(self.footerBox)
        self.setLayout(self.O1)

    def applyBackground(self):
        img = self.img_path.replace(os.sep, '/')
        self.setStyleSheet(f"""
            QFrame#MFrame {{
                background-image: url({img});
                background-repeat: no-repeat;
                background-position: center;
                background-attachment: fixed;
                border: none;
            }}
            QLabel {{
                color : white;
            }}
        """)

    def setup_wind_box(self, path):
        self.windBox = QHBoxLayout()
        wind_data, wind_timestamp = weather_fetcher.fetch_wind()
        mean_data, mean_beaufort = weather_fetcher.fetch_mean()

        self.windL = QLabel(wind_data)
        self.windL.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.windL.setMinimumHeight(165)
        self.windL.setFont(QFont('Arial', 40))
        img = os.path.join(path, "img", "wind_BG.png")
        self.windL.setStyleSheet(f"""
            background-image: url({img.replace(os.sep, '/')});
            background-repeat: no-repeat;
            background-position: center;
        """)

        self.meanL = QLabel(str(mean_data))
        self.meanL.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.meanL.setMinimumHeight(165)
        self.meanL.setFont(QFont('Arial', 40))
        img = os.path.join(path, "img", "mean_BG.png")
        self.meanL.setStyleSheet(f"""
            background-image: url({img.replace(os.sep, '/')});
            background-repeat: no-repeat;
            background-position: center;
        """)

        self.windBox.addWidget(self.windL)
        self.windBox.addWidget(self.meanL)
        self.windContainer.addLayout(self.windBox)

        self.beaufortbox = QHBoxLayout()
        self.beaufortL = QLabel(mean_beaufort)
        self.beaufortL.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.beaufortL.setFont(QFont('Arial', 20))
        self.beaufortbox.addWidget(self.beaufortL)
        self.windContainer.addLayout(self.beaufortbox)

    def setup_graph_container(self):
        self.graphContainer = QVBoxLayout()
        self.graphPlotContainer = QHBoxLayout()
        self.canvas = MplCanvas(self, width=6, height=2, dpi=100)
        self.graphPlotContainer.addWidget(self.canvas)

        self.gwb = self.create_graph_button("Wind (mean)", self.switch_to_wind)
        self.gab = self.create_graph_button("Pressure", self.switch_to_pressure)
        self.gtb = self.create_graph_button("Temperature", self.switch_to_temp)
        self.ghb = self.create_graph_button("Humidity", self.switch_to_hum)

        self.graphButtons = QHBoxLayout()
        self.graphButtons.addWidget(self.gwb)
        self.graphButtons.addWidget(self.gab)
        self.graphButtons.addWidget(self.gtb)
        self.graphButtons.addWidget(self.ghb)

        self.graphContainer.addLayout(self.graphPlotContainer)
        self.graphContainer.addLayout(self.graphButtons)

        self.windContainer.addLayout(self.graphContainer)

    def create_graph_button(self, text, method):
        button = QPushButton(text)
        button.setCheckable(True)
        button.clicked.connect(method)
        return button

    def setup_sens_container(self, path):
        self.sensFrame = QFrame(self)
        self.sensBox = QVBoxLayout(self.sensFrame)
        self.sensheaderBox = QHBoxLayout(self.sensFrame)

        self.sensHL = QLabel("SENSOR")
        self.sensHL.setFont(QFont('Arial', 15))
        self.sensheaderBox.addWidget(self.sensHL)
        self.sensBox.addLayout(self.sensheaderBox)

        self.sensgrid = QGridLayout()
        self.sensBox.addLayout(self.sensgrid)

        self.setup_sens_row(self.sensgrid, 0, 'temp', '°C', path)
        self.setup_sens_row(self.sensgrid, 1, 'hum', '%', path)
        self.setup_sens_row(self.sensgrid, 2, 'atp', 'hPa', path)

        self.sensgrid.setRowStretch(3, 1)
        self.sensBox.addLayout(self.sensgrid)

        self.setup_peak_winds()
        self.setup_forecast()

        self.sensContainer.addWidget(self.sensFrame)

    def setup_sens_row(self, grid, row, sensor, unit, path):
        sens_data = weather_fetcher.fetch_sens()
        arrow = weather_fetcher.fetch_sens_arrow(row)

        img_path = self.get_sens_image_path(sensor, path)

        img = QPixmap(img_path)
        ico = QLabel()
        ico.setPixmap(img)
        value = QLabel(sens_data[sensor] + f" {unit}")
        value.setFont(QFont('Arial', 13))
        arrow_img = QPixmap(path + f'/img/{arrow}')
        arrow_label = QLabel()
        arrow_label.setPixmap(arrow_img)

        self.assign_sens_widgets(sensor, value, arrow_label)

        grid.addWidget(ico, row, 0, Qt.AlignmentFlag.AlignCenter)
        grid.addWidget(value, row, 1, Qt.AlignmentFlag.AlignCenter)
        grid.addWidget(arrow_label, row, 2, Qt.AlignmentFlag.AlignCenter)

    def get_sens_image_path(self, sensor, path):
        if sensor == 'temp':
            return os.path.join(path, "img", "ico-generic_red.png")
        elif sensor == 'hum':
            return os.path.join(path, "img", "ico-generic_green.png")
        elif sensor == 'atp':
            return os.path.join(path, "img", "ico-generic_blue.png")
        else:
            return os.path.join(path, "img", "ico-generic.png")

    def assign_sens_widgets(self, sensor, value, arrow_label):
        if sensor == 'temp':
            self.tempvalue = value
            self.temparrow = arrow_label
        elif sensor == 'hum':
            self.humvalue = value
            self.humarrow = arrow_label
        elif sensor == 'atp':
            self.atpvalue = value
            self.atparrow = arrow_label

    def setup_peak_winds(self):
        fontsize = QFont('Arial', 10)
        self.statHeader = QLabel("PEAK WINDS  ")
        self.statHeader.setFont(QFont('Arial', 15))

        self.peak_labels = [QLabel(" NA ") for _ in range(6)]
        for label in self.peak_labels:
            label.setFont(fontsize)

        self.peaks = QVBoxLayout(self.sensFrame)
        self.peaks.addWidget(self.statHeader)
        self.peakgrid = QGridLayout()
        self.peaks.addLayout(self.peakgrid)

        peak_titles = ["Peak 10min", "Peak 1 hour", "Peak 3 hour", "Peak 6 hour", "Peak 12 hour", "Peak 24 hour"]
        for i, (title, label) in enumerate(zip(peak_titles, self.peak_labels)):
            self.peakgrid.addWidget(QLabel(title), i, 0, Qt.AlignRight)
            self.peakgrid.addWidget(label, i, 1, Qt.AlignCenter)
            self.peakgrid.addWidget(QLabel("m/s"), i, 2, Qt.AlignCenter)

        self.peakgrid.setRowStretch(5, 50)
        self.sensBox.addLayout(self.peaks)
        self.peaks.addWidget(QLabel(""))
        self.peaks.addWidget(QLabel(""))
        self.peaks.addStretch()

    def setup_forecast(self):
        self.forecast = QVBoxLayout()
        self.Fheader = QLabel("FORECAST")
        self.Fheader.setFont(QFont('Arial', 15))
        f = fc()
        self.Fforecast1 = QLabel(f[0])
        self.Fforecast2 = QLabel(f[1])
        self.forecast.addWidget(self.Fheader)
        self.forecast.addWidget(self.Fforecast1)
        self.forecast.addWidget(self.Fforecast2)
        self.sensBox.addLayout(self.forecast)

    def setup_footer(self, path):
        gps = weather_fetcher.fetch_gps()
        self.footerBox = QHBoxLayout()
        self.latitude = QLabel(f"Latitude: {gps['lat']}")
        self.longitude = QLabel(f"Longitude: {gps['long']}")
        self.altitude = QLabel(f"Altitude: {gps['alt']}")

        self.footerBox.addWidget(self.latitude)
        self.footerBox.addWidget(self.longitude)
        self.footerBox.addWidget(self.altitude)

        self.errimg = QPixmap(path + '/img/' + weather_fetcher.fetch_error_light())
        self.errico = QLabel()
        self.errico.setPixmap(self.errimg)
        self.footerBox.addWidget(self.errico)

        if psutil:
            mem = psutil.virtual_memory()
            used_mem = round(mem.used / mem.total * 100)
            self.res = QLabel(f"P:{psutil.cpu_percent()}% - M:{used_mem}%")
            self.footerBox.addWidget(self.res)


    def update_wind(self):
        wind, wind_timestamp = weather_fetcher.fetch_wind()
        mean_wind, beaufort = weather_fetcher.fetch_mean()
        try:
            self.windL.setText(wind)
            self.meanL.setText(str(mean_wind))
            self.beaufortL.setText(beaufort)
        except Exception as e:
            filename = Path(__file__).name
            error_handle(e, filename)
        QApplication.processEvents()

    def update_peaks(self):
        peaks = weather_fetcher.fetch_peaks()
        try:
            for period, label in zip(['10 MINUTE', '1 HOUR', '3 HOUR', '6 HOUR', '12 HOUR', '24 HOUR'], self.peak_labels):
                label.setText(peaks[period])
        except Exception as e:
            filename = Path(__file__).name
            error_handle(e, filename)
        QApplication.processEvents()

    def update_sens(self):
        try:
            path = str(Path(__file__).parent.absolute())
            sens = weather_fetcher.fetch_sens()
            gps = weather_fetcher.fetch_gps()

            self.tempvalue.setText(sens['temp'] + " °C")
            self.temparrow.setPixmap(QPixmap(path + f'/img/{weather_fetcher.fetch_sens_arrow(0)}'))
            self.humvalue.setText(sens['hum'] + "%")
            self.humarrow.setPixmap(QPixmap(path + f'/img/{weather_fetcher.fetch_sens_arrow(1)}'))
            self.atpvalue.setText(sens['atp'] + " hPa")
            self.atparrow.setPixmap(QPixmap(path + f'/img/{weather_fetcher.fetch_sens_arrow(2)}'))
            f = fc()
            self.Fforecast1.setText(f[0])
            self.Fforecast2.setText(f[1])

            self.latitude.setText("Latitude: " + gps['lat'])
            self.longitude.setText("Longitude: " + gps['long'])
            self.altitude.setText("Altitude: " + gps['alt'])

            self.errimg = QPixmap(path + '/img/' + weather_fetcher.fetch_error_light())
            self.errico.setPixmap(self.errimg)
            if psutil:
                mem = psutil.virtual_memory()
                used_mem = round(mem.used / mem.total * 100)
                self.res.setText(f"P:{psutil.cpu_percent()}% - M:{used_mem}%")

        except Exception as e:
            filename = Path(__file__).name
            error_handle(e, filename)
        QApplication.processEvents()

    def switch_to_wind(self):
        self.set_graph_button_state(self.gwb)
        self.update_graph()

    def switch_to_pressure(self):
        self.set_graph_button_state(self.gab)
        self.update_graph()

    def switch_to_temp(self):
        self.set_graph_button_state(self.gtb)
        self.update_graph()

    def switch_to_hum(self):
        self.set_graph_button_state(self.ghb)
        self.update_graph()

    def set_graph_button_state(self, active_button):
        buttons = [self.gwb, self.gab, self.gtb, self.ghb]
        for button in buttons:
            button.setChecked(button == active_button)

    def update_graph(self):
        try:
            graph_data = weather_fetcher.fetch_graph(12)
            self.canvas.axes.clear()
            if self.gwb.isChecked():
                self.plot_graph_data(graph_data, 'wind', 'yellow', "Mean Wind (m/s)")
            elif self.gab.isChecked():
                self.plot_graph_data(graph_data, 'atp', 'blue', "BMP (hPa)")
            elif self.gtb.isChecked():
                self.plot_graph_data(graph_data, 'temp', 'red', "Temperature (C)")
            elif self.ghb.isChecked():
                self.plot_graph_data(graph_data, 'hum', 'green', "Humidity (%)")
            self.canvas.draw()
        except Exception as e:
            filename = Path(__file__).name
            error_handle(e, filename)
        QApplication.processEvents()

    def plot_graph_data(self, graph_data, key, color, ylabel):
        self.canvas.axes.plot(graph_data[key]['x'], graph_data[key]['y'], label=key.capitalize(), color=color)
        self.canvas.axes.set_ylabel(ylabel, color=color)
        self.canvas.axes.set_xlabel("Time", color='white')
        self.canvas.axes.xaxis.set_major_locator(MaxNLocator(nbins=8))
        self.canvas.axes.yaxis.set_major_locator(MaxNLocator(integer=bool))
        self.canvas.axes.grid()

    def setup_timers(self):
        self.wind_timer = QTimer(self)
        self.wind_timer.timeout.connect(self.update_wind)
        self.wind_timer.start(1000)

        self.sens_timer = QTimer(self)
        self.sens_timer.timeout.connect(self.update_sens)
        self.sens_timer.start(5000)

        self.graph_timer = QTimer(self)
        self.graph_timer.timeout.connect(self.update_graph)
        self.graph_timer.start(60000)

        self.statistics_timer = QTimer(self)
        self.statistics_timer.timeout.connect(self.update_peaks)
        self.statistics_timer.start(60000)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec())
