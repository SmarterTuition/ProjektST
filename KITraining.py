import os
import numpy
from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QFileDialog, QTextEdit
from PyQt6 import uic
import pandas as pd
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor


class FileChooser2(QWidget):

    def __init__(self, parent=None):
        super(FileChooser2, self).__init__(parent)

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
            self.newfilename = f'Excel Datei "{os.path.basename(self.filename)}" erfolgreich geladen!'
            self.DataLabel.setText(self.newfilename)
            self.data = pd.read_excel(self.filename)

    def auswertung(self):

        # Abfangen bei fehlerhafter Benutzung der GUI
        if self.filename is None:
            self.KiResult.setText("Bitte wählen Sie zuerst eine Datei aus")
        # Abfangen falsch ausgewählter Excel-Dateien
        elif self.data.columns.size != 15:
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
            # Spalte 3 --- (Den Unterricht meiner Lehrkraft empfinde ich als wertschätzend)
            # Spalte 4 --- (Das Klassenklima empfinde ich als positiv)
            # Spalte 5 --- (Ein sehr guter Ausbildungsabschluss ist für mich sehr wichtig)
            data = self.data.iloc[:, 1:5]
            # Spalte 6 OHE --- (Geschlecht)
            temp = pd.get_dummies(pd.Categorical(self.data.iloc[:, 5], categories=["weiblich", "männlich"]), dtype=int, drop_first=True)
            data = pd.concat([data, temp], axis=1)
            # Spalte 7 --- Alter
            temp = self.data.iloc[:, 6]
            data = pd.concat([data, temp], axis=1)
            # Spalte 8 OHE --- (Aktuelle Ausbildungsrichtung)
            temp = pd.get_dummies(pd.Categorical(self.data.iloc[:, 7], categories=["kaufmännisch",
                                                                                   "gewerblich technisch"]), dtype=int,
                                  drop_first=True)
            data = pd.concat([data, temp], axis=1)
            # Spalte 9 OHE --- Reguläre Ausbildungsdauer
            temp = pd.get_dummies(pd.Categorical(self.data.iloc[:, 8], categories=["2 - 2,5-jährig",
                                                                                   "mindestens 3-jährig"]), dtype=int,
                                  drop_first=True)
            data = pd.concat([data, temp], axis=1)
            # Spalte 10 --- Aktuelle Jahrgangsstufe
            temp = self.data.iloc[:, 9]
            data = pd.concat([data, temp], axis=1)
            # Spalte 11 OHE --- Ist Ihre Muttersprache Deutsch?
            temp = pd.get_dummies(pd.Categorical(self.data.iloc[:, 10], categories=["Ja", "Nein"]), dtype=int,
                                  drop_first=True)
            data = pd.concat([data, temp], axis=1)

            # Spalte 12 OHE --- Welche größe hat das Unternehmen in welchem Sie beschäftigt sind?
            temp = pd.get_dummies(pd.Categorical(self.data.iloc[:, 11],
                                                 categories=["Ich bin derzeit in keinem Unternehmen beschäftigt",
                                                             "Kleines Unternehmen (bis 49 Personen)",
                                                             "Mittleres Unternehmen (bis 249 Personen)",
                                                             "Großunternehmen (über 249 Personen)"]), dtype=int,
                                  drop_first=True)
            data = pd.concat([data, temp], axis=1)
            # Spalte 13 OHE --- Bisherige Schulbildung
            temp = pd.get_dummies(pd.Categorical(self.data.iloc[:, 12], categories=["Mittelschulabschluss ohne Quali",
                                                                                    "Mittelschulabschluss mit Quali",
                                                                                    "Mittlere Reife Realschule",
                                                                                    "Mittlere Reife Mittelschule",
                                                                                    "Allgemeine Fachhochschulreife",
                                                                                    "Allgemeine Hochschulreife (Abitur)",
                                                                                    "Fachgebundene Fachhochschulreife"]), dtype=int,
                                  drop_first=True)
            data = pd.concat([data, temp], axis=1)
            # Spalte 14 --- Wurde Ihr Lernerfolg durch den Einsatz des digitalen Tools gefördert?
            # temp = self.data.iloc[0:self.data.shape[0], 13]
            # data = pd.concat([data, temp], axis=1)
            # Spalte 15 als Label --- Würden Sie sich einen häufigeren Einsatz digitaler Tools im Unterricht wünschen?
            # label = self.data.iloc[0:self.data.shape[0], 13]
            label = self.data.iloc[:, 14]
            # Aufteilung in Trainingsvariablen, -Daten, Testvariablen, -Daten, im Verhältnis 80/20.
            # Der random_state wurde nach erfolgreicher Optimierung der KI herausgenommen
            train_vars, test_vars, train_values, test_values = train_test_split(data, label, test_size=0.2)

            # XGBRegressor mit 150 Bäumen, einer max_depth von 5, learning_rate von 0.05 und early_stopping_rounds i.h.v. 15
            model = XGBRegressor(max_depth=5, learning_rate=0.05, n_estimators=150, early_stopping_rounds=15)

            # KI trainieren mit zwei Tabellen
            model.fit(train_vars, train_values, eval_set=[(train_vars, train_values), (test_vars, test_values)],
                      verbose=True)
            
            # KI Model speichern
            model.save_model("model.json")

            # Vorhersage für die Testvars (dritte Tabelle), Ergebnistabelle ist in predicted_values
            predicted_values = model.predict(test_vars)

            # Ausgabe der Vorhersage der KI (predicted_values) auf QTextEdit "self.KiResult"
            star = numpy.mean(predicted_values)
            self.KiResult.setText("Die ermittelte Eignung des Einsatzes des digitalen Tools in Ihrer Klasse beträgt:"
                                  "\n{:.1f} / 6 Sterne".format(star))

            # Da die Korrelationen in unserem Fall keine großen Abweichungen haben, müssen wir auch keine Spalten entfernen.
            # Der Vollständigkeit und Nachvollziehbarkeit halber bleibt dieser Block Block Bestandteil des Codes

            correlations = data[data.columns].corr()
            correlations_abs_sum = correlations[correlations.columns].abs().sum()
            # weakest_corr = correlations_abs_sum.nsmallest(5))
            print(correlations_abs_sum.nlargest(4))
