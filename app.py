from __future__ import annotations

import secrets
from typing import Any

from flask import Flask, jsonify, render_template, request, session

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)


def _init_game() -> None:
    session["target"] = secrets.randbelow(99) + 101
    session["attempts"] = 0
    session["history"] = []
    session["active"] = True


def _game_state(message: str, status: str) -> dict[str, Any]:
    return {
        "status": status,
        "message": message,
        "attempts": session.get("attempts", 0),
        "history": session.get("history", []),
        "active": session.get("active", False),
    }


@app.get("/")
def index() -> str:
    return render_template("index.html")


@app.post("/api/start")
def start_game() -> tuple[str, int] | tuple[dict[str, Any], int]:
    _init_game()
    return jsonify(_game_state("游戏已开始，猜一个 101~199 的数字。", "started")), 200


@app.post("/api/reset")
def reset_game() -> tuple[dict[str, Any], int]:
    _init_game()
    return jsonify(_game_state("已重置，重新开始猜吧！", "reset")), 200


@app.post("/api/guess")
def guess() -> tuple[dict[str, Any], int]:
    if not session.get("active"):
        return (
            jsonify(_game_state("游戏未开始或已结束，请点击开始/重来。", "inactive")),
            400,
        )

    data = request.get_json(silent=True) or {}
    raw_guess = data.get("guess")

    if raw_guess is None:
        return jsonify(_game_state("请输入一个数字。", "invalid")), 400

    try:
        guess_value = int(raw_guess)
    except (TypeError, ValueError):
        return jsonify(_game_state("请输入有效的整数。", "invalid")), 400

    if not 101 <= guess_value <= 199:
        return jsonify(_game_state("数字需要在 101~199 之间。", "invalid")), 400

    session["attempts"] = session.get("attempts", 0) + 1
    history = session.get("history", [])
    history.append(guess_value)
    session["history"] = history

    target = session.get("target", 0)
    if guess_value < target:
        return jsonify(_game_state("太小", "low")), 200
    if guess_value > target:
        return jsonify(_game_state("太大", "high")), 200

    session["active"] = False
    return jsonify(_game_state("猜对了！", "correct")), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
