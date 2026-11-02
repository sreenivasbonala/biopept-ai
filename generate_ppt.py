import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "models")
OUTPUT_PPTX = os.path.join(BASE_DIR, "BioPept_AI_Prototype_Presentation.pptx")

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

# Color Palette (REVA University Theme + Professional Dark Mode)
DARK_NAVY = RGBColor(15, 23, 42)      # #0F172A
CARD_BG = RGBColor(30, 41, 59)        # #1E293B
BORDER_COL = RGBColor(51, 65, 85)     # #334155
REVA_ORANGE = RGBColor(234, 88, 12)   # #EA580C (REVA Branding)
CYAN_ACCENT = RGBColor(56, 189, 248)  # #38BDF8
EMERALD_ACC = RGBColor(16, 185, 129)  # #10B981
TEXT_WHITE = RGBColor(248, 250, 252)  # #F8FAFC
TEXT_MUTED = RGBColor(148, 163, 184)  # #94A3B8

def add_header(slide, title_text, category_text="REVA UNIVERSITY | SCHOOL OF APPLIED SCIENCES"):
    # Header Category / University
    cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.35), Inches(11.733), Inches(0.35))
    tf_c = cat_box.text_frame
    tf_c.word_wrap = True
    tf_c.margin_left = tf_c.margin_top = tf_c.margin_right = tf_c.margin_bottom = 0
    p_c = tf_c.paragraphs[0]
    p_c.text = category_text.upper()
    p_c.font.size = Pt(10)
    p_c.font.bold = True
    p_c.font.color.rgb = REVA_ORANGE
    
    # Title
    t_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.65), Inches(11.733), Inches(0.6))
    tf_t = t_box.text_frame
    tf_t.word_wrap = True
    tf_t.margin_left = tf_t.margin_top = tf_t.margin_right = tf_t.margin_bottom = 0
    p_t = tf_t.paragraphs[0]
    p_t.text = title_text
    p_t.font.size = Pt(22)
    p_t.font.bold = True
    p_t.font.color.rgb = TEXT_WHITE

def create_card(slide, left, top, width, height, border_color=None, fill_color=None):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color if fill_color else CARD_BG
    shape.line.color.rgb = border_color if border_color else BORDER_COL
    shape.line.width = Pt(1.5)
    return shape

# ==============================================================================
# SLIDE 1: Title & Team Introduction (REVA University Template)
# ==============================================================================
slide_layout = prs.slide_layouts[6] # Blank
s1 = prs.slides.add_slide(slide_layout)
bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
bg1.fill.solid()
bg1.fill.fore_color.rgb = DARK_NAVY
bg1.line.fill.background()

# Top University Banner Box
top_card = create_card(s1, Inches(0.8), Inches(0.6), Inches(11.733), Inches(1.3), REVA_ORANGE)
tf1 = top_card.text_frame
tf1.word_wrap = True
tf1.vertical_anchor = MSO_ANCHOR.MIDDLE
p = tf1.paragraphs[0]
p.alignment = PP_ALIGN.CENTER
p.text = "REVA UNIVERSITY, BENGALURU"
p.font.size = Pt(15)
p.font.bold = True
p.font.color.rgb = REVA_ORANGE

p2 = tf1.add_paragraph()
p2.alignment = PP_ALIGN.CENTER
p2.text = "School of Applied Sciences | Department of Bioinformatics"
p2.font.size = Pt(13)
p2.font.color.rgb = TEXT_MUTED

# Main Title Box
title_card = create_card(s1, Inches(0.8), Inches(2.1), Inches(11.733), Inches(2.6), CYAN_ACCENT)
tf_main = title_card.text_frame
tf_main.word_wrap = True
tf_main.vertical_anchor = MSO_ANCHOR.MIDDLE

p_badge = tf_main.paragraphs[0]
p_badge.alignment = PP_ALIGN.CENTER
p_badge.text = "🧬 PROTOTYPE PRESENTATION | AI FOR BIOINFORMATICS TRACK"
p_badge.font.size = Pt(11)
p_badge.font.bold = True
p_badge.font.color.rgb = CYAN_ACCENT

