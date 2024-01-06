# app.py
from flask import Flask, render_template, request, jsonify
import joblib
from pathlib import Path
import numpy as np
import json

app = Flask(__name__)

model_path = Path("model/model.pkl")
vectorizer_path = Path("model/tfidf_vectorizer.pkl")
VECTORIZER = joblib.load(vectorizer_path)
MODEL = joblib.load(model_path)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()

    # Assuming your_model_module.predict takes input data and returns predictions
    tfidf = VECTORIZER .fit_transform([data['input']])
    predictions = "This tweet is " + MODEL.predict(tfidf)[0]

    def default(obj):
        if type(obj).__module__ == np.__name__:
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            else:
                return obj.item()
        raise TypeError('Unknown type:', type(obj))

    return jsonify({'predictions': json.dumps(predictions, default=default)})

if __name__ == '__main__':
    app.run(debug=True)