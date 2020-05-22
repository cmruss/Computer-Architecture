"""CPU functionality."""

import sys
import os
from datetime import datetime

""" ALU ops """
ADD = 0b10100000
SUB = 0b10100001
MUL = 0b10100010
DIV = 0b10100011
MOD = 0b10100100
CMP = 0b10100111
""" PC mutators """
CALL = 0b01010000
RET = 0b00010001
IRET = 0b00010011
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110
""" Stack ops """
PUSH = 0b01000101
POP = 0b01000110
""" Other """
NOP = 0b00000000
HLT = 0b00000001
LDI = 0b10000010
ST = 0b10000100
PRN = 0b01000111
PRA = 0b01001000

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256 # memory
        self.reg = [0] * 8 # register
        self.pc = 0 # program counter
        self.sp = 7 # stack pointer
        self.fl = 0b11000000
        self.reg[self.sp] = 0xF4
        self.ir = None # instruction register
        self.init_time = datetime.now() # time initialized
        self.halted = False # run state

        self.branch_table = {} # dict of methods
        # mathematical methods
        self.branch_table[ADD] = self.alu
        self.branch_table[SUB] = self.alu
        self.branch_table[MUL] = self.alu
        self.branch_table[DIV] = self.alu
        self.branch_table[MOD] = self.alu
        self.branch_table[CMP] = self.alu
        # pc mutator methods
        self.branch_table[CALL] = self.call
        self.branch_table[RET] = self.ret
        self.branch_table[IRET] = self.iret
        self.branch_table[JMP] = self.jmp
        self.branch_table[JEQ] = self.jeq
        self.branch_table[JNE] = self.jne
        # stack methods
        self.branch_table[PUSH] = self.push
        self.branch_table[POP] = self.pop
        # other methods
        self.branch_table[NOP] = self.nop
        self.branch_table[HLT] = self.hlt
        self.branch_table[LDI] = self.ldi
        self.branch_table[ST] = self.st
        self.branch_table[PRN] = self.prn
        self.branch_table[PRA] = self.pra
        # print(self.branch_table)

    def load(self):
        """Load a program into memory."""
        address = 0 # line pointer
        program = sys.argv[1] # the program to load
        programs = os.listdir("examples/") # programs from examples/
        try:
            with open(sys.argv[1]) as program: # grab the second sys argument as program
                for instruction in program: # iterate through the lines
                    i = instruction.find('#') # look for comments by searching the index
                    instruction = instruction[:i] # slice the comment off
                    instruction = instruction.rstrip() # remove whitespace
                    if len(instruction) > 0: # if the length of the line is greater than 0
                        # add it to the memory and convert to binary literal integer
                        self.ram[address] = int("0b"+instruction, 2) 
                        address += 1 # increment address
        except: # error handling for bad argv
            print(f"\nPlease select a program from example/:\n\n{programs}\n")
            exit()

    def alu(self, reg_a, reg_b):
        """ALU operations."""
        op = self.ir
        # ops = {}
        if op == ADD:
            self.reg[reg_a] += self.reg[reg_b]
        # ops[ADD] = self.reg[reg_a] += self.reg[reg_b]
        elif op == SUB:
            self.reg[reg_a] -= self.reg[reg_b]
        # ops[SUB] = self.reg[reg_a] += self.reg[reg_b]
        elif op == MUL:
            self.reg[reg_a] *= self.reg[reg_b]
        # ops[MUL] = self.reg[reg_a] += self.reg[reg_b]
        elif op == DIV:
            self.reg[reg_a] /= self.reg[reg_b]
        # ops[DIV] = self.reg[reg_a] += self.reg[reg_b]       
        elif op == MOD:
            self.reg[reg_a] %= self.reg[reg_b] 
        # ops[MOD] = self.reg[reg_a] += self.reg[reg_b]
        elif op == CMP:
            self.fl = self.fl & 0b11111000 # clear LGE flags
            if self.reg[reg_a] < self.reg[reg_b]:
                self.fl = self.fl | 0b00000100 # set L
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.fl = self.fl | 0b00000010 # set G
            elif self.reg[reg_a] == self.reg[reg_b]:
                self.fl = self.fl | 0b00000001 # set E
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
        ret_addr = self.pc + 2
        self.reg[self.sp] -= 1
        self.ram[self.reg[self.sp]] = ret_addr
     
        dest_addr = self.reg[reg_a]
        self.pc = dest_addr

    def ret(self):
        """
        Pop the value from the top of the stack and store it in the `PC`
        """
        ret_addr = self.ram[self.reg[self.sp]]
        self.reg[self.sp] += 1
        self.pc = ret_addr

    def iret(self):
        """
        Return from an interrupt handler.
        The following steps are executed
        1. Registers R6-R0 are popped off the stack in that order.
        2. The `FL` register is popped off the stack.
        3. The return address is popped off the stack and stored in `PC`.
        4. Interrupts are re-enabled
        """
        # print(self.ram)
        for r in reversed(range(7)):
            self.pop(r) 
            # print(f"REG {r}: {self.reg[r]}")

        self.fl = self.ram[self.reg[self.sp]]
        self.reg[self.sp] += 1
        # print(F"FL {self.fl}")
        
        self.pc = self.ram[self.reg[self.sp]]
        self.reg[self.sp] +=1
        # print(f"PC {self.pc}")
        # print(f"iret done")
        self.reg[5] = 1 # re-enable interrupts

    def jmp(self, reg_a):
        """
        Jump to the address stored in the given register.
        Set the `PC` to the address stored in the given register.
        """
        # print(self.ram[self.reg[reg_a]])
        self.pc = self.reg[reg_a]
        # print('jumping')

    def jeq(self, reg_a):
        """
        If `equal` flag is set (true), jump to the address stored in the given register.
        """
        if self.fl & 0b00000001:
            self.pc = self.reg[reg_a]
        else:
            self.pc += 2

    def jne(self, reg_a):
        """
        If `E` flag is clear (false, 0), jump to the address 
        stored in the given register.
        """
        if not self.fl & 0b00000001:
            self.pc = self.reg[reg_a]
        else:
            self.pc +=2

    def push(self, mar):
        """
        Push the value in the given register on the stack.
        Memory Address Register (MAR) contains the address being read to
        """
        self.reg[self.sp] -= 1
        self.ram[self.reg[self.sp]] = self.reg[mar]

    def pop(self, mdr):
        """
        Pop the value at the top of the stack into the given register.
        Memory Data Register (MDR) contains the read data
        """
        self.reg[mdr] = self.ram[self.reg[self.sp]]
        self.reg[self.sp] += 1

    def nop(self):
        """ No operation. Do nothing for this instruction. """
        pass

    def hlt(self):
        """
        Halt the CPU (and exit the emulator).
        """
        self.halted = True
        exit()

    def ldi(self, mar, value):
        """
        Set the value of a register to an integer.
        """
        self.reg[mar] = value
        # print(f"ldi called on register {mar}: {self.reg[mar]}")

    def st(self, reg_a, reg_b):
        """
        Store value in registerB in the address stored in registerA.
        """
        self.ram[self.reg[reg_a]] = self.reg[reg_b]

    def prn(self, mar):
        """
        Print to the console the decimal integer value that is stored in the given
        register.
        """
        print(self.reg[mar])

    def pra(self, mar):
        """
        Print to the console the ASCII character corresponding to 
        the value in the register.
        """
        print(chr(self.reg[mar]))

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
        Program Counter (PC), and store that result in the Instruction Register (ir). 
        This can just be a local variable
        """
        while not self.halted:
            # print(self.pc)
            
            time = datetime.now()
            if (time - self.init_time).seconds > 0:
                self.init_time = time # reset timer
                # if timer reaches 1 set interrupt bit
                self.reg[6] = 0b00000001
            IM = self.reg[5]
            IS = self.reg[6]
            masked_interrupts = IM & IS
            # print(time, self.init_time)
            # print(masked_interrupts)
            for i in range(8):
                if ((masked_interrupts >> i) & 1) == 1:
                    self.reg[5] = 0 # disable interrupts
                    self.reg[6] = 0 # clear the bit in IS
                    self.reg[self.sp] -= 1
                    # print(F"PC in: {self.pc}")
                    self.ram[self.reg[self.sp]] = self.pc
                    self.reg[self.sp] -= 1
                    # print(F"FL in: {self.fl}")
                    self.ram[self.reg[self.sp]] = self.fl
                    for r in range(7):
                        self.push(r)
                        # print(f"REG {r} in: {self.reg[r]}")
                    self.pc = self.ram[0xF8]
                    # print(self.pc)
                    break

            self.ir = self.ram_read(self.pc)
            pc_mutator = (self.ir & 0b00010000) >> 4 # mask to get the pc mutation value
            operand_qty = self.ir >> 6 # right shift to get the the arg value
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if operand_qty == 0:
                self.branch_table[self.ir]()

            elif operand_qty == 1:
                self.branch_table[self.ir](operand_a)

            elif operand_qty == 2:
                self.branch_table[self.ir](operand_a, operand_b)

            else:
                print(f"unknown instruction {self.ir} at address {self.pc}")
                exit(1)

            if not pc_mutator:
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
