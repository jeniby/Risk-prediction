import json
import pickle

import pandas as pd
from flask import Flask, url_for, request, jsonify

from feature_preprocessing import processing_df

app = Flask(__name__)

CLF_FILENAME = 'finalized_model.sav'

clf = pickle.load(open(CLF_FILENAME, 'rb'))

@app.route('/api/ml/get_risk',  methods=['GET'])
def get_risk():
    try:
        data = request.get_json()
        processed_df = processing_df(pd.DataFrame(data))
        result = clf.predict_proba(processed_df)[:, 1]
    except Exception as e:
        print(e)
        raise
    return jsonify(data=result.tolist())

if __name__ == '__main__':
    app.run()
