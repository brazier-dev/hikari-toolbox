from toolbox import remove_strikethrough


def test_remove_strikethrough():
    assert remove_strikethrough("~~test~~") == "test"
    assert remove_strikethrough("test") == "test"
    assert remove_strikethrough("~~test") == "~~test"
    assert remove_strikethrough("~~test~~ ~~another test~~") == "test another test"
    assert remove_strikethrough("~~test~~ another test~~") == "test another test~~"
    assert remove_strikethrough("~~test~~~") == "test~"
    assert remove_strikethrough("~~test~~ we write some random~ gibberish ~~hehe ~~") == "test we write some random~ gibberish hehe "