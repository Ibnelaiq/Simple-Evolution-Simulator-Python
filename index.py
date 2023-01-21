import pygame
import numpy as np
import sys
import struct 
import logging 



import time
from random import randint,random
from Grid import *



from Connection_String import * 

# Public variables
grid_square_size = 10
grid = []
birth_cell_cell = 0


# Settings
__start_cells = 2000
__time = 10
_Cell__default_gene_length = 2

logname = "DEBUGGING.log"

logging.basicConfig(filename=logname,
                    filemode='w',
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

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

motor_neurons_array = ["ML","MR","MU","MD","MRnd","MAx","MAy"]
# ,"SOsc"
motor_neurons_array_string = [
    ["MOVE-LEFT","neuro_motor_left"],
    ["MOVE-RIGHT","neuro_motor_right"],
    ["MOVE-UP","neuro_motor_up"],
    ["MOVE-DOWN","neuro_motor_down"],
    ["MOVE-RANDOM","neuro_motor_random_move"],
    
    ["MOVE-X-AXIS","neuro_motor_moveX"],
    ["MOVE-Y-AXIS","neuro_motor_moveY"]
]

# ["SET-OSCILLATOR","neuro_set_oscialltor_period"],

len_Moto_neurons = len(motor_neurons_array)




class Gene: 

    gene_length = 0
    _current_cell = None

    def __init__(self,cell,_gene_length):

        

        self._current_cell = cell

        self.sensory_neurons = []
        # [interneuron Obj, type = 0 for direct connection S-M & 1 = connection with internal neuron]
        self.inter_neurons = []
        self.motor_neurons = []
        
        self.brain_input_connections = []
        self.brain_output_connections = []
        
        print("           Creating Genes               ")
        print("========================================")

        for i in range(0, _gene_length):
            # 4150863785
            number = randint(10**7,10**8-1)

            logging.info("GENE:"+ str(number))
            
            

            
            # Dividing GENE into digtis
            chunks = []
            for i in range(4):
                number, remainder = divmod(number, 100)
                chunks.append(remainder)



            logging.info(str(chunks))
            # Working on one gene creating neuron 
            # [22,49,18,50]

            # Index 0 [22] => Sensory Nueron => Input
            # Index 1 [49] => Motor Nueron => Output
            # Index 2 [18] => InterNeuron => Central



            #Sensory Neuron
            current_sensory = Sensoryneuron(self.percentage_index_selection(chunks[0],len_Sen_neurons),cell)
            logging.info(current_sensory.returnName())
            self.sensory_neurons.append(current_sensory)

            # Motor Neuron
            current_motor = MotorNeuron(self.percentage_index_selection(chunks[1],len_Moto_neurons),cell)
            logging.info(current_motor.returnName())
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
            
                logging.debug("Connection OUTPUT: Connection (Inhibitory) Negative (Strength -"+str(chunks[2])+")")

            else:
            
                # Odd
                # Connection (Inhibitory) Positive
                output_connection = ConnectionString(1,chunks[2])

                logging.debug("Connection OUTPUT: Connection (Exicitedory) Positive (Strength +"+str(chunks[2])+")")


            # if connection_config[1] % 2 == 0:
            #     # Even 
            #     # Connection (Inhibitory) Negative
            #     input_connection = ConnectionString(-1,chunks[3])
                
            #     logging.debug("Connection INPUT: Connection (Inhibitory) Negative (Strength -"+str(chunks[3])+")")

            # else:
            #     # Odd
            #     # Connection (Inhibitory) Positive
            #     input_connection = ConnectionString(1,chunks[3])

            #     logging.debug("Connection INPUT: Connection (Exicitedory) Positive (Strength +"+str(chunks[3])+")")


            input_connection = ConnectionString(1,chunks[3])
            logging.debug("Connection INPUT: Connection (Exicitedory) Positive (Strength +"+str(chunks[3])+")")

            self.brain_input_connections.append(input_connection) 
            


            if connection_config[0] % 2 == 0:
                # Even
                # Connect Directly To Sensory To Motor
                self.inter_neurons.append([Interneuron(current_sensory,current_motor,0,input_connection,output_connection),0])
                
                logging.debug("Connect Directly To Sensory To Motor")
                
            else:
                if connection_config[0] >= connection_config[1]:
                    # Create New Neuron Has Mulutplier
                    self.inter_neurons.append([Interneuron(current_sensory,current_motor,1,input_connection,output_connection),1])
                    self.brain_output_connections.append(output_connection) 
                    logging.debug("Create New Interneuron")

                else:
                    # Connect To Existing One
                    len_in_neu = len(self.inter_neurons)
                    if len_in_neu > 0:
                        logging.debug("Connection To Exisiting Neuron")
                        Ineuron = self.inter_neurons[self.percentage_index_selection(chunks[2],len_in_neu)]

                        # Checking if the neuron is just a transmitter or have some strength
                        if Ineuron[1] == 0: 
                            # Selected Neuron is just transmitter can't be connected 

                            logging.debug("Create New I-Neuron Cause Selected Interneuron Is Transmitter")
                            self.inter_neurons.append([Interneuron(current_sensory,current_motor,1,input_connection,output_connection),1])
                            self.brain_output_connections.append(output_connection) 

                        else:
                            Ineuron[0].addInput(current_sensory,input_connection)
                            logging.debug("Connected To Exisiting Neuron"+ str(Ineuron))
                    else:
                        # No existing Neurons
                        logging.debug("Create New I-Neuron Cause There is no another")
                        self.inter_neurons.append([Interneuron(current_sensory,current_motor,1,input_connection,output_connection),1])
                        self.brain_output_connections.append(output_connection) 


        log("=================== CELL BRAIN STATS ================")

        log("","Motor Neurons: "+str(len(self.motor_neurons)))
        
        log("","Sensory Neurons: "+str(len(self.sensory_neurons)))

        interneuron_count = 0

        for x in self.inter_neurons:
            if(x[1] == 1):
                interneuron_count += 1
        
        log("","Inter Neurons: "+str(interneuron_count))

        log("","Brain INPUT Connections: "+str(len(self.brain_input_connections)))

        log("","Brain OUTPUT Connections: "+str(len(self.brain_output_connections)))

        

    def tick(self):
        

        for x in self.inter_neurons:
            x[0].process()
        

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

        
        print(self.type_string)

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
        
        if self.method_string == "neuro_motor_moveX" or self.method_string == "neuro_motor_moveY": 
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

    def __init__(self,sensory_neurons,motor_neuron,type,input_connection_string,output_connection_string):
        self.input_neurons.append(sensory_neurons)
        self.output_neuron = motor_neuron
        self.connection_type = type
        
        self.input_connection_string.append(input_connection_string)
        if type == 1:
            self.output_connection_string = output_connection_string

        


    def addInput(self,SensoryNeuron,connection):
        
        self.input_neurons.append(SensoryNeuron)
        self.input_connection_string.append(connection)
        
 
    # Called Each Tick From GENE 
    def process(self):
        
        index = 0 
        for S_neuron in self.input_neurons:

            input_connection = self.input_connection_string[index]

            # Get Strength Input 
            # Input from Cell * Strength Of Input Connection
            output = input_connection.calculateInput(S_neuron.giveInput())
            
            if random() <= output:
                # Direct To Motor
                if(self.output_connection_string == None):
                    self.output_neuron.do_action(output)
                else: 
                    # Do Some Stringijasdhjasldk heheh

                    if random() <= self.output_connection_string.get_strength():
                        self.output_neuron.do_action(output)

                index += 1
                # print(output)
                # return S_neuron.giveInput()


        
class Cell:
    x = 0
    y = 0
    rect = 0
    color = (0,0,0)
    lifetime = 0

    gene = None

    _creation_time = 0
    _oscilator_count = 0 
    # gene_len = global __default_gene_length
    # DEFAULT VALUES


    DEFAULT_OSC_FREQUENCY = 5

    def __init__(self,_x,_y,_lifetime,_color = (0,0,0) ):
        self.x = _x
        self.y = _y
        self.lifetime = _lifetime
        self._creation_time = time.time()
        
        self.color = _color
        
        self.gene = Gene(self,__default_gene_length)

        self.rect = pygame.Rect(self.x*grid_square_size,self.y*grid_square_size,grid_square_size,grid_square_size)
    
    def tick(self):
        self.gene.tick()


    def draw_cell(self):

        self.rect = pygame.Rect(self.x*grid_square_size,self.y*grid_square_size,grid_square_size,grid_square_size)

        grid[int(self.x)][int(self.y) ] = 1
      
      
        
        pygame.draw.rect(screen,self.color, self.rect,0)
        pygame.display.update()
        
    def move(self, flag ):

        old_rect = self.rect.copy()

        match flag:
            case 1: 
                # Moving up 
                
                if(self.y == 0):
                    return
                

                if(grid[int(self.x)][int(self.y - 1)] > 0 ):
                    return

                
                grid[int(self.x)][int(self.y)] = 0

                self.rect.move_ip(0,1 * -10)
                self.y = (self.rect.y / 10) 

                

            case 2: 
                # Moving Right
                

                if(self.x == 63):
                    return
                    
                if(grid[int(self.x + 1)][int(self.y)] > 0):
                    return

                grid[int(self.x)][int(self.y)] = 0

                self.rect.move_ip(1 * 10,0)
                self.x = (self.rect.x / 10) 

               
                
                    

            case 3: 
                # Moving Down
                if(self.y == 63):
                    return

           
                if(grid[int(self.x)][int(self.y + 1)] > 0):
                    return

                grid[int(self.x)][int(self.y)] = 0

                self.rect.move_ip(0,1 * 10)
                self.y = (self.rect.y / 10) 
                
            case 4: 
                # Moving Left
                if(self.x == 0):
                    return
                

                if(grid[int(self.x - 1)][int(self.y)] > 0):
                    return
                

                grid[int(self.x)][int(self.y)] = 0  
                
                self.rect.move_ip(1 * -10,0)
                self.x = (self.rect.x / 10) 

                

        screen.blit(bg,old_rect)
        self.draw_cell()

    def update_grid(self,x,y):
        grid[int(x)][int(y)] = 1

    def birth_cell(self):

        # If is taken 
        if(grid[self.x][self.y] > 0 ):

            self.x = randint(0,63)
            self.y = randint(0,63)
            # self.x  = 5

            self.birth_cell()
            
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
        return clamp(self.y / 63,0,1)

    # Return: How much cell is close to north border => 0 to +1
    def neuro_sensory_north_border(self):
        _y = 63 - self.y
        return clamp(_y / 63,0,1)

    # Return: How much cell is close to east border => 0 to +1
    def neuro_sensory_east_border(self):
        return clamp(self.x / 63,0,1)

    # Return: How much cell is close to west border => 0 to +1
    def neuro_sensory_west_border(self):
        _x = 63 - self.x
        return clamp(_x / 63,0,1)

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

    def neuro_set_oscialltor_period(self,min,max):
        self.DEFAULT_OSC_FREQUENCY = randint(min,max)




        



    













    
   

def log(title = "", param = ""):
    if(title != ""):
        print("==================="+ title +"===================")
    print(param)



def clamp(n, smallest, largest): 
    return sorted((smallest,n, largest))[1]





# Initialize pygame
pygame.init()

# Set the screen size
screen = pygame.display.set_mode((1000, 700))
# screen = pygame.display.set_mode((200, 700))

screen.fill("white")
# Font for text
myfont = pygame.font.SysFont(None, 20)

# Create GRID 
x_axis = 64
y_axis = 64 
grid = createGrid(x_axis,y_axis,grid_square_size,screen)
# BG for updation 
bg = pygame.Surface((grid_square_size,grid_square_size))
bg.fill((255,255,255))
rect = bg.get_rect()
border_width = 5
pygame.draw.rect(bg, (200, 204, 201),rect, 1)




# Cells and Grids Public
cells = grid
cells = []
gave_birth = 0


_time = 0


# wall_x = 3
# for wall_y in range(64):
#     wall = Cell(wall_x,wall_y,(144,144,144))

#     if(wall.birth_cell()):
#         wall.draw_cell()

def init(start_cells, generation_alive_time ):

    logging.info("Initalizing")

    gave_birth = 0
    for x in range(start_cells):

        selected_x = randint(0,63)
        selected_y = randint(0,63)
        logging.info("Creating Cell")
        cell = Cell(selected_x,selected_y,generation_alive_time)
        logging.info("Cell Created")

        
        
        if(cell.birth_cell()):
            cells.append(cell)
            cell.draw_cell()
            gave_birth = gave_birth + 1 

    pygame.display.update()

    label = myfont.render("Total Cells: "+ str(gave_birth), 1, (0,0,0))

    screen.blit(label, (700, 100))

    run = True
    clock = pygame.time.Clock()
    


    global _time

    while run:
        pygame.event.get()

        _time += clock.tick(1)
        
        # for e in pygame.event.get():
        #     if e.type == pygame.QUIT:
        #         run = False
        # 8 ticks per second
        if((_time / (generation_alive_time * 100)) > generation_alive_time):
            run = False
        # print(_time / 800)
        

        tick()
        
        
        
        pygame.display.flip()

    survived_cells = []
    if(run == False):
        for cell in cells:
            if(cell.x < 20 or cell.x > 43):
                survived_cells.append(cell)
    
        

    log("==================== RESULT ===================")
    log("Survived Cell: "+ str(len(survived_cells)))
    print(survived_cells)

    

    



def tick():
    
    for cell in cells: 
        cell.tick()
    


    



# init 
# Param 1 : Start Cells : Inital Cells 
# Param 2 : Alive Time : Generation Lifetime in Seconds  -- TICKS = seconds * 8 



init(__start_cells,__time)

