import struct
import csv
import sys

# Команды УВМ
COMMANDS = {
    'LOAD_CONST': 16,
    'READ_MEMORY': 25,
    'WRITE_MEMORY': 99,
    'BIN_OP_MAX': 30
}

class Assembler:
    @staticmethod
    def assemble(input_file, output_file, log_file):
        binary_code = []
        log_entries = []

        with open(input_file, 'r') as f:
            lines = f.readlines()

        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue  # Игнорируем пустые строки и комментарии

            parts = line.split()
            if len(parts) < 1:
                raise ValueError(f"Invalid instruction format: '{line}'")

            command = parts[0]
            if command == 'LOAD_CONST':
                if len(parts) < 2:
                    raise ValueError(f"LOAD_CONST requires a constant value: '{line}'")
                const = int(parts[1])
                binary_code.extend(struct.pack('<BIB', COMMANDS[command], const, 0)[:5])
                log_entries.append({'command': command, 'const': const, 'offset': None})
            elif command == 'READ_MEMORY':
                if len(parts) < 2:
                    raise ValueError(f"READ_MEMORY requires an offset: '{line}'")
                offset = int(parts[1])
                binary_code.extend(struct.pack('<BH', COMMANDS[command], offset))
                log_entries.append({'command': command, 'const': None, 'offset': offset})
            elif command == 'WRITE_MEMORY':
                binary_code.append(COMMANDS[command])
                log_entries.append({'command': command, 'const': None, 'offset': None})
            elif command == 'BIN_OP_MAX':
                if len(parts) < 2:
                    raise ValueError(f"BIN_OP_MAX requires an offset: '{line}'")
                offset = int(parts[1])
                binary_code.extend(struct.pack('<BH', COMMANDS[command], offset))
                log_entries.append({'command': command, 'const': None, 'offset': offset})
            else:
                raise ValueError(f"Unknown command: '{command}'")

        with open(output_file, 'wb') as f:
            f.write(bytearray(binary_code))

        with open(log_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['command', 'const', 'offset'])
            writer.writeheader()
            writer.writerows(log_entries)

class Interpreter:
    def __init__(self, memory_size=1024):
        self.memory = [0] * memory_size
        self.stack = []

    def check_stack(self, count):
        if len(self.stack) < count:
            raise IndexError(f"Stack underflow: expected at least {count} elements, but found {len(self.stack)}")

    def debug_stack(self):
        print(f"Stack state: {self.stack}")

    def debug_memory(self):
        print(f"Memory state (first 10): {self.memory[:10]}")

    def execute(self, binary_file, output_file, memory_range):
        with open(binary_file, 'rb') as f:
            code = f.read()

        pc = 0
        while pc < len(code):
            opcode = code[pc]
            print(f"Executing opcode: {opcode}, PC: {pc}")
            self.debug_stack()

            if opcode == COMMANDS['LOAD_CONST']:
                const = struct.unpack_from('<I', code, pc + 1)[0]
                self.stack.append(const)
                pc += 5
            elif opcode == COMMANDS['READ_MEMORY']:
                self.check_stack(1)
                offset = struct.unpack_from('<H', code, pc + 1)[0]
                address = self.stack.pop() + offset
                self.stack.append(self.memory[address])
                pc += 3
            elif opcode == COMMANDS['WRITE_MEMORY']:
                self.check_stack(2)
                address = self.stack.pop()
                value = self.stack.pop()
                print(f"Writing value {value} to memory address {address}")
                if 0 <= address < len(self.memory):
                    self.memory[address] = value
                else:
                    raise IndexError(f"Invalid memory address: {address}")
                self.debug_memory()
                pc += 1
            elif opcode == COMMANDS['BIN_OP_MAX']:
                self.check_stack(2)
                value1 = self.stack.pop()
                value2 = self.stack.pop()
                self.stack.append(max(value1, value2))
                print(f"Computed max({value1}, {value2}) = {max(value1, value2)}")
                pc += 3

        with open(output_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Address', 'Value'])
            for i in range(*memory_range):
                writer.writerow([i, self.memory[i]])

# Тестовая программа
if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: python script.py <input_file> <binary_file> <log_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    binary_file = sys.argv[2]
    log_file = sys.argv[3]
    output_file = sys.argv[4]

    assembler = Assembler()
    assembler.assemble(input_file, binary_file, log_file)

    interpreter = Interpreter()
    interpreter.execute(binary_file, output_file, (0, 10))
