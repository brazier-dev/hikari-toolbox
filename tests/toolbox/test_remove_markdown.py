from toolbox.strings import MarkdownFormat
from toolbox.strings import remove_markdown

test_dict = {
    "" : (MarkdownFormat.ALL, ""),
    "~~test 1~~" : (MarkdownFormat.STRIKETHROUGH, "test 1"),
    "||test 2||" : (MarkdownFormat.SPOILER, "test 2"),
    "**test 3**" : (MarkdownFormat.BOLD, "test 3"),
    "__test 4__" : (MarkdownFormat.UNDERLINE, "test 4"),
    "_test 5_" : (MarkdownFormat.ITALIC_UNDERSCORE, "test 5"),
    "*test 6*" : (MarkdownFormat.ITALIC_ASTERISK, "test 6"),
    "> test 7" : (MarkdownFormat.QUOTE, "test 7"),
    ">>> test 8" : (MarkdownFormat.MULTI_QUOTE, "test 8"),
    "`test 9`" : (MarkdownFormat.CODE_BLOCK, "test 9"),
    "```test 10```" : (MarkdownFormat.MULTI_CODE_BLOCK, "test 10"),
    "**~~test 11~~**" : (MarkdownFormat.BOLD | MarkdownFormat.STRIKETHROUGH, "test 11"),
    "*_test 12_*" : (MarkdownFormat.ITALIC_ASTERISK | MarkdownFormat.ITALIC_UNDERSCORE, "test 12"),
    "~~test 13~~": (None, "test 13"),
    "||test 14||": (None, "test 14"),
    "**test 15**" : (None, "test 15"),
    "__test 16__" : (None, "test 16"),
    "_test 17_" : (None, "test 17"),
    "*test 18*" : (None, "test 18"),
    "> test 19" : (None, "test 19"),
    ">>> test 20" : (None, "test 20"),
    "`test 21`": (None, "test 21"),
    "```test 22```" : (None, "test 22"),
    "**~~test 23~~**" : (None, "test 23"),
    "*_test 24_*": (None, "test 24"),
    "**__test 25__**": (None, "test 25"),
    "__test 26__ __test 26__": (MarkdownFormat.UNDERLINE, "test 26 test 26"),
    "**test 27** **test 27**": (MarkdownFormat.BOLD, "test 27 test 27")
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
