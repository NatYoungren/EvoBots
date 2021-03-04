import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
import random
import time
import numpy

numSteps = 1000

frontLeg_amplitude = numpy.pi / 2
frontLeg_frequency = 25
frontLeg_phaseOffset = 0

backLeg_amplitude = numpy.pi/2
backLeg_frequency = 0
backLeg_phaseOffset = numpy.pi/4

backLegSensorValues = numpy.zeros(numSteps)
frontLegSensorValues = numpy.zeros(numSteps)

frontLeg_targetAngles = numpy.linspace(-numpy.pi, numpy.pi, numSteps)
for i in range(0, numSteps):
    frontLeg_targetAngles[i] = frontLeg_amplitude * numpy.sin(frontLeg_frequency * frontLeg_targetAngles[i] + frontLeg_phaseOffset)

backLeg_targetAngles = numpy.linspace(-numpy.pi, numpy.pi, numSteps)
for i in range(0, numSteps):
    backLeg_targetAngles[i] = backLeg_amplitude * numpy.sin(backLeg_frequency * backLeg_targetAngles[i] + backLeg_phaseOffset)

#numpy.save("data/frontLeg_targetAngles", frontLeg_targetAngles)
#numpy.save("data/backLeg_targetAngles", backLeg_targetAngles)

physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

p.setGravity(0,0,-9.8)
planeId = p.loadURDF("plane.urdf")
robot = p.loadURDF("body.urdf")

p.loadSDF("world.sdf")
pyrosim.Prepare_To_Simulate("body.urdf")


for i in range(0, numSteps):
    pyrosim.Set_Motor_For_Joint(
        bodyIndex=robot,
        jointName="Torso_BackLeg",
        controlMode=p.POSITION_CONTROL,
        targetPosition=backLeg_targetAngles[i],
        maxForce=100)
    pyrosim.Set_Motor_For_Joint(
        bodyIndex=robot,
        jointName="Torso_FrontLeg",
        controlMode=p.POSITION_CONTROL,
        targetPosition=frontLeg_targetAngles[i],
        maxForce=100)
    p.stepSimulation()
    backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
    frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")
    time.sleep(1/60)

p.disconnect()
numpy.save("data/backLegSensorValues", backLegSensorValues)
numpy.save("data/frontLegSensorValues", frontLegSensorValues)