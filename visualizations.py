import pandas as pd
import plotly.express as px

# Consistent color mapping for teams
def get_team_colors(logs_df):
    teams = logs_df["team"].unique()
    return {team: px.colors.qualitative.Plotly[i % len(px.colors.qualitative.Plotly)] 
            for i, team in enumerate(teams)}

# Bar chart: Point totals for all persons, color-coded by team
def show_point_totals_by_person(logs_df, st):
    st.subheader("Point Totals by Person")
    person_points = logs_df.groupby(["team", "member"])["points"].sum().reset_index()
    team_colors = get_team_colors(logs_df)
    fig = px.bar(
        person_points,
        x="member",
        y="points",
        color="team",
        title="Point Totals by Person",
        color_discrete_map=team_colors,
    )
    st.plotly_chart(fig)

# Bar charts: Points by exercise and member, color-coded by team
def show_points_by_exercise_and_member(logs_df, st):
    st.subheader("Points by Exercise and Member")
    exercises = logs_df["exercise"].unique()
    team_colors = get_team_colors(logs_df)
    
    for exercise in exercises:
        st.write(f"**Exercise: {exercise}**")
        exercise_data = logs_df[logs_df["exercise"] == exercise]
        member_points = exercise_data.groupby(["team", "member"])["points"].sum().reset_index()
        fig = px.bar(
            member_points,
            x="member",
            y="points",
            color="team",
            title=f"Points for {exercise} by Member",
            color_discrete_map=team_colors,
        )
        st.plotly_chart(fig)

# Bar chart: Aggregated team scores, color-coded by team
def show_aggregated_team_scores(logs_df, st):
    st.subheader("Aggregated Team Scores")
    team_points = logs_df.groupby("team")["points"].sum().reset_index()
    team_colors = get_team_colors(logs_df)
    fig = px.bar(
        team_points,
        x="team",
        y="points",
        color="team",
        title="Aggregated Team Scores",
        color_discrete_map=team_colors,
    )
    st.plotly_chart(fig)