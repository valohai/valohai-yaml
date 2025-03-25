import pytest

from valohai_yaml import ValidationErrors


def test_multiple_param_build(multiple_param_config):
    step = multiple_param_config.steps["example"]
    assert step.build_command({}) == [
        "echo "
        "--unlabeled-samples=60000 "
        "--encoder-layers=1000-500-250-250-250-10 "  # dash-separated
        "--denoising-cost-x=1000,1,0.01,0.01,0.01,0.01,0.01 "  # comma-separated
        "--decoder-spec gauss "  # repeated
        "--decoder-spec railgun",  # repeated
    ]
    assert step.build_command({"encoder-layers": 6, "denoising-cost-x": (2, "e")}) == [
        "echo "
        "--unlabeled-samples=60000 "
        "--encoder-layers=6 "  # dash-separated
        "--denoising-cost-x=2,e "  # comma-separated
        "--decoder-spec gauss "  # repeated
        "--decoder-spec railgun",  # repeated
    ]
    assert step.build_command(
        {"encoder-layers": None, "denoising-cost-x": (2, "e")},
    ) == [
        "echo "
        "--unlabeled-samples=60000 "
        "--denoising-cost-x=2,e "  # comma-separated
        "--decoder-spec gauss "  # repeated
        "--decoder-spec railgun",  # repeated
    ]
    assert step.build_command({"encoder-layers": [], "denoising-cost-x": (2, "e")}) == [
        "echo "
        "--unlabeled-samples=60000 "
        "--denoising-cost-x=2,e "  # comma-separated
        "--decoder-spec gauss "  # repeated
        "--decoder-spec railgun",  # repeated
    ]


def test_multiple_param_validate(multiple_param_config):
    step = multiple_param_config.steps["example"]

    # Test that validation wraps non-lists into lists
    assert step.parameters["denoising-cost-x"].validate(0.2) == [0.2]

    # Test that invalid atoms in float lists raise errors
    with pytest.raises(ValidationErrors):
        step.parameters["denoising-cost-x"].validate((2, "e"))

    # Test that invalid atoms in integer lists raise errors
    with pytest.raises(ValidationErrors):
        step.parameters["encoder-layers"].validate([1.133])

    # Test that invalid choices in choiced lists raise errors
    with pytest.raises(ValidationErrors) as vle:
        step.parameters["decoder-spec"].validate(["gauss", "john"])
    assert "john" in str(vle.value)

    # Test that lists in non-multiples raise errors
    with pytest.raises(ValidationErrors) as vle:
        step.parameters["unlabeled-samples"].validate([1.133])
    assert "single value" in str(vle.value)
