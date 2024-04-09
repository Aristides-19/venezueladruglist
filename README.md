[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![rapid-fuzz](https://img.shields.io/badge/Rapid-Fuzz-purple.svg)](https://github.com/seatgeek/thefuzz/tree/master)
[![beautiful-soup](https://img.shields.io/badge/Beautiful-Soup-red.svg)](https://pypi.org/project/beautifulsoup4/)

Este repositorio contiene un archivo JSON de la lista de medicamentos esenciales que son comercializados en Venezuela.
La lista fue obtenida a partir de la información de venta que se muestran en las principales farmacias del país y la lista SAFER.
Se puede visualizar con más detalle en `src/input/...`.

El objetivo es proporcionar una lista completa y fiable que mencione aquellos medicamentos que pueden ser comercializados en el país,
además de poder utilizarla como base para proyectos de clasificación, búsqueda o análisis.

## Uso y Actualización de Datos
Los datos son públicos y están dispuestos para su uso en cualquier tipo de proyecto, así también el repositorio está abierto a cualquier **contribución** para mejorar la precisión, amplitud y tamaño de los datos.

La información puede ser recuperada haciendo una petición GET a [medicamentos.json](https://raw.githubusercontent.com/Aristides-19/venezueladruglist/main/medicamentos.json). 

```python
import requests

var = requests.get('https://raw.githubusercontent.com/Aristides-19/venezueladruglist/main/medicamentos.json')
```

## Script de Procesamiento de Datos
Los datos fueron procesados en el script `src/app.py`, se utilizó BeautifulSoup para extraerlos de páginas farmaceúticas públicas, 
así como el uso de expresiones regulares y NumPy para la eliminación de duplicados, luego fueron exportados a `medicamentos.json`.

## License
Este proyecto está licenciado bajo la Licencia MIT - vea el archivo `LICENSE` para más detalles.
