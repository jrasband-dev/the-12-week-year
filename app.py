import streamlit as st
import json
import pandas as pd

st.sidebar.title("12 Week Year Planner")
page = st.sidebar.selectbox("Navigate to:", ["Vision Setting", "12 Week Goals & Tactics", "Weekly Plans"])
checked_tactics = {}

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
        
        # Create columns for tactic and due inputs
        col1, col2 = st.columns(2)  # Two columns for tactic and due
        
        with col1:
            tactic_1 = st.text_input(f"Tactic #1 to Achieve Goal {i}", key=f"tactic_{i}_1")
            tactic_2 = st.text_input(f"Tactic #2 to Achieve Goal {i}", key=f"tactic_{i}_2")
            tactic_3 = st.text_input(f"Tactic #3 to Achieve Goal {i}", key=f"tactic_{i}_3")
        
        with col2:
            # Dropdown menu for Due (week)
            due_options = ["each week"] + [f"week {i}" for i in range(1, 13)]
            due_1 = st.selectbox(f"Due for Tactic #1 of Goal {i}", due_options, key=f"due_{i}_1")
            due_2 = st.selectbox(f"Due for Tactic #2 of Goal {i}", due_options, key=f"due_{i}_2")
            due_3 = st.selectbox(f"Due for Tactic #3 of Goal {i}", due_options, key=f"due_{i}_3")

        # You can store the data in `goals_data` or process it as needed
        goals_data[f"goal_{i}"] = {
            'goal': goal,
            'tactics': [
                {'tactic': tactic_1, 'due': due_1},
                {'tactic': tactic_2, 'due': due_2},
                {'tactic': tactic_3, 'due': due_3}
            ]
        }

    st.download_button(
            label="Export Goals & Tactics",
            data=json.dumps(goals_data, indent=4),
            file_name="12_week_plan.json",
            mime="application/json"
        )


elif page == "Weekly Plans":
    st.title("Create Weekly Plan")

    week_number = st.number_input("Enter the week number (1-12)", min_value=1, max_value=12, step=1)
    # File upload widget
    uploaded_file = st.file_uploader("Upload your 12-week plan JSON file", type="json")
    
    if uploaded_file is not None:
        # Read and parse the uploaded JSON
        plan_data = json.loads(uploaded_file.read())
        
        # Input for week number
        for goal_id, goal_data in plan_data.items():
            st.subheader(f"{goal_data['goal']}")
            
            # Filter tactics based on week number or "each week"
            for tactic in goal_data["tactics"]:
                tactic_due = tactic['due']
                # Only show tactics that match the week number or are set to "each week"
                if tactic_due == "each week" or f"week {week_number}" == tactic_due:
                    # Display tactic as a checkbox
                    tactic_key = f"tactic_{goal_id}_{tactic['tactic']}"
                    is_checked = st.checkbox(tactic['tactic'], key=tactic_key)
                    
                    # Store the checked status in the checked_tactics dictionary
                    if goal_id not in checked_tactics:
                        checked_tactics[goal_id] = []
                    checked_tactics[goal_id].append((tactic['tactic'], is_checked))
        
        # Optionally, display a button to save the weekly plan
        if st.button("Save Weekly Plan"):
            # Convert the weekly plan to Markdown format for display with checkboxes
            markdown_content = f"# Weekly Plan for Week {week_number}\n"
            for goal_key, tactics in checked_tactics.items():
                markdown_content += f"## {plan_data[goal_key]['goal']}\n"
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
                goal = plan_data[goal_key]["goal"]
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

    else:
        st.write("Please upload your 12-week plan JSON file to get started.")
