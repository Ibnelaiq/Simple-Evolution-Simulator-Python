import pygame
import numpy as np
import sys
import struct 
import logging 
import json



import time
from random import randint,random
from Grid import *



from Connection_String import * 

# Public variables
grid_square_size = 5
grid = []

phermones = {}
phermones[("a","a")] = "test"

birth_cell_cell = 0

# GRID SETTINGS 
x_axis = 128
y_axis = 128 


# Settings
# __start_cells = 100
# __time = 10
# This VARIABLE IS BEING USED DON"T REMOVE IT 
# _Cell__default_gene_length = 10

logname = "TICK.log"

logging.basicConfig(filename=logname,
                    filemode='w',
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level= logging.DEBUG)

# o = 0

sys.setrecursionlimit(6069)

# Update the screen
# Rnd = Random Input 0 to 1


sensory_neurons_array = ["Ag","Rnd","LSb","LNb","LEb","LWb","Osc"]

sensory_neurons_array_string = [
    ["AGE","neuro_sensory_age"],
    ["RANDOM-NUM","neuro_sensory_random"],
    ["LENGTH-SOUTH-BORDER","neuro_sensory_south_border"],
    ["LENGTH-NORTH-BORDER","neuro_sensory_north_border"],
    ["LENGTH-EAST-BORDER","neuro_sensory_east_border"],
    ["LENGTH-WEST-BORDER","neuro_sensory_west_border"],
    ["OSCILLATOR","neuro_sensory_oscillator"]
]
len_Sen_neurons = len(sensory_neurons_array)

motor_neurons_array = ["ML","MR","MU","MD","MRnd","SOsc","MAx","MAy"]
# ,"SOsc"
motor_neurons_array_string = [
    ["MOVE-LEFT","neuro_motor_left"],
    ["MOVE-RIGHT","neuro_motor_right"],
    ["MOVE-UP","neuro_motor_up"],
    ["MOVE-DOWN","neuro_motor_down"],
    ["MOVE-RANDOM","neuro_motor_random_move"],
    ["SET-OSCILLATOR","neuro_set_oscialltor_period"],
    ["MOVE-X-AXIS","neuro_motor_moveX"],
    ["MOVE-Y-AXIS","neuro_motor_moveY"]
]
# 

len_Moto_neurons = len(motor_neurons_array)

