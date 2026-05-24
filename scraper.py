import pickle
from pathlib import Path

from requests_html import HTMLSession

from models import DEBILITYS_TEXT, create_pokemon_base


URL_BASE = "https://pokexperto.net/index2.php?seccion=nds/nationaldex/movimientos_nivel&pk="
URL_FOR_STATS = "https://pokexperto.net/index2.php?seccion=nds/nationaldex/stats&pk="
POKEDEX_FILE = Path(__file__).resolve().parent / "todos_los_pokemons.pkl"


def get_pokemon(index):
    url = "{}{}".format(URL_BASE, index)

    session = HTMLSession()
    pokemon_page = session.get(url)

    pokemon_new = create_pokemon_base()
    pokemon_name = pokemon_page.html.find(".mini", first=True).text
    pokemon_new["name"] = pokemon_name.split("\n")[0]

    types = []
    for img in pokemon_page.html.find(".pkmain", first=True).find(".bordeambos", first=True).find("td", first=True).find("img"):
        types.append(img.attrs["alt"])

    pokemon_new["type"] = types
    pokemon_new["numero_pokedex"] = index

    pokemon_attacks = []

    for attack in pokemon_page.html.find(".pkmain")[-1].find("tr .check3"):
        try:
            attack_stats = {
                "name": attack.find("td")[0].text.split("\n")[0],
                "type": attack.find("td")[1].find("img", first=True).attrs["alt"],
                "min_level": int(attack.find("th")[1].text),
                "damage": int(attack.find("td")[3].text.replace("--", "0")),
            }
        except ValueError:
            continue

        pokemon_attacks.append(attack_stats)

    pokemon_new["attacks"] = pokemon_attacks

    url = "{}{}".format(URL_FOR_STATS, index)
    pokemon_page = session.get(url)

    pokemon_health = pokemon_page.html.find("table .pkmain")[3].find(
        ".bordeambos", first=True
    ).find("tr")[1].find(".right")[0].text
    pokemon_new["base_health"] = int(pokemon_health)
    pokemon_new["current_health"] = int(pokemon_health)

    return pokemon_new


def get_evolutions(all_pokemons):
    sumador = 0
    for pokemon_index in range(len(all_pokemons)):
        url = "https://www.pkparaiso.com/pokemon/lista-evoluciones.php"
        session = HTMLSession()
        pokemon_page = session.get(url)

        pokemon = None
        pokemon_fase = None
        if pokemon_index not in [104, 105, 133, 134]:
            while int(pokemon_page.html.find("div")[122].find("span")[pokemon_index * 2 + sumador].text[1:4]) != all_pokemons[pokemon_index]["numero_pokedex"]:
                sumador += 2

            pokemon = pokemon_page.html.find("div")[122].find("span")[pokemon_index * 2 + sumador].text[5:]
            pokemon_fase = pokemon_page.html.find("div")[122].find("span")[pokemon_index * 2 + 1 + sumador].text

            if pokemon_fase == "Fase inicial":
                next_fase = pokemon_page.html.find("div")[122].find("span")[pokemon_index * 2 + 3 + sumador].text.split(" ")[-1]
                next_pokemon = pokemon_page.html.find("div")[122].find("span")[pokemon_index * 2 + 2 + sumador].text[5:]

                try:
                    pokemon_fase = int(next_fase)
                    pokemon = next_pokemon
                except ValueError:
                    pokemon = None
                    pokemon_fase = None
            else:
                try:
                    pokemon_fase = int(pokemon_fase.split(" ")[-1])
                    pokemon_fase = int(pokemon_page.html.find("div")[122].find("span")[pokemon_index * 2 + 3 + sumador].text.split(" ")[-1])
                    pokemon = pokemon_page.html.find("div")[122].find("span")[pokemon_index * 2 + 2 + sumador].text[5:]

                except ValueError:
                    pokemon = None
                    pokemon_fase = None

            all_pokemons[pokemon_index]["next_evolution"] = pokemon
            all_pokemons[pokemon_index]["level_needed_to_evolution"] = pokemon_fase

        print("Aniadiendo evoluciones: numero: {} Pokemon: {} Nivel {}".format(pokemon_index, pokemon, pokemon_fase))
    return all_pokemons


def get_all_pokemons():
    all_pokemons = []
    try:
        with open(POKEDEX_FILE, "rb") as pokedex:
            all_pokemons = pickle.load(pokedex)
    except FileNotFoundError:
        print("Cargando todos los pokemons")
        for i in range(1, 151):
            all_pokemons.append(get_pokemon(i))
            print(i)
        all_pokemons = get_evolutions(all_pokemons)
        with open(POKEDEX_FILE, "wb") as pokedex:
            pickle.dump(all_pokemons, pokedex)
    return all_pokemons


def get_debilitys():
    definity_list = []
    list_debilitys = DEBILITYS_TEXT.split("\n")
    list_debilitys = [row.split(": ") for row in list_debilitys]
    for row in list_debilitys:
        provisional_list = row[1].split(", ")
        definity_list.append([row[0], provisional_list])
    return definity_list


if __name__ == "__main__":
    get_all_pokemons()
    get_debilitys()
