from toolbox.strings import MarkdownFormat
from toolbox.strings import remove_markdown

test_dict = {
    "": (MarkdownFormat.ALL, ""),
    "~~test 1~~": (MarkdownFormat.STRIKETHROUGH, "test 1"),
    "||test 2||": (MarkdownFormat.SPOILER, "test 2"),
    "**test 3**": (MarkdownFormat.BOLD, "test 3"),
    "__test 4__": (MarkdownFormat.UNDERLINE, "test 4"),
    "_test 5_": (MarkdownFormat.ITALIC_UNDERSCORE, "test 5"),
    "*test 6*": (MarkdownFormat.ITALIC_ASTERISK, "test 6"),
    "> test 7": (MarkdownFormat.QUOTE, "test 7"),
    ">>> test 8": (MarkdownFormat.MULTI_QUOTE, "test 8"),
    "`test 9`": (MarkdownFormat.CODE_BLOCK, "test 9"),
    "```test 10```": (MarkdownFormat.MULTI_CODE_BLOCK, "test 10"),
    "**~~test 11~~**": (MarkdownFormat.BOLD | MarkdownFormat.STRIKETHROUGH, "test 11"),
    "*_test 12_*": (MarkdownFormat.ITALIC_ASTERISK | MarkdownFormat.ITALIC_UNDERSCORE, "test 12"),
    "~~test 13~~": (MarkdownFormat.ALL, "test 13"),
    "||test 14||": (MarkdownFormat.ALL, "test 14"),
    "**test 15**": (MarkdownFormat.ALL, "test 15"),
    "__test 16__": (MarkdownFormat.ALL, "test 16"),
    "_test 17_": (MarkdownFormat.ALL, "test 17"),
    "*test 18*": (MarkdownFormat.ALL, "test 18"),
    "> test 19": (MarkdownFormat.ALL, "test 19"),
    ">>> test 20": (MarkdownFormat.ALL, "test 20"),
    "`test 21`": (MarkdownFormat.ALL, "test 21"),
    "```test 22```": (MarkdownFormat.ALL, "test 22"),
    "**~~test 23~~**": (MarkdownFormat.ALL, "test 23"),
    "*_test 24_*": (MarkdownFormat.ALL, "test 24"),
    "**__test 25__**": (MarkdownFormat.ALL, "test 25"),
    "__test 26__ __test 26__": (MarkdownFormat.UNDERLINE, "test 26 test 26"),
    "**test 27** **test 27**": (MarkdownFormat.BOLD, "test 27 test 27"),
    "~~test 28~~ __test 28__": (MarkdownFormat.ALL, "test 28 test 28"),
    "||test 29|| ||test 29||": (MarkdownFormat.ALL, "test 29 test 29"),
    "```test 30``` ```test 30```": (MarkdownFormat.ALL, "test 30 test 30"),
    "`test 31` `test 31`": (MarkdownFormat.ALL, "test 31 test 31"),
    "`test 32` `test 32`": (MarkdownFormat.ITALIC_ASTERISK, "`test 32` `test 32`"),
    ">>> test 33 *test 33*": (MarkdownFormat.ALL, "test 33 test 33"),
    "`test 34 _test 34_`": (MarkdownFormat.ALL, "test 34 _test 34_"),
    "```test 35 _test 35_```": (MarkdownFormat.ALL, "test 35 _test 35_"),
    "```test 36 _test 37_``` _test 38_ ```test 39 *test 40*```": (MarkdownFormat.ALL, "test 36 _test 37_ test 38 test 39 *test 40*"),
    "`test 41 **test 42**` **test 43** `__test 44__`": (MarkdownFormat.ALL, "test 41 **test 42** test 43 __test 44__")
}


def test_remove_markdown():
    for test, (format, result) in test_dict.items():
        if not format:
            assert remove_markdown(test) == result
        else:
            assert remove_markdown(test, format) == result


# MIT License
#
# Copyright (c) 2022-present HyperGH
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
