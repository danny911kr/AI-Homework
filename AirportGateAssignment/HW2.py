#CSCI561 HW2 Lee Dong Ho
#Airport Gate Assignment Problem

import random

AIR = 0
LANDING = 1
GATE = 2
TAKING_OFF = 3
COMPLETE = 4

class Airport:

    def __init__(self):
        self.time_step = 0
        self.landing_num = 0
        self.gate_num = 0
        self.taking_off_num = 0
        self.airplane_num = 0
        self.airplanes = {}
        self.max_time = 0
        self.time_schedule = None
        self.remain_ranges = []
        self.service_ranges = []

    def setEnvironment(self, inputFile):
        inputData = open(inputFile, 'r')

        # first row L,G,T
        LGTline = inputData.readline().rstrip('\n').split()
        self.landing_num = int(LGTline[0])
        self.gate_num = int(LGTline[1])
        self.taking_off_num = int(LGTline[2])

        # second row airplane_num
        self.airplane_num = int(inputData.readline().rstrip('\n'))

        # parse the text file into the list
        for i in range(self.airplane_num):
            RMSOC = inputData.readline().rstrip('\n').split()
            self.airplanes[i] = [int(RMSOC[0]), int(RMSOC[1]), int(RMSOC[2]), int(RMSOC[3]), int(RMSOC[4])]
            current_value = int(RMSOC[0])+int(RMSOC[1])+int(RMSOC[3])+int(RMSOC[4])
            if current_value > self.max_time:
                self.max_time = current_value

            self.remain_ranges.append([0,int(RMSOC[0])])
            self.service_ranges.append([int(RMSOC[2]), int(RMSOC[4])])

    # solution looks like... [i,j]-> i : remaining fuel / j : service time
    def fitness(self, solution):
        correct = 0
        false = 0
        self.time_schedule = [[-1 for col in range(self.max_time)] for row in range(self.airplane_num)]
        for i in range(self.airplane_num):
            for j in range(0, solution[i][0]):
                self.time_schedule[i][j] = AIR
            for j in range(solution[i][0], solution[i][0]+self.airplanes[i][1]):
                self.time_schedule[i][j] = LANDING
            for j in range(solution[i][0]+self.airplanes[i][1], solution[i][0]+self.airplanes[i][1]+solution[i][1]):
                self.time_schedule[i][j] = GATE
            for j in range(solution[i][0]+self.airplanes[i][1]+solution[i][1], solution[i][0]+self.airplanes[i][1]+solution[i][1]+self.airplanes[i][3]):
                self.time_schedule[i][j] = TAKING_OFF
            for j in range(solution[i][0] + self.airplanes[i][1] + solution[i][1] + self.airplanes[i][3], self.max_time):
                self.time_schedule[i][j] = COMPLETE

        for j in range(self.max_time):
            air = 0
            landing = 0
            gate = 0
            takeoff = 0
            complete = 0
            for i in range(self.airplane_num):
                if self.time_schedule[i][j] == AIR:
                    air += 1
                elif self.time_schedule[i][j] == LANDING:
                    landing += 1
                elif self.time_schedule[i][j] == GATE:
                    gate += 1
                elif self.time_schedule[i][j] == TAKING_OFF:
                    takeoff += 1
                elif self.time_schedule[i][j] == COMPLETE:
                    complete += 1
            if landing <= min(self.airplane_num,self.landing_num) and gate <= min(self.airplane_num,self.gate_num) and takeoff <= min(self.taking_off_num, self.airplane_num) or correct == self.airplane_num:
                correct += 1
            else:
                false += 1
        return false

    def initial_population(self, population_size, remain_ranges, service_ranges):
        population = []
        for i in range(population_size):
            rand_solution = []
            for j in range(len(remain_ranges)):
                minimum_r = remain_ranges[j][0]    # remain_fuel minimum
                maximum_r = remain_ranges[j][1]    # remain_fuel maximum
                minimum_s = service_ranges[j][0]   # service minimum
                maximum_s = service_ranges[j][1]   # service maximum (until complain)
                rand_solution.append([random.randint(minimum_r, maximum_r), random.randint(minimum_s, maximum_s)])
            population.append(rand_solution)
        return population

    def mutate(self, solution, remain_ranges, service_ranges):
        mutate_position = random.randint(0, len(solution) - 1)

        # get random flight from available flights
        minimum_r = remain_ranges[mutate_position][0]  # remain_fuel minimum
        maximum_r = remain_ranges[mutate_position][1]  # remain_fuel maximum
        minimum_s = service_ranges[mutate_position][0]  # service minimum
        maximum_s = service_ranges[mutate_position][1]  # service maximum (until complain)

        random_r = random.randint(minimum_r, maximum_r)
        random_s = random.randint(minimum_s, maximum_s)

        solution[mutate_position][0] = random_r
        solution[mutate_position][1] = random_s

        return solution

    def crossover(self, solution1, solution2):
        cross_position = random.randint(1, len(solution1) - 2)
        return solution1[0:cross_position] + solution2[cross_position:]

    def genetic_optimize(self, population, fitness, mutate, crossover, mutate_prob, elite):
        stop = 0
        population_size = len(population)
        top_elite = int(elite * population_size)
        end_signal = True

        while end_signal:
            gene_scores = [(fitness(v), v) for v in population]
            gene_scores.sort()
            print(gene_scores)
            if gene_scores[0][0] == 0:
                end_signal = False
                break
            if stop > 3:
                return None

            ranked_individuals = [v for (s,v) in gene_scores]
            population = ranked_individuals[0:top_elite]

            while len(population) < population_size:
                if random.random() < mutate_prob:
                    c = random.randint(0, top_elite)
                    population.append(mutate(ranked_individuals[c],self.remain_ranges,self.service_ranges))
                else:
                    c1 = random.randint(0, top_elite)
                    c2 = random.randint(0, top_elite)
                    population.append(crossover(ranked_individuals[c1], ranked_individuals[c2]))

            stop += 1
        # returns the best solution
        return gene_scores[0][1]

    def execute(self, file):
        self.setEnvironment(file)
        population = self.initial_population(self.airplane_num*10, self.remain_ranges, self.service_ranges)
        best = self.genetic_optimize(population, self.fitness, self.mutate, self.crossover, 0.2 , 0.2)
        while best == None:
            best = self.genetic_optimize(population, self.fitness, self.mutate, self.crossover, 0.2, 0.2)
        self.outputfile(best)
        return best

    # def printout(self, solution):
    #     self.time_schedule = [[0 for col in range(self.max_time)] for row in range(self.airplane_num)]
    #     for i in range(self.airplane_num):
    #         for j in range(0, solution[i][0]):
    #             self.time_schedule[i][j] = AIR
    #         for j in range(solution[i][0], solution[i][0] + self.airplanes[i][1]):
    #             self.time_schedule[i][j] = LANDING
    #         for j in range(solution[i][0] + self.airplanes[i][1],
    #                        solution[i][0] + self.airplanes[i][1] + solution[i][1]):
    #             self.time_schedule[i][j] = GATE
    #         for j in range(solution[i][0] + self.airplanes[i][1] + solution[i][1],
    #                        solution[i][0] + self.airplanes[i][1] + solution[i][1] + self.airplanes[i][3]):
    #             self.time_schedule[i][j] = TAKING_OFF
    #         for j in range(solution[i][0] + self.airplanes[i][1] + solution[i][1] + self.airplanes[i][3],
    #                        self.max_time):
    #             self.time_schedule[i][j] = COMPLETE
    #
    #     for i in self.time_schedule:
    #         print(i)

    def outputfile(self, solution):
        output_file = open("output.txt", "w")
        for i in range(self.airplane_num):
            land = solution[i][0]
            takeoff = solution[i][0] + self.airplanes[i][1] + solution[i][1]
            output_file.write(str(land) + " " + str(takeoff))
            output_file.write("\n")

        output_file.close()

airport = Airport()
best_schedule = airport.execute('input3.txt')





