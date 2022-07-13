import pyrosim.pyrosim as pyrosim
import constants as c
import random
import numpy
import os
import time

class SOLUTION:
    def __init__(self, ID):
        self.myID = ID
        self.weightsA1 = numpy.random.random(size=(c.numSensorNeurons, c.numHiddenNeurons))
        self.weightsA2 = numpy.random.random(size=(c.numHiddenNeurons, c.numMotorNeurons))
        self.weightsA1 * 2 - 1
        self.weightsA2 * 2 - 1

        self.weightsB = numpy.random.random(size=(c.numSensorNeurons, c.numMotorNeurons))
        self.weightsB * 2 - 1


    def Start_Simulation(self, directOrGUI, mode):
        self.Create_World()
        self.Create_Body()
        self.Create_Brain(mode)
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

        length = 0.1
        width = 3
        height = 1

        x = -2.5
        y = 0
        z = 0.5
        for i in range(4):
            pyrosim.Send_Cube(name="Door1" + str(i), pos=[x - (i * 3.5), y-1.65, z], size=[length, width, height])
            pyrosim.Send_Cube(name="Door2" + str(i), pos=[x - (i * 3.5), y+1.65, z], size=[length, width, height])
        pyrosim.End()

    def Create_Body(self):
        pyrosim.Start_URDF("body.urdf")

        pyrosim.Send_Cube(name="Torso", pos=[0, 0, 1], size=[1, 1, 1])

        pyrosim.Send_Joint(name="Torso_FrontLeg", parent="Torso", child="FrontLeg", type="revolute",
                           position="0 0.5 1", jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="FrontLeg", pos=[0, 0.5, 0], size=[0.2, 1, 0.2])
        pyrosim.Send_Joint(name="Torso_BackLeg", parent="Torso", child="BackLeg", type="revolute",
                           position="0 -0.5 1", jointAxis = "0 1 0")
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
                           position="0 -1 0", jointAxis="0 1 0")
        pyrosim.Send_Cube(name="BackLowerLeg", pos=[0, 0, -0.5], size=[0.2, 0.2, 1])
        pyrosim.Send_Joint(name="LeftLeg_LeftLowerLeg", parent="LeftLeg", child="LeftLowerLeg", type="revolute",
                           position="-1 0 0", jointAxis="0 1 0")
        pyrosim.Send_Cube(name="LeftLowerLeg", pos=[0, 0, -0.5], size=[0.2, 0.2, 1])
        pyrosim.Send_Joint(name="RightLeg_RightLowerLeg", parent="RightLeg", child="RightLowerLeg", type="revolute",
                           position="1 0 0", jointAxis="0 1 0")
        pyrosim.Send_Cube(name="RightLowerLeg", pos=[0, 0, -0.5], size=[0.2, 0.2, 1])

        pyrosim.End()

    def Create_Brain(self, testMode: str):
        brainName = "brain" + str(self.myID)+".nndf"
        pyrosim.Start_NeuralNetwork(brainName)
        #sensorNames = ["Torso", "BackLeg", "FrontLeg", "LeftLeg", "RightLeg", "FrontLowerLeg", "BackLowerLeg", "LeftLowerLeg", "RightLowerLeg"]
        sensorNames = ["FrontLowerLeg", "BackLowerLeg",
                       "LeftLowerLeg", "RightLowerLeg"]
        neuronCount = 0
        for sensor in sensorNames:
            pyrosim.Send_Sensor_Neuron(name=neuronCount, linkName=sensor)
            neuronCount += 1

        if testMode.upper() == "A":
            for _ in range(0, c.numHiddenNeurons):
                pyrosim.Send_Hidden_Neuron(name=neuronCount)
                neuronCount += 1


        motorNames = ["Torso_BackLeg", "Torso_FrontLeg", "Torso_LeftLeg", "Torso_RightLeg", "FrontLeg_FrontLowerLeg",
                      "BackLeg_BackLowerLeg", "LeftLeg_LeftLowerLeg", "RightLeg_RightLowerLeg"]

        for motor in motorNames:
            pyrosim.Send_Motor_Neuron(name=neuronCount, jointName=motor)
            neuronCount += 1
        if testMode.upper() == "A":
            for currentRow in range(c.numSensorNeurons):
                for currentColumn in range(c.numHiddenNeurons):
                    pyrosim.Send_Synapse(sourceNeuronName=currentRow, targetNeuronName=currentColumn+c.numSensorNeurons,
                                         weight=self.weightsA1[currentRow][currentColumn])

            for currentRow in range(c.numHiddenNeurons):
                for currentColumn in range(c.numMotorNeurons):
                    pyrosim.Send_Synapse(sourceNeuronName=currentRow+c.numSensorNeurons,
                                         targetNeuronName=currentColumn+c.numSensorNeurons+c.numHiddenNeurons,
                                         weight=self.weightsA2[currentRow][currentColumn])
        else:
            for currentRow in range(c.numSensorNeurons):
                for currentColumn in range(c.numMotorNeurons):
                    pyrosim.Send_Synapse(sourceNeuronName=currentRow, targetNeuronName=currentColumn + c.numSensorNeurons,
                                   weight=self.weightsB[currentRow][currentColumn])

        pyrosim.End()


    def Mutate(self):
        for _ in range(0,random.randint(1, 6)):
            if random.randint(0, 1):
                row = random.randint(0, c.numSensorNeurons-1)
                col = random.randint(0, c.numHiddenNeurons-1)
                self.weightsA1[row, col] = random.random() * 2 - 1
            else:
                row = random.randint(0, c.numHiddenNeurons-1)
                col = random.randint(0, c.numMotorNeurons-1)
                self.weightsA2[row, col] = random.random() * 2 - 1

            row = random.randint(0, c.numSensorNeurons - 1)
            col = random.randint(0, c.numMotorNeurons - 1)
            self.weightsB[row, col] = random.random() * 2 - 1

    def Set_ID(self, ID):
        self.myID = ID