"""
_|      _|    _|_|    _|_|_|_|_|  _|    _|  _|_|_|      _|_|    _|            _|_|_|  _|_|_|_|  _|        _|_|_|_|    _|_|_|  _|_|_|_|_|  _|_|_|    _|_|    _|      _|      _|_|_|  _|_|_|  _|      _|  
_|_|    _|  _|    _|      _|      _|    _|  _|    _|  _|    _|  _|          _|        _|        _|        _|        _|            _|        _|    _|    _|  _|_|    _|    _|          _|    _|_|  _|_|  
_|  _|  _|  _|_|_|_|      _|      _|    _|  _|_|_|    _|_|_|_|  _|            _|_|    _|_|_|    _|        _|_|_|    _|            _|        _|    _|    _|  _|  _|  _|      _|_|      _|    _|  _|  _|  
_|    _|_|  _|    _|      _|      _|    _|  _|    _|  _|    _|  _|                _|  _|        _|        _|        _|            _|        _|    _|    _|  _|    _|_|          _|    _|    _|      _|  
_|      _|  _|    _|      _|        _|_|    _|    _|  _|    _|  _|_|_|_|    _|_|_|    _|_|_|_|  _|_|_|_|  _|_|_|_|    _|_|_|      _|      _|_|_|    _|_|    _|      _|    _|_|_|    _|_|_|  _|      _|  
                                                                                                                                                                                                        
                                                                      _|_|_|_|_|                                                                                    _|_|_|_|_|       
"""
try:
    import pygame
    import random
    import time
    import math
    import json
    import sys
    import os
    import threading
    from datetime import datetime
    import pickle
except:
    #triggers if not all libraries are installed, only non native is pygame
    print("you do not have the required libraries to run this program")
    sys.exit()

#define default json values to load
default = {'layer-1': {'food': 2000, 'herbivores': 10, 'carnivores': 10}}

if os.path.exists(os.getcwd() + "/config.json"):
    #if config file exists
    Config = json.load(open(os.getcwd() + "/config.json","r"))
    
else:
    #if it doesnt
    file = open(os.getcwd() + "/config.json", "a")
    json.dump(default, file)
    file.close()
    Config = json.load(open(os.getcwd() + "/config.json","r"))
    print(f"new config file created at {os.getcwd()}")

if not os.path.exists(os.getcwd() + "/simulations"):
    os.mkdir(os.getcwd() + "/simulations")
    print(f"created a new simulations folder in {os.getcwd()}.")
    
    
#initialise fonts and displays
pygame.init()
panel = pygame.display.set_mode((1700,800),pygame.NOFRAME)
screen_size = panel.get_size()
font_alt = pygame.font.Font('freesansbold.ttf', 12)
ui_font_scale_3 = pygame.font.Font('freesansbold.ttf', 10)
big = pygame.font.Font('freesansbold.ttf', 40)

if os.path.exists(os.getcwd() + "/logo.png"):
    #if logo.png dir exists
    dvd = pygame.image.load('logo.png')
    #set the size,otherwise would take up the whole screen
    dvd = pygame.transform.scale(dvd, (100, 50))
    
else:
    #if it doesnt
    print("logo.png not found")
    #use rendered text from font glyphs instead
    dvd = big.render("logo.png is missing, please download it", True, (0,0,255))
    
img_size = dvd.get_rect().size

#define logo variables to controls movement
x = random.randint(150, 1540)
y = random.randint(150, 640)
x_speed = 1.5
y_speed = 1.5

#define color variables for ui elements
foreground = (30,30,30)
vgui_fore = (50,50,50)
vgui_bounding = (120,120,120)
vgui_state_0 = (10,10,220)
vgui_state_1 = (20,20,200)
vgui_state_2 = (20,20,180)
vgui_state_3 = (20,20,150)
vgui_state_4 = (20,20,120)
vgui_state_5 = (20,20,80)
vgui_important = (0,0,0)
vgui_aux_text_internal = (200,200,200)
vgui_aux_text_external = (200,200,200)
vgui_warning_1 = (150,20,20)
vgui_color_ON = (0,255,0)
vgui_color_OFF = (255,0,0)

#ray colours
vgui_ray_broken = (250,0,0)
vgui_ray_beam = (0,255,0)

#entity colours
vgui_group_fore = (190,190,190)
vgui_entity_herbivore = (0,250,0)
vgui_herbivore_egg = (221,100,221)
vgui_entity_dead = (70,70,70)
vgui_entity_carnivore = (250,0,0)
vgui_entity_nose = (0,0,0)

#define enttity object lists
entity_object_array = []
hunter_object_array = []
food_object_array = []
producer_object_array = []
egg_object_array = []
log_index = []

#initialise variables for sim
tab = 0
lag_comp = 0
t2p = 0
GPP = 0
NPP = 0
GSP = 0
TSC = 0
BMI = 0
PE = 0
tick = 0
balance = 0

#saved simulations
saved_simulations =  os.listdir(os.getcwd() + "/simulations")
saved_simulations = saved_simulations[::-1]
if not saved_simulations:
    saved_simulations = ["no stored simulations!"]
#genetic code variables
bases = ["G","A","T","C"]

#metric lists
SIGHT_SAMPLES = []
BMR_SAMPLES = []
SPEED_SAMPLES = []
STOMACH_MAX_SAMPLES = []
LITTER_SIZE_SAMPLES = []

NPP_SAMPLES = []
TSC_SAMPLES = []
HERBIVORE_SAMPLES = []
CARNIVORE_SAMPLES = []

#log variables
log_var = 0

def biodiversity_index():
    """calculate the biodiversity index"""
    num_organisms = len(entity_object_array)
    register = []
    for e in entity_object_array:
        if e.introgenic_dna not in register:
            register.append(e.introgenic_dna)
    num_species = len(register)
    N = num_organisms * (num_organisms - 1)
    n = 0
    for r in register:
        n+=entity_object_array.count(r) * (entity_object_array.count(r)  - 1)
    return N / n

class log_entry:
    def __init__(this,text = "",label = "",label_text = ""):
        #constructor method
        global log_var
        
        #white text on log
        this.txt = text 
        
        #special (yellow) text for log
        this.label = label 
        
        #contained text inside yellow text
        this.label_text = label_text 
        
        # calculate length and width of font glyphs to center
        txt = ui_font_scale_3.render(this.txt, True, vgui_aux_text_internal) 
        this.label_dimensions = [txt.get_width() + 20,40]
        
    def handle_hover(this):
        """draw and manage this log entry"""

        #handle offscreen logs
        if len(log_index) > 51:
            log_onscreen = log_index[len(log_index) - 51 - log_var : len(log_index) - 1 - log_var]
            
        else:
            #less than 50 logs, log scroller not needed
            log_onscreen = log_index

        #prevent drawing of offscreen objects
        if this not in log_onscreen:
            return

        #render font glyphs
        label_text = ui_font_scale_3.render(this.label_text, True, vgui_aux_text_internal)
        label = ui_font_scale_3.render(this.label, True, (255,255,0)) 
        
        #mouse variables
        c_vec = pygame.mouse.get_pos()
        c_bool = pygame.mouse.get_pressed()[0]
        txt = ui_font_scale_3.render(this.txt, True, vgui_aux_text_internal)
        
        #draw white text
        panel.blit(txt,(1000 - ((txt.get_width() + label.get_width()) / 2),30 + (log_onscreen.index(this) * 15))) 
        
        #draw special (yellow) text
        panel.blit(label,(1000 + ((txt.get_width() - label.get_width()) / 2),30 + (log_onscreen.index(this) * 15)))
        
        if (c_vec[0] > 1000 + ((txt.get_width() - label.get_width()) / 2) and c_vec[0] < 1000+label.get_width()+ ((txt.get_width() - label.get_width()) / 2)):
            #if cursor alligned on x axis
            if (c_vec[1] > 30 + (log_onscreen.index(this) * 15) and c_vec[1] <  40 + (log_onscreen.index(this) * 15)):
                #if cursor alligned on y axis
                
                if (this.label_text == ""):
                    #dont bother drawing empty contained special text
                    return
                
                if ((1000 + (txt.get_width() / 2)) + label_text.get_width()+2) > 1200:
                    #if log starts drawing off screen
                    
                    #calculate offset to add to prevent offscreen drawing
                    recession = ((1000 + (txt.get_width() / 2)) + label_text.get_width()+2) - 1200 + 5
                    
                    #draw new recessed log
                    pygame.draw.rect(panel, vgui_fore, pygame.Rect(1000 + (txt.get_width() / 2) - recession,30 + (log_onscreen.index(this) * 15),label_text.get_width()+2,15))
                    panel.blit(label_text,(1000 + (txt.get_width() / 2) - recession,30 + (log_onscreen.index(this) * 15) + 3))
                    box = group_box((1000 + (txt.get_width() / 2) - recession,30 + (log_onscreen.index(this) * 15)),"",label_text.get_width()+2,15)
                    box.draw()
                    
                else:
                    #if not offscreen
                    
                    #draw log entry
                    pygame.draw.rect(panel, vgui_fore, pygame.Rect(1000 + (txt.get_width() / 2),30 + (log_onscreen.index(this) * 15),label_text.get_width()+2,15))
                    box = group_box((1000 + (txt.get_width() / 2),30 + (log_onscreen.index(this) * 15)),"",label_text.get_width()+2,15)
                    box.draw() #draw an unrecessed box
                    panel.blit(label_text,(1000 + (txt.get_width() / 2),30 + (log_onscreen.index(this) * 15) + 3))
                    
def generate_dna_sequence(length):
    """generate a new dna sequence taking in the length of the strand as an int"""
    
    #initialise the new strand of dna
    strand = []
    
    for i in range(length):
        #does until length satisfied
        
        #adds new base from list (bases)
        strand.append(random.choice(bases))
        
    return strand

def read_dna_protein(strand):
    """REDUNDANT, reads opcode and operand from a dna strand"""

    #check for non genetic material
    if  type(strand) != list:
        return

    #check if len is too short to read a protein
    if len(strand) < 8:
        return
    
    #initialise protein variables
    active_site = read_dna_binary(strand[0:3])
    op_code = read_dna_binary(strand[4:7])
    
    if bases.index(strand[len(strand) - 1]) == 0:
        #define as negative opcode
        sign = True
        
    else:
        #positive opcode
        sign = False
        
    if (sign):
        #make opcode negative
        op_code -= op_code * 2
    
    #return protein
    return [active_site,op_code]
def read_dna_binary(strand):
    """read a numerical value from genetic material"""

    #check for non genetic material
    if  type(strand) != list:
        return
    
    #initialise binary variable
    binary = ""
    
    for i,base in enumerate(strand):
        #for each character in string (strand)
        if bases.index(base) == 1 or bases.index(base) == 2:
            #if complementary base pair A or T
            binary += "0"
            
        else:
            #if bases G or C
            binary += "1"
    
    #return as properly formatted binary
    return int(binary,2)

def create_mutation(strand):
    """manipulate a dna sequence randomly, there are 4 mutation types deletion,insertion,inversion and substitution"""
    
    if (strand == None):
        #prevent index error
        return 

    #check for non genetic material
    if type(strand) != list:
        return
        
    #make copy, for some reason was passing by ref
    mutated = strand[:]
    
    #randomly decide which mutation (weighted)
    mutation_type = random.randint(1,300)
    
    if len(strand) == 1:
        #prevent deletion on dna one base long, too stop it being completely destroyed
        mutation_type = random.randint(1,249)
        
    if mutation_type <= 300 and mutation_type > 250:
        #delete a random base
        del mutated[mutated.index(random.choice(mutated))]
        return (mutated,"DELETION")
    
    if mutation_type <= 100:
        #substitute random base for another base
        mutated[mutated.index(random.choice(mutated))] = random.choice(bases)
        return (mutated,"SUBSTITUTION")
    
    if mutation_type <= 200 and mutation_type > 150: 
        #flip dna strand
        return(mutated[::-1],"INVERSION")
    
    if mutation_type <= 150 and mutation_type > 100:
        #duplicate a random base
        mutated.append(mutated[-1])
        return (mutated,"DUPLICATION")
    
    if mutation_type <= 250 and mutation_type > 200:
        #add a new base to the strand
        mutated.append(random.choice(bases))
        return (mutated,"INSERTION")
    

