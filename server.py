from flask import Flask, request, jsonify
import pickle
import pandas as pd

#**********
# Fix для Pickle
import sys
import DTransformer
sys.modules["__main__"] = DTransformer
#*****************

with open('models/pipeline.pkl', 'rb') as pkl_file:
    model = pickle.load(pkl_file)

app = Flask(__name__)

@app.route('/')
def index():
    msg = "Test message. The server is running"
    return msg

@app.route('/predict', methods=['POST'])
def predict():
    features = pd.read_json(request.json, orient='table')
    return jsonify({"prediction":model.predict(features).tolist()})

if __name__ == '__main__':
    app.run('0.0.0.0', 5001)