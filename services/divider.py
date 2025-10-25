# services/divider.py
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/health", methods=["GET"])
def health():
    return "divider ok", 200

@app.route("/divide", methods=["POST"])
def divide():
    data = request.get_json(force=True)
    a = data.get("a")
    b = data.get("b")
    try:
        da = float(a)
        db = float(b)
        if db == 0:
            return jsonify({"error": "division by zero"}), 400
        res = da / db
    except Exception as e:
        return jsonify({"error": "invalid input", "detail": str(e)}), 400
    return jsonify({"result": res}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5004)
