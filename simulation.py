import os
import pybullet as p
import pybullet_data
import constants as c
import time
from world import WORLD
from robot import ROBOT
import pyrosim.pyrosim as pyrosim

class SIMULATION:

    def __init__(self, directOrGUI, solutionID):
        if directOrGUI == "DIRECT":
            self.physicsClient = p.connect(p.DIRECT)
        else:
            self.physicsClient = p.connect(p.GUI)

        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0,0,-9.8)

        self.directOrGUI = directOrGUI
        self.world = WORLD()
        self.robot = ROBOT(solutionID)
        self.Run()
        os.system("rm brain"+solutionID+".nndf")


    def Run(self):
        for i in range(0, c.numSteps):
            p.stepSimulation()
            self.robot.Sense(i)
            self.robot.Think()
            self.robot.Act(i)
            if self.directOrGUI != "DIRECT":
                time.sleep(1/180)

    def __del__(self):
        p.disconnect()

    def Get_Fitness(self):
        self.robot.Get_Fitness()