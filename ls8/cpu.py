"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8 
        self.sp = 7
        self.reg[self.sp] = 0xF4
        self.pc = 0
        self.ir = 0
        self.fl = 6
        self.op_table = {
                        0b10000010 : self.ldi, 
                        0b01000111 : self.prn, 
                        0b10100010 : self.mult,
                        0b00000001 : self.hlt,
                        0b01000101 : self.push,
                        0b01000110 : self.pop,
                        0b01010000 : self.call, 
                        0b00010001 : self.ret,
                        0b10100000 : self.add,
                    }

    def load(self):
        """Load a program into memory."""
        try:
            address = 0
            with open("c:/Users/billy/web27/Computer-Architecture/ls8/examples/call.ls8") as f:
                for line in f:
                    comment_split = line.split("#")
                    n = comment_split[0].strip()
                    if n == '':
                        continue

                    val = int(n, 2)
                    # store val in memory
                    self.ram[address] = val

                    address += 1
        
        except FileNotFoundError:
            print(f"{sys.argv[0]}: {filename} not found")
            sys.exit(2)

    def ldi(self, op_a, op_b):
        self.reg[op_a] = op_b

    def mult(self, op_a, op_b):
        self.reg[op_a] = self.reg[op_a] * self.reg[op_b]

    # Push the value in the given register on the stack.
    def push(self, op_a, op_b):        
        self.reg[self.sp] -= 1
        self.ram[self.reg[self.sp]] = self.reg[op_a]

    # Pop the value at the top of the stack into the given register.
    def pop(self, op_a, op_b):
        self.reg[op_a] = self.ram[self.reg[self.sp]]
        self.reg[self.sp] += 1

    # Sets the PC to the register value
    def call(self, op_a, op_b):
        self.reg[self.sp] -= 1
        self.ram[self.reg[self.sp]] = self.pc + 2
        self.pc = self.reg[op_a]
        return True

    def ret(self, op_a, op_b):
        self.pop(op_a, 0)
        self.pc = self.reg[op_a]
        return True

    def add(self, op_a, op_b):
        self.reg[op_a] = self.reg[op_a] + self.reg[op_b]

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value

    def prn(self, op_a, op_b):
        print(self.reg[op_a])

    def hlt(self, op_a, op_b):
        sys.exit()

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
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
        while True:
            self.ir = self.ram[self.pc]
            op_a = self.ram[self.pc + 1]
            op_b = self.ram[self.pc + 2]

            willJump = self.op_table[self.ir](op_a, op_b)
            if not willJump:
                self.pc += (self.ir >> 6) + 1