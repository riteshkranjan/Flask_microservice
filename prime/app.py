from flask import Flask, request, jsonify, render_template, send_file
app = Flask(__name__)
import requests
import os
from circuitbreaker import circuit
from circuitbreaker import  CircuitBreaker
from requests.exceptions import RequestException
from circuitbreaker import CircuitBreakerMonitor

class ServerDownException(Exception):
    pass

class MyCircuitBreaker(CircuitBreaker):
    FAILURE_THRESHOLD = 5
    RECOVERY_TIMEOUT = 30
    EXPECTED_EXCEPTION = ServerDownException

@app.route('/prime/calc/<int:num>')
def is_prime(num):
    a = get_sqrt(num)
    for i in range(2, a+1):
        if num%i == 0:
            return 'False'
    return 'True'

@app.route('/prime/circuits')
def circutinfo():
    return render_template("ciruit_monitor.html", all_circuits=CircuitBreakerMonitor.get_circuits(), closed_circuits=CircuitBreakerMonitor.get_closed())

@MyCircuitBreaker()
@app.route('/prime/hello')
def hello():
    return 'Hello'

@MyCircuitBreaker()
def get_sqrt(num):
    sqrt_service = "{}/sqrt/calc/{}".format(os.environ.get('HOME_URL'),num)
    r = requests.get(sqrt_service, verify=False, timeout=60)
    if r.status_code != 200:
        raise ServerDownException()
    return int(r.content.decode("utf-8"))

if __name__ == "__main__":
    import sys
    port = sys.argv[1]
    app.config['DEBUG'] = True
    app.run(port=port)