from tests.utils import config_fixture

example1_config = config_fixture("example1.yaml")
example2_config = config_fixture("example2.yaml")
example3_config = config_fixture("example3.yaml")
boolean_param_config = config_fixture("flag-param-example.yaml")
boolean_param_pass_as_config = config_fixture("flag-param-pass-as-example.yaml")
mount_config = config_fixture("mount-example.yaml")
endpoint_config = config_fixture("endpoint-example.yaml")
optional_default_param_config = config_fixture("optional-default-param.yaml")
pipeline_config = config_fixture("pipeline-example.yaml")
task_config = config_fixture("task-example.yaml")
step_with_resources = config_fixture("step-with-resources.yaml")
step_with_partial_resources = config_fixture("step-with-partial-resources.yaml")
pipeline_overridden_config = config_fixture("pipeline-with-override-example.yaml")
pipeline_with_tasks_config = config_fixture("pipeline-with-tasks-example.yaml")
pipeline_with_parameters_config = config_fixture(
    "pipeline-with-parameters-example.yaml",
)
multiple_param_config = config_fixture("multiple-param.yaml")
input_extras_config = config_fixture("input-extras.yaml")
timeouts_config = config_fixture("timeouts-example.yaml")
