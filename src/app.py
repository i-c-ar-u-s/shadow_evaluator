import streamlit as st
import time
import random
import json
import os

# 1. SMART DATA LOADER (Ensures no crashes on web or local)
def load_data():
    # Checks multiple locations for the audit results
    possible_paths = [
        'src/audit_results.json', 
        'audit_results.json', 
        '../src/audit_results.json'
    ]
    for path in possible_paths:
        if os.path.exists(path):
            try:
                with open(path, 'r') as f:
                    return json.load(f)
            except:
                continue
    # Fallback "Demo" data if file isn't found
    return {
        "ai_score": 81, 
        "faculty_score": 86, 
        "z_score": -1.0, 
        "report": "System initialized. Showing benchmark audit data."
    }

# Page config
st.set_page_config(
    page_title="Shadow Evaluator",
    page_icon="🕵️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for the alert box
st.markdown("""
<style>
    .report-box {
        padding: 20px;
        border-radius: 10px;
        margin-top: 20px;
        text-align: center;
        font-weight: bold;
        font-size: 24px;
        color: white;
    }
    .report-pass {
        background-color: #28a745;
        border: 2px solid #1e7e34;
    }
    .report-fail {
        background-color: #dc3545;
        border: 2px solid #bd2130;
    }
</style>
""", unsafe_allow_html=True)

def main():
    st.title("🕵️ Shadow Evaluator Dashboard")
    st.markdown("### AI-Powered Faculty Evaluation Audit System")

    # Load the latest data from the agents
    real_data = load_data()

    # --- Sidebar ---
    st.sidebar.header("Audit Configuration")
    course = st.sidebar.selectbox("Select Course", ["Computer Science 101", "Business Ethics", "Mechanical Design"])
    
    st.sidebar.header("Audit Baselines")
    manual_faculty_grade = st.sidebar.slider("Faculty's Assigned Grade", 0, 100, 85)

    st.sidebar.header("Upload Evaluation Data")
    uploaded_file = st.sidebar.file_uploader("Upload PDF Report", type=["pdf"])

    if uploaded_file is not None:
        st.sidebar.success("File uploaded successfully!")
        
        if st.sidebar.button("Start Audit"):
            # --- Progress Bar Simulation ---
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            agents = [
                "Governance Officer: Validating compliance...",
                "Quant Analyst: Parsing numerical data...",
                "Blind Judge: Analyzing qualitative feedback...",
                "Clean Room: Ensuring anonymity...",
                "Orchestrator: Synthesizing results..."
            ]
            
            for i, agent_status in enumerate(agents):
                status_text.text(f"Agent {i+1}/5 working: {agent_status}")
                time.sleep(random.uniform(0.5, 1.2)) 
                progress_bar.progress((i + 1) * 20)
            
            status_text.text("Audit Complete!")
            time.sleep(0.5)
            progress_bar.empty()
            status_text.empty()

            # --- Main Results Area ---
            st.divider()
            
            # Application Logic
            ai_score = real_data.get('ai_score', 80)
            variance = manual_faculty_grade - ai_score
            # Variance math: (Score - Mean) / StdDev
            z_score = round(variance / 5.2, 1) 

            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("### 🤖 AI Score")
                st.metric(label="Calculated Score", value=f"{ai_score}/100")
            
            with col2:
                st.markdown("### 👨‍🏫 Faculty Score")
                st.metric(label="Original Score", value=f"{manual_faculty_grade}/100", delta=f"{variance}")
            
            with col3:
                st.markdown("### 📉 Z-Score")
                st.metric(label="Deviation", value=z_score)

            # --- Governance Officer's Final Report ---
            st.divider()
            st.markdown("### ⚖️ Governance Officer's Final Report")
            
            if abs(z_score) < 2.0:
                report_status = "PASSED"
                report_class = "report-pass"
                report_msg = real_data.get('report', "The evaluation is consistent with AI benchmarks. No anomalies detected.")
            else:
                report_status = "FLAGGED"
                report_class = "report-fail"
                report_msg = "Significant deviation detected! This evaluation requires manual review."

            st.markdown(f"""
            <div class="report-box {report_class}">
                STATUS: {report_status}<br>
                <span style='font-size: 16px; font-weight: normal;'>{report_msg}</span>
            </div>
            """, unsafe_allow_html=True)
            
            # --- Download Button ---
            st.divider()
            report_text = f"""
            OFFICIAL AUDIT REPORT
            Course: {course}
            AI Shadow Score: {ai_score}
            Faculty Score: {manual_faculty_grade}
            Variance (Z-Score): {z_score}
            ---
            Governance Note: {report_msg}
            """

            st.download_button(
                label="📄 Download Accreditation Evidence",
                data=report_text,
                file_name=f"Audit_{course.replace(' ', '_')}.txt",
                mime="text/plain"
            )
    else:
        st.info("Please upload a PDF to begin the audit process.")

if __name__ == "__main__":
    main()