import pybullet as p
import pybullet_data
import constants as c
import time
from world import WORLD
from robot import ROBOT
import pyrosim.pyrosim as pyrosim

class SIMULATION:

    def __init__(self):
        self.physicsClient = p.connect(p.GUI)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0,0,-9.8)

        self.world = WORLD()
        self.robot = ROBOT()

    def Run(self):
        for i in range(0, c.numSteps):
            p.stepSimulation()
            self.robot.Sense(i)
            self.robot.Think()
            self.robot.Act(i)
            time.sleep(1/60)

        def __del__(self):
            p.disconnect()