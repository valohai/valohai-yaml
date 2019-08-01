from valohai_yaml.objs import Config


def test_pipeline(pipeline_config: Config):
    lr = pipeline_config.lint()
    assert lr.is_valid()
    assert len([edge for edge in pipeline_config.pipelines['My little pipeline'].edges if (
        edge.source_node == 'batch1' and
        edge.source_type == 'parameter' and
        edge.source_key == 'aspect-ratio' and
        edge.target_node == 'batch2' and
        edge.target_type == 'parameter' and
        edge.target_key == 'aspect-ratio'
    )]) == 1
    assert any(
        (edge.source_type == 'output' and edge.source_key == 'model.pb')
            for edge
            in pipeline_config.pipelines['My medium pipeline'].edges
    )
