import pygame
import random
import numpy as np
import math
import sys

SCREEN_W, SCREEN_H = 1280, 720
FPS = 60

POP_SIZE = 50
MUTATION_RATE = 0.15
MUTATION_SCALE = 0.5
ELITE_FRACTION = 0.2
PIPE_WIDTH = 80
PIPE_GAP = 160
PIPE_SPACING = 350
SCROLL_SPEED = 4

BIRD_SIZE = 34
GRAVITY = 0.6
FLAP_V = -10


NN_INPUTS = 4  
NN_HIDDEN = 6
NN_OUTPUTS = 1


def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))

def flatten_weights(W1, b1, W2, b2):
    return np.concatenate([W1.flatten(), b1.flatten(), W2.flatten(), b2.flatten()])

def unflatten_weights(vec):
    w1_size = NN_INPUTS * NN_HIDDEN
    b1_size = NN_HIDDEN
    w2_size = NN_HIDDEN * NN_OUTPUTS
    b2_size = NN_OUTPUTS
    i = 0
    W1 = vec[i:i + w1_size].reshape((NN_HIDDEN, NN_INPUTS)); i += w1_size
    b1 = vec[i:i + b1_size].reshape((NN_HIDDEN,)); i += b1_size
    W2 = vec[i:i + w2_size].reshape((NN_OUTPUTS, NN_HIDDEN)); i += w2_size
    b2 = vec[i:i + b2_size].reshape((NN_OUTPUTS,)); i += b2_size
    return W1, b1, W2, b2

def init_random_weights():
    W1 = np.random.randn(NN_HIDDEN, NN_INPUTS) * np.sqrt(2 / NN_INPUTS)
    b1 = np.zeros(NN_HIDDEN)
    W2 = np.random.randn(NN_OUTPUTS, NN_HIDDEN) * np.sqrt(2 / NN_HIDDEN)
    b2 = np.zeros(NN_OUTPUTS)
    return flatten_weights(W1, b1, W2, b2)

def forward(weights_flat, inputs):
    W1, b1, W2, b2 = unflatten_weights(weights_flat)
    z1 = W1.dot(inputs) + b1
    a1 = np.tanh(z1)
    z2 = W2.dot(a1) + b2
    out = sigmoid(z2)  # 0..1
    return out[0]

def crossover(parent_a, parent_b):
    # single-point crossover on flattened vector
    a = parent_a.copy()
    b = parent_b.copy()
    cut = random.randint(0, len(a) - 1)
    child = np.concatenate([a[:cut], b[cut:]])
    return child

def mutate(vec):
    mask = np.random.rand(vec.shape[0]) < MUTATION_RATE
    vec[mask] += np.random.randn(mask.sum()) * MUTATION_SCALE
    return vec


class Bird:
    def __init__(self, brain=None):
        self.x = 200
        self.y = SCREEN_H / 2 + random.uniform(-50, 50)
        self.vel = 0.0
        self.alive = True
        self.score = 0  # pipes passed
        self.fitness = 0.0
        self.color = (random.randint(50,255), random.randint(50,255), random.randint(50,255))
        if brain is None:
            self.brain = init_random_weights()
        else:
            self.brain = brain.copy()

    def flap(self):
        self.vel = FLAP_V

    def update(self):
        self.vel += GRAVITY
        self.y += self.vel

    def decide(self, nearest_pipe):
        
        gap_center = nearest_pipe.gap_y
        dist = (nearest_pipe.x - self.x) / SCREEN_W
        bird_y_n = self.y / SCREEN_H
        vel_n = max(-20, min(20, self.vel)) / 20.0
        gap_diff = (gap_center - self.y) / SCREEN_H  
        inputs = np.array([bird_y_n, vel_n, dist, gap_diff], dtype=np.float32)
        out = forward(self.brain, inputs)
        if out > 0.5:
            self.flap()

