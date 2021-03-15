import constants as c
import pyrosim.pyrosim as pyrosim
import pybullet as p
import numpy
class MOTOR:

    def __init__(self, jointName):
        self.jointName = jointName
        self.Prepare_To_Act()

    def Prepare_To_Act(self):
        self.amplitude = c.frontLeg_amplitude
        self.frequency = c.frontLeg_frequency
        self.offset = c.frontLeg_phaseOffset

        if self.jointName == "Torso_BackLeg":
            self.frequency *= 0.5

        self.motorValues = numpy.linspace(-numpy.pi, numpy.pi, c.numSteps)
        for i in range(0, c.numSteps):
            self.motorValues[i] = self.amplitude * numpy.sin(
                self.frequency * self.motorValues[i] + self.offset)

    def Set_Value(self, timestep, robot):
        pyrosim.Set_Motor_For_Joint(
            bodyIndex=robot.body,
            jointName=self.jointName,
            controlMode=p.POSITION_CONTROL,
            targetPosition=self.motorValues[timestep],
            maxForce=100)

    def Save_Values(self):
        numpy.save(str("data/"+self.jointName), self.motorValues)
