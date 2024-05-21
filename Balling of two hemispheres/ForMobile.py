import pygame
import sys
import random

# تعریف متغیرهای مورد نیاز
win_width = 1280
win_height = 720
paddle_width = 15
paddle_height = 200
ball_dim = 25
paddle_vel = 18

level = 0
pygame.init()
pygame.mixer.init()



# راه‌اندازی pygame

win = pygame.display.set_mode((win_width, win_height))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 26)  # فونت برای نمایش امتیاز
big_font = pygame.font.Font(None, 72)  # فونت بزرگ برای نمایش امتیاز در حالت pause
try :
    icon = pygame.image.load('ICO.png')  # بارگذاری تصویر آیکون
    pygame.display.set_icon(icon)  # تنظیم آیکون
except:
    pass
pygame.display.set_caption('Balling of Two hemispheres')  # تنظیم اسم

button_up = pygame.Rect(50, 500, 100, 100)
button_up_image = pygame.image.load('up.png').convert_alpha()
button_down = pygame.Rect(50, 610, 100, 100)
button_dn_image = pygame.image.load('dow.png').convert_alpha()
button_up2 = pygame.Rect(1130, 500, 100, 100)
button_down2 = pygame.Rect(1130, 610, 100, 100)
def draw_window(paddle1, paddle2, paddle_center, ball, score, elapsed_time, color, paused):
    win.fill(color)  # پاک کردن صفحه با رنگ متغیر
    pygame.draw.rect(win, (255-color[0], 255-color[1], 255-color[2]), paddle1)  # رسم paddle1
    pygame.draw.rect(win, (255-color[0], 255-color[1], 255-color[2]), paddle2)  # رسم paddle2
    pygame.draw.rect(win, (255-color[0], 255-color[1], 255-color[2]), paddle_center)  # رسم paddle_center
    pygame.draw.ellipse(win, (255-color[0], 255-color[1], 255-color[2]), ball)  # رسم توپ

    win.blit(button_up_image, button_up)
    win.blit(button_up_image, button_up2)
    win.blit(button_dn_image, button_down)
    win.blit(button_dn_image, button_down2)
    if paused:
        score_text = big_font.render("Score: " + str(score), 1, (255-color[0], 255-color[1], 255-color[2]))
        win.blit(score_text, (win_width / 2 - score_text.get_width() / 2, win_height / 2 - score_text.get_height() / 2))
    else:
        score_text = font.render("Score: " + str(score), 1, (255-color[0], 255-color[1], 255-color[2]))
        time_text = font.render("Time: " + str(elapsed_time), 1, (255-color[0], 255-color[1], 255-color[2]))
        win.blit(score_text, (win_width - 120, 10))
        win.blit(time_text, (10, 10))
    pygame.display.update()  # به‌روزرسانی صفحه

ball_vel = 8
score = 0

#pyinstaller -w -F -i ICO.ico MainCod.py


