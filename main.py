import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px  # NEW: For interactive charts

st.set_page_config(page_title="Grading System", page_icon="🎓", layout="wide")

st.title("🎓 Interactive Relative Grading System")
st.markdown("Upload your class scores to automatically generate a bell-curve grading distribution.")

# --- SIDEBAR: Adjustable Curve Thresholds ---
st.sidebar.header("🎛️ Adjust Bell Curve")
st.sidebar.markdown("Define the Z-score required for each grade:")
a_plus_thresh = st.sidebar.slider("A+ Threshold", 1.0, 2.5, 1.3, 0.1)
a_thresh = st.sidebar.slider("A Threshold", 0.5, 1.5, 0.8, 0.1)
b_plus_thresh = st.sidebar.slider("B+ Threshold", 0.0, 1.0, 0.4, 0.1)
b_thresh = st.sidebar.slider("B Threshold", -0.5, 0.5, 0.0, 0.1)
c_thresh = st.sidebar.slider("C Threshold", -1.0, 0.0, -0.5, 0.1)
d_thresh = st.sidebar.slider("D Threshold", -2.0, -0.5, -1.0, 0.1)

uploaded_file = st.file_uploader("📂 Upload CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file, header=1)

    with st.expander("👀 Preview Uploaded Data"):
        st.dataframe(df, use_container_width=True)

    st.divider()
    st.write("### ⚙️ Column Selection")
    
    col1, col2 = st.columns(2)
    with col1:
        id_column = st.selectbox("👤 1. Student ID/Name Column:", df.columns)
    with col2:
        mark_columns = [col for col in df.columns if col != id_column]
        score_column = st.selectbox("📊 2. Marks Column to Grade:", mark_columns)

    max_value = st.number_input("💯 Enter maximum possible marks", min_value=1.0, value=100.0)

    # Calculate Button
    if st.button("🚀 Perform Relative Grading", type="primary", use_container_width=True):
        try:
            marks = df[score_column].astype(float)
        except ValueError:
            st.error(f"❌ '{score_column}' contains text. Please select numbers.")
            st.stop()

        normalized_marks = (marks / marks.max()) * max_value
        mean = np.mean(normalized_marks)
        std = np.std(normalized_marks)
        
        if std == 0:
            st.error("🚨 Standard deviation is zero. Everyone has the exact same score!")
        else:
            z_scores = (normalized_marks - mean) / std

            # Using the dynamic thresholds from the sidebar
            def assign_grade(z):
                if z >= a_plus_thresh: return "A+"
                elif z >= a_thresh: return "A"
                elif z >= b_plus_thresh: return "B+"
                elif z >= b_thresh: return "B"
                elif z >= c_thresh: return "C"
                elif z >= d_thresh: return "D"
                else: return "F"

            grades = z_scores.apply(assign_grade)

            result_df = pd.DataFrame({
                "Student ID": df[id_column],
                "Original Marks": df[score_column],
                "Normalized Marks": normalized_marks.round(2),
                "Z-Score": z_scores.round(2),
                "Grade": grades
            })

            # Save the result to Streamlit's Session State!
            st.session_state['graded_data'] = result_df
            st.session_state['mean'] = mean

# --- DISPLAY RESULTS (Only runs if data is saved in session state) ---
if 'graded_data' in st.session_state:
    st.divider()
    st.success("✅ Grading Completed Successfully!")
    
    result_df = st.session_state['graded_data']
    mean = st.session_state['mean']

    # Colorize DataFrame
    def color_grades(val):
        colors = {'A+': '#198754', 'A': '#20c997', 'B+': '#0dcaf0', 
                  'B': '#0d6efd', 'C': '#ffc107', 'D': '#fd7e14', 'F': '#dc3545'}
        color = colors.get(val, '')
        if color: return f'background-color: {color}; color: {"black" if val in ["C", "B+"] else "white"}; font-weight: bold'
        return ''
    
    try:
        styled_df = result_df.style.map(color_grades, subset=['Grade'])
    except AttributeError:
        styled_df = result_df.style.applymap(color_grades, subset=['Grade'])
        
    st.dataframe(styled_df, use_container_width=True)

    # --- PLOTLY INTERACTIVE CHARTS ---
    st.write("### 📈 Visual Analytics")
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        # Interactive Histogram
        fig1 = px.histogram(
            result_df, x="Normalized Marks", nbins=15,
            title="Marks Distribution", color_discrete_sequence=['#6f42c1']
        )
        fig1.add_vline(x=mean, line_dash="dash", line_color="#ffc107", annotation_text="Class Average")
        fig1.update_layout(showlegend=False)
        st.plotly_chart(fig1, use_container_width=True)

    with chart_col2:
        # Interactive Bar Chart
        grade_order = ["A+", "A", "B+", "B", "C", "D", "F"]
        grade_counts = result_df["Grade"].value_counts().reindex(grade_order, fill_value=0).reset_index()
        grade_counts.columns = ['Grade', 'Count']
        
        color_map = {'A+': '#198754', 'A': '#20c997', 'B+': '#0dcaf0', 'B': '#0d6efd', 
                     'C': '#ffc107', 'D': '#fd7e14', 'F': '#dc3545'}

        fig2 = px.bar(
            grade_counts, x='Grade', y='Count', color='Grade',
            title="Grade Distribution", text_auto=True,
            color_discrete_map=color_map, category_orders={"Grade": grade_order}
        )
        fig2.update_layout(showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)

    st.divider()
    
    # Download Button (Now safely outside the main calculation button)
    csv = result_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Final Graded CSV",
        data=csv,
        file_name="final_grades.csv",
        mime="text/csv",
        type="primary"
    )