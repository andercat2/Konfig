import sys
import csv

def assemble(input_file, output_file, log_file):
    instructions = []
    with open(input_file, 'r') as f:
        lines = f.readlines()

    address = 0
    log = []

    for line in lines:
        line = line.strip()
        if not line or line.startswith(';'):
            continue

        parts = line.split()
        opcode = parts[0]
        operands = parts[1:]

        if opcode == 'LOAD_CONST':
            A = 16
            B = int(operands[0])
            instr = A | (B << 7)
            binary_instr = instr.to_bytes(5, byteorder='little')
        elif opcode == 'LOAD_MEM':
            A = 25
            B = int(operands[0])
            instr = A | (B << 7)
            binary_instr = instr.to_bytes(3, byteorder='little')
        elif opcode == 'STORE_MEM':
            A = 99
            instr = A
            binary_instr = instr.to_bytes(1, byteorder='little')
        elif opcode == 'MAX':
            A = 30
            B = int(operands[0])
            instr = A | (B << 7)
            binary_instr = instr.to_bytes(3, byteorder='little')
        else:
            continue

        instructions.append(binary_instr)
        log.append({'address': address, 'instruction': binary_instr.hex()})
        address += len(binary_instr)

    with open(output_file, 'wb') as f:
        for instr in instructions:
            f.write(instr)

    with open(log_file, 'w', newline='') as csvfile:
        fieldnames = ['address', 'instruction']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for entry in log:
            writer.writerow(entry)

if __name__ == '__main__':
    assemble(sys.argv[1], sys.argv[2], sys.argv[3])