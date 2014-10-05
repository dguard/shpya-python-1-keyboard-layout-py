import os
from app.models import Analyzer
from app.collections import layout, estimate

if __name__ == "__main__":
    text = ""
    with open(os.path.join(os.path.dirname(__file__), 'books', 'en_madame_bovary.txt')) as book:
        text = book.read()

    list_key_estimate = [
        estimate.KeyRateCenterActivity(),
        estimate.KeyRateMiddleRow(),
        estimate.KeyRateLongFinger(),
        estimate.KeyRateRightHand(),
        estimate.KeyRateThumbFinger(),
        estimate.KeyRateUnnamedFinger(),
        estimate.KeyChangeHands(),
        estimate.KeyUsage(),
        estimate.KeySpeed(),
        estimate.KeyTime(),
        estimate.TimeTotal(),
        estimate.RateTotal(),
        estimate.UsageTotal(),
    ]

    qwertyAnalyzer = Analyzer(text=text, layout=layout.layoutQwerty)
    for listener in list_key_estimate:
        qwertyAnalyzer.add_listener(listener)
    qwertyAnalyzer.analyze()

    colemakAnalyzer = Analyzer(text=text, layout=layout.layoutColemak)
    for listener in list_key_estimate:
        colemakAnalyzer.add_listener(listener)
    colemakAnalyzer.analyze()

    dworakAnalyzer = Analyzer(text=text, layout=layout.layoutDworak)
    for listener in list_key_estimate:
        dworakAnalyzer.add_listener(listener)
    dworakAnalyzer.analyze()

    # print(layout.layoutQwerty.statistics)
    # print(layout.layoutColemak.statistics)
    # print(layout.layoutDworak.statistics)