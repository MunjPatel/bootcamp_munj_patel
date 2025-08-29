import sys
import os

src_path = os.path.abspath(os.path.join(os.getcwd(), 'src'))

if src_path not in sys.path:
    sys.path.append(src_path)

import utilities
from flask import Flask, request, jsonify
import numpy as np

app = Flask(__name__)
model = utilities.load_model("model/model.pkl")

@app.route('/predict', methods=['GET']) # Change POST to GET
def predict():
    try:
        # Get the 'last_close' value from URL query parameters (e.g., ?last_close=150.75)
        last_close_str = request.args.get('last_close')
        
        # Check if the parameter exists
        if last_close_str is None:
            return jsonify({"error": "Missing 'last_close' parameter in the URL"}), 400

        last_close = float(last_close_str)
        
        # Use your prediction logic
        prediction = utilities.predict_price(model, last_close)
        
        return jsonify({"predicted_close": prediction})
    except ValueError:
        return jsonify({"error": "Invalid value for 'last_close'. Must be a number."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/plot', methods=['GET'])
def plot():
    return app.send_static_file('price_trend.png')

if __name__ == '__main__':
    app.run(debug=True)