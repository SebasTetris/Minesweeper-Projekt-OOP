import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

class Tile:

    possible_types = ['Bomb', 'Number']

    def __init__(self, type='Number'):

        try:
            assert type in Tile.possible_types
        
        except AssertionError:
            logging.error('Unbekannter Tile Typ!')

        self.type = type
        
        self.flag   = False
        self.opened = False
        
        if type == 'Number':
            self.value  = 0
        
        elif type == 'Bomb':
            self.symbol = '💣'


    def is_bomb(self):
        return self.type == 'Bomb'


    def open_field(self):
        self.opened = True


    def set_flag(self):
        self.flag   = True
        self.symbol = '🚩'


    def unset_flag(self):
        self.flag = False


    def __repr__(self):

        try:        
            if self.flag:
                return self.symbol
            
            elif not self.opened:
                return '?'
            
            elif self.opened and self.type == 'Number':
                return self.value
            
            elif self.opened and self.type == 'Bomb':
                return self.symbol

            raise AssertionError
        
        except Exception:
            logging.error('Fehler bei der __repr__ Funktion des Tiles.')