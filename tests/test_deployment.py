from valohai_yaml.objs import Config, Deployment


def test_automatic_deployment_example_is_pristine(pipeline_with_automatic_deployment_creation_config):
    config = pipeline_with_automatic_deployment_creation_config

    assert len(config.deployments) == 1

    deployment = config.deployments.get("us-west-qa")
    assert isinstance(deployment, Deployment)
    assert deployment.name == "us-west-qa"
    assert deployment.defaults.get("target") == "acme-corp-us-west-cluster"
    assert deployment.defaults.get("allow-cors") is None
    assert deployment.defaults.get("allow-configuration-snippets") is None

    assert config.deployments.get("i-dont-exist") is None

    config.lint().is_valid()


def test_minimal_valid_but_ineffective():
    config = Config.parse([{"deployment": {"name": "my-deployment"}}])
    deployment = config.deployments.get("my-deployment")
    assert deployment.name == "my-deployment"
    assert deployment.defaults is None

    # it is acceptable, but we warn that it doesn't auto-create deployments
    lint_result = config.lint()
    assert lint_result.warning_count == 1
    assert 'Deployment "my-deployment" has no defaults.target' in next(lint_result.warnings)["message"]


def test_minimal_that_will_create_a_deployment():
    config = Config.parse(
        [
            {
                "deployment": {
                    "name": "my-deployment",
                    "defaults": {
                        "target": "my-first-cluster",
                    },
                },
            },
        ],
    )
    deployment = config.deployments.get("my-deployment")
    assert deployment.name == "my-deployment"
    assert deployment.defaults.get("target") == "my-first-cluster"
    assert deployment.defaults.get("allow-cors") is None
    assert deployment.defaults.get("allow-configuration-snippets") is None


def test_that_you_can_define_if_cors_is_allowed():
    config = Config.parse(
        [
            {
                "deployment": {
                    "name": "my-deployment",
                    "defaults": {
                        "target": "my-second-cluster",
                        "allow-cors": True,
                    },
                },
            },
        ],
    )
    deployment = config.deployments.get("my-deployment")
    assert deployment.name == "my-deployment"
    assert deployment.defaults.get("target") == "my-second-cluster"
    assert deployment.defaults.get("allow-cors") is True
    assert deployment.defaults.get("allow-configuration-snippets") is None


def test_that_you_can_define_if_snippets_are_allowed():
    config = Config.parse(
        [
            {
                "deployment": {
                    "name": "my-deployment",
                    "defaults": {
                        "target": "my-third-cluster",
                        "allow-cors": False,
                        "allow-configuration-snippets": True,
                    },
                },
            },
        ],
    )
    deployment = config.deployments.get("my-deployment")
    assert deployment.name == "my-deployment"
    assert deployment.defaults.get("target") == "my-third-cluster"
    assert deployment.defaults.get("allow-cors") is False
    assert deployment.defaults.get("allow-configuration-snippets") is True


def test_deployment_merging():
    a = Config.parse([{"deployment": {"name": "aws-mars1-prod"}}])
    b = Config.parse([{"deployment": {"name": "aws-mars1-dev"}}])
    c = a.merge_with(b)
    assert len(c.deployments) == 2
    for deployment_name in a.deployments.keys() & b.deployments.keys():
        assert deployment_name in c.deployments
