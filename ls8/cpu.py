"""CPU functionality."""
import sys

HLT = 0b00000001
LDI =  0b10000010
PRN =  0b01000111
ADD =  0b10100000
MUL =  0b10100010
POP =  0b01000110
PUSH =  0b01000101

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0]*256
        self.reg = [0]*8
        self.pc = 0
        self.s_pointer = 7
        self.stopped = False
        self.reg[self.s_pointer] = 0xF4
        self.branch_table = {
            HLT: self.handleHalt, 
            LDI: self.handleLDI,
            PRN: self.handlePrint,
            MUL: self.handleMulti,
            PUSH: self.handlePush,
            POP: self.handlePop
        }
        
    def load(self):
        """Load a program into memory."""
        address = 0
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
        elif op == "LDI":
            self.handleLDI(reg_a, reg_b)
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
    def handlePrint(self, reg_val1, reg_val2):
        val = self.reg[reg_val1]
        self.pc +=2
        print(val)      
    def handleMulti(self, reg_val1, reg_val2):
        self.alu('MUL', reg_val1, reg_val2)
        self.pc +=3
    def handleLDI(self, reg_val1, reg_val2):
        self.reg[reg_val1] = reg_val2
        self.pc +=3
    def handleHalt(self, reg_val1, reg_val2):
        self.stopped = True
        print('Stopping program')
        sys.exit(1)        
    def handleADD(self, reg_val1, reg_val2):
        self.alu('ADD', reg_val1, reg_val2)
        self.pc += 3
    def handlePush(self, reg_num, reg_num2):
        self.reg[self.s_pointer] -= 1        
        val = self.reg[reg_num]
        self.ram[self.reg[self.s_pointer]] = val
        self.pc += 2
    def handlePop(self, reg_num, reg_num2):
        val = self.ram[self.reg[self.s_pointer]]
        self.reg[reg_num] = val
        self.reg[self.s_pointer] += 1
        self.pc += 2
    def run(self):
        """Run the CPU."""

        while not self.stopped:
            Ir = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            if Ir in self.branch_table:
                self.branch_table[Ir](operand_a, operand_b)
            else:
                print('Unknown instruction', Ir)
                sys.exit(1)