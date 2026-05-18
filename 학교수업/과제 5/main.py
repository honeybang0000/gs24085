# =============================================
# main.py - 프로그램 실행 진입점
# 학습 루프 제어, pygame 시각화, 결과 그래프 출력
# =============================================

import sys
import pygame
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # GUI 없는 환경 대비

from env import SnakeEnv
from rl_agent import QLearningAgent
from settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, GRID_SIZE, GRID_COUNT,
    FPS_TRAINING, FPS_DISPLAY,
    EPISODES, MAX_STEPS, SHOW_EVERY,
    COLOR_BG, COLOR_GRID, COLOR_SNAKE, COLOR_SNAKE_HEAD,
    COLOR_FOOD, COLOR_TEXT, COLOR_UI_BG,
    UP, DOWN, LEFT, RIGHT
)


# ─── 시각화 함수들 ───────────────────────────────────────────

def draw_grid(surface):
    """격자 선 그리기"""
    for x in range(0, SCREEN_WIDTH, GRID_SIZE):
        pygame.draw.line(surface, COLOR_GRID, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
        pygame.draw.line(surface, COLOR_GRID, (0, y), (SCREEN_WIDTH, y))


def draw_snake(surface, snake):
    """뱀 그리기 (머리는 밝은색)"""
    for i, (x, y) in enumerate(snake.body):
        color = COLOR_SNAKE_HEAD if i == 0 else COLOR_SNAKE
        rect = pygame.Rect(x * GRID_SIZE + 1, y * GRID_SIZE + 1,
                           GRID_SIZE - 2, GRID_SIZE - 2)
        pygame.draw.rect(surface, color, rect, border_radius=4)


def draw_food(surface, food):
    """먹이 그리기 (원형)"""
    fx, fy = food.get_position()
    cx = fx * GRID_SIZE + GRID_SIZE // 2
    cy = fy * GRID_SIZE + GRID_SIZE // 2
    pygame.draw.circle(surface, COLOR_FOOD, (cx, cy), GRID_SIZE // 2 - 2)


def draw_ui(surface, font, episode, score, epsilon, q_size):
    """상단 정보 UI"""
    ui_rect = pygame.Rect(0, SCREEN_HEIGHT, SCREEN_WIDTH, 60)
    pygame.draw.rect(surface, COLOR_UI_BG, ui_rect)

    texts = [
        f"Episode: {episode}/{EPISODES}",
        f"Score: {score}",
        f"ε: {epsilon:.3f}",
        f"Q-states: {q_size}",
    ]
    for i, text in enumerate(texts):
        surf = font.render(text, True, COLOR_TEXT)
        surface.blit(surf, (10 + i * 130, SCREEN_HEIGHT + 10))


def render_frame(surface, font, env, agent, episode):
    """한 프레임 렌더링"""
    surface.fill(COLOR_BG)
    draw_grid(surface)
    draw_snake(surface, env.get_snake())
    draw_food(surface, env.get_food())
    draw_ui(surface, font, episode, env.get_score(),
            agent.get_epsilon(), agent.get_q_table_size())
    pygame.display.flip()


# ─── 그래프 저장 ─────────────────────────────────────────────

def save_reward_graph(rewards, scores):
    """에피소드별 보상 & 점수 그래프 저장"""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    fig.patch.set_facecolor('#0f0f19')

    # 보상 그래프
    window = 50
    ax1.set_facecolor('#14141e')
    ax1.plot(rewards, color='#32dc64', alpha=0.4, linewidth=0.8, label='보상')
    if len(rewards) >= window:
        moving_avg = [sum(rewards[max(0,i-window):i+1]) /
                      min(i+1, window) for i in range(len(rewards))]
        ax1.plot(moving_avg, color='#64ffaa', linewidth=2, label=f'{window}회 이동평균')
    ax1.set_title('에피소드별 누적 보상', color='white', fontsize=13)
    ax1.set_xlabel('Episode', color='#aaaaaa')
    ax1.set_ylabel('Total Reward', color='#aaaaaa')
    ax1.tick_params(colors='#aaaaaa')
    ax1.legend(facecolor='#1e1e2e', labelcolor='white')
    ax1.spines['bottom'].set_color('#444')
    ax1.spines['left'].set_color('#444')
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)

    # 점수 그래프
    ax2.set_facecolor('#14141e')
    ax2.plot(scores, color='#ff5050', alpha=0.4, linewidth=0.8, label='점수(먹이)')
    if len(scores) >= window:
        score_avg = [sum(scores[max(0,i-window):i+1]) /
                     min(i+1, window) for i in range(len(scores))]
        ax2.plot(score_avg, color='#ffaa64', linewidth=2, label=f'{window}회 이동평균')
    ax2.set_title('에피소드별 점수 (먹이 수)', color='white', fontsize=13)
    ax2.set_xlabel('Episode', color='#aaaaaa')
    ax2.set_ylabel('Score', color='#aaaaaa')
    ax2.tick_params(colors='#aaaaaa')
    ax2.legend(facecolor='#1e1e2e', labelcolor='white')
    ax2.spines['bottom'].set_color('#444')
    ax2.spines['left'].set_color('#444')
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)

    plt.tight_layout()
    plt.savefig('training_result.png', dpi=120, bbox_inches='tight',
                facecolor='#0f0f19')
    plt.close()
    print("[결과] 학습 그래프 저장: training_result.png")


