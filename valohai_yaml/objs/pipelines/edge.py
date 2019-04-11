from ..base import Item


def _split_prop(prop):
    return prop.split('.', 2)


edge_types = {
    'input',
    'output',
    'parameter',
    'metadata',
}


class Edge(Item):

    def __init__(self, source, target, configuration=None):
        if configuration is None:
            configuration = {}
        self.source = source
        self.target = target
        self.configuration = configuration

    @property
    def source_node(self):
        return _split_prop(self.source)[0]

    @property
    def source_type(self):
        return _split_prop(self.source)[1]

    @property
    def source_key(self):
        return _split_prop(self.source)[2]

    @property
    def target_node(self):
        return _split_prop(self.target)[0]

    @property
    def target_type(self):
        return _split_prop(self.target)[1]

    @property
    def target_key(self):
        return _split_prop(self.target)[2]

    @classmethod
    def parse(cls, data):
        if isinstance(data, list):  # Must be a shorthand
            data = {
                'source': data[0],
                'target': data[1],
            }
        return super(Edge, cls).parse(data)

    def lint(self, lint_result, context):
        pipeline = context['pipeline']
        node_map = pipeline.node_map
        if self.source_node not in node_map:
            lint_result.add_error('Pipeline {pipeline} edge source node {source_node} does not exist'.format(
                pipeline=pipeline.name,
                source_node=self.source_node,
            ))
        if self.target_node not in node_map:
            lint_result.add_error('Pipeline {pipeline} edge target node {target_node} does not exist'.format(
                pipeline=pipeline.name,
                target_node=self.target_node,
            ))
        if self.source_type not in edge_types:
            lint_result.add_error(
                'Pipeline {pipeline} source type {type} (between {source_node} and {target_node}) not valid'.format(
                    pipeline=pipeline.name,
                    source_node=self.source_node,
                    target_node=self.target_node,
                    type=self.source_type,
                ))
        if self.target_type not in edge_types:
            lint_result.add_error(
                'Pipeline {pipeline} target type {type} (between {source_node} and {target_node}) not valid'.format(
                    pipeline=pipeline.name,
                    source_node=self.source_node,
                    target_node=self.target_node,
                    type=self.target_type,
                ))

    def serialize_expanded(self):
        return {
            'source_node': self.source_node,
            'source_type': self.source_type,
            'source_key': self.source_key,
            'target_node': self.target_node,
            'target_type': self.target_type,
            'target_key': self.target_key,
            'configuration': self.configuration,
        }
