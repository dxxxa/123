# [How to Assembly, Disassembly and Emulate Machine Code using Python](https://www.thepythoncode.com/article/arm-x86-64-assembly-disassembly-and-emulation-in-python)
To run this:
- `pip3 install -r requirements.txt`
##
# [[] / []]()
Процессоры выполняют ассемблерный код, который является низкоуровневым языком программирования, который непосредственно использует регистры и память внутри собственного исполняемого файла. Код сборки хранится в собранном виде, в виде двоичных данных, существуют руководства по процессору, которые определяют, как каждая инструкция может быть закодирована в байты данных.

Дизассемблирование — это обратный процесс сборки, байты данных анализируются и переводятся в инструкции сборки (которые более читаемы для пользователей).

Различные архитектуры процессоров могут иметь разные наборы инструкций, и один процессор может выполнять только инструкции сборки в своем собственном наборе инструкций, чтобы запустить код, предназначенный для разных архитектур, нам нужно использовать эмулятор, который представляет собой программу, которая преобразует код для неподдерживаемой архитектуры в код, который может работать в хост-системе.

Существует множество сценариев, в которых сборка, дизассемблирование или эмуляция кода для разных архитектур могут быть полезны, одним из основных интересов является обучение (большинство университетов преподают сборку MIPS) для запуска и тестирования программ, написанных для разных устройств, таких как маршрутизаторы (fuzzing и т. Д.), И для обратного проектирования.

В этом уроке мы будем собирать, дизассемблировать и эмулировать ассемблерный код, написанный для ARM с использованием движка Keystone, движка Capstone и движка Unicorn, которые являются фреймворками, которые предлагают удобные привязки Python для манипулирования кодом сборки, они поддерживают различные архитектуры (x86, ARM, MIPS, SPARC и т. Д.), И они имеют встроенную поддержку основных операционных систем (включая Linux, Windows и MacOS).

Во-первых, давайте установим эти три фреймворка:

pip3 install keystone-engine capstone unicorn
Для демонстрации этого учебника мы возьмем факториальную функцию, реализованную в сборке ARM, соберем код и эмулируем его.

Мы также разберем функцию x86 (чтобы показать, как можно легко обрабатывать несколько архитектур).

Сборка ARM
Мы начинаем с импорта того, что нам понадобится для сборки ARM:

# We need to emulate ARM
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UcError
# for accessing the R0 and R1 registers
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1
# We need to assemble ARM code
from keystone import Ks, KS_ARCH_ARM, KS_MODE_ARM, KsError
Давайте напишем наш ассемблерный код ARM, который вычисляет factorial(r0), где r0 — входной регистр:

ARM_CODE = """
// n is r0, we will pass it from python, ans is r1
mov r1, 1       	// ans = 1
loop:
cmp r0, 0       	// while n >= 0:
mulgt r1, r1, r0	//   ans *= n
subgt r0, r0, 1 	//   n = n - 1
bgt loop        	// 
                	// answer is in r1
"""
Соберем приведенный выше ассемблерный код (преобразуем его в байт-код):

print("Assembling the ARM code")
try:
    # initialize the keystone object with the ARM architecture
    ks = Ks(KS_ARCH_ARM, KS_MODE_ARM)
    # Assemble the ARM code
    ARM_BYTECODE, _ = ks.asm(ARM_CODE)
	# convert the array of integers into bytes
    ARM_BYTECODE = bytes(ARM_BYTECODE)
    print(f"Code successfully assembled (length = {len(ARM_BYTECODE)})")
    print("ARM bytecode:", ARM_BYTECODE)
except KsError as e:
    print("Keystone Error: %s" % e)
    exit(1)
Функция Ks возвращает ассемблер в режиме ARM, метод asm() собирает код и возвращает байты и количество собранных инструкций.

Байт-код теперь может быть записан в области памяти и выполнен процессором ARM (или эмулирован, в нашем случае):

# memory address where emulation starts
ADDRESS = 0x1000000

print("Emulating the ARM code")
try:
    # Initialize emulator in ARM mode
    mu = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    # map 2MB memory for this emulation
    mu.mem_map(ADDRESS, 2 * 1024 * 1024)
    # write machine code to be emulated to memory
    mu.mem_write(ADDRESS, ARM_BYTECODE)
    # Set the r0 register in the code, let's calculate factorial(5)
    mu.reg_write(UC_ARM_REG_R0, 5)
    # emulate code in infinite time and unlimited instructions
    mu.emu_start(ADDRESS, ADDRESS + len(ARM_BYTECODE))
    # now print out the R0 register
    print("Emulation done. Below is the result")
    # retrieve the result from the R1 register
    r1 = mu.reg_read(UC_ARM_REG_R1)
    print(">>  R1 = %u" % r1)
except UcError as e:
    print("Unicorn Error: %s" % e)
В приведенном выше коде инициализируем эмулятор в режиме ARM, сопоставляем 2 МБ памяти по указанному адресу (2*1024*1024 байта), записываем результат нашей сборки в область картографируемой памяти, устанавливаем регистр r0 равным 5, и начинаем эмулировать наш код.

