import datetime
from RanBALL.train_and_predict import train_and_predict

def Predict(Exp,exp_type):
    start_time = datetime.datetime.now()
    print("B-ALL subtype identification...")
    if 'Exp' not in locals():
        print("No expression data is provided!")
    print("-----------------------------------------------------------------------")
    print("Preprocessing:")
    
    if 'exp_type' == 'Raw_count':
        tpm = TPM.transform_counts(Exp)
    elif 'exp_type' == 'FPKM':
        tpm = TPM.transform_fpkm(Exp)
    elif 'exp_type' == 'TPM':
        tpm = Exp
    
    results = train_and_predict(tpm_test = tpm)

    end_time = datetime.datetime.now()

    t = (end_time - start_time).total_seconds() / 60.0  # difference time in minutes

    print("Prediction completed!")
    print("-----------------------------------------------------------------------")
    print("Total running time:", t, "minutes")

    return results

