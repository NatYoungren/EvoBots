import os
from hillclimber import HILL_CLIMBER

hc = HILL_CLIMBER()
hc.parent.Evaluate("GUI")
hc.Evolve()
hc.Show_Best()


#for i in [0, 1, 2, 3, 4]:
#    os.system("python3 generate.py")
#    os.system("python3 simulate.py")