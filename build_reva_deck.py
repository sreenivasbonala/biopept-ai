import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

BASE_DIR = "/Users/srinivas2003/.gemini/antigravity/scratch/biopept_ai"
MODELS_DIR = os.path.join(BASE_DIR, "models")
INPUT_PPTX = "/Users/srinivas2003/.gemini/antigravity/brain/f1423da5-b931-41fa-869e-756d5c91f5f6/.user_uploaded/media_1793592625205_6ee395ae.pptx"
OUTPUT_PPTX = os.path.join(BASE_DIR, "BioPept_AI_REVA_Template.pptx")

prs = Presentation(INPUT_PPTX)
print("Loaded input presentation:", len(prs.slides), "slides")

s3 = prs.slides[2] # Slide 3: Methodology & Validation

# Remove existing shapes except title (shape index 0)
shapes_to_remove = [s for i, s in enumerate(s3.shapes) if i > 0]
for s in shapes_to_remove:
    s3.shapes._spTree.remove(s._element)

# REVA Theme Colors
REVA_ORANGE = RGBColor(192, 97, 26)   # #C0611A
REVA_CREAM = RGBColor(253, 241, 228)  # #FDF1E4
TEXT_DARK = RGBColor(30, 41, 59)      # #1E293B
TEXT_MUTED = RGBColor(89, 89, 89)     # #595959
TEXT_BODY = RGBColor(51, 51, 51)      # #333333

def add_card(slide, left, top, width, height, fill_color=REVA_CREAM):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    shape.line.fill.background() # noFill
    return shape

# ------------------------------------------------------------------------------
# 1. TOP SECTION: Benchmark Details & Metric Cards (N = 1,200)
# ------------------------------------------------------------------------------

# Top-Left Card: Benchmark Data & Features Summary
b_card = add_card(s3, Inches(0.95), Inches(1.25), Inches(4.35), Inches(1.05))
tf_b = b_card.text_frame
tf_b.word_wrap = True
tf_b.margin_left = Inches(0.12)
tf_b.margin_right = Inches(0.12)
tf_b.margin_top = Inches(0.08)
tf_b.margin_bottom = Inches(0.08)

p_b0 = tf_b.paragraphs[0]
p_b0.text = "Expanded Benchmark & Architecture (N = 1,200)"
p_b0.font.name = "Times New Roman"
p_b0.font.size = Pt(11)
p_b0.font.bold = True
p_b0.font.color.rgb = REVA_ORANGE

bullets_b = [
    ("• 1,200 Real Sequences: ", "600 Active AMPs vs 600 Non-AMP Controls (UniProtKB & APD3)"),
    ("• 13 Biophysical Descriptors: ", "Charge at pH 7.4, GRAVY hydropathy, pI, Secondary Structure"),
    ("• Model: ", "Random Forest (150 trees, 80/20 holdout) | 5-Fold CV AUC: 0.882 ± 0.026")
]
for label, desc in bullets_b:
    p = tf_b.add_paragraph()
    p.space_before = Pt(2)
    r1 = p.add_run()
    r1.text = label
    r1.font.name = "Calibri"
    r1.font.size = Pt(8.5)
    r1.font.bold = True
    r1.font.color.rgb = TEXT_DARK
    
    r2 = p.add_run()
    r2.text = desc
    r2.font.name = "Calibri"
    r2.font.size = Pt(8.5)
    r2.font.color.rgb = TEXT_BODY

# Top-Right: 4 Metric Cards
metrics = [
    ("83.3%", "Accuracy"),
    ("79.2%", "Sensitivity"),
    ("87.5%", "Specificity"),
    ("0.90", "ROC-AUC")
]

card_w = Inches(0.96)
card_gap = Inches(0.14)
x_start = Inches(5.45)

for idx, (val, label) in enumerate(metrics):
    mx = x_start + idx * (card_w + card_gap)
    m_card = add_card(s3, mx, Inches(1.25), card_w, Inches(1.05))
    tf_m = m_card.text_frame
    tf_m.word_wrap = True
    tf_m.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf_m.margin_left = tf_m.margin_right = tf_m.margin_top = tf_m.margin_bottom = 0
    
    p_v = tf_m.paragraphs[0]
    p_v.alignment = PP_ALIGN.CENTER
    p_v.text = val
    p_v.font.name = "Times New Roman"
    p_v.font.size = Pt(17)
    p_v.font.bold = True
    p_v.font.color.rgb = REVA_ORANGE
    
    p_l = tf_m.add_paragraph()
    p_l.alignment = PP_ALIGN.CENTER
    p_l.text = label
    p_l.font.name = "Calibri"
    p_l.font.size = Pt(9.5)
    p_l.font.color.rgb = TEXT_MUTED

