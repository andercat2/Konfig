LOAD_CONST 15      # Число 1
LOAD_CONST 25      # Число 2
BIN_OP_MAX 0       # max(15, 25)
LOAD_CONST 0       # Адрес для сохранения результата
WRITE_MEMORY       # Сохранить результат по адресу 0

LOAD_CONST 30      # Число 3
LOAD_CONST 10      # Число 4
BIN_OP_MAX 0       # max(30, 10)
LOAD_CONST 1       # Адрес для сохранения результата
WRITE_MEMORY       # Сохранить результат по адресу 1

LOAD_CONST 50      # Число 5
LOAD_CONST 40      # Число 6
BIN_OP_MAX 0       # max(50, 40)
LOAD_CONST 2       # Адрес для сохранения результата
WRITE_MEMORY       # Сохранить результат по адресу 2
