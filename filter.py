import sys
from scipy import signal
from PyQt5.QtGui import QDoubleValidator, QIntValidator
from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QMenuBar, QMenu, QAction, QWidget, \
    QGroupBox, QPushButton, QComboBox, QVBoxLayout, QLabel, QLineEdit
import pyqtgraph as pg
import numpy as np

class Ui_MainWindow(object):
    amplitude1 = 25.0
    frequency1 = 0.3
    amplitude2 = 40.0
    frequency2 = 0.7
    order = 10
    frequencyLow = 0.05
    frequencyHigh = 0.65
    typeFiltr = "highpass"

    def setupUi(self, MainWindow):

        MainWindow.setGeometry(50, 50, 1500, 785)
        MainWindow.setWindowTitle("CFS")

        self.mainMenu = QMenuBar(MainWindow)
        self.mainMenu.setGeometry(QRect(0, 0, 1000, 21))
        self.fileMenu = QMenu('&Sygnał', self.mainMenu)
        MainWindow.setMenuBar(self.mainMenu)
        self.actionOpenExample = QAction('&Przykładowy sygnał', MainWindow)
        self.actionOpenExample.setShortcut('Ctrl+P')
        self.actionOpenExample.setStatusTip('Sygnał z sumą sygnałów sinusoidalnych o częstotliwościach z pasm zaporowego i przepustowego.')
        self.fileMenu.addAction(self.actionOpenExample)
        self.actionOpenExample.triggered.connect(self.plotExample)
        self.fileMenu.addSeparator()
        self.mainMenu.addAction(self.fileMenu.menuAction())

        self.centralwidget = QWidget(MainWindow)
        self.groupBoxSignalExample = QGroupBox(self.centralwidget)
        self.groupBoxSignalExample.setTitle("Tworzenie sumy sygnałów sinusoidalnych:")
        self.groupBoxSignalExample.setGeometry(QRect(10, 20, 270, 111))
        self.labelIPlotSin = QLabel(self.groupBoxSignalExample)
        self.labelIPlotSin.setGeometry(QRect(10, -20, 150, 111))
        self.labelIPlotSin.setText("Perwszy sygnał sinusoidalny o")
        self.labelAmplitude = QLabel(self.groupBoxSignalExample)
        self.labelAmplitude.setGeometry(QRect(10, 0, 60, 111))
        self.labelAmplitude.setText("Amplitudzie:")

        self.valueAmplitude = QLineEdit(self.groupBoxSignalExample)
        self.valueAmplitude.setValidator(QDoubleValidator(-100.99, 100.99, 2))
        self.valueAmplitude.setMaxLength(7)
        self.valueAmplitude.setText("25")
        self.valueAmplitude.setGeometry(QRect(70, 47, 45, 15))

        self.labelFrequency = QLabel(self.groupBoxSignalExample)
        self.labelFrequency.setGeometry(QRect(140, 0, 70, 111))
        self.labelFrequency.setText("Częstotliwości:")
        self.valueFrequency = QLineEdit(self.groupBoxSignalExample)
        self.valueFrequency.setValidator(QDoubleValidator(-100.9, 100.9, 2))
        self.valueFrequency.setGeometry(QRect(215, 47, 45, 15))
        self.valueFrequency.setMaxLength(7)
        self.valueFrequency.setText("0,3")

        self.labelIIPlotSin = QLabel(self.groupBoxSignalExample)
        self.labelIIPlotSin.setGeometry(QRect(10, 20, 60, 111))
        self.labelIIPlotSin.setText("Drugi sygnał")
        self.labelAmplitudeII = QLabel(self.groupBoxSignalExample)
        self.labelAmplitudeII.setGeometry(QRect(10, 40, 60, 111))
        self.labelAmplitudeII.setText("Amplitudzie:")
        self.valueAmplitudeII = QLineEdit(self.groupBoxSignalExample)
        self.valueAmplitudeII.setValidator(QDoubleValidator(-100.99, 100.99, 2))
        self.valueAmplitudeII.setGeometry(QRect(70, 88, 45, 15))
        self.valueAmplitudeII.setMaxLength(7)
        self.valueAmplitudeII.setText("40")

        self.labelFrequencyII = QLabel(self.groupBoxSignalExample)
        self.labelFrequencyII.setGeometry(QRect(140, 40, 70, 111))
        self.labelFrequencyII.setText("Częstotliwości:")
        self.valueFrequencyII = QLineEdit(self.groupBoxSignalExample)
        self.valueFrequencyII.setValidator(QDoubleValidator(-100.99, 100.99, 2))
        self.valueFrequencyII.setGeometry(QRect(215, 88, 45, 15))
        self.valueFrequencyII.setMaxLength(7)
        self.valueFrequencyII.setText("0,7")

        self.groupBoxTypeFiltration = QGroupBox(self.centralwidget)
        self.groupBoxTypeFiltration.setGeometry(QRect(300, 20, 131, 111))
        self.groupBoxTypeFiltration.setTitle("Rodzaj filtracji:")
        self.comboBoxTypeFiltation = QComboBox(self.groupBoxTypeFiltration)
        self.comboBoxTypeFiltation.setGeometry(QRect(5, 30, 120, 25))
        self.comboBoxTypeFiltation.addItem("górnoprzepustowy")
        self.comboBoxTypeFiltation.addItem("środkowozaporowy")
        self.comboBoxTypeFiltation.addItem("środkowoprzepustowy")
        self.comboBoxTypeFiltation.addItem("dolnoprzepustowy")

        self.comboBoxTypeFiltation.currentIndexChanged.connect(self.updateTypeFiltr)

        self.groupBoxParametrsFiltr = QGroupBox(self.centralwidget)
        self.groupBoxParametrsFiltr.setGeometry(QRect(455, 20, 171, 111))
        self.groupBoxParametrsFiltr.setTitle("Parametry do filtracji:")
        self.labelOrder = QLabel(self.groupBoxParametrsFiltr)
        self.labelOrder.setGeometry(QRect(10, 10, 26, 45))
        self.labelOrder.setText("Rząd:")

        self.valueOrder = QLineEdit(self.groupBoxParametrsFiltr)
        self.valueOrder.setValidator(QIntValidator(1, 100))
        self.valueOrder.setGeometry(QRect(110, 25, 45, 14))
        self.valueOrder.setMaxLength(3)
        self.valueOrder.setText("10")

        self.labelFrequencyLow = QLabel(self.groupBoxParametrsFiltr)
        self.labelFrequencyLow.setGeometry(QRect(10, 30, 100, 45))
        self.labelFrequencyLow.setText("Częstotliwość dolna:")

        self.valueFrequencyLow = QLineEdit(self.groupBoxParametrsFiltr)
        self.valueFrequencyLow.setValidator(QDoubleValidator(-100.99, 100.99, 2))
        self.valueFrequencyLow.setGeometry(QRect(110, 45, 45, 14))
        self.valueFrequencyLow.setMaxLength(7)
        self.valueFrequencyLow.setText("0,05")
        self.valueFrequencyLow.setDisabled(True)

        self.labelFrequencyHigh = QLabel(self.groupBoxParametrsFiltr)
        self.labelFrequencyHigh.setGeometry(QRect(10, 50, 100, 45))
        self.labelFrequencyHigh.setText("Częstotliwość górna:")

        self.valueFrequencyHigh = QLineEdit(self.groupBoxParametrsFiltr)
        self.valueFrequencyHigh.setValidator(QDoubleValidator(-100.99, 100.99, 2))
        self.valueFrequencyHigh.setGeometry(QRect(110, 65, 45, 14))
        self.valueFrequencyHigh.setMaxLength(7)
        self.valueFrequencyHigh.setText("0,65")

        self.pushButtonFiltring = QPushButton(self.centralwidget)
        self.pushButtonFiltring.setGeometry(QRect(650, 90, 70, 25))
        self.pushButtonFiltring.setText("Filtruj")
        self.pushButtonFiltring.clicked.connect(self.updatePlot)

        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')

        self.x, self.y = self.creatingSignal()

        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(12, 130, 10, 10)
        self.plotSygnalWej = pg.PlotWidget()
        self.makePlotWej()
        self.plotSygnalWej.setTitle("SYGNAŁ WEJŚCIOWY")
        self.plotSygnalWej.setLabel('bottom', "Czas", units='s')
        self.plotSygnalWej.setLabel('left', "Amplituda", units='')
        self.verticalLayout.addWidget(self.plotSygnalWej)

        self.plotSygnalFiltr = pg.PlotWidget()
        self.filtring()
        self.makePlotFilter()
        self.plotSygnalFiltr.setTitle("SYGNAŁ PO FILTRACJI")
        self.plotSygnalFiltr.setLabel('bottom', "Czas", units='s')
        self.plotSygnalFiltr.setLabel('left', "Amplituda", units='')
        self.verticalLayout.addWidget(self.plotSygnalFiltr)

        MainWindow.setCentralWidget(self.centralwidget)

    def filtring(self):

        if self.typeFiltr == "highpass":
            butter = signal.butter(self.order, self.frequencyHigh, btype=self.typeFiltr, fs=self.sampling_rate, output='sos')
            self.y_filtr = signal.sosfilt(butter, self.y)

        else:
            if self.typeFiltr == "lowpass":
                butter = signal.butter(self.order, self.frequencyLow, btype=self.typeFiltr, fs=self.sampling_rate, output='sos')
                self.y_filtr = signal.sosfilt(butter, self.y)

            else:
                butter = signal.butter(self.order, [self.frequencyLow, self.frequencyHigh], btype=self.typeFiltr, fs=self.sampling_rate, output='sos')
                self.y_filtr = signal.sosfilt(butter, self.y)

    def creatingSignal(self):
        self.sampling_rate = 1000  # samples per second
        time = 171.3  # seconds
        times = np.linspace(0, time, time * self.sampling_rate)
        y = self.amplitude1 * np.sin(2 * np.pi * times * self.frequency1 ) + self.amplitude2 * np.sin(2 * np.pi * times * self.frequency2 )

        return times, y

    def plotExample(self):
        self.amplitude1 = 25.0
        self.frequency1 = 0.3
        self.amplitude2 = 40.0
        self.frequency2 = 0.7
        self.order = 10
        self.frequencyLow = 0.05
        self.frequencyHigh = 0.65
        self.typeFiltr = "highpass"
        self.valueAmplitude.setText("25")
        self.valueFrequency.setText("0,3")
        self.valueAmplitudeII.setText("40")
        self.valueFrequencyII.setText("0,7")
        self.valueOrder.setText("10")
        self.valueFrequencyHigh.setText("0,65")
        self.valueFrequencyLow.setText("0,05")
        self.valueFrequencyLow.setDisabled(True)
        self.valueFrequencyHigh.setDisabled(False)
        self.comboBoxTypeFiltation.setCurrentIndex(0)

        self.x, self.y = self.creatingSignal()

        self.makePlotWej()
        self.filtring()
        self.makePlotFilter()

    def makePlotWej(self):

        self.plotSygnalWej.plot(x=self.x, y=self.y, pen='k', clear=True)
        tempMinX = min(self.x)
        tempMaxX = max(self.x)
        tempMinY = min(self.y)
        tempMaxY = max(self.y)

        tempDistanceX = 0.02
        if tempMaxX <= 10.0:
            pass
        else:
            if tempMaxX <= 100.0:
                tempDistanceX = 0.2
            else:
                tempDistanceX = 2.0

        if tempMinY > 0:
            tempDistanceMinY = tempMinY - tempMinY / 2
        else:
            if tempMinY < 0:
                tempDistanceMinY = tempMinY + tempMinY / 2
            else:
                tempDistanceMinY = - 10

        if tempMaxY < 0:
            tempDistanceMaxY = tempMaxX - tempMaxX / 2
        else:
            if tempMaxY > 0:
                tempDistanceMaxY = tempMaxY + tempMaxY / 2
            else:
                tempDistanceMaxY = + 10

        self.plotSygnalWej.setRange(xRange=[tempMinX - tempDistanceX, tempMaxX + tempDistanceX],
                                yRange=[tempDistanceMinY, tempDistanceMaxY])
        self.plotSygnalWej.setLimits(xMin=tempMinX - tempDistanceX, xMax=tempMaxX + tempDistanceX, yMin=tempDistanceMinY,
                                  yMax=tempDistanceMaxY)

    def makePlotFilter(self):
        self.plotSygnalFiltr.plot(x=self.x, y=self.y_filtr, pen='k', clear=True)

        tempMinX = min(self.x)
        tempMaxX = max(self.x)
        tempMinY = min(self.y_filtr)
        tempMaxY = max(self.y_filtr)

        tempDistanceX = 0.02
        if tempMaxX <= 10.0:
            pass
        else:
            if tempMaxX <= 100.0:
                tempDistanceX = 0.2
            else:
                tempDistanceX = 2.0

        if tempMinY > 0:
            tempDistanceMinY = tempMinY - tempMinY / 2
        else:
            if tempMinY < 0:
                tempDistanceMinY = tempMinY + tempMinY / 2
            else:
                tempDistanceMinY = - 10

        if tempMaxY < 0:
            tempDistanceMaxY = tempMaxX - tempMaxX / 2
        else:
            if tempMaxY > 0:
                tempDistanceMaxY = tempMaxY + tempMaxY / 2
            else:
                tempDistanceMaxY = + 10

            self.plotSygnalFiltr.setRange(xRange=[tempMinX - tempDistanceX, tempMaxX + tempDistanceX],
                                yRange=[tempDistanceMinY, tempDistanceMaxY])
            self.plotSygnalFiltr.setLimits(xMin=tempMinX - tempDistanceX, xMax=tempMaxX + tempDistanceX, yMin=tempDistanceMinY,
                                 yMax=tempDistanceMaxY)

    def updatePlot(self):

        try:
            self.amplitude1 = float(self.validator(self.valueAmplitude.text()))
        except:
            QMessageBox.information(None, 'Informacja', 'Niepoprawna wartość w amplitudzie\npierwszego sygnału sinusoidalnego.', QMessageBox.Ok)
            self.amplitude1 = 25.0


        try:
            self.amplitude2 = float(self.validator(self.valueAmplitudeII.text()))
        except:
            QMessageBox.information(None, 'Informacja', 'Niepoprawna wartość w amplitudzie\ndrugiego sygnału sinusoidalnego.', QMessageBox.Ok)
            self.amplitude2 = 40.0


        try:
            self.frequency1 = float(self.validator(self.valueFrequency.text()))
        except:
            QMessageBox.information(None, 'Informacja', 'Niepoprawna wartość w czestotliwści\nperwszego sygnału sinusoidalnego.', QMessageBox.Ok)
            self.frequency1 = 0.3

        try:
            self.frequency2 = float(self.validator(self.valueFrequencyII.text()))

        except:
            QMessageBox.information(None, 'Informacja', 'Niepoprawna wartość w czestotliwości\ndrugiego sygnału sinusoidalnego.', QMessageBox.Ok)
            self.frequency2 = 0.7


        self.order = int(self.validator(self.valueOrder.text()))

        try:
            self.frequencyLow = float(self.validator(self.valueFrequencyLow.text()))
        except:
            QMessageBox.information(None, 'Informacja', 'Niepoprawna wartość w czestotliwości\ndolnej parametru do filtracji.', QMessageBox.Ok)
            self.frequencyLow = 0.5

        try:
            self.frequencyHigh = float(self.validator(self.valueFrequencyHigh.text()))

        except:
            QMessageBox.information(None, 'Informacja', 'Niepoprawna wartość w czestotliwości\ngornej parametru do filtracji.', QMessageBox.Ok)
            self.frequencyHigh = 1.0

        try:
            self.x, self.y = self.creatingSignal()
            self.makePlotWej()
            self.filtring()
            self.makePlotFilter()
        except:
            QMessageBox.information(None, 'Informacja', 'Bład.', QMessageBox.Ok)

    def validator(self, str):
        if str == "":
            return "0"

        temp = str.replace(",", ".")

        return temp

    def updateTypeFiltr(self):

        temp = self.comboBoxTypeFiltation.currentText()

        if (temp == "górnoprzepustowy"):
            self.typeFiltr = "highpass"
            self.valueFrequencyLow.setDisabled(True)
            self.valueFrequencyHigh.setDisabled(False)
        else:
            if (temp == "środkowozaporowy"):
                self.typeFiltr = "bandstop"
                self.valueFrequencyLow.setDisabled(False)
                self.valueFrequencyHigh.setDisabled(False)
            else:
                if (temp == "środkowoprzepustowy"):
                    self.typeFiltr = "bandpass"
                    self.valueFrequencyLow.setDisabled(False)
                    self.valueFrequencyHigh.setDisabled(False)
                else:
                        self.typeFiltr = "lowpass"
                        self.valueFrequencyLow.setDisabled(False)
                        self.valueFrequencyHigh.setDisabled(True)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QMainWindow()
    gui = Ui_MainWindow()
    gui.setupUi(window)
    window.show()
    sys.exit(app.exec_())