def distance_to(vec_point_a,vec_point_b):
    """calculate linear distance between two coordinates"""

    #only used in this function, no need for global definition
    Sqr = lambda x: x*x

    #find opp and adj from vec differences
    change_in_x = abs(vec_point_a[0] - vec_point_b[0])
    change_in_y = abs(vec_point_a[1] - vec_point_b[1])
    
    #perform pythagoras to find hyp, the distance between the two points
    return math.sqrt(Sqr(change_in_x) + Sqr(change_in_y))

def rad_to_deg(vec_point_a,vec_point_b):
    """calculate the relative angle between two 2d coordinates"""
    
    #initialise new variables for better readability
    x1, y1 = vec_point_a
    x2, y2 = vec_point_b 
    
    #convert to relative angle
    angle = math.degrees(math.atan2(y2 - y1, x2 - x1)) 
    
    return angle

def pythag(opp,hyp):
    """calculate the size of the adjacent length"""
    
    try:
        #find sine angle
        sine = (opp/hyp)
        
    except:
        #if opp and hyp are perfectly alligned
        return 0
    
    #return arc sine of sine value to find length
    return (math.asin(sine) * 57.296)

def point_of_orbit(host_vec,rotation_float,radius_int):
    """tangent calculation for generating a coordinate relative to another"""
    
    #find cos and sin of rotation 
    c = math.cos(rotation_float * 0.0174)
    s = math.sin(rotation_float * 0.0174)
    
    #return the position with the radius offset alongside from the host vector
    return [(host_vec[0] + radius_int * c),(host_vec[1] + radius_int * s)]

def trace_ray(from_vec,to_vec,array):
    """check for occlusion between two points"""
    
    #initialise setting variables
    lazy_trace_threshold = 0
    ray_skip_mult = 1 # skip a ray step per trace
    ray_visualize = False
    ray_ignore_groups = [False,False]
    ray_hitbox_add = 0 # remove ray precision
    ray_angle = rad_to_deg(from_vec,to_vec) #angle to trace
    
    for ray in range(500 - lazy_trace_threshold):
        #completes per step of ray
        
        #calculate new point of ray
        RayPos = point_of_orbit(from_vec,ray_angle,ray*ray_skip_mult)
        
        if (not ray_ignore_groups[0]):
            #group 0, food objects
            
            for food_obj in array:
                #repeat for each food object
                if (distance_to(RayPos,food_obj.pos) > 3):
                    #didnt collide with non target
                    continue 
                    
                if (food_obj.pos == to_vec):
                    #collided with intended target
                    pygame.draw.line(panel,vgui_ray_beam,from_vec,to_vec)
                    return True
                
                else:
                    #draw line from original trace point to ray position to show where ray was occluded
                    if (ray_visualize):
                        #draw lines too current raypos
                        pygame.draw.line(panel,vgui_ray_beam,from_vec,to_vec)
                        pygame.draw.line(panel,vgui_ray_broken,RayPos,to_vec)
                        
                    return False
                
def get_next_move_to(from_vec,rotation_float,radius = 0.2):
    """calculate the next path step from one coordinate to another by rotation"""
    
    #rotation based method to find next step
    if (not vgui_checkbox_sim_lag_comp.state):
        #without accounting for lag
        return point_of_orbit(from_vec,rotation_float,radius)
    
    #return new position
    return point_of_orbit(from_vec,rotation_float,radius / lag_comp + 1)

def think_next_move(to_vec,from_vec,step):
    """calculate the next path step from one coordinate to another by coordinate"""
    
    if (to_vec == None or from_vec == None):
        #prevent useless return value
        return
    
    #add or subtract position to find position one step forward to target
    step *= 0.5 / lag_comp # account for lag
    from_vec[0] += math.ceil(step * (to_vec[0] - from_vec[0] >= 0) - step * (to_vec[0] - from_vec[0] < 0))
    from_vec[1] += math.ceil(step * (to_vec[1] - from_vec[1] >= 0) - step * (to_vec[1] - from_vec[1] < 0))

    #return new position
    return from_vec

def is_in_triangle(point_a_vec,point_b_vec,point_c_vec,target_vec):
    """check if a coordinate is inside a triangle of coordinates"""
    
    #check if point is inside triangulated area
    if (area_of_triangle(target_vec,point_a_vec,point_b_vec) < 0 and area_of_triangle(target_vec,point_b_vec,point_c_vec) < 0 and area_of_triangle(target_vec,point_c_vec,point_a_vec) < 0):
        #if the point was inside triangulated coordinates
        return True
    
def area_of_triangle(point_a_vec,point_b_vec,point_c_vec):
    """calculate a triangle area"""
    
    #return b*h / 2 to find triangle area
    return ((point_a_vec[0] * (point_b_vec[1] - point_c_vec[1])) + (point_b_vec[0] * (point_c_vec[1] - point_a_vec[1])) + (point_c_vec[0] * (point_a_vec[1] - point_b_vec[1]))) / 2 

def clamp(value,maxi,mini):
    """prevent a value being too small or large"""
    
    #std::clamp replacement
    
    #handle containers
    if type(value) == list or type(value) == tuple:
        #define new container (list)
        new = []
        
        for val in value:
            #for each value in the container
            
            if (val > maxi):
                new.append(maxi)
            elif(val<mini):
                new.append(mini)
            else:
                new.append(val)
                
        return new
    
    #check for bound violations
    if (value > maxi):
        return maxi
    if (value < mini):
        return mini
    
    return value

class vector2:
    
    def __init__(this,x,y):
        #constructor method
        this.x = x
        this.y = y
        
    #needs overloads
    
class vector3:
    
    def __init__(this,x,y,z):
        #constructor method
        this.x = x
        this.y = y
        this.z = z
    #needs overloads
        

class food:
    
    def __init__(this):
        #constructor method
        
        #define attributes
        this.pos = [random.randint(150,650),random.randint(50,550)] #random spot in the simulation area
        this.carbs = random.randint(0 + vgui_slider_nutrients.get_val(),255)    
        this.protein = random.randint(0 + vgui_slider_nutrients.get_val(),255)
        this.being_eaten = False
        
    def draw(this):
        #draw method
        pygame.draw.circle(panel,(this.carbs,this.protein,0),this.pos,2)
        
class egg:
    
    def __init__(this,pos,genes,intron, count_down = 3000):
        #constructor method
        
        #define attributes
        this.pos = pos
        this.genes = genes
        this.intron = intron
        this.count_down = count_down
        this.log = log_entry("egg laid: progress: " + str(this.count_down)," parent",str(this.genes)) # add a dynamic log entry showing the egg progress 
        
        #add to log index
        log_index.append(this.log)
        
    def draw(this):
        #draw method
        pygame.draw.circle(panel,vgui_herbivore_egg,this.pos,3) #draw the egg
        
    def tick(this):
        """refresh this object"""
        #called every sim tick to update hatching
        
        #decrement countdown
        this.count_down -= (1 / lag_comp) * balance
        
        if (this.count_down < 0):
            #countdown ended
            
            #define new infant herbivore
            infant = herbivore()
            infant.egg_progress = -600
            infant.genes = this.genes
            log_index.append(log_entry("herbivore born: ","genome",str(infant.genes)))
            infant.introgenic_dna = this.intron
            infant.pos = this.pos
            
            #on birth mutation (genetic variation)
            if (random.randint(1,100) < vgui_slider_birth_muta_chance.val):
                #define strand variables
                index_to_patch = infant.genes.index(random.choice(infant.genes))
                mutated = create_mutation(infant.genes[index_to_patch])
                old_strand = infant.genes[index_to_patch]
                
                #check if a mutation occured
                try:
                    mutated[1]
                except:
                    mutated = [mutated]
                    mutated.append("SHORT") # temporary measure to stop genetic material being completely deleted
                
                #add to log
                log_index.append(log_entry("a mutation has occured on birth! type: " + mutated[1]," details",str(str(old_strand) + "  ->  " +  str(mutated[0])) + " -> " + str(read_dna_binary(old_strand)) + " -> " + str(read_dna_binary(mutated[0]))))
                
                #update genes
                infant.genes[index_to_patch] = mutated[0]
            
            #update newly added genes
            infant.refold() #refold proteins
            
            #add to entity object array
            entity_object_array.append(infant)
            
            #remove egg from object array
            del egg_object_array[egg_object_array.index(this)]
            
            #try and remove log
            try:
                del log_index[log_index.index(this.log)]
                
            except:
                return
            
            return
        
        try:
            
            #update log entry to show countdown
            this.new_log = log_entry("egg laid: progress: " + str(math.ceil(this.count_down)),"parent",str(this.genes))
            log_index[log_index.index(this.log)] = this.new_log
            this.log = this.new_log
            
        except:
            
            return
        
