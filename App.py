import streamlit as st
import pandas as pd
import numpy as np
import io
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

# =========================================================
# PAGE SETTINGS
# =========================================================

st.set_page_config(
    page_title="MadiNeutro AI",
    page_icon="🤖",
    layout="wide"
)

# =========================================================
# LANGUAGE
# =========================================================

if "language" not in st.session_state:
    st.session_state.language = "English"

language = st.sidebar.selectbox(
    "🌐 Language / اللغة",
    ["English", "العربية"]
)

st.session_state.language = language

arabic = language == "العربية"

# =========================================================
# TRANSLATIONS
# =========================================================

T = {
    "title": "MadiNeutro AI"
    if not arabic else "MadiNeutro AI",

    "subtitle":
        "Neutrosophic Entropy-Based Multi-Criteria Decision Making Platform"
        if not arabic
        else
        "منصة اتخاذ القرار متعدد المعايير باستخدام المنطق النيوتروسوفي وEntropy",

    "settings":
        "⚙️ System Settings"
        if not arabic else
        "⚙️ إعدادات النظام",

    "domain":
        "Application Domain"
        if not arabic else
        "مجال التطبيق",

    "data":
        "1️⃣ Data Input"
        if not arabic else
        "1️⃣ إدخال البيانات",

    "results":
        "2️⃣ Decision Results"
        if not arabic else
        "2️⃣ نتائج القرار",

    "analysis":
        "3️⃣ Results Analysis"
        if not arabic else
        "3️⃣ تحليل النتائج",

    "charts":
        "4️⃣ Data Visualization"
        if not arabic else
        "4️⃣ الرسوم البيانية",

    "export":
        "5️⃣ Export Results"
        if not arabic else
        "5️⃣ تصدير النتائج",

    "about":
        "About MadiNeutro AI"
        if not arabic else
        "عن MadiNeutro AI",

    "best":
        "Best Alternative"
        if not arabic else
        "أفضل بديل",

    "score":
        "Final Score"
        if not arabic else
        "الدرجة النهائية",

    "alternatives":
        "Number of Alternatives"
        if not arabic else
        "عدد البدائل",

    "criteria":
        "Number of Criteria"
        if not arabic else
        "عدد المعايير",

    "download_csv":
        "📥 Download CSV"
        if not arabic else
        "📥 تحميل CSV",

    "download_pdf":
        "📄 Download PDF Report"
        if not arabic else
        "📄 تحميل تقرير PDF",

    "download_excel":
        "📊 Download Excel"
        if not arabic else
        "📊 تحميل Excel",

    "interpretation":
        "Interpretation"
        if not arabic else
        "التفسير العلمي"
}

# =========================================================
# HEADER
# =========================================================

st.title("🤖 " + T["title"])

st.subheader(T["subtitle"])

st.write(
    "A research-oriented decision support system using "
    "Neutrosophic Logic and Entropy."
    if not arabic
    else
    "نظام دعم قرار بحثي يعتمد على المنطق النيوتروسوفي وتحليل Entropy."
)

st.divider()

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.header(T["settings"])

domain = st.sidebar.selectbox(
    T["domain"],
    [
        "Agricultural Crop Evaluation"
        if not arabic else "تقييم المحاصيل الزراعية",

        "Companies and Projects"
        if not arabic else "تقييم الشركات والمشاريع",

        "Universities Evaluation"
        if not arabic else "تقييم الجامعات",

        "Custom"
        if not arabic else "مخصص"
    ]
)

# =========================================================
# DEFAULT DATA
# =========================================================

if "Agricultural" in domain or "الزراعية" in domain:

    default_data = {
        "Alternative": [
            "Tomato",
            "Papaya",
            "Banana",
            "Millet",
            "Sesame",
            "Cotton"
        ],

        "Truth (T)": [
            0.90,
            0.85,
            0.80,
            0.75,
            0.70,
            0.68
        ],

        "Indeterminacy (I)": [
            0.05,
            0.08,
            0.10,
            0.10,
            0.10,
            0.12
        ],

        "Falsity (F)": [
            0.05,
            0.07,
            0.10,
            0.15,
            0.20,
            0.18
        ]
    }

elif "Companies" in domain or "الشركات" in domain:

    default_data = {
        "Alternative": [
            "Company A",
            "Company B",
            "Company C",
            "Company D"
        ],

        "Truth (T)": [
            0.85,
            0.70,
            0.90,
            0.65
        ],

        "Indeterminacy (I)": [
            0.08,
            0.15,
            0.05,
            0.10
        ],

        "Falsity (F)": [
            0.07,
            0.15,
            0.05,
            0.25
        ]
    }

