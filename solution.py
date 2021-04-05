import pyrosim.pyrosim as pyrosim
import constants as c
import random
import numpy
import os

class SOLUTION:
    def __init__(self):
        self.weights = numpy.random.random(size=(3,2))
        self.weights * 2 - 1

    def Evaluate(self, argDG):
        self.Create_World()
        self.Create_Body()
        self.Create_Brain()
        if argDG == "DIRECT":
            os.system("python3 simulate.py DIRECT")
        else:
            os.system("python3 simulate.py GUI")
        f = open("fitness.txt", "r")
        self.fitness = float(f.read())
        print("FITNESS: ",self.fitness)
        f.close()

    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")

        length = 1
        width = 2
        height = 3

        x = 4
        y = 4
        z = 1.5

        pyrosim.Send_Cube(name="Box", pos=[x, y, z], size=[length, width, height])
        pyrosim.End()

    def Create_Body(self):
        pyrosim.Start_URDF("body.urdf")

        pyrosim.Send_Cube(name="Torso", pos=[c.x, c.y, c.z], size=[c.length, c.width, c.height])
        pyrosim.Send_Joint(name="Torso_FrontLeg", parent="Torso", child="FrontLeg", type="revolute",
                           position="0.5 0.0 1")
        pyrosim.Send_Cube(name="FrontLeg", pos=[0.5, 0.0, -0.5], size=[c.length, c.width, c.height])
        pyrosim.Send_Joint(name="Torso_BackLeg", parent="Torso", child="BackLeg", type="revolute",
                           position="-0.5 0.0 1")
        pyrosim.Send_Cube(name="BackLeg", pos=[-0.5, 0.0, -0.5], size=[c.length, c.width, c.height])
        pyrosim.End()

    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork("brain.nndf")
        pyrosim.Send_Sensor_Neuron(name=0, linkName="Torso")
        pyrosim.Send_Sensor_Neuron(name=1, linkName="BackLeg")
        pyrosim.Send_Sensor_Neuron(name=2, linkName="FrontLeg")
        pyrosim.Send_Motor_Neuron(name=3, jointName="Torso_BackLeg")
        pyrosim.Send_Motor_Neuron(name=4, jointName="Torso_FrontLeg")

        for currentRow in range(3):
            for currentColumn in range(2):
                pyrosim.Send_Synapse(sourceNeuronName=currentRow, targetNeuronName=currentColumn+3,
                                     weight=self.weights[currentRow][currentColumn])
        pyrosim.End()

    def Mutate(self):
        randomRow = random.randint(0,2)
        randomColumn = random.randint(0,1)
        self.weights[randomRow,randomColumn] = random.random() * 2 - 1


