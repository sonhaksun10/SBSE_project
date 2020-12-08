DEBUG = False

#Main function variables
TEST_PGM = ['sed']
NUM_VERSIONS = {'sed':7}
NUM_TESTCASES = {'sed':360}
#TRIALS_PER_VERSION = 30
TRIALS_PER_VERSION = 2
TRY_ALGORITHM = ['NSGA2','SPEA2','TAEA']
RESULT_DIRECTORY = "../Result/"

#Genetic algorithm variables
#POP = 250
POP = 20
MAX_IT = 30
FIT_FUNC_GENERATED = True
LARGE = 999999999999

CROSSOVER_RATE = 0.9
MUTATION_RATE = 0.1

# TAEA only
MAX_ARCHIVE_TAEA: int = 2 * POP
CA_DA_RATIO = 0.5

#NGSA-3
reference = [[0.9,0.9,0.9],[0.95,0.8,0.88],[0.87,0.96,0.84],[0.79,0.92,0.93],[0.82,0.90,0.96]] #example reference pt

#SPEA2
MAX_ARCHIVE_SPEA2: int = POP