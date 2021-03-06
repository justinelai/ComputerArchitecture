"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
POP = 0b01000110
PUSH = 0b01000101

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.ram = [0] * 256 #256 bytes of memory
        self.pc = 0 # Program Counter, address of the currently executing instruction
        self.branchtable = {}
        self.branchtable[HLT] = self.handle_hlt
        self.branchtable[LDI] = self.handle_ldi
        self.branchtable[PRN] = self.handle_prn
        self.branchtable[MUL] = self.handle_mul
        self.branchtable[PUSH] = self.push
        self.branchtable[POP] = self.pop
        self.sp = 7
        self.reg[self.sp] = 0xf4 # initialize stack pointer to empty stack

    def push(self, *operands):
        self.reg[self.sp] -= 1 #decrement sp
        reg_num = self.ram[self.pc + 1]
        reg_value = self.reg[reg_num]
        self.ram[self.reg[self.sp]] = reg_value # copy register value into memory at address SP
        self.pc += 2
    
    def pop(self, *operands):
        val = self.ram[self.reg[self.sp]]
        reg_num = self.ram[self.pc + 1]
        self.reg[reg_num] = val # copy val FROM memory at SP into register
        self.reg[self.sp] += 1
        self.pc += 2

    def load(self):
        if len(sys.argv) != 2:
            print("Usage: file.py filename", file=sys.stderr)
            sys.exit(1)
        try:
            address = 0
            with open(sys.argv[1]) as f:
                for line in f:
                    # Ignore comments
                    comment_split = line.split("#")
                    num = comment_split[0].strip()
                    if num == "":
                        continue  # Ignore blank lines
                    value = int(num, 2)   # Base 10, but ls-8 is base 2
                    self.ram[address] = value
                    address += 1
        except FileNotFoundError:
            print(f"{sys.argv[0]}: {sys.argv[1]} not found")
            sys.exit(2)
        
    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
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

    def ram_read(self, address):
        # should accept the address to read and return the value stored there.
        return self.ram[address]
       
    def ram_write(self, address, value):
        # should accept a value to write, and the address to write it to.
        self.ram[address] = value

    def run(self):
        """Run the CPU."""
        print("Running CPU...")
        running = True
        while running:
            self.trace()
            ir = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            self.branchtable[ir](operand_a, operand_b)
    
    def handle_hlt(self, operand_a, operand_b):
        print("Halted!")
        self.running = False
        sys.exit(1) # Error exit status
    def handle_ldi(self, operand_a, operand_b):
        # LDI register immediate - Set the value of a register to an integer.
        self.reg[operand_a] = operand_b
        self.pc += 3
    def handle_prn(self, operand_a, operand_b):
        # PRN register pseudo-instruction - Print numeric value stored in the given register.
        # Print to the console the decimal integer value that is stored in the given register.
        print(self.reg[operand_a])
        self.pc += 2
    def handle_mul(self, operand_a, operand_b):
        self.alu("MUL", operand_a, operand_b)
        self.pc += 3