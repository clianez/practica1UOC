# Práctica1: Web scraping
# Descripción.

Se pretende la recolección de ciertos datos de dos páginas webs relacionadas con el mundo de los coches de alta gama: Porsche y Lamborghini. Estos datos servirán para realizar un estudio de mercado. Las páginas que han sido analizadas aportan información técnica bastante detallada de cada uno de los modelos analizados.

# Miembros del equipo.

La actividad ha sido realizada por Cristina Liánez López y Manuel Padrón Martínez.

# Dependencias.

El código está pensado para ser ejecutado en python 3. Con las siguientes dependencias:
* Para hacer el scraping de las webs, se ha utilizado selenium.

# Ficheros del código fuente.

* **src/main.py**: punto de entrada al programa. Creación del dataset.
* **src/porsche.py**: realiza scraping en la página de Porsche.
* **src/scrapingLambo.py**: realiza scraping en la página de Lamborghini.

# Instalación de dependencias y ejecución del código.

1. Descargar el repositorio.
1. Instalar las dependencias.
```
pip3 install selenium
```
3. En el directorio src ejecutar el programa main.
```
python main.py
```



# Recursos.

* Lawson, R. (2015). Web Scraping with Python. Packt Publishing Ltd. Chapter 2. Scraping the Data.
* Mitchel, R. (2015). Web Scraping with Python: Collecting Data from the Modern Web. O'Reilly Media, Inc. Chapter 1. Your First Web Scraper.
* Muthukadan, B (2018). Selenium with Python. https://selenium-python.readthedocs.io/
