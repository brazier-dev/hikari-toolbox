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
