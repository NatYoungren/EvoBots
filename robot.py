import pybullet as p
import pyrosim.pyrosim as pyrosim
from pyrosim.neuralNetwork import NEURAL_NETWORK
from sensor import SENSOR
from motor import MOTOR
import os

class ROBOT:

    def __init__(self, solutionID):
        self.robot = p.loadURDF("body.urdf")
        self.myID = solutionID
        pyrosim.Prepare_To_Simulate("body.urdf")
        fileName = "brain"+str(self.myID)+".nndf"
        self.nn = NEURAL_NETWORK(fileName)
        #os.system("rm " + fileName)

        self.Prepare_To_Sense()
        self.Prepare_To_Act()


    def Prepare_To_Sense(self):
        self.sensors = {}

        for linkName in pyrosim.linkNamesToIndices:
            self.sensors[linkName] = SENSOR(linkName)

    def Sense(self, timestep):
        for s in self.sensors.values():
            s.Get_Value(timestep)

    def Think(self):
        self.nn.Update()
        #self.nn.Print()

    def Prepare_To_Act(self):
        self.motors = {}

        for jointName in pyrosim.jointNamesToIndices:
            self.motors[jointName] = MOTOR(jointName)

    def Act(self, timestep):
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
                desiredAngle = self.nn.Get_Value_Of(neuronName)
                self.motors[jointName].Set_Value(desiredAngle, self)
                #print(neuronName, jointName, desiredAngle)

    def Get_Fitness(self):
        stateOfLinkZero = p.getLinkState(self.robot, 0)
        positionOfLinkZero = stateOfLinkZero[0]
        xCoordinateOfLinkZero = positionOfLinkZero[0]
        print(xCoordinateOfLinkZero)
        tmpFileName = "tmp"+str(self.myID)+".txt"
        fileName = "fitness"+str(self.myID)+".txt"
        f = open(tmpFileName, "w")
        f.write(str(xCoordinateOfLinkZero))
        f.close()
        os.system("mv "+tmpFileName + " "+ fileName)