class Gene: 

    gene_length = 0
    _current_cell = None
    color = ""

    def __init__(self,cell,_gene_length,generated_gene):

        

        self._current_cell = cell

        self.sensory_neurons = []
        # [interneuron Obj, type = 0 for direct connection S-M & 1 = connection with internal neuron]
        self.inter_neurons = []
        self.motor_neurons = []
        
        self.brain_input_connections = []
        self.brain_output_connections = []

        self.gene_chunks = []
        
        # print("           Creating Genes               ")
        # print("========================================")

        for i in range(0, _gene_length):
            # 4150863785
            if generated_gene == None:

                number = randint(10**7,10**8-1)

                chunks = []
                for i in range(4):
                    number, remainder = divmod(number, 100)
                    chunks.append(remainder)           

            else:
                
                chunks = generated_gene[i]


            self.gene_chunks.append(chunks)

            # logging.info(str(chunks))
            # Working on one gene creating neuron 
            # [22,49,18,50]

            # Index 0 [22] => Sensory Nueron => Input
            # Index 1 [49] => Motor Nueron => Output
            # Index 2 [18] => InterNeuron => Central
            # Index 3 [18] =>  FOR CONDITION OF CONNECTIONS

            

         

    


            #Sensory Neuron
            current_sensory = Sensoryneuron(self.percentage_index_selection(chunks[0],len_Sen_neurons),cell)
            # logging.info(current_sensory.returnName())
            self.sensory_neurons.append(current_sensory)

            # Motor Neuron
            current_motor = MotorNeuron(self.percentage_index_selection(chunks[1],len_Moto_neurons),cell)
            # logging.info(current_motor.returnName())
            self.motor_neurons.append(current_motor)
        
            # connection_config = [1,8]

            connection_config = [int(d) for d in str(chunks[2])]
            connection_output_config = [int(d) for d in str(chunks[3])]
            
            if len(connection_config) == 1 : connection_config.append(0)
            if len(connection_output_config) == 1 : connection_output_config.append(0)

            if connection_output_config[1] % 2 == 0:
                # Even 
                # Connection (Inhibitory) Negative
                output_connection = ConnectionString(-1,chunks[2])
            
                # logging.debug("Connection OUTPUT: Connection (Inhibitory) Negative (Strength -"+str(chunks[2])+")")

            else:
            
                # Odd
                # Connection (Inhibitory) Positive
                output_connection = ConnectionString(1,chunks[2])

                # logging.debug("Connection OUTPUT: Connection (Exicitedory) Positive (Strength +"+str(chunks[2])+")")


            # if connection_config[1] % 2 == 0:
            #     # Even 
            #     # Connection (Inhibitory) Negative
            #     input_connection = ConnectionString(-1,chunks[3])
                
            #     # logging.debug("Connection INPUT: Connection (Inhibitory) Negative (Strength -"+str(chunks[3])+")")

            # else:
            #     # Odd
            #     # Connection (Inhibitory) Positive
            #     input_connection = ConnectionString(1,chunks[3])

            #     # logging.debug("Connection INPUT: Connection (Exicitedory) Positive (Strength +"+str(chunks[3])+")")


            input_connection = ConnectionString(1,chunks[3])
            # logging.debug("Connection INPUT: Connection (Exicitedory) Positive (Strength +"+str(chunks[3])+")")

            self.brain_input_connections.append(input_connection) 
            


            if connection_config[0] % 2 == 0:
                # Even
                # Connect Directly To Sensory To Motor
                self.inter_neurons.append([Interneuron(current_sensory,current_motor,0,input_connection,output_connection),0])
                
                # logging.debug("Connect Directly To Sensory To Motor")
                
            else:
                if connection_config[0] >= connection_config[1]:
                    # Create New Neuron Has Mulutplier
                    self.inter_neurons.append([Interneuron(current_sensory,current_motor,1,input_connection,output_connection),1])
                    self.brain_output_connections.append(output_connection) 
                    # logging.debug("Create New Interneuron")

                else:
                    # Connect To Existing One
                    len_in_neu = len(self.inter_neurons)
                    if len_in_neu > 0:
                        # logging.debug("Connection To Exisiting Neuron")
                        Ineuron = self.inter_neurons[self.percentage_index_selection(chunks[2],len_in_neu)]

                        # Checking if the neuron is just a transmitter or have some strength
                        if Ineuron[1] == 0: 
                            # Selected Neuron is just transmitter can't be connected 

                            # logging.debug("Create New I-Neuron Cause Selected Interneuron Is Transmitter")
                            self.inter_neurons.append([Interneuron(current_sensory,current_motor,1,input_connection,output_connection),1])
                            self.brain_output_connections.append(output_connection) 

                        else:
                            Ineuron[0].addInput(current_sensory,input_connection)
                            # logging.debug("Connected To Exisiting Neuron"+ str(Ineuron))
                    else:
                        # No existing Neurons
                        # logging.debug("Create New I-Neuron Cause There is no another")
                        self.inter_neurons.append([Interneuron(current_sensory,current_motor,1,input_connection,output_connection),1])
                        self.brain_output_connections.append(output_connection) 

        
      

        # log("=================== CELL BRAIN STATS ================")

        # log("","Motor Neurons: "+str(len(self.motor_neurons)))
        
        # log("","Sensory Neurons: "+str(len(self.sensory_neurons)))

        # interneuron_count = 0

        # for x in self.inter_neurons:
        #     if(x[1] == 1):
        #         interneuron_count += 1
        
        # log("","Inter Neurons: "+str(interneuron_count))

        # log("","Brain INPUT Connections: "+str(len(self.brain_input_connections)))

        # log("","Brain OUTPUT Connections: "+str(len(self.brain_output_connections)))

        
    
    def gene_color(self):
        return self.numbers_to_rgb(self.gene_chunks)



    def numbers_to_rgb(self,chunks ):
        # Initialize variables
        r, g, b = 0, 0, 0
        # Iterate through the list of numbers
        for num in chunks:
            
            # Add the values to the r, g, and b variables
            r += int(num[0])
            g += int(num[1])
            b += int((num[2] + num[3]) / 2)

        # Divide by n to get the average values
        r = r // _Cell__default_gene_length
        g = g // _Cell__default_gene_length
        b = b // _Cell__default_gene_length

        r -= 20
        g += 50
        # b += b_brightness_value

        r = min(255, max(0, r))
        g = min(255, max(0, g))
        b = min(255, max(0, b)) 

        # Return the RGB color as a tuple
        return (r, g, b)
        
    

    def tick(self):
        # logging.critical("GENE TICK")
        i = 0
        for x in self.inter_neurons:
            # logging.critical("CALLING INTER-NEURON => "+str(i) + "TICK")
            x[0].process()
            # logging.critical("ENDED INTER-NEURON => "+str(i) + "TICK")
            i += 1
            
        

    def percentage_index_selection(self, percentage, array_len):
        # calculate the index using the given percentage
        return int(percentage * array_len / 100)

