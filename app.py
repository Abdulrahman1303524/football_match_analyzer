import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import io

# ==========================================
# 1. إعدادات الصفحة والتنسيق العام
# ==========================================
st.set_page_config(page_title="Pro Football Analyzer", layout="wide", page_icon="⚽")
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

st.title("⚽ Pro Football Match Analyzer")
st.write("Enter match statistics for two teams to get a professional analysis, AI prediction, and downloadable report.")

# ==========================================
# 2. دالة جمع البيانات (مع إضافة الشعارات)
# ==========================================
# قاموس للشعارات (يمكنك إضافة المزيد من الفرق هنا لاحقاً)
LOGO_DICT = {
    "Real Madrid": "https://upload.wikimedia.org/wikipedia/en/thumb/5/56/Real_Madrid_CF.svg/150px-Real_Madrid_CF.svg.png",
    "FC Barcelona": "https://upload.wikimedia.org/wikipedia/en/thumb/4/47/FC_Barcelona_%28crest%29.svg/150px-FC_Barcelona_%28crest%29.svg.png",
    "Egypt": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/fe/Egypt_national_football_team_logo.svg/150px-Egypt_national_football_team_logo.svg.png",
    "Greece": "https://upload.wikimedia.org/wikipedia/en/thumb/4/4e/Greece_national_football_team_logo.svg/150px-Greece_national_football_team_logo.svg.png"
}

def team_inputs(label, key, emoji, default_name):
    st.subheader(f"{emoji} {label}")
    name = st.text_input("Team name", value=default_name, key=f"name_{key}")
    
    # عرض الشعار ديناميكياً إذا كان الاسم موجوداً في القاموس
    if name.strip().title() in LOGO_DICT:
      st.image(LOGO_DICT[name.strip().title()], width=100)  
    else:
        st.write("🔍 *(Logo not found for this team)*")
        
    c1, c2 = st.columns(2)
    with c1:
        goals = st.number_input("Goals", min_value=0, key=f"goals_{key}")
        shots = st.number_input("Total shots", min_value=0, key=f"shots_{key}")
        on_target = st.number_input("Shots on target", min_value=0, key=f"target_{key}")
    with c2:
        possession = st.number_input("Possession (%)", min_value=0, max_value=100, key=f"pos_{key}")
        passes = st.number_input("Completed passes", min_value=0, key=f"pass_{key}")
        attempted = st.number_input("Attempted passes", min_value=0, key=f"att_{key}")
        
    return {
        "Team": name.strip() or default_name,
        "Goals": int(goals),
        "Shots": int(shots),
        "Shots on target": int(on_target),
        "Possession (%)": int(possession),
        "Completed passes": int(passes),
        "Attempted passes": int(attempted),
    }

left, right = st.columns(2)
with left:
    team_a = team_inputs("Team A", "a", "🔴", "Real Madrid")
with right:
    team_b = team_inputs("Team B", "b", "🔵", "FC Barcelona")

# ==========================================
# 3. قسم التحليل والنتائج
# ==========================================
st.markdown("---")
st.header("📊 Match Analysis Results")

data = pd.DataFrame([team_a, team_b])
data.set_index("Team", inplace=True)

st.subheader("Statistics Comparison")
st.dataframe(data, use_container_width=True)

data["Shot Accuracy (%)"] = (data["Shots on target"] / data["Shots"].replace(0, 1)) * 100
data["Pass Accuracy (%)"] = (data["Completed passes"] / data["Attempted passes"].replace(0, 1)) * 100

st.subheader("Advanced Metrics")
st.dataframe(data[["Shot Accuracy (%)", "Pass Accuracy (%)"]].round(1), use_container_width=True)

# ==========================================
# 4. الرسوم البيانية بألوان الفرق
# ==========================================
st.subheader("📈 Visual Analysis")

def plot_bar_comparison(metric1, metric2, title, ylabel):
    fig, ax = plt.subplots(figsize=(6, 4))
    teams = data.index.tolist()
    x = np.arange(len(teams))
    width = 0.35
    
    # ألوان ديناميكية (الفريق الأول أحمر، الثاني أزرق)
    rects1 = ax.bar(x - width/2, data[metric1], width, label=metric1, color='#e74c3c')
    rects2 = ax.bar(x + width/2, data[metric2], width, label=metric2, color='#3498db')
    
    ax.set_ylabel(ylabel)
    ax.set_title(title, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(teams)
    ax.legend()
    ax.bar_label(rects1, padding=3)
    ax.bar_label(rects2, padding=3)
    fig.tight_layout()
    st.pyplot(fig)

col1, col2 = st.columns(2)
with col1:
    plot_bar_comparison('Goals', 'Shots', 'Goals vs Total Shots', 'Count')
with col2:
    plot_bar_comparison('Completed passes', 'Attempted passes', 'Passes Comparison', 'Count')

# ==========================================
# 5. الذكاء الاصطناعي والتحليل النهائي
# ==========================================
st.markdown("---")
st.header("🤖 AI Match Prediction")

score_a = (team_a["Goals"] * 3) + (team_a["Shots on target"] * 2) + team_a["Possession (%)"] + (data.loc[team_a["Team"], "Pass Accuracy (%)"] * 0.5)
score_b = (team_b["Goals"] * 3) + (team_b["Shots on target"] * 2) + team_b["Possession (%)"] + (data.loc[team_b["Team"], "Pass Accuracy (%)"] * 0.5)

if score_a > score_b:
    winner = team_a["Team"]
    st.success(f"🏆 **AI Predicts:** {winner} was the better team overall based on performance metrics!")
elif score_b > score_a:
    winner = team_b["Team"]
    st.success(f"🏆 **AI Predicts:** {winner} was the better team overall based on performance metrics!")
else:
    st.info("🤝 **AI Predicts:** It's a very balanced match! Both teams performed equally.")

st.subheader("📝 Final Match Verdict")
if team_a["Goals"] > team_b["Goals"]:
    st.success(f"🥇 **Result:** {team_a['Team']} wins the match!")
elif team_b["Goals"] > team_a["Goals"]:
    st.success(f"🥇 **Result:** {team_b['Team']} wins the match!")
else:
    st.info("🤝 **Result:** It's a draw!")

# ==========================================
# 6. ميزة تحميل التقرير (Excel)
# ==========================================
st.markdown("---")
st.subheader("📥 Download Match Report")

# تحويل البيانات إلى ملف Excel في الذاكرة
def convert_df_to_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Match_Stats')
    processed_data = output.getvalue()
    return processed_data

excel_data = convert_df_to_excel(data)

st.download_button(
    label="📊 Download Data as Excel",
    data=excel_data,
    file_name="match_analysis.xlsx",
    mime="application/vnd.ms-excel"
)
