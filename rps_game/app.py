"""
app.py - Flask 웹 애플리케이션 진입점
Render 배포용 (gunicorn 사용)
"""

import os
import json
from flask import Flask, render_template, request, jsonify, session

from player import Player
from ai import AI
from game import Game

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "rps-ai-secret-2024-change-me")


# ─────────────────────────────────────────
# 세션 기반 게임 상태 관리
# ─────────────────────────────────────────


def get_game() -> Game:
    """세션에서 게임 상태를 복원합니다."""
    if "game_data" not in session:
        player = Player(name="Player")
        ai = AI(name="AI", pattern_length=3)
        return Game(player, ai)

    try:
        return Game.from_dict(json.loads(session["game_data"]))
    except Exception:
        player = Player(name="Player")
        ai = AI(name="AI", pattern_length=3)
        return Game(player, ai)


def save_game(game: Game) -> None:
    """게임 상태를 세션에 저장합니다."""
    session["game_data"] = json.dumps(game.to_dict())


# ─────────────────────────────────────────
# 라우트
# ─────────────────────────────────────────


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/play", methods=["POST"])
def play():
    """한 라운드 진행"""
    data = request.get_json(force=True)
    player_move = data.get("move", "")

    if player_move not in ["rock", "scissors", "paper"]:
        return jsonify({"error": "잘못된 이동입니다."}), 400

    game = get_game()
    round_data = game.play_round(player_move)
    save_game(game)

    return jsonify(
        {
            "round_data": round_data,
            "stats": game.get_stats(),
        }
    )


@app.route("/api/stats", methods=["GET"])
def stats():
    """현재 게임 통계 조회"""
    game = get_game()
    return jsonify(game.get_stats())


@app.route("/api/reset", methods=["POST"])
def reset():
    """게임 초기화"""
    session.pop("game_data", None)
    return jsonify({"status": "ok", "message": "게임이 초기화되었습니다."})


# ─────────────────────────────────────────
# 실행
# ─────────────────────────────────────────

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
