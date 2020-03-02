import pytest
from tests.utils import config_fixture

example1_config = config_fixture('example1.yaml')
example2_config = config_fixture('example2.yaml')
example3_config = config_fixture('example3.yaml')
boolean_param_config = config_fixture('flag-param-example.yaml')
boolean_param_pass_as_config = config_fixture('flag-param-pass-as-example.yaml')
mount_config = config_fixture('mount-example.yaml')
endpoint_config = config_fixture('endpoint-example.yaml')
optional_default_param_config = config_fixture('optional-default-param.yaml')
pipeline_config = config_fixture('pipeline-example.yaml')
multiple_param_config = config_fixture('multiple-param.yaml')


@pytest.fixture
def local_repository_path(tmpdir, monkeypatch):
    repository_dir = str(tmpdir.mkdir("repository"))
    monkeypatch.setenv("VH_REPOSITORY_DIR", repository_dir)
    return repository_dir
