from toolbox import remove_strikethrough, remove_code_block, remove_multi_code_block, remove_bold, remove_underline, remove_italic_underscore, remove_italic_asterisk, remove_spoiler, remove_quote, remove_multi_quote

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
    assert remove_code_block("test  ``more randomness`") == "test  `more randomness"
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


def test_remove_italic_underscore():
    assert remove_italic_underscore("") == ""
    assert remove_italic_underscore("_test_") == "test"
    assert remove_italic_underscore("test") == "test"
    assert remove_italic_underscore("_test") == "_test"
    assert remove_italic_underscore("_test_ _another test_") == "test another test"
    assert remove_italic_underscore("_test_ another test_") == "test another test_"
    assert remove_italic_underscore("_test_ _another test_ _and another one_") == "test another test and another one"
    assert remove_italic_underscore("_test__") == "test_"
    assert remove_italic_underscore("test  __more randomness_") == "test  _more randomness"
    assert remove_italic_underscore("test  _ _more randomness_") == "test   more randomness_"
    assert (
        remove_italic_underscore("_test_ we write some random_ gibberish _hehe _")
        == "test we write some random gibberish hehe _"
    )
    assert remove_italic_underscore("_test \nwith line break_") == "test \nwith line break"


def test_remove_italic_asterisk():
    assert remove_italic_asterisk("") == ""
    assert remove_italic_asterisk("*test*") == "test"
    assert remove_italic_asterisk("test") == "test"
    assert remove_italic_asterisk("*test") == "*test"
    assert remove_italic_asterisk("*test* *another test*") == "test another test"
    assert remove_italic_asterisk("*test* another test*") == "test another test*"
    assert remove_italic_asterisk("*test* *another test* *and another one*") == "test another test and another one"
    assert remove_italic_asterisk("*test**") == "test*"
    assert remove_italic_asterisk("test  **more randomness*") == "test  *more randomness"
    assert remove_italic_asterisk("test  * *more randomness*") == "test   more randomness*"
    assert (
        remove_italic_asterisk("*test* we write some random* gibberish *hehe *")
        == "test we write some random gibberish hehe *"
    )
    assert remove_italic_asterisk("*test \nwith line break*") == "test \nwith line break"


def test_remove_spoiler():
    assert remove_spoiler("") == ""
    assert remove_spoiler("||test||") == "test"
    assert remove_spoiler("test") == "test"
    assert remove_spoiler("||test") == "||test"
    assert remove_spoiler("||test|| ||another test||") == "test another test"
    assert remove_spoiler("||test|| another test||") == "test another test||"
    assert remove_spoiler("||test|| ||another test|| ||and another one||") == "test another test and another one"
    assert remove_spoiler("||test||||") == "test||"
    assert remove_spoiler("test  ||||more randomness||") == "test  ||more randomness"
    assert remove_spoiler("test  || ||more randomness||") == "test   more randomness||"
    assert (
        remove_spoiler("||test|| we write some random|| gibberish ||hehe ||")
        == "test we write some random gibberish hehe ||"
    )
    assert remove_spoiler("||test \nwith line break||") == "test \nwith line break"


def test_remove_quote():
    assert remove_quote("") == ""
    assert remove_quote("a") == "a"
    assert remove_quote("> b") == "b"
    assert remove_quote("\n> c") == "\nc"
    assert remove_quote("> \nd") == "\nd"
    assert remove_quote(">e") == ">e"
    assert remove_quote("> fgh") == "fgh"
    assert remove_quote("\n\n\n> i") == "\n\n\ni"

def test_remove_multi_quote():
    assert remove_multi_quote("") == ""
    assert remove_multi_quote("a") == "a"
    assert remove_multi_quote(">>> b") == "b"
    assert remove_multi_quote("\n>>> c") == "\nc"
    assert remove_multi_quote(">>> \nd") == "\nd"
    assert remove_multi_quote(">>>e") == ">>>e"
    assert remove_multi_quote(">>> fgh") == "fgh"
    assert remove_multi_quote("\n\n\n>>> i") == "\n\n\ni"