import typing as t

import hikari

__all__: t.Sequence[str] = ("sort_roles",)


def sort_roles(roles: t.Sequence[hikari.Role], ascending: bool = False) -> t.Sequence[hikari.Role]:
    """Sort a list of roles based on position. By default it is in a descending order.

    Parameters
    ----------
    roles : Sequence[hikari.Role]
        The list of roles to sort.
    ascending : bool, optional
        Whether to sort in ascending order, by default False.

    Returns
    -------
    Sequence[hikari.Role]
        The sorted list of roles.
    """
    return sorted(roles, key=lambda r: r.position, reverse=not ascending)


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
