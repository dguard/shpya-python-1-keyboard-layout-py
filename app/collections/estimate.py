from app.models import AnalyzeListener, EndEstimateListener


class MiddleRowEstimate(EndEstimateListener):
    description = 'Пальцы редко убегают из среднего ряда'

    def on_end_analyze(self, layout):
        for key in layout.keys:
            rate = self.default_rate
            if key.pos_y == 2:
                rate = self.max_rate
            self.update_key_rate(rate, key)


class LongFingerEstimate(EndEstimateListener):
    description = 'Работают указательные пальцы'

    listPos = [
        [4, 5, 6, 7, 8],
        [3, 4, 5, 6],
        [3, 4, 5, 6],
        [2, 3, 4, 5, 6],
        []
    ]


class UnnamedFingerEstimate(EndEstimateListener):
    description = 'Работают безымянные пальцы'

    listPos = [
        [1, 10],
        [1, 8],
        [1, 8],
        [1, 8],
        []
    ]


class CenterActivityEstimate(EndEstimateListener):
    description = 'Наибольшая активность сосредоточена в центре клавиатуры'

    listPos = [
        [],
        [2, 3, 4, 5, 6, 7],
        [2, 3, 4, 5, 6, 7],
        [2, 3, 4, 5, 6, 7],
        []
    ]


class ChangeHandsEstimate(AnalyzeListener):
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

    @staticmethod
    def on_end_analyze(layout):
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


class RightHandEstimate(EndEstimateListener):
    description = 'Правая рука задействована чуть больше, чем левая'

    listPos = [
        [7, 8, 9, 10, 11, 12],
        [5, 6, 7, 8, 9, 10, 11, 12],
        [5, 6, 7, 8, 9, 10, 11],
        [5, 6, 7, 8, 9, 10],
        [0]
    ]


class ThumbFingerEstimate(EndEstimateListener):
    description = 'Работают большие пальцы'
    listPos = [
        [],
        [],
        [],
        [],
        [0]
    ]


class UsageEstimate(AnalyzeListener):

    def on_find_key(self, layout, key):
        key.statistics['usage'] += 1