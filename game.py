from os import name as os_name
from os import system
from random import choice, randint
from time import sleep

from models import create_player_profile
from scraper import get_all_pokemons, get_debilitys


def get_exp(profile, pokemons_used, all_pokemons):
    for i in range(len(profile["pokemon_inventary"])):
        amount_of_this_pokemon = pokemons_used.count(profile["pokemon_inventary"][i])

        for _ in range(amount_of_this_pokemon):
            profile["pokemon_inventary"][i]["current_exp"] += randint(3, 6)
        pokemon_inventary_copy = profile["pokemon_inventary"][i].copy()

        profile["pokemon_inventary"][i]["level"] += int(profile["pokemon_inventary"][i]["current_exp"] / 10)
        profile["pokemon_inventary"][i]["current_exp"] = int(profile["pokemon_inventary"][i]["current_exp"] % 10)

        if (
            profile["pokemon_inventary"][i]["name"] == pokemon_inventary_copy["name"]
            and profile["pokemon_inventary"][i]["level"] != pokemon_inventary_copy["level"]
        ):
            profile["pokemon_inventary"][i]["current_health"] = profile["pokemon_inventary"][i]["base_health"]
            print("{} ha subido a nivel {}".format(profile["pokemon_inventary"][i]["name"], profile["pokemon_inventary"][i]["level"]))
        if (
            pokemon_inventary_copy["next_evolution"] != None
            and profile["pokemon_inventary"][i]["name"] == pokemon_inventary_copy["name"]
            and profile["pokemon_inventary"][i]["level"] != pokemon_inventary_copy["level"]
            and pokemon_inventary_copy["level"] < pokemon_inventary_copy["level_needed_to_evolution"]
            and profile["pokemon_inventary"][i]["level"] >= pokemon_inventary_copy["level_needed_to_evolution"]
        ):
            pokemon_inventary_copy = profile["pokemon_inventary"][i].copy()
            profile["pokemon_inventary"][i] = all_pokemons[profile["pokemon_inventary"][i]["numero_pokedex"]]

            profile["pokemon_inventary"][i]["current_exp"] = pokemon_inventary_copy["current_exp"]
            profile["pokemon_inventary"][i]["level"] = pokemon_inventary_copy["level"]

            print("{} ha evolucionado a {}".format(pokemon_inventary_copy["name"], profile["pokemon_inventary"][i]["name"]))

    return profile["pokemon_inventary"]


def get_object(profile):
    random_number = randint(1, 100)

    if random_number <= 40:
        if random_number <= 20:
            profile["health_potion"] += 1
            print("Has conseguido una pocion")
        else:
            profile["pokebals"] += 1
            print("Has conseguido una pokeball")
    return profile


def get_player_profile(all_pokemons):
    return create_player_profile(all_pokemons)


def any_pokemon_lives(profile):
    return sum([pokemon["current_health"] for pokemon in profile["pokemon_inventary"]]) > 0


def convert_types_in_string(pokemon):
    types_to_print = ""
    for types in pokemon["type"]:
        if types_to_print != "":
            types_to_print += ", "
        types_to_print += types
    return types_to_print


def create_life_bar(profile, BAR_SIZE, pokemon_enemy, active_pokemon):
    system("cls" if os_name == "nt" else "clear")
    asteriscos_pokemon_enemy = int(pokemon_enemy["current_health"] * BAR_SIZE / pokemon_enemy["base_health"])
    asteriscos_my_pokemon = int(active_pokemon["current_health"] * BAR_SIZE / active_pokemon["base_health"])

    pokeon_types = convert_types_in_string(pokemon_enemy)
    print(
        "Vida enemigo {} = [{}{}]{}/{} ¦ Tipo: {}\n".format(
            pokemon_enemy["name"],
            "#" * asteriscos_pokemon_enemy,
            " " * (BAR_SIZE - asteriscos_pokemon_enemy),
            pokemon_enemy["current_health"],
            pokemon_enemy["base_health"],
            pokeon_types,
        )
    )
    pokeon_types = convert_types_in_string(active_pokemon)
    print(
        "Vida tu {} = [{}{}]{}/{} ¦ Tipo: {}\n".format(
            active_pokemon["name"],
            "#" * asteriscos_my_pokemon,
            " " * (BAR_SIZE - asteriscos_my_pokemon),
            active_pokemon["current_health"],
            active_pokemon["base_health"],
            pokeon_types,
        )
    )