elif "Universities" in domain or "الجامعات" in domain:

    default_data = {
        "Alternative": [
            "University A",
            "University B",
            "University C",
            "University D"
        ],

        "Truth (T)": [
            0.88,
            0.80,
            0.92,
            0.75
        ],

        "Indeterminacy (I)": [
            0.06,
            0.10,
            0.04,
            0.12
        ],

        "Falsity (F)": [
            0.06,
            0.10,
            0.04,
            0.13
        ]
    }

else:

    default_data = {
        "Alternative": [
            "Alternative A",
            "Alternative B",
            "Alternative C",
            "Alternative D"
        ],

        "Truth (T)": [
            0.85,
            0.75,
            0.90,
            0.70
        ],

        "Indeterminacy (I)": [
            0.10,
            0.15,
            0.05,
            0.20
        ],

        "Falsity (F)": [
            0.05,
            0.10,
            0.05,
            0.10
        ]
    }

# =========================================================
# DATA EDITOR
# =========================================================

st.header(T["data"])

df = pd.DataFrame(default_data)

edited_df = st.data_editor(
    df,
    num_rows="dynamic",
    use_container_width=True
)

# =========================================================
# CLEAN DATA
# =========================================================

numeric_columns = [
    c for c in edited_df.columns
    if c != "Alternative"
]

for col in numeric_columns:

    edited_df[col] = pd.to_numeric(
        edited_df[col],
        errors="coerce"
    )

edited_df[numeric_columns] = (
    edited_df[numeric_columns]
    .fillna(0)
    .clip(0, 1)
)

# =========================================================
# NEUTROSOPHIC ENTROPY
# =========================================================

if (
    "Truth (T)" in edited_df.columns
    and "Indeterminacy (I)" in edited_df.columns
    and "Falsity (F)" in edited_df.columns
):

    edited_df["Entropy (E)"] = (
        edited_df["Indeterminacy (I)"]
        + edited_df["Falsity (F)"]
    ) / 2

    edited_df["Final Score"] = (
        edited_df["Truth (T)"]
        * (1 - edited_df["Entropy (E)"])
    )

else:

    # Generic custom mode

    criteria = [
        c for c in edited_df.columns
        if c != "Alternative"
    ]

    normalized = pd.DataFrame()

    for col in criteria:

        min_value = edited_df[col].min()
        max_value = edited_df[col].max()

        if max_value != min_value:

            normalized[col] = (
                edited_df[col] - min_value
            ) / (max_value - min_value)

        else:

            normalized[col] = 1

    edited_df["Final Score"] = normalized.mean(axis=1)

    edited_df["Entropy (E)"] = (
        1 - edited_df["Final Score"]
    )

# =========================================================
# ROUNDING
# =========================================================

edited_df["Final Score"] = (
    edited_df["Final Score"]
    .clip(0, 1)
    .round(4)
)

edited_df["Entropy (E)"] = (
    edited_df["Entropy (E)"]
    .clip(0, 1)
    .round(4)
)

# =========================================================
# RANK
# =========================================================

edited_df["Rank"] = (
    edited_df["Final Score"]
    .rank(
        ascending=False,
        method="min"
    )
    .astype(int)
)

results_df = (
    edited_df
    .sort_values(
        by="Final Score",
        ascending=False
    )
    .reset_index(drop=True)
)

# =========================================================
# RESULTS
# =========================================================

st.header(T["results"])

st.dataframe(
    results_df,
    use_container_width=True
)

# =========================================================
# BEST RESULT
# =========================================================

best = results_df.iloc[0]

best_name = best["Alternative"]
best_score = best["Final Score"]

st.success(
    (
        f"🏆 Best alternative: **{best_name}** "
        f"with a final score of **{best_score:.4f}**"
        if not arabic
        else
        f"🏆 أفضل بديل هو: **{best_name}** "
        f"بدرجة نهائية **{best_score:.4f}**"
    )
)

# =========================================================
# METRICS
# =========================================================

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        T["alternatives"],
        len(results_df)
    )

with c2:
    st.metric(
        T["criteria"],
        len(numeric_columns)
    )

with c3:
    st.metric(
        T["score"],
        f"{best_score:.4f}"
    )

# =========================================================
# SCIENTIFIC ANALYSIS
# =========================================================

st.header(T["analysis"])

second_score = (
    results_df.iloc[1]["Final Score"]
    if len(results_df) > 1
    else 0
)

difference = best_score - second_score

if best_score >= 0.80:

    level_en = "very strong"
    level_ar = "قوية جدًا"

