# =============================================
# main.py - 실행 진입점
# 시작 시 Q-learning / DQN 선택 메뉴 표시
# =============================================

import sys
import pygame
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from env import SnakeEnv
from rl_agent import QLearningAgent
from dqn_agent import DQNAgent
from settings import *


# ─── 시각화 공통 함수 ─────────────────────────────────

def draw_grid(surface):
    for x in range(0, SCREEN_WIDTH, GRID_SIZE):
        pygame.draw.line(surface, COLOR_GRID, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
        pygame.draw.line(surface, COLOR_GRID, (0, y), (SCREEN_WIDTH, y))

def draw_snake(surface, snake):
    for i, (x, y) in enumerate(snake.body):
        color = COLOR_SNAKE_HEAD if i == 0 else COLOR_SNAKE
        rect = pygame.Rect(x*GRID_SIZE+1, y*GRID_SIZE+1, GRID_SIZE-2, GRID_SIZE-2)
        pygame.draw.rect(surface, color, rect, border_radius=4)

def draw_food(surface, food):
    fx, fy = food.get_position()
    cx = fx * GRID_SIZE + GRID_SIZE // 2
    cy = fy * GRID_SIZE + GRID_SIZE // 2
    pygame.draw.circle(surface, COLOR_FOOD, (cx, cy), GRID_SIZE//2-2)

def render_frame(surface, font, env, agent, episode, mode):
    surface.fill(COLOR_BG)
    draw_grid(surface)
    draw_snake(surface, env.get_snake())
    draw_food(surface, env.get_food())

    # UI 정보
    ui_rect = pygame.Rect(0, SCREEN_HEIGHT, SCREEN_WIDTH, 60)
    pygame.draw.rect(surface, COLOR_UI_BG, ui_rect)

    episodes = DQN_EPISODES if mode == 'dqn' else QL_EPISODES
    label    = "DQN" if mode == 'dqn' else "Q-Learning"
    color    = COLOR_DQN if mode == 'dqn' else COLOR_QL

    # 에피소드별 정보
    if mode == 'dqn':
        info2 = f"Memory: {agent.get_memory_size()}"
    else:
        info2 = f"Q-states: {agent.get_q_table_size()}"

    texts = [
        (f"[{label}]",            color),
        (f"EP: {episode}/{episodes}", COLOR_TEXT),
        (f"Score: {env.get_score()}",  COLOR_TEXT),
        (f"ε: {agent.get_epsilon():.3f}", COLOR_TEXT),
        (info2,                    COLOR_TEXT),
    ]
    for i, (text, col) in enumerate(texts):
        surf = font.render(text, True, col)
        surface.blit(surf, (5 + i * 95, SCREEN_HEIGHT + 10))

    pygame.display.flip()

def save_graph(rewards, scores, mode):
    label = "DQN" if mode == 'dqn' else "Q-Learning"
    color_r = '#5090ff' if mode == 'dqn' else '#ffb432'
    color_a = '#90c8ff' if mode == 'dqn' else '#ffd882'

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    fig.patch.set_facecolor('#0f0f19')

    for ax, data, title, col in [
        (ax1, rewards, f'[{label}] 에피소드별 누적 보상', color_r),
        (ax2, scores,  f'[{label}] 에피소드별 점수',     color_r),
    ]:
        ax.set_facecolor('#14141e')
        ax.plot(data, color=col, alpha=0.4, linewidth=0.8)
        window = 50
        if len(data) >= window:
            avg = [sum(data[max(0,i-window):i+1])/min(i+1,window) for i in range(len(data))]
            ax.plot(avg, color=color_a, linewidth=2, label=f'{window}회 이동평균')
        ax.set_title(title, color='white', fontsize=12)
        ax.tick_params(colors='#aaaaaa')
        ax.legend(facecolor='#1e1e2e', labelcolor='white')
        for spine in ['top','right']:
            ax.spines[spine].set_visible(False)
        for spine in ['bottom','left']:
            ax.spines[spine].set_color('#444')

    plt.tight_layout()
    fname = f'result_{mode}.png'
    plt.savefig(fname, dpi=120, bbox_inches='tight', facecolor='#0f0f19')
    plt.close()
    print(f"[결과] 그래프 저장: {fname}")


# ─── 시작 메뉴 ───────────────────────────────────────

def show_menu(surface, clock):
    """
    Q-learning / DQN 선택 메뉴
    ↑↓ 또는 1/2 키로 선택, Enter로 확정
    """
    title_font  = pygame.font.SysFont("consolas", 28, bold=True)
    option_font = pygame.font.SysFont("consolas", 20)
    desc_font   = pygame.font.SysFont("consolas", 13)

    selected = 0   # 0 = Q-learning, 1 = DQN
    options = [
        {
            "label": "1. Q-Learning",
            "color": COLOR_QL,
            "desc": [
                "- 상태: 11개 이진값 (2^11 = 2048가지)",
                "- Q-table: 딕셔너리 (288 × 4 실제 사용)",
                "- 주변 3방향 위험 감지 (1칸 앞)",
                "- 학습 빠름, 긴 뱀에서 한계 있음",
            ]
        },
        {
            "label": "2. DQN (Deep Q-Network)",
            "color": COLOR_DQN,
            "desc": [
                "- 상태: 16개 실수값 (주변 8칸 위험 감지)",
                "- 신경망: 16 → 256 → 128 → 4",
                "- 경험 리플레이 버퍼 (100,000개)",
                "- 타겟 네트워크로 학습 안정화",
            ]
        },
    ]

    while True:
        surface.fill(COLOR_MENU_BG)

        # 제목
        title = title_font.render("🐍 Snake Reinforcement Learning", True, COLOR_HIGHLIGHT)
        surface.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 40))

        sub = option_font.render("학습 방법을 선택하세요  [↑↓ / 1 / 2]  Enter로 시작", True, COLOR_TEXT)
        surface.blit(sub, (SCREEN_WIDTH//2 - sub.get_width()//2, 85))

        # 선택지
        for i, opt in enumerate(options):
            y_base = 140 + i * 160
            is_sel = (i == selected)

            # 선택된 항목 배경
            if is_sel:
                bg = pygame.Surface((SCREEN_WIDTH - 40, 140), pygame.SRCALPHA)
                bg.fill((*opt["color"], 30))
                surface.blit(bg, (20, y_base - 10))
                pygame.draw.rect(surface, opt["color"],
                                 (20, y_base-10, SCREEN_WIDTH-40, 140), 2, border_radius=8)

            # 라벨
            prefix = "▶ " if is_sel else "  "
            label_surf = option_font.render(prefix + opt["label"], True,
                                            opt["color"] if is_sel else COLOR_TEXT)
            surface.blit(label_surf, (40, y_base))

            # 설명
            for j, line in enumerate(opt["desc"]):
                col = COLOR_TEXT if is_sel else (100, 100, 100)
                d = desc_font.render(line, True, col)
                surface.blit(d, (60, y_base + 30 + j * 22))

        # 하단 안내
        hint = desc_font.render("학습 중 창 닫으면 현재까지 결과 저장됨", True, (80, 80, 80))
        surface.blit(hint, (SCREEN_WIDTH//2 - hint.get_width()//2, SCREEN_HEIGHT + 30))

        pygame.display.flip()
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP, pygame.K_w):
                    selected = (selected - 1) % 2
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    selected = (selected + 1) % 2
                elif event.key == pygame.K_1:
                    return 'ql'
                elif event.key == pygame.K_2:
                    return 'dqn'
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    return 'ql' if selected == 0 else 'dqn'


# ─── 학습 루프 ────────────────────────────────────────

def run_training(surface, clock, font, mode):
    """Q-learning / DQN 공통 학습 루프"""

    episodes  = DQN_EPISODES  if mode == 'dqn' else QL_EPISODES
    max_steps = DQN_MAX_STEPS if mode == 'dqn' else QL_MAX_STEPS
    show_every= DQN_SHOW_EVERY if mode == 'dqn' else QL_SHOW_EVERY

    env   = SnakeEnv(mode=mode)
    agent = DQNAgent() if mode == 'dqn' else QLearningAgent()

    all_rewards, all_scores = [], []
    label = "DQN" if mode == 'dqn' else "Q-Learning"

    print(f"\n{'='*50}")
    print(f"  [{label}] 학습 시작!  총 {episodes} 에피소드")
    print(f"{'='*50}\n")

    for episode in range(1, episodes + 1):

        # 창 닫기 체크
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                save_graph(all_rewards, all_scores, mode)
                agent.save()
                sys.exit()

        state = env.reset()
        agent.reset_episode_reward()
        show = (episode % show_every == 0)

        for step in range(max_steps):
            action = agent.get_action(state, training=True)
            next_state, reward, done = env.step(action)

            # ── 에이전트별 학습 방식 다름 ──
            if mode == 'dqn':
                agent.remember(state, action, reward, next_state, done)
                agent.learn()   # 버퍼에서 샘플링하여 신경망 학습
            else:
                agent.update(state, action, reward, next_state, done)

            state = next_state

            if show:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        save_graph(all_rewards, all_scores, mode)
                        agent.save()
                        sys.exit()
                render_frame(surface, font, env, agent, episode, mode)
                clock.tick(FPS_DISPLAY)

            if done:
                break

        agent.decay_epsilon()
        all_rewards.append(agent.total_reward)
        all_scores.append(env.get_score())

        if not show:
            surface.fill(COLOR_BG)
            info = font.render(
                f"[{label}] Training... EP {episode}/{episodes}  "
                f"Best: {max(all_scores)}  "
                f"ε: {agent.get_epsilon():.3f}",
                True, COLOR_DQN if mode == 'dqn' else COLOR_QL
            )
            surface.blit(info, (10, SCREEN_HEIGHT//2))
            pygame.display.flip()
            clock.tick(60)

        if episode % 100 == 0:
            recent = all_scores[-100:]
            print(f"[EP {episode:4d}]  "
                  f"avg: {sum(recent)/len(recent):.2f}  "
                  f"max: {max(recent)}  "
                  f"ε: {agent.get_epsilon():.4f}")

    # 학습 완료
    print(f"\n{'='*50}")
    print(f"  [{label}] 학습 완료!")
    print(f"  최고 점수: {max(all_scores)}")
    print(f"  마지막 100회 평균: {sum(all_scores[-100:])/100:.2f}")
    print(f"{'='*50}\n")

    agent.save()
    save_graph(all_rewards, all_scores, mode)


# ─── 메인 ─────────────────────────────────────────────

def main():
    pygame.init()
    surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT + 60))
    pygame.display.set_caption("🐍 Snake RL - Q-Learning & DQN")
    clock = pygame.time.Clock()
    font  = pygame.font.SysFont("consolas", 12)

    # 메뉴에서 모드 선택
    mode = show_menu(surface, clock)

    pygame.display.set_caption(
        f"🐍 Snake RL - {'DQN' if mode == 'dqn' else 'Q-Learning'}"
    )

    # 선택된 모드로 학습 시작
    run_training(surface, clock, font, mode)

    pygame.quit()


if __name__ == "__main__":
    main()
