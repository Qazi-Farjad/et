import sqlite3
from typing import List, Dict
from .base import TeamRepository, MemberRepository, ExerciseRepository, LogRepository

class SQLiteTeamRepository(TeamRepository):
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def add_team(self, name: str) -> None:
        self.conn.execute("INSERT INTO teams (name) VALUES (?)", (name,))
        self.conn.commit()

    def get_teams(self) -> List[Dict]:
        return [{"id": row[0], "name": row[1]} for row in self.conn.execute("SELECT id, name FROM teams").fetchall()]

class SQLiteMemberRepository(MemberRepository):
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def add_member(self, team_id: int, name: str) -> None:
        self.conn.execute("INSERT INTO members (team_id, name) VALUES (?, ?)", (team_id, name))
        self.conn.commit()

    def get_members(self) -> List[Dict]:
        return [{
            "id": row[0],
            "name": row[1],
            "team": row[2],
            "team_id": row[3]
                 } for row in self.conn.execute(
                     "SELECT m.id, m.name, teams.name  as team, teams.id as team_id FROM members m join teams on teams.id = m.team_id"
                     ).fetchall()]

    def get_members_by_team(self, team_id: int) -> List[Dict]:
        return [{
            "id": row[0],
            "name": row[1],
            "team": row[2],
            "team_id": row[3]
                 } for row in self.conn.execute(
                     "SELECT m.id, m.name, teams.name as team, teams.id as team_id FROM members m join teams on teams.id = m.team_id WHERE team_id = ?", (team_id,)
                     ).fetchall()]

class SQLiteExerciseRepository(ExerciseRepository):
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def add_exercise(self, name: str, points_per_rep: int) -> None:
        self.conn.execute("INSERT INTO exercises (name, points_per_rep) VALUES (?, ?)", (name, points_per_rep))
        self.conn.commit()

    def get_exercises(self) -> List[Dict]:
        return [{"id": row[0], "name": row[1], "points_per_rep": row[2]}
                for row in self.conn.execute("SELECT id, name, points_per_rep FROM exercises").fetchall()]

    def update_exercise(self, exercise_id: int, name: str, points_per_rep: int) -> None:
        self.conn.execute(
            "UPDATE exercises SET name = ?, points_per_rep = ? WHERE id = ?",
            (name, points_per_rep, exercise_id),
        )
        self.conn.commit()

class SQLiteLogRepository(LogRepository):
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def add_log(self, team_id: int, member_id: int, exercise_id: int, reps: int) -> None:
        # Fetch points_per_rep for the exercise
        points_per_rep = self.conn.execute(
            "SELECT points_per_rep FROM exercises WHERE id = ?", (exercise_id,)
        ).fetchone()[0]

        # Calculate points
        points = reps * points_per_rep

        # Insert the log with calculated points
        self.conn.execute("""
            INSERT INTO logs (team_id, member_id, exercise_id, reps, points)
            VALUES (?, ?, ?, ?, ?)
        """, (team_id, member_id, exercise_id, reps, points))
        self.conn.commit()

    def get_logs(self) -> List[Dict]:
        return [{"team": row[0], "member": row[1], "exercise": row[2], "reps": row[3], "points": row[4], "timestamp": row[5]}
                for row in self.conn.execute("""
                    SELECT t.name, m.name, e.name, l.reps, l.points, l.timestamp
                    FROM logs l
                    JOIN teams t ON l.team_id = t.id
                    JOIN members m ON l.member_id = m.id
                    JOIN exercises e ON l.exercise_id = e.id
                """).fetchall()]
    
    def get_logs_by_member(self, member_id: int) -> List[Dict]:
        return [{"Member": row[0], "Exercise": row[1], "Reps": row[2], "Date": row[3]}
                for row in self.conn.execute("""
                    SELECT m.name, e.name, l.reps, date(l.timestamp)
                    FROM logs l
                    JOIN members m ON l.member_id = m.id
                    JOIN exercises e ON l.exercise_id = e.id
                    WHERE member_id = ?
                """, (member_id,)).fetchall()]
    
    def get_logs_by_team(self, team_id: int) -> List[Dict]:
        return [{"team": row[0], "member": row[1], "exercise": row[2], "reps": row[3], "points": row[4], "timestamp": row[5]}
                for row in self.conn.execute("""
                    SELECT t.name, m.name, e.name, l.reps, l.points, l.timestamp
                    FROM logs l
                    JOIN teams t ON l.team_id = t.id
                    JOIN members m ON l.member_id = m.id
                    JOIN exercises e ON l.exercise_id = e.id
                    WHERE t.id = ?
                """, (team_id,)).fetchall()]
