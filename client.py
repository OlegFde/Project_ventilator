import requests
import pandas as pd
from tkinter import filedialog as fd

if __name__ == '__main__':
    
    df = pd.read_csv(fd.askopenfilename(), index_col=0)
    df.drop('id', axis=1, inplace=True)
    result = df.to_json(orient="table")
    
    # POST-request
    r = requests.post('http://localhost:5001/predict', json=result)
    # request status
    print('Status code: {}'.format(r.status_code))
    
    if r.status_code == 200:
        # if success
        print('Prediction: {}'.format(r.json()['prediction']))
    else:
        # if fault
        print(r.text)
