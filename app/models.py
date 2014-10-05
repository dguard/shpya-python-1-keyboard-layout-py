import copy


class Analyzer(object):

    def __init__(self, text, layout):
        self.text = text
        self.layout = layout
        self.statistics = {}
        self.listeners = []

    def add_listener(self, listener):
        self.listeners.append(listener)

    def analyze(self):
        for symbol in self.text:
            self.analyze_symbol(symbol)
        self.on_end_analyze()

    def analyze_symbol(self, symbol):
        for key in self.layout.keys:
            if key.symbol == symbol:
                self.on_find_key(key)

    def on_find_key(self, key):
        for listener in self.listeners:
            listener.on_find_key(self.layout, key)

    def on_end_analyze(self):
        for listener in self.listeners:
            listener.on_end_analyze(self.layout)


class AnalyzeListener(object):
    def on_find_key(self, layout, key):
        pass

    def on_end_analyze(self, layout):
        pass


class EndEstimateListener(AnalyzeListener):
    default_rate = 0.9
    max_rate = 1
    listPos = []

    def on_end_analyze(self, layout):
        for key in layout.keys:
            rate = self.default_rate
            for pos_y, row in enumerate(self.listPos):
                for pos_x in row:
                    if key.pos_y == pos_y and key.pos_x == pos_x:
                        rate = self.max_rate
            self.update_key_rate(rate, key)

    def update_key_rate(self, rate, key):
        key.statistics[self.__class__.__name__] = rate
        key.statistics['rate'] *= rate


class Key(object):

    def __init__(self, name, symbol, pos_x=-1, pos_y=-1, mod=-1):
        self.statistics = {
            'rate': 1,
            'usage': 1
        }
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
                        key = copy.deepcopy(key)
                        key.mod = mod['name']
                        key.pos_y = pos_y
                        key.pos_x = pos_x
                    else:
                        key = Key(name=key, symbol=key, pos_y=pos_y, pos_x=pos_x, mod=mod['name'])
                    new_keys.append(key)
        return new_keys