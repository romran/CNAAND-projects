**Note:** For the screenshots, you can store all of your answer images in the `answer-img` directory.

## Verify the monitoring installation

*TODO:* run `kubectl` command to show the running pods and services for all components. Take a screenshot of the output and include it here to verify the installation

![](/answer-img/services.PNG)

## Setup the Jaeger and Prometheus source
*TODO:* Expose Grafana to the internet and then setup Prometheus as a data source. Provide a screenshot of the home page after logging into Grafana.

![](/answer-img/grafana-login.PNG)

## Create a Basic Dashboard
*TODO:* Create a dashboard in Grafana that shows Prometheus as a source. Take a screenshot and include it here.

![](/answer-img/basic-dashboard.PNG)

## Describe SLO/SLI
*TODO:* Describe, in your own words, what the SLIs are, based on an SLO of *monthly uptime* and *request response time*.

Service-Level Indicators or SLIs measure the availability of the given Service-Level Objective or SLOs. For the given SLOs system should track:
- HTTP statuses for *monthly uptime* to cover SLO like: 99% of all HTTP statuses will be 20x in a given month
- Latency and service times for *request response time* to cover SLO like: 99% of all requests will take less than 20ms in a given month

## Creating SLI metrics.
*TODO:* It is important to know why we want to measure certain metrics for our customer. Describe in detail 5 metrics to measure these SLIs. 

Metrics to measure SLIs should be described in terms of four core properties, called the Four Golden Signals, including Availability:
- Latency - The time taken to serve a request (usually measured in ms)
- Traffic - The amount of stress on a system from demand (such as the number of HTTP requests/second)
- Errors - The number of requests that are failing (such as number of HTTP 500 responses)
- Saturation - The overall capacity of a service (such as the percentage of memory or CPU used)
- Availability - The overall time system services are available (such as the percentage of uptime)

## Create a Dashboard to measure our SLIs
*TODO:* Create a dashboard to measure the uptime of the frontend and backend services We will also want to measure to measure 40x and 50x errors. Create a dashboard that show these values over a 24 hour period and take a screenshot.

![](/answer-img/slis-dashboard.PNG)

## Tracing our Flask App
*TODO:*  We will create a Jaeger span to measure the processes on the backend. Once you fill in the span, provide a screenshot of it here.

![](/answer-img/jaeger_trace.PNG)

## Jaeger in Dashboards
*TODO:* Now that the trace is running, let's add the metric to our current Grafana dashboard. Once this is completed, provide a screenshot of it here.

![](/answer-img/jaeger_grafana.PNG)

## Report Error
*TODO:* Using the template below, write a trouble ticket for the developers, to explain the errors that you are seeing (400, 500, latency) and to let them know the file that is causing the issue.

TROUBLE TICKET

Name: GET http://localhost:8081/star 404 (NOT FOUND)

Date: 2020-11-13

Subject: The requested URL was not found on the server.

Affected Area: Backend service

Severity: High

Description: Seems given Mongo DB uri doesn't exist in backend service.

## Creating SLIs and SLOs
*TODO:* We want to create an SLO guaranteeing that our application has a 99.95% uptime per month. Name three SLIs that you would use to measure the success of this SLO.

- Availability: CPU usage between 0.05% and 99.95%
- Saturation: memory usage between 0.05% and 99.95%
- Traffic: more than 99.95% of HTTP request should return status code 20x  
- Errors: less than 0.05% of HTTP request should return status code 50x or 40x
## Building KPIs for our plan
*TODO*: Now that we have our SLIs and SLOs, create KPIs to accurately measure these metrics. We will make a dashboard for this, but first write them down here.

- Availability KPI could be measured with `process_cpu_seconds_total` function for CPU usage
- Saturation KPI could be measure with `container_memory_max_usage_bytes` function for memory usage
- Traffic KPI could be measured with `flask_http_request_total` from `flask_prometheus_exporter` by filtering 20x status code 
- Errors KPI could be measured with `flask_http_request_total` from `flask_prometheus_exporter` by filtering 50x and 40x status code 

## Final Dashboard
*TODO*: Create a Dashboard containing graphs that capture all the metrics of your KPIs and adequately representing your SLIs and SLOs. Include a screenshot of the dashboard here, and write a text description of what graphs are represented in the dashboard.  

![](/answer-img/final-dashboard.PNG)
- `CPU usage` - application CPU usage to measure Availability SLI
- `Memory usage` - application memory usage to measure Saturation SLI
- `Number of 20x response` - number of 20x responses for frontend and backend to measure Traffic SLI
- `Number of 40x and 50x errors` - number of 40x and 50x errors to measure Errors SLI