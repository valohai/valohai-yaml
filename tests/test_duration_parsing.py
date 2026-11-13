import datetime

import pytest

from valohai_yaml.utils.duration import parse_duration

TEST_CASES = [
    ("60 minutes  ", datetime.timedelta(hours=1)),
    ("1h10m", datetime.timedelta(hours=1, minutes=10)),
    ("2w", datetime.timedelta(weeks=2)),
    ("1.5d", datetime.timedelta(days=1, hours=12)),
    ("1.5d 2hörs", datetime.timedelta(days=1, hours=14)),
    ("3600", datetime.timedelta(hours=1)),
    ("1h30", datetime.timedelta(hours=1, seconds=30)),
    ("1mins", datetime.timedelta(minutes=1)),
    ("1mo", datetime.timedelta(days=30)),
    ("2 months", datetime.timedelta(days=60)),
    ("", None),
    ("   ", None),
    (72, datetime.timedelta(seconds=72)),
]


@pytest.mark.parametrize("case,expected", TEST_CASES)
def test_duration_parsing(case, expected):
    assert parse_duration(case) == expected