class herbivore:
    def __init__(this):
        #constructor method
        
        #initialise attributes
        this.genes = [generate_dna_sequence(7),generate_dna_sequence(2),generate_dna_sequence(6),generate_dna_sequence(2),generate_dna_sequence(8),generate_dna_sequence(1)]
        this.pos = [random.randint(150,650),random.randint(50,550)]
        this.rotation = 0 # vision cone rotation
        this.introgenic_dna = generate_dna_sequence(25) # dna that doesnt do anything significant, will make this add visual remarks on species later 
        this.target = None
        this.wait_for = 0
        this.dummy = None
        this.egg_progress = 0
        this.nutrition = 100
        this.dead = False
        this.nose = 0

        #define hormone levels for fight or flight variables
        this.epinephrine = 0
        this.cns_stimulant = 0
        this.cns_depressant = 0
        this.tolerance_factor = 1
        
        #form functional proteins
        this.refold()
        
    def refold(this):
        """read dna again"""
        #reset variables after a dna change
        
        this.stomach = 10
        this.stomach_max = read_dna_binary(this.genes[0]) + 20
        this.bmr = read_dna_binary(this.genes[1]) + 1
        this.sight = read_dna_binary(this.genes[2])
        this.speed = read_dna_binary(this.genes[3])
        this.litter_size = read_dna_binary(this.genes[5]) + 1
        
    def draw(this,override_clamp = False):
        #draw method
        
        #clamps
        if not override_clamp:
            this.speed = clamp(this.speed,100,0)
            this.pos = [this.pos[0],this.pos[1]]
            this.pos[0] = clamp(this.pos[0],650,150)
            this.pos[1] = clamp(this.pos[1],550,50)
        #calculate nose position
        this.nose = point_of_orbit(this.pos,this.rotation,10)
        
        #draw nose and body
        pygame.draw.line(panel,vgui_entity_nose,this.pos,this.nose,3)#nose layer
        pygame.draw.circle(panel,vgui_entity_herbivore,this.pos,5)#body layer
        
        if (this.dead):
            pygame.draw.circle(panel,vgui_entity_dead,this.pos,5)#body layer

    def sight_check(this,target_vec):
        """is the target vec in the vision cone?"""
        #method to check if a target is in the vision cone 
        
        #create triangle points for vision cone
        p_1 = point_of_orbit(this.pos, this.rotation + 270, (this.sight * abs((vgui_slider_smog.get_val() / 100) - 1)))
        p_2 = point_of_orbit(this.pos, this.rotation + 90, (this.sight * abs((vgui_slider_smog.get_val() / 100) - 1)))
        p_3 = point_of_orbit(this.pos, this.rotation, (this.sight * abs((vgui_slider_smog.get_val() / 100) - 1)))
        
        if (is_in_triangle(p_1,p_2,p_3,target_vec)):
            #if in vision cone
            return True
        
        else:
            #if isnt 
            return False
        
    def create_move(this):
        """call every tick to refresh object"""
        #sim called method (external)
        
        try:
            #check if the target was killed by by other means
            food_object_array.index(this.target)
            
        except:
            #remove the target and return
            this.target = None
            return
        
        #update position and rotation
        this.rotation = rad_to_deg(this.pos,this.target.pos) 
        this.pos = think_next_move(this.target.pos,this.pos,this.speed + 2 + (this.epinephrine /100))
        
        #if collides with target (eats)
        if (distance_to(this.pos,this.target.pos) <= (4/lag_comp) + 1):
            
            #add food calories to stomach
            this.stomach+= (this.target.carbs * 0.1 + this.target.protein * 0.1)
            
            #if stomach is full, add to biomass instead
            if (this.stomach > (this.stomach_max * 0.95)):
                this.nutrition+= ((this.target.carbs * 0.1 + this.target.protein * 0.1) * 0.35)
            
            #remove food obj from array
            del food_object_array[food_object_array.index(this.target)]
            
            #force to wait for digestion/eating
            this.wait_for = random.randint(math.ceil(60 / (this.bmr * (1 + (vgui_slider_temperature.get_val() / 100)))),math.ceil(250 / (this.bmr * (1 + (vgui_slider_temperature.get_val() / 100)))))
            
    def wander(this):
        """alternative refresh method"""
        #wander method
        
        if (this.dummy == None):
            #make a new dummy target
            this.dummy = dummy()
            
        #update target
        this.rotation = rad_to_deg(this.pos,this.dummy.pos)
        this.pos = think_next_move(this.dummy.pos,this.pos,(((this.speed - (this.cns_depressant*1.3)) + 2 + (this.epinephrine / 200))))
        
        #if collides with dummy target
        if (distance_to(this.pos,this.dummy.pos) <= (4/lag_comp) + 1):
             #remove dummy
             this.dummy = None
             
             #force to pause
             this.wait_for = random.randint(math.ceil(60 / this.bmr),math.ceil(250 / (this.bmr * (1 + (vgui_slider_temperature.get_val() / 100)))))
            
    def kill(this):
        #kill method
        this.dead = True
        
    def decay(this):
        #decay method 
        
        #visual bleeding
        #pygame.draw.line(panel,(255,0,0),this.pos,point_of_orbit(this.pos,random.randint(0,360),random.randint(1,10)),10)
        
        #if fully decomposed
        if (this.nutrition < 0):
            del entity_object_array[entity_object_array.index(this)]
            return
        
        #remove biomass from decaying corpse
        this.nutrition -= 0.1 / lag_comp
        
        #dont add food 10% of the time
        if (random.randint(1,200) != 20):
            return
        
        #add new food around corpse to return biomass to environment
        decay = food()
        decay.pos = [this.pos[0] + 2 + random.randint(-7,5),this.pos[1] + 2 + random.randint(-7,5)]
        food_object_array.append(decay)
        
    def run(this,obj):
        #run method (fight or flight)

        #create new target for entity to follow
        this.wait_for = 0
        this.target = None
        this.dummy = dummy()
        this.dummy.pos = point_of_orbit(this.pos, obj.rotation + random.randint(-5,5), 50) # face them precisely away from their pursuer 
        
        #update hormones
        this.epinephrine+=0.7 * this.cns_depressant # add adrenaline, dulled by exhaustion
        this.epinephrine = clamp(this.epinephrine,20 * this.cns_depressant,0)
            
        #if off the map
        if (clamp(this.dummy.pos[0],650,150) != this.dummy.pos[0] or clamp(this.dummy.pos[1],550,50) != this.dummy.pos[1]):
            this.dummy = dummy()
            
        #move target
        this.wander()
        return
        
        
class carnivore:
    
    def __init__(this):
        #constructor method
        
        #attribute definitions
        this.pos = [random.randint(150,650),random.randint(50,550)]
        this.rotation = 0
        this.nose = 0
        this.egg_progress = 0
        this.dead = False
        this.wait_for = 0
        
        # genetic code definitions
        this.strand_stomach = generate_dna_sequence(7)
        this.strand_bmr = generate_dna_sequence(3)
        this.strand_sight = generate_dna_sequence(6)
        this.strand_speed = generate_dna_sequence(3)
        this.strand_reprod = generate_dna_sequence(8)
        this.strand_litter_size = generate_dna_sequence(1)
        
        #read functional proteins and their effects
        this.sight = read_dna_binary(this.strand_sight) + 30
        this.target = None
        this.dummy = None
        this.stomach_max = read_dna_binary(this.strand_stomach) + 70
        this.stomach = this.stomach_max / 2
        this.speed = read_dna_binary(this.strand_speed) - 1
        this.bmr = read_dna_binary(this.strand_bmr)+1
        this.litter_size = read_dna_binary(this.strand_litter_size)+1

        
    def draw(this):
        #draw method
        
        #calculate nose pos
        this.nose = point_of_orbit(this.pos,this.rotation,10)
        
        #draw body and nose
        pygame.draw.line(panel,vgui_entity_nose,this.pos,this.nose,3)#nose layer
        pygame.draw.circle(panel,vgui_entity_carnivore,this.pos,5)#body layer
        
    def sight_check(this,target_vec):
        #create points of vision cone
        p_1 = point_of_orbit(this.pos, this.rotation + 270, (this.sight * abs((vgui_slider_smog.get_val() / 100) - 1)))
        p_2 = point_of_orbit(this.pos, this.rotation + 90, (this.sight * abs((vgui_slider_smog.get_val() / 100) - 1)))
        p_3 = point_of_orbit(this.pos, this.rotation, (this.sight * abs((vgui_slider_smog.get_val() / 100) - 1)))
        
        #check if is visible
        if (is_in_triangle(p_1,p_2,p_3,target_vec)):
            #visible
            return True
        
        else:
            #occuluded
            return False
        
    def create_move(this):
        #sim called method 
        
        #check if target still exists
        try:
            #try and find in obj array
            entity_object_array.index(this.target)
            
        except:
            #remove target because doesnt exist
            this.target = None
            return
        
        #if chasing target and target is no longer in sight
        if (not this.sight_check(this.target.pos)):
            #organisms forgets about its prey
            this.target = None
            return
        
        #trigger their fight or flight response
        this.target.run(this)
        
        #update position and rotation
        this.rotation = rad_to_deg(this.pos,this.target.pos)
        this.pos = think_next_move(this.target.pos,this.pos,this.speed + 2)
        
        #if collided with target
        if (distance_to(this.pos,this.target.pos) <= (4/lag_comp) + 1):
            #add log entry
            log_index.append(log_entry("herbivore killed: ","victim genes",str(this.target.introgenic_dna))) 
            
            #kill target and add calories to stomach
            this.target.kill()
            this.stomach+=this.target.nutrition * 0.65
            this.target.nutrition-=this.target.nutrition * 0.65
            this.target = None
            
            #force to pause
            this.wait_for = random.randint(math.ceil(160 / this.bmr),math.ceil(400 / this.bmr))
            
    def wander(this):
        #wander method
        
        #if doesnt have a target to move too
        if (this.dummy == None):
            this.dummy = dummy()
            this.dummy.pos = point_of_orbit(this.pos,random.randint(1,360),random.randint(40,120))
            while (clamp(this.dummy.pos[0],650,150) != this.dummy.pos[0] or clamp(this.dummy.pos[1],550,50) != this.dummy.pos[1]):
                this.dummy.pos = point_of_orbit(this.pos,random.randint(1,360),random.randint(40,120))
                
        #update position and rotation
        this.rotation = rad_to_deg(this.pos,this.dummy.pos) 
        this.pos = think_next_move(this.dummy.pos,this.pos,this.speed + 2)
        
        #if reached dummy
        if (distance_to(this.pos,this.dummy.pos) <= (4/lag_comp) + 1):
             #emove dummy
             this.dummy = None
            
             #force to pause
             this.wait_for = random.randint(math.ceil(60 / this.bmr),math.ceil(250 / this.bmr))
            
    def kill(this):
        #kill method
        this.dead = True
        
    def decay(this):
        #decay method *UNUSED
        x = 2
        
class dummy:
    
    def __init__(this):
        #constructor method
        
        #define attributes
        this.pos = [random.randint(150,650),random.randint(50,550)]
        
        #clamp in sim area
        this.pos[0] = clamp(this.pos[0],650,150)
        this.pos[1] = clamp(this.pos[1],550,50)

    
class button:
    def __init__(this,position_vec,label_str):
        """
        attributes:
            pos : a 2d vector with x and y coordinates
            label : a string containing the button text
        """
        #constructor method
        
        #init attributes
        this.pos = position_vec 
        this.label = str(label_str)
        this.s_bool = False
    def draw(this):
        #draw method
        
        #mouse variables
        c_vec = pygame.mouse.get_pos()
        c_bool = pygame.mouse.get_pressed()[0]
        
        #draw button background
        pygame.draw.rect(panel, vgui_fore, pygame.Rect(this.pos[0],this.pos[1],60,13))
        
        #check for hover
        if (c_vec[0] > this.pos[0] and c_vec[0] < this.pos[0] + 60 and c_vec[1] > this.pos[1] and c_vec[1] < this.pos[1] + 13):
            #check for l=Louse press
            if (c_bool and not this.s_bool):
                #clicked
                this.s_bool = True
                return True
            
            else:
                #hovered
                
                #draw hovered colour over button base rect
                pygame.draw.rect(panel, vgui_state_4, pygame.Rect(this.pos[0],this.pos[1],60,13))
                
                #render new text that is centered
                txt = font_alt.render(this.label, True, vgui_aux_text_internal)
                panel.blit(txt,(this.pos[0] - (txt.get_width() / 2) + 30,this.pos[1]))
                
                return False
            
        #render font glyphs to center
        this.s_bool = c_bool
        txt = font_alt.render(this.label, True, vgui_aux_text_internal)
        panel.blit(txt,(this.pos[0] - (txt.get_width() / 2) + 30,this.pos[1]))
        