def main():
    pygame.mixer.music.load('./sound/background.mp3')
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1)
    ball_wall_collision_sound = pygame.mixer.Sound('./sound/-.mp3')
    ball_paddle_collision_sound = pygame.mixer.Sound('./sound/+.mp3')
    ball_paddle_center_sound = pygame.mixer.Sound('./sound/Center.mp3')
    global score
    ball_dim = 15  # تعریف اولیه ball_dim
    paddle1 = pygame.Rect(0, win_height / 2, paddle_width, paddle_height)
    paddle2 = pygame.Rect(win_width - paddle_width, win_height / 2, paddle_width, paddle_height)
    paddle_center = pygame.Rect(win_width / 2, win_height / 2, paddle_width, 60)  # اضافه کردن paddle_center
    ball = pygame.Rect(win_width / 2, win_height / 2, ball_dim, ball_dim)
    ball_dx = ball_dy = ball_vel
    paddle1_dy = paddle2_dy = 0
    paddle_center_dy = random.choice([-paddle_vel, paddle_vel])  # حرکت تصادفی paddle_center

    start_time = pygame.time.get_ticks()
    color = (0, 0, 0)
    paused = False  # اضافه کردن متغیر paused
    while True:
        elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
        if score > 10 and score < 30:
            if elapsed_time % 2  == 0 :
                color = (0, 0, 0)  # سیاه
            else:
                color = (255, 255, 255)  #
        if score > 30:
            if pygame.time.get_ticks() % 2 == 0 :
                color = (0, 0, 0)  # سیاه
            else:
                color = (255, 255, 255)  #

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_up.collidepoint(event.pos):
                    paddle1_dy = -paddle_vel
                elif button_down.collidepoint(event.pos):
                    paddle1_dy = paddle_vel
                if button_up2.collidepoint(event.pos):
                    paddle2_dy = -paddle_vel
                elif button_down2.collidepoint(event.pos):
                    paddle2_dy = paddle_vel
            elif event.type == pygame.MOUSEBUTTONUP:
                if button_up.collidepoint(event.pos) or button_down.collidepoint(event.pos):
                    paddle1_dy = 0
                if button_up2.collidepoint(event.pos) or button_down2.collidepoint(event.pos):
                    paddle2_dy = 0
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    paddle1_dy = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    paddle2_dy = 0

        if not paused:
            paddle1.move_ip(0, paddle1_dy)
            paddle2.move_ip(0, paddle2_dy)
            paddle_center.move_ip(0, paddle_center_dy)  # حرکت paddle_center
            ball.move_ip(ball_dx, ball_dy)
            if ball.colliderect(paddle1):
                ball_dx *= -1
                score += level + 1
                pygame.mixer.Sound.play(ball_paddle_collision_sound)
                # اگر توپ هنوز در دسته است، آن را به خارج از دسته منتقل کنید
                if ball.colliderect(paddle1):
                    ball.left = paddle1.right
            elif ball.colliderect(paddle2):
                ball_dx *= -1
                score += level + 1
                pygame.mixer.Sound.play(ball_paddle_collision_sound)
                # اگر توپ هنوز در دسته است، آن را به خارج از دسته منتقل کنید
                if ball.colliderect(paddle2):
                    ball.right = paddle2.left
            elif ball.colliderect(paddle_center):  # برخورد توپ با paddle_center
                ball_dx *= -1
                score += level
                pygame.mixer.Sound.play(ball_paddle_center_sound)
                # اگر توپ هنوز در دسته است، آن را به خارج از دسته منتقل کنید
                if ball.colliderect(paddle_center):
                    ball.left = paddle_center.right if ball_dx > 0 else paddle_center.left
            paddle1.height = max(15, paddle_height - score * 5)
            paddle2.height = max(15, paddle_height - score * 5)

            if paddle1.top <= 0 or paddle1.bottom >= win_height:
                paddle1_dy = 0
            if paddle2.top <= 0 or paddle2.bottom >= win_height:
                paddle2_dy = 0
            if paddle_center.top <= 0 or paddle_center.bottom >= win_height:  # تغییر جهت حرکت paddle_center
                paddle_center_dy *= -1
            if ball.left <= 0:
                ball_dx *= -1
                score += level -2  # کاهش امتیاز
                pygame.mixer.Sound.play(ball_wall_collision_sound)
            if ball.right >= win_width:
                ball_dx *= -1
                score += level -2 # کاهش امتیاز
                pygame.mixer.Sound.play(ball_wall_collision_sound)
            if ball.top <= 0 or ball.bottom >= win_height:
                ball_dy *= -1
            if ball.colliderect(paddle1) or ball.colliderect(paddle2):
                ball_dx *= -1
                score += level + 1
            # تغییر اندازه توپ بر اساس امتیاز
            ball_dim = max(8, 30 - score /4)
            ball.width = ball.height = ball_dim
        draw_window(paddle1, paddle2, paddle_center, ball, score, elapsed_time, color, paused)  # اضافه کردن paused به تابع رسم
        clock.tick(60)

if __name__ == "__main__":
    main()
