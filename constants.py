import numpy

numSteps = 2000
numberOfGenerations = 40
populationSize = 20

numSensorNeurons = 4
numHiddenNeurons = 4
numMotorNeurons = 8

motorJointRange = 0.6
maxForce = 200

frontLeg_amplitude = numpy.pi / 2
frontLeg_frequency = 25
frontLeg_phaseOffset = 0

backLeg_amplitude = numpy.pi/2
backLeg_frequency = 0
backLeg_phaseOffset = numpy.pi/4

length = 1
width = 1
height = 1


# Torso coordinates
x = 0
y = 0
z = 1