def damage_with_debilitys(debilitys, pokemon_attacked, attack_received):
    multiplier = 0
    for types in pokemon_attacked["type"]:
        for row in debilitys:
            if types.lower() == row[0].lower():
                for pokemon_type in row[1]:
                    if attack_received["type"] == pokemon_type.lower():
                        multiplier += 1.25

    if multiplier == 0:
        damage_caused = attack_received["damage"]
    else:
        damage_caused = attack_received["damage"] * multiplier

    return damage_caused


def enemy_turn_action(pokemon_enemy, active_pokemon, debilitys):
    print("Turno enemigo:\n\nAtaque utilizado:")
    attack_index = randint(0, len(pokemon_enemy["attacks"]) - 1)
    print(pokemon_enemy["attacks"][attack_index]["name"])

    damage_caused = damage_with_debilitys(debilitys, active_pokemon, pokemon_enemy["attacks"][attack_index])
    print("Te ha quitado {} de salud a {}".format(damage_caused, active_pokemon["name"]))

    active_pokemon["current_health"] -= damage_caused
    input("Seleccione enter para continuar...")

    return active_pokemon["current_health"]


def my_turn_action(profile, pokemon_enemy, active_pokemon, BAR_SIZE, debilitys):
    valid_input = []
    attack_used = ""

    attacks_definitives = []
    for attack in active_pokemon["attacks"]:
        if active_pokemon["level"] >= attack["min_level"]:
            attacks_definitives.append(attack)

    while attack_used not in valid_input:
        counter = 1
        if attacks_definitives == []:
            print("Tu pokemon no tiene suficiente nivel para acceder a ")
            input("Seleccione enter para continuar...")
            break
        else:
            for attack in attacks_definitives:
                print("{}.- {} ¦ Tipo: {} ¦ Poder: {}".format(counter, attack["name"], attack["type"], attack["damage"]))
                valid_input.append(str(counter))
                counter += 1
            attack_used = input("Seleccione el indice del ataque: ")

            if attack_used not in valid_input:
                create_life_bar(profile, BAR_SIZE, pokemon_enemy, active_pokemon)

    print("Ataque utilizado: {}".format(active_pokemon["attacks"][int(attack_used) - 1]["name"]))
    reduced_life = damage_with_debilitys(debilitys, pokemon_enemy, active_pokemon["attacks"][int(attack_used) - 1])
    print("\nHas quitado {} de salud a {}".format(reduced_life, pokemon_enemy["name"]))

    pokemon_enemy["current_health"] -= reduced_life

    input("Seleccione enter para continuar...")
    return pokemon_enemy


def choose_pokemon(profile, BAR_SIZE, pokemon_enemy, active_pokemon, action="utilizar"):
    valid_input = []
    pokemon_used = ""
    while pokemon_used not in valid_input or (
        profile["pokemon_inventary"][int(pokemon_used) - 1]["current_health"] <= 0 and action == "utilizar"
    ):
        if active_pokemon is not None:
            create_life_bar(profile, BAR_SIZE, pokemon_enemy, active_pokemon)
        print("Elije el pokemon que quieres {}: ".format(action))
        counter = 1
        for pokemon in profile["pokemon_inventary"]:
            if profile["pokemon_inventary"][counter - 1]["current_health"] <= 0:
                print("{}.- {} ¦ MUERTO".format(counter, pokemon["name"]))
            else:
                types_to_print = convert_types_in_string(pokemon)
                print(
                    "{}.- {} - {}/{} ¦ Tipo: {}¦ Nivel: {} ¦ EXP: {}".format(
                        counter,
                        pokemon["name"],
                        pokemon["current_health"],
                        pokemon["base_health"],
                        types_to_print,
                        pokemon["level"],
                        pokemon["current_exp"],
                    )
                )
            valid_input.append(str(counter))
            counter += 1
        pokemon_used = input("Seleccione el indice del pokemon: ")

        system("cls" if os_name == "nt" else "clear")
        if (
            (pokemon_used not in valid_input or profile["pokemon_inventary"][int(pokemon_used) - 1]["current_health"] <= 0)
            and active_pokemon is not None
        ):
            create_life_bar(profile, BAR_SIZE, pokemon_enemy, active_pokemon)

    return profile["pokemon_inventary"][int(pokemon_used) - 1]


