#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

role_regex = re.compile('[a-z0-9]-*|$')
instance_size_regex = re.compile('[a-z0-9]\.-*|$')
zk_cluster_regex = re.compile('[a-z0-9]-*|$')
kafka_cluster_regex = re.compile('[a-z0-9]-*|$')
kafka_topic_regex = re.compile('[a-z0-9]-*|$')
kafka_partitions_regex = re.compile('^([z0-9]*)$|^([0-9]*,)*([0-9]*)$')

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

def validate_role(tag):
    if tag != role_regex.search(tag).group():
        return ValidatorResponse(False,msg="Role should be lowercase:  %s"%tag)
    return ValidatorResponse(True)

def validate_instance_size(tag):
    if tag != instance_size_regex.search(tag).group():
        return ValidatorResponse(False,msg="instance size:  %s"%tag)
    return ValidatorResponse(True)

def validate_zk_cluster(tag):
    if tag != zk_cluster_regex.search(tag).group():
        return ValidatorResponse(False,msg="ZK Cluster:  %s"%tag)
    return ValidatorResponse(True)

def validate_kafka_cluster(tag):
    if tag != kafka_cluster_regex.search(tag).group():
        return ValidatorResponse(False,msg="Kafka Cluster:  %s"%tag)
    return ValidatorResponse(True)

def validate_kafka_topic(tag):
    if tag != kafka_topic_regex.search(tag).group():
        return ValidatorResponse(False,msg="Kafka Topic:  %s"%tag)
    return ValidatorResponse(True)

def validate_kafka_partitions(tag):
    if tag != kafka_partitions_regex.search(tag).group():
        return ValidatorResponse(False,msg="Kafka Partitions:  %s"%tag)
    return ValidatorResponse(True)

class ValidatorResponse:
    def __init__(self, valid, msg=""):
        self.valid = valid
        self.msg = msg 
