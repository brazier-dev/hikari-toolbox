from toolbox import remove_strikethrough, remove_code_block, remove_multi_code_block, remove_bold, remove_underline


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


def test_remove_code_block():
    assert remove_code_block("`test`") == "test"
    assert remove_code_block("test") == "test"
    assert remove_code_block("`test") == "`test"
    assert remove_code_block("`test` `another test`") == "test another test"
    assert remove_code_block("`test` another test`") == "test another test`"
    assert remove_code_block("`test` `another test` `and another one`") == "test another test and another one"
    assert remove_code_block("`test``") == "test`"
    assert remove_code_block("test  ``more randomness`") == "test  more randomness`"
    assert remove_code_block("test  ` `more randomness`") == "test   more randomness`"
    assert (
        remove_code_block("`test` we write some random` gibberish `hehe `")
        == "test we write some random gibberish hehe `"
    )
    assert remove_code_block("`test \nwith line break`") == "test \nwith line break"


def test_remove_multi_code_block():
    assert remove_multi_code_block("```test```") == "test"
    assert remove_multi_code_block("test") == "test"
    assert remove_multi_code_block("```test``` ```another test```") == "test another test"
    assert remove_multi_code_block("```test``` another test`") == "test another test`"
    assert remove_multi_code_block("```test``` ```another test``` ```and another one```") == "test another test and another one"
    assert remove_multi_code_block("```test````") == "test`"
    assert remove_multi_code_block("test  ``` ```more randomness`") == "test   more randomness`"
    assert (
        remove_multi_code_block("```test``` we write some random` gibberish ```hehe ```")
        == "test we write some random` gibberish hehe "
    )
    assert remove_multi_code_block("```test \nwith line break```") == "test \nwith line break"


def test_remove_bold():
    assert remove_bold("**test**") == "test"
    assert remove_bold("test") == "test"
    assert remove_bold("**test") == "**test"
    assert remove_bold("**test** **another test**") == "test another test"
    assert remove_bold("**test** another test**") == "test another test**"
    assert remove_bold("**test** **another test** **and another one**") == "test another test and another one"
    assert remove_bold("**test***") == "test*"
    assert remove_bold("test  ***more randomness**") == "test  *more randomness"
    assert remove_bold("test  ** **more randomness**") == "test   more randomness**"
    assert (
        remove_bold("**test** we write some random** gibberish **hehe **")
        == "test we write some random gibberish hehe **"
    )
    assert remove_bold("**test \nwith line break**") == "test \nwith line break"


def test_remove_underline():
    assert remove_underline("__test__") == "test"
    assert remove_underline("test") == "test"
    assert remove_underline("__test") == "__test"
    assert remove_underline("__test__ __another test__") == "test another test"
    assert remove_underline("__test__ another test__") == "test another test__"
    assert remove_underline("__test__ __another test__ __and another one__") == "test another test and another one"
    assert remove_underline("__test___") == "test_"
    assert remove_underline("test  ___more randomness__") == "test  _more randomness"
    assert remove_underline("test  __ __more randomness**") == "test   more randomness**"
    assert (
        remove_underline("__test__ we write some random__ gibberish __hehe __")
        == "test we write some random gibberish hehe __"
    )
    assert remove_underline("__test \nwith line break__") == "test \nwith line break"