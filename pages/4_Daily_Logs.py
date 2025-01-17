import streamlit as st
from db import get_conn
import pandas as pd
from repos.sqlite import SQLiteLogRepository, SQLiteTeamRepository, SQLiteMemberRepository

st.set_page_config(layout="wide")

# Initialize database and repositories
conn = get_conn()
team_repo = SQLiteTeamRepository(conn)
log_repo = SQLiteLogRepository(conn)
member_repo = SQLiteMemberRepository(conn)

st.title("📋 Daily Logs")
# Fetch all teams
teams = team_repo.get_teams()
if teams:
    # Create a tab for each team
    tabs = st.tabs([team["name"] for team in teams])

    for i, team in enumerate(teams):
        with tabs[i]:
            st.subheader(f"Team: {team['name']}")

            # Fetch logs for the team
            logs = log_repo.get_logs_by_team(team["id"])
            if logs:
                logs_df = pd.DataFrame(logs)

                # Convert timestamp to date
                logs_df["date"] = pd.to_datetime(logs_df["timestamp"]).dt.date

                # Get unique exercises for the team
                exercises = logs_df["exercise"].unique()

                # Get all members in the team
                members = member_repo.get_members_by_team(team["id"])
                member_names = [member["name"] for member in members]

                # Display exercises in a 2x2 grid
                cols = st.columns(2)  # Create 2 columns for the grid

                for j, exercise in enumerate(exercises):
                    # Alternate between columns for each exercise
                    with cols[j % 2]:
                        st.write(f"**Exercise: {exercise}**")

                        # Filter logs for the current exercise
                        exercise_logs = logs_df[logs_df["exercise"] == exercise]

                        # Pivot the table: Members as columns, Reps as values
                        pivot_table = exercise_logs.pivot_table(
                            index="date",
                            columns="member",
                            values="reps",
                            aggfunc="sum",
                            fill_value=0,
                        ).reset_index()

                        # Ensure all members have a column, even if they have no logs
                        for member in member_names:
                            if member not in pivot_table.columns:
                                pivot_table[member] = 0

                        # Reorder columns to match member order
                        pivot_table = pivot_table[["date"] + member_names]

                        # Rename columns for better readability
                        pivot_table = pivot_table.rename(columns={"date": "Day"}).set_index("Day")

                        # Display the table
                        st.table(pivot_table)
            else:
                st.info(f"No logs found for {team['name']}.")
else:
    st.warning("No teams found. Add teams in the 'Manage Teams and Exercises' section.")