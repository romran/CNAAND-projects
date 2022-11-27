from flask import Flask, render_template
import logging

from jaeger_client import Config
from prometheus_flask_exporter import PrometheusMetrics
from flask_opentracing import FlaskTracing

# def init_tracer(service):
#     logging.getLogger('').handlers = []
#     logging.basicConfig(format='%(message)s', level=logging.DEBUG)

#     config = Config(
#         config={
#             'sampler': {
#                 'type': 'const',
#                 'param': 1,
#             },
#             'logging': True,
#         },
#         service_name=service,
#     )

#     # this call also sets opentracing.tracer
#     return config.initialize_tracer()

app = Flask(__name__)

# metrics = PrometheusMetrics(app, group_by='endpoint')
# metrics = PrometheusMetrics(app)
metrics = PrometheusMetrics(app, group_by='endpoint')
metrics.info("app_info", "App Info, this can be anything you want", version="1.0.3")
# config = Config(
#     config={
#         'sampler':
#         {'type': 'const',
#          'param': 1},
#                         'logging': True,
#                         'reporter_batch_size': 1,}, 
#                         service_name="service")
# jaeger_tracer = config.initialize_tracer()
# tracing = FlaskTracing(jaeger_tracer, True, app)
# tracing = FlaskTracing(init_tracer('frontend-service'), True, app)

@app.route('/')
def homepage():
    return render_template("main.html")


if __name__ == "__main__":
    # app.run(debug=True)
    app.run()