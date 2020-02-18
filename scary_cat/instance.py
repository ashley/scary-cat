from .validator import (
    InvalidResponse,
    validate_required_fields,
    validate_role,
    validate_instance_size,
    validate_zk_cluster,
    validate_kafka_cluster,
    validate_kafka_topic,
    validate_kafka_partitions
)

class Provision:
    role = 'tagdex'
    instance_size = ''
    zk_cluster = ''
    kafka_cluster = ''
    kafka_topic = ''
    partitions = ''
    additional_tags = ''

    def __init__(self, params=None):
        if params == None:
            return
        param_map = {'ROLE': self.role, 'INSTANCE_SIZE': self.instance_size, 'ZK_CLUSTER': self.zk_cluster, 'KAFKA_CLUSTER': self.kafka_cluster, 'KAFKA_TOPIC': self.kafka_topic, 'PARTITIONS': self.partitions, 'ADDITIONAL_TAGS': self.additional_tags}
        assert len(params) == len(param_map)
        for line in params:
            assert len(line) ==2
            if line[0] in param_map.keys():
                setattr(self, line[0].lower(), line[1])

    def __str__(self):
        formatted = [('%s: %s' % (str(t[0]),str(t[1]))) for t in self.as_tuples()]
        return '\n'.join(formatted)

    def as_tuples(self):
        return [
            ('ROLE', self.role),
            ('INSTANCE_SIZE', self.instance_size),
            ('ZK_CLUSTER', self.zk_cluster),
            ('KAFKA_CLUSTER', self.kafka_cluster),
            ('KAFKA_TOPIC', self.kafka_topic),
            ('PARTITIONS', self.partitions),
            ('ADDITIONAL_TAGS', self.additional_tags),
        ]

    def validate(self):
        try:
            validate_required_fields(self.as_tuples())
            validate_role(self.role)
            validate_instance_size(self.instance_size)
            validate_zk_cluster(self.zk_cluster)
            validate_kafka_cluster(self.kafka_cluster)
            validate_kafka_topic(self.kafka_topic)
            validate_kafka_partitions(self.partitions)
        except InvalidResponse as e:
            return False, str(e)
        return True, None

class RemoveHosts:
    nodes = ''
    shell_username = ''
    why = ''

    def __init__(self, params=None):
        if params == None:
            return
        param_map = {'NODES': self.nodes, 'SHELL_USERNAME': self.shell_username, 'WHY': self.why}
        assert len(params) == len(param_map)
        for line in params:
            assert len(line) ==2
            if line[0] in param_map.keys():
                setattr(self, line[0].lower(), line[1])

    def __str__(self):
        formatted = [('%s: %s' % (str(t[0]),str(t[1]))) for t in self.as_tuples()]
        return '\n'.join(formatted)

    def as_tuples(self):
        return [
            ('NODES', self.nodes),
            ('SHELL_USERNAME', self.shell_username),
            ('WHY', self.why),
        ]

    def validate(self):
        try:
            validate_required_fields(self.as_tuples())
        except InvalidResponse as e:
            return False, str(e)
        return True, None
