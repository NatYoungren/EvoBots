import constants as c
import pyrosim.pyrosim as pyrosim
import pybullet as p
import numpy
class MOTOR:

    def __init__(self, jointName):
        self.jointName = jointName

    def Set_Value(self, desiredAngle, robot):
        pyrosim.Set_Motor_For_Joint(
            bodyIndex=robot.robot,
            jointName=self.jointName,
            controlMode=p.POSITION_CONTROL,
            targetPosition=desiredAngle,
            maxForce=c.maxForce)