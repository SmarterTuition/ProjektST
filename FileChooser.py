import numpy
from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QFileDialog, QTextEdit
from PyQt6 import uic
import pandas as pd
from xgboost import XGBRegressor


class FileChooser(QWidget):

    def __init__(self, parent=None):
        super(FileChooser, self).__init__(parent)

        self.path = None
        self.fileType = None
        self.filename = None
        self.type = None
        self.loadedfilename = None
        self.newfilename = None
        self.data = None

        uic.loadUi("ST_GUI2.ui", self)
        # UI-Elemente verbinden sowie Implementierung der Funktionsaufrufe
        self.chooser = self.findChild(QPushButton, "OpenExcel")
        self.chooser.clicked.connect(self.open)
        self.DataLabel = self.findChild(QLabel, "label")
        self.startKI = self.findChild(QPushButton, "StartKi")
        self.startKI.clicked.connect(self.auswertung)
        self.KiResult = self.findChild(QTextEdit, "KiResult")

    def open(self):

        # Auslesen des Pfades bei Auswahl einer xls oder xlsx Datei
        self.path = "./"
        self.fileType = "Excel (*.xls);;Excel( *.xlsx)"
        self.filename, self.type = QFileDialog.getOpenFileName(self, self.path, self.fileType)

        if self.filename == "":
            return
        if self.filename.endswith(".xls") or self.filename.endswith(".xlsx"):
            self.loadedfilename = self.filename.rsplit('/')
            self.newfilename = "Excel Datei {fn} erfolgreich geladen!".format(fn='"' + self.loadedfilename[-1] + '"')
            self.DataLabel.setText(self.newfilename)
            self.data = pd.read_excel('{file}'.format(file=self.filename))

    def auswertung(self):

        # Abfangen bei fehlerhafter Benutzung der GUI
        if self.filename is None:
            self.KiResult.setText("Bitte wählen Sie zuerst eine Datei aus")
        # Abfangen falsch ausgewählter Excel-Dateien
        elif self.data.columns.size != 13:
            self.KiResult.setText(
                "Die ausgewählt Datei entspricht nicht dem vorgegebenem Format (15 Spalten)\nBitte überprüfen Sie die ausgewählte Datei")
        else:
            pd.set_option('display.expand_frame_repr', False)
            # Die Office-ID der Lehrkraft wird in unserem Fall nicht benötigt, da nur eine Lehrkraft die Umfragen
            # durchgeführt hat. Da diese aber in Zukunft von Nutzen sein könnte, wird diese in der Umfrage verbleiben.

            # data = self.data.iloc[0:self.data.shape[0],0]
            # temp = pd.get_dummies(data, drop_first=True)
            # data = temp

            # Spalte 2 --- (Beurteilen Sie Ihre eigene Motivation in dem unterrichteten Fach)
            data = self.data.iloc[0:self.data.shape[0], 1]
            # Spalte 3 --- (Den Unterricht meiner Lehrkraft empfinde ich als wertschätzend)
            temp = self.data.iloc[0:self.data.shape[0], 2]
            data = pd.concat([data, temp], axis=1)
            # Spalte 4 --- (Das Klassenklima empfinde ich als positiv)
            temp = self.data.iloc[0:self.data.shape[0], 3]
            data = pd.concat([data, temp], axis=1)
            # Spalte 5 --- (Ein sehr guter Ausbildungsabschluss ist für mich sehr wichtig)
            temp = self.data.iloc[0:self.data.shape[0], 4]
            data = pd.concat([data, temp], axis=1)
            # Spalte 6 OHE --- (Geschlecht)
            temp1 = self.data.iloc[0:self.data.shape[0], 5]
            temp = pd.get_dummies(temp1, drop_first=True)
            data = pd.concat([data, temp], axis=1)
            # Spalte 7 --- Alter
            temp = self.data.iloc[0:self.data.shape[0], 6]
            data = pd.concat([data, temp], axis=1)
            # Spalte 8 OHE --- (Aktuelle Ausbildungsrichtung)
            temp1 = self.data.iloc[0:self.data.shape[0], 7]
            temp = pd.get_dummies(temp1, drop_first=True)
            data = pd.concat([data, temp], axis=1)
            # Spalte 9 OHE --- Reguläre Ausbildungsdauer
            temp1 = self.data.iloc[0:self.data.shape[0], 8]
            temp = pd.get_dummies(temp1, drop_first=True)
            data = pd.concat([data, temp], axis=1)
            # Spalte 10 --- Aktuelle Jahrgangsstufe
            temp = self.data.iloc[0:self.data.shape[0], 9]
            data = pd.concat([data, temp], axis=1)
            # Spalte 11 OHE --- Ist Ihre Muttersprache Deutsch?
            temp1 = self.data.iloc[0:self.data.shape[0], 10]
            temp = pd.get_dummies(temp1, drop_first=True)
            data = pd.concat([data, temp], axis=1)
            # Spalte 12 OHE --- Welche größe hat das Unternehmen in welchem Sie beschäftigt sind?
            temp1 = self.data.iloc[0:self.data.shape[0], 11]
            temp = pd.get_dummies(temp1, drop_first=True)
            data = pd.concat([data, temp], axis=1)
            # Spalte 13 OHE --- Bisherige Schulbildung
            temp1 = self.data.iloc[0:self.data.shape[0], 12]
            temp = pd.get_dummies(temp1, drop_first=True)
            data = pd.concat([data, temp], axis=1)
            # Spalte 14 --- Wurde Ihr Lernerfolg durch den Einsatz des digitalen Tools gefördert?
            # temp = self.data.iloc[0:self.data.shape[0], 13]
            # data = pd.concat([data, temp], axis=1)
            # Spalte 15 als Label --- Würden Sie sich einen häufigeren Einsatz digitaler Tools im Unterricht wünschen?
            # label = self.data.iloc[0:self.data.shape[0], 13]

            # XGBRegressor mit 150 Bäumen, einer max_depth von 5, learning_rate von 0.05 und early_stopping_rounds i.h.v. 15
            model = XGBRegressor()
            model.load_model('model.json')
            prediction = model.predict(data)

            star = numpy.mean(prediction)
            self.KiResult.setText("Die ermittelte Eignung des Einsatzes des digitalen Tools in Ihrer Klasse beträgt:"
                                  "\n{:.1f} / 6 Sterne".format(star))
