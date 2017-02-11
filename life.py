import numpy as np
import os
from time import sleep

from sense_hat import SenseHat

### Set up config variables
## User adjustable
# Random Seed
try :
    SEED = int(os.getenv('SEED'))
except (TypeError, ValueError) as e:
    SEED = None
## Preset
# Field size
SIZE = (8, 8)  # The Size of the SenseHAT LED matrix
PIXEL = [0, 128, 0]  # R, G, B colour of the displayed state
ZERO = [0, 0, 0]
DELAY = 1.0  # seconds between updates

sense = SenseHat()

# https://jakevdp.github.io/blog/2013/08/07/conways-game-of-life/
def life_step(X):
    """Game of life step using generator expressions"""
    nbrs_count = sum(np.roll(np.roll(X, i, 0), j, 1)
                     for i in (-1, 0, 1) for j in (-1, 0, 1)
                     if (i != 0 or j != 0))
    return (nbrs_count == 3) | (X & (nbrs_count == 2))

def display(state):
    """Convert Game of Life state into display pixel values"""
    a = state.reshape(SIZE[0]*SIZE[1])
    leds = [ PIXEL if x else ZERO for x in a.tolist() ]
    sense.set_pixels(leds)

def initialize(size, seed=None):
    """Initialize the Game of Life field"""
    np.random.seed(SEED)
    X1 = np.zeros(SIZE, dtype=bool)
    X = np.zeros(SIZE, dtype=bool)
    r = np.random.random(SIZE)
    X = (r > 0.75)
    return X, X1

if __name__ == "__main__":
    sense.clear()  # no arguments defaults to off

    X, X1 = initialize(SIZE, SEED)  # set up display
    display(X)
    reset = False

    while True:  # Main loop
        if reset or len(sense.stick.get_events()) > 0:
            reset = False
            X, X1 = initialize(SIZE, SEED)  # set up display
            display(X)
        sleep(DELAY)
        X = life_step(X)
        display(X)
        if np.array_equal(X, X1):
            reset = True
            sleep(DELAY * 3)
        X1 = X
