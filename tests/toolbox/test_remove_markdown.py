from toolbox.strings import MarkdownFormat
from toolbox.strings import remove_markdown


def test_remove_markdown():
    assert remove_markdown("", MarkdownFormat.ALL) == ""
    assert remove_markdown("~~a~~", MarkdownFormat.STRIKETHROUGH) == "a"
    assert remove_markdown("||b||", MarkdownFormat.SPOILER) == "b"
    assert remove_markdown("**c**", MarkdownFormat.BOLD) == "c"
    assert remove_markdown("__d__", MarkdownFormat.UNDERLINE) == "d"
    assert remove_markdown("_e_", MarkdownFormat.ITALIC_UNDERSCORE) == "e"
    assert remove_markdown("*f*", MarkdownFormat.ITALIC_ASTERISK) == "f"
    assert remove_markdown("> g", MarkdownFormat.QUOTE) == "g"
    assert remove_markdown(">>> h", MarkdownFormat.MULTI_QUOTE) == "h"
    assert remove_markdown("`i`", MarkdownFormat.CODE_BLOCK) == "i"
    assert remove_markdown("```j```", MarkdownFormat.MULTI_CODE_BLOCK) == "j"
    assert remove_markdown("**~~k~~**", MarkdownFormat.BOLD | MarkdownFormat.STRIKETHROUGH) == "k"
    assert remove_markdown("*_l_*", MarkdownFormat.ITALIC_ASTERISK | MarkdownFormat.ITALIC_UNDERSCORE) == "l"
    assert remove_markdown("~~a~~") == "a"
    assert remove_markdown("||b||") == "b"
    assert remove_markdown("**c**") == "c"
    assert remove_markdown("__d__") == "d"
    assert remove_markdown("_e_") == "e"
    assert remove_markdown("*f*") == "f"
    assert remove_markdown("> g") == "g"
    assert remove_markdown(">>> h") == "h"
    assert remove_markdown("`i`") == "i"
    assert remove_markdown("```j```") == "j"
    assert remove_markdown("**~~k~~**") == "k"
    assert remove_markdown("*_l_*") == "l"
    assert remove_markdown("**__h__**") == "h"


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
