from random import choice


POKEMON_BASE = {
    "name": "",
    "type": None,
    "attacks": None,
    "current_health": 100,
    "base_health": 100,
    "level": 1,
    "current_exp": 0,
    "numero_pokedex": 0,
    "next_evolution": "",
    "level_needed_to_evolution": 0,
}

DEBILITYS_TEXT = (
    "Acero: Lucha, Fuego, Tierra\n"
    "Agua: Planta, Electrico\n"
    "Bicho: Volador, Fuego, Roca\n"
    "Dragon: Hada, Hielo, Dragon\n"
    "Electrico: Tierra\n"
    "Fantasma: Fantasma, Siniestro\n"
    "Fuego: Tierra, Agua, Roca\n"
    "Hada: Acero, Veneno\n"
    "Hielo: Lucha, Acero, Roca, Fuego\n"
    "Lucha: Psiquico, Volador, Hielo\n"
    "Normal: Lucha\n"
    "Planta: Volador, Bicho, Veneno, Hielo, Fuego\n"
    "Psíquico: Bicho, Fantasma, Siniestro\n"
    "Roca: Lucha, Tierra, Acero, Agua, Planta\n"
    "Siniestro: Lucha, Hada, Bicho\n"
    "Tierra: Agua, Planta, Hielo\n"
    "Veneno: Tierra, Psiquico\n"
    "Volador: Roca, Hielo, Electrico"
)


def create_pokemon_base():
    return POKEMON_BASE.copy()


def create_player_profile(all_pokemons, player_name="Matias"):
    return {
        "player_name": player_name,
        "pokemon_inventary": [choice(all_pokemons) for _ in range(3)],
        "combats": 0,
        "pokebals": 1,
        "health_potion": 1,
        "battle_history": [],
    }
