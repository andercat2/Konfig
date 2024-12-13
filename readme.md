# Учебная виртуальная машина (УВМ)

Этот проект реализует **ассемблер** и **интерпретатор** для учебной виртуальной машины (УВМ). Программа позволяет:
- Ассемблировать текстовые команды УВМ в бинарный формат.
- Выполнять бинарные команды, используя интерпретатор.
- Сохранять результаты выполнения в CSV-файл.

---

## Состав проекта

1. **`main.py`**: основной скрипт для ассемблера и интерпретатора.
2. **Файл команд УВМ** (например, `test.asm`): текстовый файл с командами для ассемблера.
3. **Бинарный файл** (например, `binary.bin`): файл, содержащий скомпилированные команды УВМ.
4. **Файл лога** (например, `log.csv`): файл, содержащий ассемблированные инструкции для отладки.
5. **Файл результатов** (например, `output.csv`): файл, содержащий значения памяти после выполнения.
6. **`uvm_tests.py`**: модуль с тестами для проверки работы ассемблера и интерпретатора.

---

## Команды УВМ

| Команда         | Код   | Описание                                                                 |
|-----------------|-------|-------------------------------------------------------------------------|
| `LOAD_CONST`    | `16`  | Загружает константу в стек.                                             |
| `READ_MEMORY`   | `25`  | Читает значение из памяти с заданным смещением и помещает его в стек.   |
| `WRITE_MEMORY`  | `99`  | Записывает значение из стека в память.                                 |
| `BIN_OP_MAX`    | `30`  | Вычисляет максимум двух значений в стеке.                              |

---

## Формат ввода

Пример содержимого файла `test.asm`:
```asm
LOAD_CONST 10      # Загружаем число 10
LOAD_CONST 20      # Загружаем число 20
BIN_OP_MAX 0       # Вычисляем max(10, 20)
LOAD_CONST 0       # Указываем адрес памяти для записи
WRITE_MEMORY       # Сохраняем результат в памяти
```

---

## Использование

1. **Ассемблирование**:
   ```bash
   python main.py <input_file> <binary_file> <log_file> <output_file>
   ```
   Например:
   ```bash
   python main.py test.asm binary.bin log.csv output.csv
   ```

2. **Результаты выполнения**:
   После выполнения команды результаты будут записаны в файл `output.csv` в формате:
   ```csv
   Address,Value
   0,20
   1,0
   2,0
   ...
   ```

---

## Тестирование

### Покрытие тестов

Тесты покрывают основные операции УВМ и проверяют корректность выполнения команд. Пример запуска тестов:
```bash
python -m unittest uvm_tests.py
```
Вывод успешного выполнения тестов:
```
Executing opcode: 16, PC: 0
Stack state: []
Executing opcode: 16, PC: 5
Stack state: [10]
Executing opcode: 30, PC: 10
Stack state: [10, 20]
Computed max(20, 10) = 20
Executing opcode: 16, PC: 13
Stack state: [20]
Executing opcode: 99, PC: 18
Stack state: [20, 0]
Writing value 20 to memory address 0
Memory state (first 10): [20, 0, 0, 0, 0, 0, 0, 0, 0, 0]
.
Executing opcode: 16, PC: 0
Stack state: []
Executing opcode: 16, PC: 5
Stack state: [100]
Executing opcode: 99, PC: 10
Stack state: [100, 0]
Writing value 100 to memory address 0
Memory state (first 10): [100, 0, 0, 0, 0, 0, 0, 0, 0, 0]
Executing opcode: 16, PC: 11
Stack state: []
Executing opcode: 25, PC: 16
Stack state: [0]
Executing opcode: 16, PC: 19
Stack state: [100]
Executing opcode: 99, PC: 24
Stack state: [100, 0]
Writing value 100 to memory address 0
Memory state (first 10): [100, 0, 0, 0, 0, 0, 0, 0, 0, 0]
.
Executing opcode: 16, PC: 0
Stack state: []
Executing opcode: 16, PC: 5
Stack state: [15]
Executing opcode: 30, PC: 10
Stack state: [15, 25]
Computed max(25, 15) = 25
Executing opcode: 16, PC: 13
Stack state: [25]
Executing opcode: 99, PC: 18
Stack state: [25, 0]
Writing value 25 to memory address 0
Memory state (first 10): [25, 0, 0, 0, 0, 0, 0, 0, 0, 0]
Executing opcode: 16, PC: 19
Stack state: []
Executing opcode: 16, PC: 24
Stack state: [30]
Executing opcode: 30, PC: 29
Stack state: [30, 10]
Computed max(10, 30) = 30
Executing opcode: 16, PC: 32
Stack state: [30]
Executing opcode: 99, PC: 37
Stack state: [30, 1]
Writing value 30 to memory address 1
Memory state (first 10): [25, 30, 0, 0, 0, 0, 0, 0, 0, 0]
Executing opcode: 16, PC: 38
Stack state: []
Executing opcode: 16, PC: 43
Stack state: [50]
Executing opcode: 30, PC: 48
Stack state: [50, 40]
Computed max(40, 50) = 50
Executing opcode: 16, PC: 51
Stack state: [50]
Executing opcode: 99, PC: 56
Stack state: [50, 2]
Writing value 50 to memory address 2
Memory state (first 10): [25, 30, 50, 0, 0, 0, 0, 0, 0, 0]
.
----------------------------------------------------------------------
Ran 3 tests in 0.016s

OK
```

### Пример 1: Вычисление max

Входной файл:
```asm
LOAD_CONST 15
LOAD_CONST 25
BIN_OP_MAX 0
LOAD_CONST 0
WRITE_MEMORY
```

Ожидаемый результат в памяти:
```csv
Address,Value
0,25
1,0
2,0
...
```

---

## Ошибки и их решение

1. **Пустые строки или отсутствующие значения**:
   - **Ошибка**: `ValueError: LOAD_CONST requires a constant value.`
   - **Решение**: Проверьте, чтобы каждая команда имела необходимые параметры.

2. **Перепутанные значения в стеке**:
   - **Ошибка**: Неправильный результат команды `BIN_OP_MAX`.
   - **Решение**: Исправили логику команды для работы с двумя значениями в стеке.

3. **Адреса вне памяти**:
   - **Ошибка**: `IndexError: Invalid memory address.`
   - **Решение**: Убедитесь, что адрес записи находится в пределах выделенной памяти.

---

## Контакты

Если у вас есть вопросы или предложения, создайте issue в репозитории или свяжитесь со мной напрямую. Удачного кодинга!
