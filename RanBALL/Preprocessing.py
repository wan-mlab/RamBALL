import numpy as np
import pandas as pd

class TPM():
    def counts2TPM(count, efflength):
        RPK = count / (efflength / 1000)  # Reads Per Kilobase
        PMSC_rpk = np.sum(RPK) / 1e6      # "per million" scaling factor
        return RPK / PMSC_rpk
    
    def FPKM2TPM(fpkm):
        fpkmtotpm = fpkm/sum(fpkm)*1e6 
        return fpkmtotpm
    
    def transform_counts(counts):
        efflen = pd.read_csv('Data/geneid_efflen_vm25_gencode.csv')
        efflen.index = efflen['geneid']
        efflen = efflen.drop(columns='geneid')
        intset = np.intersect1d(counts.columns, efflen.index)
        counts = counts.loc[:,intset]
        rown = counts.index
        coln = counts.columns
        efflen1 = efflen.loc[intset,] 
        tpm = np.apply_along_axis(lambda c: counts2TPM(c ,efflen1['efflen']), 1, counts)
        tpm = np.log2(tpm +1)
        tpm = pd.DataFrame(tpm)
        tpm.index = rown
        tpm.columns = coln
        ensembl = pd.read_csv('/Data/ensembl_list.csv')
        tpm_n = pd.DataFrame(0, index=tpm.index, columns=ensembl['ensembl'])
        for n in tpm.columns:
            if n in ensembl['ensembl'].values:
                tpm_n.loc[:,n] = tpm.loc[:,n]

        return tpm_n

    def transform_fpkm(fpkm):
        
        rown = fpkm.index
        coln = fpkm.columns
        tpm = np.apply_along_axis(lambda c: FPKM2TPM(c), 1, fpkm)
        tpm = np.log2(tpm +1)
        tpm = pd.DataFrame(tpm)
        tpm.index = rown
        tpm.columns = coln
        ensembl = pd.read_csv('/Data/ensembl_list.csv')
        tpm_n = pd.DataFrame(0, index=tpm.index, columns=ensembl['ensembl'])
        for n in tpm.columns:
            if n in ensembl['ensembl'].values:
                tpm_n.loc[:,n] = tpm.loc[:,n]

        return tpm_n