import argparse
from bitstring import BitArray
'''
For the alpha implementation, we consider these valid instructions only: add, sub, and addi. Additionally, we will only work with registers 0 to 7.
'''

def r_type_registers(rs, rt, rd, shamt, funct, registers): #Finds the change in registers from the operation
    #Converting registers to decimal
    rs = BitArray(bin=rs)
    rs = rs.int
    rt = BitArray(bin=rt)
    rt = rt.int
    rd = BitArray(bin=rd)
    rd = rd.int
    #Doing the operation
    if funct == '100000':
        registers[rd] = registers[rs] + registers[rt]
    elif funct == '100010':
        registers[rd] = registers[rs] - registers[rt]
    else:
        registers[rd] = registers[rd]
    return registers

def r_type_control(funct): #Finds the control signals of the r_type function given its funct
    if funct == '100010': #Sub
        return '1001000100'
    elif funct == '100000': #Add
        return '1001000100'
    else:
        return '0'
def i_type_registers(opcode, rs, rt, immd, registers): #Finds the change in registers given the I type operation
    rs = BitArray(bin=rs)
    rs = rs.int
    rt = BitArray(bin=rt)
    rt = rt.int
    immd = BitArray(bin=immd)
    immd = immd.int
    if opcode == '001000':
        registers[rt] = registers[rs] + immd
    else:
        registers[rt] = registers[rt]
    return registers
def i_type_control(opcode): #Finds the control signal given the I typ eoperation
    if opcode == '001000':
        return "0101000000"
    else:
        return "0"
def registers_to_string(registers = [], *args): #For printing the registers in out_registers.txt, assumes has already been converted to decimal
    str_reg = ""
    for r in registers:
        str_reg = str_reg + (str(r) + "|")
    str_reg = str_reg[0:(len(str_reg) - 1)]
    return str_reg
        


def main():
    #Creating the argparser
    parser = argparse.ArgumentParser(prog = "Mips Assembly Binary Encoder", description="Takes in an input file of MIPS Binary and ")
    parser.add_argument('--program',type=str,help="Provide the filename and filepath of the input file. Example: -i ~/alpha.bin")
    args = parser.parse_args()
    inFile = open(args.program, "r")
    outControl = open("out_control.txt", "w")
    outRegister = open("out_registers.txt","w")
    pc = 65536
    outRegister.write("65536|0|0|0|0|0|0|0|0\n")
    lineCount = 0
    registers = [0, 0, 0, 0, 0, 0, 0, 0]
    for line in inFile:
        lineCount += 1
        if (lineCount > 100): #Check if over 100 lines have been written
            break
        else: 
            #Parse the instructions
            opcode = line[0:6]
            rs = line[6:11]
            rt = line[11:16]
            if opcode != '000000': #If not an R Type
                immediate = line[16:32]
                outControl.write(str(i_type_control(opcode)) + "\n")
                pc += 4;
                registers = i_type_registers(opcode, rs, rt, immediate, registers)
                outRegister.write(str(pc) + "|" + str(registers_to_string(registers)) + "\n")
            else: #If an R Type
                rd = line[16:21]
                shamt = line[21:26]
                funct = line[26:32]
                outControl.write(str(r_type_control(funct)) + "\n")
                pc += 4;
                registers = r_type_registers(rs, rt, rd, shamt, funct,registers)
                outRegister.write(str(pc) + "|" + str(registers_to_string(registers)) + "\n")
            

          

main()
print("Program Finished")