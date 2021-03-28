import constants as c
import numpy
import pyrosim.pyrosim as pyrosim
class SENSOR:

    def __init__(self, linkName):
        self.linkName = linkName
        self.values = numpy.zeros(c.numSteps)

    def Get_Value(self, timestep):
        self.values[timestep] = pyrosim.Get_Touch_Sensor_Value_For_Link(self.linkName)
        #if timestep == c.numSteps-1:
        #    self.Save_Values()

    def Save_Values(self):
        numpy.save(str("data/"+self.linkName), self.values)