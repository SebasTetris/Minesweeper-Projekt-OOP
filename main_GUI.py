"""
Das ist die Minesweeper Lösung für die GUI.
"""

from PIL import ImageTk, Image
from world import World

import tkinter as tk
import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
import os  # Wird benötigt, um den Pfad dynamisch zu ermitteln

BACKGROUND_COLOR = "white"

SIZE_FIELD = 50       # Bilder sind 32x32 pixels

def load_images():
    """
    Lädt alle benötigten Bilder für das Minesweeper-Spiel.
    
    Durch die Verwendung von os.path.join und os.path.dirname wird der Pfad zu den Bildern dynamisch ermittelt. 
    Dies macht den Code portabel und unabhängig vom spezifischen Dateipfad des Benutzers.
    
    Returns:
        dict: Ein Dictionary, das die geladenen Bilder mit ihren Namen als Schlüssel enthält.
    """
    # Ermittelt den Pfad des aktuellen Skripts und ergänzt ihn um den relativen Pfad zum Bilderordner
    images_path = os.path.join(os.path.dirname(__file__), "images")
    
    images = {}
    
    # Dynamische Ermittlung der Pfade für die Bilder
    questionmark_path = os.path.join(images_path, "questionmark.jpg")
    bomb_path = os.path.join(images_path, "bomb.jpg")
    flag_path = os.path.join(images_path, "flag.jpg")
    
    # Fragezeichen Bild
    im = Image.open(questionmark_path)
    images["questionmark"] = ImageTk.PhotoImage(im)
    
    # Zahlen Bilder (von 0 bis 8)
    for i in range(9):
        number_path = os.path.join(images_path, f"{i}.jpg")
        im = Image.open(number_path)
        images[i] = ImageTk.PhotoImage(im)
    
    # Bombe Bild
    im = Image.open(bomb_path)
    images["bomb"] = ImageTk.PhotoImage(im)
    
    # Flagge Bild
    im = Image.open(flag_path)
    images["flag"] = ImageTk.PhotoImage(im)
    
    logging.info("Alle Bilder wurden geladen.")
    
    return images


def create_image(x, y, image):
    """
    Abkürzung für die create_image Funktion

    Args:
        x (int): x-Koordinate
        y (int): y-Koordinate
        image (PhotoImage): Das Bild
    """
    canvas.create_image(x*SIZE_FIELD, y*SIZE_FIELD, anchor="nw", image=image)


def draw_board(world):
    """
    Zeichnet für alle x und y Werte die richtigen Bilder

    Args:
        world (World)
    """
    for y in range(world.height):
        for x in range(world.width):

            tile = world[y,x]

            if tile.flag:
                create_image(x, y, images["flag"])

            elif not tile.opened:
                # Add the image to the canvas, and set the anchor to the top left / north west corner
                create_image(x, y, images["questionmark"])

            else:
                if tile.type == "Number":
                    create_image(x, y, images[tile.value])
                
                if tile.type == "Bomb":
                    create_image(x, y, images['bomb'])


def reset():
    """Erstellt eine neue Welt"""

    global world
    world = World()
    
    global already_lost 
    already_lost = False
    
    draw_board(world)


def left_click(event):
    """
    Führt den Left Click aus, um ein Feld zu öffnen und checkt, ob man verloren oder gewonnen hat.

    Args:
        event
    """
    global already_lost
    
    if already_lost:
        return
    
    # Die Koordinaten ausrechnen
    x_coor, y_coor = event.x // SIZE_FIELD, event.y // SIZE_FIELD
    
    # Das Feld aufmachen
    world.open_field(y_coor, x_coor)

    # Bomb
    if world[y_coor, x_coor].type == "Bomb":
        already_lost = True
        logging.info("Verloren")

    # Victory
    if world.check_victory():
        logging.info("Gewonnen!")

    draw_board(world)


def right_click(event):
    """
    Führt den Right Click aus, um eine Flage zu setzten und zu entfernen.

    Args:
        event
    """
    global already_lost

    if already_lost:
        return
    
    # Die Koordinaten ausrechnen
    x_coor, y_coor = event.x // SIZE_FIELD, event.y // SIZE_FIELD

    if not world[y_coor, x_coor].opened:
        world.set_flag(y_coor, x_coor)
    
    draw_board(world)


window = tk.Tk()
window.title("Minesweeper")

world = World()
already_lost = False

canvas = tk.Canvas(window, bg=BACKGROUND_COLOR, height=world.height*SIZE_FIELD, width=world.width*SIZE_FIELD)
canvas.pack()

# Das Menu erstellen
my_menu = tk.Menu(window)
window.config(menu=my_menu)

# Die Menuoptionen erstellen
my_menu.add_command(label="Neustart",        command=reset)
my_menu.add_command(label="Spiel verlassen", command=window.destroy)

# Die Bilder laden
images = load_images()

# Die Events anbinden
canvas.bind("<Button-1>", left_click)
canvas.bind("<Button-3>", right_click)

draw_board(world)

window.mainloop()