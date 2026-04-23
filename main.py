import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.title("Relative Grading System")

uploaded_file = st.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file:
    # Read file
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file, header=1)

    st.write("### Preview of Data")
    st.dataframe(df)

    st.write("---")
    st.write("### Column Selection")
    
    # 1. Select the ID column (This is safely tucked away from the math)
    id_column = st.selectbox(
        "1. Select the Student ID or Name column (for labeling only):", 
        df.columns
    )
    
    # 2. Select the Marks column (We hide the ID column from this list so it can't be picked by mistake)
    mark_columns = [col for col in df.columns if col != id_column]
    score_column = st.selectbox(
        "2. Select the Marks column to be graded:", 
        mark_columns
    )

    max_value = st.number_input("Enter maximum possible marks for the selected column", min_value=1.0, value=100.0)

    if st.button("Perform Relative Grading"):
        
        # We wrap this in a try-except block just in case a text column is selected for marks
        try:
            marks = df[score_column].astype(float)
        except ValueError:
            st.error(f"The column '{score_column}' contains text. Please select a column with numerical scores.")
            st.stop()

        # Normalize marks based on the user-defined max_value
        normalized_marks = (marks / marks.max()) * max_value

        mean = np.mean(normalized_marks)
        std = np.std(normalized_marks)
        
        if std == 0:
            st.error("Standard deviation is zero. Cannot perform relative grading. (Did everyone get the exact same score?)")
        else:
            z_scores = (normalized_marks - mean) / std

            def assign_grade(z):
                if z >= 1.2: return "A+"
                elif z >= 0.8: return "A"
                elif z >= 0.4: return "B+"
                elif z >= 0: return "B"
                elif z >= -0.5: return "C"
                elif z >= -1.0: return "D"
                else: return "F"

            grades = z_scores.apply(assign_grade)

            # -------------------------------
            # Create a Clean Output DataFrame
            # -------------------------------
            # This directly combines the ID column we saved earlier with the new math results
            result_df = pd.DataFrame({
                "Student ID": df[id_column],
                "Original Marks": df[score_column],
                "Normalized Marks": normalized_marks.round(2), # Rounding for cleaner display
                "Z-Score": z_scores.round(2),
                "Grade": grades
            })

            st.write("### Final Graded Data")
            st.dataframe(result_df)

            # -------------------------------
            # Visualization
            # -------------------------------
            st.write("### Distribution Plot")

            fig, ax = plt.subplots()
            ax.hist(normalized_marks, bins=10, edgecolor='black', color='skyblue')
            ax.axvline(mean, color='red', linestyle='dashed', linewidth=2, label='Mean')
            ax.set_title(f"{score_column} Distribution")
            ax.set_xlabel("Normalized Marks")
            ax.legend()
            st.pyplot(fig)

            st.write("### Grade Distribution")

            grade_order = ["A+", "A", "B+", "B", "C", "D", "F"]
            grade_counts = result_df["Grade"].value_counts().reindex(grade_order, fill_value=0)

            fig2, ax2 = plt.subplots()
            ax2.bar(grade_counts.index, grade_counts.values, color='coral', edgecolor='black')
            ax2.set_title("Grade Distribution")
            ax2.set_xlabel("Grades")
            ax2.set_ylabel("Number of Students")
            st.pyplot(fig2)

            # -------------------------------
            # Download CSV
            # -------------------------------
            csv = result_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download Final Graded CSV",
                data=csv,
                file_name="final_grades.csv",
                mime="text/csv",
            )