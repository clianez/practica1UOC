# -*- coding: utf-8 -*-
from scrapingLambo import scrapingLambo
from porsche import scrapingPorsche
import csv

# Cabeceras para el fichero csv
header = [['marca', 'modelo', 'altura', 'anchoBase', 'anchoTotal', 'longitud', 'peso',
           'cilindrada', 'consumo', 'potencia', 'aceleracion', 'velocidadMax', 'precio']]

# Hace el scraping de Lamborghini
lambo = scrapingLambo()

# Hace el scraping de Porsche
porsche = scrapingPorsche()

with open('../csv/carsTecnicsFeatures.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(header)
    writer.writerows(lambo)
    writer.writerows(porsche)
