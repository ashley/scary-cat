#!/usr/bin/env python3
from __future__ import absolute_import
import os
from datadog import initialize, api
from prettycli import red, blue

from .instance import Provision

options = {
}

def scrape_host(host):
    try:
        host = host['tags_by_source']
        box = Provision()
        box.instance_size = get_tag(host,'instance-type','Amazon Web Services')
        box.zk_cluster = get_tag(host,'zk_cluster','Chef')
        box.kafka_cluster = get_tag(host,'kafka_cluster','Chef')
        box.kafka_topic = get_tag(host,'kafka_topic','Chef')
        box.partitions = get_partitions(host,'kafka_partition','Chef')
        return box
    except:
        print(red('There was an error parsing host from Datadog'))
        raise

def get_tag(host, sub_label, main_label):
    try:
        tags = host[main_label]
        for tag in tags:
            context = tag.split(':')
            if len(context) != 2:
                continue
            if context[0] == sub_label:
                return context[1]
    except:
        print(host)
        raise

def get_partitions(host, sub_label, main_label):
    try:
        tags = host[main_label]
        result = []
        for tag in tags:
            context = tag.split(':')
            if len(context) != 2:
                continue
            if context[0] == sub_label:
                result.append(context[1])
        arr = [int(x) for x in result]
        arr.sort()
        return ','.join(map(str, arr))
    except Exception:
        print(host)
        raise

def get_host(host_id):
    print(blue("Searching Host on Datadog..."))
    res = api.Hosts.search(filter='service:tagdex,host:'+host_id)
    hosts = res['host_list']
    assert len(hosts) == 1, "We found more than one host with that host_id. The host may be inval    id."
    host = hosts[0]
    return scrape_host(host)

def get_dependencies():
    if os.getenv("DATADOG_API_KEY"):
            options['api_key'] = os.getenv("DATADOG_API_KEY") 
    else:
        print(red("DATADOG_API_KEY missing from environment variables"))
        exit()
    if os.getenv("DATADOG_APP_KEY"):
            options['app_key'] = os.getenv("DATADOG_APP_KEY") 
    else:
        print(red("DATADOG_APP_KEY missing from environment variables"))
        exit()
    return options

get_dependencies()
initialize(**options)
