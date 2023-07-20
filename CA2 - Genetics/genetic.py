import random
import time 

crossoverProbability = 0.7
carryPercentage = 0.1
populationSize = 30
mutationProbability = 0.05

class EquationBuilder:
    
    def __init__(self, operators, operands, equationLength, goalNumber):
        self.operators = operators
        self.operands = operands
        self.equationLength = equationLength
        self.goalNumber = goalNumber
        # Create the earliest population at the begining
        self.population = self.makeFirstPopulation()
        
    def makeFirstPopulation(self):
        population = []
        for i in range(populationSize):
            chromosome = []
            for j in range(self.equationLength):
                if j % 2 == 0:
                    chromosome.append(random.choice(self.operands))
                else:
                    chromosome.append(random.choice(self.operators))
            population.append(chromosome)
        return population
        #TODO create random chromosomes to build the early population, and return it

    def findEquation(self):
        # Create a new generation of chromosomes, and make it better in every iteration
        while (True):
            random.shuffle(self.population)

            fitnesses = []
            for i in range(populationSize):
                fitness = self.calcFitness(self.population[i])
                if fitness == 0:
                    return self.population[i]
                fitnesses.append((fitness, self.population[i])) 

            fitnesses.sort(key=lambda x: x[0], reverse = True) 
            carriedChromosomes = []
            for i in range(0, int(populationSize*carryPercentage)):
                fit , chromosome = fitnesses[populationSize - 1 -i]
                carriedChromosomes.append(chromosome) 

            # A pool consisting of potential candidates for mating (crossover and mutation)    
            matingPool = self.createMatingPool(fitnesses)

            # The pool consisting of chromosomes after crossover
            crossoverPool = self.createCrossoverPool(matingPool)

            # Delete the previous population
            self.population.clear()

            # Create the portion of population that is undergone crossover and mutation
            #for i in range(populationSize - int(populationSize*carryPercentage)):
            for i in range(populationSize - len(carriedChromosomes)):
                self.population.append(self.mutate(crossoverPool[i]))
                
            # Add the prominent chromosomes directly to next generation
            self.population.extend(carriedChromosomes)
    
    def createMatingPool(self, fitnesses):
        matingPool = []
        for i in range(populationSize):
            fitness, chromosome = fitnesses[i]
            for j in range(i+1):
                matingPool.append(chromosome)
        random.shuffle(matingPool)
        return matingPool[0:populationSize]
        
    
    def createCrossoverPool(self, matingPool):
        crossoverPool = []
        i = 0
        while i < len(matingPool)-1:
            firstParent, secondParent = matingPool[i], matingPool[i+1]
            if (random.random() > crossoverProbability):
                crossoverPool.append(firstParent)
                crossoverPool.append(secondParent)
            else:
                crossoverPoint = random.randrange(1, self.equationLength - 1)
                firstChild = firstParent[:crossoverPoint] + secondParent[crossoverPoint:]
                secondChild = secondParent[:crossoverPoint] + firstParent[crossoverPoint:]
                crossoverPool.append(firstChild)
                crossoverPool.append(secondChild)
            i += 2
        return crossoverPool[0:populationSize]
        #TODO don't perform crossover and add the chromosomes to the next generation directly to crossoverPool
        #TODO find 2 child chromosomes, crossover, and add the result to crossoverPool
             

    
    def mutate(self, chromosome):
        if random.random() > mutationProbability:
            return chromosome
        else:
            evenIndex , oddIndex = random.randrange(0, self.equationLength -1, 2), random.randrange(1, self.equationLength -1, 2)
            chromosome[evenIndex] = random.choice(self.operands)
            chromosome[oddIndex] = random.choice(self.operators)
        #TODO mutate the input chromosome 
        return chromosome

    def calcFitness(self, chromosome):
        chromosomeStr = ''.join(str(chrom) for chrom in chromosome)
        chromRes = eval(chromosomeStr)
        fitness = abs(self.goalNumber - chromRes)
        return fitness
        #TODO define the fitness measure here


operands = [1, 2, 3, 4, 5, 6, 7, 8]
operators = ['+', '-', '*']
equationLength = 21
goalNumber = 18019


equationBuilder = EquationBuilder(operators, operands, equationLength, goalNumber)
start = time.time()
equation = equationBuilder.findEquation()
print(f'Algorithm time: {time.time() - start}')

strEquarion = ''.join(str(chrom) for chrom in equation)
print(strEquarion)