class Sensoryneuron:

    type_index = 0
    type_code  = ""
    type_string = "" 

    _current_cell = None
    
    method_string = ""
    # Functions 
    METHOD_Age = ""




    def __init__(self,index,cell):
        self.type_index    = index
        self.type_code     = sensory_neurons_array[index]
        self.type_string   = sensory_neurons_array_string[index][0]
        self.method_string = sensory_neurons_array_string[index][1]
        self._current_cell = cell

        
        # print(self.type_string)

    # Return Name For Debugging
    def returnName(self):
        return self.type_string

    # Output for InterNeuron
    def giveInput(self):
        method = getattr(self._current_cell,self.method_string)
        return method()

class MotorNeuron:

    type_index = 0
    type_code  = ""
    type_string = "" 
    
    method_string = ""

    _current_cell = None
    
    def __init__(self,index,cell):
        self.type_index    = index
        self.type_code     = motor_neurons_array[index]
        self.type_string   = motor_neurons_array_string[index][0]
        self.method_string = motor_neurons_array_string[index][1]
        self._current_cell = cell


    # Return Name For Debugging
    def returnName(self):
        return self.type_string

    # Output for InterNeuron
    def do_action(self,flag):
        
        _flag = 1
        
        if self.method_string == "neuro_motor_moveX" or self.method_string == "neuro_motor_moveY" or self.method_string == "neuro_set_oscialltor_period": 
            if flag <= 0.5:
                _flag = -1
            

        method = getattr(self._current_cell,self.method_string)
        
        return method(str(_flag))

class Interneuron:
    
    input_neurons = []
    output_neuron = 0
    output = 0

    # If 0 it is neutral just work as a transfer 
    # If 1 Has multiplier Get Multiple From Connection

    connection_type = 0
    input_connection_string = []
    # If this is none than just work as a transfer
    output_connection_string = None

    def __init__(self,sensory_neurons,motor_neuron,type,_input_connection_string,output_connection_string):

        self.input_connection_string = []
        self.input_neurons           = []

        self.input_neurons.append(sensory_neurons)
        self.output_neuron = motor_neuron
        self.connection_type = type

        self.input_connection_string = []
        
        self.input_connection_string.append(_input_connection_string)

        # print(self.input_connection_string)

        if type == 1:
            self.output_connection_string = output_connection_string

        


    def addInput(self,SensoryNeuron,connection):
        
        self.input_neurons.append(SensoryNeuron)
        self.input_connection_string.append(connection)
        
 
    # Called Each Tick From GENE 
    def process(self):
        
        index = 0 
        output = 0
        for S_neuron in self.input_neurons:

            input_connection = self.input_connection_string[index]

            # Get Strength Input 
            # Input from Cell * Strength Of Input Connection
            
            output += input_connection.calculateInput(S_neuron.giveInput())
            index += 1
            
        if random() <= output:
            # Direct To Motor
            if(self.output_connection_string == None):
                self.output_neuron.do_action(output)
            else: 
                # Do Some Stringijasdhjasldk heheh

                if random() <= self.output_connection_string.get_strength():
                    self.output_neuron.do_action(output)

        # print(output)
        
        
