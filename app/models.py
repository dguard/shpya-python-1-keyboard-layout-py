import copy


class Analyzer(object):

    def __init__(self, text):
        self.text = text
        self.statistics = {}
        self.key_listeners = []
        self.end_analyze_listeners = []

    def add_key_listener(self, listener):
        self.key_listeners.append(listener)

    def add_end_analyze_listener(self, listener):
        self.end_analyze_listeners.append(listener)

    def analyze(self, layout):
        for listener in self.key_listeners + self.end_analyze_listeners:
            self.statistics[listener.__class__.__name__] = copy.deepcopy(layout)

        for symbol in self.text:
            self.analyze_symbol(symbol, layout)
        self.on_end_analyze()

    def analyze_symbol(self, symbol, layout):
        for key in layout.keys:
            if key.symbol == symbol:
                self.on_find_key(key)

    def on_find_key(self, key):
        for listener in self.key_listeners:
            listener.on_find_key(self.get_layout_by_listener(listener), key)

    def on_end_analyze(self):
        for listener in self.end_analyze_listeners:
            listener.on_end_analyze(self.get_layout_by_listener(listener), self)

    def get_layout_by_listener(self, listener):
        return self.statistics[listener.__class__.__name__]


class KeyListener(object):
    def on_find_key(self, layout, key):
        raise NotImplementedError("Should have implemented this")


class EndAnalyzeListener(object):
    def on_end_analyze(self, layout):
        raise NotImplementedError("Should have implemented this")


class EstimateListener(KeyListener):
    default_rate = 0.8
    max_rate = 1
    listPos = []

    def on_find_key(self, layout, key):
        rate = self.default_rate

        for pos_y, row in enumerate(self.listPos):
            for pos_x in row:
                if key.pos_x == pos_x and key.pos_y == pos_y:
                    rate = self.max_rate
        self.update_key_rate(rate, key, layout)

    @staticmethod
    def update_key_rate(rate, key, layout):
        for index, layout_key in enumerate(layout.keys):
            if layout_key.__str__() == key.__str__():
                layout.keys[index].rate = rate
        key.rate *= rate


class Key(object):
    rate = 1

    def __init__(self, name, symbol, pos_x=-1, pos_y=-1, mod=-1):
        self.name = name
        self.symbol = symbol
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.mod = mod

    def __str__(self):
        return self.mod + self.name


class Layout(object):
    KEY_ENTER = Key(name='Enter', symbol='\n')
    KEY_SPACE = Key(name='Space', symbol=' ')
    KEY_SHIFT = Key(name='Shift', symbol='')

    def __init__(self, name, mods):
        self.name = name
        self.keys = self.format_keys_in_mods(mods)

    @staticmethod
    def format_keys_in_mods(mods):
        new_keys = []

        for mod in mods:
            for pos_y, row in enumerate(mod['keys']):
                for pos_x, key in enumerate(row):
                    if key.__class__.__name__ == 'Key':
                        key.mod = mod['name']
                        key.pos_y = pos_y
                        key.pos_x = pos_x
                    else:
                        key = Key(name=key, symbol=key, pos_y=pos_y, pos_x=pos_x, mod=mod['name'])
                    new_keys.append(key)
        return new_keys