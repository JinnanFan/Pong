import pygame
pygame.init()

# Settings for the game window
WIDTH, HEIGHT = 700, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")
FPS = 60

# Settings for the score board
SCORE_FONT = pygame.font.SysFont("comicsans", 50, italic=True)
WINNING_SCORE = 50

# Settings for paddles, ball
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_RADIUS = 7

# Color options
WHITE = (255,255,255)
PURPLE= (205,182,228)
BLACK = (0,0,0)

class Paddle:
    COLOR = WHITE
    VEL = 4

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
    def draw(self, win):
        pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))

    def move(self, up=True):
        if up:
            self.y -= self.VEL
        else:
            self.y += self.VEL


class Ball:
    COLOR = BLACK
    VEL_MAX = 2

    def __init__(self, x, y, radius):
        self.x = self.original_x= x
        self.y = self.original_y = y
        self.radius = radius
        self.x_vel = self.VEL_MAX # the reason why we put ball's velocity in its constructor is that this is actually its atrributes (properties), like the posion attributes of paddles
        self.y_vel = 0

    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.x_vel *= -1
        self.y_vel = 0


def draw_window(win, paddles, ball, left_score, right_score):
    win.fill(PURPLE)
    # draw the score board
    left_score_text= SCORE_FONT.render(f"{left_score}", 1, WHITE)
    right_score_text= SCORE_FONT.render(f"{right_score}", 1, WHITE)
    win.blit(left_score_text, (WIDTH//4, 20))
    win.blit(right_score_text, (WIDTH * 3//4, 20))
 
    # draw two paddles
    for paddle in paddles:
        paddle.draw(win)

    # draw a dashed line in the middle of game window
    N = 25
    dashed_line_height = HEIGHT/N
    for i in range(N):
        if i%2 == 0:
            continue
        pygame.draw.rect(win, WHITE, (WIDTH//2 - 5, i*dashed_line_height, 10, dashed_line_height))
    
    # draw a ball     
    ball.draw(win)

    # make sure to do this dispaly update as last step due to its long running time
    pygame.display.update()


def handle_paddle_movement(keys_pressed, left_paddle, right_paddle):
    # Use w and s to move the left paddle up and down while keeping it wthin the displayed game window
    if keys_pressed[pygame.K_w] and left_paddle.y - left_paddle.VEL >= 0: # UP
        left_paddle.move(up=True)
    if keys_pressed[pygame.K_s] and left_paddle.y + PADDLE_HEIGHT + left_paddle.VEL <= HEIGHT: # DOWN
        left_paddle.move(up=False)
    # Use arrow keys to move the right paddle up and down while keeping it wthin the displayed game window
    if keys_pressed[pygame.K_UP] and right_paddle.y - left_paddle.VEL >= 0: # UP
        right_paddle.move(up=True)
    if keys_pressed[pygame.K_DOWN] and right_paddle.y + PADDLE_HEIGHT + right_paddle.VEL <= HEIGHT: # DOWN
        right_paddle.move(up=False)


def handle_ball_collision(ball, left_paddle, right_paddle):
    # handle the ball collison with ceilings first: y velocity will be opposite when collision happens
    if ball.y - ball.radius <= 0 or ball.y + ball.radius >= HEIGHT: 
        ball.y_vel *= -1

    else:
        if ball.x_vel < 0 and ball.x - ball.radius <= left_paddle.x + left_paddle.width: # check the collision with the left paddle
            ball_paddle_collison(ball, left_paddle)
   
        if ball.x_vel > 0 and ball.x + ball.radius >= right_paddle.x:
            ball_paddle_collison(ball, right_paddle)

# handle the ball collison with paddles: x velocity will be opposite when colliison happens, and y velocity will change depands on the displacement of the ball center to the paddle center
def ball_paddle_collison(ball, paddle):
    if ball.y >= paddle.y and ball.y <= paddle.y + paddle.height:
        ball.x_vel *= -1

        paddle_center = paddle.y + paddle.height/2
        d = paddle_center - ball.y # d is the displacement between the ball and the center of the paddle 
        ball.y_vel  = d*ball.VEL_MAX/(paddle.height/2)
        ball.y_vel *= -1


def main():
    clock = pygame.time.Clock()
    # Initilize paddles, ball and score display
    left_paddle = Paddle(10, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = Paddle(WIDTH - PADDLE_WIDTH - 10, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = Ball(WIDTH//2, HEIGHT//2, BALL_RADIUS)
    left_score = 0
    right_score = 0
    
    run = True
    while run:
        clock.tick(FPS)
        draw_window(WIN, [left_paddle, right_paddle], ball, left_score, right_score)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        keys_pressed = pygame.key.get_pressed()
        handle_paddle_movement(keys_pressed, left_paddle, right_paddle)

        ball.move()
        handle_ball_collision(ball, left_paddle, right_paddle)
        
        if ball.x < 0:
            right_score += 1
            ball.reset()
        elif ball.x > WIDTH:
            left_score += 1
            ball.reset()
    
    pygame.quit()


if __name__ == '__main__':
    main()