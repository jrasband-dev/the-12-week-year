import streamlit as st
import json

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
        
        if goal:
            goals_data[f"Goal {i}"] = {
                "Goal": goal,
                "Tactics": [tactic_1, tactic_2, tactic_3]
            }
    
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
        
        # Initialize session state for checkboxes if not already initialized
        if "checked_tactics" not in st.session_state:
            st.session_state.checked_tactics = {goal_key: [False] * len(goal_content["Tactics"])
                                                for goal_key, goal_content in plan_data.items()}
        
        # Display each goal with tactics as checkboxes, using session state for persistence
        for goal_key, goal_content in plan_data.items():
            st.subheader(goal_content["Goal"])
            tactics = goal_content["Tactics"]
            
            for idx, tactic in enumerate(tactics):
                if tactic:  # Only display non-empty tactics
                    # Each checkbox is tied to session state
                    st.session_state.checked_tactics[goal_key][idx] = st.checkbox(
                        tactic,
                        key=f"{goal_key}_{idx}",
                        value=st.session_state.checked_tactics[goal_key][idx]
                    )

        # Display and save checked status as a JSON file for progress tracking
        if st.button("Save Weekly Plan with Checkboxes"):
            weekly_plan_data = {
                "Week": week_number,
                "Goals": {}
            }
            for goal_key, tactics in st.session_state.checked_tactics.items():
                weekly_plan_data["Goals"][goal_key] = {
                    "Goal": plan_data[goal_key]["Goal"],
                    "Tactics": [
                        {"Tactic": plan_data[goal_key]["Tactics"][i], "Completed": status}
                        for i, status in enumerate(tactics)
                    ]
                }
            
            st.download_button(
                label="Download Weekly Plan with Progress as JSON",
                data=json.dumps(weekly_plan_data, indent=4),
                file_name=f"weekly_plan_week_{week_number}.json",
                mime="application/json"
            )