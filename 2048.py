import pygame
import random

# 初始化Pygame
pygame.init()

# 定义颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
COLORS = {
    0: (205, 193, 180),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46)
}

# 设置窗口大小
WINDOW_SIZE = (440, 440)

# 设置内边距和方块大小
PADDING = 10
BLOCK_SIZE = 90
BLOCK_GAP = 10

# 初始化窗口
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("2048")

# 设置字体
font = pygame.font.Font(None, 36)


# 游戏状态
class GameState:
    PLAYING = 0
    GAME_OVER = 1


# 创建游戏状态对象
game_state = GameState.PLAYING

# 游戏结束界面按钮颜色
BUTTON_COLOR = (200, 200, 200)
HOVER_COLOR = (150, 150, 150)


# 创建棋盘
def create_board():
    return [[0] * 4 for _ in range(4)]


# 在随机空白位置生成一个新的数字2或4
def place_new_tile(board):
    empty_tiles = [(i, j) for i in range(4) for j in range(4) if board[i][j] == 0]
    if empty_tiles:
        row, col = random.choice(empty_tiles)
        numbers = [1, 2]
        board[row][col] = random.choice([2 * random.choice(numbers), 4 * random.choice(numbers)])


# 绘制游戏结束界面
def draw_end_screen(score, success=False):
    screen.fill(WHITE)

    if success:
        # 绘制 "Congratulations!" 文本
        congrats_text = font.render("Congratulations!", True, BLACK)
        congrats_text_rect = congrats_text.get_rect(center=(WINDOW_SIZE[0] / 2, WINDOW_SIZE[1] / 2 - 80))
        screen.blit(congrats_text, congrats_text_rect)

        # 绘制 "You Win!" 文本
        win_text = font.render("You Win!", True, BLACK)
        win_text_rect = win_text.get_rect(center=(WINDOW_SIZE[0] / 2, WINDOW_SIZE[1] / 2 - 40))
        screen.blit(win_text, win_text_rect)

    else:
        # 绘制 "Game Over" 文本
        game_over_text = font.render("Game Over!", True, BLACK)
        game_over_text_rect = game_over_text.get_rect(center=(WINDOW_SIZE[0] / 2, WINDOW_SIZE[1] / 2 - 40))
        screen.blit(game_over_text, game_over_text_rect)

    # 绘制得分文本
    score_text = font.render(f"Score: {score}", True, BLACK)
    score_text_rect = score_text.get_rect(center=(WINDOW_SIZE[0] / 2, WINDOW_SIZE[1] / 2))
    screen.blit(score_text, score_text_rect)

    # 绘制重新开始按钮
    restart_button = font.render("Restart", True, BLACK)
    restart_rect = restart_button.get_rect(center=(WINDOW_SIZE[0] / 2 - 70, WINDOW_SIZE[1] / 2 + 60))
    screen.blit(restart_button, restart_rect)

    # 绘制退出游戏按钮
    quit_button = font.render("Quit", True, BLACK)
    quit_rect = quit_button.get_rect(center=(WINDOW_SIZE[0] / 2 + 70, WINDOW_SIZE[1] / 2 + 60))
    screen.blit(quit_button, quit_rect)

    pygame.display.flip()

    # 返回按钮的位置信息
    return restart_rect, quit_rect


# 绘制棋盘
def draw_board(board):
    screen.fill(WHITE)
    pygame.draw.rect(screen, DARK_GRAY, (
        PADDING, PADDING, 4 * BLOCK_SIZE + 3 * BLOCK_GAP + 2 * PADDING, 4 * BLOCK_SIZE + 3 * BLOCK_GAP + 2 * PADDING))
    for row in range(4):
        for col in range(4):
            draw_block(row, col, board[row][col])

            # 检查是否出现2048
            if board[row][col] == 2048:
                success_rect = draw_end_screen(calculate_score(board), success=True)
                pygame.display.flip()
                return success_rect  # 返回成功界面按钮位置信息

    pygame.display.flip()


