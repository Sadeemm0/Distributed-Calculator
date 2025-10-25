# services/subtractor.py
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/health", methods=["GET"])
def health():
    return "subtractor ok", 200

@app.route("/subtract", methods=["POST"])
def subtract():
    data = request.get_json(force=True)
    a = data.get("a")
    b = data.get("b")
    try:
        res = float(a) - float(b)
    except Exception as e:
        return jsonify({"error": "invalid input", "detail": str(e)}), 400
    return jsonify({"result": res}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
