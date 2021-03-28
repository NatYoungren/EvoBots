import pyrosim.pyrosim as pyrosim
import constants as c
import random
def Create_World():
    pyrosim.Start_SDF("world.sdf")

    length = 1
    width = 2
    height = 3

    x = 4
    y = 4
    z = 1.5

    pyrosim.Send_Cube(name="Box", pos=[x, y, z], size=[length, width, height])
    pyrosim.End()

def Generate_Body():
    pyrosim.Start_URDF("body.urdf")

    pyrosim.Send_Cube(name="Torso", pos=[c.x, c.y, c.z], size=[c.length, c.width, c.height])
    pyrosim.Send_Joint(name="Torso_FrontLeg", parent="Torso", child="FrontLeg", type="revolute", position="0.5 0.0 1")
    pyrosim.Send_Cube(name="FrontLeg", pos=[0.5, 0.0, -0.5], size=[c.length, c.width, c.height])
    pyrosim.Send_Joint(name="Torso_BackLeg", parent="Torso", child="BackLeg", type="revolute", position="-0.5 0.0 1")
    pyrosim.Send_Cube(name="BackLeg", pos=[-0.5, 0.0, -0.5], size=[c.length, c.width, c.height])
    pyrosim.End()

def Generate_Brain():
    pyrosim.Start_NeuralNetwork("brain.nndf")
    pyrosim.Send_Sensor_Neuron(name=0, linkName="Torso")
    pyrosim.Send_Sensor_Neuron(name=1, linkName="BackLeg")
    pyrosim.Send_Sensor_Neuron(name=2, linkName="FrontLeg")
    pyrosim.Send_Motor_Neuron(name=3, jointName="Torso_BackLeg")
    pyrosim.Send_Motor_Neuron(name=4, jointName="Torso_FrontLeg")

    for i in [0,1,2]:
        for j in [3,4]:
            pyrosim.Send_Synapse(sourceNeuronName=i, targetNeuronName=j, weight=random.random())

    pyrosim.End()

Create_World()
Generate_Body()
Generate_Brain()
#Create_Robot()