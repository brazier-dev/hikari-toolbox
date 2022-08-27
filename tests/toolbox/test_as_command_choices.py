import hikari
import pytest

import toolbox


@pytest.fixture
def same_name_and_value():
    return (
        hikari.CommandChoice(name="a", value="a"),
        hikari.CommandChoice(name="b", value="b"),
        hikari.CommandChoice(name="c", value="c"),
    )

@pytest.fixture
def diff_name_and_value():
    return (
        hikari.CommandChoice(name="a", value="d"),
        hikari.CommandChoice(name="b", value="e"),
        hikari.CommandChoice(name="c", value="f"),
    )

def test_sequence_choices(same_name_and_value):
    assert toolbox.as_command_choices(["a", "b", "c"]) == same_name_and_value

def test_sequence_sequence_choices(diff_name_and_value):
    assert toolbox.as_command_choices([["a", "d"], ["b", "e"], ["c", "f"]]) == diff_name_and_value

def test_dict_choices(diff_name_and_value):
    assert (
        toolbox.as_command_choices(
            {
                "a": "d",
                "b": "e",
                "c": "f",
            }
        )
        == diff_name_and_value
    )

def test_vargs_choices(same_name_and_value):
    assert toolbox.as_command_choices("a", "b", "c") == same_name_and_value

def test_vargs_sequence_choices(diff_name_and_value):
    assert toolbox.as_command_choices(["a", "d"], ["b", "e"], ["c", "f"]) == diff_name_and_value

def test_kwargs_choices(diff_name_and_value):
    toolbox.as_command_choices(
        a="d",
        b="e",
        c="f",
    ) == diff_name_and_value
