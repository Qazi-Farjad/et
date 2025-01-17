from abc import ABC, abstractmethod
from typing import List, Dict

# Abstract base class for Team repository
class TeamRepository(ABC):
    @abstractmethod
    def add_team(self, name: str) -> None:
        pass

    @abstractmethod
    def get_teams(self) -> List[Dict]:
        pass

# Abstract base class for Member repository
class MemberRepository(ABC):
    @abstractmethod
    def add_member(self, team_id: int, name: str) -> None:
        pass

    @abstractmethod
    def get_members_by_team(self, team_id: int) -> List[Dict]:
        pass

# Abstract base class for Exercise repository
class ExerciseRepository(ABC):
    @abstractmethod
    def add_exercise(self, name: str) -> None:
        pass

    @abstractmethod
    def get_exercises(self) -> List[Dict]:
        pass

# Abstract base class for Log repository
class LogRepository(ABC):
    @abstractmethod
    def add_log(self, team_id: int, member_id: int, exercise_id: int, weight: float, reps: int) -> None:
        pass

    @abstractmethod
    def get_logs(self) -> List[Dict]:
        pass