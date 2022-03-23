# DLsP Projektaufgabe: Prozessüberwachung einer Waschmaschine - Dokumentation

## Inhaltsverzeichnis
1.	Prozessbeschreibung
2.	Datenerfassung
3.	Datentypee
4.	Datenmenge
5.	Datenprotokolle	
6.	Analyse	
7.	Datenbankanbindung	
8.	Datenzugänglichkeit	
9.	Benutzeroberfläche	

## 1 Prozessbeschreibung
Die verschiedenen Betriebszustände einer Waschmaschine sollen diagnostiziert werden. Hierzu wird ein IoT-Device mit einer IMU (Inertial Measurement Unit) verwendet. Die Vibrationen sind signifikant für den Betriebszustand. Die Daten sollen aufbereitet, umgewandelt, komprimiert, klassifiziert und dargestellt werden.
Zur Datenerfassung wird das IoT-Device an der Waschmaschine angebracht. Es erfasst die Vibrationen der Waschmaschine. Die Daten werden als UTF8-String via MQTT an einen Broker übermittelt. Der Broker ist mit einem MongoDB-Server verbunden. Der Broker konvertiert die Daten in ein JSON-Dict und schreibt sie in eine Collection, die auf dem MongoDB-Server liegt.
Die Daten können von Jedermann mit den Zugangsdaten vom Server abgerufen werden. Die abgerufenen Daten werden per fast Fourier Transformation und Power-Spectral-Density analysiert und visualisiert. Das Ergebnis soll in einem GUI ausgegeben werden können.

## 2 Datenerfassung
Zur Datenerfassung wird das IoT-Device an der Waschmaschine angebracht. Das IoT-Device besteht aus einem ESP8266 Microcontroller (Wemos D1 Mini) und einem MPU6050 Beschleunigungssensor und Gyroskop. Via I2C-Bus liest der Microcontroller die Daten des MPU6050. Zur Programmierung des IoT-Devices wird Micropython verwendet.

![WaMa](/../main/11_Abbildungen/WaMa.jpg)

Die Waschmaschine hat eine maximale Drehzahl von 1.200 Umdrehungen pro Minute. Zur Sicherheit sollte die Messung mit der zehnfachen Frequenz stattfinden, also mit mindestens 12.000 Messungen pro Minute bzw. 200 Hz.

## 3 Datentypen
Jeder Datensatz hat eine Größe von 121 Byte und beinhaltet 6 Variablen:
1.	dev	Name des IoT-Device		String mit 6 Zeichen
2.	dt	DateTime			String mit 19 Zeichen
3.	time	Unix epoch time		Integer mit 10 Zeichen
4.	x_a	X-Beschleunigung 		float
5.	y_a	Y-Beschleunigung		float
6.	z_a	Z-Beschleunigung		float

## 4 Datenmenge
Pro Messung werden 100 Datensätze erfasst. Jede Messung erzeugt 12.100 Byte bzw. 11,82 kB an Daten. Alle 30 Sekunden findet eine Messung statt. Pro Stunde werden bis zu 1.452.000 Byte bzw. 1,38 mB Daten erzeugt. Pro Tag würde eine Datenmenge von bis zu 33,23 mB anfallen.

## 5 Datenprotokolle
Das IoT-Device übermittelt die Daten per MQTT-Protokoll als UTF8-String an den Broker. Es hat sich herausgestellt, dass das MQTT-Protokoll zu langsam ist, um Daten in einer Geschwindigkeit von 200 Hz zu senden. Die Frequenz zur Messung wurde auf 100 Hz reduziert. Da die immer noch fünfmal so hoch wie die maximale Drehzahl der Waschmaschine ist, könnten trotzdem geeignete Messwerte ohne Aliasing erfasst werden.

## 6 Analyse
Abb. 6-1 zeigt den Plot aller Messdaten. Es wird deutlich, dass es unterschiedliche Zustände gibt.

![Abb6-1](/../main/11_Abbildungen/Abb6-1.png)

Abb. 6 2 visualisiert die Messdaten eines Waschmaschinen-Zyklus. Es können vier unterschiedliche Zustände erkannt werden: (1) Leerlauf, (2) leichter Waschgang, (3) starker Waschgang und (4) Schleudergang.

