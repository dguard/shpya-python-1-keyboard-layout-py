from app.models import Analyzer
from app.collections import layout, estimate

if __name__ == "__main__":
    text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor"
    qwertyAnalyzer = Analyzer(text=text)

    list_estimate = [
        estimate.CenterActivityEstimate(), estimate.ChangeHandsEstimate(), estimate.MiddleRowEstimate(),
        estimate.LongFingerEstimate(), estimate.RightHandEstimate(), estimate.ThumbFingerEstimate(),
        estimate.UnnamedFingerEstimate()
    ]
    for listener in list_estimate:
        qwertyAnalyzer.add_key_listener(estimate.CenterActivityEstimate())

    qwertyAnalyzer.analyze(layout.layoutQwerty)