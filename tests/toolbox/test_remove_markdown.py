from toolbox.remove_markdown import remove_strikethrough, remove_code_blocks, remove_multi_code_blocks, remove_bold, remove_underlines, remove_underscore_italics, remove_asterisk_italics, remove_spoilers, remove_quotes, remove_multi_quotes

def test_remove_strikethrough():
    assert remove_strikethrough("~~a~~") == "a"
    assert remove_strikethrough("~b~") == "~b~"
    assert remove_strikethrough("c") == "c"
    assert remove_strikethrough("~~d") == "~~d"
    assert remove_strikethrough("~~e~~ ~~f g~~") == "e f g"
    assert remove_strikethrough("~~h~~ i j~~") == "h i j~~"
    assert remove_strikethrough("~~k~~ ~~l m~~ ~~n op~~") == "k l m n op"
    assert remove_strikethrough("~~q~~~") == "q~"
    assert remove_strikethrough("r  ~~~s t~~") == "r  ~s t"
    assert remove_strikethrough("~~a~~bcde~ f ~~g ~~") == "abcde~ f g "
    assert remove_strikethrough("~~h \nij k~~") == "h \nij k"


def test_remove_code_blockss():
    assert remove_code_blocks("`a`") == "a"
    assert remove_code_blocks("b") == "b"
    assert remove_code_blocks("`c") == "`c"
    assert remove_code_blocks("`d` `e f`") == "d e f"
    assert remove_code_blocks("`g` h i`") == "g h i`"
    assert remove_code_blocks("`j` `k l` `m no`") == "j k l m no"
    assert remove_code_blocks("`p``") == "p`"
    assert remove_code_blocks("q  ``r s`") == "q  `r s"
    assert remove_code_blocks("t  ` `u v`") == "t   u v`"
    assert remove_code_blocks("`a`bcde` f `g `") == "abcde f g `"
    assert remove_code_blocks("`h \nij k`") == "h \nij k"


def test_remove_multi_code_blockss():
    assert remove_multi_code_blocks("```a```") == "a"
    assert remove_multi_code_blocks("b") == "b"
    assert remove_multi_code_blocks("```c``` ```d e```") == "c d e"
    assert remove_multi_code_blocks("```f``` g h`") == "f g h`"
    assert remove_multi_code_blocks("```i``` ```j k``` ```l mn```") == "i j k l mn"
    assert remove_multi_code_blocks("```o````") == "o`"
    assert remove_multi_code_blocks("p  ``` ```q r`") == "p   q r`"
    assert remove_multi_code_blocks("```a```bcde` f ```g ```") == "abcde` f g "
    assert remove_multi_code_blocks("```h \nij k```") == "h \nij k"


def test_remove_bold():
    assert remove_bold("**a**") == "a"
    assert remove_bold("b") == "b"
    assert remove_bold("**c") == "**c"
    assert remove_bold("**d** **e f**") == "d e f"
    assert remove_bold("**g** h i**") == "g h i**"
    assert remove_bold("**j** **k l** **mn o**") == "j k l mn o"
    assert remove_bold("**p***") == "p*"
    assert remove_bold("q  ***r s**") == "q  *r s"
    assert remove_bold("t  ** **u v**") == "t   u v**"
    assert remove_bold("**a**bcde** f **g **") == "abcde f g **"
    assert remove_bold("**h \nij k**") == "h \nij k"


def test_remove_underliness():
    assert remove_underlines("__a__") == "a"
    assert remove_underlines("b") == "b"
    assert remove_underlines("__c") == "__c"
    assert remove_underlines("__d__ __e f__") == "d e f"
    assert remove_underlines("__g__ h i__") == "g h i__"
    assert remove_underlines("__j__ __k l__ __mn o__") == "j k l mn o"
    assert remove_underlines("__p___") == "p_"
    assert remove_underlines("q  ___r s__") == "q  _r s"
    assert remove_underlines("t  __ __u v__") == "t   u v__"
    assert remove_underlines("__a__bcde__ f __g __") == "abcde f g __"
    assert remove_underlines("__h \nij k__") == "h \nij k"


def test_remove_underscore_italics():
    assert remove_underscore_italics("") == ""
    assert remove_underscore_italics("_a_") == "a"
    assert remove_underscore_italics("b") == "b"
    assert remove_underscore_italics("_c") == "_c"
    assert remove_underscore_italics("_d_ _e f_") == "d e f"
    assert remove_underscore_italics("_g_ h i_") == "g h i_"
    assert remove_underscore_italics("_j_ _k l_ _mn o_") == "j k l mn o"
    assert remove_underscore_italics("_p__") == "p_"
    assert remove_underscore_italics("q  __r s_") == "q  _r s"
    assert remove_underscore_italics("t  _ _u v_") == "t   u v_"
    assert remove_underscore_italics("_a_bcde_ f _g _") == "abcde f g _"
    assert remove_underscore_italics("_h \nij k_") == "h \nij k"


def test_remove_asterisk_italics():
    assert remove_asterisk_italics("") == ""
    assert remove_asterisk_italics("*a*") == "a"
    assert remove_asterisk_italics("b") == "b"
    assert remove_asterisk_italics("*c") == "*c"
    assert remove_asterisk_italics("*d* *e f*") == "d e f"
    assert remove_asterisk_italics("*g* h i*") == "g h i*"
    assert remove_asterisk_italics("*j* *k l* *mn o*") == "j k l mn o"
    assert remove_asterisk_italics("*p**") == "p*"
    assert remove_asterisk_italics("q  **r s*") == "q  *r s"
    assert remove_asterisk_italics("t  * *u v*") == "t   u v*"
    assert remove_asterisk_italics("*a*bcde* f *g *") == "abcde f g *"
    assert remove_asterisk_italics("*h \nij k*") == "h \nij k"


def test_remove_spoilerss():
    assert remove_spoilers("") == ""
    assert remove_spoilers("||a||") == "a"
    assert remove_spoilers("b") == "b"
    assert remove_spoilers("||c") == "||c"
    assert remove_spoilers("||d|| ||e f||") == "d e f"
    assert remove_spoilers("||g|| h i||") == "g h i||"
    assert remove_spoilers("||j|| ||k l|| ||m n o||") == "j k l m n o"
    assert remove_spoilers("||p||||") == "p||"
    assert remove_spoilers("q || ||r s||") == "q  r s||"
    assert remove_spoilers("t  || ||u v||") == "t   u v||"
    assert remove_spoilers("||a||bcde|| f ||g ||") == "abcde f g ||"
    assert remove_spoilers("||h \ni j k||") == "h \ni j k"


def test_remove_quotess():
    assert remove_quotes("") == ""
    assert remove_quotes("a") == "a"
    assert remove_quotes("> b") == "b"
    assert remove_quotes("\n> c") == "\nc"
    assert remove_quotes("> \nd") == "\nd"
    assert remove_quotes(">e") == ">e"
    assert remove_quotes("> fgh") == "fgh"
    assert remove_quotes("\n\n\n> i") == "\n\n\ni"


def test_remove_multi_quotess():
    assert remove_multi_quotes("") == ""
    assert remove_multi_quotes("a") == "a"
    assert remove_multi_quotes(">>> b") == "b"
    assert remove_multi_quotes("\n>>> c") == "\nc"
    assert remove_multi_quotes(">>> \nd") == "\nd"
    assert remove_multi_quotes(">>>e") == ">>>e"
    assert remove_multi_quotes(">>> fgh") == "fgh"
    assert remove_multi_quotes("\n\n\n>>> i j k") == "\n\n\ni j k"