class slider:
    
    def __init__(this,position_vec,label_str,min_int,max_int,value_int,invert = False,experimental = False,sign = "",polar = False):
        """
        attributes:
            pos : a 2d vector with x and y coordinates
            label : a string containing the slider text
            min : the minimum slider return value int
            max : the maximum slider return value int
            val : the screen position of the value expressed as an integer length
            invert: boolean value to invert the color indicators
            experimental : boolean value to show the slighter strange experimental slider with individually coloured sections
        """
        #constructor method
        
        #init math attributes
        this.pos = position_vec
        this.label = str(label_str)
        this.min = min_int
        this.max = max_int
        this.val = abs((value_int / (this.max-this.min)) * 100) 
        this.sign = sign
        this.polar = polar
        
        #visual attributes
        this.invert = invert
        this.experimental = experimental
        
    def draw(this):
        #draw method
        
        #define mouse variables
        c_vec = pygame.mouse.get_pos()
        c_bool = pygame.mouse.get_pressed()[0]
        
        #draw slider base and slider value rect
        pygame.draw.rect(panel, vgui_fore, pygame.Rect(this.pos[0],this.pos[1],100,12))
        pygame.draw.rect(panel, vgui_fore, pygame.Rect(this.pos[0] - 1,this.pos[1] - 1,this.val + 2,14)) 
        
        #if in experimental visual mode (individual lines instead of rect)
        if (this.experimental):
            for i in range(math.floor(this.val)):
                #for each line to be drawn
                if (this.invert):
                    #create inverted colour depending on slider val
                    colour = clamp((i*2.55,255 - (i*2.55),0),255,0)
                    
                    #draw line
                    pygame.draw.line(panel,colour,(this.pos[0] + i,this.pos[1]),(this.pos[0] + i,this.pos[1]+12))
                    
                else:
                    #create colour val, green is high and red is low
                    colour = clamp((255 - (i*2.55),i*2.55,0),255,0)
                    
                    #draw line
                    pygame.draw.line(panel,colour,(this.pos[0] + i,this.pos[1]),(this.pos[0] + i,this.pos[1]+12))
                    
        elif (this.invert):
            #create inverted colour depending on slider val
            colour = clamp((this.val*2.55,255 - (this.val*2.55),0),255,0)
            
            #draw solid rect
            pygame.draw.rect(panel,colour,pygame.Rect(this.pos[0],this.pos[1],this.val,12))
            
        else:
            #create colour val 
            colour = clamp((255 - (this.val*2.55),this.val*2.55,0),255,0)
            
            #draw solid rect
            pygame.draw.rect(panel, colour, pygame.Rect(this.pos[0],this.pos[1],this.val,12))
       
        #if hovered and clicked
        if (c_vec[0] > this.pos[0] and c_vec[0] < this.pos[0] + 100 and c_vec[1] > this.pos[1] and c_vec[1] < this.pos[1] + 12):
            if (c_bool):
                #update val
                this.val = c_vec[0] - this.pos[0]
        
        #render font glyphs
        panel.blit(ui_font_scale_3.render(str(math.floor(((this.val / 100) * (this.max - this.min)) + this.min)) + this.sign, True, vgui_aux_text_external),(this.pos[0]+102,this.pos[1]))
        txt = ui_font_scale_3.render(this.label, True, vgui_aux_text_external)
        panel.blit(txt,(this.pos[0] - (txt.get_width() / 2) + 50,this.pos[1] + 13))
        
        #convert to useable int
        return math.floor(((this.val / 100) * (this.max - this.min)) + this.min)
    def get_val(this):
        return math.floor(((this.val / 100) * (this.max - this.min)) + this.min)
    
class check_box: 
    
    def __init__(this,position_vec,label_str,state):
        """
        attributes:
            pos : a 2d vector with x and y coordinates
            label : a string containing the button text
            state : boolean value containing the on/off state of the checkbox
            c_state : boolean value containing a copy of the mouse pressed which is used as a substitute to bitflagging functionality of getasynckeypressed
            hovered : boolean value returning if the box is being hovered, used by other ui functions containing check boxes
        """
        #constructor method
        
        #define attributes
        this.pos = position_vec
        this.label = str(label_str)
        this.state = state
        
        #cursor check attributes
        this.c_state = False
        this.hovered = False
        
    def draw(this):
        #draw method
        
        #define mouse variables
        this.hovered = False
        c_vec = pygame.mouse.get_pos()
        c_bool = pygame.mouse.get_pressed()[0]
        
        #draw base and state of checkbox
        pygame.draw.rect(panel, vgui_fore, pygame.Rect(this.pos[0],this.pos[1],14,14))
        pygame.draw.rect(panel, vgui_color_OFF, pygame.Rect(this.pos[0] + 3,this.pos[1] + 3,8,8))
        
        #if ON
        if (this.state):
            #draw green overlap
            pygame.draw.rect(panel, vgui_color_ON, pygame.Rect(this.pos[0] + 3,this.pos[1] + 3,8,8))
        
        #check if hovered
        if (c_vec[0] > this.pos[0] and c_vec[0] < this.pos[0] + 10 and c_vec[1] > this.pos[1] and c_vec[1] < this.pos[1] + 10):
            #used by other classes
            this.hovered = True
            
            if (c_bool != this.c_state and c_bool):
                #if clicked,update state to opposite
                this.state = not this.state
                
        #update mouse attributes to
        this.c_state = c_bool
        
        #draw label text
        panel.blit(ui_font_scale_3.render(this.label, True, vgui_aux_text_external),(this.pos[0]+15,this.pos[1] + 2))
        
        return this.state
    
def draw_visual_bar(value,minim,maxim,pos,label,color = vgui_state_1):
    #draw background rect and overlay rect for val
    pygame.draw.rect(panel, vgui_fore, pygame.Rect(pos[0],pos[1],100,10))
    pygame.draw.rect(panel, color, pygame.Rect(pos[0],pos[1],((value / (maxim-minim)) * 100),10))
    
    #draw value font glyph
    panel.blit(ui_font_scale_3.render(str(math.floor(((value / 100) * (maxim - minim)) + minim)), True, vgui_aux_text_external),(pos[0]+102,pos[1]))
    
    #render font glyphs of label
    txt = ui_font_scale_3.render(label, True, vgui_aux_text_external)
    panel.blit(txt,(pos[0] - (txt.get_width() / 2) + 50,pos[1] + 11))
    
