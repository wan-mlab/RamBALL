# RanBALL: An Ensemble Random Projection Model for Identifying Subtypes of B-cell Acute Lymphoblastic Leukemia

**RanBALL** (an Ensemble **Ran**dom Projection-Based Model for Identifying **B**-Cell **A**cute **L**ymphoblastic **L**eukemia Subtypes), an accurate and cost-effective model for B-ALL subtype identification based on transcriptomic profiling only. Leveraging the random projection and SVM techniques, our **RanBALL** enables to identify accurately and efficiently 20 distinct B-ALL subtypes, which could provide reliable diagnostic insights that can significantly aid clinical decision-making processes.

## Flowchart of RanBALL
![Flowchart of RanBALL](Flowchart.png)

## Installation
1. Clone the RanBALL git repository
```bash
git clone https://github.com/wan-mlab/RanBALL.git
```
2. Navigate to the directory of RanBALL package
```bash
cd /your path/RanBALL
pip install .
```
## Tutorial
### Jupyter notebook
1. Modify the System Path and import module
```bash
import sys; sys.path.append('RanBALL')
from RanBALL import RanBALL
```
2. unzip and read the test file
```bash
test = pd.read_csv('filter_TPM_test.csv', index_col=0)
```
3. B-ALL subtype prediction
```bash
RanBALL.Predict(Exp = test, exp_type = 'TPM')
```
   exp_type also could be 'Raw_count' and 'FPKM', which would be transformed to TPM for model training.

4. Example Outputs

![Example Outputs](output1.png)
The prediction results will be stored and exported to the Prediction_results.csv 
## Authors
Lusheng Li, Hanyu Xiao, Xinchao Wu, Shibiao Wan

## Publication
RanBALL: Identifying B-cell acute lymphoblastic leukemia subtypes based on an ensemble random projection model, Cancer Research, vol. 84 (6_ Supplement), pp.4907-4907.
*Li, L.., Xiao, H., Khoury, J. D., Wang, J., & Wan, S*.*
[AACR Annual Meeting 2024, San Diego, CA, Apr. 2024](https://aacrjournals.org/cancerres/article/84/6_Supplement/4907/738413)