class Cell:
    x = 0
    y = 0
    rect = 0
    color = (0,0,0)
    lifetime = 0

    gene = None
    gene_chunks = None
    
    phermones_index = 0
    
    _creation_time = 0
    _oscilator_count = 0 

    type = ""
    
    # gene_len = global __default_gene_length
    # DEFAULT VALUES


    DEFAULT_OSC_FREQUENCY = 5

    def __init__(self,_x,_y,_lifetime, generated_gene,type = "CELL"):

        self.x = _x
        self.y = _y
        self.type = type
        self.lifetime = _lifetime
        self._creation_time = time.time()

        
        
        # THIS WILL NOT RETURN AN ERROR
        if type == "CELL":
            
            self.gene = Gene(self,__default_gene_length,generated_gene)

            self.gene_chunks = self.gene.gene_chunks

            self.color = self.gene.gene_color()

            


        self.rect = pygame.Rect(self.x*grid_square_size,self.y*grid_square_size,grid_square_size,grid_square_size)



    
    def tick(self):
        # logging.critical("CELL GENE TICK STARTED")
        self.gene.tick()
        # logging.critical("CELL GENE TICK ENDED")


    def draw_cell(self):

        self.rect = pygame.Rect(self.x*grid_square_size,self.y*grid_square_size,grid_square_size,grid_square_size)
        
        
        # Update Pheromone AXIS
        
        

        grid[int(self.x)][int(self.y) ] = 1


      
      
        
        pygame.draw.rect(screen,self.color, self.rect,0)
        # pygame.display.update()
        # pygame.display.flip()
        
    def move(self, flag ):

        old_rect = self.rect.copy()

        phermones[(self.x,self.y)] = self.gene_chunks

        old_x = self.x
        old_y = self.y
        

        match flag:
            case 1: 
                # Moving up 
                
                if(self.y == 0):
                    return
                

                if(grid[int(self.x)][int(self.y - 1)] > 0 ):
                    return

                
                grid[int(self.x)][int(self.y)] = 0

                self.rect.move_ip(0,1 * - grid_square_size)
                self.y = (self.rect.y / grid_square_size) 

                

            case 2: 
                # Moving Right
                

                if(self.x == (x_axis - 1)):
                    return
                    
                if(grid[int(self.x + 1)][int(self.y)] > 0):
                    return

                grid[int(self.x)][int(self.y)] = 0

                self.rect.move_ip(1 * grid_square_size,0)
                self.x = (self.rect.x / grid_square_size) 

               
                
                    

            case 3: 
                # Moving Down
                if(self.y == (y_axis - 1)):
                    return

           
                if(grid[int(self.x)][int(self.y + 1)] > 0):
                    return

                grid[int(self.x)][int(self.y)] = 0

                self.rect.move_ip(0,1 * grid_square_size)
                self.y = (self.rect.y / grid_square_size) 
                
            case 4: 
                # Moving Left
                if(self.x == 0):
                    return
                

                if(grid[int(self.x - 1)][int(self.y)] > 0):
                    return
                

                grid[int(self.x)][int(self.y)] = 0  
                
                self.rect.move_ip(1 * -grid_square_size,0)
                self.x = (self.rect.x / grid_square_size) 


        phermones[(self.x,self.y)] = phermones.pop((old_x,old_y))

        screen.blit(bg,old_rect)

        self.draw_cell()

    def update_grid(self,x,y):
        grid[int(x)][int(y)] = 1

    def birth_cell(self):

        # If is taken 
        if(grid[self.x][self.y] > 0 ):

            self.x = randint(0,(x_axis - 1))
            self.y = randint(0,(y_axis - 1))
            # self.x  = 5

            self.birth_cell()
        
        phermones[(self.x,self.y)] = self.gene_chunks
        return True
    
    # SENSORY NEURONS
    # Return Age in Ranging 0 to +1
    def neuro_sensory_age(self):
        current_time = time.time()
        value =  ( current_time - self._creation_time ) / self.lifetime
        val = clamp(value,0,1)
        return val

    # Return: Random Output between 0 to +1
    def neuro_sensory_random(self):
        rnd_number = np.random.rand()
        return rnd_number

    # Return: How much cell is close to south border => 0 to +1
    def neuro_sensory_south_border(self):
        return clamp(self.y / (y_axis - 1),0,1)

    # Return: How much cell is close to north border => 0 to +1
    def neuro_sensory_north_border(self):
        _y = (y_axis - 1) - self.y
        return clamp(_y / (y_axis - 1),0,1)

    # Return: How much cell is close to east border => 0 to +1
    def neuro_sensory_east_border(self):
        return clamp(self.x / (x_axis - 1),0,1)

    # Return: How much cell is close to west border => 0 to +1
    def neuro_sensory_west_border(self):
        _x = (x_axis - 1) - self.x
        return clamp(_x / (x_axis - 1),0,1)

    # Return: Positive signal per oscillator frequency
    def neuro_sensory_oscillator(self):
        self._oscilator_count += 1
        if self._oscilator_count == self.DEFAULT_OSC_FREQUENCY:
            self._oscilator_count = 0
            return 1
        else:
            return 0


    # MOTOR NEURONS

    # Move in x Axis
    def neuro_motor_moveX(self,flag):
        # Move Forward
        if(flag == 1):
            self.neuro_motor_right()
        elif(flag == -1):
            self.neuro_motor_left()

    # Move in x Axis
    def neuro_motor_moveY(self,flag):
        # Move Forward
        if(flag == 1):
            self.neuro_motor_up()
        elif(flag == -1):
            self.neuro_motor_down()


    # Move To Right
    def neuro_motor_right(self,flag = ""):
        self.move(2)
    # Move To Left
    def neuro_motor_left(self,flag = ""):
        self.move(4)
    # Move To Up
    def neuro_motor_up(self,flag = ""):
        self.move(1)
    # Move To Down
    def neuro_motor_down(self,flag = ""):
        self.move(3)
  
    # Move In Random Direction
    def neuro_motor_random_move(self,flag = ""):
        
        random_int = randint(1,4)

        match random_int:
            case 1:
                self.neuro_motor_up()
            case 2:
                self.neuro_motor_right()
            case 3:
                self.neuro_motor_down()
            case 4:
                self.neuro_motor_left()

    def neuro_set_oscialltor_period(self,flag = ""):
        if flag != "":
            self.DEFAULT_OSC_FREQUENCY += int(flag)

