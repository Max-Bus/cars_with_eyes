from population import Population
from racetrack import RaceTrack
from mapdata import *

p = Population(RaceTrack(), POPSIZE)
p.initialize_population(None, None)
p.generalize(30)
