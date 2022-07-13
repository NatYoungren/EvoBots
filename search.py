import os
import time
import numpy as np
from parallelHillClimber import PARALLEL_HILL_CLIMBER

for mode in ["a", "b"]:
    print(mode, "Running now")
    phc = PARALLEL_HILL_CLIMBER(mode)
    phc.Evolve()
    np.save("fitness_table_" + mode, phc.fitness_scores)
    np.save("trajectories_" + mode, phc.trajectories)

    phc.Show_Best()
    time.sleep(15)


#for i in [0, 1, 2, 3, 4]:
#    os.system("python3 generate.py")
#    os.system("python3 simulate.py")