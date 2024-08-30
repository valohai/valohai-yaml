from valohai_yaml.objs.pipelines.edge_merge_mode import EdgeMergeMode
from valohai_yaml.pipelines.conversion import PipelineConverter


def test_edge_override_mode(edge_merge_mode_config):
    config = edge_merge_mode_config
    pipeline = config.pipelines["check-edge-merge-mode"]
    assert len(pipeline.nodes) == 3
    converted_pipeline = PipelineConverter(config=config, commit_identifier="latest").convert_pipeline(pipeline)
    node0 = converted_pipeline["nodes"][0]
    node1 = converted_pipeline["nodes"][1]
    node2 = converted_pipeline["nodes"][2]

    # override-mode not defined
    assert node0["edge-merge-mode"] == EdgeMergeMode.REPLACE.value

    # override-mode = replace
    assert node1["edge-merge-mode"] == EdgeMergeMode.REPLACE.value

    # override-mode = append
    assert node2["edge-merge-mode"] == EdgeMergeMode.APPEND.value
