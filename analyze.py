import numpy
import matplotlib.pyplot

backLeg_targetAngles = numpy.load("data/backLeg_targetAngles.npy")

frontLeg_targetAngles = numpy.load("data/frontLeg_targetAngles.npy")
#backLegSensorValues = numpy.load("data/backLegSensorValues.npy")

#frontLegSensorValues = numpy.load("data/frontLegSensorValues.npy")


matplotlib.pyplot.plot(backLeg_targetAngles, label="BackLeg", linewidth = 2.5)
matplotlib.pyplot.plot(frontLeg_targetAngles, label="FrontLeg", linewidth = 2)

#matplotlib.pyplot.plot(frontLegSensorValues, label="FrontLeg")

matplotlib.pyplot.legend()
matplotlib.pyplot.show()