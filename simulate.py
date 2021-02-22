import pybullet as p
import pybullet_data
import time

physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

p.setGravity(0,0,-9.8)
planeId = p.loadURDF("plane.urdf")
planeId = p.loadURDF("body.urdf")

p.loadSDF("world.sdf")

for i in range(0, 999):
    p.stepSimulation()
    time.sleep(1/60)

p.disconnect()