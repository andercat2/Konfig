import unittest
import os
from main import Assembler, Interpreter

class TestUVM(unittest.TestCase):

    def setUp(self):
        self.input_file = "test.asm"
        self.binary_file = "binary.bin"
        self.log_file = "log.csv"
        self.output_file = "output.csv"

    def tearDown(self):
        for file in [self.input_file, self.binary_file, self.log_file, self.output_file]:
            if os.path.exists(file):
                os.remove(file)

    def test_max_operation(self):
        program = """LOAD_CONST 10
LOAD_CONST 20
BIN_OP_MAX 0
LOAD_CONST 0
WRITE_MEMORY
"""
        with open(self.input_file, "w") as f:
            f.write(program)

        assembler = Assembler()
        assembler.assemble(self.input_file, self.binary_file, self.log_file)

        interpreter = Interpreter()
        interpreter.execute(self.binary_file, self.output_file, (0, 10))

        with open(self.output_file, "r") as f:
            result = f.readlines()

        self.assertEqual(result[1].strip(), "0,20")

    def test_multiple_max_operations(self):
        program = """LOAD_CONST 15
LOAD_CONST 25
BIN_OP_MAX 0
LOAD_CONST 0
WRITE_MEMORY
LOAD_CONST 30
LOAD_CONST 10
BIN_OP_MAX 0
LOAD_CONST 1
WRITE_MEMORY
LOAD_CONST 50
LOAD_CONST 40
BIN_OP_MAX 0
LOAD_CONST 2
WRITE_MEMORY
"""
        with open(self.input_file, "w") as f:
            f.write(program)

        assembler = Assembler()
        assembler.assemble(self.input_file, self.binary_file, self.log_file)

        interpreter = Interpreter()
        interpreter.execute(self.binary_file, self.output_file, (0, 10))

        with open(self.output_file, "r") as f:
            result = f.readlines()

        self.assertEqual(result[1].strip(), "0,25")
        self.assertEqual(result[2].strip(), "1,30")
        self.assertEqual(result[3].strip(), "2,50")

    def test_memory_read_write(self):
        program = """LOAD_CONST 100
LOAD_CONST 0
WRITE_MEMORY
LOAD_CONST 0
READ_MEMORY 0
LOAD_CONST 0
WRITE_MEMORY
"""
        with open(self.input_file, "w") as f:
            f.write(program)

        assembler = Assembler()
        assembler.assemble(self.input_file, self.binary_file, self.log_file)

        interpreter = Interpreter()
        interpreter.execute(self.binary_file, self.output_file, (0, 10))

        with open(self.output_file, "r") as f:
            result = f.readlines()

        self.assertEqual(result[1].strip(), "0,100")

if __name__ == "__main__":
    unittest.main()