def log(title = "", param = ""):
    if(title != ""):
        print("==================="+ title +"===================")
    print(param)

def clamp(n, smallest, largest): 
    return sorted((smallest,n, largest))[1]

# Initialize pygame
pygame.init()

# Set the screen size
screen = pygame.display.set_mode((700, 800))
# screen = pygame.display.set_mode((200, 700))

screen.fill("white")
# Font for text
myfont = pygame.font.SysFont(None, 20)



# BG for updation 
bg = pygame.Surface((grid_square_size,grid_square_size))
bg.fill((255,255,255))
rect = bg.get_rect()
border_width = 5
pygame.draw.rect(bg, (200, 204, 201),rect, 1)

# Cells and Grids Public

cells = []
gave_birth = 0


_time = 0




def init(start_cells, generation_alive_time, generation_genes = None ):
    global __MUTATION_PERCENT
    __MUTATION_PERCENT /= 100

    global _time
    _time = 0

    global cells
    cells = []

    global grid
    grid = []
    grid = createGrid(x_axis,y_axis,grid_square_size,screen)

    # logging.info("Initalizing")
    screen.fill("white")
    increment_generation()
    
    global gave_birth

    gave_birth = 0

    starting = start_cells if generation_genes == None else len(generation_genes)

    draw_walls()
    
    def generate_cell(x,_generation_genes): 
        selected_x = randint(0,(x_axis - 1))
        selected_y = randint(0,(y_axis - 1))

        if(x == -1):
            has_gene = _generation_genes
        else:
            has_gene = None if _generation_genes == None else _generation_genes[x]

        cell = Cell(selected_x,selected_y,generation_alive_time,has_gene)

        

        if(cell.birth_cell()):

            cells.append(cell)
            cell.draw_cell()
            global gave_birth
            gave_birth = gave_birth + 1 
            pygame.display.flip()

            
    for x in range(starting):
        generate_cell(x,generation_genes)

    if(starting != start_cells):
        
        left_cells = start_cells - starting
        _gen = len(generation_genes) - 1
        for x in range(left_cells):
            rnd = randint(0, _gen)
            generate_cell(-1,generation_genes[rnd])



    
    log("==================== GENERATION CREATED ===================")
    
    log("Cells: "+ str(gave_birth))




  

    run = True
    clock = pygame.time.Clock()
    
    global __TOTAL_ITERATIONS
    TOTAL_ITERATIONS = __TOTAL_ITERATIONS

    global __TICKS_PER_SECOND 
    TICKS_PER_SECOND = __TICKS_PER_SECOND
    


    
    

    

    while True:
        create_survivable_area()
        pygame.event.get()

        if(TOTAL_ITERATIONS <= 0):

            if(run == False): continue
            # Pause TICKKING GENERATION 
            
            run = False
            # RUN REPORT ONCE
            create_survivable_area()

            

            survived_cells = [] 


            for cell in cells:
                # LEFT AND RIGHT
                # if(cell.x < 20 or cell.x > (128-20)):
                # BOTTOM HORIZONTAL
                # if(cell.y >= 108):
                # MIDDLE
                # if(cell.y >= 58 and cell.y <=  78):
                # LEFT VERTICAL 
                if(cell.x < 20 ):
                    survived_cells.append([
                                cell.x,
                                cell.y])

            total_survived_cells = len(survived_cells)
           

            # 1. Create two arrays, "parent1_genes" and "parent2_genes", that represent the genes of the two parent cells.
            # 2. Create an empty array, "offspring_genes", that will be used to store the genes of the offspring.
            # 3. Use a loop to iterate through the genes of both parent arrays. 
            # 4. For each iteration, randomly select a gene from either the "parent1_genes" or "parent2_genes" array and add it to the "offspring_genes" array.
            # 5. Before adding the selected gene to the "offspring_genes" array, calculate a random number between 0 and 1. If this number is less than your desired mutation rate, change the selected gene to a random value.
            # 6. Continue the loop until all genes from both parent arrays have been added to the "offspring_genes" array.
            # 7. The "offspring_genes" array now contains the genes of the offspring, which is a combination of the genes from both parent cells with the possibility of mutations.
            
            # EACH CELL -> NEXT GEN GENES 
            next_gen = []

            total    = 0
            defeated = 0 
            found    = 0

            # logging.critical(phermones.keys())
            for male in survived_cells:
                total += 1
                male_gene = phermones[(male[0],male[1])]
                fe_male_gene = get_rnd_adj(male[0],male[1],10)

                if fe_male_gene == None:
                    defeated += 1
                else:
                    found += 1
                    next_gen.append(generate_offspring_gene(male_gene,fe_male_gene))
                
                
                
                

                

            log("Survived Cell: "+ str(total_survived_cells))
            log("Mutations "+ str(MUTATION_COUNT))


            # log("==RES==")
            # log("Total => ",str(total))
            # log("Defeated => ",str(defeated))
            # log("Found => ",str(found))

            # with open("GENERATION-BRAINS.json", 'w+', encoding='utf-8') as fw:
            #     json.dump(next_gen, fw, ensure_ascii=False, indent=4)
            

            init(__start_cells,__time,next_gen)

            
        else:
            # print(TOTAL_ITERATIONS)
            # TICK
            for cell in cells: 
                cell.tick()
            
            pygame.display.flip()

            clock.tick(TICKS_PER_SECOND)

            TOTAL_ITERATIONS -= 1 
        