# ─── 메인 학습 루프 ──────────────────────────────────────────

def main():
    # pygame 초기화
    pygame.init()
    surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT + 60))
    pygame.display.set_caption("🐍 Snake Q-Learning")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas", 13)

    env   = SnakeEnv()
    agent = QLearningAgent()

    all_rewards = []
    all_scores  = []

    print(f"\n{'='*50}")
    print(f"  Snake Q-Learning 학습 시작!")
    print(f"  총 에피소드: {EPISODES} | 맵: {GRID_COUNT}x{GRID_COUNT}")
    print(f"{'='*50}\n")

    for episode in range(1, EPISODES + 1):

        # ── pygame 이벤트 처리 ──
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                save_reward_graph(all_rewards, all_scores)
                agent.save()
                sys.exit()

        state = env.reset()
        agent.reset_episode_reward()
        show = (episode % SHOW_EVERY == 0)  # 시각화 여부

        for step in range(MAX_STEPS):
            # 행동 선택
            action = agent.get_action(state, training=True)

            # 환경에서 한 스텝 수행
            next_state, reward, done = env.step(action)

            # Q값 업데이트
            agent.update(state, action, reward, next_state, done)

            state = next_state

            # 시각화 (SHOW_EVERY마다)
            if show:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        save_reward_graph(all_rewards, all_scores)
                        agent.save()
                        sys.exit()
                render_frame(surface, font, env, agent, episode)
                clock.tick(FPS_DISPLAY)

            if done:
                break

        # 에피소드 종료 처리
        agent.decay_epsilon()
        all_rewards.append(agent.total_reward)
        all_scores.append(env.get_score())

        # 빠른 학습 시 배경만 표시
        if not show:
            surface.fill(COLOR_BG)
            info = font.render(
                f"Training... Episode {episode}/{EPISODES}  |  "
                f"Best Score: {max(all_scores):.0f}  |  "
                f"ε: {agent.get_epsilon():.3f}",
                True, COLOR_TEXT
            )
            surface.blit(info, (10, SCREEN_HEIGHT // 2))
            pygame.display.flip()
            clock.tick(FPS_TRAINING)

        # 콘솔 출력
        if episode % 100 == 0:
            recent = all_scores[-100:]
            print(f"[Episode {episode:4d}]  "
                  f"avg_score: {sum(recent)/len(recent):.2f}  "
                  f"max_score: {max(recent)}  "
                  f"ε: {agent.get_epsilon():.4f}  "
                  f"Q-states: {agent.get_q_table_size()}")

    # 학습 완료
    print(f"\n{'='*50}")
    print("  학습 완료!")
    print(f"  최종 최고 점수: {max(all_scores)}")
    print(f"  최종 평균 점수 (마지막 100회): "
          f"{sum(all_scores[-100:])/100:.2f}")
    print(f"{'='*50}\n")

    agent.save()
    save_reward_graph(all_rewards, all_scores)

    pygame.quit()


if __name__ == "__main__":
    main()