elif best_score >= 0.60:

    level_en = "strong"
    level_ar = "قوية"

elif best_score >= 0.40:

    level_en = "moderate"
    level_ar = "متوسطة"

else:

    level_en = "relatively weak"
    level_ar = "منخفضة نسبيًا"

if not arabic:

    analysis_text = f"""
    **Decision Analysis**

    The highest-ranked alternative is **{best_name}**,
    with a final score of **{best_score:.4f}**.

    The obtained score indicates a **{level_en}**
    decision performance under the current input values.

    The difference between the first and second ranked
    alternatives is approximately **{difference:.4f}**.

    A larger difference indicates clearer separation between
    the leading alternative and the next alternative.

    The ranking should be interpreted according to the
    selected criteria and input values.
    """

else:

    analysis_text = f"""
    **التحليل العلمي للنتائج**

    البديل الحاصل على المرتبة الأولى هو **{best_name}**
    بدرجة نهائية مقدارها **{best_score:.4f}**.

    وتشير هذه الدرجة إلى أن مستوى أداء القرار هو
    **{level_ar}** وفقًا للقيم المدخلة حاليًا.

    يبلغ الفرق بين البديل الأول والثاني تقريبًا
    **{difference:.4f}**.

    وكلما زاد الفرق بين المرتبتين الأولى والثانية،
    كان التمييز بين البديل الأفضل والبديل التالي أوضح.

    يجب تفسير النتائج في ضوء المعايير والقيم المدخلة
    في نموذج اتخاذ القرار.
    """

st.info(analysis_text)

# =========================================================
# CHART 1 - RANKING
# =========================================================

st.header(T["charts"])

st.subheader(
    "📊 Ranking / ترتيب البدائل"
)

chart_df = results_df[
    ["Alternative", "Final Score"]
].set_index("Alternative")

st.bar_chart(chart_df)

# =========================================================
# CHART 2 - ENTROPY
# =========================================================

st.subheader(
    "📈 Entropy / تحليل عدم اليقين"
)

entropy_df = results_df[
    ["Alternative", "Entropy (E)"]
].set_index("Alternative")

st.bar_chart(entropy_df)

# =========================================================
# CHART 3 - T I F
# =========================================================

if (
    "Truth (T)" in results_df.columns
    and "Indeterminacy (I)" in results_df.columns
    and "Falsity (F)" in results_df.columns
):

    st.subheader(
        "🔬 Neutrosophic Components / المكونات النيوتروسوفية"
    )

    tif_df = results_df[
        [
            "Alternative",
            "Truth (T)",
            "Indeterminacy (I)",
            "Falsity (F)"
        ]
    ].set_index("Alternative")

    st.line_chart(tif_df)

# =========================================================
# DOWNLOAD CSV
# =========================================================

st.header(T["export"])

csv_data = results_df.to_csv(
    index=False
).encode("utf-8-sig")

st.download_button(
    label=T["download_csv"],
    data=csv_data,
    file_name="MadiNeutro_Results.csv",
    mime="text/csv"
)

# =========================================================
# EXCEL
# =========================================================

excel_buffer = io.BytesIO()

with pd.ExcelWriter(
    excel_buffer,
    engine="openpyxl"
) as writer:

    results_df.to_excel(
        writer,
        index=False,
        sheet_name="Decision Results"
    )

excel_buffer.seek(0)

