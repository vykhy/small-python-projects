import pygame
from pong import Game
import neat
import os
import pickle

pygame.init()

WIDTH, HEIGHT = 1000, 650
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

game = Game(WIN, WIDTH, HEIGHT)

class PongGame:
    def __init__(self, window, width, height):
        self.game = Game(window, width, height)
        self.left_paddle = self.game.left_paddle
        self.right_paddle = self.game.right_paddle
        self.ball = self.game.ball
    
    def test_ai(self, genome, config):
        """
            This method lets us test the best version of the ai
            Player controls left paddle and ai controls the right paddle
        """
        # initialize network
        net = neat.nn.FeedForwardNetwork.create(genome, config)

        run = True
        clock = pygame.time.Clock()
        while run:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break

            # handle key presses to move paddle (for Player)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                self.game.move_paddle(left=True, up=True)    
            if keys[pygame.K_s]:
                self.game.move_paddle(True, up=False)
            
            # to move paddle with AI decision
            # get output from the neural network
            output = net.activate((self.right_paddle.y, self.ball.y, abs(self.right_paddle.x - self.ball.x)))
            # get decision from output
            decision = output.index(max(output))

            # handle paddle movement according to decision
            if decision == 0:
                pass
            elif decision == 1:
                self.game.move_paddle(left=False, up=True)
            else:
                self.game.move_paddle(left=False, up=False)

            # basic game loop and draw
            game_info = self.game.loop()
            self.game.draw()
            pygame.display.update()

        pygame.quit()
    
    def train_ai(self, genome1, genome2, config):
        """
            This method tests two genomes against each other
        """
        # initialize neural networks from genome
        net1 = neat.nn.FeedForwardNetwork.create(genome1, config)
        net2 = neat.nn.FeedForwardNetwork.create(genome2, config)

        # start game
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

            # get output of neural network 1
            output1 = net1.activate((self.left_paddle.y, self.ball.y, abs(self.left_paddle.x - self.ball.x)))
            # get decision of neural network 1
            decision1 = output1.index(max(output1))

            # handle left paddle with output of neural network 1
            if decision1 == 0:
                pass
            elif decision1 == 1:
                self.game.move_paddle(left=True, up=True)
            else:
                self.game.move_paddle(left=True, up=False)

            # get output of neural network 2
            output2 = net2.activate((self.right_paddle.y, self.ball.y, abs(self.right_paddle.x - self.ball.x)))
            # get decision of neural network 2
            decision2 = output2.index(max(output2))

            # handle right paddle with output of neural network 2
            if decision2 == 0:
                pass
            elif decision2 == 1:
                self.game.move_paddle(left=False, up=True)
            else:
                self.game.move_paddle(left=False, up=False)

            # print(output1, output2)

            # run basic game loop and draw methods
            game_info = self.game.loop()
            self.game.draw(draw_score=False, draw_hits=True)
            pygame.display.update()

            # if any of the genomes score, or test runs too long
            # calculate the fitness of the genomes and break
            if game_info.left_score >= 1 or game_info.right_score >= 1 or game_info.left_hits > 50:
                self.calculate_fitness(genome1, genome2, game_info)
                break
    
    def calculate_fitness(self, genome1, genome2, game_info):
        # fitness is the sum of all the hits it achieved against all other genomes
        # here we add its score against the current opponent
        genome1.fitness += game_info.left_hits
        genome2.fitness += game_info.right_hits

def eval_genome(genomes, config):
    """
        This method evaluates genomes by running every NN against ever other NN to pick the best Neural net
    """
    width, height = 1000, 650
    window = pygame.display.set_mode((width, height))

    # for each genome, create pong game and train it against all other genomes
    for i, (genome_id1, genome_1) in enumerate(genomes):
        if i == len(genomes) - 1:
            break
        genome_1.fitness = 0
        for genome_id2, genome_2 in genomes[i+1:]:
            genome_2.fitness = 0 if genome_2.fitness == None else genome_2.fitness
            game = PongGame(window, width, height)
            game.train_ai(genome_1, genome_2, config)

def run_neat(config):
    p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-30')  # -- UNCOMMENT AND RUN TO PICK UP TRAINING FROM PREVIOUS CHECKPOINT
    # p = neat.Population(config)  -- RUN THIS LINE FOR INITIAL TRAINING --
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(1))

    # get the best AI  from training run of 50 generations
    winner = p.run(eval_genome, 50)
    # save winner to file
    with open('best.pickle', 'wb') as f:
        pickle.dump(winner, f)

def test_ai(config):
    # get the best AI model
    with open('best.pickle', 'rb') as f:
        winner = pickle.load(f)
    
    # initialize game
    game = PongGame(WIN, WIDTH, HEIGHT)
    # run test to play against the best AI
    game.test_ai(winner, config)

if __name__=="__main__":
    # get config file
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    # run_neat(config)    # Uncomment this line and run to train the AI
    test_ai(config)   # Uncomment this line and run to play against the AI
