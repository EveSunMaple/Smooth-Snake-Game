import pygame
import random
import math

# 初始化
pygame.init()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Smooth Snake Game")
clock = pygame.time.Clock()

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# 游戏参数
cell_size = 20
speed = 200  # 像素/秒
turn_smoothness = 0.2  # 转向平滑度（0-1）
body_spacing = 20  # 身体段间距

class Snake:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.head = [screen_width/2, screen_height/2]
        self.body = []
        self.direction = pygame.Vector2(1, 0)
        self.next_direction = pygame.Vector2(1, 0)
        self.length = 300
        self.alive = True
    
    def update(self, delta_time):
        if not self.alive:
            return
        
        # 平滑转向
        self.direction += (self.next_direction - self.direction) * turn_smoothness
        if self.direction.length() > 0:
            self.direction = self.direction.normalize()
        
        # 更新头部位置
        self.head[0] += self.direction.x * speed * delta_time
        self.head[1] += self.direction.y * speed * delta_time
        
        # 记录头部位置到身体
        self.body.insert(0, self.head.copy())
        
        # 保持身体长度
        while len(self.body) > self.length:
            self.body.pop()
        
        # 碰撞检测
        self.check_collisions()
    
    def check_collisions(self):
        # 边界检测
        if (self.head[0] < 0 or self.head[0] > screen_width or
            self.head[1] < 0 or self.head[1] > screen_height):
            self.alive = False
        
        # 自碰检测
        for segment in self.body[10:]:  # 跳过前几个段避免误判
            if math.dist(self.head, segment) < cell_size/2:
                self.alive = False
    
    def grow(self):
        self.length += 3
    
    def draw(self):
        if not self.alive:
            return
        
        # 绘制头部
        pygame.draw.circle(screen, GREEN, self.head, cell_size//2)
        
        # 绘制身体
        for i, pos in enumerate(self.body):
            alpha = 255 * (1 - i/self.length)
            color = (0, 255, 0, alpha)
            radius = cell_size//2 * (1 - i/(self.length*2))
            pygame.draw.circle(screen, GREEN, pos, radius)

class Food:
    def __init__(self):
        self.respawn()
    
    def respawn(self):
        self.pos = [
            random.randint(cell_size, screen_width - cell_size),
            random.randint(cell_size, screen_height - cell_size)
        ]
    
    def check_collision(self, snake_head):
        return math.dist(self.pos, snake_head) < cell_size
    
    def draw(self):
        pygame.draw.circle(screen, RED, self.pos, cell_size//2)

def game_loop():
    snake = Snake()
    food = Food()
    score = 0
    
    running = True
    while running:
        delta_time = clock.tick(60)/1000
        
        # 事件处理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if not snake.alive:
                    snake.reset()
                    score = 0
                    food.respawn()
                
                if event.key == pygame.K_UP and snake.direction.y != 1:
                    snake.next_direction = pygame.Vector2(0, -1)
                elif event.key == pygame.K_DOWN and snake.direction.y != -1:
                    snake.next_direction = pygame.Vector2(0, 1)
                elif event.key == pygame.K_LEFT and snake.direction.x != 1:
                    snake.next_direction = pygame.Vector2(-1, 0)
                elif event.key == pygame.K_RIGHT and snake.direction.x != -1:
                    snake.next_direction = pygame.Vector2(1, 0)
        
        # 游戏逻辑更新
        snake.update(delta_time)
        
        if food.check_collision(snake.head):
            snake.grow()
            food.respawn()
            score += 1
        
        # 绘制
        screen.fill(BLACK)
        food.draw()
        snake.draw()
        
        # 显示分数
        font = pygame.font.Font(None, 36)
        text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(text, (10, 10))
        
        # 游戏结束提示
        if not snake.alive:
            text = font.render("Game Over! Press any key to restart", True, WHITE)
            screen.blit(text, (screen_width//2 - 200, screen_height//2))
        
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    game_loop()