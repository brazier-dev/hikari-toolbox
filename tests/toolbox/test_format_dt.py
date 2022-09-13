import datetime

import pytest

import toolbox


def test_no_style():
    time = datetime.datetime.now()
    assert toolbox.format_dt(time) == f"<t:{int(time.timestamp())}>"


def test_has_style():
    time = datetime.datetime.now()
    assert toolbox.format_dt(time, style="t") == f"<t:{int(time.timestamp())}:t>"


def test_invalid_style():
    with pytest.raises(ValueError):
        toolbox.format_dt(datetime.datetime.now(), "INVALID")
