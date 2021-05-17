import numpy

numSteps = 1200
numberOfGenerations = 15
populationSize = 10

numSensorNeurons = 4
numHiddenNeurons = 4
numMotorNeurons = 8

motorJointRange = 0.4
maxForce = 100

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