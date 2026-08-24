import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="MadiNeutro AI", layout="wide", page_icon="🤖"
)

st.title("🤖 MadiNeutro AI: Multi-Criteria Decision Making Platform")
st.write(
    "نظام اتخاذ القرار الشامل القائم على المنطق النيوتروسوفي ومعايير Entropy"
)

# شريط إعدادات اسم القطاع
st.sidebar.header("⚙️ إعدادات النظام")
domain = st.sidebar.selectbox(
    "اختر مجال التطبيق:",
    [
        "تقييم المحاصيل الزراعية",
        "تقييم الشركات والمشاريع",
        "اختيار أفضل الكوادر / الجامعات",
        "مخصص (Custom)",
    ],
)

# بيانات افتراضية قابلة للتعديل
if domain == "تقييم الشركات والمشاريع":
    default_data = {
        "Alternative (البديل)": [
            "Company A",
            "Company B",
            "Company C",
            "Company D",
        ],
        "Performance (T)": [0.85, 0.70, 0.90, 0.65],
        "Indeterminacy (I)": [0.08, 0.15, 0.05, 0.10],
        "Falsity (F)": [0.07, 0.15, 0.05, 0.25],
    }
elif domain == "اختيار أفضل الكوادر / الجامعات":
    default_data = {
        "Alternative (البديل)": ["University A", "University B", "University C"],
        "Quality (T)": [0.88, 0.80, 0.92],
        "Indeterminacy (I)": [0.06, 0.10, 0.04],
        "Falsity (F)": [0.06, 0.10, 0.04],
    }
else:
    default_data = {
        "Alternative (البديل)": [
            "Tomato",
            "Papaya",
            "Banana",
            "Millet",
            "Sesame",
            "Cotton",
        ],
        "Truth (T)": [0.90, 0.85, 0.80, 0.75, 0.70, 0.68],
        "Indeterminacy (I)": [0.05, 0.08, 0.10, 0.10, 0.10, 0.12],
        "Falsity (F)": [0.10, 0.07, 0.15, 0.15, 0.20, 0.18],
    }

st.header("1️⃣ جدول البيانات والمدخلات (أدخل/عدّل أي قيم)")
df = pd.DataFrame(default_data)
edited_df = st.data_editor(df, num_rows="dynamic")

# الحسابات النيوتروسوفية
edited_df["Entropy (E)"] = (
    edited_df["Indeterminacy (I)"] + edited_df["Falsity (F)"]
)

# تحديد عمود Truth وحساب الوزن النهائي
t_col = [c for c in edited_df.columns if "(T)" in c][0]
edited_df["Final Score"] = (
    edited_df[t_col] * (1 - edited_df["Entropy (E)"])
).round(4)
edited_df["Rank"] = (
    edited_df["Final Score"].rank(ascending=False, method="min").astype(int)
)

results_df = edited_df.sort_values(by="Rank")

st.header("2️⃣ الترتيب النهائي والتحليل")
st.dataframe(results_df, use_container_width=True)

st.header("3️⃣ الرسم البياني المقارن")
st.bar_chart(results_df.set_index("Alternative (البديل)")["Final Score"])

top_item = results_df.iloc[0]["Alternative (البديل)"]
st.success(f"🏆 الخيار الأفضل تقييماً بناءً على الخوارزمية هو: **{top_item}**")
