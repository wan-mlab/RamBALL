import numpy as np
import pandas as pd
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder
from scipy.sparse import csr_matrix
import math
import os

def ranM(scdata, p, seedn):
    # for random projection; note scdata: m*n, m is the feature dimensions, n is the sample number; p is the reduced dimension
    m = scdata.shape[0]  # the number of features
    n = scdata.shape[1]  # number of samples

    s = np.sqrt(m)  # according to the paper 'Very Sparse Random Projection'

    if seedn % 1 == 0:
        np.random.seed(int(seedn))
        x0 = np.random.choice([np.sqrt(s), 0, -np.sqrt(s)], size=m * p, replace=True, p=[1/(2*s), 1 - 1/s, 1/(2*s)])
    else:
        x0 = np.random.choice([np.sqrt(s), 0, -np.sqrt(s)], size=m * p, replace=True, p=[1/(2*s), 1 - 1/s, 1/(2*s)])

    x = csr_matrix(x0.reshape(m, p), dtype=np.float32)

    return x  # the same format, feature*sample

def train_and_predict(tpm_test):
    score = np.zeros(shape = (len(tpm_test.index),20))
    pro = np.zeros(shape = (len(tpm_test.index),20))
    P = [600,700,800,900,1000,1100,1200,1300,1400,1500,1600,1700,1800,1900,2000,2100,2200,2300,2400,2500]
    for p in P:
        oritpm = np.array(tpm_test.T)
        rM = ranM(tpm_test.T, p, 1)
        ntpm = (1 / np.sqrt(p)) * np.transpose(rM) @ oritpm
        ntpm = np.transpose(ntpm)
        ntpm = pd.DataFrame(ntpm)
        ntpm.index = tpm_test.index
        with open(os.path.dirname(__file__) + '/models/model_' + str(p) +'RP.h5', 'rb') as f:
            model = pickle.load(f)
        score = score + model.decision_function(ntpm.loc[tpm_test.index,])
        pro = pro + model.predict_proba(ntpm.loc[tpm_test.index,])
    final_score = score / len(P)
    final_pro = pro / len(P)
    Probability = final_pro.max(axis=1)
    pred = np.argmax(final_score,axis = 1)
    label_transform = {0:'BCL2/MYC', 1:'DUX4', 2:'ETV6-RUNX1',3:'ETV6-RUNX1-like', 4:'HLF',
       5:'High hyperdiploid', 6:'IKZF1 N159Y', 7:'KMT2A group',
       8:'Low hyperdiploid', 9:'Low hypodiploid', 10:'MEF2D', 11:'NUTM1',
       12:'Near haploid', 13:'PAX5 P80R', 14:'PAX5alt', 15:'Ph', 16:'Ph-like',
       17:'TCF3-PBX1', 18:'ZNF384 group', 19:'iAMP21'}
    sub_pred = [label_transform[value] for value in pred]

    results = {'Samples':tpm_test.index, 'Subtype_pred': sub_pred,'Probability': Probability}
    results = pd.DataFrame(results)
    results.to_csv('Prediction_results.csv', index=False)
    print(results)
    return results
