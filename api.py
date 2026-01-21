# API endpoint for financial risk analysis
# Requires: flask, risk_scorer
from flask import Flask, request, jsonify
from risk_scorer import compute_scores

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze():
    print("Received request")
    data = request.json
    if not data or 'description' not in data:
        return jsonify({"error": "Invalid input: requires 'description' field"}), 400
    
    try:
        result = compute_scores(data)
        return jsonify(result)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)