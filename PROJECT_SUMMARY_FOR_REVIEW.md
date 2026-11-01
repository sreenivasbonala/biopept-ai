# BioPept-AI: Project Overview & Evaluation Guide

## 1. Aim of the Project
The primary objective of **BioPept-AI** is to combat global Antimicrobial Resistance (AMR) by providing an intelligent, rapid computational screening platform for **Therapeutic Antimicrobial Peptides (AMPs)**. Instead of spending months and high costs on wet-lab screening, BioPept-AI extracts 13 biophysical and physicochemical descriptors directly from peptide primary sequences and classifies their therapeutic efficacy using a trained Machine Learning model.

## 2. Key Modules & Features
1. **🔬 Single Peptide Predictor**:
   - Computes live Physicochemical properties (MW, pI, Net Charge at pH 7.4, GRAVY hydropathy, instability index, secondary structure fractions).
   - Machine Learning probability prediction (Active AMP vs Non-AMP).
   - 2D Polar Helical Wheel projection (Alpha-helix amphipathicity visualization).
   - Residue frequency distribution bar chart.
2. **📊 High-Throughput Batch Screening**:
   - Supports uploading custom `.fasta` or `.csv` files containing hundreds of candidate sequences.
   - Generates interactive sortable screening reports and one-click CSV export.
3. **🗄️ Curated Database (UniProtKB & APD3)**:
   - 200 experimentally characterized real peptides (100 active AMPs and 100 negative control human hormones/proteins with genuine UniProt Accessions).
   - Searchable and exportable.
4. **📈 Model Validation & Metrics Dashboard**:
   - Test Accuracy: **97.5%**
   - Sensitivity (Recall): **100.0%** (zero false negatives)
   - Specificity: **95.0%**
   - ROC-AUC: **0.980**
   - 5-Fold Stratified Cross-Validation ROC-AUC: **0.963**
   - Publication-grade ROC curves, Confusion Matrices, and Feature Importance rankings.

## 3. How to Run the Project (For Your Friend)
### On Mac / Linux:
```bash
pip install -r requirements.txt
streamlit run app.py
```
*(Or double click `run_mac_linux.sh`)*

### On Windows:
```cmd
pip install -r requirements.txt
streamlit run app.py
```
*(Or double click `run_windows.bat`)*

Then open `http://localhost:8501` in your web browser.

## 4. How to Test (Step-by-Step)
1. Go to **Single Peptide Predictor** -> Select **Magainin-2** -> Click **Analyze & Predict** (Result: Active AMP, 98.01% confidence).
2. Go to **High-Throughput Screening** -> Upload `data/unseen_real_test_candidates.csv` (or `.fasta`) -> Click **Execute High-Throughput Screening**.
3. Observe how Phase-III Clinical Trial AMPs (Pexiganan, Omiganan) are predicted as Active AMPs while human hormone controls (GLP-1, GnRH, Somatostatin) are accurately segregated as Non-AMPs.
4. Download the screening report as CSV.
