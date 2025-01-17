import streamlit as st
import pandas as pd
from db import get_conn
from repos.sqlite import SQLiteLogRepository
from visualizations import *

st.set_page_config(layout="wide")

# Initialize database and repositories
conn = get_conn()
log_repo = SQLiteLogRepository(conn)

st.title("📊 Visualizations")

logs = log_repo.get_logs()
if logs:
    logs_df = pd.DataFrame(logs)

    # Create a grid layout for the charts
    col1, col2 = st.columns(2)  # Two columns for the grid

    with col1:
        # Chart 1: Point Totals by Team
        show_point_totals_by_person(logs_df, st)

    with col2:
        # Chart 3: Reps Over Time
        show_aggregated_team_scores(logs_df, st)


    # Add a spacer between rows
    st.write("")  # Empty space for better spacing

    col3, col4 = st.columns(2)  # Two columns for the grid

    with col3:
        # Chart 3: Total Points by Member
        show_points_by_exercise_and_member(logs_df, st)

    with col4:
        # Chart 4: Points Distribution by Exercise
        pass

else:
    st.info("No logs available for visualization.")