p_t = tf_main.add_paragraph()
p_t.alignment = PP_ALIGN.CENTER
p_t.text = "BioPept-AI"
p_t.font.size = Pt(38)
p_t.font.bold = True
p_t.font.color.rgb = TEXT_WHITE

p_sub = tf_main.add_paragraph()
p_sub.alignment = PP_ALIGN.CENTER
p_sub.text = "An AI-Driven Screening Platform & Curated Knowledgebase for Therapeutic Antimicrobial Peptides"
p_sub.font.size = Pt(14)
p_sub.font.color.rgb = RGBColor(203, 213, 225)

# Presenters Card
pres_card = create_card(s1, Inches(0.8), Inches(4.9), Inches(11.733), Inches(1.8))
tf_pres = pres_card.text_frame
tf_pres.word_wrap = True
tf_pres.vertical_anchor = MSO_ANCHOR.MIDDLE

p_pr1 = tf_pres.paragraphs[0]
p_pr1.alignment = PP_ALIGN.CENTER
p_pr1.text = "Presenters / Student Investigators:"
p_pr1.font.size = Pt(12)
p_pr1.font.bold = True
p_pr1.font.color.rgb = REVA_ORANGE

p_pr2 = tf_pres.add_paragraph()
p_pr2.alignment = PP_ALIGN.CENTER
p_pr2.text = "B. Sreenivas  &  N. Santhosh"
p_pr2.font.size = Pt(18)
p_pr2.font.bold = True
p_pr2.font.color.rgb = TEXT_WHITE

p_pr3 = tf_pres.add_paragraph()
p_pr3.alignment = PP_ALIGN.CENTER
p_pr3.text = "MSc Bioinformatics — I Semester  |  REVA University Science Fair 2026"
p_pr3.font.size = Pt(12)
p_pr3.font.color.rgb = TEXT_MUTED

# ==============================================================================
# SLIDE 2: Clinical Challenge & Problem Formulation
# ==============================================================================
s2 = prs.slides.add_slide(slide_layout)
bg2 = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
bg2.fill.solid()
bg2.fill.fore_color.rgb = DARK_NAVY
bg2.line.fill.background()
add_header(s2, "The Clinical Challenge: Antimicrobial Resistance (AMR) & Discovery Bottlenecks")

# 3 Column Cards
c_w = Inches(3.644)
c_h = Inches(5.3)
y_top = Inches(1.5)

# Card 1: Problem
card1 = create_card(s2, Inches(0.8), y_top, c_w, c_h, RGBColor(239, 68, 68))
tf = card1.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "⚠️ THE GLOBAL AMR CRISIS"
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = RGBColor(239, 68, 68)

points1 = [
    "• Conventional small-molecule antibiotics are failing rapidly against multidrug-resistant (MDR) superbugs.",
    "• WHO projects over 10 million deaths annually by 2050 without innovative antibacterial classes.",
    "• Bacterial envelope mutations continually defeat single-target intracellular enzyme inhibitors."
]
for pt in points1:
    p = tf.add_paragraph()
    p.text = pt
    p.font.size = Pt(11)
    p.font.color.rgb = RGBColor(226, 232, 240)
    p.space_before = Pt(8)

# Card 2: Why Peptides?
card2 = create_card(s2, Inches(4.844), y_top, c_w, c_h, CYAN_ACCENT)
tf = card2.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "🧬 WHY ANTIMICROBIAL PEPTIDES?"
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = CYAN_ACCENT

points2 = [
    "• Natural host-defense peptides (AMPs) target microbial lipid bilayers via biophysical disruption (pore lysis).",
    "• Negligible propensity to induce pathogen resistance due to fundamental membrane-level electrostatic attack.",
    "• Potent against Gram-negative, Gram-positive, and recalcitrant drug-resistant biofilm matrices."
]
for pt in points2:
    p = tf.add_paragraph()
    p.text = pt
    p.font.size = Pt(11)
    p.font.color.rgb = RGBColor(226, 232, 240)
    p.space_before = Pt(8)