def choose_action(profile, BAR_SIZE, pokemon_enemy, active_pokemon):
    action = None
    while action not in ["A", "C", "P", "V", "M"]:
        create_life_bar(profile, BAR_SIZE, pokemon_enemy, active_pokemon)
        action = input(
            "Que quieres hacer?\n"
            "A = Atacar\n"
            "C = Cambiar pokemon\n"
            "P = Lanzar pokemon\n"
            "V = Pocion de vida\n"
            "M = Menu\n"
        )
    return action


def throw_pokeball(profile, enemy_pokemon):
    if profile["pokebals"] > 0:
        probability = 100 - (100 * enemy_pokemon["current_health"] / enemy_pokemon["base_health"])

        if randint(1, 100) <= probability * 2:
            print("{} ha entrado en la pokeball...".format(enemy_pokemon["name"]))
            sleep(1)
            if randint(1, 100) <= probability * 1.5:
                print("{} parece que se ha capturado...".format(enemy_pokemon["name"]))
                sleep(1)
                if randint(1, 100) <= probability:
                    print("{} se ha capturado".format(enemy_pokemon["name"]))
                    input("Seleccione enter para continuar...")
                    return True
                else:
                    print("{} salio de la pokeball".format(enemy_pokemon["name"]))
                    input("Seleccione enter para continuar...")
                    return False
            else:
                print("{} salio de la pokeball".format(enemy_pokemon["name"]))
                input("Seleccione enter para continuar...")
                return False
        else:
            print("{} esquivo la pokeball".format(enemy_pokemon["name"]))
            input("Seleccione enter para continuar...")
            return False
    else:
        print("No tienes pokeballs, has perdido el turno")


def heal_pokemon(profile, BAR_SIZE, pokemon_enemy, active_pokemon):
    system("cls" if os_name == "nt" else "clear")
    create_life_bar(profile, BAR_SIZE, pokemon_enemy, active_pokemon)
    pokemon_to_heal = choose_pokemon(profile, BAR_SIZE, pokemon_enemy, active_pokemon, "curar")
    if profile["health_potion"] > 0:
        pokemon_to_heal["current_health"] += 10

        if pokemon_to_heal["current_health"] > pokemon_to_heal["base_health"]:
            pokemon_to_heal["current_health"] = pokemon_to_heal["base_health"]
    else:
        print("No tienes pociones, has perdido el turno")
        input("Seleccione enter para continuar...")

    return pokemon_to_heal


def go_menu(profile, BAR_SIZE, pokemon_enemy, active_pokemon):
    action = None
    while action != "Q":
        counter = 1
        create_life_bar(profile, BAR_SIZE, pokemon_enemy, active_pokemon)
        action = input(
            "Que quieres hacer?\n"
            "I = Inventario\n"
            "P = Ver pokemon\n"
            "V = ver combates realizados\n"
            "Q = Volver al combate\n"
        )

        if action == "I":
            print("Inventario:\nPokeballs: {}\nPociones: {}\n".format(profile["pokebals"], profile["health_potion"]))
        elif action == "P":
            for pokemon in profile["pokemon_inventary"]:
                if profile["pokemon_inventary"][counter - 1]["current_health"] <= 0:
                    print("{}.- {} ¦ MUERTO".format(counter, pokemon["name"]))
                else:
                    types_to_print = convert_types_in_string(pokemon)
                    print(
                        "{}.- {} - {}/{} ¦ Tipo: {}¦ Nivel: {} ¦ EXP: {}".format(
                            counter,
                            pokemon["name"],
                            pokemon["current_health"],
                            pokemon["base_health"],
                            types_to_print,
                            pokemon["level"],
                            pokemon["current_exp"],
                        )
                    )
                counter += 1
        elif action == "V":
            [print("Combate numero {}: {}".format(i + 1, profile["battle_history"][i])) for i in range(len(profile["battle_history"]))]
        elif action == "Q":
            return None
        else:
            print("Opcion no valida")

        input("Seleccione enter para continuar...")


