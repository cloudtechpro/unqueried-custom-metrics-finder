# Unqueried Custom Metrics Finder

This script identifies custom metrics in Datadog that have not been queried in the last 24 hours. It leverages the Datadog API to fetch metric information and performs queries to determine if the metrics have been used recently.

## Prerequisites

Before you can use this script, ensure you have the following:

1. **Python 3.x** installed on your system.
2. **Datadog API and Application keys** set up as environment variables.

## Setting Up Environment Variables

Make sure you have the Datadog API and Application keys set in your environment:

```sh
export DD_API_KEY="your_datadog_api_key"
export DD_APP_KEY="your_datadog_application_key"
```

## Installation
1. Clone the repository or copy the script to your local machine.
2. Install the required Python packages using pip:
```
pip install requests datadog_api_client
```

## Usage
Run the script using Python:
```
python unqueried_custom_metrics.py
```

## Script Overview
### Imports
The script imports necessary libraries and modules:
- `os` for environment variable access.
- `requests` for making HTTP requests.
- `datetime` and `timedelta` for handling time calculations.
- Datadog client libraries for API interactions.

## Environment Variables
The script fetches the Datadog API and Application keys from environment variables:
```
DATADOG_API_KEY = os.getenv('DD_API_KEY')
DATADOG_APP_KEY = os.getenv('DD_APP_KEY')
```

## Functions
- `is_custom_metric(metric_name)`: Checks if a given metric name is a custom metric by comparing it against a list of standard prefixes.
- `query_metric_data(metric_name, start, end)`: Queries Datadog for data on a specific metric within a given time range.
- `get_unqueried_custom_metrics()`: Fetches all metrics, checks if they are custom, and determines if they have been queried in the last 24 hours.

## Main Function
The main() function coordinates the script's operations:

- Calls `get_unqueried_custom_metrics()` to get the list of custom metrics and identify unqueried ones.
- Prints out the unqueried custom metrics and provides a summary of the checked and unqueried metrics.

Example Output
After running the script, you will see output similar to this:
```
Custom metrics not queried in the last 24 hours:
custom.metric1
custom.metric2
...
Total custom metrics checked: 50
Total unqueried custom metrics: 10
```

## Error Handling
The script includes basic error handling to manage issues during API calls and data processing.