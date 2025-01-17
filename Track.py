import streamlit as st
from db import init_db, get_conn
from repos.sqlite import SQLiteMemberRepository, SQLiteExerciseRepository, SQLiteLogRepository, SQLiteTeamRepository

st.set_page_config(page_title="Track", layout="wide")

# Main app title
st.title("Exercise Tracker")
# Welcome message
st.write("Use the sidebar to navigate to different sections.")

# Initialize database and repositories
conn = get_conn()
init_db(conn)

team_repo = SQLiteTeamRepository(conn)
member_repo = SQLiteMemberRepository(conn)
exercise_repo = SQLiteExerciseRepository(conn)
log_repo = SQLiteLogRepository(conn)

# Cache the selected member in session state
if "selected_member" not in st.session_state:
    st.session_state.selected_member = None

# Select Member
teams = team_repo.get_teams()
if teams:
    # Get all members across all teams
    all_members = []
    for team in teams:
        members = member_repo.get_members_by_team(team["id"])
        all_members.extend(members)

    st.subheader("Banda select karo")
    selected_member = st.selectbox(
        "Member",
        all_members,
        format_func=lambda x: f"{x['name']}",
        index=(
            all_members.index(st.session_state.selected_member)
            if st.session_state.selected_member in all_members
            else 0
        ),
    )
    
    if st.button("Set as Current User"):
        st.session_state.selected_member = selected_member
        st.success(f"Current user set to {selected_member['name']}!")

    # Display the current user and log entry in the second column
    if st.session_state.selected_member:
        st.subheader(f"User: {selected_member['name']}, Team: {selected_member['team']}")

        # Log Reps for All Exercises
        st.write("**Log Reps for All Exercises**")
        exercises = exercise_repo.get_exercises()
        if exercises:
            # Create a form for logging reps
            with st.form("log_reps_form"):
                # Add a number input for each exercise
                reps_data = {}
                for exercise in exercises:
                    reps_data[exercise["id"]] = st.number_input(
                        f"Reps for {exercise['name']}",
                        min_value=0,
                        value=0,
                        key=f"reps_{exercise['id']}",
                    )
                
                # Submit button for the form
                if st.form_submit_button("Log Reps for All Exercises"):
                    # Log reps for each exercise
                    for exercise_id, reps in reps_data.items():
                        if reps > 0:  # Only log if reps are greater than 0
                            log_repo.add_log(
                                st.session_state.selected_member["team_id"],
                                st.session_state.selected_member["id"],
                                exercise_id,
                                reps,
                            )
                    st.success("Reps logged successfully for all exercises!")
        else:
            st.warning("No exercises found. Add exercises in the 'Manage Teams and Exercises' section.")
    else:
        st.warning("Please select a member to log reps.")
else:
    st.warning("No teams found. Add teams in the 'Manage Teams and Exercises' section.")