class PipePair:
    def __init__(self, x):
        self.x = x
        margin = 60
        self.gap_y = random.randint(margin + PIPE_GAP//2, SCREEN_H - margin - PIPE_GAP//2)
        self.passed = False

    def update(self):
        self.x -= SCROLL_SPEED

    def collides(self, bird: Bird):
        bx1 = bird.x
        by1 = bird.y
        bx2 = bird.x + BIRD_SIZE
        by2 = bird.y + BIRD_SIZE

        top_x1 = self.x
        top_y1 = 0
        top_x2 = self.x + PIPE_WIDTH
        top_y2 = self.gap_y - PIPE_GAP/2

        bot_x1 = self.x
        bot_y1 = self.gap_y + PIPE_GAP/2
        bot_x2 = self.x + PIPE_WIDTH
        bot_y2 = SCREEN_H

        def rect_overlap(ax1, ay1, ax2, ay2, bx1, by1, bx2, by2):
            return not (ax2 < bx1 or ax1 > bx2 or ay2 < by1 or ay1 > by2)

        if rect_overlap(bx1, by1, bx2, by2, top_x1, top_y1, top_x2, top_y2):
            return True
        if rect_overlap(bx1, by1, bx2, by2, bot_x1, bot_y1, bot_x2, bot_y2):
            return True
        return False

def evaluate_fitness(pop):
    for b in pop:
        b.fitness = b.score

def next_generation(old_pop):
    evaluate_fitness(old_pop)
    old_pop.sort(key=lambda b: b.fitness, reverse=True)
    best = old_pop[0]
    elites_count = max(1, int(ELITE_FRACTION * POP_SIZE))

    new_pop = []
    for i in range(elites_count):
        brain = old_pop[i].brain.copy()
        child = Bird(brain=brain)
        new_pop.append(child)

    while len(new_pop) < POP_SIZE:
        a, b = random.sample(old_pop[:max(elites_count,2)], 2)
        child_brain = crossover(a.brain, b.brain)
        child_brain = mutate(child_brain)
        new_pop.append(Bird(brain=child_brain))

    return new_pop, best

def draw_text(surf, text, x, y, size=24, color=(0,0,0)):
    font = pygame.font.SysFont("Arial", size)
    img = font.render(text, True, color)
    surf.blit(img, (x, y))

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption("Flappy GA")
    clock = pygame.time.Clock()

    bg_color = (135, 206, 235)  
    pipe_color = (60, 179, 113)
    top_pipe_color = (34,139,34)

    generation = 1
    global POP_SIZE
    population = [Bird() for _ in range(POP_SIZE)]
    pipes = []
    for i in range(6):
        pipes.append(PipePair(SCREEN_W + i * PIPE_SPACING))

    best_ever_score = 0

    run = True
    ticks = 0

    while run:
        clock.tick(FPS)
        ticks += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:

                    population = [Bird() for _ in range(POP_SIZE)]
                    generation = 1
                    pipes = [PipePair(SCREEN_W + i * PIPE_SPACING) for i in range(6)]
                    best_ever_score = 0

        alive = [b for b in population if b.alive]

        if len(alive) == 0:
            population, best = next_generation(population)
            gen_best_score = best.score
            best_ever_score = max(best_ever_score, best.score)
            pipes = [PipePair(SCREEN_W + i * PIPE_SPACING) for i in range(6)]
            for b in population:
                b.x = 200
                b.y = SCREEN_H/2 + random.uniform(-30,30)
                b.vel = 0
                b.alive = True
                b.score = 0
            generation += 1
            ticks = 0
            continue

        for p in pipes:
            p.update()

        if pipes and pipes[0].x < -PIPE_WIDTH:
            pipes.pop(0)
            new_x = pipes[-1].x + PIPE_SPACING
            pipes.append(PipePair(new_x))

        for b in alive:
            # nearest pipe:
            nearest = None
            for p in pipes:
                if p.x + PIPE_WIDTH > b.x - 10:
                    nearest = p
                    break
            if nearest is None:
                nearest = pipes[0]
            b.decide(nearest)
            b.update()

            # collisions with pipes
            for p in pipes:
                if p.collides(b):
                    b.alive = False
                    break

            # out of bounds
            if b.y < -50 or b.y > SCREEN_H + 50:
                b.alive = False

            # score increments when passes pipe center x
            for p in pipes:
                if (not p.passed) and (p.x + PIPE_WIDTH/2 < b.x):
                    p.passed = True

            for p in pipes:
                if not getattr(p, "_score_marked", False):

                    pass

            if not hasattr(b, "last_pipe_index"):
                b.last_pipe_index = -1

            for idx, p in enumerate(pipes):
                if p.x + PIPE_WIDTH > b.x - 10:
                    if idx - 1 > b.last_pipe_index:
                        b.score += 1
                        b.last_pipe_index = idx - 1
                    break


        screen.fill(bg_color)


        for p in pipes:
            top_rect = pygame.Rect(int(p.x), 0, PIPE_WIDTH, int(p.gap_y - PIPE_GAP/2))
            bot_rect = pygame.Rect(int(p.x), int(p.gap_y + PIPE_GAP/2), PIPE_WIDTH, SCREEN_H - int(p.gap_y + PIPE_GAP/2))
            pygame.draw.rect(screen, top_pipe_color, top_rect)
            pygame.draw.rect(screen, pipe_color, bot_rect)


        for b in population:
            rect = pygame.Rect(int(b.x), int(b.y), BIRD_SIZE, BIRD_SIZE)
            if b.alive:
                pygame.draw.ellipse(screen, b.color, rect)
            else:
                pygame.draw.ellipse(screen, (80,80,80), rect)


        alive_count = sum(1 for b in population if b.alive)
        best_score = max(b.score for b in population)
        best_ever_score = max(best_ever_score, best_score)

        draw_text(screen, f"Generation: {generation}", 10, 10, size=26)
        draw_text(screen, f"Alive: {alive_count}/{POP_SIZE}", 10, 40, size=22)
        draw_text(screen, f"Best this gen: {best_score}", 10, 68, size=22)
        draw_text(screen, f"Best ever: {best_ever_score}", 10, 96, size=22)
        draw_text(screen, f"FPS: {int(clock.get_fps())}", SCREEN_W - 120, 10, size=20)


        first_alive = next((b for b in population if b.alive), None)
        if first_alive:
            for p in pipes:
                if p.x + PIPE_WIDTH > first_alive.x - 10:
                    gx = int(p.x + PIPE_WIDTH/2)
                    pygame.draw.line(screen, (255,0,0), (gx,0), (gx, SCREEN_H), 1)
                    break

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
