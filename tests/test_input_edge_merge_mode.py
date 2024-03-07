from valohai_yaml.pipelines.conversion import PipelineConverter


def test_input_override_mode(input_edge_merge_mode_config):
    config = input_edge_merge_mode_config
    pipeline = config.pipelines["check-edge-merge-mode"]
    assert len(pipeline.nodes) == 3
    converted_pipeline = PipelineConverter(config=config, commit_identifier="latest").convert_pipeline(pipeline)
    step1 = converted_pipeline["nodes"][0]
    step2 = converted_pipeline["nodes"][1]
    step3 = converted_pipeline["nodes"][2]

    # override-mode not defined
    assert step1["template"]["inputs"]["dataset"] == []

    # override-mode = replace
    assert step2["template"]["inputs"]["dataset"] == []

    # override-mode = append
    assert step3["template"]["inputs"]["dataset"] == ["/step3"]