# 绘制单个方块
def draw_block(row, col, value):
    color = COLORS[value]
    x = PADDING + col * (BLOCK_SIZE + BLOCK_GAP) + PADDING
    y = PADDING + row * (BLOCK_SIZE + BLOCK_GAP) + PADDING
    pygame.draw.rect(screen, color, (x, y, BLOCK_SIZE, BLOCK_SIZE))
    if value != 0:
        text = font.render(str(value), True, BLACK)
        text_rect = text.get_rect(center=(x + BLOCK_SIZE / 2, y + BLOCK_SIZE / 2))
        screen.blit(text, text_rect)


# 判断游戏是否结束
def is_game_over(board):
    for row in board:
        if 0 in row:
            return False
        for j in range(3):
            if row[j] == row[j + 1]:
                return False
    return True


# 计算总得分
def calculate_score(board):
    return sum(sum(row) for row in board)


# 向左移动
def move_left(board):
    score = 0
    for row in board:
        # 移动数字
        for i in range(1, 4):
            for j in range(i, 0, -1):
                if row[j - 1] == 0:
                    row[j - 1] = row[j]
                    row[j] = 0
                elif row[j - 1] == row[j]:
                    row[j - 1] *= 2
                    score += row[j - 1]
                    row[j] = 0
                else:
                    break
    place_new_tile(board)
    return score


# 向右移动
def move_right(board):
    score = 0
    for row in board:
        # 移动数字
        for i in range(2, -1, -1):
            for j in range(i, 3):
                if row[j + 1] == 0:
                    row[j + 1] = row[j]
                    row[j] = 0
                elif row[j + 1] == row[j]:
                    row[j + 1] *= 2
                    score += row[j + 1]
                    row[j] = 0
                else:
                    break
    place_new_tile(board)
    return score


# 向上移动
def move_up(board):
    score = 0
    for col in range(4):
        # 移动数字
        for i in range(1, 4):
            for j in range(i, 0, -1):
                if board[j - 1][col] == 0:
                    board[j - 1][col] = board[j][col]
                    board[j][col] = 0
                elif board[j - 1][col] == board[j][col]:
                    board[j - 1][col] *= 2
                    score += board[j - 1][col]
                    board[j][col] = 0
                else:
                    break
    place_new_tile(board)
    return score


# 向下移动
def move_down(board):
    score = 0
    for col in range(4):
        # 移动数字
        for i in range(2, -1, -1):
            for j in range(i, 3):
                if board[j + 1][col] == 0:
                    board[j + 1][col] = board[j][col]
                    board[j][col] = 0
                elif board[j + 1][col] == board[j][col]:
                    board[j + 1][col] *= 2
                    score += board[j + 1][col]
                    board[j][col] = 0
                else:
                    break
    place_new_tile(board)
    return score


# 游戏主循环
def main():
    global game_state
    board = create_board()
    place_new_tile(board)
    draw_board(board)
    score = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if game_state == GameState.PLAYING:
                    if event.key == pygame.K_LEFT:
                        score += move_left(board)
                    elif event.key == pygame.K_RIGHT:
                        score += move_right(board)
                    elif event.key == pygame.K_UP:
                        score += move_up(board)
                    elif event.key == pygame.K_DOWN:
                        score += move_down(board)
                    success_rect = draw_board(board)  # 检查2048并更新游戏界面
                    if success_rect:  # 如果出现2048，显示成功界面并等待用户操作
                        game_state = GameState.GAME_OVER
                        restart_rect, quit_rect = success_rect
                        pygame.display.flip()
                        continue
                    if is_game_over(board):
                        game_state = GameState.GAME_OVER
                        restart_rect, quit_rect = draw_end_screen(score)
                elif game_state == GameState.GAME_OVER:
                    if event.key == pygame.K_r:  # 重新开始游戏
                        board = create_board()
                        place_new_tile(board)
                        draw_board(board)
                        score = 0
                        game_state = GameState.PLAYING
                    elif event.key == pygame.K_q:  # 退出游戏
                        running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 左键点击
                    mouse_pos = event.pos
                    if game_state == GameState.GAME_OVER:
                        if restart_rect.collidepoint(mouse_pos):  # 点击了重新开始按钮
                            board = create_board()
                            place_new_tile(board)
                            draw_board(board)
                            score = 0
                            game_state = GameState.PLAYING
                        elif quit_rect.collidepoint(mouse_pos):  # 点击了退出按钮
                            running = False
    pygame.quit()


if __name__ == "__main__":
    main()
