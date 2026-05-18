"""
game.py - 게임 로직 관리 클래스
"""

from player import Player
from ai import AI


class Game:
    """가위바위보 게임을 관리하는 클래스"""

    MOVES = ["rock", "scissors", "paper"]

    # WINS[a] = b  → a가 b를 이긴다
    WINS = {
        "rock": "scissors",
        "scissors": "paper",
        "paper": "rock",
    }

    MOVE_KR = {
        "rock": "바위 ✊",
        "scissors": "가위 ✌️",
        "paper": "보 🖐️",
    }

    def __init__(self, player: Player, ai: AI):
        self.player = player
        self.ai = ai
        self.round: int = 0
        self.result_history: list[dict] = []

    # ─────────────────────────────────────────
    # 핵심 로직
    # ─────────────────────────────────────────

    def play_round(self, player_move: str) -> dict | None:
        """
        한 라운드를 진행합니다.
        Returns: 라운드 결과 딕셔너리 또는 None (잘못된 이동)
        """
        if player_move not in self.MOVES:
            return None

        self.round += 1

        # AI는 플레이어의 현재 히스토리를 보고 이동 결정 (이번 이동 포함 전)
        ai_move = self.ai.choose_move(self.player.get_history())

        # 플레이어 이동 기록
        self.player.add_move(player_move)

        # 승패 판정
        result = self._determine_winner(player_move, ai_move)

        if result == "player":
            self.player.add_score()
        elif result == "ai":
            self.ai.add_score()

        # 예측 정보 수집
        prediction_info = self.ai.get_prediction_info()

        round_data = {
            "round": self.round,
            "player_move": player_move,
            "player_move_kr": self.MOVE_KR[player_move],
            "ai_move": ai_move,
            "ai_move_kr": self.MOVE_KR[ai_move],
            "result": result,
            "result_kr": self._result_kr(result),
            "predicted_player_move": prediction_info["predicted_player_move"],
            "ai_confidence": prediction_info["confidence"],
            "player_score": self.player.score,
            "ai_score": self.ai.score,
        }

        self.result_history.append(round_data)
        return round_data

    def _determine_winner(self, player_move: str, ai_move: str) -> str:
        if player_move == ai_move:
            return "draw"
        elif self.WINS[player_move] == ai_move:
            return "player"
        else:
            return "ai"

    def _result_kr(self, result: str) -> str:
        return {"player": "🎉 플레이어 승!", "ai": "🤖 AI 승!", "draw": "🤝 무승부"}.get(
            result, ""
        )

    # ─────────────────────────────────────────
    # 통계
    # ─────────────────────────────────────────

    def get_stats(self) -> dict:
        total = self.round
        wins = sum(1 for r in self.result_history if r["result"] == "player")
        losses = sum(1 for r in self.result_history if r["result"] == "ai")
        draws = total - wins - losses

        win_rate = round(wins / total * 100, 1) if total > 0 else 0.0

        return {
            "round": self.round,
            "player_score": self.player.score,
            "ai_score": self.ai.score,
            "total_rounds": total,
            "wins": wins,
            "losses": losses,
            "draws": draws,
            "win_rate": win_rate,
            "player_move_counts": self.player.get_move_counts(),
            "result_history": self.result_history[-10:],  # 최근 10개
        }

    # ─────────────────────────────────────────
    # 직렬화
    # ─────────────────────────────────────────

    def reset(self) -> None:
        self.player.reset()
        self.ai.reset()
        self.round = 0
        self.result_history = []

    def to_dict(self) -> dict:
        return {
            "player": self.player.to_dict(),
            "ai": self.ai.to_dict(),
            "round": self.round,
            "result_history": self.result_history,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Game":
        player = Player.from_dict(data.get("player", {}))
        ai = AI.from_dict(data.get("ai", {}))
        game = cls(player, ai)
        game.round = data.get("round", 0)
        game.result_history = data.get("result_history", [])
        return game