![Abb62](/../main/11_Abbildungen/Abb62.png)

Ein näherer Blick auf die Messdaten der markierten Bereiche stärkt den Eindruck. Wie in Abb. 6 3 zu sehen ist, unterscheiden sich die Ausschläge der Messdaten der vier Betriebszustände. Der Leerlauf zeigt einen ruhigen Verlauf, der Schleudergang zeigt die stärksten Ausschläge.

![Abb63](/../main/11_Abbildungen/Abb63.png)

In Abb. 6 4 werden die Fast Fourier Transformationen der vier Betriebszustände dargestellt. Sie unterscheiden sich deutlich. Leerlauf und leichter Waschgang sehen sich zwar ähnlich, jedoch sind die Ausschläge des leichten Waschgangs im Verlauf stärker. Der starke Waschgang und der Schleudergang unterscheiden sich deutlich von den beiden vorherigen und voneinander. 

![Abb64](/../main/11_Abbildungen/Abb64.png)

Die in Abb. 6 5 dargestellten Power-Spectral-Density verstärkt den Eindruck, dass sich vier Betriebszustände unterscheiden lassen.

![Abb65](/../main/11_Abbildungen/Abb65.png)

## 7 Klassifizierung
Die Klassifizierung findet mittels KMeans statt. KMeans wird unächst mit allen bisherigen Daten via `KMeans(n_clusters 0 4).fit(df_train)` trainiert. Abb. 7 1 veranschaulicht die Klassifizierung.

![101](/../main/11_Abbildungen/101.png)

Neu aufgezeichnete Daten oder ein beliebiger Datensatz können zur Klassifzierung übergeben werden. Mittels `KMeans().fit_predict(df_test)` findet die Klassifizierung des Datnesatzes statt. Abb. 7 2 veranschaulicht die Klassifizierung.

![103](/../main/11_Abbildungen/103.png)

## 8 Datenbankanbindung
Es kann sowohl ein lokaler MongoDB-Server oder eine MongoDB Atlas Cloud-Server genutzt werden. Es bietet sich an, einen Cloud-Server zu nutzen. Die Daten können jederzeit via Code 8 1 aus der MongoDB Atlas Cloud-Datenbank exportiert werden.
`cd C:\Program Files\MongoDB\Server\4.2\bin`
`mongoexport --uri mongodb+srv://test:test@cluster1337.kv1ih.mongodb.net/ProjectData --collection Data  --out=C:\Users\Tony\Desktop\WaMaData.json`
Die Daten werden als JSON-Datei auf dem Desktop abgelegt.

## 9 Datenzugänglichkeit
Auf die Daten kann mit den folgenden Informationen zugegriffen werden:
- URI           `mongodb+srv://test:test@cluster1337.kv1ih.mongodb.net/ProjectData`
- Dataset       `ProjectData`
- Collection    `Data`

## 10 Benutzeroberfläche
Die Benutzeroberfläche wird mit Qt generiert. In einem ersten Schritt sollen die Daten vom MongoDB Atlas Cloud-Server abgerufen werden. Die Daten werden in einen Pandas Dataframe geschrieben, um effizient verarbeitet werden zu können.

![Abb91](/../main/11_Abbildungen/Abb91.png)

Per *Daten > importieren* lassen sich die Daten vom MongoDB-Server abrufen (vgl. Abb. 10 1). Die Statusausgabe gibt *„Dataframe erfolgreich erstellt.“* aus, sobald das Dataframe erstellt ist (vgl. Abb. 10 2).

![Abb91](/../main/11_Abbildungen/Abb92.png)

In einem nächsten Schritt sollen die Daten visualisiert werden. Der Nutzer mit per *Daten > aktualisieren* (vgl. Abb. 10 1). die Möglichkeit haben, den Betrachtungszeitraum des Dataframes einzugrenzen. Dazu können Start und Ende des Betrachtungszeitraums in einem Dialogfenster mit Datum und Uhrzeit festgelegt werden.

![Abb93](/../main/11_Abbildungen/Abb93.png)

Anhand der Daten soll das Dataframe gefiltert werden. Daraus sollen die Analysen zum Betrachtungszeitraum angestellt und visualisiert werden.

