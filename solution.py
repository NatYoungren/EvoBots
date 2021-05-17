import pyrosim.pyrosim as pyrosim
import constants as c
import random
import numpy
import os
import time

class SOLUTION:
    def __init__(self, ID):
        self.myID = ID
        self.weights1 = numpy.random.random(size=(c.numSensorNeurons,c.numHiddenNeurons))
        self.weights2 = numpy.random.random(size=(c.numHiddenNeurons,c.numMotorNeurons))
        self.weights1 * 2 - 1
        self.weights2 * 2 - 1

    def Start_Simulation(self, directOrGUI):
        self.Create_World()
        self.Create_Body()
        self.Create_Brain()
        IDstr = str(self.myID)
        os.system("python3 simulate.py " + directOrGUI + " " + IDstr + " 2&>1 &")

    def Wait_For_Simulation_To_End(self):
        fileName = "fitness" + str(self.myID) + ".txt"
        while not os.path.exists(fileName):
            time.sleep(0.01)
        f = open(fileName, "r")
        self.fitness = float(f.read())
        print("FITNESS " + str(self.myID) + ": ", self.fitness)
        f.close()
        os.system("rm " + fileName)

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

        pyrosim.Send_Cube(name="Torso", pos=[0, 0, 1], size=[1, 1, 1])

        pyrosim.Send_Joint(name="Torso_FrontLeg", parent="Torso", child="FrontLeg", type="revolute",
                           position="0 0.5 1", jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="FrontLeg", pos=[0, 0.5, 0], size=[0.2, 1, 0.2])
        pyrosim.Send_Joint(name="Torso_BackLeg", parent="Torso", child="BackLeg", type="revolute",
                           position="0 -0.5 1", jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="BackLeg", pos=[0, -0.5, 0], size=[0.2, 1, 0.2])
        pyrosim.Send_Joint(name="Torso_LeftLeg", parent="Torso", child="LeftLeg", type="revolute",
                           position="-0.5 0 1", jointAxis="0 1 0")
        pyrosim.Send_Cube(name="LeftLeg", pos=[-0.5, 0, 0], size=[1, 0.2, 0.2])
        pyrosim.Send_Joint(name="Torso_RightLeg", parent="Torso", child="RightLeg", type="revolute",
                           position="0.5 0 1", jointAxis="0 1 0")
        pyrosim.Send_Cube(name="RightLeg", pos=[0.5, 0, 0], size=[1, 0.2, 0.2])

        pyrosim.Send_Joint(name="FrontLeg_FrontLowerLeg", parent="FrontLeg", child="FrontLowerLeg", type="revolute",
                           position="0 1 0", jointAxis="1 0 0")
        pyrosim.Send_Cube(name="FrontLowerLeg", pos=[0, 0, -0.5], size=[0.2, 0.2, 1])
        pyrosim.Send_Joint(name="BackLeg_BackLowerLeg", parent="BackLeg", child="BackLowerLeg", type="revolute",
                           position="0 -1 0", jointAxis="1 0 0")
        pyrosim.Send_Cube(name="BackLowerLeg", pos=[0, 0, -0.5], size=[0.2, 0.2, 1])
        pyrosim.Send_Joint(name="LeftLeg_LeftLowerLeg", parent="LeftLeg", child="LeftLowerLeg", type="revolute",
                           position="-1 0 0", jointAxis="0 1 0")
        pyrosim.Send_Cube(name="LeftLowerLeg", pos=[0, 0, -0.5], size=[0.2, 0.2, 1])
        pyrosim.Send_Joint(name="RightLeg_RightLowerLeg", parent="RightLeg", child="RightLowerLeg", type="revolute",
                           position="1 0 0", jointAxis="0 1 0")
        pyrosim.Send_Cube(name="RightLowerLeg", pos=[0, 0, -0.5], size=[0.2, 0.2, 1])

        pyrosim.End()

    def Create_Brain(self):
        brainName = "brain" + str(self.myID)+".nndf"
        pyrosim.Start_NeuralNetwork(brainName)
        #sensorNames = ["Torso", "BackLeg", "FrontLeg", "LeftLeg", "RightLeg", "FrontLowerLeg", "BackLowerLeg", "LeftLowerLeg", "RightLowerLeg"]
        sensorNames = ["FrontLowerLeg", "BackLowerLeg",
                       "LeftLowerLeg", "RightLowerLeg"]
        neuronCount = 0
        for sensor in sensorNames:
            pyrosim.Send_Sensor_Neuron(name=neuronCount, linkName=sensor)
            neuronCount += 1

        for _ in range(0, c.numHiddenNeurons):
            pyrosim.Send_Hidden_Neuron(name=neuronCount)
            neuronCount += 1

        motorNames = ["Torso_BackLeg", "Torso_FrontLeg", "Torso_LeftLeg", "Torso_RightLeg", "FrontLeg_FrontLowerLeg",
                      "BackLeg_BackLowerLeg", "LeftLeg_LeftLowerLeg", "RightLeg_RightLowerLeg"]

        for motor in motorNames:
            pyrosim.Send_Motor_Neuron(name=neuronCount, jointName=motor)
            neuronCount += 1

        for currentRow in range(c.numSensorNeurons):
            for currentColumn in range(c.numHiddenNeurons):
                pyrosim.Send_Synapse(sourceNeuronName=currentRow, targetNeuronName=currentColumn+c.numSensorNeurons,
                                     weight=self.weights1[currentRow][currentColumn])

        for currentRow in range(c.numHiddenNeurons):
            for currentColumn in range(c.numMotorNeurons):
                pyrosim.Send_Synapse(sourceNeuronName=currentRow+c.numSensorNeurons,
                                     targetNeuronName=currentColumn+c.numSensorNeurons+c.numHiddenNeurons,
                                     weight=self.weights2[currentRow][currentColumn])
        pyrosim.End()


    def Mutate(self):
        for _ in range(0,random.randint(0, 3)):
            randomRow = random.randint(0,c.numSensorNeurons-1)
            randomColumn = random.randint(0,c.numHiddenNeurons-1)
            self.weights1[randomRow,randomColumn] = random.random() * 2 - 1

        for _ in range(0,random.randint(0, 3)):
            randomRow = random.randint(0, c.numHiddenNeurons-1)
            randomColumn = random.randint(0, c.numMotorNeurons-1)
            self.weights2[randomRow, randomColumn] = random.random() * 2 - 1

    def Set_ID(self, ID):
        self.myID = ID