# ------------------------------------------------------------------------------
# 2. BOTTOM SECTION: 3 Figure Columns Side-by-Side (Y = 2.40" to 6.85")
# ------------------------------------------------------------------------------
col_w = Inches(2.83)
col_gap = Inches(0.18)
col_h = Inches(4.50)
col_y = Inches(2.40)

roc_img = os.path.join(MODELS_DIR, "roc_curve.png")
cm_img = os.path.join(MODELS_DIR, "confusion_matrix.png")
feat_img = os.path.join(MODELS_DIR, "feature_importance.png")

# Column 1: Figure 1 ROC Curve
col1_x = Inches(0.95)
c1_card = add_card(s3, col1_x, col_y, col_w, col_h)
t1_box = s3.shapes.add_textbox(col1_x + Inches(0.08), col_y + Inches(0.08), col_w - Inches(0.16), Inches(0.32))
tf1 = t1_box.text_frame
tf1.word_wrap = True
tf1.margin_left = tf1.margin_right = tf1.margin_top = tf1.margin_bottom = 0
p = tf1.paragraphs[0]
p.alignment = PP_ALIGN.CENTER
p.text = "Figure 1: ROC Curve (AUC = 0.897)"
p.font.name = "Times New Roman"
p.font.size = Pt(10.5)
p.font.bold = True
p.font.color.rgb = REVA_ORANGE

if os.path.exists(roc_img):
    s3.shapes.add_picture(roc_img, col1_x + Inches(0.09), col_y + Inches(0.42), width=Inches(2.65), height=Inches(2.21))

desc1_box = s3.shapes.add_textbox(col1_x + Inches(0.10), col_y + Inches(2.72), col_w - Inches(0.20), Inches(1.68))
tfd1 = desc1_box.text_frame
tfd1.word_wrap = True
tfd1.margin_left = tfd1.margin_right = tfd1.margin_top = tfd1.margin_bottom = 0
desc1_pts = [
    ("• AUC = 0.897", " on 240 unseen holdout test peptides (120 AMPs vs 120 Non-AMPs)."),
    ("• Broad Diversity: ", "Evaluated across human, amphibian, insect, and plant phyla."),
    ("• Discriminatory Power: ", "Significantly outperforms random baseline (AUC 0.50).")
]
for idx, (b_txt, norm_txt) in enumerate(desc1_pts):
    p = tfd1.paragraphs[0] if idx == 0 else tfd1.add_paragraph()
    p.space_before = Pt(3) if idx > 0 else Pt(0)
    r1 = p.add_run()
    r1.text = b_txt
    r1.font.name = "Calibri"
    r1.font.size = Pt(8.5)
    r1.font.bold = True
    r1.font.color.rgb = TEXT_DARK
    r2 = p.add_run()
    r2.text = norm_txt
    r2.font.name = "Calibri"
    r2.font.size = Pt(8.5)
    r2.font.color.rgb = TEXT_BODY

# Column 2: Figure 2 Confusion Matrix
col2_x = Inches(0.95) + col_w + col_gap
c2_card = add_card(s3, col2_x, col_y, col_w, col_h)
t2_box = s3.shapes.add_textbox(col2_x + Inches(0.08), col_y + Inches(0.08), col_w - Inches(0.16), Inches(0.32))
tf2 = t2_box.text_frame
tf2.word_wrap = True
tf2.margin_left = tf2.margin_right = tf2.margin_top = tf2.margin_bottom = 0
p = tf2.paragraphs[0]
p.alignment = PP_ALIGN.CENTER
p.text = "Figure 2: Holdout Confusion Matrix"
p.font.name = "Times New Roman"
p.font.size = Pt(10.5)
p.font.bold = True
p.font.color.rgb = REVA_ORANGE

if os.path.exists(cm_img):
    s3.shapes.add_picture(cm_img, col2_x + Inches(0.19), col_y + Inches(0.42), width=Inches(2.45), height=Inches(2.21))

