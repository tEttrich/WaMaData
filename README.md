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
![This is an image](/../main/11_Abbildungen/WaMa.jpg)
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
![Abb6-1](/../main/11_Abbildungen/Abb6-1.jpg)

Abb. 6 2 visualisiert die Messdaten eines Waschmaschinen-Zyklus. Es können vier unterschiedliche Zustände erkannt werden: (1) Leerlauf, (2) leichter Waschgang, (3) starker Waschgang und (4) Schleudergang.

Ein näherer Blick auf die Messdaten der markierten Bereiche stärkt den Eindruck. Wie in Abb. 6 2 zu sehen ist, unterscheiden sich die Ausschläge der Messdaten der vier Betriebszustände. Der Leerlauf zeigt einen ruhigen Verlauf, der Schleudergang zeigt die stärksten Ausschläge.

In Abb. 6 4 werden die Fast Fourier Transformationen der vier Betriebszustände dargestellt. Sie unterscheiden sich deutlich. Leerlauf und leichter Waschgang sehen sich zwar ähnlich, jedoch sind die Ausschläge des leichten Waschgangs im Verlauf stärker. Der starke Waschgang und der Schleudergang unterscheiden sich deutlich von den beiden vorherigen und voneinander. 

Die in Abb. 6 5 dargestellten Power-Spectral-Density verstärkt den Eindruck, dass sich vier Betriebszustände unterscheiden lassen.

## 7 Datenbankanbindung
Es kann sowohl ein lokaler MongoDB-Server oder eine MongoDB Atlas Cloud-Server genutzt werden. Es bietet sich an, einen Cloud-Server zu nutzen. Die Daten können jederzeit via Code 7 1 aus der MongoDB Atlas Cloud-Datenbank exportiert werden.
\cd C:\Program Files\MongoDB\Server\4.2\bin
\mongoexport --uri mongodb+srv://test:test@cluster1337.kv1ih.mongodb.net/ProjectData --collection Data  --out=C:\Users\Tony\Desktop\WaMaData.json

Die Daten werden als JSON-Datei auf dem Desktop abgelegt.




