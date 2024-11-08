import streamlit as st
import json
import pandas as pd

st.sidebar.title("12 Week Year Planner")
page = st.sidebar.selectbox("Navigate to:", ["Vision Setting", "12 Week Goals & Tactics", "Weekly Plans"])

if page == "Vision Setting":
    st.title("Vision Setting")
    st.subheader("Define Your Long-Term Vision")
    long_term_vision = st.text_area("What's your vision for the future?")

    st.download_button(
            label="Download Vision",
            data=long_term_vision,
            file_name="vision.json",
            mime="application/json"
        )

elif page == "12 Week Goals & Tactics":
    st.title("12 Week Goals & Tactics")
    
    goals_data = {}
    for i in range(1, 4):  # Up to three goals
        st.subheader(f"Goal {i}")
        goal = st.text_input(f"Set Goal {i}", key=f"goal_{i}")
        
        tactic_1 = st.text_area(f"Tactic #1 to Achieve Goal {i}", key=f"tactic_{i}_1")
        tactic_2 = st.text_area(f"Tactic #2 to Achieve Goal {i}", key=f"tactic_{i}_2")
        tactic_3 = st.text_area(f"Tactic #3 to Achieve Goal {i}", key=f"tactic_{i}_3")
        
        # Add dropdown for Due field
        due_field = st.selectbox(
            f"Due for Goal {i}",
            options=["Each week", "Week 1", "Week 2", "Week 3", "Week 4", "Week 5", "Week 6", "Week 7", "Week 8", "Week 9", "Week 10", "Week 11", "Week 12"],
            key=f"due_{i}"
        )
        
        if goal:
            goals_data[f"Goal {i}"] = {
                "Goal": goal,
                "Tactics": [tactic_1, tactic_2, tactic_3],
                "Due": due_field
            }
    
    if st.button("Export Goals & Tactics"):
        st.download_button(
            label="Download Goals & Tactics as JSON",
            data=json.dumps(goals_data, indent=4),
            file_name="12_week_plan.json",
            mime="application/json"
        )

elif page == "Weekly Plans":
    st.title("Weekly Plans")

    # Add input for week number
    week_number = st.number_input("Enter the Week Number (1-12)", min_value=1, max_value=12, step=1)

    # Upload JSON file
    uploaded_file = st.file_uploader("Upload your 12 Week Plan JSON file", type="json")
    
    if uploaded_file:
        plan_data = json.load(uploaded_file)
        
        # Display each goal with tactics as checkboxes, filtering by the selected week
        checked_tactics = {}
        for goal_key, goal_content in plan_data.items():
            st.subheader(goal_content["Goal"])
            tactics = goal_content["Tactics"]
            due_date = goal_content["Due"]
            checked_tactics[goal_key] = []
            
            for tactic in tactics:
                if tactic:  # Check if tactic text is not empty
                    if due_date == "Each week" or due_date == f"Week {week_number}":
                        is_checked = st.checkbox(tactic, key=f"{goal_key}_{tactic}")
                        checked_tactics[goal_key].append((tactic, is_checked))
        
        # Convert the weekly plan to Markdown format for display with checkboxes
        if st.button("Save Weekly Plan"):
            markdown_content = f"# Weekly Plan for Week {week_number}\n"
            for goal_key, tactics in checked_tactics.items():
                markdown_content += f"## {plan_data[goal_key]['Goal']}\n"
                for tactic, completed in tactics:
                    checkbox = "[x]" if completed else "[ ]"
                    markdown_content += f"- {checkbox} {tactic}\n"
                markdown_content += "\n"

            # Provide the Markdown content as a downloadable file
            st.download_button(
                label="Download Weekly Plan as Markdown",
                data=markdown_content,
                file_name=f"weekly_plan_week_{week_number}.md",
                mime="text/markdown"
            )

            # Prepare CSV export
            csv_data = []
            for goal_key, tactics in checked_tactics.items():
                goal = plan_data[goal_key]["Goal"]
                for tactic, completed in tactics:
                    csv_data.append([goal, tactic, "Completed" if completed else "Incomplete"])

            # Convert the data to a pandas DataFrame and export as CSV
            df = pd.DataFrame(csv_data, columns=["Goal", "Tactic", "Status"])

            st.download_button(
                label="Download Weekly Plan as CSV",
                data=df.to_csv(index=False),
                file_name=f"weekly_plan_week_{week_number}.csv",
                mime="text/csv"
            )
