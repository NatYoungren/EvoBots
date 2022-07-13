from solution import SOLUTION
import constants as c
import copy
import os
import numpy as np

class PARALLEL_HILL_CLIMBER:
    def __init__(self, m):
        os.system("rm brain*.nndf")
        os.system("rm fitness*.txt")
        self.mode = m
        self.nextAvailableID = 0
        self.parents = {}

        self.fitness_scores = np.zeros(shape=(c.populationSize, c.numberOfGenerations))
        self.generationNum = 0

        self.trajectories = np.zeros(shape=(c.numberOfGenerations, c.numSteps, 3))

        for i in range(0, c.populationSize):
            self.parents[i] = SOLUTION(self.nextAvailableID)
            self.nextAvailableID += 1

    def Evolve(self):
        self.Evaluate(self.parents)
        # self.parent.Evaluate("DIRECT")
        for currentGeneration in range(c.numberOfGenerations):
            self.Evolve_For_One_Generation()

    def Evolve_For_One_Generation(self):
        self.Spawn()
        self.Mutate()
        self.Evaluate(self.children)
        self.Print()
        self.Select()
        self.generationNum += 1


    def Spawn(self):
        self.children = {}
        for i in self.parents.keys():
            self.children[i] = copy.deepcopy(self.parents[i])
            self.children[i].Set_ID(self.nextAvailableID)
            self.nextAvailableID += 1

    def Mutate(self):
        for i in self.children.keys():
            self.children[i].Mutate()

    def Select(self):
        index = 0
        for i in self.parents.keys():
            self.fitness_scores[index][self.generationNum] = self.parents[i].fitness
            index += 1
            if self.parents[i].fitness > self.children[i].fitness:
                self.parents[i] = self.children[i]

    def Add_Trajectory(self):
        lowestFitness = self.parents[0]
        for p in self.parents.values():
            if p.fitness < lowestFitness.fitness:
                winner = p

        print(type(lowestFitness))
        print(lowestFitness.fitness)

        self.trajectories[self.generationNum] = lowestFitness.trajectory

    def Show_Best(self):
        lowestFitness = self.parents[0]
        for i in self.parents.values():
            if i.fitness < lowestFitness.fitness:
                lowestFitness = i
        print("Lowest:", lowestFitness.fitness)
        lowestFitness.Start_Simulation("GUI", self.mode)

    def Evaluate(self, solutions):
        for p in solutions.keys():
            solutions[p].Start_Simulation("DIRECT", self.mode)
        for p in solutions.keys():
            solutions[p].Wait_For_Simulation_To_End()

    def Print(self):
        for i in self.parents.keys():
            print("\n",i,self.parents[i].fitness, self.children[i].fitness)
