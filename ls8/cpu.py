"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.pc = 0
        self.reg = [0] * 8
        self.halted = False 

    def load(self):
        """Load a program into memory."""

        address = 0

        program = sys.argv[1]

        with open(sys.argv[1]) as program: # grab the second sys argument as program

            for instruction in program: # iterate through the lines

                i = instruction.find('#') # look for comments by searching the index
                instruction = instruction[:i] # slice the comment off
                instruction = instruction.rstrip() # remove whitespace

                if len(instruction) > 0: # if the length of the line is greater than 0
                    # add it to the memory and convert to binary literal integer
                    self.ram[address] = int("0b"+instruction, 2) 
                    address += 1 # increment address


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "DIV":
            self.reg[reg_a] /= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")
        self.pc += 3

    def ldi(self, mar, value):
        """
        Set the value of a register to an integer.
        """
        print(f"ldi called on {self.reg[mar]}")
        self.reg[mar] = value
        self.pc += 3

    def prn(self, mar):
        """
        Print to the console the decimal integer value that is stored in the given
        register.
        """
        print(self.reg[mar])
        self.pc += 2

    def ram_read(self, mar):
        """
        Should accept the address to read and return the value stored there.
        Memory Address Register (MAR) contains the address being read to
        Memory Data Register (MDR) contains the read data
        """
        mdr = self.ram[mar]
        return mdr

    def ram_write(self, mdr, mar):
        """
        Should accept a value to write, and the address to write it to.
        Memory Data Register (MDR) contains the data to write
        Memory Address Register (MAR) contains the address being written to
        """
        self.ram[mar] = mdr

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
        """
        Run the CPU. It needs to read the memory address that's stored in register 
        Program Counter (PC), and store that result in the Instruction Register (IR). 
        This can just be a local variable
        """
        
        LDI = 0b10000010
        PRN = 0b01000111
        MUL = 0b10100010
        HLT = 0b00000001


        while not self.halted:
            IR = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
                
            # branch_table = { 
            #     "LDI": self.ldi(operand_a, operand_b),
            #     "PRN": self.prn(operand_a),
            #     "MUL": self.alu("MUL", operand_a, operand_b),
            #     "HLT": self.hlt()
            #      }

            # branch_table["IR"]()

            if IR == PRN:
                self.prn(operand_a)

            elif IR == LDI:
                self.ldi(operand_a, operand_b)

            elif IR == MUL:
                self.alu("MUL", operand_a, operand_b)
            
            elif IR == HLT:
                self.hlt()

            else:
                print(f"unknown instruction {IR} at address {self.pc}")
                exit(1)


    def hlt(self):
        """
        Halt the CPU (and exit the emulator).
        """
        self.halted = True
        print(f"exiting")
        exit()
