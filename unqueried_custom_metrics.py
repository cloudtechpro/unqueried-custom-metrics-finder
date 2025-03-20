#!/usr/bin/env python3
# Must be the first line
from __future__ import print_function

"""
Get All Unqueried Custom Metrics in the Last 24 hours
"""

import os
import requests
from datetime import datetime, timedelta
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.metrics_api import MetricsApi

# Fetch the API keys from environment variables
DATADOG_API_KEY = os.getenv('DD_API_KEY')
DATADOG_APP_KEY = os.getenv('DD_APP_KEY')

# Ensure the API keys are set
if not DATADOG_API_KEY or not DATADOG_APP_KEY:
    raise ValueError("Please set the DD_API_KEY and DD_APP_KEY environment variables")

# Set up the Datadog configuration
configuration = Configuration()
configuration.api_key['apiKeyAuth'] = DATADOG_API_KEY
configuration.api_key['appKeyAuth'] = DATADOG_APP_KEY

def is_custom_metric(metric_name):
    standard_prefixes = [
        'datadog.', 'aws.', 'gcp.', 'azure.', 'system.', 'synthetics.',
        'docker.', 'kubernetes.', 'postgresql.', 'redis.', 'nginx.', 'jvm.',
        'jmx.', 'vm.', 'elasticsearch.', 'dd.', 'elastic_cloud.', 'containerd.',
        'kubernetes_state', 'process.', 'kafka.', 'confluent_cloud.', 'cloudflare.',
        'timescale.', 'container.', 'cri.', 'kubelet.', 'kube_proxy.', 'kube_scheduler.',
        'kube_controller_manager.', 'kube_apiserver.', 'kube_dns.'
    ]
    return not any(metric_name.startswith(prefix) for prefix in standard_prefixes)

def query_metric_data(metric_name, start, end):
    url = "https://api.datadoghq.com/api/v1/query"
    params = {
        "from": start,
        "to": end,
        "query": f"avg:{metric_name}{{*}}"
    }
    headers = {
        "DD-API-KEY": DATADOG_API_KEY,
        "DD-APPLICATION-KEY": DATADOG_APP_KEY
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

def get_unqueried_custom_metrics():
    with ApiClient(configuration) as api_client:
        metrics_api = MetricsApi(api_client)
        
        # Fetch tag configurations (which includes metrics)
        response = metrics_api.list_tag_configurations()
        metrics = response.data

        unqueried_metrics = []
        checked_metrics = []
        two_hours_ago = datetime.now() - timedelta(hours=24)
        start_time = int(two_hours_ago.timestamp())
        end_time = int(datetime.now().timestamp())

        # Filter metrics that have not been queried in the last 24 hours
        for metric in metrics:
            metric_dict = metric.to_dict()
            metric_name = metric_dict['id']
            if is_custom_metric(metric_name):
                checked_metrics.append(metric_name)
                print(f"Checking custom metric: {metric_name}")

                try:
                    query_response = query_metric_data(metric_name, start_time, end_time)
                    if not query_response.get("series"):
                        print(f"Adding metric {metric_name} to unqueried list")
                        unqueried_metrics.append(metric_name)
                except Exception as e:
                    print(f"Error querying metric {metric_name}: {e}")
        
        return checked_metrics, unqueried_metrics

def main():
    checked_metrics, unqueried_metrics = get_unqueried_custom_metrics()
    print("Custom metrics not queried in the last 24 hours:")
    for metric_id in unqueried_metrics:
        print(metric_id)
    print(f"Total custom metrics checked: {len(checked_metrics)}")
    print(f"Total unqueried custom metrics: {len(unqueried_metrics)}")

if __name__ == '__main__':
    main()