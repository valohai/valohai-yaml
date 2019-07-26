from valohai_yaml.objs import Config


def test_pipeline(pipeline_config: Config):
    e0 = pipeline_config.pipelines['My little pipeline'].edges[0]
    assert e0.source_node == 'batch1'
    assert e0.source_type == 'parameter'
    assert e0.source_key == 'aspect-ratio'
    assert e0.target_node == 'batch2'
    assert e0.target_type == 'parameter'
    assert e0.target_key == 'aspect-ratio'
