"""
Das ist die Minesweeper Lösung für die Konsole.
Diese Lösung benutzt Klassen.
"""

from world import World

import logging
logging.basicConfig(level=logging.DEBUG, format='\n%(levelname)s: %(message)s\n')

def print_instructions():
    """
    Gibt die Anweisungen auf der Konsole
    """
    print("======================================================")
    print("Anweisungen:")
    print("1. Gib die Reihe und die Spalte an, z.B. '2 3'")
    print("2. Um eine Flage zu setzten, gib noch ein 'F' ein, z.B. '2 3 F'")


def create_world():
    """Diese Funktion erstellt eine Standard oder Custom World!

    Returns:
        world: Das Board
    """
    try:
        print('Gib die Dimensionen ein oder drücke `Enter` um ein klassisches Spiel zu starten!')
        n_row   = int(input('Gib die Anzahl an Zeilen  ein: '))
        n_col   = int(input('Gib die Anzahl an Spalten ein: '))
        n_bombs = int(input('Gib die Anzahl an Bomben  ein: '))

    except Exception:
        logging.info('Classic Settings!')
        return World()
    
    else:
        logging.info('Custom Settings!')
        return World(n_row, n_col, n_bombs)

def start():

    world = create_world()

    game_over = False

    while not game_over:

        print(world)
        print_instructions()

        try:
            user_input = input("\nGib die Reihe und die Spalte an:  ").split()
            row, col = int(user_input[0]), int(user_input[1])

            assert row < world.height and col < world.width

        except Exception:
            logging.error('Falscher Input!')
        
        # Flage setzten oder entfernen
        if len(user_input) == 3 and user_input[2].lower() == 'f':
            world.set_flag(row, col)
        
        # Feld öffnen
        if len(user_input) == 2:
            
            world.open_field(row, col)

            if world[row, col].flag:  # Man muss den Flag erst entfernen!
                continue

            if world[row, col].is_bomb():
                print("GAME OVER!!!")
                game_over = True
                print(world)

        # Sollten alle Felder aufgedeckt sein, dann GEWONNEN
        if world.check_victory():
            print("Gewonnen!")
            game_over = True
            print(world)

#---------------------------------------#

while True:

    start()

    usr = input('Willst du nochmal spielen [j/n]\n').lower()
    
    if usr == 'n':
        print('Auf Wiedersehen! :D')
        break

#---------------------------------------#