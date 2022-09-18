from toolbox import remove_strikethrough, remove_block, remove_multiblock


def test_remove_strikethrough():
    assert remove_strikethrough("~~test~~") == "test"
    assert remove_strikethrough("~test~") == "~test~"
    assert remove_strikethrough("test") == "test"
    assert remove_strikethrough("~~test") == "~~test"
    assert remove_strikethrough("~~test~~ ~~another test~~") == "test another test"
    assert remove_strikethrough("~~test~~ another test~~") == "test another test~~"
    assert remove_strikethrough("~~test~~ ~~another test~~ ~~and another one~~") == "test another test and another one"
    assert remove_strikethrough("~~test~~~") == "test~"
    assert remove_strikethrough("test  ~~~more randomness~~") == "test  ~more randomness"
    assert (
        remove_strikethrough("~~test~~ we write some random~ gibberish ~~hehe ~~")
        == "test we write some random~ gibberish hehe "
    )
    assert remove_strikethrough("~~test \nwith line break~~") == "test \nwith line break"


def test_remove_block():
    assert remove_block("`test`") == "test"
    assert remove_block("test") == "test"
    assert remove_block("`test") == "`test"
    assert remove_block("`test` `another test`") == "test another test"
    assert remove_block("`test` another test`") == "test another test`"
    assert remove_block("`test` `another test` `and another one`") == "test another test and another one"
    assert remove_block("`test``") == "test`"
    assert remove_block("test  ``more randomness`") == "test  more randomness`"
    assert remove_block("test  ` `more randomness`") == "test   more randomness`"
    assert (
        remove_block("`test` we write some random` gibberish `hehe `")
        == "test we write some random gibberish hehe `"
    )
    assert remove_block("`test \nwith line break`") == "test \nwith line break"

def test_remove_multiblock():
    assert remove_multiblock("```test```") == "test"
    assert remove_multiblock("test") == "test"
    assert remove_multiblock("```test``` ```another test```") == "test another test"
    assert remove_multiblock("```test``` another test`") == "test another test`"
    assert remove_multiblock("```test``` ```another test``` ```and another one```") == "test another test and another one"
    assert remove_multiblock("```test````") == "test`"
    assert remove_multiblock("test  ``` ```more randomness`") == "test   more randomness`"
    assert (
        remove_multiblock("```test``` we write some random` gibberish ```hehe ```")
        == "test we write some random` gibberish hehe "
    )
    assert remove_multiblock("```test \nwith line break```") == "test \nwith line break"
