import os
import datetime
import pickle
from random import randint
from vectors import Vector
import pygame

import states, objects, pause_st
from common import WIDTH, GRID, clock, no_joystick, joy, show_fps, switch_state, read_all_controls
from engine.room import Room


def save_best_score(score):
    with open(os.path.join("data", "data.dat"), "rb") as data_file:
        prev_best_score = int(pickle.load(data_file)[0])
        if score > prev_best_score:
            data_to_write = [score, datetime.datetime.now()]
            with open(os.path.join("data", "data.dat"), "wb") as data_file2:
                pickle.dump(data_to_write, data_file2)


def game_state1(window, control):  # NORMAL
    joy_ctrl = read_all_controls()
    can_move = True
    score_font = pygame.font.SysFont("calibri", 35, True)
    score = 0
    snake = objects.Snake()
    food = objects.Food(randint(0, 39) * GRID, randint(0, 29) * GRID)
    MOVE = pygame.USEREVENT + 1
    pygame.time.set_timer(MOVE, 37)
    game = Room()

    while game.run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                control["state"] = switch_state(game, states.QUIT)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT and not snake.dirs["left"] and can_move:
                    snake.dir = Vector(snake.vel, 0, 0)
                    snake.change_direction("right")
                    can_move = False
                elif event.key == pygame.K_LEFT and not snake.dirs["right"] and can_move:
                    snake.dir = Vector(-snake.vel, 0, 0)
                    snake.change_direction("left")
                    can_move = False
                elif event.key == pygame.K_DOWN and not snake.dirs["up"] and can_move:
                    snake.dir = Vector(0, snake.vel, 0)
                    snake.change_direction("down")
                    can_move = False
                elif event.key == pygame.K_UP and not snake.dirs["down"] and can_move:
                    snake.dir = Vector(0, -snake.vel, 0)
                    snake.change_direction("up")
                    can_move = False
                elif event.key == pygame.K_ESCAPE:
                    switch_state(game, pause_st.pause_state, window, control)
                elif event.key == pygame.K_b:
                    snake.grow()
            elif event.type == MOVE:
                snake.move1()
                can_move = True
                if snake.collide():
                    control["state"] = switch_state(game, states.GAME_OVER)

        if not no_joystick:
            if joy.get_button(joy_ctrl["pause"]):
                switch_state(game, pause_st.pause_state, window, control)
            if str(joy.get_hat(0)) == joy_ctrl["left"] and not snake.dirs["right"] and can_move:
                snake.dir = Vector(-snake.vel, 0, 0)
                snake.change_direction("left")
                can_move = False
            elif str(joy.get_hat(0)) == joy_ctrl["right"] and not snake.dirs["left"] and can_move:
                snake.dir = Vector(snake.vel, 0, 0)
                snake.change_direction("right")
                can_move = False
            elif str(joy.get_hat(0)) == joy_ctrl["up"] and not snake.dirs["down"] and can_move:
                snake.dir = Vector(0, -snake.vel, 0)
                snake.change_direction("up")
                can_move = False
            elif str(joy.get_hat(0)) == joy_ctrl["down"] and not snake.dirs["up"] and can_move:
                snake.dir = Vector(0, snake.vel, 0)
                snake.change_direction("down")
                can_move = False

        window.fill((16, 16, 16))
        if snake.eat(food):
            snake.grow()
            score += 1
            food = objects.Food(randint(0, 39) * GRID, randint(0, 29) * GRID)
        snake.show(window)
        food.show(window)
        window.blit(score_font.render("SCORE: " + str(score), True, (255, 255, 255)), (WIDTH // 2 - 72, 38))
        show_fps(window)
        pygame.display.flip()
        clock.tick(60)

    save_best_score(score)


def game_state2(window, control):  # EASY
    joy_ctrl = read_all_controls()
    can_move = True
    score_font = pygame.font.SysFont("calibri", 35, True)
    score = 0
    snake = objects.Snake()
    food = objects.Food(randint(0, 39) * GRID, randint(0, 29) * GRID)
    MOVE = pygame.USEREVENT + 1
    pygame.time.set_timer(MOVE, 60)
    game = Room()

    while game.run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                control["state"] = switch_state(game, states.QUIT)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT and not snake.dirs["left"] and can_move:
                    snake.dir = Vector(snake.vel, 0, 0)
                    snake.change_direction("right")
                    can_move = False
                elif event.key == pygame.K_LEFT and not snake.dirs["right"] and can_move:
                    snake.dir = Vector(-snake.vel, 0, 0)
                    snake.change_direction("left")
                    can_move = False
                elif event.key == pygame.K_DOWN and not snake.dirs["up"] and can_move:
                    snake.dir = Vector(0, snake.vel, 0)
                    snake.change_direction("down")
                    can_move = False
                elif event.key == pygame.K_UP and not snake.dirs["down"] and can_move:
                    snake.dir = Vector(0, -snake.vel, 0)
                    snake.change_direction("up")
                    can_move = False
                elif event.key == pygame.K_ESCAPE:
                    switch_state(game, pause_st.pause_state, window, control)
                elif event.key == pygame.K_b:
                    snake.grow()
            elif event.type == MOVE:
                snake.move1()
                can_move = True
                if snake.collide():
                    control["state"] = switch_state(game, states.GAME_OVER)

        if not no_joystick:
            if joy.get_button(joy_ctrl["pause"]):
                switch_state(game, pause_st.pause_state, window, control)
            if str(joy.get_hat(0)) == joy_ctrl["left"] and not snake.dirs["right"] and can_move:
                snake.dir = Vector(-snake.vel, 0, 0)
                snake.change_direction("left")
                can_move = False
            elif str(joy.get_hat(0)) == joy_ctrl["right"] and not snake.dirs["left"] and can_move:
                snake.dir = Vector(snake.vel, 0, 0)
                snake.change_direction("right")
                can_move = False
            elif str(joy.get_hat(0)) == joy_ctrl["up"] and not snake.dirs["down"] and can_move:
                snake.dir = Vector(0, -snake.vel, 0)
                snake.change_direction("up")
                can_move = False
            elif str(joy.get_hat(0)) == joy_ctrl["down"] and not snake.dirs["up"] and can_move:
                snake.dir = Vector(0, snake.vel, 0)
                snake.change_direction("down")
                can_move = False

        window.fill((26, 26, 26))
        if snake.eat(food):
            snake.grow()
            score += 1
            food = objects.Food(randint(0, 39) * GRID, randint(0, 29) * GRID)
        snake.show(window)
        food.show(window)
        window.blit(score_font.render("SCORE: " + str(score), True, (255, 255, 255)), (WIDTH // 2 - 72, 38))
        show_fps(window)
        pygame.display.flip()
        clock.tick(60)

    save_best_score(score)


def game_state3(window, control):  # HARD
    joy_ctrl = read_all_controls()
    can_move = True
    score_font = pygame.font.SysFont("calibri", 35, True)
    score = 0
    snake = objects.Snake()
    food = objects.Food(randint(0, 39) * GRID, randint(0, 29) * GRID)
    MOVE = pygame.USEREVENT + 1
    pygame.time.set_timer(MOVE, 35)
    game = Room()

    while game.run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                control["state"] = switch_state(game, states.QUIT)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT and not snake.dirs["left"] and can_move:
                    snake.dir = Vector(snake.vel, 0, 0)
                    snake.change_direction("right")
                    can_move = False
                elif event.key == pygame.K_LEFT and not snake.dirs["right"] and can_move:
                    snake.dir = Vector(-snake.vel, 0, 0)
                    snake.change_direction("left")
                    can_move = False
                elif event.key == pygame.K_DOWN and not snake.dirs["up"] and can_move:
                    snake.dir = Vector(0, snake.vel, 0)
                    snake.change_direction("down")
                    can_move = False
                elif event.key == pygame.K_UP and not snake.dirs["down"] and can_move:
                    snake.dir = Vector(0, -snake.vel, 0)
                    snake.change_direction("up")
                    can_move = False
                elif event.key == pygame.K_ESCAPE:
                    switch_state(game, pause_st.pause_state, window, control)
                elif event.key == pygame.K_b:
                    snake.grow()
            elif event.type == MOVE:
                if not snake.move2():
                    control["state"] = switch_state(game, states.GAME_OVER)
                can_move = True
                if snake.collide():
                    control["state"] = switch_state(game, states.GAME_OVER)

        if not no_joystick:
            if joy.get_button(joy_ctrl["pause"]):
                switch_state(game, pause_st.pause_state, window, control)
            if str(joy.get_hat(0)) == joy_ctrl["left"] and not snake.dirs["right"] and can_move:
                snake.dir = Vector(-snake.vel, 0, 0)
                snake.change_direction("left")
                can_move = False
            elif str(joy.get_hat(0)) == joy_ctrl["right"] and not snake.dirs["left"] and can_move:
                snake.dir = Vector(snake.vel, 0, 0)
                snake.change_direction("right")
                can_move = False
            elif str(joy.get_hat(0)) == joy_ctrl["up"] and not snake.dirs["down"] and can_move:
                snake.dir = Vector(0, -snake.vel, 0)
                snake.change_direction("up")
                can_move = False
            elif str(joy.get_hat(0)) == joy_ctrl["down"] and not snake.dirs["up"] and can_move:
                snake.dir = Vector(0, snake.vel, 0)
                snake.change_direction("down")
                can_move = False

        window.fill((14, 14, 14))
        if snake.eat(food):
            snake.grow()
            score += 1
            food = objects.Food(randint(0, 39) * GRID, randint(0, 29) * GRID)
        snake.show(window)
        food.show(window)
        window.blit(score_font.render("SCORE: " + str(score), True, (255, 255, 255)), (WIDTH // 2 - 72, 38))
        show_fps(window)
        pygame.display.flip()
        clock.tick(60)

    save_best_score(score)
