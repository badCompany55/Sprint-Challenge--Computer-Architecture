"""CPU functionality."""

import sys

HTL = 0b00000001 # HLT Stops the run
LDI = 0b10000010 # LDI R0,8
PRN = 0b01000111 # PRN R0
MUL = 0b10100010 # MUL R0,R1
ADD = 0b10100000
PUSH = 0b01000101 # Push
POP = 0b01000110 # Pop
CALL = 0b01010000
RET = 0b00010001
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.fl = 0
        self.reg[7] = 0xF4

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    def load(self, file):
        """Load a program into memory."""
        address = 0

        program = []
        f = open(f'./examples/{file}.ls8', "r")
        fr = f.readlines()
        for x in fr:
            if "#" not in x and x.strip():
                new_x = int(x, 2)
                program.append(new_x)
            elif " #" in x:
                index = x.index(" ")
                split = x[0:index + 1]
                new_x = int(split, 2)
                program.append(new_x)



        # For now, we've just hardcoded a program:

       # program = [
       #     # From print8.ls8
       #     LDI, # LDI R0,8
       #     0b00000000,
       #     0b00001000,
       #     PRN, # PRN R0
       #     0b00000000,
       #     HTL,
       # ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ALU_ADD":
            self.reg[reg_a] = self.reg[reg_a] + self.reg[reg_b]
        elif op == "ALU_MUL":
            self.reg[reg_a] = self.reg[reg_a] * self.reg[reg_b]
        elif op == "ALU_CMP":
            if self.reg[reg_a] == self.reg[reg_b]:
                self.fl = 0b00000001
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.fl = 0b10000010
            else:
                self.fl = 0b00000100

        #elif op == "SUB": etc

        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def push(self, val):
        self.reg[7] -= 1
        self.ram_write(self.reg[7], val)
#        print("val", val)
#        print("valueReg:", self.ram[self.reg[7]])

    def pop(self):
        val = self.ram[self.reg[7]]
        self.reg[7] += 1
        return val

    def run(self):
        running = True

        while running:
            """Run the CPU."""
            # store the memory address in pc in a local variable
            # this the location of the command that needs to be ran
            IR = self.ram_read(self.pc)

#             instructions state that up to 2 memory slots will be used
#             using ram_read, get the next 2 commands and store them
#             in operand_a / operand_b

#            shift the binary 6 places to the right. 
#            this is will give me the last two digits
#            check if it is a 1 or a 2 
#            if 1, add one to the pc for the first arg
#            if 2 add two for the second arg
#                add one for the first arg
#            this calculated the amount to add to the pc at the beginning
#            instead of doing it in each block
            number_of_opers = IR >> 6
            if number_of_opers == 2:
                operand_a = self.ram_read(self.pc + 1)
                operand_b = self.ram_read(self.pc + 2)
            else:
                operand_a = self.ram_read(self.pc + 1)


            if IR == HTL:
                self.pc = 0
                running = False
            elif IR == LDI:
                self.reg[operand_a] = operand_b
            elif IR == PRN:
                print(self.reg[operand_a])
            elif IR == MUL:
                self.alu("ALU_MUL", operand_a, operand_b)
                # print("MUL")
            elif IR == PUSH:
                self.push(self.reg[operand_a])
            elif IR == POP:
                self.reg[operand_a] = self.pop()
            elif IR == CALL:
                self.push(self.pc + 1)
                self.pc = self.reg[operand_a] - 2
            elif IR == ADD:
                self.alu("ALU_ADD", operand_a, operand_b)
                # print("ADD")
            elif IR == RET:
                self.pc = self.pop()
            elif IR == CMP:
                self.alu("ALU_CMP", operand_a, operand_b)
            elif IR == JMP:
                self.pc = self.reg[operand_a] - number_of_opers - 1
            elif IR == JEQ:
                if self.fl == 0b00000001:
                    self.pc = self.reg[operand_a] - number_of_opers - 1
            elif IR == JNE:
                if self.fl == 0b00000100:
                    self.pc = self.reg[operand_a] - number_of_opers - 1

            #    return self.reg[operand_a]
            self.pc += number_of_opers + 1