def actions(profile, action, BAR_SIZE, pokemon_enemy, active_pokemon, debilitys):
    breaker = False
    if action == "A":
        create_life_bar(profile, BAR_SIZE, pokemon_enemy, active_pokemon)
        pokemon_enemy = my_turn_action(profile, pokemon_enemy, active_pokemon, BAR_SIZE, debilitys)
        if pokemon_enemy["current_health"] < 0:
            pokemon_enemy["current_health"] = 0
    elif action == "C":
        active_pokemon = choose_pokemon(profile, BAR_SIZE, pokemon_enemy, active_pokemon)
    elif action == "P":
        capture = throw_pokeball(profile, pokemon_enemy)
        if profile["pokebals"] > 0:
            profile["pokebals"] -= 1

        if capture:
            profile["pokemon_inventary"].append(pokemon_enemy)
            breaker = True
    elif action == "V":
        pokemon_healed = heal_pokemon(profile, BAR_SIZE, pokemon_enemy, active_pokemon)
        profile["health_potion"] -= 1
        for pokemon in profile["pokemon_inventary"]:
            if pokemon["name"] == pokemon_healed["name"] and pokemon["current_health"] + 10 == pokemon_healed["base_health"]:
                pokemon["current_health"] = pokemon_healed["current_health"]
                break
    elif action == "M":
        go_menu(profile, BAR_SIZE, pokemon_enemy, active_pokemon)

    return [profile, pokemon_enemy, active_pokemon, breaker]


def fight(profile, pokemon_enemy, debilitys, all_pokemons):
    system("cls" if os_name == "nt" else "clear")
    BAR_SIZE = 20

    pokemons_used = []
    active_pokemon = choose_pokemon(profile, BAR_SIZE, pokemon_enemy, None)

    enemy_turn = True
    while any_pokemon_lives(profile) and pokemon_enemy["current_health"] > 0:
        system("cls" if os_name == "nt" else "clear")
        create_life_bar(profile, BAR_SIZE, pokemon_enemy, active_pokemon)

        if not enemy_turn:
            active_pokemon["current_health"] = enemy_turn_action(pokemon_enemy, active_pokemon, debilitys)
            if active_pokemon["current_health"] < 0:
                active_pokemon["current_health"] = 0
            enemy_turn = True
        else:
            action = None
            if active_pokemon["current_health"] <= 0:
                active_pokemon = choose_pokemon(profile, BAR_SIZE, pokemon_enemy, active_pokemon)
            while action not in ["A", "C", "P", "V"]:
                action = choose_action(profile, BAR_SIZE, pokemon_enemy, active_pokemon)
                profile, pokemon_enemy, active_pokemon, breaker = actions(
                    profile, action, BAR_SIZE, pokemon_enemy, active_pokemon, debilitys
                )

            pokemons_used.append(active_pokemon)
            if breaker:
                break
            enemy_turn = False

        for pokemon in profile["pokemon_inventary"]:
            if pokemon == active_pokemon:
                pokemon["current_health"] = active_pokemon["current_health"]
                break

    create_life_bar(profile, BAR_SIZE, pokemon_enemy, active_pokemon)
    print("---   SE ACABO EL COMBATE   ---")

    if not any_pokemon_lives(profile):
        print("Has perdido")
    else:
        print("Has ganado")
        profile["combats"] += 1
        profile = get_object(profile)
        profile["pokemon_inventary"] = get_exp(profile, pokemons_used, all_pokemons)
        profile["battle_history"].append(pokemon_enemy["name"])
    input("Seleccione enter para continuar...")

    return profile


def main():
    debilitys = get_debilitys()
    all_pokemons = get_all_pokemons()

    profile = get_player_profile(all_pokemons)

    while any_pokemon_lives(profile):
        pokemon_enemy = choice(all_pokemons)
        profile = fight(profile, pokemon_enemy, debilitys, all_pokemons)

    print("Has perdido en el combate numero {}".format(profile["combats"]))
    print("Historial de combates:")
    [print("Combate numero {}: {}".format(i + 1, profile["battle_history"][i])) for i in range(len(profile["battle_history"]))]


if __name__ == "__main__":
    main()
