# =============================================
# rl_agent.py - Q-Learning 에이전트
# =============================================

import random
import pickle
import os
from collections import defaultdict
from settings import (
    QL_ALPHA, QL_GAMMA,
    QL_EPSILON_START, QL_EPSILON_MIN, QL_EPSILON_DECAY,
    ACTIONS
)


class QLearningAgent:
    """
    Q-Learning 에이전트
    - Q-table: 딕셔너리 {state튜플: [Q_UP, Q_DOWN, Q_LEFT, Q_RIGHT]}
    - 상태: 11개 이진값 튜플 (env.py의 _get_ql_state)
    """

    def __init__(self):
        self.q_table = defaultdict(lambda: [0.0] * len(ACTIONS))
        self.epsilon = QL_EPSILON_START
        self.alpha   = QL_ALPHA
        self.gamma   = QL_GAMMA
        self.total_reward = 0

    def get_action(self, state, training=True):
        """ε-greedy 행동 선택"""
        if training and random.random() < self.epsilon:
            return random.choice(ACTIONS)
        return self.q_table[state].index(max(self.q_table[state]))

    def update(self, state, action, reward, next_state, done):
        """벨만 방정식으로 Q값 업데이트"""
        current_q = self.q_table[state][action]
        if done:
            target = reward
        else:
            target = reward + self.gamma * max(self.q_table[next_state])
        self.q_table[state][action] += self.alpha * (target - current_q)
        self.total_reward += reward

    def decay_epsilon(self):
        self.epsilon = max(QL_EPSILON_MIN, self.epsilon * QL_EPSILON_DECAY)

    def reset_episode_reward(self):
        self.total_reward = 0

    def save(self, path="q_table.pkl"):
        with open(path, "wb") as f:
            pickle.dump(dict(self.q_table), f)

    def load(self, path="q_table.pkl"):
        if os.path.exists(path):
            with open(path, "rb") as f:
                data = pickle.load(f)
            self.q_table = defaultdict(lambda: [0.0] * len(ACTIONS), data)
            self.epsilon = QL_EPSILON_MIN

    def get_epsilon(self):      return self.epsilon
    def get_q_table_size(self): return len(self.q_table)
