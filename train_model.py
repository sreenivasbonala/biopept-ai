import os
import json
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

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
MODELS_DIR = os.path.join(BASE_DIR, "models")
os.makedirs(MODELS_DIR, exist_ok=True)

csv_path = os.path.join(DATA_DIR, "real_benchmark_peptides.csv")
df = pd.read_csv(csv_path)
print(f"Loaded {len(df)} peptides from {csv_path}")

FEATURE_NAMES = [
    "Length",
    "Molecular_Weight",
    "Isoelectric_Point",
    "Net_Charge_pH74",
    "GRAVY_Hydrophobicity",
    "Aromaticity",
    "Instability_Index",
    "Helix_Fraction",
    "Turn_Fraction",
    "Sheet_Fraction",
    "Basic_Residues_Ratio",
    "Acidic_Residues_Ratio",
    "Hydrophobic_Residues_Ratio"
]

def extract_features_single(seq):
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
    
    # Residue class ratios
    basic_count = sum(seq.count(aa) for aa in "KRH")
    acidic_count = sum(seq.count(aa) for aa in "DE")
    hydrophobic_count = sum(seq.count(aa) for aa in "AILMFWV")
    
    return [
        length,
        mw,
        pi,
        charge,
        gravy,
        aroma,
        instability,
        sec_struc[0], # Helix
        sec_struc[1], # Turn
        sec_struc[2], # Sheet
        basic_count / length,
        acidic_count / length,
        hydrophobic_count / length
    ]

# Extract feature matrix
X_list = []
y_list = []
for idx, row in df.iterrows():
    try:
        feats = extract_features_single(row["Sequence"])
        X_list.append(feats)
        y_list.append(row["Label"])
    except Exception as e:
        print(f"Skipping sequence at index {idx}: {e}")

X = np.array(X_list)
y = np.array(y_list)

print(f"Feature matrix shape: {X.shape}, Label vector shape: {y.shape}")

# Train/Test Split (80% train, 20% test stratified)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)

print(f"Training samples: {len(X_train)}, Testing samples: {len(X_test)}")

# Cross-Validation on Training set
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
rf_cv = RandomForestClassifier(n_estimators=100, max_depth=6, random_state=42)
cv_scores = cross_val_score(rf_cv, X_train, y_train, cv=cv, scoring="roc_auc")
print(f"5-Fold Cross-Validation ROC-AUC: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")

# Fit final model
rf = RandomForestClassifier(n_estimators=120, max_depth=6, random_state=42)
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
    "Total_Samples": int(len(df)),
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

print("\n--- FINAL TEST EVALUATION METRICS ---")
for k, v in metrics.items():
    print(f"{k}: {v}")

# Save metrics JSON
metrics_path = os.path.join(MODELS_DIR, "metrics_summary.json")
with open(metrics_path, "w") as f:
    json.dump(metrics, f, indent=4)

# Save Model
model_path = os.path.join(MODELS_DIR, "amp_random_forest.pkl")
joblib.dump({"model": rf, "features": FEATURE_NAMES}, model_path)
print(f"\n✅ Model saved to {model_path}")

# -------------------------------------------------------------
# GENERATE PLOTS
# -------------------------------------------------------------
# 1. ROC Curve
fpr, tpr, _ = roc_curve(y_test, y_prob)
fig_roc, ax_roc = plt.subplots(figsize=(6, 5))
ax_roc.plot(fpr, tpr, color="#1E88E5", lw=2.5, label=f"Random Forest (AUC = {roc_auc:.3f})")
ax_roc.plot([0, 1], [0, 1], color="grey", lw=1.5, linestyle="--", label="Random Classifier (AUC = 0.500)")
ax_roc.set_xlim([0.0, 1.0])
ax_roc.set_ylim([0.0, 1.05])
ax_roc.set_xlabel("False Positive Rate (1 - Specificity)", fontsize=11, fontweight="bold")
ax_roc.set_ylabel("True Positive Rate (Sensitivity)", fontsize=11, fontweight="bold")
ax_roc.set_title("Receiver Operating Characteristic (ROC) Curve", fontsize=12, fontweight="bold", pad=10)
ax_roc.legend(loc="lower right", frameon=True)
ax_roc.grid(True, linestyle=":", alpha=0.6)
fig_roc.tight_layout()
fig_roc.savefig(os.path.join(MODELS_DIR, "roc_curve.png"), dpi=300)
plt.close(fig_roc)

# 2. Confusion Matrix Plot
fig_cm, ax_cm = plt.subplots(figsize=(5, 4.5))
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["Non-AMP", "Active AMP"])
disp.plot(cmap="Blues", ax=ax_cm, values_format="d")
ax_cm.set_title("Test Set Confusion Matrix", fontsize=12, fontweight="bold", pad=10)
fig_cm.tight_layout()
fig_cm.savefig(os.path.join(MODELS_DIR, "confusion_matrix.png"), dpi=300)
plt.close(fig_cm)

# 3. Feature Importance Plot
importances = rf.feature_importances_
sorted_idx = np.argsort(importances)
fig_feat, ax_feat = plt.subplots(figsize=(8, 5.5))
ax_feat.barh(np.array(FEATURE_NAMES)[sorted_idx], importances[sorted_idx], color="#00897B", edgecolor="black", alpha=0.85)
ax_feat.set_xlabel("Mean Decrease in Impurity (Feature Importance)", fontsize=11, fontweight="bold")
ax_feat.set_title("Random Forest Bio-Physicochemical Feature Importances", fontsize=12, fontweight="bold", pad=10)
ax_feat.grid(axis="x", linestyle=":", alpha=0.6)
fig_feat.tight_layout()
fig_feat.savefig(os.path.join(MODELS_DIR, "feature_importance.png"), dpi=300)
plt.close(fig_feat)

print(f"✅ Plots generated successfully in {MODELS_DIR}")
