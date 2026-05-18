# =============================================
# rl_agent.py - 강화학습 에이전트
# Q-table 관리, 행동 선택, Q값 업데이트를 담당합니다.
# =============================================

import random
import pickle
import os
from collections import defaultdict
from settings import (
    ALPHA, GAMMA, EPSILON_START, EPSILON_MIN, EPSILON_DECAY,
    ACTIONS
)


class QLearningAgent:
    """
    Q-Learning 에이전트
    - Q-table: {state: [Q값_UP, Q값_DOWN, Q값_LEFT, Q값_RIGHT]}
    - ε-greedy 정책으로 행동 선택
    """

    def __init__(self):
        # defaultdict: 처음 보는 상태는 자동으로 0으로 초기화
        self.q_table = defaultdict(lambda: [0.0] * len(ACTIONS))
        self.epsilon = EPSILON_START
        self.alpha   = ALPHA
        self.gamma   = GAMMA
        self.total_reward = 0

    def get_action(self, state, training=True):
        """
        ε-greedy 정책으로 행동 선택
        - training=True: 탐험(random) vs 활용(최적행동)
        - training=False: 항상 최적 행동 선택
        """
        if training and random.random() < self.epsilon:
            return random.choice(ACTIONS)  # 탐험: 무작위 행동
        else:
            q_values = self.q_table[state]
            return q_values.index(max(q_values))  # 활용: Q값 최대 행동

    def update(self, state, action, reward, next_state, done):
        """
        벨만 방정식으로 Q값 업데이트
        Q(s,a) ← Q(s,a) + α [ r + γ·max Q(s',a') - Q(s,a) ]
        """
        current_q = self.q_table[state][action]

        if done:
            target = reward  # 종료 상태는 미래 보상 없음
        else:
            max_next_q = max(self.q_table[next_state])
            target = reward + self.gamma * max_next_q

        # Q값 업데이트
        self.q_table[state][action] += self.alpha * (target - current_q)
        self.total_reward += reward

    def decay_epsilon(self):
        """에피소드 종료 시 탐험율 감소"""
        self.epsilon = max(EPSILON_MIN, self.epsilon * EPSILON_DECAY)

    def reset_episode_reward(self):
        self.total_reward = 0

    def save(self, path="q_table.pkl"):
        """Q-table을 파일로 저장"""
        with open(path, "wb") as f:
            pickle.dump(dict(self.q_table), f)
        print(f"[저장] Q-table 저장 완료: {path}")

    def load(self, path="q_table.pkl"):
        """저장된 Q-table 불러오기"""
        if os.path.exists(path):
            with open(path, "rb") as f:
                data = pickle.load(f)
            self.q_table = defaultdict(lambda: [0.0] * len(ACTIONS), data)
            self.epsilon = EPSILON_MIN  # 불러올 땐 탐험 최소화
            print(f"[불러오기] Q-table 로드 완료: {path}")
        else:
            print(f"[경고] {path} 파일이 없습니다. 새로 학습을 시작합니다.")

    def get_epsilon(self):
        return self.epsilon

    def get_q_table_size(self):
        return len(self.q_table)