# Card 3: Wet-Lab Bottleneck & AI Solution
card3 = create_card(s2, Inches(8.888), y_top, c_w, c_h, EMERALD_ACC)
tf = card3.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "🚀 THE BIOPEPT-AI SOLUTION"
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = EMERALD_ACC

points3 = [
    "• Wet-lab solid-phase synthesis costs thousands of dollars and months per peptide library with high attrition.",
    "• BioPept-AI extracts 13 biophysical descriptors to predict therapeutic activity in under 5 seconds.",
    "• Eliminates false negatives and provides structural amphipathic insight prior to chemical synthesis."
]
for pt in points3:
    p = tf.add_paragraph()
    p.text = pt
    p.font.size = Pt(11)
    p.font.color.rgb = RGBColor(226, 232, 240)
    p.space_before = Pt(8)

# ==============================================================================
# SLIDE 3: Publication-Quality Empirical Validation (Figures 1, 2, and 3)
# ==============================================================================
s3 = prs.slides.add_slide(slide_layout)
bg3 = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
bg3.fill.solid()
bg3.fill.fore_color.rgb = DARK_NAVY
bg3.line.fill.background()
add_header(s3, "Publication-Quality Empirical Validation & Model Interpretability", "REVA UNIVERSITY | BENCHMARK RIGOR & MACHINE LEARNING METRICS")

# Top Metrics Banner Card
kpi_card = create_card(s3, Inches(0.8), Inches(1.30), Inches(11.733), Inches(0.68), EMERALD_ACC)
tf_k = kpi_card.text_frame
tf_k.word_wrap = True
tf_k.vertical_anchor = MSO_ANCHOR.MIDDLE
p_k = tf_k.paragraphs[0]
p_k.alignment = PP_ALIGN.CENTER
p_k.text = "🎯 Test Accuracy: 97.5%   |   ⚡ Sensitivity (Recall): 100.0% (0 False Negatives)   |   🛡️ Specificity: 95.0%   |   📈 ROC-AUC: 0.980   |   🔁 5-Fold CV: 0.963 ± 0.017"
p_k.font.size = Pt(11)
p_k.font.bold = True
p_k.font.color.rgb = TEXT_WHITE

# 3 Figure Columns Side-by-Side
fig_w = Inches(3.72)
fig_h = Inches(5.05)
fig_y = Inches(2.10)

roc_img = os.path.join(MODELS_DIR, "roc_curve.png")
cm_img = os.path.join(MODELS_DIR, "confusion_matrix.png")
feat_img = os.path.join(MODELS_DIR, "feature_importance.png")

# Figure 1: ROC Curve Card
col1_left = Inches(0.80)
card_f1 = create_card(s3, col1_left, fig_y, fig_w, fig_h, CYAN_ACCENT)
# Card Title Box
t1_box = s3.shapes.add_textbox(col1_left + Inches(0.1), fig_y + Inches(0.08), fig_w - Inches(0.2), Inches(0.35))
tf1 = t1_box.text_frame
tf1.word_wrap = True
tf1.margin_left = tf1.margin_top = tf1.margin_right = tf1.margin_bottom = 0
p = tf1.paragraphs[0]
p.alignment = PP_ALIGN.CENTER
p.text = "Figure 1: ROC Curve (AUC = 0.980)"
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = CYAN_ACCENT

# Insert Image 1
if os.path.exists(roc_img):
    s3.shapes.add_picture(roc_img, col1_left + Inches(0.12), fig_y + Inches(0.45), width=Inches(3.48), height=Inches(2.90))

# Subtext 1
c1_box = s3.shapes.add_textbox(col1_left + Inches(0.12), fig_y + Inches(3.42), fig_w - Inches(0.24), Inches(1.5))
tfc1 = c1_box.text_frame
tfc1.word_wrap = True
tfc1.margin_left = tfc1.margin_top = tfc1.margin_right = tfc1.margin_bottom = 0
desc1 = [
    "• ROC-AUC of 0.980 on unseen 20% holdout test peptides.",
    "• 100% True Positive Rate at only 0.05 False Positive Rate.",
    "• Steep vertical ascent proves robust discriminatory power far exceeding random classifier baseline (AUC 0.50)."
]
for idx, d in enumerate(desc1):
    p = tfc1.paragraphs[0] if idx == 0 else tfc1.add_paragraph()
    p.text = d
    p.font.size = Pt(9.5)
    p.font.color.rgb = RGBColor(226, 232, 240)
    p.space_before = Pt(3) if idx > 0 else Pt(0)

