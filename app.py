import streamlit as st
import json

st.sidebar.title("12 Week Year Planner")
page = st.sidebar.selectbox("Navigate to:", ["Vision Setting", "12 Week Goals & Tactics", "Weekly Plans"])

if page == "Vision Setting":
    st.title("Vision Setting")
    st.subheader("Define Your Long-Term Vision")
    long_term_vision = st.text_area("What's your vision for the future?")

    if st.button("Export Vision"):
        vision_data = {
            "Long-Term Vision": long_term_vision,
        }
        st.download_button(
            label="Download Vision",
            data=json.dumps(vision_data),
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
    
    if st.button("Export Goals & Tactics"):
        st.download_button(
            label="Download Goals & Tactics as JSON",
            data=json.dumps(goals_data, indent=4),
            file_name="12_week_plan.json",
            mime="application/json"
        )

elif page == "Weekly Plans":
    st.title("Weekly Plans")

    # Upload JSON file
    uploaded_file = st.file_uploader("Upload your 12 Week Plan JSON file", type="json")
    
    if uploaded_file:
        plan_data = json.load(uploaded_file)
        
        # Display each goal with tactics as checkboxes
        checked_tactics = {}
        for goal_key, goal_content in plan_data.items():
            st.subheader(goal_content["Goal"])
            tactics = goal_content["Tactics"]
            checked_tactics[goal_key] = []
            
            for tactic in tactics:
                if tactic:  # Check if tactic text is not empty
                    is_checked = st.checkbox(tactic, key=f"{goal_key}_{tactic}")
                    checked_tactics[goal_key].append((tactic, is_checked))
