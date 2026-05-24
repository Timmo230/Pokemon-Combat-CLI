# Pokemon Combat

Juego de combate por turnos en terminal inspirado en Pokemon. Obtiene datos de los Pokemon mediante scraping web y guarda una cache local en `todos_los_pokemons.pkl` para no descargar todo en cada ejecucion.

## Requisitos

- Python 3.12 o compatible
- Conexion a internet la primera vez que se ejecuta

## Instalacion

Desde la carpeta del proyecto:

```bash
cd "/home/matias/Escritorio/pokemon/pokemonProyect"
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
- El juego debe ejecutarse desde esta carpeta para que la cache se lea y se escriba en la ruta esperada.
