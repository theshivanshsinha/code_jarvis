from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def hello():
    return "<h1>Test Flask App is Running!</h1>"

@app.route('/api/test')
def test():
    return jsonify({"status": "success", "message": "Test endpoint is working!"})

if __name__ == "__main__":
    print("Starting test Flask server on http://127.0.0.1:5001/")
    print("Press Ctrl+C to stop")
    app.run(host="0.0.0.0", port=5001, debug=True)