def get_rnd_adj(x,y,depth = 10):
    # print(depth)
    if(depth <= 0):
        return None

    # x = int (x)
    # y = int (y)
    rnd = randint(0,3)
    
    match rnd:
        case 0:
            arr = (x, 0 if y - 1 == 0 else y - 1)
        case 1: 
            arr = ( (x_axis - 1) if x + 1 == x_axis else x + 1,y)
        case 2:
            arr = (x, (y_axis - 1) if y + 1 == y_axis else y + 1)
        case 3:
            arr = (0 if x-1 == 0 else x - 1,y)

    # logging.debug(str(arr))

    try:
        return phermones[arr]
    except KeyError:
        depth -=1 
        get_rnd_adj(x,y,depth) 

    # if "a,a" not in phermones.keys():

    #     depth -= 1
        
    #     get_rnd_adj(x,y,depth) 

    # else:
    #     return phermones[arr]
        


def generate_offspring_gene(malegene,femalegene): 
    # print("asd"+ str(malegene)+str(femalegene))
    offspring_gene = []

    # 10 GENE PER CELL 
    for index in range(_Cell__default_gene_length):
        
        gene = []        
        
        for i in range(4):

            _rnd = randint(0,1)
            rnd = randint(0,_Cell__default_gene_length - 1 )  
            
            # Mutataion 
            if random() < __MUTATION_PERCENT:
                # MUTATES

                global MUTATION_COUNT
                MUTATION_COUNT += 1 

                rnd_gene = randint(0,99)
                gene.append(rnd_gene)
                # print("mutates")

            else:
                if _rnd == 1:
                    
                    gene.append(malegene[rnd][randint(0,3)])

                # FEMALE
                else:
                    
                    gene.append(femalegene[rnd][randint(0,3)]) 

        offspring_gene.append(gene)

    return offspring_gene
 
