import streamlit as st
import pandas as pd
import altair as alt

# Upload Excel file
uploaded_file = st.file_uploader("📂 Upload your Excel file", type=["xlsx"])

if uploaded_file is not None:
    # Read the Excel file
    df = pd.read_excel(uploaded_file)

    # Define Pass/Fail Criteria
    df["Result"] = df.apply(lambda row: "Pass" if row["EXTERNAL"] >= 45 and row["TOTAL"] >= 50 else "Fail", axis=1)

    # Get subject-wise pass/fail count
    subject_pass_fail = df.groupby(["SUBJECT CODE", "Result"]).size().unstack(fill_value=0)
    
    # Get department-wise pass/fail count
    department_pass_fail = df.groupby(["DEPARTMENT", "Result"]).size().unstack(fill_value=0)

    # Compute average marks per subject
    subject_avg = df.groupby("SUBJECT CODE")[["INTERNAL", "EXTERNAL", "TOTAL"]].mean().reset_index()

    # =======================
    # 📚 Subject-wise Pass/Fail Chart
    # =======================
    st.subheader("📊 Subject-wise Pass/Fail Count")

    subject_df = subject_pass_fail.reset_index().melt(id_vars="SUBJECT CODE", var_name="Result", value_name="Count")

    color_scale = alt.Scale(domain=["Pass", "Fail"], range=["lightgreen", "lightcoral"])

    chart1 = alt.Chart(subject_df).mark_bar(width=30).encode(
        x=alt.X("SUBJECT CODE:N", title="Subjects", axis=alt.Axis(labelAngle=-45, labelFontSize=14, titleFontSize=16)),
        y=alt.Y("Count:Q", title="Student Count", axis=alt.Axis(labelFontSize=14, titleFontSize=16)),
        color=alt.Color("Result:N", scale=color_scale, legend=alt.Legend(title="Result", labelFontSize=14, titleFontSize=16)),
        xOffset=alt.X("Result:N")
    ).properties(title=alt.TitleParams("", fontSize=18, fontWeight="bold"))

    text1 = chart1.mark_text(
        align="center", baseline="bottom", dy=-5, fontSize=16, fontWeight="bold", color="black"
    ).encode(text="Count:Q")

    st.altair_chart(chart1 + text1, use_container_width=True)

    # =======================
    # 📚 Department-wise Pass/Fail Chart
    # =======================
    st.subheader("🏢 Department-wise Pass/Fail Count")

    department_df = department_pass_fail.reset_index().melt(id_vars="DEPARTMENT", var_name="Result", value_name="Count")

    chart2 = alt.Chart(department_df).mark_bar(width=30).encode(
        x=alt.X("DEPARTMENT:N", title="Departments", axis=alt.Axis(labelAngle=-45, labelFontSize=14, titleFontSize=16)),
        y=alt.Y("Count:Q", title="Student Count", axis=alt.Axis(labelFontSize=14, titleFontSize=16)),
        color=alt.Color("Result:N", scale=color_scale, legend=alt.Legend(title="Result", labelFontSize=14, titleFontSize=16)),
        xOffset=alt.X("Result:N")
    ).properties(title=alt.TitleParams("", fontSize=18, fontWeight="bold"))

    text2 = chart2.mark_text(
        align="center", baseline="bottom", dy=-5, fontSize=16, fontWeight="bold", color="black"
    ).encode(text="Count:Q")

    st.altair_chart(chart2 + text2, use_container_width=True)

   
    # =======================
    # 📊 Average Marks per Subject Chart
    st.subheader("📈 Average Marks per Subject")

    # Round values to 2 decimal places
    subject_avg_melted = subject_avg.melt(id_vars="SUBJECT CODE", var_name="Category", value_name="Average Marks")
    subject_avg_melted["Average Marks"] = subject_avg_melted["Average Marks"].round(2)

    # Define colors
    color_palette = alt.Scale(domain=["INTERNAL", "EXTERNAL", "TOTAL"], range=["#4682B4", "#8B0000", "#228B22"])

    # Create grouped bar chart with spacing
    chart3 = alt.Chart(subject_avg_melted).mark_bar(width=20).encode(
        x=alt.X("SUBJECT CODE:N", title="Subjects", axis=alt.Axis(labelAngle=-45, labelFontSize=14, titleFontSize=16)),
        y=alt.Y("Average Marks:Q", title="Average Marks", axis=alt.Axis(labelFontSize=14, titleFontSize=16)),
        color=alt.Color("Category:N", scale=color_palette, legend=alt.Legend(title="Category", labelFontSize=14, titleFontSize=16)),
        xOffset=alt.X("Category:N", sort=["INTERNAL", "EXTERNAL", "TOTAL"])  # Adds spacing between bars
    ).properties(title=alt.TitleParams("", fontSize=18, fontWeight="bold"))

    # Add text labels with two decimal places
    text3 = chart3.mark_text(
        align="center", baseline="bottom", dy=-5, fontSize=12, fontWeight="bold", color="black"
    ).encode(text=alt.Text("Average Marks:Q", format=".2f"))  # Format to 2 decimal places

    # Render chart
    st.altair_chart(chart3 + text3, use_container_width=True)

    


    import altair as alt
    import pandas as pd

    # Function to assign grades
    def assign_grade(marks):
        if marks >= 91:
            return "O"
        elif marks >= 81:
            return "A+"
        elif marks >= 71:
            return "A"
        elif marks >= 61:
            return "B+"
        elif marks >= 51:
            return "B"
        elif marks >= 40:
            return "C"
        else:
            return "U"  # Fail

    # Apply grading function
    df["Grade"] = df["TOTAL"].apply(assign_grade)

    # Define grade order
    grade_order = ["O", "A+", "A", "B+", "B", "C", "U"]

    # Ensure all grades appear for each subject (even if count is 0)
    subjects = df["SUBJECT CODE"].unique()
    all_combinations = pd.MultiIndex.from_product([subjects, grade_order], names=["SUBJECT CODE", "Grade"])
    subject_grade_counts = df.groupby(["SUBJECT CODE", "Grade"]).size().reindex(all_combinations, fill_value=0).reset_index(name="Count")

    # Define color scale
    grade_color_scale = alt.Scale(
        domain=grade_order,
        range=["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2"]
    )

    # Create base chart with bars (Set height **here**)
    base = alt.Chart(subject_grade_counts).mark_bar().encode(
        y=alt.Y("Grade:N", title="Grade", sort=grade_order),
        x=alt.X("Count:Q", title="Number of Students"),
        color=alt.Color("Grade:N", scale=grade_color_scale, legend=None)
    ).properties(
        width=600,
        height=150  # ✅ Height is set in the base chart, NOT in facet()
    )

    # Text labels (only for non-zero counts)
    text = base.mark_text(
        align="left",
        baseline="middle",
        dx=3,  # Moves text slightly right for visibility
        fontSize=14,
        fontWeight="bold",
        color="black"
    ).encode(
        text=alt.condition(alt.datum.Count > 0, alt.Text("Count:Q"), alt.value(""))  # Show only non-zero values
    )

    # Combine base bars and text, then facet by subject
    final_chart = alt.layer(base, text).facet(
        row=alt.Row("SUBJECT CODE:N", title="Subject"),
        spacing=10  # Adjust spacing between subjects
    )

    # Render chart
    st.altair_chart(final_chart, use_container_width=True)
