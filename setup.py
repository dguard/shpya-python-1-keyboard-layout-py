from app.models import Analyzer
from app.collections import layout, estimate

if __name__ == "__main__":
    text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor"
    qwertyAnalyzer = Analyzer(text=text, layout=layout.layoutQwerty)

    list_key_estimate = [
        estimate.ChangeHandsEstimate(),
        estimate.CenterActivityEstimate(),
        estimate.MiddleRowEstimate(),
        estimate.LongFingerEstimate(),
        estimate.RightHandEstimate(),
        estimate.ThumbFingerEstimate(),
        estimate.UnnamedFingerEstimate(),
        estimate.UsageEstimate(),
        estimate.SpeedEstimate()
    ]
    for listener in list_key_estimate:
        qwertyAnalyzer.add_listener(listener)
    qwertyAnalyzer.analyze()

    for key in layout.layoutQwerty.keys:
        if key.pos_x == 0:
            print()
        print("%s%s%s" % ('|', key.statistics['speed'], '|'), end=' ')