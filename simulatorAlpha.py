import argparse
from bitstring import BitArray
'''

'''

def r_type_registers(rs, rt, rd, shamt, funct):
    return 0
def r_type_control(funct):
    if funct == '100010': #Sub
        return '1001000100'
    elif funct == '100000': #Add
        return '1001000100'
    else:
        return '0'
def i_type_registers(opcode, rs, rt, immd):
    return 0
def i_type_control(opcode):
    if opcode == '001000':
        return "0101000000"
    else:
        return "0"


def main():
    parser = argparse.ArgumentParser(prog = "Mips Assembly Binary Encoder", description="Takes in an input file of MIPS Binary and ")
    parser.add_argument('--program',type=str,help="Provide the filename and filepath of the input file. Example: -i ~/alpha.bin")
    args = parser.parse_args()
    print("Input File: " + args.program)
    inFile = open(args.program, "r")
    outControl = open("out_control.txt", "w")
    outRegister = open("out_registers.txt","w")
    pc = 65536
    outRegister.write("65536|0|0|0|0|0|0|0|0\n")
    lineCount = 0
    registers = [0,0,0,0,0,0,0,0]
    for line in inFile:
        lineCount += 1
        if (lineCount > 100): #Check if over 100 lines have been written
            break
        else: 
            opcode = line[0:6]
            print(opcode)
            rs = line[6:11]
            print(rs)
            rt = line[11:16]
            print(rt)
            if opcode != '000000':
                immediate = line[16:32]
                print(len(immediate))
                outControl.write(str(i_type_control(opcode)) + "\n")
                pc += 4;
                outRegister.write(str(pc) + " | " + str(i_type_registers(opcode, rs, rt, immediate)) + "\n")
            else:
                rd = line[16:21]
                print(rd)
                shamt = line[21:26]
                print(shamt)
                funct = line[26:32]
                print(funct)
                outControl.write(str(r_type_control(funct)) + "\n")
                pc += 4;
                outRegister.write(str(pc) + " | " + str(r_type_registers(rs, rt, rd, shamt, funct)) + "\n")
            

          

main()