# Figure 2: Confusion Matrix Card
col2_left = Inches(4.80)
card_f2 = create_card(s3, col2_left, fig_y, fig_w, fig_h, EMERALD_ACC)
# Card Title Box
t2_box = s3.shapes.add_textbox(col2_left + Inches(0.1), fig_y + Inches(0.08), fig_w - Inches(0.2), Inches(0.35))
tf2 = t2_box.text_frame
tf2.word_wrap = True
tf2.margin_left = tf2.margin_top = tf2.margin_right = tf2.margin_bottom = 0
p = tf2.paragraphs[0]
p.alignment = PP_ALIGN.CENTER
p.text = "Figure 2: Test Set Confusion Matrix"
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = EMERALD_ACC

# Insert Image 2
if os.path.exists(cm_img):
    s3.shapes.add_picture(cm_img, col2_left + Inches(0.25), fig_y + Inches(0.45), width=Inches(3.22), height=Inches(2.90))

# Subtext 2
c2_box = s3.shapes.add_textbox(col2_left + Inches(0.12), fig_y + Inches(3.42), fig_w - Inches(0.24), Inches(1.5))
tfc2 = c2_box.text_frame
tfc2.word_wrap = True
tfc2.margin_left = tfc2.margin_top = tfc2.margin_right = tfc2.margin_bottom = 0
desc2 = [
    "• 20 out of 20 Active AMPs correctly classified (100% Recall).",
    "• ZERO False Negatives: Critical safety guarantee so no active lead is missed.",
    "• 19 out of 20 Non-AMP controls correctly rejected (95% Specificity; 1 single false alert)."
]
for idx, d in enumerate(desc2):
    p = tfc2.paragraphs[0] if idx == 0 else tfc2.add_paragraph()
    p.text = d
    p.font.size = Pt(9.5)
    p.font.color.rgb = RGBColor(226, 232, 240)
    p.space_before = Pt(3) if idx > 0 else Pt(0)

# Figure 3: Feature Importance Card
col3_left = Inches(8.80)
card_f3 = create_card(s3, col3_left, fig_y, Inches(3.733), fig_h, REVA_ORANGE)
# Card Title Box
t3_box = s3.shapes.add_textbox(col3_left + Inches(0.1), fig_y + Inches(0.08), Inches(3.733) - Inches(0.2), Inches(0.35))
tf3 = t3_box.text_frame
tf3.word_wrap = True
tf3.margin_left = tf3.margin_top = tf3.margin_right = tf3.margin_bottom = 0
p = tf3.paragraphs[0]
p.alignment = PP_ALIGN.CENTER
p.text = "Figure 3: Bio-Feature Importances (Gini)"
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = REVA_ORANGE

# Insert Image 3
if os.path.exists(feat_img):
    s3.shapes.add_picture(feat_img, col3_left + Inches(0.12), fig_y + Inches(0.55), width=Inches(3.49), height=Inches(2.40))

# Subtext 3
c3_box = s3.shapes.add_textbox(col3_left + Inches(0.12), fig_y + Inches(3.05), Inches(3.733) - Inches(0.24), Inches(1.9))
tfc3 = c3_box.text_frame
tfc3.word_wrap = True
tfc3.margin_left = tfc3.margin_top = tfc3.margin_right = tfc3.margin_bottom = 0
desc3 = [
    "• Top Drivers: Sequence Length (14.2%) and Net Charge at pH 7.4 (12.8%).",
    "• Molecular Weight & Isoelectric Point (pI) drive selective lipid permeation.",
    "• Secondary structure fractions (Helix & Sheet) contribute significantly to amphipathic pore formation in bacterial membranes."
]
for idx, d in enumerate(desc3):
    p = tfc3.paragraphs[0] if idx == 0 else tfc3.add_paragraph()
    p.text = d
    p.font.size = Pt(9.5)
    p.font.color.rgb = RGBColor(226, 232, 240)
    p.space_before = Pt(3) if idx > 0 else Pt(0)