class color_selector:
    
    def __init__(this,position_vec,current_col_vec,label_str):
        #attributes:
        #pos : a 2d vector with x and y coordinates
        #col : a 3d vector storing the current colour of the referenced variable
        #state : bool open/close state of the interface
        #c_state : boolean value containing a copy of the mouse pressed which is used as a substitute to bitflagging functionality of getasynckeypressed
        #label : contains a string label for telling the user what colour its editing
        #extras :  stores a selection interface object for selection different modes
        
        #define attributes
        this.pos = position_vec
        this.col = clamp(current_col_vec,255,0)
        this.state = False
        this.c_state = False
        this.label = str(label_str)
        this.extras = selection_interface_s((position_vec[0] + 51,position_vec[1]),["default","flip blue","no blue"],0)
        
    def draw(this):
        #draw method
        
        #mouse variables
        c_vec = pygame.mouse.get_pos()
        c_bool = pygame.mouse.get_pressed()[0]
        
        #if color selection interface is triggered
        if (this.state):
            #draw background for color selection interface, pertrudes by 1 pixel
            pygame.draw.rect(panel, vgui_bounding, pygame.Rect(this.pos[0] - 1,this.pos[1] - 1,52,52))#bounding scope
            
            #iterate through each colour to draw its respective pixel
            for red in range(50):
                #x axis
                
                for green in range(50):
                    #y axis
                    
                    #if selected half blue option
                    if (this.extras.selected == 1):
                        blue = (red + green) // 2
                        
                    #if selected no blue option
                    elif (this.extras.selected == 2):
                        blue = 0
                    
                    #if default setting
                    else:
                        blue = (50 - ((red + green) // 2))
                    
                    #draw pixel on colour selection palet
                    pygame.draw.rect(panel, (red * 5,green * 5,blue * 5), pygame.Rect(this.pos[0] + red,this.pos[1] + green,1,1))
            
            #check for mouse press on colour palet
            if (c_vec[0] > this.pos[0] and c_vec[0] < this.pos[0] + 50 and c_vec[1] > this.pos[1] and c_vec[1] < this.pos[1] + 50 and c_bool and c_bool != this.c_state):
                #half blue option
                if (this.extras.selected == 1):
                    #select new colour
                    this.col = ((c_vec[0] - this.pos[0]) * 5,(c_vec[1] - this.pos[1]) * 5, (((c_vec[0] - this.pos[0])+(c_vec[1] - this.pos[1])) // 2) * 5)
                
                #no blue option
                elif (this.extras.selected == 2):
                    #select new colour
                    this.col = ((c_vec[0] - this.pos[0]) * 5,(c_vec[1] - this.pos[1]) * 5,0)
                
                #default option
                else:
                    #select new colour
                    this.col = ((c_vec[0] - this.pos[0]) * 5,(c_vec[1] - this.pos[1]) * 5,(50 - (((c_vec[0] - this.pos[0]) + (c_vec[1] - this.pos[1])) // 2)) * 5)
            
            #if pressed outside of colour selection and not selecting blue option
            elif (c_bool and c_bool != this.c_state and not this.extras.hovered):
                #close colour palet menu
                this.state = not this.state
            
            #draw colour preview and its border
            pygame.draw.rect(panel, vgui_important, pygame.Rect(this.c2s()[0] - 1,this.c2s()[1] - 1,4,4))
            pygame.draw.rect(panel, this.col, pygame.Rect(this.c2s()[0],this.c2s()[1],2,2))
            
            #draw blue option selection interface
            this.extras.draw()
        
        #if not opened
        else:
            #draw colour preview and its border
            pygame.draw.rect(panel, vgui_bounding, pygame.Rect(this.pos[0] - 1,this.pos[1] - 1,32,12))
            pygame.draw.rect(panel, this.col, pygame.Rect(this.pos[0],this.pos[1],30,10))
            
            #if pressed on colour preview
            if (c_vec[0] > this.pos[0] and c_vec[0] < this.pos[0] + 30 and c_vec[1] > this.pos[1] and c_vec[1] < this.pos[1] + 10 and c_bool and c_bool != this.c_state):
                #open colour palet menu
                this.state = not this.state
          
            #draw font glyph for label
            panel.blit(ui_font_scale_3.render(this.label, True, vgui_aux_text_external),(this.pos[0]+31,this.pos[1]))
        
        #save last mouse state to prevent double presses
        this.c_state = c_bool
        
    def c2s(this): 
        """convert colour to screen"""
        #c2s method to convert a colour to screen position
        
        #calculate screen position of red and green colours (x and y)
        reversed_red = (this.col[0] / 5) + this.pos[0]
        reversed_green = (this.col[1] / 5) + this.pos[1]
        
        #return as 2d colour vector, blue is calculated elsewhere
        return (reversed_red,reversed_green)
    
class selection_interface_s:
    
    def __init__(this,position_vec,selections_array,selected_pointer):
        """
        attributes:
            pos : a 2d vector with x and y coordinates
            state : bool open/close state of the interface
            c_state : boolean value containing a copy of the mouse pressed which is used as a substitute to bitflagging functionality of getasynckeypressed
            hovered : bool value is true when a box is being hovered
            selections : contains all selections stored as strings
            selected : contains a pointer to the selected selection
        """
        #constructor method
        
        #selections attributes
        this.pos = position_vec
        this.selections = selections_array
        this.selected = selected_pointer
        
        #mouse state attributes
        this.state = False
        this.c_state = False
        this.hovered = False

        
    def draw(this):
        #draw method
        
        #mouse variables
        c_vec = pygame.mouse.get_pos()
        c_bool = pygame.mouse.get_pressed()[0]
        
        #redefinition to prevent always being True after hovering for first time
        this.hovered = False
        
        txt = ui_font_scale_3.render(this.selections[this.selected], True, vgui_aux_text_internal)
        
        #prevent overflow
        recession = 0
        if txt.get_width() > 50:
            recession = txt.get_width() - 45
        #if hovering main selection
        if (c_vec[0] > this.pos[0] and c_vec[0] < this.pos[0] + 50 + recession and c_vec[1] > this.pos[1] and c_vec[1] < this.pos[1] + 10):
            this.hovered = True
            
            #if mouse is pressed
            if (c_bool and c_bool != this.c_state):
                
                #update state and last state
                this.state = not this.state
                this.c_state = this.state
                
        #draw main selection option 
        pygame.draw.rect(panel, vgui_bounding, pygame.Rect(this.pos[0] - 1,this.pos[1] - 1,52+ recession,12))
        pygame.draw.rect(panel, vgui_fore, pygame.Rect(this.pos[0],this.pos[1],50+ recession,10))

        #render font glyphs for main selection
        panel.blit(txt,(this.pos[0] - (txt.get_width() / 2) + (25 + (recession // 2)),this.pos[1]))
        #if selection interface is opened
        if (this.state):
            
            #for each selectable option
            for selection in range(len(this.selections)):

                txt = ui_font_scale_3.render(this.selections[selection], True, vgui_aux_text_internal)
                
                #prevent overfow
                if txt.get_width() > 50:
                    recession = txt.get_width() - 45
                    
                #draw bounding and selection rect
                pygame.draw.rect(panel, vgui_bounding, pygame.Rect(this.pos[0] - 1,this.pos[1] - 1 + 10 + (selection * 10),52+recession,12))
                pygame.draw.rect(panel, vgui_fore, pygame.Rect(this.pos[0],this.pos[1] + 10 + (selection * 10),50+recession,10))
                
                #render font glyph for referenced selection
                panel.blit(txt,(this.pos[0] - (txt.get_width() / 2) + 25 + (recession // 2),this.pos[1] + 10 + (selection * 10)))
                
                #if the selection is the selected option
                if (selection == this.selected):
                    
                    #draw overlay to show selection on gui
                    pygame.draw.rect(panel, vgui_state_1, pygame.Rect(this.pos[0],this.pos[1] + 10 + (selection * 10),50+recession,10))
                    
                    #render new font glyph to prevent overdrawing 
                    txt = ui_font_scale_3.render(this.selections[selection], True, vgui_fore,)
                    panel.blit(txt,(this.pos[0] - (txt.get_width() / 2) + 25 + (recession // 2),this.pos[1] + 10 + (selection * 10)))
                
                #if current selection is hovered
                if (c_vec[0] > this.pos[0] and c_vec[0] < this.pos[0] + 50+recession and c_vec[1] > this.pos[1] + 10 + (selection * 10) and c_vec[1] < this.pos[1] + 20 + (selection * 10)):
                    this.hovered = True
                    
                    #if mouse pressed
                    if (c_bool and c_bool != this.c_state):
                        
                        #update selected option and close menu
                        this.selected = selection
                        this.state = not this.state
                        
        #update last mouse position
        this.c_state = c_bool
        
class selection_interface_m:
    
    def __init__(this,position_vec,selections_array,selected_array,label_str):
        """
        attributes:
            pos : a 2d vector with x and y coordinates
            state : bool open/close state of the interface
            c_state : boolean value containing a copy of the mouse pressed which is used as a substitute to bitflagging functionality of getasynckeypressed
            hovered : bool value is true when a box is being hovered
            selections : contains all selections stored as strings
            selected : contains an array of pointers to the selected selections
            label : a string containing the header information
        """
        #constructor method
        
        #selection attributes
        this.pos = position_vec
        this.selections = selections_array
        this.selected = selected_array
        
        #mouse attributes
        this.state = False
        this.c_state = False
        
        #main text
        this.label = label_str
        
    def draw(this):
        
        #mouse variables
        c_vec = pygame.mouse.get_pos()
        c_bool = pygame.mouse.get_pressed()[0]
        
        #draw main selection bounding and main rect
        pygame.draw.rect(panel, vgui_bounding, pygame.Rect(this.pos[0] - 1,this.pos[1] - 1,52,12))
        pygame.draw.rect(panel, vgui_fore, pygame.Rect(this.pos[0],this.pos[1],50,10))
        
        #render font glyph for main selection
        txt = ui_font_scale_3.render(this.label, True, vgui_aux_text_internal)
        panel.blit(txt,(this.pos[0] - (txt.get_width() / 2) + 25,this.pos[1]))
        
        #if selection interface is opened
        if (this.state):
            
            #for each selection
            for selection in range(len(this.selections)):
                
                #draw body and bounding
                pygame.draw.rect(panel, vgui_bounding, pygame.Rect(this.pos[0] - 1,this.pos[1] - 1 + 10 + (selection * 10),52,12))
                pygame.draw.rect(panel, vgui_fore, pygame.Rect(this.pos[0],this.pos[1] + 10 +(selection * 10),50,10))
                
                #render font glyph for selection text
                txt = ui_font_scale_3.render(this.selections[selection], True, vgui_aux_text_internal)
                panel.blit(txt,(this.pos[0] - (txt.get_width() / 2) + 25,this.pos[1] + 10 +(selection * 10)))
                
                #if in the selection list
                if (this.selected[selection]):
                    
                    #draw overlay to show selection
                    pygame.draw.rect(panel, vgui_state_4, pygame.Rect(this.pos[0],this.pos[1] + 10 + (selection * 10),50,10))
                    
                    #render new font glyph for text to prevent overdrawing
                    txt = ui_font_scale_3.render(this.selections[selection], True, vgui_aux_text_internal)
                    panel.blit(txt,(this.pos[0] - (txt.get_width() / 2) + 25,this.pos[1] + 10 + (selection * 10)))
                
                #if hovered and pressed on current selection
                if (c_vec[0] > this.pos[0] and c_vec[0] < this.pos[0] + 50 and c_vec[1] > this.pos[1] + 10 + (selection * 10) and c_vec[1] < this.pos[1] + 20 + (selection * 10) and c_bool and c_bool != this.c_state):
                    
                    #update selections state
                    this.selected[selection] = not this.selected[selection]
        
        #if main body selection is pressed
        if ((c_vec[0] > this.pos[0] and c_vec[0] < this.pos[0] + 50 and c_vec[1] > this.pos[1] and c_vec[1] < this.pos[1] + 10 and c_bool and c_bool != this.c_state)):
            
            #open/close interface
            this.state = not this.state
        
        #save last mouse state to prevent double presses, replacement for bitflagging
        this.c_state = c_bool
        
class warning:
    
    def __init__(this,pos,label,label2 = "",label3 = ""):
        #constructor method
        
        #main warning text variables
        this.label = label
        this.label2 = label2
        this.label3 = label3
        
        #position of warning
        this.pos = pos
        
        #exit button
        this.button = button([this.pos[0] + 50 ,this.pos[1] + 40],"ok")
        
    def draw(this):
        #draw method
        
        #draw bounding and main body
        pygame.draw.rect(panel, vgui_bounding, pygame.Rect(this.pos[0] - 1,this.pos[1] - 1,102,52))
        pygame.draw.rect(panel, vgui_warning_1, pygame.Rect(this.pos[0],this.pos[1],100,50))
        
        #render font glyphs for main text
        panel.blit(ui_font_scale_3.render(this.label, True, vgui_aux_text_internal, vgui_warning_1),(this.pos[0],this.pos[1] + 5))
        panel.blit(ui_font_scale_3.render(this.label2, True, vgui_aux_text_internal, vgui_warning_1),(this.pos[0],this.pos[1] + 15))
        panel.blit(ui_font_scale_3.render(this.label3, True, vgui_aux_text_internal, vgui_warning_1),(this.pos[0],this.pos[1] + 25))
        
        #if exit button pressed
        if (this.button.draw()):
            return True
        
        return False
    
class verticle_slider:
    
    def __init__(this,pos,mini,maxi,val,length):
        #constructor method
        
        #define slider attributes
        this.pos = pos
        this.min = mini
        this.max = maxi
        this.val = length - abs((val / (this.max-this.min)) * length)
        this.len = length + 40
        
    def draw(this,maxi):
        this.max = maxi
        #draw method
        
        #draw main slider body and bounding
        pygame.draw.rect(panel, vgui_fore, pygame.Rect(this.pos[0],this.pos[1],13,this.len - 40))
        pygame.draw.rect(panel, vgui_aux_text_internal, pygame.Rect(this.pos[0],this.val-30,13,20))
        
        #mouse variables
        c_vec = pygame.mouse.get_pos()
        c_bool = pygame.mouse.get_pressed()[0]
        
        #if mouse hovered over slider area
        if ((c_vec[0] > this.pos[0] and c_vec[0] < this.pos[0] + 13 and c_vec[1] > this.pos[1] and c_vec[1] < this.pos[1] + (this.len - 48))):
            
            #draw overlay over slider 
            pygame.draw.rect(panel, (144,144,144), pygame.Rect(this.pos[0],this.val - 30,13,20))
            
            #if mouse press
            if c_bool:
                #update slider value
                this.val = c_vec[1] + this.pos[1]
                
        #return converted value to useable int
        return abs(this.max - math.floor(((this.val / this.len) * (this.max - this.min)) + this.min))
    
class group_box:
    
    def __init__(this,pos,label,base,height):
        #constructor method
        
        #position and size attributes
        this.pos = pos
        this.b = base
        this.h = height
        
        #define main text
        this.label = ui_font_scale_3.render(label, True, vgui_aux_text_external,foreground)
        

    def draw(this):
        #draw method
        
        #draw box as joined lines
        pygame.draw.line(panel,vgui_bounding,this.pos,(this.pos[0] + this.b,this.pos[1]))
        pygame.draw.line(panel,vgui_bounding,this.pos,(this.pos[0],this.pos[1] + this.h))
        pygame.draw.line(panel,vgui_bounding,(this.pos[0] + this.b,this.pos[1]),(this.pos[0] + this.b,this.pos[1] + this.h))
        pygame.draw.line(panel,vgui_bounding,(this.pos[0] + this.b,this.pos[1] + this.h),(this.pos[0],this.pos[1] + this.h))
        
        #render main text font glyph
        panel.blit(this.label,(this.pos[0] + (this.b // 5),this.pos[1] - 5))

def trim_list_data(List, max_items, trim_factor):
    if len(List) > max_items:
        for i,data_entry in enumerate(List):
            if i % trim_factor == 0:
                
                #delete every data point per trim factor
                del List[i]
    return List

def plot_graph(List,colour,x_pos,y_pos,width):
    #null check to stop max producing an error
    if not List:
        return
    #grab max val in List
    List_max = max(List)
    
    for i,data_point in enumerate(List):
        
        #draw graph point
        pygame.draw.rect(panel, colour, pygame.Rect(x_pos + i,y_pos - math.ceil((data_point / List_max) * width),1,1))
        
        try:
            #join graph points with line
            pygame.draw.line(panel, colour,(x_pos + i,y_pos - math.ceil((data_point / List_max) * width)),(1350 + i + 1,y_pos - math.ceil((List[i + 1] / List_max) * width)))
        
        except:
            #catch if theres no next data point to join
            continue
        
def handle_metrics():
    """handle sim metrics"""
    
    #grab sample data from global frame
    global NPP_SAMPLES
    global TSC_SAMPLES
    global HERBIVORE_SAMPLES
    global CARNIVORE_SAMPLES
    
    global SIGHT_SAMPLES
    global BMR_SAMPLES
    global SPEED_SAMPLES
    global STOMACH_MAX_SAMPLES
    global LITTER_SIZE_SAMPLES
    
    #screen height is 800px
    
    #draw graph 1 area
    pygame.draw.rect(panel, vgui_fore, pygame.Rect(1350,75,300,300))
    
    #draw graph 2 area
    pygame.draw.rect(panel, vgui_fore, pygame.Rect(1350,425,300,300))
    
    #render info text as font glyph for graph 1
    panel.blit(ui_font_scale_3.render("NPP TREND", True, vgui_aux_text_external),(1250,75))
    panel.blit(ui_font_scale_3.render("TSC TREND", True, vgui_aux_text_external),(1250,95))
    panel.blit(ui_font_scale_3.render("HERBIVORE TREND", True, vgui_aux_text_external),(1250,115))
    panel.blit(ui_font_scale_3.render("CARNIVORE TREND", True, vgui_aux_text_external),(1250,135))
    
    #graph 1 header
    txt = ui_font_scale_3.render("ENVIRONMENT GRAPH", True, vgui_aux_text_external)
    panel.blit(txt,(1500 - (txt.get_width() / 2),55))
    
    #render info text as font glyph for graph 2
    panel.blit(ui_font_scale_3.render("LITTER SIZE TREND", True, vgui_aux_text_external),(1250,430))
    panel.blit(ui_font_scale_3.render("STOMACH TREND", True, vgui_aux_text_external),(1250,450))
    panel.blit(ui_font_scale_3.render("SPEED TREND", True, vgui_aux_text_external),(1250,470))
    panel.blit(ui_font_scale_3.render("BMR TREND", True, vgui_aux_text_external),(1250,490))
    panel.blit(ui_font_scale_3.render("SIGHT TREND", True, vgui_aux_text_external),(1250,510))

    #graph 2 header
    txt = ui_font_scale_3.render("GENE GRAPH - (will take ages to show a trend)", True, vgui_aux_text_external)
    panel.blit(txt,(1500 - (txt.get_width() / 2),405))
    
    #render preview colour rects
    pygame.draw.rect(panel, (0,255,255), pygame.Rect(1230,431,8,8))
    pygame.draw.rect(panel, (255,0,255), pygame.Rect(1230,451,8,8))
    pygame.draw.rect(panel, (0,0,255), pygame.Rect(1230,471,8,8))
    pygame.draw.rect(panel, (0,255,0), pygame.Rect(1230,491,8,8))
    pygame.draw.rect(panel, (255,0,0), pygame.Rect(1230,511,8,8))

    #graph 1 previews
    pygame.draw.rect(panel, (0,0,255), pygame.Rect(1230,76,8,8))
    pygame.draw.rect(panel, (255,0,0), pygame.Rect(1230,96,8,8))
    pygame.draw.rect(panel, (0,255,0), pygame.Rect(1230,116,8,8))
    pygame.draw.rect(panel, (255,255,0), pygame.Rect(1230,136,8,8))
    
    #handle when the graph points start going offscreen
    NPP_SAMPLES = trim_list_data(NPP_SAMPLES, 300, 2)
    TSC_SAMPLES = trim_list_data(TSC_SAMPLES, 300, 2)
    HERBIVORE_SAMPLES = trim_list_data(HERBIVORE_SAMPLES, 300, 2)
    CARNIVORE_SAMPLES = trim_list_data(CARNIVORE_SAMPLES, 300, 2)
    
    SIGHT_SAMPLES = trim_list_data(SIGHT_SAMPLES, 300, 2)
    BMR_SAMPLES = trim_list_data(BMR_SAMPLES, 300, 2)
    SPEED_SAMPLES = trim_list_data(SPEED_SAMPLES, 300, 2)
    STOMACH_MAX_SAMPLES = trim_list_data(STOMACH_MAX_SAMPLES, 300, 2)
    LITTER_SIZE_SAMPLES = trim_list_data(LITTER_SIZE_SAMPLES, 300, 2)
    
    #iterate plot graphs for sample data (graph 1)
    plot_graph(NPP_SAMPLES,(0,0,255),1350,375,300)
    plot_graph(TSC_SAMPLES,(255,0,0),1350,375,300)
    plot_graph(HERBIVORE_SAMPLES,(0,255,0),1350,375,300)
    plot_graph(CARNIVORE_SAMPLES,(255,255,0),1350,375,300)
    
    #graph 2
    plot_graph(SIGHT_SAMPLES,(255,0,0),1350,725,300)
    plot_graph(BMR_SAMPLES,(0,255,0),1350,725,300)
    plot_graph(SPEED_SAMPLES,(0,0,255),1350,725,300)
    plot_graph(STOMACH_MAX_SAMPLES,(255,0,255),1350,725,300)
    plot_graph(LITTER_SIZE_SAMPLES,(0,255,255),1350,725,300)
    




#save current simulation session
def dump_objects(file,data,base_folder):
    with open(base_folder + f"/{file}.pickle","wb") as f:
            #dump objects
            pickle.dump(data,f)
            
            #close handle to file (memory leak protection)
            f.close()
            
def save_current_session(name):
    #create its own folder
    base_folder  = os.getcwd()+"/simulations/"+name
    graph_folder  = os.getcwd()+"/simulations/"+name+"/graphs"
    
    os.mkdir(base_folder)
    os.mkdir(base_folder + "/graphs")
    
    #save herbivore objects
    dump_objects("herbivores",entity_object_array,base_folder)
            
    #save carnivore objects
    dump_objects("carnivores",hunter_object_array,base_folder)
            
    #save food objects
    dump_objects("food",food_object_array,base_folder)

    #save log objects
    dump_objects("log",log_index,base_folder)

    #save graph metrics
    dump_objects("NPP",NPP_SAMPLES,graph_folder)

    dump_objects("TSC",TSC_SAMPLES,graph_folder)

    dump_objects("HERBIVORE",HERBIVORE_SAMPLES,graph_folder)

    dump_objects("CARNIVORE",CARNIVORE_SAMPLES,graph_folder)

    dump_objects("SIGHT",SIGHT_SAMPLES,graph_folder)

    dump_objects("BMR",BMR_SAMPLES,graph_folder)

    dump_objects("SPEED",SPEED_SAMPLES,graph_folder)

    dump_objects("STOMACH_MAX",STOMACH_MAX_SAMPLES,graph_folder)

    dump_objects("LITTER_SIZE",LITTER_SIZE_SAMPLES,graph_folder)
    

def load_objects(file,data,base_folder):
    with open(base_folder + f"/{file}.pickle","rb") as f:
            #load objects
            data = pickle.load(f)
            
            #close handle to file (memory leak protection)
            f.close()
    return data

def load_previous_session(name):
    base_folder  = os.getcwd()+"/simulations/"+name
    graph_folder = os.getcwd()+"/simulations/"+name+"/graphs"
    if (not os.path.exists(base_folder) or not os.path.exists(graph_folder)):
        print(f"error loading file at {base_folder}, are you trying to run an out of date simulation file?")
        return
    global entity_object_array
    global hunter_object_array
    global food_object_array
    global log_index
    
    global NPP_SAMPLES
    global TSC_SAMPLES
    global HERBIVORE_SAMPLES
    global CARNIVORE_SAMPLES
    
    global SIGHT_SAMPLES
    global BMR_SAMPLES
    global SPEED_SAMPLES
    global STOMACH_MAX_SAMPLES
    global LITTER_SIZE_SAMPLES
    
    #load herbivore objects
    entity_object_array=load_objects("herbivores",entity_object_array,base_folder)
            
    #load carnivore objects
    hunter_object_array=load_objects("carnivores",hunter_object_array,base_folder)
            
    #load food objects
    food_object_array=load_objects("food",food_object_array,base_folder)

    #load log objects
    log_index=load_objects("log",log_index,base_folder)

    #load graph metrics
    NPP_SAMPLES=load_objects("NPP",NPP_SAMPLES,graph_folder)

    TSC_SAMPLES=load_objects("TSC",TSC_SAMPLES,graph_folder)
    
    HERBIVORE_SAMPLES=load_objects("HERBIVORE",HERBIVORE_SAMPLES,graph_folder)
    
    CARNIVORE_SAMPLES=load_objects("CARNIVORE",CARNIVORE_SAMPLES,graph_folder)
    
    SIGHT_SAMPLES=load_objects("SIGHT",SIGHT_SAMPLES,graph_folder)

    BMR_SAMPLES=load_objects("BMR",BMR_SAMPLES,graph_folder)

    SPEED_SAMPLES=load_objects("SPEED",SPEED_SAMPLES,graph_folder)

    STOMACH_MAX_SAMPLES=load_objects("STOMACH_MAX",STOMACH_MAX_SAMPLES,graph_folder)

    LITTER_SIZE_SAMPLES=load_objects("LITTER_SIZE",LITTER_SIZE_SAMPLES,graph_folder)
        
    print(f"succesfully loaded {len(entity_object_array)} herbivores {len(hunter_object_array)} carnivores {len(food_object_array)} food and {len(log_index)} logs")
            
#define ui buttons
vgui_test_button = color_selector(
   (500,500),
   (480,50,20),
   178
   )
vgui_button_back = button(
    (1,589),
    "<- back")
vgui_button_exit = button(
    (749,1),
    " quit ")
vgui_button_start = button(
    (375,300),
    "start")
vgui_button_options = button(
    (375,315),
    "options")
vgui_button_theme = button(
    (375,330),
    "theme")
vgui_button_entity_list_manager = button(
    (375,345),
    "edit ents")
vgui_load_sim = button(
    (100,200),
    "load")

#define ui sliders
vgui_slider_food = slider(
    (100,75),
    "food amount",
    0,
    5000,
    Config["layer-1"]["food"])

xspeed = slider(
    (20,75),
    "change logo speed x ",
    0,
    10,
    x_speed,
    True,
    True)

yspeed = slider(
    (20,100),
    "change logo speed y ",
    0,10,
    y_speed,
    True,
    True)

vgui_slider_herb = slider(
    (100,100),
    "herbivore amount",
    0,
    100,
    Config["layer-1"]["herbivores"])

vgui_slider_carn = slider(
    (100,125),
    "carnivore amount",
    0,
    20,
    Config["layer-1"]["carnivores"],
    True)

vgui_slider_ray_lazy = slider(
    (500,75),
    "lazy tracing",
    0,
    400,
    20)

vgui_slider_ray_mult = slider(
    (500,100),
    "speed multiplier",
    1,
    10,
    1)

vgui_slider_ray_add = slider(
    (500,125),
    "drunk ray",
    1,
    10,
    5)

vgui_slider_sim_slow_val = slider(
    (36,100),
    "slow amount",
    1,
    100,
    5,
    True)
#selection pressures
vgui_slider_photosynth = slider(
    (660,50),
    "GPP",
    1,
    1000,
    100)

vgui_slider_nutrients = slider(
    (660,75),
    "soil nutrients",
    0,
    100,
    0)

vgui_slider_temperature = slider(
    (660,100),
    "temperature",
    -100,
    100,
    100,
    True,
    sign = "°")

vgui_slider_birth_muta_chance = slider(
    (660,150),
    "mutation chance birth",
    0,
    100,
    50,
    True,
    sign = "%")

vgui_slider_random_muta_chance = slider(
    (660,175),
    "mutation chance random",
    0,
    100,
    10,
    True,
    sign = "%")

vgui_slider_smog = slider(
    (660,225),
    "smog",
    1,
    100,
    10,
    True,
    sign = "%")

vgui_slider_pollution = slider(
    (660,250),
    "pollution",
    1,
    100,
    10,
    True,
    sign = "%")

#define checkbox ui elements
vgui_checkbox_sim_slow_bool = check_box(
    (1,100),
    "slow",
    False)

vgui_checkbox_sim_lag_comp = check_box(
    (1,150),
    "lag comp",
    True)

vgui_checkbox_ray_visualise = check_box(
    (500,160),
    "visualise",
    False)

vgui_checkbox_visualise_math = check_box(
    (100,180),
    "visualise math",
    False)

vgui_checkbox_ray_master = check_box(
    (100,195),
    "ray tracing",
    False)

#define colour selection interface ui elements
vgui_color_ray_visualise_1 = color_selector(
    (570,160),
    vgui_ray_beam,
    "beam")

vgui_color_ray_visualise_2 = color_selector(
    (570,212),
    vgui_ray_broken,
    "broken")

vgui_color_state_0 = color_selector(
    (50,50),
    vgui_state_0,
    "vgui_state_0")

vgui_color_state_1 = color_selector(
    (50,105),
    vgui_state_1,
    "vgui_state_1")

vgui_color_state_2 = color_selector(
    (50,160),
    vgui_state_2,
    "vgui_state_2")

vgui_color_state_3 = color_selector(
    (50,215),
    vgui_state_3,
    "vgui_state_3")

vgui_color_state_4 = color_selector(
    (50,270),
    vgui_state_4,
    "vgui_state_4")

vgui_color_state_5 = color_selector(
    (50,325),
    vgui_state_5,
    "vgui_state_5")

vgui_color_bounding = color_selector(
    (50,380),
    vgui_bounding,
    "vgui_bounding")

foreground_color = color_selector(
    (50,435),
    foreground,
    "foreground")

vgui_fore_color = color_selector(
    (50,490),
    vgui_fore,
    "vgui_fore")

vgui_herbivore_color = color_selector(
    (200,50),
    vgui_entity_herbivore,
    "vgui_entity_herbivore")

vgui_carnivore_color = color_selector(
    (200,105),
    vgui_entity_carnivore,
    "vgui_entity_carnivore")

vgui_nose_color = color_selector(
    (200,160),
    vgui_entity_nose,
    "vgui_entity_nose")

vgui_text_internal_color = color_selector(
    (200,215),
    vgui_aux_text_internal,
    "vgui_aux_text_internal")

vgui_text_external_color = color_selector(
    (200,270),
    vgui_aux_text_external,
    "vgui_aux_text_external")

vgui_egg_color = color_selector(
    (200,325),
    vgui_herbivore_egg,
    "vgui_herbivore_egg")

vgui_color_dead = color_selector(
    (200,380),
    vgui_entity_dead,
    "vgui_entity_dead")

vgui_color_ON_state = color_selector(
    (200,435),
    vgui_color_ON,
    "vgui_color_ON")

vgui_color_OFF_state = color_selector(
    (200,490),
    vgui_color_OFF,
    "vgui_color_OFF")

#define single selection interfaces
vgui_slc_ray_ignore = selection_interface_m(
    (500,212),
    ["food","creatures"],
    [False,False],
    "ignore")

vgui_color_blindness = selection_interface_s(
    (350,50),
    ["normal","deutera","protano","tritano"],
    0)

vgui_saved_simulations = selection_interface_s(
    (200,200),
    saved_simulations,
    0)

#define warnings ui elements
vgui_warning_conf = warning(
    [300,250],
    "first time setup",
    "because didnt find",
    "config")

#verticle sliders
vgui_slider_scroll = verticle_slider(
    [1200,25],
    0,
    len(log_index) - 51,
    0,
    750)
#define group boxes ui elements
environment = group_box(
    [60,60],
    "environment",
    180,
    200)

raytracing = group_box(
    [460,60],
    "ray tracing",
    180,
    200)

log_box = group_box(
    [799,25],
    "",
    400,
    550)

program_bounding = group_box(
    [0,0],
    "",
    1699,
    799)

#define preview organisms
ui_herbivore = herbivore()
ui_carnivore = carnivore()
ui_food = food()

#update positions from randomly generated ones
ui_egg = egg((100,670),None,None)
ui_herbivore.pos = (100,690)
ui_carnivore.pos = (100,710)
ui_food.pos = (100,730)


#define mutation reasons
mut_reasons = ["radiation","protein misfold","mitosis error"]

for i in range(Config["layer-1"]["food"]):
    #add starting food
    food_object_array.append(food())
    
for i in range(Config["layer-1"]["herbivores"]):
    #add starting herbivores
    entity_object_array.append(herbivore())
    
for i in range(Config["layer-1"]["carnivores"]):
    #add starting carnivores 
    hunter_object_array.append(carnivore())
    
def sim_thread():
    """start the simulation main thread"""
    
    #grab metrics from global frame
    global balance
    global NPP_SAMPLES
    global NPP
    global TSC
    global SIGHT_SAMPLES
    global BMR_SAMPLES
    global SPEED_SAMPLES
    global STOMACH_MAX_SAMPLES
    global LITTER_SIZE_SAMPLES
    
    #set volatile metrics back
    NPP = 0
    TSC = 0
    
    #for each food object in list
    for food_obj in food_object_array:
        #draw food
        food_obj.draw()
        
        #add calories to NPP
        NPP += food_obj.carbs + food_obj.protein
    
    #for each egg in list
    for egg_obj in egg_object_array:
        #draw egg
        egg_obj.draw()
        
        #countdown or hatch egg
        egg_obj.tick()
    
    #for herbivore in list
    for herbivore in entity_object_array:
        #draw herbivore
        herbivore.draw()
        
        #if dead
        if (herbivore.dead):
            #decay herbivore, returning biomass to food objects
            herbivore.decay()
            
            #exclude from computation
            continue
        
        #if random mutation should occur
        if ((tick % 2000 * lag_comp) == 0) and random.randint(0,100) < vgui_slider_random_muta_chance.val:
            
            #find pointer to genes to mutate
            index_to_patch = herbivore.genes.index(random.choice(herbivore.genes))
            
            #define mutated gene
            mutated = create_mutation(herbivore.genes[index_to_patch])
            
            try:
                #try and reference second base in sequence
                mutated[1]
                
            except:
                #would return single base not as list
                
                #redefine as list
                mutated = [mutated]
                
                #change mutation type
                mutated.append("UNEDITABLE")
            
            
            #save previous strand for logging
            old_strand = herbivore.genes[index_to_patch]
            
            #add log entry showing mutation info
            log_index.append(log_entry("a mutation has occured due to " + random.choice(mut_reasons) + " type: " + mutated[1]," details",str(str(old_strand) + "  ->  " +  str(mutated[0])) + " -> " + str(read_dna_binary(old_strand)) + " -> " + str(read_dna_binary(mutated[0]))))
            
            
            #patch genes 
            herbivore.genes[index_to_patch] = mutated[0]
            
            #update functional proteins
            herbivore.refold()
        
        #add total stomach contents from herbivore to TSC
        TSC += herbivore.stomach
        
        #if waiting
        if (herbivore.wait_for > 0):
            #remove some wait time
            herbivore.wait_for -= 1 / lag_comp
            
            #exclude from computation
            continue
        
        #if starved
        if (herbivore.stomach <= 0):
            
            #kill herbivore
            herbivore.dead = True
            
            #add to log info
            log_index.append(log_entry("herbivore starved"," genes",str(herbivore.introgenic_dna)))
            
            #exclude from computation
            continue
        
        
        
        #handle hormone levels
        if herbivore.epinephrine > 0:
            #depreciate epi levels
            herbivore.epinephrine -= (0.1 / lag_comp) * abs(((vgui_slider_pollution.get_val()) / 100) - 1)
            
            #add exhaustion
            herbivore.cns_depressant += (0.01)  * abs(((vgui_slider_pollution.get_val()) / 100) - 1) # pollution causes disruption to endocrine system
        
        #remove exhaustion if no epi
        elif (herbivore.cns_depressant > 0):
            herbivore.cns_depressant -= (0.03)  * abs(((vgui_slider_pollution.get_val()) / 100) - 1)
        
        #if should lay egg
        if (herbivore.egg_progress > (900 / balance)):
            
            #for each egg per litter
            for i in range(herbivore.litter_size):
                
                #add new egg to list
                egg_object_array.append(egg([herbivore.pos[0] + random.randint(1,3),herbivore.pos[1] + random.randint(1,3)],herbivore.genes,herbivore.introgenic_dna))
                
                #remove stomach contents
                herbivore.stomach -= herbivore.stomach_max * 0.2
                
                #refractory period
                herbivore.egg_progress = -200 / balance
        
        #if shouldnt lay egg
        elif herbivore.stomach > (herbivore.stomach_max * 0.9):
            #add egg progress
            herbivore.egg_progress += ((1 / lag_comp) * balance) * abs(((vgui_slider_pollution.get_val()) / 100) - 1) #pollution reduces reproduction.
        
        #if has a target
        if (herbivore.target != None):
            
            #call method to compute movement
            herbivore.create_move()
            
        #if doesnt, should find new target
        else:
            
            #calculate which radian the organism is looking at
            if (herbivore.nose[0] > herbivore.pos[0]):
                #if nose x larger than herbivore x
                radian = 0
                
            else:
                #if nose x smaller than herbivore x
                radian = 1
            
            #for possible target food in list
            for food in food_object_array:
                
                #exclude food behind organism
                if (radian == 0 and food.pos[0] < herbivore.pos[0]):
                    continue
                    
                if (radian == 1 and food.pos[0] > herbivore.pos[0]):
                    continue
                
                #exclude food outside of rectangular rough vision cone
                if abs(food.pos[0] - herbivore.pos[0]) > herbivore.sight:
                    continue
                    
                if abs(food.pos[1] - herbivore.pos[1]) > (herbivore.sight // 2):
                    continue
                
                #if cant see food
                if (not herbivore.sight_check(food.pos)):
                    #isnt potential target
                    continue
                
                #update target
                herbivore.target = food
                
                #found target, no need for anymore computation
                break
            
            #wanders if cant find any food
            herbivore.wander()
        
        #update stomach contents due to respiration and metabolic activity
        herbivore.stomach -= ((herbivore.bmr * (1 + (vgui_slider_temperature.get_val() / 100))) / (100 * lag_comp))
        
        #clamp hormone and stomach values
        herbivore.stomach = clamp(herbivore.stomach,herbivore.stomach_max,0)
        herbivore.cns_depressant = clamp(herbivore.cns_depressant,1,0)
    
    #for each predator in list
    for carnivore in hunter_object_array:
        #draw predator
        carnivore.draw()
        
        #if is dead, should decay to release biomass
        if (carnivore.dead):
            carnivore.decay()
            continue
        
        #if waiting, should tick down waiting period
        if (carnivore.wait_for > 0):
            carnivore.wait_for -= 1 / lag_comp
            continue
        
        #if has a target, should move to that target
        if (carnivore.target != None):
            carnivore.create_move()
        
        #if doesnt, will find new one
        else:
            
            #calculate radian that the organism can see
            if (carnivore.nose[0] > carnivore.pos[0]):
                radian = 0
                
            else:
                radian = 1
            
            #for possible target to select
            for prey in entity_object_array:
                #shouldnt select dead targets, excludes
                if (prey.dead):
                    continue
                
                #shouldnt select targets not in visible radian, excludes
                if (radian == 0 and prey.pos[0] < carnivore.pos[0]):
                    continue
                    
                if (radian == 1 and prey.pos[0] > carnivore.pos[0]):
                    continue
                
                #shouldnt select targets in rough vision cone rect, excludes
                if abs(prey.pos[0] - carnivore.pos[0]) > carnivore.sight:
                    continue
                    
                if abs(prey.pos[1] - carnivore.pos[1]) > (carnivore.sight // 2):
                    continue
                
                #shouldnt select target it cant see, excludes
                if (not carnivore.sight_check(prey.pos)):
                    continue
                
                #update target
                carnivore.target = prey
                
                break
            
            #wanders if cant find prey
            carnivore.wander()
        
        #decrement stomach due to metabolic activity and respiration
        carnivore.stomach -= (carnivore.bmr / (100 * lag_comp))
        
        #clamp stomach value
        carnivore.stomach = clamp(carnivore.stomach,carnivore.stomach_max,0)
    
    #every 15th tick
    if tick % 15 == 0:
        
        #add sample data to lists
        NPP_SAMPLES.append(NPP)
        TSC_SAMPLES.append(TSC)
        HERBIVORE_SAMPLES.append(len(entity_object_array))
        CARNIVORE_SAMPLES.append(len(hunter_object_array))
        
        #calculate gene averages
        sight_total = 0
        bmr_total = 0
        speed_total = 0
        litter_size_total = 0
        stomach_max_total = 0
        
        for gene_holder in entity_object_array:
            sight_total+=gene_holder.sight
            bmr_total+=gene_holder.bmr
            speed_total+=gene_holder.speed
            litter_size_total+=gene_holder.litter_size
            stomach_max_total+=gene_holder.stomach_max
            
        #find average sight
        SIGHT_SAMPLES.append(sight_total / len(entity_object_array))
        BMR_SAMPLES.append(bmr_total / len(entity_object_array))
        SPEED_SAMPLES.append(speed_total / len(entity_object_array))
        LITTER_SIZE_SAMPLES.append(litter_size_total / len(entity_object_array))
        STOMACH_MAX_SAMPLES.append(stomach_max_total / len(entity_object_array))
    
def vgui_thread():
    """compute external ui elements"""
    
    #grab metrics from global frame 
    global NPP
    global balance
    
    #slow down program if slow button selected
    if (vgui_checkbox_sim_slow_bool.draw()):
        time.sleep(0.1 * (vgui_slider_sim_slow_val.draw() / 100))
        
    #draw selection pressure sliders
    vgui_checkbox_sim_lag_comp.draw()
    vgui_slider_birth_muta_chance.draw()
    vgui_slider_random_muta_chance.draw()
    vgui_slider_temperature.draw()
    vgui_slider_nutrients.draw()
    vgui_slider_smog.draw()
    vgui_slider_pollution.draw()
    
    #show balance metric
    draw_visual_bar(balance * 100,1,500,(660,600),"balance",(255,255,0))
    
    #render organism images for preview
    ui_herbivore.draw(True)
    ui_carnivore.draw()
    ui_egg.draw()
    ui_food.draw()
    
    #render organism preview text as font glyph
    txt = ui_font_scale_3.render("-EGG ", True, vgui_aux_text_internal)
    panel.blit(txt,(120,670))
    
    txt = ui_font_scale_3.render("-HERBIVORE", True, vgui_aux_text_internal)
    panel.blit(txt,(120,690))

    txt = ui_font_scale_3.render("-CARNIVORE ", True, vgui_aux_text_internal)
    panel.blit(txt,(120,710))

    txt = ui_font_scale_3.render("-FOOD", True, vgui_aux_text_internal)
    panel.blit(txt,(120,730))
    
def simulation():
    """links computation of simulation and ui elements"""
    #grab current tab and sim ticks from global frame
    global tab
    global tick
    
    #update GPP rate from slider
    _GPP = vgui_slider_photosynth.draw()
    
    #computes if food should be added based off photosynthesis rate
    if (random.randint(1,math.ceil(1000 * lag_comp)) <  _GPP):
        
        #allow GPP values above 1000 to have an effect
        if (_GPP > 1000):
            #add multiple food objects depending on size of overflow
            for i in range(_GPP // 1000):
                  food_object_array.append(food())
                    
        food_object_array.append(food())
        
    #draw sim area background
    pygame.draw.rect(panel, (90,90,90), pygame.Rect(150,50,500,500))
    
    #if button to return to home screen is pressed
    if (vgui_button_back.draw()):
        tab = 0
        
    #call threads
    vgui_thread()
    sim_thread()
    
    #updated ticks alive for sim
    tick+=1
    
def options():
    
    #grab option variables to be updated from global frame
    global tab
    global vgui_ray_beam
    global vgui_ray_broken
    
    #if back button to return to home screen is pressed
    if (vgui_button_back.draw()):
        tab = 0
        
    #draw ui elements
    environment.draw()
    raytracing.draw()
    Config["layer-1"]["food"] = vgui_slider_food.draw()
    Config["layer-1"]["herbivores"] = vgui_slider_herb.draw()
    Config["layer-1"]["carnivores"] = vgui_slider_carn.draw()
    vgui_checkbox_ray_master.draw()
    vgui_slider_ray_lazy.draw()
    vgui_slider_ray_mult.draw()
    vgui_slider_ray_add.draw()
    vgui_checkbox_ray_visualise.draw()
    vgui_color_ray_visualise_1.draw()
    vgui_color_ray_visualise_2.draw()
    vgui_slc_ray_ignore.draw()
    
    #update selected colour variables
    vgui_ray_beam = vgui_color_ray_visualise_1.col 
    vgui_ray_broken = vgui_color_ray_visualise_2.col
    
def theme():
    #grab colour variables from global frame
    global tab
    global vgui_state_0
    global vgui_state_1
    global vgui_state_2
    global vgui_state_3
    global vgui_state_4
    global vgui_state_5
    global vgui_fore
    global foreground
    global vgui_bounding
    global vgui_entity_herbivore
    global vgui_entity_carnivore
    global vgui_aux_text_internal
    global vgui_aux_text_external
    global vgui_entity_nose
    global vgui_herbivore_egg
    global vgui_entity_dead
    
    #return to main screen
    if (vgui_button_back.draw()):
        tab = 0
        
    #draw colour interfaces
    vgui_color_state_0.draw()
    vgui_color_state_1.draw()
    vgui_color_state_2.draw()
    vgui_color_state_3.draw()
    vgui_color_state_4.draw()
    vgui_color_state_5.draw()
    vgui_color_dead.draw()
    vgui_color_bounding.draw()
    foreground_color.draw()
    vgui_fore_color.draw()
    vgui_herbivore_color.draw()
    vgui_carnivore_color.draw()
    vgui_nose_color.draw()
    vgui_text_internal_color.draw()
    vgui_text_external_color.draw()
    vgui_egg_color.draw()
    vgui_color_ON_state.draw()
    vgui_color_OFF_state.draw()
    vgui_color_blindness.draw()
    
    #update colour variables
    vgui_state_0 = vgui_color_state_0.col
    vgui_state_1 = vgui_color_state_1.col
    vgui_state_2 = vgui_color_state_2.col
    vgui_state_3 = vgui_color_state_3.col
    vgui_state_4 = vgui_color_state_4.col
    vgui_state_5 = vgui_color_state_5.col
    vgui_herbivore_egg = vgui_egg_color.col
    vgui_bounding = vgui_color_bounding.col
    foreground = foreground_color.col
    vgui_fore = vgui_fore_color.col
    vgui_entity_herbivore = vgui_herbivore_color.col
    vgui_entity_carnivore = vgui_carnivore_color.col
    vgui_entity_nose = vgui_nose_color.col
    vgui_aux_text_internal = vgui_text_internal_color.col
    vgui_aux_text_external = vgui_text_external_color.col
    vgui_entity_dead = vgui_color_dead.col
    
def main_menu():
    #grab current tab from global frame
    global tab
    
    #grab logo variables from global frame
    global x
    global y
    global img_size
    global x_speed
    global y_speed
    
    #draw buttons to different ui areas
    if vgui_button_theme.draw():
        tab = 3
        
    if vgui_button_start.draw():
        tab = 2
        
    if vgui_button_options.draw():
        tab = 1
    vgui_saved_simulations.draw()
    if (vgui_load_sim.draw()):
        load_previous_session(saved_simulations[vgui_saved_simulations.selected])
    #handle x axis collision with border
    if (x + img_size[0] >= 1700) or (x <= 0):
        x_speed = -x_speed
        
    #handle y axis collision with border
    if (y + img_size[1] >= 800) or (y <= 0):
        y_speed = -y_speed
    
    #move the logo
    x += x_speed / lag_comp
    y += y_speed / lag_comp
    
    #update xspeed as per slider
    if x_speed <  0:
        x_speed = -xspeed.draw()
        
    else:
        x_speed = xspeed.draw()
    
    #update yspeed as per slider
    if y_speed < 0:
        y_speed = -yspeed.draw()
        
    else:
        y_speed = yspeed.draw()
        
    #draw logo
    panel.blit(dvd,(x,y))
    
def log_manager():
    #grab log offset from global frame
    global log_var
    
    #draw log bounding 
    pygame.draw.rect(panel,vgui_fore,pygame.Rect(810,25,380,750))
    
    #draw log text info as font glyph
    txt = font_alt.render("simulation log (hover over yellow text for extra information)", True, (255,255,255))
    panel.blit(txt,(1000 - (txt.get_width() / 2),10))
    
    #draw log scroller if needed
    if (len(log_index) > 51):
        log_var = abs(vgui_slider_scroll.draw(len(log_index) - 51))
        
        
    #reverse log entry list to prevent overdraw
    for pointer in range(len(log_index)):
        log_index[len(log_index) - pointer - 1].handle_hover()
        
def main():
    
    #grab lag comp and t2p from global frame
    global lag_comp
    global t2p
    
    #clamp lag comp
    lag_comp = clamp(lag_comp,3,0.01)
    
    #start time
    sample_time = time.time()
    
    #for pygame events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            
            #dump config file on external exit command
            json.dump(Config,open(os.getcwd() + "/config.json","w"))
            
            #exit thread and program
            pygame.quit()
            sys. exit()
    
    #draw backdrop
    panel.fill(foreground)
    
    #define threads
    thread_metrics = threading.Thread(
        target=handle_metrics,
        args=()
        ) 
    
    thread_log = threading.Thread(
        target=log_manager,
        args=()
        )
    
    #start threads
    thread_log.start()
    thread_metrics.start()
    
    #wait for threads to complete before continuing
    thread_log.join()
    thread_metrics.join()
    
    
    #ui section function calls
    if (tab == 0):
        main_menu()
        
    elif (tab == 1):
        options()
        
    elif (tab == 2):
        simulation()
        
    elif (tab == 3):
        theme()
        
    #internal exit command
    if (vgui_button_exit.draw()):
        now = datetime.now()
        dt_string = now.strftime("%d,%m,%Y (%H-%M-%S)")
        save_current_session("SESSION " + dt_string)
        json.dump(Config,open(os.getcwd() + "/config.json","w"))
        pygame.quit()
        sys. exit()
    
    #if processing time not instant
    if ((time.time() - sample_time) != 0):
        
        #calculate lag comp
        lag_comp = ((math.ceil(1 / (time.time() - sample_time))) / 100)
        
        #calculate processing time
        #t2p = (time.time() - sample_time)
        
        #render font glyph to show processing time
        #txt = ui_font_scale_3.render(f"processing time {t2p} ", True, vgui_aux_text_internal)
        #panel.blit(txt,(400 - ((txt.get_width() + txt.get_width()) / 2),600))
    
    #draw main program border
    program_bounding.draw()

    #refresh canvas
    pygame.display.flip()

    
#add an info log entry
log_index.append(log_entry("a project made by henry frodsham"," read ","please familiarise yourself with the ui elements in options before starting the simulation"))

while True:
    #main loop
    
    #iterate through entity list
    summ = 0
    for i in entity_object_array:
        
        #exclude dead organisms
        if i.dead:
            continue
        
        #add counter for living organism
        summ += 1
        
    try:
        
        #try calculate simulation balance metric based off herbivores and eggs as a proportion of carnivores
        balance = (len(hunter_object_array) / (((summ + (len(egg_object_array) // 2))) * 4) + 1)
        
    except:
        
        #debug info
        print(f"exception caught, {summ}, {egg_object_array} , {hunter_object_array}")
        
        #reinject new organisms if natural balance is not maintained
        for i in range(15):
             entity_object_array.append(herbivore())
    
    
    #redefine main ui elements based off screen size 
    screen_size = panel.get_size()
    vgui_button_back = button((1,screen_size[1]-14),"<- back")
    master = group_box((0,0),"",screen_size[0] - 401,screen_size[1] - 1)
    log = group_box((0,0),"",1299,599)
    #call main function
    main()
