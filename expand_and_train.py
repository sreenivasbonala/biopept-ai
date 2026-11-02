import os
import re
import json
import io
import urllib.request
import urllib.parse
import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from Bio.SeqUtils.ProtParam import ProteinAnalysis
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, roc_curve, confusion_matrix, ConfusionMatrixDisplay
)

BASE_DIR = "/Users/srinivas2003/.gemini/antigravity/scratch/biopept_ai"
DATA_DIR = os.path.join(BASE_DIR, "data")
MODELS_DIR = os.path.join(BASE_DIR, "models")
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)

# 1. Load existing curated 200 peptides as base seed
old_csv = os.path.join(DATA_DIR, "real_benchmark_peptides.csv")
backup_csv = os.path.join(DATA_DIR, "real_benchmark_peptides_200_backup.csv")
if os.path.exists(old_csv) and not os.path.exists(backup_csv):
    import shutil
    shutil.copy(old_csv, backup_csv)
    print("Backed up 200-peptide dataset to:", backup_csv)

existing_df = pd.read_csv(old_csv) if os.path.exists(old_csv) else pd.DataFrame()
print(f"Existing dataset seed: {len(existing_df)} sequences")

# 2. Fetch Additional Real AMPs from UniProtKB
print("\n--- Fetching Real Antimicrobial Peptides from UniProtKB ---")
headers = {"User-Agent": "BioPept-AI/2.0 (Academic Research; REVA University)"}

amp_records = []
if not existing_df.empty:
    for _, row in existing_df[existing_df["Label"] == 1].iterrows():
        amp_records.append({
            "Name": row["Name"], "Sequence": row["Sequence"].strip().upper(),
            "Source_Organism": row["Source_Organism"], "UniProt_Accession": row["UniProt_Accession"],
            "Biological_Class": row["Biological_Class"], "Biological_Function": row["Biological_Function"],
            "Label": 1
        })

# Query UniProt for reviewed AMPs with sizes up to 1000
query_amp = "reviewed:true AND (keyword:KW-0929 OR keyword:KW-0044)"
url_amp = f"https://rest.uniprot.org/uniprotkb/search?query={urllib.parse.quote(query_amp)}&format=tsv&fields=accession,id,gene_names,organism_name,length,sequence,ft_peptide&size=500"

