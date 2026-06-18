import sys
import math
import pygame

# Import theo thứ tự: resources phải được import trước renderer
from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    BOARD_X, BOARD_Y, BOARD_SIZE, CELL_SIZE,
)
import resources          # noqa: F401  — khởi tạo pygame, screen, font, bg_image
from resources import screen
import ai                 # noqa: F401  — gắn minimax/alphabeta/bot_move vào CaroGame
from game_logic import CaroGame
from renderer import (
    draw_menu, draw_difficulty_menu,
    draw_board, draw_status,
    draw_game_over_popup, draw_confirm_quit,
)


def main():
    """Hàm chạy vòng lặp xử lý chính của trò chơi."""
    game  = CaroGame()
    clock = pygame.time.Clock()

    # ── Định nghĩa các nút bấm ────────────────────────────────────────────────
    btn_y    = BOARD_Y + BOARD_SIZE + 60
    btn_undo = pygame.Rect(SCREEN_WIDTH // 2 - 110, btn_y, 100, 40)
    btn_menu = pygame.Rect(SCREEN_WIDTH // 2 +  10, btn_y, 100, 40)

    btn_yes = pygame.Rect(SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 + 20, 100, 40)
    btn_no  = pygame.Rect(SCREEN_WIDTH // 2 +  20, SCREEN_HEIGHT // 2 + 20, 100, 40)

    btn_replay_popup = pygame.Rect(SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 + 20, 100, 40)
    btn_menu_popup   = pygame.Rect(SCREEN_WIDTH // 2 +  20, SCREEN_HEIGHT // 2 + 20, 100, 40)

    btn_minimax   = pygame.Rect(SCREEN_WIDTH // 2 - 125, SCREEN_HEIGHT // 2 -  40, 250, 50)
    btn_alphabeta = pygame.Rect(SCREEN_WIDTH // 2 - 125, SCREEN_HEIGHT // 2 +  30, 250, 50)
    btn_2p        = pygame.Rect(SCREEN_WIDTH // 2 - 125, SCREEN_HEIGHT // 2 + 100, 250, 50)

    btn_easy = pygame.Rect(SCREEN_WIDTH // 2 - 125, SCREEN_HEIGHT // 2 -  50, 250, 45)
    btn_med  = pygame.Rect(SCREEN_WIDTH // 2 - 125, SCREEN_HEIGHT // 2 +   5, 250, 45)
    btn_hard = pygame.Rect(SCREEN_WIDTH // 2 - 125, SCREEN_HEIGHT // 2 +  60, 250, 45)
    btn_back = pygame.Rect(SCREEN_WIDTH // 2 - 125, SCREEN_HEIGHT // 2 + 125, 250, 40)

    # ── Vòng lặp chính ────────────────────────────────────────────────────────
    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()

        # ── Xử lý sự kiện ─────────────────────────────────────────────────────
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                if game.state == 'MENU':
                    if btn_minimax.collidepoint(event.pos):
                        game.game_mode = 1
                        game.ai_type   = 'Minimax'
                        game.state     = 'DIFFICULTY'
                    elif btn_alphabeta.collidepoint(event.pos):
                        game.game_mode = 1
                        game.ai_type   = 'Alpha-Beta'
                        game.state     = 'DIFFICULTY'
                    elif btn_2p.collidepoint(event.pos):
                        game.game_mode = 2
                        game.reset_game()
                        game.state = 'PLAYING'

                elif game.state == 'DIFFICULTY':
                    if btn_easy.collidepoint(event.pos):
                        game.ai_depth = 2
                        game.reset_game()
                        game.state = 'PLAYING'
                    elif btn_med.collidepoint(event.pos):
                        game.ai_depth = 3
                        game.reset_game()
                        game.state = 'PLAYING'
                    elif btn_hard.collidepoint(event.pos):
                        game.ai_depth = 4
                        game.reset_game()
                        game.state = 'PLAYING'
                    elif btn_back.collidepoint(event.pos):
                        game.state = 'MENU'

                elif game.state == 'PLAYING':
                    if btn_menu.collidepoint(event.pos):
                        game.state = 'CONFIRM_QUIT'
                    elif (len(game.history) > 0
                          and game.undo_count < 2
                          and not getattr(game, 'just_undid', False)
                          and btn_undo.collidepoint(event.pos)):
                        game.undo()
                    elif game.game_over:
                        if pygame.time.get_ticks() - getattr(game, 'game_over_time', 0) > 1500:
                            if btn_replay_popup.collidepoint(event.pos):
                                game.reset_game()
                            elif btn_menu_popup.collidepoint(event.pos):
                                game.state = 'MENU'
                    else:
                        if game.game_mode == 2 or (game.game_mode == 1 and game.current_player == 'X'):
                            x, y = event.pos
                            if BOARD_X <= x < BOARD_X + BOARD_SIZE and BOARD_Y <= y < BOARD_Y + BOARD_SIZE:
                                c = (x - BOARD_X) // CELL_SIZE
                                r = (y - BOARD_Y) // CELL_SIZE
                                if game.make_move(r, c, game.current_player):
                                    if game.check_win(r, c, game.current_player):
                                        game.game_over      = True
                                        game.winner         = game.current_player
                                        game.winning_line   = game.get_winning_line(game.current_player)
                                        game.game_over_time = pygame.time.get_ticks()
                                    elif game.is_board_full():
                                        game.game_over      = True
                                        game.winner         = 'Draw'
                                        game.game_over_time = pygame.time.get_ticks()
                                    else:
                                        game.current_player = 'O' if game.current_player == 'X' else 'X'

                elif game.state == 'CONFIRM_QUIT':
                    if btn_yes.collidepoint(event.pos):
                        game.state = 'MENU'
                    elif btn_no.collidepoint(event.pos):
                        game.state = 'PLAYING'

        # ── Vẽ khung hình ─────────────────────────────────────────────────────
        if game.state == 'MENU':
            draw_menu(mouse_pos, btn_minimax, btn_alphabeta, btn_2p)

        elif game.state == 'DIFFICULTY':
            draw_difficulty_menu(mouse_pos, btn_easy, btn_med, btn_hard, btn_back)

        else:
            draw_board(game)
            draw_status(game, btn_undo, btn_menu, mouse_pos)

            if game.state == 'CONFIRM_QUIT':
                draw_confirm_quit(mouse_pos, btn_yes, btn_no)

            if game.game_over and game.state == 'PLAYING':
                if pygame.time.get_ticks() - getattr(game, 'game_over_time', 0) > 1500:
                    draw_game_over_popup(game, mouse_pos, btn_replay_popup, btn_menu_popup)

            # ── Lượt của bot ──────────────────────────────────────────────────
            if (game.game_mode == 1
                    and not game.game_over
                    and game.current_player == 'O'
                    and game.state == 'PLAYING'):
                pygame.display.flip()
                pygame.time.delay(500)
                move = game.bot_move()
                if move:
                    r, c = move
                    game.make_move(r, c, 'O')
                    if game.check_win(r, c, 'O'):
                        game.game_over      = True
                        game.winner         = 'O'
                        game.winning_line   = game.get_winning_line('O')
                        game.game_over_time = pygame.time.get_ticks()
                    elif game.is_board_full():
                        game.game_over      = True
                        game.winner         = 'Draw'
                        game.game_over_time = pygame.time.get_ticks()
                    else:
                        game.current_player = 'X'

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
