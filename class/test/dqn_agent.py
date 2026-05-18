# =============================================
# dqn_agent.py - DQN 에이전트
#
# Q-learning과의 차이:
# - Q-table(딕셔너리) 대신 신경망으로 Q값 계산
# - 경험 리플레이 버퍼로 과거 경험을 재활용
# - 타겟 네트워크로 학습 안정화
# =============================================

import random
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from collections import deque
from settings import (
    DQN_GAMMA, DQN_LR,
    DQN_EPSILON_START, DQN_EPSILON_MIN, DQN_EPSILON_DECAY,
    DQN_BATCH_SIZE, DQN_MEMORY_SIZE, DQN_TARGET_UPDATE,
    DQN_STATE_SIZE, DQN_ACTION_SIZE,
    ACTIONS
)


# ─── 신경망 구조 ──────────────────────────────────────
class QNetwork(nn.Module):
    """
    Q값을 근사하는 신경망
    입력: 상태(16개 실수) → 출력: 각 행동의 Q값(4개)

    Q-learning:  상태 → 테이블 조회 → Q값
    DQN:         상태 → 신경망 계산 → Q값  ← 이 차이!
    """
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(DQN_STATE_SIZE, 256),  # 입력층 → 은닉층1
            nn.ReLU(),
            nn.Linear(256, 128),             # 은닉층1 → 은닉층2
            nn.ReLU(),
            nn.Linear(128, DQN_ACTION_SIZE)  # 은닉층2 → 출력층(Q값)
        )

    def forward(self, x):
        return self.net(x)


# ─── 경험 리플레이 버퍼 ───────────────────────────────
class ReplayBuffer:
    """
    과거 경험 (상태, 행동, 보상, 다음상태, 종료여부) 저장
    - Q-learning: 경험을 즉시 쓰고 버림
    - DQN: 버퍼에 쌓아두고 무작위로 꺼내 재활용
           → 연속된 경험의 상관관계를 끊어 학습 안정화
    """
    def __init__(self, max_size=DQN_MEMORY_SIZE):
        self.buffer = deque(maxlen=max_size)

    def push(self, state, action, reward, next_state, done):
        self.buffer.append((state, action, reward, next_state, done))

    def sample(self, batch_size):
        return random.sample(self.buffer, batch_size)

    def __len__(self):
        return len(self.buffer)


# ─── DQN 에이전트 ─────────────────────────────────────
class DQNAgent:
    """
    DQN 에이전트
    - 메인 네트워크: Q값 계산 및 학습
    - 타겟 네트워크: 안정적인 목표값 계산용 (주기적으로 메인 복사)
    """

    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # 메인 네트워크 (학습)
        self.main_net   = QNetwork().to(self.device)
        # 타겟 네트워크 (목표값 계산, 주기적 업데이트)
        self.target_net = QNetwork().to(self.device)
        self.target_net.load_state_dict(self.main_net.state_dict())
        self.target_net.eval()

        self.optimizer = optim.Adam(self.main_net.parameters(), lr=DQN_LR)
        self.memory    = ReplayBuffer()
        self.epsilon   = DQN_EPSILON_START
        self.gamma     = DQN_GAMMA
        self.steps     = 0
        self.total_reward = 0

    def get_action(self, state, training=True):
        """ε-greedy 행동 선택"""
        if training and random.random() < self.epsilon:
            return random.choice(ACTIONS)

        # 신경망으로 Q값 계산 → 최대값 행동 선택
        state_tensor = torch.FloatTensor(state).unsqueeze(0).to(self.device)
        with torch.no_grad():
            q_values = self.main_net(state_tensor)
        return q_values.argmax().item()

    def remember(self, state, action, reward, next_state, done):
        """경험 버퍼에 저장"""
        self.memory.push(state, action, reward, next_state, done)
        self.total_reward += reward

    def learn(self):
        """
        버퍼에서 무작위 샘플 꺼내 신경망 학습
        - 버퍼가 batch_size보다 작으면 학습 안 함
        """
        if len(self.memory) < DQN_BATCH_SIZE:
            return

        batch = self.memory.sample(DQN_BATCH_SIZE)
        states, actions, rewards, next_states, dones = zip(*batch)

        # numpy → tensor 변환
        states      = torch.FloatTensor(np.array(states)).to(self.device)
        actions     = torch.LongTensor(actions).to(self.device)
        rewards     = torch.FloatTensor(rewards).to(self.device)
        next_states = torch.FloatTensor(np.array(next_states)).to(self.device)
        dones       = torch.FloatTensor(dones).to(self.device)

        # 현재 Q값: 메인 네트워크로 계산
        current_q = self.main_net(states).gather(1, actions.unsqueeze(1)).squeeze(1)

        # 목표 Q값: 타겟 네트워크로 계산 (벨만 방정식)
        with torch.no_grad():
            max_next_q = self.target_net(next_states).max(1)[0]
            target_q   = rewards + self.gamma * max_next_q * (1 - dones)

        # 손실 계산 및 역전파
        loss = nn.MSELoss()(current_q, target_q)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        # 타겟 네트워크 주기적 업데이트
        self.steps += 1
        if self.steps % DQN_TARGET_UPDATE == 0:
            self.target_net.load_state_dict(self.main_net.state_dict())

    def decay_epsilon(self):
        self.epsilon = max(DQN_EPSILON_MIN, self.epsilon * DQN_EPSILON_DECAY)

    def reset_episode_reward(self):
        self.total_reward = 0

    def save(self, path="dqn_model.pth"):
        torch.save(self.main_net.state_dict(), path)
        print(f"[저장] DQN 모델 저장: {path}")

    def load(self, path="dqn_model.pth"):
        import os
        if os.path.exists(path):
            self.main_net.load_state_dict(torch.load(path, map_location=self.device))
            self.target_net.load_state_dict(self.main_net.state_dict())
            self.epsilon = DQN_EPSILON_MIN
            print(f"[불러오기] DQN 모델 로드: {path}")

    def get_epsilon(self):       return self.epsilon
    def get_memory_size(self):   return len(self.memory)
