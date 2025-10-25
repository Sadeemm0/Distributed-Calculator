from flask import Flask, request, jsonify
import requests
import threading
import time

app = Flask(__name__)

available_services = {
    'add': [], 'subtract': [], 'multiply': [], 'divide': []
}

SERVICE_PORTS = {
    'add': 5001, 'subtract': 5002, 'multiply': 5003, 'divide': 5004
}

def health_check():
    while True:
        for service, port in SERVICE_PORTS.items():
            url = f"http://localhost:{port}/health"
            try:
                response = requests.get(url, timeout=2)
                if response.status_code == 200:
                    if url not in available_services[service]:
                        available_services[service].append(url)
                else:
                    if url in available_services[service]:
                        available_services[service].remove(url)
            except:
                if url in available_services[service]:
                    available_services[service].remove(url)
        time.sleep(3)

@app.route('/calculate/<operation>', methods=['POST'])
def calculate(operation):
    if operation not in available_services:
        return jsonify({"error": "Unknown operation"}), 400
    service_urls = available_services[operation]
    if not service_urls:
        return jsonify({"error": f"Service {operation} unavailable"}), 503
    service_url = service_urls[0].replace('/health', f'/{operation}')
    data = request.json
    try:
        a = float(data.get('a'))
        b = float(data.get('b'))
    except:
        return jsonify({"error": "Invalid parameters"}), 400
    try:
        resp = requests.post(service_url, json={'a': a, 'b': b}, timeout=5)
        return jsonify(resp.json()), resp.status_code
    except:
        return jsonify({"error": "Service error"}), 500

if __name__ == "__main__":
    threading.Thread(target=health_check, daemon=True).start()
    app.run(host='0.0.0.0', port=5000)
