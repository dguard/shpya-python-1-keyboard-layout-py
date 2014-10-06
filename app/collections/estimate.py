from app.models import AnalyzeListener, EstimateListener


# start single section
class KeyRateMiddleRow(EstimateListener):
    description = 'Пальцы редко убегают из среднего ряда'

    def on_end_analyze(self, layout):
        for key in layout.keys:
            rate = self.default_rate
            if key.pos_y == 2:
                rate = self.max_rate
                self.update_count(key, key.statistics['usage'], True)
            else:
                self.update_count(key, 0)
            self.update_key_rate(rate, key)


class KeyRateLongFinger(EstimateListener):
    description = 'Работают указательные пальцы'

    listPos = [
        [4, 5, 6, 7, 8],
        [3, 4, 5, 6],
        [3, 4, 5, 6],
        [2, 3, 4, 5, 6],
        []
    ]


class KeyRateUnnamedFinger(EstimateListener):
    description = 'Работают безымянные пальцы'

    listPos = [
        [1, 10],
        [1, 8],
        [1, 8],
        [1, 8],
        []
    ]


class KeyRateCenterActivity(EstimateListener):
    description = 'Наибольшая активность сосредоточена в центре клавиатуры'

    listPos = [
        [],
        [2, 3, 4, 5, 6, 7],
        [2, 3, 4, 5, 6, 7],
        [2, 3, 4, 5, 6, 7],
        []
    ]


class KeyRateRightHand(EstimateListener):
    description = 'Правая рука задействована чуть больше, чем левая'

    listPos = [
        [7, 8, 9, 10, 11, 12],
        [5, 6, 7, 8, 9, 10, 11, 12],
        [5, 6, 7, 8, 9, 10, 11],
        [5, 6, 7, 8, 9, 10],
        [0]
    ]


class KeyRateThumbFinger(EstimateListener):
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
            if 'change_hands' not in self.previous_key.statistics:
                self.previous_key.statistics['change_hands'] = 0
            if self.hands_changed(self.previous_key, key):
                self.previous_key.statistics['change_hands'] += 1
        self.previous_key = key

    def on_end_analyze(self, layout):
        for key in layout.keys:
            if 'change_hands' not in key.statistics:
                key.statistics['change_hands'] = 0

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
    name = "Количество нажатий клавиши"

    def on_find_key(self, layout, key):
        key.statistics['usage'] += 1


class KeySpeed(AnalyzeListener):
    name = "Скорость нажатия клавиши"
    default_key_speed = 200

    def on_end_analyze(self, layout):
        for key in layout.keys:
            key.statistics['speed'] = 1 / key.statistics['rate'] * self.default_key_speed
# end single section


# start total section
class KeyTotalTime(AnalyzeListener):
    name = "Общее время потраченное на нажатие одной клавиши"
    depends = [KeyUsage, KeySpeed]

    def on_end_analyze(self, layout):
        for key in layout.keys:
            key.statistics['total_time'] = key.statistics['usage'] * key.statistics['speed']


class TotalTime(AnalyzeListener):
    name = "Общее время набора в секундах"
    depends = [KeyTotalTime]

    def on_end_analyze(self, layout):
        time_total = 0
        for key in layout.keys:
            time_total += key.statistics['total_time']
        layout.statistics['time_total'] = {
            'name': self.name,
            'value': "{0:.3f}".format(time_total / 100 / 60),
            'raw_value': time_total
        }


class TotalUsage(AnalyzeListener):
    name = "Суммарное количество нажатий клавиш"
    depends = [KeyUsage]

    def on_end_analyze(self, layout):
        usage_total = 0
        for key in layout.keys:
            usage_total += key.statistics['usage']
        layout.statistics['usage_total'] = {
            'name': self.name,
            'raw_value': usage_total,
            'value': usage_total
        }


class TotalAvgRate(AnalyzeListener):
    name = "Средняя эффективность клавиш"

    def on_end_analyze(self, layout):
        rate_total = 0
        for key in layout.keys:
            rate_total += key.statistics['rate'] * key.statistics['usage'] / layout.statistics['usage_total']['raw_value']
        layout.statistics['rate_total'] = {
            'name': self.name,
            'value': "{0:.2f}".format(rate_total*100),
            'raw_value': rate_total
        }


class TotalUsagePerMinute(AnalyzeListener):
    name = "Символов за минуту"
    depends = [TotalUsage, TotalTime],

    def on_end_analyze(self, layout):
        usage_per_minute = layout.statistics['usage_total']['raw_value'] \
                       / (layout.statistics['time_total']['raw_value'] / 100 / 60)
        layout.statistics['usage_per_minute'] = {
            'name': self.name,
            'value': "{0:.2f}".format(usage_per_minute),
            'raw_value': usage_per_minute
        }


class TotalAnalyzeListener(AnalyzeListener):
    name = ""
    field = ""

    def on_end_analyze(self, layout):
        value = 0
        for key in layout.keys:
            value += key.statistics[self.field]

        value = value / layout.statistics['usage_total']['raw_value'] * 100

        layout.statistics[self.field] = {
            'name': self.name,
            'value': "{0:.2f}".format(value),
            'raw_value': value,
        }


class TotalKeyRateMiddleRow(TotalAnalyzeListener):
    name = "Процент нахождения рук в центральном ряду"
    depends = [KeyRateMiddleRow, TotalUsage],
    field = 'KeyRateMiddleRow_count'


class TotalKeyRateLongFinger(TotalAnalyzeListener):
    name = "Процент использования указательного пальца"
    depends = [KeyRateLongFinger, TotalUsage],
    field = 'KeyRateLongFinger_count'


class TotalKeyRateUnnamedFinger(TotalAnalyzeListener):
    name = "Процент использования безымянного пальца"
    depends = [KeyRateUnnamedFinger, TotalUsage],
    field = 'KeyRateUnnamedFinger_count'


class TotalKeyRateCenterActivity(TotalAnalyzeListener):
    name = "Процент использования центральной части клавиатуры"
    depends = [KeyRateCenterActivity, TotalUsage],
    field = 'KeyRateCenterActivity_count'


class TotalKeyRateRightHand(TotalAnalyzeListener):
    name = "Процент использования правой руки"
    depends = [KeyRateRightHand, TotalUsage],
    field = 'KeyRateRightHand_count'


class TotalKeyRateThumbFinger(TotalAnalyzeListener):
    name = "Процент использования большого пальца"
    depends = [KeyRateThumbFinger, TotalUsage],
    field = 'KeyRateThumbFinger_count'


class TotalChangeHandsPercent(TotalAnalyzeListener):
    name = "Процент чередований рук"
    depends = [KeyChangeHands, TotalUsage],
    field = 'change_hands'

# end total section