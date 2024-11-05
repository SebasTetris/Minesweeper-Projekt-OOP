import random
import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

from tile import Tile 

class World:

    def __init__(self, height=8, width=8, bombs=15):
        """
        Eine Instanz der Klasse initialisieren

        Args:
            height (int, optional): Die Anzahl an Reihen. Defaults to 8.
            width (int, optional): Die Anzahl an Spalten. Defaults to 8.
            bombs (int, optional): Die Anzahl an Bomben. Defaults to 15.
        """

        self.height = height
        self.width  = width
        self.bombs = bombs

        try:
            assert self.bombs < self.width * self.height
        except AssertionError:
            logging.error('Zu viele Bomben ausgewählt!')

        self.number_of_flags = 0

        # Das leere Board initialisieren und die Bomben erstellen
        self.generate_board_with_bombs(self.bombs)

        # Die Werte der Felder ausrechnen
        self.generate_values()

        logging.info('Das Board wurde erfolgreich initialisiert!')


    def open_field(self, row, col):
        """
        Diese Funktion öffnet das angegeben Feld

        Args:
            row (int): Die Reihe des Feldes
            col (int): Die Spalte des Feldes
        """
        try:
            assert not self[row, col].opened
        except AssertionError:
            logging.warning('Das Feld wurde schon geöffnetn!')
        
        try:
            assert not self[row, col].flag
        except AssertionError:
            logging.warning('Das Feld ist eine Flage!')
             
        else:
            self[row, col].open_field()
            self.opened_fields += 1
        

    def set_flag(self, row, col):
        """
        Diese Funktion setzt eine Flage auf das angegeben Feld

        Args:
            row (int): Die Reihe des Feldes
            col (int): Die Spalte des Feldes
        """

        if self[row, col].flag:
            logging.info(f'Die Flage wurde aus {row} {col} entfernt.')
            self[row, col].unset_flag()
            self.number_of_flags -= 1
        
        else:
            logging.info(f'Die Flage wurde in {row} {col} hinzugefügt.')
            self[row, col].set_flag()
            self.number_of_flags +=1


    def generate_board_with_bombs(self, number_of_bombs):
        """
        Initialisiert das Board mit leeren Tiles und Bomben 

        Args:
            number_of_bombs (int): Die Anzahl der Bomben
        """
        self.opened_fields   = 0
        self.number_of_flags = 0

        self.data = []
        
        # Initialisiere alle leeren Felder
        for _ in range(self.height):
            row = [Tile() for _ in range(self.width)]
            self.data.append(row)

        total_cells = self.width * self.height

        bombs = random.sample(range(total_cells), number_of_bombs)

        for b in bombs:
            row = b // self.width
            col = b  % self.width 
            self[row, col] = Tile("Bomb")


    def generate_values(self):
      
        # Für alle Zellen
        # Keine elifs oder verschachtelten ifs mit `or`, weil eine Zelle mehrere Konditionen erfüllen kann
        # ZB oben und unten links eine Bombe, dann 2 mal += 1
        for row in range(self.height):
            for col in range(self.width):

                # Sollte die Zelle eine Bombe sein, dann mach einfach weiter
                if self[row, col].type == "Bomb":
                    continue

                # OBEN
                # Wenn es NICHT die erste Reihe ist und die row-1 eine Bombe ist
                if row > 0  and self[row-1, col].type =="Bomb":
                    self[row, col].value += 1

                # UNTEN
                # Wenn es NICHT die letzte Reihe ist und die row+1 eine Bombe ist
                if row < self.height-1 and self[row+1, col].type == "Bomb":
                    self[row, col].value += 1

                # RECHTS
                # Wenn es NICHT die erste Spalte ist und die col-1 eine Bombe ist
                if col > 0 and self[row, col-1].type == "Bomb":
                    self[row, col].value += 1
                
                # LINKS
                # Wenn es NICHT die letzte Spalte ist und die col+1 eine Bombe ist
                if col < self.width-1  and self[row, col+1].type=="Bomb":
                    self[row, col].value += 1

                # OBEN RECHTS
                if col > 0 and row > 0 and self[row-1, col-1].type == "Bomb":
                    self[row, col].value += 1

                # UNTEN RECHTS
                if col > 0 and row < self.height -1 and self[row+1, col-1].type == "Bomb":
                    self[row, col].value += 1
                
                # OBEN LINKS
                if col < self.width -1 and row > 0 and self[row-1, col+1].type == "Bomb":
                    self[row, col].value += 1

                # UNTEN LINKS
                if col < self.width -1 and row < self.height -1  and self[row+1, col+1].type == "Bomb":
                    self[row, col].value += 1


    def check_victory(self):
        """
        Die Funktion testet die Siegbedingung

        Returns:
            bool: Ob das Spiel gewonnen ist
        """
        total_cells = self.width * self.height
        return self.opened_fields == total_cells - self.bombs


    def __setitem__(self, point, value):
        """
        Die setter Funktion für eine Zelle

        Args:
            point (Tuple): Die row, col Koordinaten
            value (int): Der Wert der Zelle
        """
        row, col = point
        assert isinstance(value, Tile)
        self.data[row][col] = value


    def __getitem__(self, point):
        """
        Die getter Funktion für eine Zelle

        Args:
            point (Tuple): Die row, col Koordinaten

        Returns:
            int: Der Wert der Zelle
        """
        row, col = point
        assert isinstance(self.data[row][col], Tile)
        return self.data[row][col]

    def __repr__(self):
        """
        Die representation Funktion der Klasse, die automatisch bei Verwendung von `print` aufgeruden wird

        Returns:
            str: Das Board in einer lesbaren Form
        """

        s = "\n\t\t\tMINESWEEPER\n"
        
        col_header = '    ' # Header für Columns
        hline = '   |'      # Horizontale Linie

        # Den Column Header und die Horizontale Linie bauen anhand der angegebenen width
        for c in range(self.width):
            col_header += f'{c:^6}'
            hline += '-----|'

        s += col_header + '\n'
        
        # Für jede Zeile
        for row in range(self.height):

            s += hline + '\n'   
            str_row = ''
            
            # Für jede Spalte
            for col in range(self.width):             
                symbol = self[row, col].__repr__()

                if symbol == '💣' or symbol == "🚩":
                    str_row += f"{symbol:^4}|"

                else: 
                    str_row += f"{symbol:^5}|"
            
            # Schreibe die Zeilennummer und die Inhalte
            s += f" {row} |{str_row}\n"

        s += hline

        s += f"\n\nGesetzte Flaggen: {self.number_of_flags}\n"
        s += f"Geöffnete Felder: {self.opened_fields}\n"

        return s    

# ZUM TESTEN IN TILE.PY DIE OPEN AUF TRUE SETZEN!
# w = World(8, 8, 5)
# print(w)