def draw_survivable_area(start_x,start_y,end_x,end_y):
    
    survivable_area = pygame.Rect(start_x * grid_square_size,start_y * grid_square_size,end_x * grid_square_size,end_y * grid_square_size)

    pygame.draw.rect(screen, (34,139,34), survivable_area, 1)

    pygame.display.flip()

def draw_walls():
    # pass
    wall_x = 20
    for wall_y in range(64):
        
        wall = Cell(wall_x,wall_y,10,None,"WALL")

        if(wall.birth_cell()):
            wall.draw_cell()


    
    
def create_survivable_area():
    # LEFT VERTICAL 
    draw_survivable_area(0,0,20,128)
    # RIGHT VERTICAL 
    # draw_survivable_area(128 - 20,0,20,128)
    # BOTTOM HORIZONTAL
    # draw_survivable_area(0,128 - 20,128,20)

    # draw_survivable_area(0,58,128,20)
    



# init 
# Param 1 : Start Cells : Inital Cells 
# Param 2 : Alive Time : Generation Lifetime in Seconds  -- TICKS = seconds * 8 

# THESE VARIABLE ARE BEING USED DON"T REMOVE THEM 
__start_cells = 2000

__time = 20

__GENERATION = 1 

_Cell__default_gene_length = 30

__TOTAL_ITERATIONS = 200  

# IN PERCENT LIKE IF 20 then 20 / 100 = 0.2 chance

__MUTATION_PERCENT = 1  

MUTATION_COUNT   = 0
# 10 seconds at 20 fps TOTAL FRAMES FOR EACH GENE

__TICKS_PER_SECOND = 20
def increment_generation():
    global __GENERATION

    label = myfont.render("GENERATION #: "+ str(__GENERATION), 1, (24,0,0))

    screen.blit(label, (100, 650))

    __GENERATION += 1 




init(__start_cells,__time)