# ==============================================================================
# SLIDE 4: Working Prototype Architecture & Live Demo Walkthrough
# ==============================================================================
s4 = prs.slides.add_slide(slide_layout)
bg4 = s4.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
bg4.fill.solid()
bg4.fill.fore_color.rgb = DARK_NAVY
bg4.line.fill.background()
add_header(s4, "Live Prototype Capabilities & Demonstration Walkthrough")

# Banner for Live URL
url_card = create_card(s4, Inches(0.8), Inches(1.45), Inches(11.733), Inches(0.65), CYAN_ACCENT)
tf_u = url_card.text_frame
tf_u.vertical_anchor = MSO_ANCHOR.MIDDLE
p = tf_u.paragraphs[0]
p.alignment = PP_ALIGN.CENTER
p.text = "🌐 LIVE CLOUD APPLICATION: https://biopept-ai-eonpmshgbh5kwkkqvpjy4e.streamlit.app/"
p.font.size = Pt(12)
p.font.bold = True
p.font.color.rgb = CYAN_ACCENT

# 4 Feature Cards (2x2 Grid)
f_w = Inches(5.66)
f_h = Inches(2.25)

# Module 1
m1 = create_card(s4, Inches(0.8), Inches(2.30), f_w, f_h)
tf = m1.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "1. Single Sequence Predictor & Biomolecular Palette"
p.font.size = Pt(12)
p.font.bold = True
p.font.color.rgb = CYAN_ACCENT
p = tf.add_paragraph()
p.text = "• Instant Bayesian activity prediction with mechanistic interpretations.\n• Color-Coded Primary Structure Ribbon (Hydrophobic, Cationic, Acidic, Polar).\n• 2D Polar Helical Wheel Projection proving amphipathic alpha-helical clustering."
p.font.size = Pt(10)
p.font.color.rgb = RGBColor(226, 232, 240)
p.space_before = Pt(4)

# Module 2
m2 = create_card(s4, Inches(6.866), Inches(2.30), f_w, f_h)
tf = m2.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "2. High-Throughput Batch FASTA/CSV Screening"
p.font.size = Pt(12)
p.font.bold = True
p.font.color.rgb = EMERALD_ACC
p = tf.add_paragraph()
p.text = "• Automated multi-peptide library ingestion (FASTA / CSV formats).\n• Live pool-level KPI analytics: Total Evaluated, Active Hit %, Mean Charge.\n• Full clinical screening reports exportable to Excel/CSV with one click."
p.font.size = Pt(10)
p.font.color.rgb = RGBColor(226, 232, 240)
p.space_before = Pt(4)

# Module 3
m3 = create_card(s4, Inches(0.8), Inches(4.75), f_w, f_h)
tf = m3.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "3. Blind Validation on Phase-III Clinical Trial AMPs"
p.font.size = Pt(12)
p.font.bold = True
p.font.color.rgb = RGBColor(245, 158, 11)
p = tf.add_paragraph()
p.text = "• Tested on 14 completely unseen biological candidate peptides.\n• Accurately classifies clinical trial drugs Pexiganan (MSI-78) & Omiganan (MBI-226).\n• 100% negative control segregation for human GLP-1, GnRH & Somatostatin."
p.font.size = Pt(10)
p.font.color.rgb = RGBColor(226, 232, 240)
p.space_before = Pt(4)

# Module 4
m4 = create_card(s4, Inches(6.866), Inches(4.75), f_w, f_h)
tf = m4.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "4. Curated UniProt Knowledgebase & Open Access"
p.font.size = Pt(12)
p.font.bold = True
p.font.color.rgb = RGBColor(192, 132, 252)
p = tf.add_paragraph()
p.text = "• Integrated 200-peptide searchable database with direct UniProt Accession cross-links.\n• Enterprise dark-mode design with publication-grade ROC & confusion matrices.\n• 100% open-source reproducible pipeline on GitHub: sreenivasbonala/biopept-ai."
p.font.size = Pt(10)
p.font.color.rgb = RGBColor(226, 232, 240)
p.space_before = Pt(4)

