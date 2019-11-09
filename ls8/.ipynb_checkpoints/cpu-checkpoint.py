"""CPU functionality."""

import sys

HTL = 0b00000001 # HLT Stops the run
LDI = 0b10000010 # LDI R0,8
PRN = 0b01000111 # PRN R0
MUL = 0b10100010 # MUL R0,R1

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8 
        self.pc = 0
        
    def ram_read(self, MAR):
        return self.ram[MAR]
    
    def ram_write(self, MDR, MAR):
        self.ram[MAR] = MDR

    def load(self, file):
        """Load a program into memory."""
        address = 0
        
        program = []
        f = open(f'./examples/{file}', "r")
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
            new_val = self.reg[reg_a] + self.reg[reg_b]
        elif op == "ALU_MUL":
            self.reg[reg_a] = self.reg[reg_a] * self.reg[reg_b]
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

    def run(self):
        running = True
        
        while running:
            """Run the CPU."""
            # store the memory address in pc in a local variable
            # this the location of the command that needs to be ran
            IR = self.ram_read(self.pc)

            # instructions state that up to 2 memory slots will be used
            # using ram_read, get the next 2 commands and store them
            # in operand_a / operand_b
            
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
               
            #    return self.reg[operand_a]
            self.pc += number_of_opers + 1
            
        
        
