# Práctica1: Web scraping
# Descripción

Se pretende la recolección de ciertos datos de dos páginas webs relacionadas con el mundo de los coches de alta gama: Porsche y Lamborghini. Estos datos servirán para realizar un estudio de mercado. Las páginas que han sido analizadas aportan información técnica bastante detallada de cada uno de los modelos analizados.

# Miembros del equipo

La actividad ha sido realizada por Cristina Liánez López y Manuel Padrón Martínez.

# Descripción del dataset

El dataset recibe el nombre de **carsTecnicsFeatures** y los datos que contiene son los siguientes:

* **Marca**: se han analizado dos marcas Porsche y Lamborghini
* **Modelo**: modelo de coche analizado dentro de las marcas anteriores
* **altura**: dimensiones en altura del vehículo desde el suelo
* **anchoBase**: dimensiones en anchura del vehículo excluidos los espejos retrovisores
* **anchoTotal**:  dimensiones en anchura del vehículo incluidos los espejos retrovisores
* **longitud**: dimensiones de largo del vehículo
* **peso**: peso en seco o tara
* **cilindrada**: cantidad de cm3 del motor
* **consumo**: litros a los 100km de consumo medio o combinado 
* **potencia**: CV de potencia de motor
* **aceleración**: segundos que tarda en pasar de 0-100km
* **velocidadMax**: velocidad máxima que puede alcanzar en km/h
* **precio**: precio base o desde


# Ficheros del código fuente

* src/main.py: punto de entrada al programa. Inicia el proceso de scraping.
* src/scraper.py: contiene la implementación de la clase AccidentsScraper cuyos métodos generan el conjunto de datos a partir de la base de datos online PlaneCrashInfo.
* src/reason_classifier.py: contiene la implementación de la clase que se encarga de asignar una causa a un resumen de accidente dado. Para ello, utiliza la librería TextBlob.


# Recursos

* Lawson, R. (2015). Web Scraping with Python. Packt Publishing Ltd. Chapter 2. Scraping the Data.
* Mitchel, R. (2015). Web Scraping with Python: Collecting Data from the Modern Web. O'Reilly Media, Inc. Chapter 1. Your First Web Scraper.
* Muthukadan, B (2018). Selenium with Python. https://selenium-python.readthedocs.io/
