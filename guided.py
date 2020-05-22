"""
Number bases
============

how many digits

Base 2      "binary"        eg: 5 = 101, PYTHON 0b101, `bin()`
Base 8      "octal"         PYTHON `oct()`
Base 10     "decimal"       PYTHON `dec()`
Base 16     "hexadecimal"   eg: 5 = 5, PYTHON 0x5, `hex()`
Base 64     "base 64"

0-9
a-z
A-z
/
-

"""
# BINARY
#-------#
"""
BASE 2
+-----8's place (0b1000)
|+----4's place (0b100)
||+---2's place (0b10)
|||+--1's place (0b1)
||||
0000
0001
0010
0011
0100

Binary conversion to decimal
----------------------------
1100
1 * 8 + 1 * 4 = 12
ob110 == 12

"Octet" == Byte | 8 bits
1/2 Byte == Nibble | 4 bits

"""

# HEX
#----#
"""
BASE 16 (0-9A-F)
----------------
 0
 1
 2
 3
 4
 5
 6
 7
 8
 9
 A
 B
 C
 D
 E
 F == 15 == 0b1111
10

One hex digit is exactly 4 bits.
Hex conversion to binary
------------------------
0x06 == 0b00000110

  0     6
0000  0110 <-- "nibble"

0x2A == 0b00101010

  2     A
0010  1010

Binary conversion to hex
------------------------
0b11001100 == 0x??
              0xCC

1100  1100
  C     C

255 = 0b11111111 = 0xFF

#FF00FF
 RRGGBB
(255, 0, 255)
"""

# A simple virtual CPU
# A program that emulates a CPU
#------------------------------#
"""
I want to:
* Store a sequence of instructions
* Go through those instructions, doing whatever they ask

Instructions:
* Print "cmruss" on the screen
* Halts the proogram
"""
PRINT_CMRUSS = 1
HALT  = 2
SAVE_REG = 3
PRINT_REG = 4
ADD = 5 # add two registers

memory = [
    PRINT_CMRUSS, # Print cmruss
    SAVE_REG, # SAVE_REG R0, 12
    0,
    12,
    SAVE_REG,
    1,
    10,
    ADD,
    0,
    1,
    PRINT_REG,
    0,
    HALT, # Halt
]

halted = False

registers = [0,0,0,0,0,0,0,0] # Like variables, named R0-R7

pc = 0  # "Program Counter": index into the memory array,
        # AKA "pointer", "address", "location"

while not halted:
    instruction = memory[pc]

    if instruction == PRINT_CMRUSS:
        print("cmruss")
        pc += 1
        
    elif instruction == SAVE_REG:
        reg_num = memory[pc + 1]
        value = memory[pc + 2]
        registers[reg_num] = value
        pc += 3

    elif instruction == PRINT_REG:
        reg_num = memory[pc + 1]
        print(registers[reg_num])
        pc +=2 

    elif instruction == ADD:
        reg_a = registers[memory[pc + 1]]
        reg_b = registers[memory[pc + 2]]
        registers[memory[pc+1]] = reg_a + reg_b
        pc += 3

    elif instruction == HALT:
        halted = True

    else:
        print(f"unknown instruction {instruction} at address {pc}")
        exit(1)

"""
Bitwise Operations
------------------

12 = 0b1100

1100
1000
1011

1100
0110
0011

Similiar to Boolean operations: and, or, not

A  B        A & B  AND
-------------------
0  0          0
1  0          0
0  1          0
1  1          1

A  B        A | B  OR
-------------------
0  0          0
1  0          1
0  1          1
1  1          1

A  B        A ^ B  XOR
-------------------
0  0          0
1  0          1
0  1          1
1  1          0

    11101001  255.255.255.0 subnet mask
&   00001111  AND-mask
------------
    00001001

    11101001
|   00001111
------------
    11101111

~   1100 NOT
-------- Two's principle
    0011 Swaps 

Shifting
--------
   vv
11001010
   ^^
    11001010
&   00011000 Mask the bits you want
------------
    00001000 
       ^^
    00001000 Shift right by 3
    00000100 x = x >> 3
    00000010
    00000001
          ^^

BASE 10 Analogy
---------------
  vv
123456
009900 Mask
------
003400

003400 Shift
000340
000034

Hex and-mask, shift
------------
  RRGGBB
0xff7fff
0x00ff00 
--------
0x007f00 >> 8
0x00007f

Left shift mulitplies by base
Right shift divides by base

Binary is base 2

0b11000 = 24
0b01100 = 12
0b00110 = 6
0b00011 = 3
0b00001 = 1

BASE 10 Analogy

  12
 120
1200
 120
  12
   1
"""

# Given an object/dictionary with keys and values that consist of both strings and integers, design an algorithm to calculate and return the sum of all of the numeric values. 
# For example, given the following object/dictionary as input:
# ```
my_dict = {
  "cat": "bob",
  "dog": 23,
  19: 18,
  90: "fish"
}

# Your algorithm should return 41, the sum of the values 23 and 18. 
# You may use whatever programming language you'd like.
# Verbalize your thought process as much as possible before writing any code. Run through the UPER problem solving framework while going through your thought process.
def add_ints(dict_obj):
    total = 0
    for k in dict_obj:
        if isinstance(dict_obj[k], int):
            total += dict_obj[k]
    return total

print(add_ints(my_dict))