# ==============================================================================
# SLIDE 5: Translational Impact, Future Scope & Conclusion
# ==============================================================================
s5 = prs.slides.add_slide(slide_layout)
bg5 = s5.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
bg5.fill.solid()
bg5.fill.fore_color.rgb = DARK_NAVY
bg5.line.fill.background()
add_header(s5, "Translational Impact, Future Scope & Conclusions")

# 2 Columns
c_w5 = Inches(5.66)
c_h5 = Inches(3.6)

# Left: Impact & Future
left_5 = create_card(s5, Inches(0.8), Inches(1.5), c_w5, c_h5, CYAN_ACCENT)
tf = left_5.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "🎯 SCIENTIFIC & TRANSLATIONAL IMPACT"
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = CYAN_ACCENT

impact_pts = [
    "• High-Throughput Acceleration: Reduces preclinical screening from months to seconds.",
    "• Zero False Negatives (100% Sensitivity): Guarantees no genuine therapeutic candidate is discarded in discovery pipelines.",
    "• Cost Reduction: Eliminates expensive wet-lab peptide synthesis failures.",
    "• Future Scope: Integration of Meta's ESM-2 zero-shot protein language model embeddings and automated AlphaFold 3D molecular docking."
]
for pt in impact_pts:
    p = tf.add_paragraph()
    p.text = pt
    p.font.size = Pt(10.5)
    p.font.color.rgb = RGBColor(226, 232, 240)
    p.space_before = Pt(6)

# Right: Summary & Repos
right_5 = create_card(s5, Inches(6.866), Inches(1.5), c_w5, c_h5, EMERALD_ACC)
tf = right_5.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "📦 PROJECT DELIVERABLES SUMMARY"
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = EMERALD_ACC

summary_pts = [
    "• Live Cloud Application: https://biopept-ai-eonpmshgbh5kwkkqvpjy4e.streamlit.app/",
    "• GitHub Code Repository: https://github.com/sreenivasbonala/biopept-ai",
    "• Verified Benchmark Dataset: 200 UniProtKB / APD3 experimentally validated peptides",
    "• Offline Package: Standalone cross-platform desktop launcher (Mac & Windows)",
    "• Conference Standard: Formatted for REVA University Science Fair 2026."
]
for pt in summary_pts:
    p = tf.add_paragraph()
    p.text = pt
    p.font.size = Pt(10.5)
    p.font.color.rgb = RGBColor(226, 232, 240)
    p.space_before = Pt(6)

# Bottom Thank You Box
ty_card = create_card(s5, Inches(0.8), Inches(5.35), Inches(11.733), Inches(1.5), REVA_ORANGE)
tf_ty = ty_card.text_frame
tf_ty.word_wrap = True
tf_ty.vertical_anchor = MSO_ANCHOR.MIDDLE

p_ty = tf_ty.paragraphs[0]
p_ty.alignment = PP_ALIGN.CENTER
p_ty.text = "THANK YOU!"
p_ty.font.size = Pt(24)
p_ty.font.bold = True
p_ty.font.color.rgb = REVA_ORANGE

p_d = tf_ty.add_paragraph()
p_d.alignment = PP_ALIGN.CENTER
p_d.text = "Department of Bioinformatics | School of Applied Sciences | REVA University, Bengaluru"
p_d.font.size = Pt(12)
p_d.font.color.rgb = TEXT_WHITE

p_q = tf_ty.add_paragraph()
p_q.alignment = PP_ALIGN.CENTER
p_q.text = "B. Sreenivas & N. Santhosh — Open for Faculty Questions & Live Prototype Demonstration"
p_q.font.size = Pt(11)
p_q.font.color.rgb = CYAN_ACCENT

prs.save(OUTPUT_PPTX)
print(f"✅ Generated 5-Slide Presentation: {OUTPUT_PPTX}")
