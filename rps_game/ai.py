"""
ai.py - 패턴 학습 AI 객체 정의

전략:
1. Markov Chain (패턴 기반): 최근 N번의 이동 패턴으로 다음 이동 예측
2. Frequency Fallback: 패턴 데이터 부족 시 가장 자주 쓰는 이동 대응
3. Random Fallback: 데이터가 전혀 없을 때 랜덤
"""

import random
from collections import defaultdict


class AI:
    """패턴 학습 AI 클래스"""

    MOVES = ["rock", "scissors", "paper"]

    # 각 이동을 이기는 이동 (counter[x] = x를 이기는 이동)
    COUNTER = {
        "rock": "paper",      # 바위를 이기는 건 보자기
        "scissors": "rock",   # 가위를 이기는 건 바위
        "paper": "scissors",  # 보자기를 이기는 건 가위
    }

    def __init__(self, name: str = "AI", pattern_length: int = 3):
        self.name = name
        self.score: int = 0
        self.pattern_length = pattern_length
        self.move_history: list[str] = []
        self._last_predicted: str | None = None
        self._confidence: float = 0.0

    # ─────────────────────────────────────────
    # 패턴 학습 & 예측 (매번 전체 히스토리로 재계산)
    # ─────────────────────────────────────────

    def _build_pattern_table(self, player_history: list[str]) -> dict:
        """플레이어 히스토리로 Markov 패턴 테이블 구축"""
        table: dict = defaultdict(lambda: defaultdict(int))
        n = self.pattern_length

        for i in range(len(player_history) - n):
            pattern = tuple(player_history[i : i + n])
            next_move = player_history[i + n]
            table[pattern][next_move] += 1

        return table

    def predict_next_move(self, player_history: list[str]) -> tuple[str, float]:
        """
        플레이어의 다음 이동을 예측합니다.
        Returns: (예측 이동, 신뢰도 0.0~1.0)
        """
        if not player_history:
            return random.choice(self.MOVES), 0.0

        n = self.pattern_length

        # ── 전략 1: 마르코프 패턴 매칭 ──
        if len(player_history) >= n:
            table = self._build_pattern_table(player_history)
            recent_pattern = tuple(player_history[-n:])

            if recent_pattern in table:
                move_counts = table[recent_pattern]
                total = sum(move_counts.values())
                predicted = max(move_counts, key=move_counts.get)
                confidence = move_counts[predicted] / total
                return predicted, confidence

        # ── 전략 2: 단순 빈도 기반 ──
        if len(player_history) >= 2:
            freq: dict = defaultdict(int)
            for move in player_history:
                freq[move] += 1
            total = len(player_history)
            predicted = max(freq, key=freq.get)
            confidence = freq[predicted] / total
            return predicted, confidence

        # ── 전략 3: 랜덤 ──
        return random.choice(self.MOVES), 0.0

    def choose_move(self, player_history: list[str]) -> str:
        """
        플레이어의 다음 이동을 예측하고 이기는 이동을 선택합니다.
        """
        predicted, confidence = self.predict_next_move(player_history)
        self._last_predicted = predicted
        self._confidence = confidence

        counter_move = self.COUNTER[predicted]
        self.move_history.append(counter_move)
        return counter_move

    # ─────────────────────────────────────────
    # 상태 관리
    # ─────────────────────────────────────────

    def add_score(self) -> None:
        self.score += 1

    def get_prediction_info(self) -> dict:
        """마지막 예측 정보 반환"""
        return {
            "predicted_player_move": self._last_predicted,
            "confidence": round(self._confidence * 100, 1),
        }

    def reset(self) -> None:
        self.score = 0
        self.move_history = []
        self._last_predicted = None
        self._confidence = 0.0

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "score": self.score,
            "move_history": self.move_history,
            "pattern_length": self.pattern_length,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "AI":
        ai = cls(
            name=data.get("name", "AI"),
            pattern_length=data.get("pattern_length", 3),
        )
        ai.score = data.get("score", 0)
        ai.move_history = data.get("move_history", [])
        return ai
