# Pokemon Combat

Juego de combate por turnos en terminal inspirado en Pokemon. Obtiene datos de los Pokemon mediante scraping web y guarda una cache local en `todos_los_pokemons.pkl` para no descargar todo en cada ejecucion.

## Requisitos

- Python 3.12 o compatible
- Conexion a internet la primera vez que se ejecuta

## Instalacion

Desde la carpeta del proyecto:

```bash
cd ruta/al/proyecto
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Ejecucion

Con el entorno activado:

```bash
python3 pokemon_combat.py
```

Tambien puedes ejecutarlo sin activar el entorno:

```bash
./.venv/bin/python3 pokemon_combat.py
```

## Notas

- La primera ejecucion puede tardar porque genera `todos_los_pokemons.pkl`.
- El juego puede ejecutarse desde cualquier ubicacion si usas `main.py` o `pokemon_combat.py` dentro de la carpeta del proyecto.
