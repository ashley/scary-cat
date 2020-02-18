#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

role_regex = re.compile('[a-z0-9\-]*|$')
instance_size_regex = re.compile('[a-z0-9\.\-]*|$')
zk_cluster_regex = re.compile('[a-z0-9\-]*|$')
kafka_cluster_regex = re.compile('[a-z0-9\-]*|$')
kafka_topic_regex = re.compile('[a-z0-9\-]*|$')
kafka_partitions_regex = re.compile('([z0-9]*)$|^([0-9]*,)*([0-9]*)')
hosts_regex = re.compile('^(i-[a-z0-9]*)$|^(i-[a-z0-9]*,)*(i-[a-z0-9]*)$')

"""
ROLE: tagdex
INSTANCE_SIZE: i3.xlarge
ZK_CLUSTER: zookeeper-metrics-1
KAFKA_CLUSTER: kafka-metrics-1
KAFKA_TOPIC: points-slicer-datadog
PARTITIONS: 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15

AsdeE: nope
asdasd: asda,adsasd
Uasd_ajk:asdk124
TITLE: 0,a ,1, asd
"""

def validate_required_fields(tags):
    for tag in tags:
        if tag[1] == '' and tag[0] != 'ADDITIONAL_TAGS':
            raise InvalidResponse(msg="%s field is required"%tag[0])

def validate_role(tag):
    if role_regex.search(tag) != None and tag == role_regex.search(tag).group():
        return
    raise InvalidResponse(msg="Role should be lowercase:  %s"%tag)

def validate_instance_size(tag):
    if instance_size_regex.search(tag) != None and tag == instance_size_regex.search(tag).group():
        return
    raise InvalidResponse(msg="instance size:  %s"%tag)

def validate_zk_cluster(tag):
    if zk_cluster_regex.search(tag) != None and tag == zk_cluster_regex.search(tag).group():
        return
    raise InvalidResponse(msg="ZK Cluster:  %s"%tag)

def validate_kafka_cluster(tag):
    if kafka_cluster_regex.search(tag) != None and tag == kafka_cluster_regex.search(tag).group():
        return
    raise InvalidResponse(msg="Kafka Cluster:  %s"%tag)

def validate_kafka_topic(tag):
    if kafka_topic_regex.search(tag) != None and tag == kafka_topic_regex.search(tag).group():
        return
    raise InvalidResponse(msg="Kafka Topic:  %s"%tag)

def validate_kafka_partitions(tag):
    if kafka_partitions_regex.search(tag) != None and tag == kafka_partitions_regex.search(tag).group():
        return
    raise InvalidResponse(msg="Kafka Partitions:  %s"%tag)

def validate_hosts(tag):
    # https://pythex.org/?regex=%5E(i-%5Ba-z0-9%5D*)%24%7C%5E(i-%5Ba-z0-9%5D*%2C)*(i-%5Ba-z0-9%5D*)%24&test_string=i-123nksa%0Ai-213xsa%2Ci-123xasjdascd%0Ai-213xsa%2Ci-123xasjdascd%2Ci-asd3d%0A%0Ai-1231as%2C%20asd1%2C%0Ai-123asd3%2C%20i-123nksa%0Ai-213xsa%2Ci-123xasjda.scd%0Ai-213xsa%2Ci-123xasjdai-scd%0A%0A%0Ai-213xsa%2Ci-123xasjdascd%2C%0A&ignorecase=0&multiline=1&dotall=0&verbose=0
    if None != hosts_regex.search(tag) and tag == hosts_regex.search(tag).group():
        return
    raise InvalidResponse(msg="Hosts should have no space between hosts. Just commas.:  %s"%tag)

class InvalidResponse(Exception):
    msg = ""
    def __init__(self, msg=None):
        if msg is not None:
            self.msg = msg

    def __str__(self):
        return self.msg
