import time
import neat
from bird import *
from pipe import Pipe
from base import Base

WIN_WIDTH = 500
WIN_HEIGHT = 800

def draw_window(window, birds, pipes, base, score):
    window.blit(images.BG_IMG, (0, 0))

    for pipe in pipes:
        pipe.draw(window)
    base.draw(window)

    for bird in birds:
        bird.draw(window)

    text = images.STAT_FONT.render('Score:' + str(score), 1, (0, 0, 0))
    window.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))

    images.pygame.display.update()

def main(genomes, config):
    nets = []
    ge = []
    birds = []

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        birds.append(Bird(230, 350))
        g.fitness = 0
        ge.append(g)

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
                images.pygame.quit()
                quit()
        # bird.move()
        # base.move()

        pipe_ind = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                pipe_ind = 1
        else:
            run = False
            break

        for index, bird in enumerate(birds):
            bird.move()
            ge[index].fitness += 0.1

            output = nets[index].activate((bird.y, abs(bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)))

            if output[0] > 0.5:
                bird.jump()

        rem = []
        add_pipe = False
        for pipe in pipes:
            for index, bird in enumerate(birds):
                if pipe.collide(bird):
                    ge[index].fitness -= 1
                    birds.pop(index)
                    nets.pop(index)
                    ge.pop(index)
            
            if not pipe.passed and pipe.x < birds[0].x:
                pipe.passed = True
                add_pipe = True

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

            pipe.move()

        if add_pipe:
            score += 1
            for g in ge:
                g.fitness += 5
            pipes.append(Pipe(700))    
 
        for r in rem:
            pipes.remove(r)

        for index, bird in enumerate(birds):
            if bird.y + bird.img.get_height() >= 730 or bird.y < 0:
                birds.pop(index)
                nets.pop(index)
                ge.pop(index)
        
        draw_window(window, birds, pipes, base, score)


def run(config_path):
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    
    population = neat.Population(config)

    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    winnder = population.run(main, 50)

# if __name__ == 'main':
local_dir = images.os.path.dirname(__file__)
config_path = images.os.path.join(local_dir, 'config_feedforward.txt')
run(config_path)