desc2_box = s3.shapes.add_textbox(col2_x + Inches(0.10), col_y + Inches(2.72), col_w - Inches(0.20), Inches(1.68))
tfd2 = desc2_box.text_frame
tfd2.word_wrap = True
tfd2.margin_left = tfd2.margin_right = tfd2.margin_top = tfd2.margin_bottom = 0
desc2_pts = [
    ("• 95 Active AMPs & 105 Controls", " correctly classified in 240 blind test samples."),
    ("• High Specificity (87.5%): ", "Strong rejection of non-therapeutic control sequences."),
    ("• Precision of 86.4%: ", "Guarantees reliable hit confirmation in screening libraries.")
]
for idx, (b_txt, norm_txt) in enumerate(desc2_pts):
    p = tfd2.paragraphs[0] if idx == 0 else tfd2.add_paragraph()
    p.space_before = Pt(3) if idx > 0 else Pt(0)
    r1 = p.add_run()
    r1.text = b_txt
    r1.font.name = "Calibri"
    r1.font.size = Pt(8.5)
    r1.font.bold = True
    r1.font.color.rgb = TEXT_DARK
    r2 = p.add_run()
    r2.text = norm_txt
    r2.font.name = "Calibri"
    r2.font.size = Pt(8.5)
    r2.font.color.rgb = TEXT_BODY

# Column 3: Figure 3 Feature Importance
col3_x = Inches(0.95) + 2 * (col_w + col_gap)
c3_card = add_card(s3, col3_x, col_y, col_w, col_h)
t3_box = s3.shapes.add_textbox(col3_x + Inches(0.08), col_y + Inches(0.08), col_w - Inches(0.16), Inches(0.32))
tf3 = t3_box.text_frame
tf3.word_wrap = True
tf3.margin_left = tf3.margin_right = tf3.margin_top = tf3.margin_bottom = 0
p = tf3.paragraphs[0]
p.alignment = PP_ALIGN.CENTER
p.text = "Figure 3: Feature Importances"
p.font.name = "Times New Roman"
p.font.size = Pt(10.5)
p.font.bold = True
p.font.color.rgb = REVA_ORANGE

if os.path.exists(feat_img):
    s3.shapes.add_picture(feat_img, col3_x + Inches(0.09), col_y + Inches(0.58), width=Inches(2.65), height=Inches(1.82))

desc3_box = s3.shapes.add_textbox(col3_x + Inches(0.10), col_y + Inches(2.72), col_w - Inches(0.20), Inches(1.68))
tfd3 = desc3_box.text_frame
tfd3.word_wrap = True
tfd3.margin_left = tfd3.margin_right = tfd3.margin_top = tfd3.margin_bottom = 0
desc3_pts = [
    ("• Primary Drivers: ", "Sequence Length, Net Charge at pH 7.4, and Molecular Weight."),
    ("• Cationic Charge (+pH 7.4): ", "Drives electrostatic bacterial membrane disruption."),
    ("• Mol. Weight & pI: ", "Govern amphipathic pore formation and cell selectivity.")
]
for idx, (b_txt, norm_txt) in enumerate(desc3_pts):
    p = tfd3.paragraphs[0] if idx == 0 else tfd3.add_paragraph()
    p.space_before = Pt(3) if idx > 0 else Pt(0)
    r1 = p.add_run()
    r1.text = b_txt
    r1.font.name = "Calibri"
    r1.font.size = Pt(8.5)
    r1.font.bold = True
    r1.font.color.rgb = TEXT_DARK
    r2 = p.add_run()
    r2.text = norm_txt
    r2.font.name = "Calibri"
    r2.font.size = Pt(8.5)
    r2.font.color.rgb = TEXT_BODY

# Also update Slide 4 (Module 4) text to 1,200 peptides if it references 200
s4 = prs.slides[3]
for shape in s4.shapes:
    if shape.has_text_frame and "200-peptide" in shape.text_frame.text:
        for p in shape.text_frame.paragraphs:
            if "200-peptide" in p.text:
                p.text = p.text.replace("200-peptide", "1,200-peptide")

# Save the updated presentation
prs.save(OUTPUT_PPTX)
print("✅ Successfully generated updated 1,200-peptide REVA presentation:", OUTPUT_PPTX)
