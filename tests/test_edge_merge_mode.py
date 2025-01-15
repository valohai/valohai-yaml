from valohai_yaml.objs.pipelines.edge_merge_mode import EdgeMergeMode
from valohai_yaml.pipelines.conversion import PipelineConverter


def test_edge_override_mode(edge_merge_mode_config):
    config = edge_merge_mode_config
    pipeline = config.pipelines["check-edge-merge-mode"]
    assert len(pipeline.nodes) == 3
    converted_pipeline = PipelineConverter(config=config, commit_identifier="latest").convert_pipeline(pipeline)
    nodes = converted_pipeline["nodes"]

    # override-mode not defined, so it's elided
    assert "edge-merge-mode" not in nodes[0]

    # override-mode = replace, but that's the default so not included
    assert "edge-merge-mode" not in nodes[1]

    # override-mode = append
    assert nodes[2]["edge-merge-mode"] == EdgeMergeMode.APPEND.value