st.download_button(
    label=T["download_excel"],
    data=excel_buffer,
    file_name="MadiNeutro_Results.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# =========================================================
# PDF GENERATION
# =========================================================

def create_pdf(results, best_name, best_score, difference, arabic):

    buffer = io.BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=35,
        leftMargin=35,
        topMargin=35,
        bottomMargin=35
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "Title",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=20,
        spaceAfter=20
    )

    normal_style = ParagraphStyle(
        "Normal",
        parent=styles["BodyText"],
        fontSize=10,
        leading=15
    )

    story = []

    story.append(
        Paragraph(
            "MadiNeutro AI",
            title_style
        )
    )

    story.append(
        Paragraph(
            "Neutrosophic Entropy-Based "
            "Multi-Criteria Decision Making",
            normal_style
        )
    )

    story.append(Spacer(1, 15))

    if arabic:

        story.append(
            Paragraph(
                f"<b>أفضل بديل:</b> {best_name}",
                normal_style
            )
        )

        story.append(
            Paragraph(
                f"<b>الدرجة النهائية:</b> {best_score:.4f}",
                normal_style
            )
        )

        story.append(
            Paragraph(
                f"<b>الفرق عن البديل الثاني:</b> {difference:.4f}",
                normal_style
            )
        )

    else:

        story.append(
            Paragraph(
                f"<b>Best Alternative:</b> {best_name}",
                normal_style
            )
        )

        story.append(
            Paragraph(
                f"<b>Final Score:</b> {best_score:.4f}",
                normal_style
            )
        )

        story.append(
            Paragraph(
                f"<b>Difference from second rank:</b> "
                f"{difference:.4f}",
                normal_style
            )
        )

    story.append(Spacer(1, 20))

    table_data = [
        [
            "Rank",
            "Alternative",
            "Entropy",
            "Final Score"
        ]
    ]

    for _, row in results.iterrows():

        table_data.append(
            [
                str(row["Rank"]),
                str(row["Alternative"]),
                f'{row["Entropy (E)"]:.4f}',
                f'{row["Final Score"]:.4f}'
            ]
        )

    table = Table(
        table_data,
        repeatRows=1
    )

    table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.HexColor("#1F4E78")
            ),
            (
                "TEXTCOLOR",
                (0, 0),
                (-1, 0),
                colors.white
            ),
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.grey
            ),
            (
                "ALIGN",
                (0, 0),
                (-1, -1),
                "CENTER"
            ),
            (
                "FONTNAME",
                (0, 0),
                (-1, 0),
                "Helvetica-Bold"
            ),
            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, 0),
                8
            )
        ])
    )

    story.append(table)

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            (
                "This report was generated automatically by "
                "MadiNeutro AI."
                if not arabic
                else
                "تم إنشاء هذا التقرير تلقائيًا بواسطة "
                "منصة MadiNeutro AI."
            ),
            normal_style
        )
    )

    doc.build(story)

    buffer.seek(0)

    return buffer


pdf_file = create_pdf(
    results_df,
    best_name,
    best_score,
    difference,
    arabic
)

st.download_button(
    label=T["download_pdf"],
    data=pdf_file,
    file_name="MadiNeutro_Report.pdf",
    mime="application/pdf"
)

# =========================================================
# ABOUT
# =========================================================

st.divider()

st.header(T["about"])

if arabic:

    st.write(
        """
        **MadiNeutro AI** هي منصة لدعم اتخاذ القرار متعدد
        المعايير، صُممت لتقييم البدائل باستخدام المنطق
        النيوتروسوفي وتحليل Entropy.

        تتيح المنصة إدخال البيانات، حساب الدرجات،
        ترتيب البدائل، تحليل النتائج، عرض الرسوم البيانية،
        وتصدير النتائج بصيغ مختلفة.
        """
    )

else:

    st.write(
        """
        **MadiNeutro AI** is a research-oriented Multi-Criteria
        Decision Making platform designed to evaluate alternatives
        using Neutrosophic Logic and Entropy-based analysis.

        The platform supports data input, scoring, ranking,
        result interpretation, visualization, and report export.
        """
    )

