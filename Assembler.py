"""
Author : Ahmed Mohamed Sobhey Heakl
ID     : 120190044
Section: 1
"""


memory_ref = {
    "AND": "0",
    "ADD": "1",
    "LDA": "2",
    "STA": "3",
    "BUN": "4",
    "BSA": "5",
    "ISZ": "6"    
}

reg_ref = {
    "CLA":"7800",
    "CLE":"7400",
    "CMA":"7200",
    "CME":"7100",
    "CIR":"7080",
    "CIL":"7040",
    "INC":"7020",
    "SPA":"7010",
    "SNA":"7008",
    "SZA":"7004",
    "SZE":"7002",
    "HLT":"7001"
}

inp_ref = {
    "INP":'F800',
    "OUT":"F400",
    "SKI":"F200",
    "SKO":"F100",
    "ION":"F080",
    "IOF":"F040"
}


import re
# Load in the assembly file
assembly = open('assemblyCode.asm', 'r')

# Read the lines
lines = assembly.readlines()
lst_of_instructs = [re.sub(' +', ' ', line.replace("\t", " ")).split() for line in lines]
for idx, line in enumerate(lst_of_instructs):
    for idx2, sent in enumerate(line):
        # Omit comments
        if sent[0] == "/":
            lst_of_instructs[idx] = line[:idx2]

# Initialize the location counter
location_counter = original_location_counter = 0

# Dictionary to store the (name, location) pair
pass1 = {}

# Dictionary to store the (location, instruction)
pass2 = {}


# Calculate the hex value of a negative number
def calc_neg_hex(val, bits=16):
    return hex(2**bits + val)

def second_pass():
    """
    The second pass of the program which alters the content 
    of the pass2 dict and store the instructions values in hex
    """
    
    # Loop through each line again
    for line in lst_of_instructs:
        if(line[0] == "ORG"):
            olc = int(line[1])
            continue
        
        # Check if the program ends
        if(line[0] == "END"):
            print("Program assembled!")
            
            # Write instructions and locations in the output file
            with open("output.asm", 'w') as f:
                for loc, instruct in pass2.items():
                    f.write(str(loc) + "\t" + str(instruct) + "\n")
            break
    
        if len(line) == 1:
            # Register Reference Instructions
            if(reg_ref.get(line[0], -1) != -1):
                pass2[olc] = reg_ref[line[0]]
                
            # Input Reference Instructions
            else:
                pass2[olc] = inp_ref[line[0]]
            olc+=1 
            continue
        
        # Memory Reference Instruction
        if memory_ref.get(line[0], -1) != -1:
            
            # Indirect Reference
            if len(line) > 2:
                pass2[olc] = hex(int(memory_ref[line[0]]) + 8)[2:].upper() + str(pass1[line[1]])
                
            # Direct Reference
            else:
                pass2[olc] = memory_ref[line[0]] + str(pass1[line[1]])
        else:
            # Variable containing instruction
            if len(line) == 2:
                pass2[olc] = reg_ref[line[1]]
            else:
            
                # If it is decimal, convert it
                if line[1] == "DEC":
                    val = int(line[2])
                    if(val < 0): val = calc_neg_hex(val)[2:]
                    else: val = hex(val)[2:]
                else:
                    val = line[2]

                # Store the values in the pass2 dict
                val = val.zfill(4).upper()
                pass2[olc] = val
        # Increment the location counter
        olc += 1
        
def first_pass():
    """
    First pass of the program which stores the location
    and the names of the variable in the 'pass1' dict
    """
    # First pass
    for idx, elem in enumerate(lst_of_instructs):
        # Check for the ORG instruction
        if elem[0] == "ORG":
            
            # Store the value of the location counter
            location_counter = int(elem[1]) - 2            
            
        # If you reached the end, do the second pass
        elif elem[0] == "END":
            second_pass()
            
        # Increment the counter
        location_counter += 1
        
        # Store the values of the variables and their locations
        if elem[0][-1] == ",":
            pass1[elem[0][:-1]] = location_counter
first_pass()
pass2

