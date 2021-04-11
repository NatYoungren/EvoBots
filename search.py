import os
from parallelHillClimber import PARALLEL_HILL_CLIMBER

phc = PARALLEL_HILL_CLIMBER()
# phc.parent.Evaluate("GUI")
phc.Evolve()
phc.Show_Best()


#for i in [0, 1, 2, 3, 4]:
#    os.system("python3 generate.py")
#    os.system("python3 simulate.py")