st.caption(
    "Developed for scientific and research applications."
)
st.markdown("""
<style>

.dev-card {
    max-width: 760px;
    margin: 40px auto;
    padding: 40px 30px;
    border-radius: 28px;
    background: linear-gradient(
        135deg,
        #0f172a 0%,
        #172554 45%,
        #1d4ed8 75%,
        #2563eb 100%
    );
    color: white;
    box-shadow: 0 15px 40px rgba(0,0,0,0.35);
    text-align: center;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    overflow: hidden;
}

.avatar {
    width: 105px;
    height: 105px;
    margin: 0 auto 20px auto;
    border-radius: 50%;
    background: rgba(255,255,255,0.95);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 52px;
    box-shadow: 0 6px 20px rgba(0,0,0,0.25);
}

.name-ar {
    font-size: 31px;
    font-weight: 800;
    margin-bottom: 3px;
}

.name-en {
    font-size: 19px;
    font-weight: 500;
    opacity: 0.9;
    margin-bottom: 10px;
}

.title {
    font-size: 16px;
    opacity: 0.9;
    margin-bottom: 20px;
}

.badge {
    display: inline-block;
    padding: 9px 20px;
    background: white;
    color: #1d4ed8;
    border-radius: 40px;
    font-weight: 700;
    margin-bottom: 25px;
    box-shadow: 0 5px 15px rgba(0,0,0,0.15);
}

.project-description {
    background: rgba(255,255,255,0.10);
    padding: 20px;
    border-radius: 18px;
    margin-bottom: 25px;
    line-height: 1.6;
    backdrop-filter: blur(6px);
}

.project-title {
    font-size: 21px;
    font-weight: 800;
    margin-bottom: 8px;
}

.project-subtitle {
    font-size: 14px;
    opacity: 0.9;
}

.tech-container {
    margin: 20px 0;
}

.tech {
    display: inline-block;
    background: rgba(255,255,255,0.15);
    padding: 7px 13px;
    border-radius: 30px;
    margin: 4px;
    font-size: 13px;
    border: 1px solid rgba(255,255,255,0.15);
}

.grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 15px;
    margin-top: 25px;
}

.box {
    background: rgba(255,255,255,0.12);
    padding: 20px 12px;
    border-radius: 17px;
    backdrop-filter: blur(6px);
    transition: transform 0.3s ease, background 0.3s ease;
}

.box:hover {
    transform: translateY(-5px);
    background: rgba(255,255,255,0.20);
}

.box-icon {
    font-size: 27px;
    margin-bottom: 6px;
}

.box-title {
    font-weight: 700;
    font-size: 15px;
}

.box-text {
    font-size: 13px;
    opacity: 0.85;
    margin-top: 4px;
}

.links {
    margin-top: 30px;
}

.link-button {
    display: inline-block;
    padding: 10px 18px;
    margin: 5px;
    border-radius: 30px;
    background: rgba(255,255,255,0.13);
    color: white !important;
    text-decoration: none !important;
    font-weight: 600;
    border: 1px solid rgba(255,255,255,0.20);
    transition: transform 0.25s ease, background 0.25s ease;
}

.link-button:hover {
    transform: translateY(-3px);
    background: rgba(255,255,255,0.25);
}

.footer {
    margin-top: 28px;
    padding-top: 20px;
    border-top: 1px solid rgba(255,255,255,0.15);
    font-size: 13px;
    opacity: 0.85;
    line-height: 1.7;
}

@media (max-width: 600px) {

    .dev-card {
        margin: 20px 10px;
        padding: 30px 18px;
    }

    .name-ar {
        font-size: 26px;
    }

    .name-en {
        font-size: 17px;
    }

    .grid {
        grid-template-columns: 1fr;
    }

    .project-title {
        font-size: 19px;
    }
}

</style>


<div class="dev-card">

    <div class="avatar">
        👩🏻‍💻
    </div>

    <div class="name-ar">
        مديحة عبدالله عوبل
    </div>

    <div class="name-en">
        Madiha Abdullah Aobel
    </div>

    <div class="title">
        Founder • Developer • Mathematics Researcher
    </div>

    <div class="badge">
        🚀 Creator of MadiNeutro AI
    </div>

    <div class="project-description">

        <div class="project-title">
            🤖 MadiNeutro AI
        </div>

        <div class="project-subtitle">
            AI-Powered Multi-Criteria Decision Making Platform
            <br>
            Based on Neutrosophic Logic & Information Entropy
        </div>

    </div>

    <div class="tech-container">

        <span class="tech">
            🧠 Neutrosophic Logic
        </span>

        <span class="tech">
            📊 MCDM
        </span>

        <span class="tech">
            🔢 Information Entropy
        </span>

        <span class="tech">
            🤖 Artificial Intelligence
        </span>

        <span class="tech">
            📈 Data Analysis
        </span>

    </div>

    <div class="grid">

        <div class="box">
            <div class="box-icon">🤖</div>
            <div class="box-title">MadiNeutro AI</div>
            <div class="box-text">Version 1.0.0</div>
        </div>

        <div class="box">
            <div class="box-icon">🏛️</div>
            <div class="box-title">University of Aden</div>
            <div class="box-text">Faculty of Science</div>
        </div>

        <div class="box">
            <div class="box-icon">🇾🇪</div>
            <div class="box-title">Yemen</div>
            <div class="box-text">Republic of Yemen</div>
        </div>

        <div class="box">
            <div class="box-icon">📅</div>
            <div class="box-title">August 2026</div>
            <div class="box-text">Initial Release</div>
        </div>

    </div>

    <div class="links">

        <a
            class="link-button"
            href="mailto:madialmassady@gmail.com">
            📧 Email
        </a>

        <a
            class="link-button"
            href="https://github.com/YOUR_USERNAME"
            target="_blank">
            🌐 GitHub
        </a>

        <a
            class="link-button"
            href="https://scholar.google.com/"
            target="_blank">
            🎓 Google Scholar
        </a>

    </div>

    <div class="footer">

        Developed & Designed by
        <b>Madiha Abdullah Aobel</b>

        <br>

        Mathematics Researcher • AI & Decision Science

        <br><br>

        © 2026 MadiNeutro AI
        • Version 1.0.0

    </div>

</div>

""", unsafe_allow_html=True)
