import argparse
from bitstring import BitArray
'''
For the beta implementation, we consider these valid instructions only: add, sub, and addi. lw, sw, bne, beq Additionally, we will only work with registers 0 to 7.
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
def i_type_registers(opcode, rs, rt, immd, registers, memory): #Finds the change in registers given the I type operation
    rs = BitArray(bin=rs)
    rs = rs.int
    rt = BitArray(bin=rt)
    rt = rt.int
    immd = BitArray(bin=immd)
    immd = immd.int
    if opcode == '001000':
        registers[rt] = registers[rs] + immd
    elif opcode == '100011':
        registers[rt] = str(memory[int(registers[rs]/4) + int(immd/4)]).replace("\n","")
    return registers
def i_type_memory(opcode, memory, registers, rs, rt, immd):
    rs = BitArray(bin=rs)
    rs = rs.int
    rt = BitArray(bin=rt)
    rt = rt.int
    immd = BitArray(bin=immd)
    immd = immd.int
    if opcode == '101011':
        print(registers[rt])
        memory[int(registers[rs]/4) + int(immd/4)] = str(registers[rt]) + "\n" 
        return memory
    else:
        return memory
def i_type_control(opcode):
     #Finds the control signal given the I typ eoperation
    if opcode == '001000':
        return "0101000000"
    elif opcode == '101011':
        return "X1X0010000"
    elif opcode == '100011':
        return "0111100000"
    else:
        return '0'
def registers_to_string(registers = [], *args): #For printing the registers in out_registers.txt, assumes has already been converted to decimal
    str_reg = ""
    for r in registers:
        str_reg = str_reg + (str(r) + "|")
    str_reg = str_reg[0:(len(str_reg) - 1)]
    return str_reg


def main():
    #Creating the argparser
    parser = argparse.ArgumentParser(prog = "Mips Assembly Binary Encoder", description="Takes in an input file of MIPS Binary and ")
    parser.add_argument('--program',type=str,help="Provide the filename and filepath of the input binary file. Example: -i ~/alpha.bin")
    parser.add_argument('--memory',type=str,help="Provide the filename and filepath of the input memory file. Example: -i ~/memory.txt")
    
    args = parser.parse_args()
    inFile = open(args.program, "r")
    instructions = inFile.readlines()
    memFile = open(args.memory, "r")
    memory = memFile.readlines()
    outControl = open("out_control.txt", "w")
    outRegister = open("out_registers.txt","w")
    outMemory = open("out_memory.txt", "w")
    pc = 65536
    outRegister.write("65536|0|0|0|0|0|0|0|0\n")
    registers = [0, 0, 0, 0, 0, 0, 0, 0]
    lineCount = len(instructions)
    i = 0

    while (i < 100) or (i < lineCount):
        if i == lineCount:
            break
        line = instructions[i]
        #Parse the instructions
        opcode = line[0:6]
        rs = str(line)[6:11]
        rt = str(line)[11:16]
        a = True
        if opcode == '000100' or opcode == '000101':
            rs = BitArray(bin=rs)
            rt = BitArray(bin=rt)
            immediate = BitArray(bin=line[16:32])
            if immediate[0] == 1:
                immediate = (immediate.int) + 1
            else:
                immediate = immediate.int
            if (opcode == '000100'):
                if (registers[rs.int] == registers[rt.int]):
                    i += immediate - 1
                    if immediate < 0:
                        pc += 4*immediate 
                    else:
                        pc += 4*immediate + 4
                    outRegister.write(str(pc) + "|" + str(registers_to_string(registers)) + "\n")
                    if (i > 100 or i > lineCount):
                        outControl.write("X0X0001011\n")
                        outControl.write("!!! Segmentation Fault !!!\r\n")
                        outRegister.write("!!! Segmentation Fault !!!\r\n")
                        outRegister.close
                        outControl.close
                        outMemory.close
                        break
                    else:
                        outControl.write("X0X0001010\n")
                        continue
                else:
                    outControl.write("X0X0001011\n")
            elif opcode == '000101':
                if (registers[rs.int] != registers[rt.int]):
                    i += immediate 
                    if immediate < 0:
                        pc += 4*immediate 
                    else:
                        pc += 4*immediate + 4
                    outRegister.write(str(pc) + "|" + str(registers_to_string(registers)) + "\n")
                    if (i > 100 or i > lineCount):
                        outControl.write("X0X0001111\n")
                        outControl.write("!!! Segmentation Fault !!!\r\n")
                        outRegister.write("!!! Segmentation Fault !!!\r\n")
                        outRegister.close
                        outControl.close
                        outMemory.close
                        break
                    else:
                         outControl.write("X0X0001110\n")
                         continue
                else:
                    pc += 4
                    outRegister.write(str(pc) + "|" + str(registers_to_string(registers)) + "\n")
                    outControl.write("X0X0001111\n")
            else:
                print("Error")
                break
        elif (opcode != '000000'): #If not an R Type
            immediate = str(line)[16:32]
            temp = str(i_type_control(opcode))
            outControl.write(str(temp) + "\n")
            pc += 4;
            registers = i_type_registers(opcode, rs, rt, immediate, registers, memory)
            outRegister.write(str(pc) + "|" + str(registers_to_string(registers)) + "\n")
            memory = i_type_memory(opcode, memory, registers, rs, rt, immediate)
            print(memory)

            
        
        else: #If an R Type
            rd = str(line)[16:21]
            shamt = str(line)[21:26]
            funct = str(line)[26:32]
            outControl.write(str(r_type_control(funct)) + "\n")
            pc += 4;
            registers = r_type_registers(rs, rt, rd, shamt, funct,registers)
            outRegister.write(str(pc) + "|" + str(registers_to_string(registers)) + "\n")
        i += 1
    for line in memory:
        outMemory.write(line)
    outControl.close
    outMemory.close
    outRegister.close
    inFile.close
    memFile.close

          

main()
print("Program Finished")