try:
    req = urllib.request.Request(url_amp, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as resp:
        tsv_data = resp.read().decode("utf-8")
    df_u_amp = pd.read_csv(io.StringIO(tsv_data), sep="\t")
    print(f"Fetched {len(df_u_amp)} raw AMP records from UniProtKB")
    
    for _, row in df_u_amp.iterrows():
        seq = str(row["Sequence"]).strip().upper()
        pep_field = str(row.get("Peptide", ""))
        acc = str(row["Entry"])
        org = str(row.get("Organism", "Eukaryota"))
        entry_name = str(row.get("Entry Name", acc))
        
        # Check mature peptide annotations
        if pep_field and pep_field != "nan":
            matches = re.findall(r"PEPTIDE\s+(\d+)\.\.(\d+)(?:;\s*/note=\"([^\"]+)\")?", pep_field)
            for m in matches:
                start, end = int(m[0]), int(m[1])
                p_note = m[2] if len(m) > 2 and m[2] else entry_name
                mat_seq = seq[start-1:end]
                if 8 <= len(mat_seq) <= 80 and all(c in "ACDEFGHIKLMNPQRSTVWY" for c in mat_seq):
                    amp_records.append({
                        "Name": p_note, "Sequence": mat_seq, "Source_Organism": org,
                        "UniProt_Accession": acc, "Biological_Class": "Antimicrobial Peptide",
                        "Biological_Function": "Antibacterial membrane disruption", "Label": 1
                    })
        elif 10 <= len(seq) <= 60 and all(c in "ACDEFGHIKLMNPQRSTVWY" for c in seq):
            amp_records.append({
                "Name": entry_name, "Sequence": seq, "Source_Organism": org,
                "UniProt_Accession": acc, "Biological_Class": "Antimicrobial Peptide",
                "Biological_Function": "Antibacterial membrane disruption", "Label": 1
            })
except Exception as e:
    print(f"Error fetching AMPs from UniProt: {e}")

# 3. Query UniProt for Family Defensins and Cathelicidins if needed
query_amp2 = "reviewed:true AND (family:defensin OR family:cathelicidin OR family:cecropin OR family:magainin) AND length:[10 TO 80]"
url_amp2 = f"https://rest.uniprot.org/uniprotkb/search?query={urllib.parse.quote(query_amp2)}&format=tsv&fields=accession,id,gene_names,organism_name,length,sequence,ft_peptide&size=500"
try:
    req = urllib.request.Request(url_amp2, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as resp:
        tsv_data2 = resp.read().decode("utf-8")
    df_u_amp2 = pd.read_csv(io.StringIO(tsv_data2), sep="\t")
    print(f"Fetched {len(df_u_amp2)} additional family AMP records from UniProtKB")
    for _, row in df_u_amp2.iterrows():
        seq = str(row["Sequence"]).strip().upper()
        pep_field = str(row.get("Peptide", ""))
        acc = str(row["Entry"])
        org = str(row.get("Organism", "Eukaryota"))
        entry_name = str(row.get("Entry Name", acc))
        if pep_field and pep_field != "nan":
            matches = re.findall(r"PEPTIDE\s+(\d+)\.\.(\d+)(?:;\s*/note=\"([^\"]+)\")?", pep_field)
            for m in matches:
                start, end = int(m[0]), int(m[1])
                p_note = m[2] if len(m) > 2 and m[2] else entry_name
                mat_seq = seq[start-1:end]
                if 8 <= len(mat_seq) <= 80 and all(c in "ACDEFGHIKLMNPQRSTVWY" for c in mat_seq):
                    amp_records.append({
                        "Name": p_note, "Sequence": mat_seq, "Source_Organism": org,
                        "UniProt_Accession": acc, "Biological_Class": "Antimicrobial Peptide",
                        "Biological_Function": "Antibacterial membrane disruption", "Label": 1
                    })
        elif 10 <= len(seq) <= 60 and all(c in "ACDEFGHIKLMNPQRSTVWY" for c in seq):
            amp_records.append({
                "Name": entry_name, "Sequence": seq, "Source_Organism": org,
                "UniProt_Accession": acc, "Biological_Class": "Antimicrobial Peptide",
                "Biological_Function": "Antibacterial membrane disruption", "Label": 1
            })
except Exception as e:
    print(f"Error fetching family AMPs: {e}")

df_amps_all = pd.DataFrame(amp_records).drop_duplicates(subset=["Sequence"]).reset_index(drop=True)
print(f"✅ Total Unique Real AMP Sequences: {len(df_amps_all)}")

target_amps_count = min(len(df_amps_all), 600)
df_amps_final = df_amps_all.iloc[:target_amps_count].copy()
print(f"Selected {len(df_amps_final)} AMPs for training dataset.")

# 4. Fetch Real Non-AMP Biological Controls from UniProtKB
print("\n--- Fetching Real Non-AMP Controls from UniProtKB ---")
non_amp_records = []
if not existing_df.empty:
    for _, row in existing_df[existing_df["Label"] == 0].iterrows():
        non_amp_records.append({
            "Name": row["Name"], "Sequence": row["Sequence"].strip().upper(),
            "Source_Organism": row["Source_Organism"], "UniProt_Accession": row["UniProt_Accession"],
            "Biological_Class": row["Biological_Class"], "Biological_Function": row["Biological_Function"],
            "Label": 0
        })

query_non_amp = "reviewed:true AND NOT keyword:KW-0929 AND NOT keyword:KW-0044 AND NOT keyword:KW-0800 AND length:[12 TO 65]"
url_non_amp = f"https://rest.uniprot.org/uniprotkb/search?query={urllib.parse.quote(query_non_amp)}&format=tsv&fields=accession,id,gene_names,organism_name,length,sequence&size=800"

try:
    req = urllib.request.Request(url_non_amp, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as resp:
        tsv_non = resp.read().decode("utf-8")
    df_u_non = pd.read_csv(io.StringIO(tsv_non), sep="\t")
    print(f"Fetched {len(df_u_non)} Non-AMP control records from UniProtKB")
    for _, row in df_u_non.iterrows():
        seq = str(row["Sequence"]).strip().upper()
        acc = str(row["Entry"])
        org = str(row.get("Organism", "Metabolic / Structural"))
        entry_name = str(row.get("Entry Name", acc))
        if 10 <= len(seq) <= 65 and all(c in "ACDEFGHIKLMNPQRSTVWY" for c in seq):
            non_amp_records.append({
                "Name": entry_name, "Sequence": seq, "Source_Organism": org,
                "UniProt_Accession": acc, "Biological_Class": "Non-Antimicrobial Control",
                "Biological_Function": "Intracellular metabolic / physiological regulation", "Label": 0
            })
except Exception as e:
    print(f"Error fetching Non-AMPs from UniProt: {e}")

df_non_all = pd.DataFrame(non_amp_records).drop_duplicates(subset=["Sequence"]).reset_index(drop=True)
print(f"✅ Total Unique Real Non-AMP Sequences: {len(df_non_all)}")

# Balance with AMP count
target_non_count = len(df_amps_final)
df_non_final = df_non_all.iloc[:target_non_count].copy()
print(f"Selected {len(df_non_final)} Non-AMP controls for training dataset.")

# 5. Combine and Create 1,000+ Real Benchmark Dataset
df_total = pd.concat([df_amps_final, df_non_final], ignore_index=True)
# Add clean Peptide_ID
df_total["Peptide_ID"] = [
    f"AMP-{i+1:04d}" if row["Label"] == 1 else f"CTL-{i+1:04d}"
    for i, row in df_total.iterrows()
]
cols = ["Peptide_ID", "Name", "Sequence", "Source_Organism", "UniProt_Accession", "Biological_Class", "Biological_Function", "Label"]
df_total = df_total[cols].sample(frac=1.0, random_state=42).reset_index(drop=True)

total_seqs = len(df_total)
print(f"\n==========================================")
print(f"🎉 FINAL REAL BENCHMARK DATASET: {total_seqs} SEQUENCES!")
print(f"Active AMPs: {sum(df_total['Label'] == 1)} | Non-AMP Controls: {sum(df_total['Label'] == 0)}")
print(f"==========================================")

# Save the dataset
benchmark_1000_path = os.path.join(DATA_DIR, "real_benchmark_peptides_1000.csv")
df_total.to_csv(benchmark_1000_path, index=False)
# Also overwrite main real_benchmark_peptides.csv
df_total.to_csv(old_csv, index=False)
print("Saved to:", benchmark_1000_path, "and updated", old_csv)

# ------------------------------------------------------------------------------
# 6. FEATURE EXTRACTION (13 Bio-Physicochemical Descriptors)
# ------------------------------------------------------------------------------
print("\n--- Extracting 13 Bio-Physicochemical Descriptors ---")
FEATURE_NAMES = [
    "Length", "Molecular_Weight", "Isoelectric_Point", "Net_Charge_pH74",
    "GRAVY_Hydrophobicity", "Aromaticity", "Instability_Index",
    "Helix_Fraction", "Turn_Fraction", "Sheet_Fraction",
    "Basic_Residues_Ratio", "Acidic_Residues_Ratio", "Hydrophobic_Residues_Ratio"
]

def extract_features(seq):
    seq = seq.strip().upper()
    analyser = ProteinAnalysis(seq)
    length = len(seq)
    mw = analyser.molecular_weight()
    pi = analyser.isoelectric_point()
    charge = analyser.charge_at_pH(7.4)
    gravy = analyser.gravy()
    aroma = analyser.aromaticity()
    try:
        instability = analyser.instability_index()
    except Exception:
        instability = 40.0
    sec_struc = analyser.secondary_structure_fraction() # (helix, turn, sheet)
    basic_count = sum(seq.count(aa) for aa in "KRH")
    acidic_count = sum(seq.count(aa) for aa in "DE")
    hydrophobic_count = sum(seq.count(aa) for aa in "AILMFWV")
    return [
        length, mw, pi, charge, gravy, aroma, instability,
        sec_struc[0], sec_struc[1], sec_struc[2],
        basic_count / length, acidic_count / length, hydrophobic_count / length
    ]

X_list = [extract_features(s) for s in df_total["Sequence"]]
X = np.array(X_list)
y = df_total["Label"].values

print(f"Feature matrix shape: {X.shape}, Label vector shape: {y.shape}")

# ------------------------------------------------------------------------------
# 7. MODEL TRAINING & 5-FOLD CROSS-VALIDATION
# ------------------------------------------------------------------------------
X_train, X_test, y_train, y_test, df_tr, df_ts = train_test_split(
    X, y, df_total, test_size=0.20, random_state=42, stratify=y
)

print(f"Training partition: {len(X_train)} peptides | Testing partition: {len(X_test)} peptides")

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
rf_cv = RandomForestClassifier(n_estimators=120, max_depth=8, random_state=42)
cv_scores = cross_val_score(rf_cv, X_train, y_train, cv=cv, scoring="roc_auc")
print(f"5-Fold CV ROC-AUC: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")

# Fit final Random Forest model
rf = RandomForestClassifier(n_estimators=150, max_depth=8, random_state=42)
rf.fit(X_train, y_train)

# Predictions on Test set
y_pred = rf.predict(X_test)
y_prob = rf.predict_proba(X_test)[:, 1]

acc = accuracy_score(y_test, y_pred)
prec = precision_score(y_test, y_pred)
rec = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
roc_auc = roc_auc_score(y_test, y_prob)
cm = confusion_matrix(y_test, y_pred)
tn, fp, fn, tp = cm.ravel()
specificity = tn / (tn + fp)

metrics = {
    "Total_Samples": int(len(df_total)),
    "Train_Samples": int(len(X_train)),
    "Test_Samples": int(len(X_test)),
    "Accuracy": round(float(acc) * 100, 2),
    "Sensitivity_Recall": round(float(rec) * 100, 2),
    "Specificity": round(float(specificity) * 100, 2),
    "Precision": round(float(prec) * 100, 2),
    "F1_Score": round(float(f1) * 100, 2),
    "ROC_AUC": round(float(roc_auc), 4),
    "CV_5Fold_ROC_AUC": round(float(cv_scores.mean()), 4),
    "Confusion_Matrix": {
        "True_Positive": int(tp),
        "True_Negative": int(tn),
        "False_Positive": int(fp),
        "False_Negative": int(fn)
    },
    "Features": FEATURE_NAMES
}

print("\n--- NEW EVALUATION METRICS ON 1,000+ DATASET ---")
for k, v in metrics.items():
    print(f"{k}: {v}")

# Save metrics JSON
with open(os.path.join(MODELS_DIR, "metrics_summary.json"), "w") as f:
    json.dump(metrics, f, indent=4)

# Save Model
model_path = os.path.join(MODELS_DIR, "amp_random_forest.pkl")
joblib.dump({"model": rf, "features": FEATURE_NAMES}, model_path)
print(f"✅ Model saved to {model_path}")

# Save Holdout Test Results CSV
test_res = df_ts.copy()
test_res["Predicted_Class"] = ["Active AMP" if p == 1 else "Non-AMP" for p in y_pred]
test_res["AMP_Probability_%"] = np.round(y_prob * 100, 2)
test_res["Classification_Status"] = [
    "True Positive (Correct)" if yt==1 and yp==1 else
    "True Negative (Correct)" if yt==0 and yp==0 else
    "False Positive (Alert)" if yt==0 and yp==1 else "False Negative (Missed)"
    for yt, yp in zip(y_test, y_pred)
]
test_res_path = os.path.join(DATA_DIR, "Empirical_Model_Validation_Results.csv")
test_res.to_csv(test_res_path, index=False)

# ------------------------------------------------------------------------------
# 8. GENERATE NEW 300 DPI PUBLICATION FIGURES
# ------------------------------------------------------------------------------
print("\n--- Generating New Publication Figures (300 DPI) ---")

# Figure 1: ROC Curve
fpr, tpr, _ = roc_curve(y_test, y_prob)
fig_roc, ax_roc = plt.subplots(figsize=(6, 5), dpi=300)
ax_roc.plot(fpr, tpr, color="#0284C7", lw=2.5, label=f"Random Forest (AUC = {roc_auc:.3f})")
ax_roc.plot([0, 1], [0, 1], color="gray", linestyle="--", label="Random Classifier (AUC = 0.500)")
ax_roc.set_xlim([0.0, 1.0])
ax_roc.set_ylim([0.0, 1.05])
ax_roc.set_xlabel("False Positive Rate (1 - Specificity)", fontsize=11, fontweight="bold")
ax_roc.set_ylabel("True Positive Rate (Sensitivity)", fontsize=11, fontweight="bold")
ax_roc.set_title(f"Receiver Operating Characteristic (ROC) Curve (N = {len(X_test)})", fontsize=12, fontweight="bold", pad=10)
ax_roc.legend(loc="lower right", frameon=True)
ax_roc.grid(True, linestyle=":", alpha=0.6)
fig_roc.tight_layout()
fig_roc.savefig(os.path.join(MODELS_DIR, "roc_curve.png"), dpi=300)
plt.close(fig_roc)

# Figure 2: Confusion Matrix
fig_cm, ax_cm = plt.subplots(figsize=(5.5, 4.8), dpi=300)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["Non-AMP", "Active AMP"])
disp.plot(cmap="Blues", ax=ax_cm, values_format="d")
ax_cm.set_title(f"Holdout Test Confusion Matrix (N = {len(X_test)})", fontsize=12, fontweight="bold", pad=10)
fig_cm.tight_layout()
fig_cm.savefig(os.path.join(MODELS_DIR, "confusion_matrix.png"), dpi=300)
plt.close(fig_cm)

# Figure 3: Feature Importance
importances = rf.feature_importances_
sorted_idx = np.argsort(importances)
fig_feat, ax_feat = plt.subplots(figsize=(8, 5.5), dpi=300)
ax_feat.barh(np.array(FEATURE_NAMES)[sorted_idx], importances[sorted_idx], color="#0D9488", edgecolor="black", alpha=0.85)
ax_feat.set_xlabel("Mean Decrease in Impurity (Feature Importance)", fontsize=11, fontweight="bold")
ax_feat.set_title(f"Feature Importances across 13 Bio-Physicochemical Descriptors", fontsize=12, fontweight="bold", pad=10)
ax_feat.grid(axis="x", linestyle=":", alpha=0.6)
fig_feat.tight_layout()
fig_feat.savefig(os.path.join(MODELS_DIR, "feature_importance.png"), dpi=300)
plt.close(fig_feat)

print("✅ Successfully generated new 300 DPI plots in models/!")
