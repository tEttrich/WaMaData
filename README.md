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
