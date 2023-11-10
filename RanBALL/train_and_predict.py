import numpy as np
import pandas as pd
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder
from scipy.sparse import csr_matrix
import math

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
    subtype = pd.read_csv('/data/subtype.csv',encoding='gbk')
    dind = subtype[subtype.iloc[:,4] == '0'].index
    subtype = subtype.drop(index= dind)
    tpm_train = pd.read_csv('/data/filter_HTSeq_TPM.csv')
    tpm_train = tpm_train.drop(index= subtype['patient'])
    ind = tpm_train[tpm_train.subtype == 'Other'].index
    tpm_train = tpm_train.drop(index= ind)
    cind = tpm_train[tpm_train.subtype == 'CRLF2(non-Ph-like)'].index
    tpm_train = tpm_train.drop(index= cind)
    tpm_train.loc[:,'subtype'][tpm_train.loc[:, 'subtype'] == 'ZNF384'] = 'ZNF384 group'
    tpm_train.loc[:,'subtype'][tpm_train.loc[:, 'subtype'] == 'ZNF384-like'] = 'ZNF384 group'
    tpm_train.loc[:,'subtype'][tpm_train.loc[:, 'subtype'] == 'KMT2A'] = 'KMT2A group'
    tpm_train.loc[:,'subtype'][tpm_train.loc[:, 'subtype'] == 'KMT2A-like'] = 'KMT2A group'
    enc = LabelEncoder()
    enc.fit(tpm_train['subtype']) 
    tpm_train['subtype'] = enc.transform(tpm_train['subtype'])
    X_traintpm = tpm_train.drop(['subtype'], axis=1)
    ytpm = tpm_train['subtype']
    merged_tpm =pd.concat([X_traintpm, tpm_test], ignore_index=False)
    score = np.zeros(shape = (len(tpm_test.index),20))
    pro = np.zeros(shape = (len(tpm_test.index),20))
    P = [600,700,800,900,1000,1100,1200,1300,1400,1500,1600,1700,1800,1900,2000,2100,2200,2300,2400,2500]
    for p in P:
        oritpm = np.array(merged_tpm.T)
        rM = ranM(merged_tpm.T, p, 0.5)
        ntpm = (1 / np.sqrt(p)) * np.transpose(rM) @ oritpm
        ntpm = np.transpose(ntpm)
        model = SVC(kernel = 'linear',probability = True)
        ntpm = pd.DataFrame(ntpm)
        ntpm.index = merged_tpm.index
        model.fit(ntpm.loc[X_traintpm.index,], ytpm)
        score = score + model.decision_function(ntpm.loc[tpm_test.index,])
        pro = pro + model.predict_proba(ntpm.loc[tpm_test.index,])
    final_score = score / len(P)
    final_pro = pro / len(P)
    Probability = final_pro.max(axis=1)
    pred = np.argmax(final_score,axis = 1)
    sub_pred = enc.inverse_transform(pred)

    results = {'Samples':tpm_test.index, 'Subtype_pred': sub_pred,'Probability': Probability}
    results = pd.DataFrame(results)
    results.to_csv('Prediction_results.csv', index=False)
    print(results)
    return results
