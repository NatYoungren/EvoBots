import pyrosim.pyrosim as pyrosim

pyrosim.Start_SDF("boxes.sdf")

length = 1
width = 1
height = 1

z = 0.5
scalar = 1
for x in range(0,8,1):
    for y in range(0,8,1):
        for layer in range(0, 10):

            pyrosim.Send_Cube(name=str("Box"+str(layer)), pos=[x, y, z], size=[scalar * length, scalar * width, scalar * height])
            z += scalar/2 + scalar/2*0.9
            scalar *= 0.9
        z = 0.5
        scalar = 1



pyrosim.End()