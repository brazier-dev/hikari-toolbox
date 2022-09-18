from toolbox import remove_strikethrough, remove_code_block, remove_multi_code_block, remove_bold, remove_underline, remove_italic_underscore, remove_italic_asterisk, remove_spoiler, remove_quote, remove_multi_quote

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


def test_remove_code_block():
    assert remove_code_block("`a`") == "a"
    assert remove_code_block("b") == "b"
    assert remove_code_block("`c") == "`c"
    assert remove_code_block("`d` `e f`") == "d e f"
    assert remove_code_block("`g` h i`") == "g h i`"
    assert remove_code_block("`j` `k l` `m no`") == "j k l m no"
    assert remove_code_block("`p``") == "p`"
    assert remove_code_block("q  ``r s`") == "q  `r s"
    assert remove_code_block("t  ` `u v`") == "t   u v`"
    assert remove_code_block("`a`bcde` f `g `") == "abcde f g `"
    assert remove_code_block("`h \nij k`") == "h \nij k"


def test_remove_multi_code_block():
    assert remove_multi_code_block("```a```") == "a"
    assert remove_multi_code_block("b") == "b"
    assert remove_multi_code_block("```c``` ```d e```") == "c d e"
    assert remove_multi_code_block("```f``` g h`") == "f g h`"
    assert remove_multi_code_block("```i``` ```j k``` ```l mn```") == "i j k l mn"
    assert remove_multi_code_block("```o````") == "o`"
    assert remove_multi_code_block("p  ``` ```q r`") == "p   q r`"
    assert remove_multi_code_block("```a```bcde` f ```g ```") == "abcde` f g "
    assert remove_multi_code_block("```h \nij k```") == "h \nij k"


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


def test_remove_underline():
    assert remove_underline("__a__") == "a"
    assert remove_underline("b") == "b"
    assert remove_underline("__c") == "__c"
    assert remove_underline("__d__ __e f__") == "d e f"
    assert remove_underline("__g__ h i__") == "g h i__"
    assert remove_underline("__j__ __k l__ __mn o__") == "j k l mn o"
    assert remove_underline("__p___") == "p_"
    assert remove_underline("q  ___r s__") == "q  _r s"
    assert remove_underline("t  __ __u v__") == "t   u v__"
    assert remove_underline("__a__bcde__ f __g __") == "abcde f g __"
    assert remove_underline("__h \nij k__") == "h \nij k"


def test_remove_italic_underscore():
    assert remove_italic_underscore("") == ""
    assert remove_italic_underscore("_a_") == "a"
    assert remove_italic_underscore("b") == "b"
    assert remove_italic_underscore("_c") == "_c"
    assert remove_italic_underscore("_d_ _e f_") == "d e f"
    assert remove_italic_underscore("_g_ h i_") == "g h i_"
    assert remove_italic_underscore("_j_ _k l_ _mn o_") == "j k l mn o"
    assert remove_italic_underscore("_p__") == "p_"
    assert remove_italic_underscore("q  __r s_") == "q  _r s"
    assert remove_italic_underscore("t  _ _u v_") == "t   u v_"
    assert remove_italic_underscore("_a_bcde_ f _g _") == "abcde f g _"
    assert remove_italic_underscore("_h \nij k_") == "h \nij k"


def test_remove_italic_asterisk():
    assert remove_italic_asterisk("") == ""
    assert remove_italic_asterisk("*a*") == "a"
    assert remove_italic_asterisk("b") == "b"
    assert remove_italic_asterisk("*c") == "*c"
    assert remove_italic_asterisk("*d* *e f*") == "d e f"
    assert remove_italic_asterisk("*g* h i*") == "g h i*"
    assert remove_italic_asterisk("*j* *k l* *mn o*") == "j k l mn o"
    assert remove_italic_asterisk("*p**") == "p*"
    assert remove_italic_asterisk("q  **r s*") == "q  *r s"
    assert remove_italic_asterisk("t  * *u v*") == "t   u v*"
    assert remove_italic_asterisk("*a*bcde* f *g *") == "abcde f g *"
    assert remove_italic_asterisk("*h \nij k*") == "h \nij k"


def test_remove_spoiler():
    assert remove_spoiler("") == ""
    assert remove_spoiler("||a||") == "a"
    assert remove_spoiler("b") == "b"
    assert remove_spoiler("||c") == "||c"
    assert remove_spoiler("||d|| ||e f||") == "d e f"
    assert remove_spoiler("||g|| h i||") == "g h i||"
    assert remove_spoiler("||j|| ||k l|| ||m n o||") == "j k l m n o"
    assert remove_spoiler("||p||||") == "p||"
    assert remove_spoiler("q || ||r s||") == "q  r s||"
    assert remove_spoiler("t  || ||u v||") == "t   u v||"
    assert remove_spoiler("||a||bcde|| f ||g ||") == "abcde f g ||"
    assert remove_spoiler("||h \ni j k||") == "h \ni j k"


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
    assert remove_multi_quote("\n\n\n>>> i j k") == "\n\n\ni j k"