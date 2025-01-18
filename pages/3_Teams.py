import streamlit as st
import pandas as pd
from db import get_conn, sqlite3
from repos.sqlite import SQLiteTeamRepository, SQLiteMemberRepository, SQLiteLogRepository, SQLiteExerciseRepository

st.set_page_config(layout="wide")

conn = get_conn()
team_repo = SQLiteTeamRepository(conn)
member_repo = SQLiteMemberRepository(conn)
log_repo = SQLiteLogRepository(conn)
exercise_repo = SQLiteExerciseRepository(conn)


tab1, tab2, tab3 = st.tabs(["👥 Teams", "⚙️ Manage Teams", "Edit Exercises",])

with tab1:
    # Fetch all teams and members
    teams = team_repo.get_teams()
    exercises = exercise_repo.get_exercises()
    if teams:
        # Use expanders to organize teams
        for team in teams:
            with st.expander(f"Team: {team['name']}", expanded=True):
                members = member_repo.get_members_by_team(team["id"])
                if members:
                    # Create a list to store member data
                    member_data = []

                    for member in members:
                        # Fetch logs for the member
                        logs = log_repo.get_logs_by_member(member["id"])
                        logs_df = pd.DataFrame(logs)
                        # logs_df
                        last_log_date = max(log["Date"] for log in logs) if logs else "No logs"
                        # logs_df.columns
                        tmp = {"Member": member["name"]}
                        for ex in exercises:
                            if len(logs_df) == 0:
                                tmp[ex['name']] = 0
                            else:
                                tmp[ex['name']] = logs_df[logs_df['Exercise'] == ex['name']]['Reps'].sum()
                        tmp["Last Log"] = last_log_date
                        # Add data to the list
                        member_data.append(tmp)

                    # Display the data in a table
                    st.table(pd.DataFrame(member_data).astype(str))
                else:
                    st.warning("No members found for this team.")
    else:
        st.warning("No teams found. Add teams in the 'Manage Teams and Exercises' section.")

with tab2:
    # Add Team
    st.header("Add Team")
    team_name = st.text_input("Team Name")
    if st.button("Add Team"):
        if team_name:
            try:
                team_repo.add_team(team_name)
                st.success(f"Team '{team_name}' added!")
            except sqlite3.IntegrityError:
                st.error("Team name already exists.")
        else:
            st.error("Team name is required.")

    # Add Member to Team
    st.header("Add Member")
    teams = team_repo.get_teams()
    if teams:
        selected_team = st.selectbox("Select Team", teams, format_func=lambda x: x["name"])
        member_name = st.text_input("Member Name")
        if st.button("Add Member"):
            if member_name:
                member_repo.add_member(selected_team["id"], member_name)
                st.success(f"Member '{member_name}' added to '{selected_team['name']}'!")
            else:
                st.error("Member name is required.")
    else:
        st.warning("No teams found. Add a team first.")

with tab3:
    # Display and Edit Exercises
    st.header("Current Exercises")
    exercises = exercise_repo.get_exercises()
    if exercises:
        # Display exercises in a table
        st.table(exercises)

        # Edit Exercise
        st.subheader("Edit Exercise")
        exercise_to_edit = st.selectbox(
            "Select Exercise to Edit",
            exercises,
            format_func=lambda x: f"{x['name']} ({x['points_per_rep']} points per rep)",
        )
        new_name = st.text_input("New Exercise Name", value=exercise_to_edit["name"])
        new_points_per_rep = st.number_input(
            "New Points per Rep",
            min_value=1,
            value=exercise_to_edit["points_per_rep"],
        )
        if st.button("Update Exercise"):
            exercise_repo.update_exercise(exercise_to_edit["id"], new_name, new_points_per_rep)
            st.success(f"Exercise '{exercise_to_edit['name']}' updated!")
    else:
        st.info("No exercises found. Add exercises above.")

    # Add Exercise
    st.header("Add New Exercise")
    exercise_name = st.text_input("Exercise Name")
    points_per_rep = st.number_input("Points per Rep", min_value=1, value=1)
    if st.button("Add Exercise"):
        if exercise_name:
            try:
                exercise_repo.add_exercise(exercise_name, points_per_rep)
                st.success(f"Exercise '{exercise_name}' added!")
            except sqlite3.IntegrityError:
                st.error("Exercise name already exists.")
        else:
            st.error("Exercise name is required.")

