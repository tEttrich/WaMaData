import createDataframe

import sys
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QDialog
from PySide6.QtCore import QFile, QIODevice


def datenImportieren():
    w.labelStatus.setText("Importiere Daten von MongoDB Atlas. Bitte warten!")
    df = createDataframe.createDF()
    w.labelStatus.setText("Dataframe erfolgreich erstellt.")
    return df

def chartAktualisieren():
    d = loader.load(QFile("dialogChartAktualisieren.ui"))
    if d.exec() == QDialog.Accepted:
        dateTimeStart = d.dateTimeStart.dateTime().toSecsSinceEpoch()
        dateTimeEnde = d.dateTimeEnde.dateTime().toSecsSinceEpoch()
        print(dateTimeStart, dateTimeEnde)

        query = {'time':{"$lte":dateTimeEnde, "$gte":dateTimeStart}}
        data = dbOperations.get_multiple_data(query)
        print(len(data), type(data))
        return data


if __name__ == "__main__":
    app = QApplication(sys.argv)

    ui_file_name = "mainwindow.ui"
    ui_file = QFile(ui_file_name)
    if not ui_file.open(QIODevice.ReadOnly):
        print(f"Cannot open {ui_file_name}: {ui_file.errorString()}")
        sys.exit(-1)
    loader = QUiLoader()
    w = loader.load(ui_file)
    ui_file.close()
    if not w:
        print(loader.errorString())
        sys.exit(-1)

    w.show()

    w.actionAktualisieren.triggered.connect(chartAktualisieren)
    df = w.actionImportieren.triggered.connect(datenImportieren)
    # data = w.actionAktualisieren.triggered.connect(chartAktualisieren)
    # data = w.buttonAktualisieren.clicked.connect(chartAktualisieren)
    #w.connect(w.buttonAktualisieren, SIGNAL('clicked()'), chartAktualisieren())
    #datenImportieren()
    #w.connect(w.dabeiBeenden, SIGNAL('triggered()'), )


    sys.exit(app.exec())
