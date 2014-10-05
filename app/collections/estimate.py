from app.models import AnalyzeListener, EndEstimateListener


class KeyRateMiddleRow(EndEstimateListener):
    description = 'Пальцы редко убегают из среднего ряда'

    def on_end_analyze(self, layout):
        for key in layout.keys:
            rate = self.default_rate
            if key.pos_y == 2:
                rate = self.max_rate
            self.update_key_rate(rate, key)


class KeyRateLongFinger(EndEstimateListener):
    description = 'Работают указательные пальцы'

    listPos = [
        [4, 5, 6, 7, 8],
        [3, 4, 5, 6],
        [3, 4, 5, 6],
        [2, 3, 4, 5, 6],
        []
    ]


class KeyRateUnnamedFinger(EndEstimateListener):
    description = 'Работают безымянные пальцы'

    listPos = [
        [1, 10],
        [1, 8],
        [1, 8],
        [1, 8],
        []
    ]


class KeyRateCenterActivity(EndEstimateListener):
    description = 'Наибольшая активность сосредоточена в центре клавиатуры'

    listPos = [
        [],
        [2, 3, 4, 5, 6, 7],
        [2, 3, 4, 5, 6, 7],
        [2, 3, 4, 5, 6, 7],
        []
    ]


class KeyRateRightHand(EndEstimateListener):
    description = 'Правая рука задействована чуть больше, чем левая'

    listPos = [
        [7, 8, 9, 10, 11, 12],
        [5, 6, 7, 8, 9, 10, 11, 12],
        [5, 6, 7, 8, 9, 10, 11],
        [5, 6, 7, 8, 9, 10],
        [0]
    ]


class KeyRateThumbFinger(EndEstimateListener):
    description = 'Работают большие пальцы'
    listPos = [
        [],
        [],
        [],
        [],
        [0]
    ]


class KeyChangeHands(AnalyzeListener):
    description = 'Эффективное чередование рук'

    left_hand = [
        [0, 1, 2, 3, 4, 5, 6],
        [0, 1, 2, 3, 4],
        [0, 1, 2, 3, 4],
        [0, 1, 2, 3, 4],
        []
    ]

    def __init__(self):
        self.previous_key = None

    def on_find_key(self, layout, key):
        if self.previous_key:
            if 'hands_changed' not in key.statistics:
                key.statistics['hands_changed'] = 0
            if self.hands_changed(self.previous_key, key):
                key.statistics['hands_changed'] += 1
        self.previous_key = key

    def on_end_analyze(self, layout):
        for key in layout.keys:
            if 'hands_changed' not in key.statistics:
                key.statistics['hands_changed'] = 0

    def hands_changed(self, previous_key, current_key):
        previous_hand = self.detect_hand(previous_key)
        current_hand = self.detect_hand(current_key)
        return previous_hand != current_hand

    def detect_hand(self, key):
        for pos_y, row in enumerate(self.left_hand):
            for pos_x in row:
                if key.pos_x == pos_x and key.pos_y == pos_y:
                    return "left"
        return "right"


class KeyUsage(AnalyzeListener):
    def on_find_key(self, layout, key):
        key.statistics['usage'] += 1


class KeySpeed(AnalyzeListener):
    default_key_speed = 200

    def on_end_analyze(self, layout):
        for key in layout.keys:
            key.statistics['speed'] = 1 / key.statistics['rate'] * self.default_key_speed


class KeyTime(AnalyzeListener):
    depends = [KeyUsage, KeySpeed]

    def on_end_analyze(self, layout):
        for key in layout.keys:
            key.statistics['time'] = key.statistics['usage'] * key.statistics['speed']


class TimeTotal(AnalyzeListener):
    depends = [KeyTime]

    def on_end_analyze(self, layout):
        time_total = 0
        for key in layout.keys:
            time_total += key.statistics['time']
        layout.statistics['time_total'] = time_total


class UsageTotal(AnalyzeListener):
    depends = [KeyUsage]

    def on_end_analyze(self, layout):
        usage_total = 0
        for key in layout.keys:
            usage_total += key.statistics['usage']
        layout.statistics['usage_total'] = usage_total


class RateTotal(AnalyzeListener):
    def on_end_analyze(self, layout):
        rate_total = 0
        for key in layout.keys:
            rate_total += key.statistics['rate']
        layout.statistics['rate_total'] = rate_total