"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""


        #8 general-purpose 8-bit numeric registers R0-R7.
        #R5 is reserved as the interrupt mask (IM)
        #R6 is reserved as the interrupt status (IS)
        #R7 is reserved as the stack pointer (SP)
        #Only hold values between 0-255. After performing math on registers in the emulator, bitwise-AND the result with 0xFF (255) to keep the register values in that range.
        
        self.reg = [0b0] * 8
        self.ram = [0b0] * 2**8 #256 bytes of memory
        self.pc = 0 # Program Counter, address of the currently executing instruction
        self.mar = None # Memory Address Register (MAR) contains the address that is being read or written to.
        self.mdr = None # Memory Data Register (MDR) contains the data that was read or the data to write. 
        # You don't need to add the MAR or MDR to your CPU class, but they would make handy parameter names for ram_read() and ram_write(), if you wanted.
        self.ir = None # Instruction register contains a copy of the currently executing instruction

        self.opcodes = {
            0b10000010: "LDI",
            0b01000111: "PRN",
            0b00000001: "HLT"
        }


    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def ram_read(self, address):
        # should accept the address to read and return the value stored there.
        return self.ram[address]
       
    def ram_write(self, value, address):
        # should accept a value to write, and the address to write it to.
        return self.ram[address] = value

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
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
        """Run the CPU."""
        """
        It needs to read the memory address that's stored in register PC, and store that result in IR, the Instruction Register. This can just be a local variable in run(). 
        """
        running = True
        print("Running CPU...")
        while True:
            self.ir = self.ram_read(self.pc)
            opcode = self.opcodes[self.ir]
            if opcode has two args
                operand_a = self. [self.pc + 1]
                operand_b = 
            elif opcode has one arg
                operand_a = 
            else: