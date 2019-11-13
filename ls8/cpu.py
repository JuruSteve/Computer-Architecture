"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0]*256
        self.reg = [0]*8
        self.pc = 0
        self.instructions = {'HLT':0b00000001, 'LDI': 0b10000010, 'PRN': 0b01000111, "ADD": 0b10100000, "MUL": 0b10100010, "PUSH": 0b01000101, "POP": 0b01000110} 
    
    # def run(self, file_instructions):
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
        new_commands = []
        if len(sys.argv) != 2:
            print("Usage: ls8.py filename")
            sys.exit(1)
        else:
            address = 0
            with open(f"examples/{sys.argv[1]}") as f:
                for line in f:
                    l = line.split('\n')[0].split('#')[0].strip()
                    if line == '':
                        continue
                    new_commands.append(l)
        for instruction in new_commands:
            if instruction != '':
                self.ram[address] = int(instruction, 2)
                address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")
    
    def ram_read(self, adr_to_read):
        return self.ram[adr_to_read]
    def ram_write(self, adr_to_write, value):
        self.ram[adr_to_write] = value
        # return self.ram[adr_to_write]
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
        halted = False

        while not halted:
            Ir = self.ram[self.pc]
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            if Ir == self.instructions['HLT']:
                halted = True
            elif Ir == self.instructions['LDI']:
                self.reg[operand_a] = operand_b
                self.pc +=3
            elif Ir == self.instructions['PRN']:
                val = self.reg[operand_a]
                self.pc +=2
                print(val)
            elif Ir == self.instructions['MUL']:
                self.alu('MUL', operand_a, operand_b)
                self.pc +=3
            else:
                print('Unknown instruction')
                sys.exit(1)