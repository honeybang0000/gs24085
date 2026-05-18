"""
player.py - 플레이어 객체 정의
"""


class Player:
    """사용자 플레이어를 나타내는 클래스"""

    VALID_MOVES = ["rock", "scissors", "paper"]

    def __init__(self, name: str = "Player"):
        self.name = name
        self.move_history: list[str] = []
        self.score: int = 0

    def add_move(self, move: str) -> bool:
        """플레이어의 이동을 기록합니다."""
        if move not in self.VALID_MOVES:
            return False
        self.move_history.append(move)
        return True

    def add_score(self) -> None:
        """점수를 1 올립니다."""
        self.score += 1

    def get_history(self) -> list[str]:
        """이동 기록을 반환합니다."""
        return list(self.move_history)

    def get_move_counts(self) -> dict:
        """각 이동의 빈도를 반환합니다."""
        counts = {move: 0 for move in self.VALID_MOVES}
        for move in self.move_history:
            counts[move] += 1
        return counts

    def reset(self) -> None:
        """플레이어 상태를 초기화합니다."""
        self.move_history = []
        self.score = 0

    def to_dict(self) -> dict:
        """직렬화용 딕셔너리 반환"""
        return {
            "name": self.name,
            "move_history": self.move_history,
            "score": self.score,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Player":
        """딕셔너리로부터 Player 객체 복원"""
        p = cls(name=data.get("name", "Player"))
        p.move_history = data.get("move_history", [])
        p.score = data.get("score", 0)
        return p
