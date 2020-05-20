"""CPU functionality."""

import sys

""" ALU ops """
ADD = 0b10100000
SUB = 0b10100001
MUL = 0b10100010
DIV = 0b10100011
MOD = 0b10100100
""" PC mutators """
CALL = 0b01010000
RET = 0b00010001
""" Stack ops """
PUSH = 0b01000101
POP = 0b01000110
""" Other """
NOP = 0b00000000
HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256 # memory
        self.pc = 0 # program counter
        self.sp = 0xF4 # stack pointer
        self.reg = [0] * 8 # register
        self.IR = None # instruction register
        self.halted = False # run state

        self.branch_table = {} # dict of methods
        # mathematical methods
        self.branch_table[ADD] = self.alu
        self.branch_table[MUL] = self.alu
        self.branch_table[DIV] = self.alu
        self.branch_table[MOD] = self.alu
        # pc mutator methods
        self.branch_table[CALL] = self.call
        self.branch_table[RET] = self.ret
        # stack methods
        self.branch_table[PUSH] = self.push
        self.branch_table[POP] = self.pop
        # other
        self.branch_table[NOP] = self.nop
        self.branch_table[HLT] = self.hlt
        self.branch_table[LDI] = self.ldi
        self.branch_table[PRN] = self.prn
        # print(self.branch_table)

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


    def alu(self, reg_a, reg_b):
        """ALU operations."""
        op = self.IR

        if op == ADD:
            self.reg[reg_a] += self.reg[reg_b]

        elif op == SUB:
            self.reg[reg_a] -= self.reg[reg_b]

        elif op == MUL:
            self.reg[reg_a] *= self.reg[reg_b]

        elif op == DIV:
            self.reg[reg_a] /= self.reg[reg_b]
        
        elif op == MOD:
            self.reg[reg_a] %= self.reg[reg_b] 
        else:
            raise Exception("Unsupported ALU operation")

    def call(self, reg_a):
        """
        Calls a subroutine (function) at the address stored in the register.
        The address of the instruction following `CALL` is
        pushed onto the stack.
        The PC is set to the address stored in the given register.
        We jump to that location in RAM and execute the first instruction in the subroutine. 
        The PC can move forward or backwards from its current location.
        """
        ret_addr = self.pc + 1
        self.sp -= 1
        self.ram[self.sp] = ret_addr
     
        dest_addr = self.reg[reg_a]
        self.pc = dest_addr

    def ret(self):
        """
        Pop the value from the top of the stack and store it in the `PC`
        """
        ret_addr = self.ram[self.sp]
        self.pc = ret_addr

    def push(self, mar):
        """
        Push the value in the given register on the stack.
        Memory Address Register (MAR) contains the address being read to
        """
        self.sp -= 1
        self.ram[self.sp] = self.reg[mar]

    def pop(self, mdr):
        """
        Pop the value at the top of the stack into the given register.
        Memory Data Register (MDR) contains the read data
        """
        self.reg[mdr] = self.ram[self.sp]
        self.sp += 1

    def nop(self):
        """ No operation. Do nothing for this instruction. """
        pass

    def hlt(self):
        """
        Halt the CPU (and exit the emulator).
        """
        self.halted = True
        # print(f"exiting")
        exit()

    def ldi(self, mar, value):
        """
        Set the value of a register to an integer.
        """
        self.reg[mar] = value
        # print(f"ldi called on register {mar}: {self.reg[mar]}")

    def prn(self, mar):
        """
        Print to the console the decimal integer value that is stored in the given
        register.
        """
        print(self.reg[mar])

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

    def run(self):
        """
        Run the CPU. It needs to read the memory address that's stored in register 
        Program Counter (PC), and store that result in the Instruction Register (IR). 
        This can just be a local variable
        """
    
        while not self.halted:
            self.IR = self.ram_read(self.pc)
            operand_qty = self.IR >> 6 # right shift to get the the arg value
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if operand_qty == 0:
                self.branch_table[self.IR]()

            elif operand_qty == 1:
                self.branch_table[self.IR](operand_a)

            elif operand_qty == 2:
                self.branch_table[self.IR](operand_a, operand_b)

            else:
                print(f"unknown instruction {self.IR} at address {self.pc}")
                exit(1)

            if self.IR != CALL | self.IR != RET: # call and return mutate pc
                self.pc += operand_qty + 1 # increment by number of args add 1 for self

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

