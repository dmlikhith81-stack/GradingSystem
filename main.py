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

    # select column for data analysis
    column = st.selectbox("Select column for grading", df.columns)

    max_value = st.number_input("Enter maximum marks", min_value=1.0, value=100.0)

    if st.button("Perform Relative Grading"):

        marks = df[column].astype(float)

        # Normalize marks 
        marks = (marks / marks.max()) * max_value

        mean = np.mean(marks)
        std = np.std(marks)

        
        if std == 0:
            st.error("Standard deviation is zero. Cannot perform relative grading.")
        else:
            z_scores = (marks - mean) / std

            def assign_grade(z):
                if z >= 1.5:
                    return "A+"
                elif z >= 1.0:
                    return "A"
                elif z >= 0.5:
                    return "B+"
                elif z >= 0:
                    return "B"
                elif z >= -0.5:
                    return "C"
                elif z >= -1.0:
                    return "D"
                else:
                    return "F"

            grades = z_scores.apply(assign_grade)

            df["Normalized Marks"] = marks
            df["Z-Score"] = z_scores
            df["Grade"] = grades

            st.write("### Graded Data")
            st.dataframe(df)

            # -------------------------------
            # Visualization
            # -------------------------------
            st.write("### Distribution Plot")

            fig, ax = plt.subplots()
            ax.hist(marks, bins=10)
            ax.axvline(mean, linestyle='dashed', linewidth=1)
            ax.set_title("Marks Distribution")
            st.pyplot(fig)

            st.write("### Grade Distribution")

            grade_counts = df["Grade"].value_counts()

            fig2, ax2 = plt.subplots()
            ax2.bar(grade_counts.index, grade_counts.values)
            ax2.set_title("Grade Distribution")
            st.pyplot(fig2)

            # -------------------------------
            # Download CSV
            # -------------------------------
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download Graded CSV",
                data=csv,
                file_name="graded_output.csv",
                mime="text/csv",
            )