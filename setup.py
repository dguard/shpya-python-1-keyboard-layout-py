import os
from app.models import Analyzer
from app.collections import layout, estimate

if __name__ == "__main__":

    print('Выполнение программы может занять продолжительное время... \nПросьба сохранять спокойствие...\n')

    # you may write own estimate and add in this list, see app/collections/estimate for more info
    # depends not supported yet, you must add estimate specified in "depends" manually before adding your own estimate
    list_key_estimate = [
        # single key statistic
        estimate.KeyRateCenterActivity(),
        estimate.KeyRateMiddleRow(),
        estimate.KeyRateLongFinger(),
        estimate.KeyRateRightHand(),
        estimate.KeyRateThumbFinger(),
        estimate.KeyRateUnnamedFinger(),
        estimate.KeyChangeHands(),
        estimate.KeyUsage(),
        estimate.KeySpeed(),

        # summary estimates of layout
        estimate.KeyTotalTime(),
        estimate.TotalTime(),
        estimate.TotalUsage(),
        estimate.TotalAvgRate(),
        estimate.TotalUsagePerMinute(),

        estimate.TotalKeyRateMiddleRow(),
        estimate.TotalKeyRateLongFinger(),
        estimate.TotalKeyRateUnnamedFinger(),
        estimate.TotalKeyRateCenterActivity(),
        estimate.TotalKeyRateRightHand(),
        estimate.TotalKeyRateThumbFinger(),
        estimate.TotalChangeHandsPercent()
    ]

    # for analyze english layouts, please comment off russian
    # text = "Test"
    with open(os.path.join(os.path.dirname(__file__), 'books', 'en_madame_bovary.txt')) as book:
        text = book.read()
    layouts_for_analyze = [
        layout.layoutQwerty,
        layout.layoutColemak,
        layout.layoutDworak
    ]

    # for analyze russian layouts, please comment off english
    # with open(os.path.join(os.path.dirname(__file__), 'books', 'ru_prestuplenie_i_nakazanie.txt'), encoding='utf8') \
    #         as book:
    #     text = book.read()
    #     layouts_for_analyze = [
    #         layout.layoutYacuken,
    #     ]

    # output summary results
    for l in layouts_for_analyze:
        analyzer = Analyzer(text=text, layout=l)
        for listener in list_key_estimate:
            analyzer.add_listener(listener)
        analyzer.analyze()

        print('Раскладка "%s"' % l.name)
        for statistic in analyzer.layout.statistics.values():
            print("%s: %s" % (statistic['name'], statistic['value']))
        print("\n")