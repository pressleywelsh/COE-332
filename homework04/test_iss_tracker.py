from iss_tracker import vectors, timeRange, recentEpoch, calcSpeed, averageSpeed
import pytest

row1 = vectors(** { "EPOCH": "2026-112T03:19:44.000Z",
                   "X": "4823.7049518326174",
                   "Y": "-7391.2265840193756",
                   "Z": "2056.9934175602849",
                   "X_DOT": "-4.2761938457203185",
                   "Y_DOT": "2.9048571639827412",
                   "Z_DOT": "6.1384927501843697"})
row2 = vectors(**{ "EPOCH": "2026-118T14:52:10.000Z",
                  "X": "-6532.1847265918304",
                  "Y": "4127.9936402851746",
                  "Z": "-1789.5523049182736",
                  "X_DOT": "5.1047293847562019",
                  "Y_DOT": "-2.7381946573209481",
                  "Z_DOT": "4.9823175604912837"})
row3 = vectors(**{ "EPOCH": "2026-121T08:07:36.000Z",
                  "X": "2894.6603827510948",
                  "Y": "5943.2174086291753",
                  "Z": "-6321.8847092516384",
                  "X_DOT": "-3.8472195061738420",
                  "Y_DOT": "6.2149837502918473",
                  "Z_DOT": "-1.9275406837192056"})
row4 = vectors(**{ "EPOCH": "2026-130T19:44:02.000Z",
                  "X": "-7210.4483751902641",
                  "Y": "-1432.8809467510382",
                  "Z": "3678.5027193846502",
                  "X_DOT": "2.5093178461927530",
                  "Y_DOT": "-6.8912745038216491",
                  "Z_DOT": "3.1159482073649185"})
row5 = vectors(**{"EPOCH": "2002-145T18:22:11.000Z",
                  "X": "-6894.3175028419264",
                  "Y": "2143.8847095621937",
                  "Z": "3281.4905627483912",
                  "X_DOT": "2.9473185620914837",
                  "Y_DOT": "5.8217493048172641",
                  "Z_DOT": "-3.6149281752038472"})

def test_timeRange():
    assert(timeRange(row1, row2, row3, row4) == (f"The data spans from {row1.EPOCH} to {row4.EPOCH}"))
    assert(timeRange(row1, row2, row3) == (f"The data spans from {row1.EPOCH} to {row3.EPOCH}"))
    assert(timeRange(row1, row2, row3) != (f"The data spans from {row3.EPOCH} to {row4.EPOCH}"))
def test_timeRange_exceptions():
    with pytest.raises(IndexError):
        timeRange([])

def test_recentEpoch():
    assert(recentEpoch(row1, row5) == (row1))
    assert(recentEpoch(row3, row5) != (row5))

def test_recentEpoch_exceptions():
    with pytest.raises(IndexError):
        recentEpoch([])

def test_calcSpeed():
    expected = sqrt((row1.X_DOT ** 2) + (row1.Y_DOT ** 2) + (row1.Z_DOT ** 2))
    assert calcSpeed(row1) == expected
    assert calcSpeed(row1) != 0.0

def test_averageSpeed():
    expected = (calcSpeed(row1) + calcSpeed(row2)) / 2
    assert averageSpeed([row1, row2]) == expected
    assert averageSpeed([row4]) == calcSpeed(row4)
