import toolbox
from tests import utils


def test_sort_roles():
    roles = [
        utils.make_role(position=1),
        utils.make_role(position=3),
        utils.make_role(position=2),
    ]

    roles = toolbox.sort_roles(roles)

    assert roles[0].position == 3
    assert roles[1].position == 2
    assert roles[2].position == 1