Метод emu_start() принимает необязательный аргумент timeout и необязательное максимальное количество эмулируемых инструкций, что может быть полезно для изолированного кода или ограничения эмуляции определенной частью кода.

После компетов эмуляции читаем содержимое регистра r1, которое должно содержать результат эмуляции, выполнение кода выводит следующие результаты:

Assembling the ARM code
Code successfully assembled (length = 20)
ARM bytecode: b'\x01\x10\xa0\xe3\x00\x00P\xe3\x91\x00\x01\xc0\x01\x00@\xc2\xfb\xff\xff\xca'
Emulating the ARM code
Emulation done. Below is the result
>>  R1 = 120
Получаем ожидаемый результат, факториал 5 равен 120.

Разборка кода x86-64
Теперь, что, если у нас есть машинный код x86, и мы хотим разобрать его, следующий код делает это:

# We need to emulate ARM and x86 code
from unicorn import Uc, UC_ARCH_X86, UC_MODE_64, UcError
# for accessing the RAX and RDI registers
from unicorn.x86_const import UC_X86_REG_RDI, UC_X86_REG_RAX
# We need to disassemble x86_64 code
from capstone import Cs, CS_ARCH_X86, CS_MODE_64, CsError

X86_MACHINE_CODE = b"\x48\x31\xc0\x48\xff\xc0\x48\x85\xff\x0f\x84\x0d\x00\x00\x00\x48\x99\x48\xf7\xe7\x48\xff\xcf\xe9\xea\xff\xff\xff"
# memory address where emulation starts
ADDRESS = 0x1000000
try:
      # Initialize the disassembler in x86 mode
      md = Cs(CS_ARCH_X86, CS_MODE_64)
      # iterate over each instruction and print it
      for instruction in md.disasm(X86_MACHINE_CODE, 0x1000):
            print("0x%x:\t%s\t%s" % (instruction.address, instruction.mnemonic, instruction.op_str))
except CsError as e:
      print("Capstone Error: %s" % e)
Инициализируем дизассемблер в режиме x86-64, дизассемблируем предоставленный машинный код, перебираем инструкции в результате дизассемблирования, и для каждого из них печатаем инструкцию и адрес, где она происходит.

Это дает следующие результаты:

0x1000: xor     rax, rax
0x1003: inc     rax
0x1006: test    rdi, rdi
0x1009: je      0x101c
0x100f: cqo
0x1011: mul     rdi
0x1014: dec     rdi
0x1017: jmp     0x1006
Теперь попробуем эмулировать его с помощью движка Unicorn:

try:
    # Initialize emulator in x86_64 mode
    mu = Uc(UC_ARCH_X86, UC_MODE_64)
    # map 2MB memory for this emulation
    mu.mem_map(ADDRESS, 2 * 1024 * 1024)
    # write machine code to be emulated to memory
    mu.mem_write(ADDRESS, X86_MACHINE_CODE)
    # Set the r0 register in the code to the number of 7
    mu.reg_write(UC_X86_REG_RDI, 7)
    # emulate code in infinite time & unlimited instructions
    mu.emu_start(ADDRESS, ADDRESS + len(X86_MACHINE_CODE))
    # now print out the R0 register
    print("Emulation done. Below is the result")
    rax = mu.reg_read(UC_X86_REG_RAX)
    print(">>> RAX = %u" % rax)
except UcError as e:
    print("Unicorn Error: %s" % e)
Выпуск:

Emulation done. Below is the result
>>> RAX = 5040
Получаем результат 5040, а вводим 7. Если мы посмотрим поближе на этот ассемблерный код x86, мы заметим, что этот код вычисляет факториал регистра rdi (5040 является факториалом 7).

Заключение
Три фреймворка управляют кодом ассемблера единообразно, как вы можете видеть в коде, эмулирующем сборку x86-64, который действительно похож на версию эмуляции ARM. Дизассемблирование и сборка кода также выполняется таким же образом с любой поддерживаемой архитектурой.

Следует иметь в виду, что эмулятор Unicorn эмулирует необработанный машинный код, он не эмулирует вызовы Windows API, а также не анализирует и эмулирует форматы файлов, такие как PE и ELF.

В некоторых сценариях полезно эмулировать всю операционную систему, или программу, которая находится в форме драйвера ядра, или двоичного файла, предназначенного для другой операционной системы, есть отличный фреймворк, построенный поверх Unicorn, который обрабатывает эти ограничения, предлагая при этом привязки Python, который является фреймворком Qiling, он также позволяет двоичное инструментирование (например, подделка системных вызовов, возвращаемых значений, дескрипторов файлов и т. Д.).

После тестирования трех фреймворков Python мы приходим к выводу, что манипулировать ассемблерным кодом с помощью Python очень просто, простота Python в сочетании с удобными и единообразными интерфейсами Python, предлагаемыми Keystone, Capstone и Unicorn, позволяет легко собирать, разбирать и эмулировать код сборки для разных архитектур.