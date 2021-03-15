import pybullet as p
import pyrosim.pyrosim as pyrosim
from sensor import SENSOR
from motor import MOTOR

class ROBOT:

    def __init__(self):
        self.body = p.loadURDF("body.urdf")
        pyrosim.Prepare_To_Simulate("body.urdf")

        self.Prepare_To_Sense()
        self.Prepare_To_Act()

    def Prepare_To_Sense(self):
        self.sensors = {}

        for linkName in pyrosim.linkNamesToIndices:
            self.sensors[linkName] = SENSOR(linkName)

    def Sense(self, timestep):
        for s in self.sensors.values():
            s.Get_Value(timestep)

    def Prepare_To_Act(self):
        self.motors = {}

        for jointName in pyrosim.jointNamesToIndices:
            self.motors[jointName] = MOTOR(jointName)

    def Act(self, timestep):
        for m in self.motors.values():
            m.Set_Value(timestep, self)