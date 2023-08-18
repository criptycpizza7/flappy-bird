import time
import neat
from bird import *
from pipe import Pipe
from base import Base

WIN_WIDTH = 500
WIN_HEIGHT = 800

def draw_window(window, bird, pipes, base, score):
    window.blit(images.BG_IMG, (0, 0))

    for pipe in pipes:
        pipe.draw(window)
    base.draw(window)
    bird.draw(window)

    text = images.STAT_FONT.render('Score:' + str(score), 1, (0, 0, 0))
    window.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))

    images.pygame.display.update()

def main():
    bird = Bird(230, 350)
    base = Base(730)
    pipes = [Pipe(700)]
    window = images.pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

    clock = images.pygame.time.Clock()

    score = 0

    run = True
    while run:
        clock.tick(30)
        for event in images.pygame.event.get():
            if event.type == images.pygame.QUIT:
                run = False
        # bird.move()
        base.move()

        rem = []
        add_pipe = False
        for pipe in pipes:
            if pipe.collide(bird):
                pass #
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)
            
            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True
            pipe.move()
    
        if add_pipe:
            score += 1
            pipes.append(Pipe(700))    
 
        for r in rem:
            pipes.remove(r)

        if bird.y + bird.img.get_height() >= 730:
            pass #
        draw_window(window, bird, pipes, base, score)
    images.pygame.quit()
    quit()

main()