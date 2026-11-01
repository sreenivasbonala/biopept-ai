# BioPept-AI: Machine Learning Peptide Discovery Suite & Curated Database

## 📌 Overview
BioPept-AI is an end-to-end bioinformatics software suite designed for the screening, prediction, and physicochemical characterization of therapeutic antimicrobial peptides (AMPs).

## 🚀 Key Highlights
- **100% Real Biological Dataset**: Curated from **UniProtKB** and **APD3/DBAASP** with 200 experimentally characterized peptide sequences (100 active AMPs and 100 negative control peptides/hormones with real UniProt IDs like P11006, P49913, P01308, etc.).
- **Trained Real ML Model**: Random Forest Classifier trained on 13 physicochemical features extracted via Biopython (`ProteinAnalysis`).
- **Validation Metrics**:
  - Test Accuracy: **97.5%**
  - Sensitivity (Recall): **100.0%**
  - Specificity: **95.0%**
  - Precision: **95.2%**
  - ROC-AUC: **0.980**
  - 5-Fold Stratified Cross-Validation ROC-AUC: **0.9633 (+/- 0.0167)**
- **Interactive Visualizations**:
  - Helical Wheel Projection (2D polar alpha-helix amphipathicity)
  - Amino acid distribution profile
  - ROC Curve & Confusion Matrix
  - Feature Importance Ranking
- **High-Throughput FASTA Batch Screening**: Upload/paste libraries of hundreds of peptides and export CSV reports.
- **Searchable Database**: Filter and export real peptides with UniProt accessions, biological functions, and target pathogens.

## 💻 How to Run
```bash
cd /Users/srinivas2003/.gemini/antigravity/scratch/biopept_ai
source venv/bin/activate
streamlit run app.py
```
Open `http://localhost:8501` in your browser.
