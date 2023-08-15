def Ramball(Exp,exp_type):
    start_time = datetime.datetime.now()
    print("B-ALL subtype indentification...")
    if 'Exp' not in locals():
        print("No expression data is provided!")
    print("-----------------------------------------------------------------------")
    print("Preprocessing:")
    
    if 'exp_type' == 'Raw_count':
        tpm = TPM.transform(Exp)
    
    prediction = train_and_predict(tpm_test = tpm)

    end_time = datetime.datetime.now()

    t = (end_time - start_time).total_seconds() / 60.0  # difference time in minutes

    print("Prediction complete!")
    print("-----------------------------------------------------------------------")
    print("Total running time:", t, "minutes")

