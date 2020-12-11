#Course Number:		CIS4362
#Course Name:		Cryptology
#Assignment Name:	Multi Cipher
#My Name:			Stephen Wehlburg
#Date:				December 10th 2020
import curses
from curses import wrapper
from curses.textpad import Textbox, rectangle
from enum import Enum
from ctypes import *
from timeit import timeit
import os.path,subprocess
from subprocess import STDOUT,PIPE
import time


#States for state machine
class options(Enum):
    BASE = 0
    READ_FILE = 1
    READ_INPUT = 2
    APPLY_PYTHON = 3
    APPLY_C = 4
    APPLY_JAVA = 5
    CHANGE_R = 12
    CHANGE_KEY1 = 10
    CHANGE_KEY2 = 11
    CHANGE_BENCH = 6
    BENCHMARK = 7
    QUIT = 8
    INVALID = 9


#Helper function to center text
def centeredText(background, num_cols, row, text):
    start_posit = int(num_cols/2) - int(len(text) / 2)
    background.addstr(row, start_posit, text)


#The basic menu
def base_menu(background, text, r, key1, key2, bench, status):
    rectangle(background, 0, 0, 30, 79)
    centeredText(background, 80, 1, "Welcome to the Multi Cipher App!")
    rectangle(background, 2, 20, 14, 59)
    background.addstr(3, 22, "[F] Read text from a local File")
    background.addstr(4, 22, "[I] Read text from user Input prompt")
    background.addstr(5, 22, "[P] Apply Python ciphers to this text")
    background.addstr(6, 22, "[C] Apply C ciphers to this text")
    background.addstr(7, 22, "[J] Apply Java ciphers to this text")
    background.addstr(8, 22, "[R] Change Rail/Rot")
    background.addstr(9, 22, "[1] Change Key 1")
    background.addstr(10, 22, "[2] Change Key 2")
    background.addstr(11, 22, "[N] Change # of benchmarks")
    background.addstr(12, 22, "[B] Run Benchmarks on all ciphers")
    background.addstr(13, 22, "[Q] Quit the Application")
    rectangle(background, 15, 2, 21, 77)
    background.addstr(16, 4, "TEXT        [" + text + "]")
    background.addstr(17, 4, "RAILS/ROT   [" + str(r) + "]")
    background.addstr(18, 4, "KEY 2       [" + key1 + "]")
    background.addstr(19, 4, "KEY 1       [" + key2 + "]")
    background.addstr(20, 4, "BENCHMARKS  [" + str(bench) + "]")
    background.addstr(31, 1, 'Status: ' + status)


#When info needs to be prompted
def prompt_menu(background, prompt, prompt_input):
    rectangle(background, 22, 1, 27, 78)
    centeredText(background, 80, 23, prompt)
    rectangle(background, 24, 6, 26, 73)
    background.addstr(25, 7, prompt_input)


#So the code doesn't just stall
def pre_benchmark(background):
    rectangle(background, 22, 1, 29, 78)
    centeredText(background, 80, 23, "Running benchmarks.... ")


#Big menu to show the benchmarks
def benchmark_menu(background,
                   p_rail_timer, p_caesar_timer, p_trans_timer, p_four_timer,
                   c_rail_timer, c_caesar_timer, c_trans_timer, c_four_timer,
                   j_rail_timer, j_caesar_timer, j_trans_timer, j_four_timer):
    rectangle(background, 22, 1, 29, 78)
    centeredText(background, 80, 23, "Results from Benchmark")
    centeredText(background, 80, 24, "--------------------------------------------------------------------------")
    centeredText(background, 80, 25, "             Rail-Fence       Caesar       Transposition       Four-Square")

    p_msg = "Python     {rftime:0>7.3f}s         {ctime:0>7.3f}s     {ttime:0>7.3f}s            {ftime:0>7.3f}s  "
    p_msg = p_msg.format(rftime=p_rail_timer, ctime=p_caesar_timer, ttime=p_trans_timer, ftime=p_four_timer)
    centeredText(background, 80, 26, p_msg)

    c_msg = "C-Lang     {rftime:0>7.3f}s         {ctime:0>7.3f}s     {ttime:0>7.3f}s            {ftime:0>7.3f}s  "
    c_msg = c_msg.format(rftime=c_rail_timer, ctime=c_caesar_timer, ttime=c_trans_timer, ftime=c_four_timer)
    centeredText(background, 80, 27, c_msg)

    j_msg = "  Java     {rftime:0>7.3f}s         {ctime:0>7.3f}s     {ttime:0>7.3f}s            {ftime:0>7.3f}s  "
    j_msg = j_msg.format(rftime=j_rail_timer, ctime=j_caesar_timer, ttime=j_trans_timer, ftime=j_four_timer)
    centeredText(background, 80, 28, j_msg)


#The main program
def run_gui(background):
    text = "HELLOWORLDFIGHTME"
    r = 3
    key1 = "PANTS"
    key2 = "HECK"
    bench = 100

    status = "Application started successfully."

    prompt = str()
    prompt_input = str()
    prompt_status = False
    prompt_state = options.BASE

    library = load_cipher_lib("./libciphers.so")
    compile_java('ciphers.java')

    c_timer = 0
    p_timer = 0

    while True:
        background.clear()
        win = curses.newwin(0, 0)
        base_menu(background, text, r, key1, key2, bench, status)
        if prompt_status:
            prompt_menu(background, prompt, prompt_input)
        elif prompt_state == options.BENCHMARK:
            pre_benchmark(background)

        win.refresh()

        if prompt_state == options.BENCHMARK:
            curses.ungetch('a')
            char_in = background.getch()

            '''
            Python
            '''

            textP = text
            p_rail_timer = timeit(lambda: rail_fence(textP, r), number=bench)

            textP = text
            p_caesar_timer = timeit(lambda: caesar(textP, r), number=bench)

            textP = text
            p_trans_timer = timeit(lambda: trans(textP, key1), number=bench)

            textP = text
            p_four_timer = timeit(lambda: four(textP, key1, key2), number=bench)

            '''
            C
            '''

            textC = text
            buffer = create_string_buffer(len(textC) + 1)
            c_rail_timer = timeit(lambda: library.rail_fence(textC.encode("cp437"),
                                                            buffer, len(textC),
                                                            r),
                                  number=bench)

            textC = text
            buffer = create_string_buffer(len(textC) + 1)
            c_caesar_timer = timeit(lambda: library.caesar(textC.encode("cp437"),
                                                             buffer, len(textC),
                                                             r),
                                  number=bench)

            textC = text
            buffer = create_string_buffer(len(textC) + 1)
            c_trans_timer = timeit(lambda: library.trans(textC.encode("cp437"),
                                                        buffer,
                                                        len(textC) + 1,
                                                        key1.encode("cp437"),
                                                        len(key1.encode("cp437"))),
                                  number=bench)

            textC = text
            buffer = create_string_buffer(len(textC) + 1)
            c_four_timer = timeit(lambda: library.four(textC.encode("cp437"),
                                                        buffer,
                                                        len(textC) + 1,
                                                        key1.encode("cp437"),
                                                        len(key1.encode("cp437")),
                                                        key2.encode("cp437"),
                                                        len(key2.encode("cp437"))
                                                        ),
                                   number=bench)

            '''
            Java
            '''

            textJ = text
            j_rail_timer = timeit(lambda: execute_java('ciphers.java', str(bench) + ' 0 ' + textJ + ' ' + str(r)), number=1)

            textJ = text
            j_caesar_timer = timeit(lambda: execute_java('ciphers.java', str(bench) + ' 1 ' + textJ + ' ' + str(r)), number=1)

            textJ = text
            j_trans_timer = timeit(lambda: execute_java('ciphers.java', str(bench) + ' 2 ' + textJ + ' ' + key1), number=1)

            textJ = text
            j_four_timer = timeit(lambda: execute_java('ciphers.java', str(bench) + ' 3 ' + textJ + ' ' + key1 + ' ' + key2), number=1)

            curses.ungetch('a')
            char_in = background.getch()
            background.clear()
            win = curses.newwin(0, 0)
            base_menu(background, text, r, key1, key2, bench, status)
            status = "Benchmark results displayed."
            benchmark_menu(background,
                           p_rail_timer, p_caesar_timer, p_trans_timer, p_four_timer,
                           c_rail_timer, c_caesar_timer, c_trans_timer, c_four_timer,
                           j_rail_timer, j_caesar_timer, j_trans_timer, j_four_timer)
            prompt_state = options.BASE
            win.refresh()


        '''
        The update section
        '''

        char_in = background.getch()
        if prompt_state == options.BASE:
            if char_in == 70 or char_in == 102:
                prompt_state = options.READ_FILE
            elif char_in == 73 or char_in == 105:
                prompt_state = options.READ_INPUT
            elif char_in == 80 or char_in == 112:
                prompt_state = options.APPLY_PYTHON
            elif char_in == 67 or char_in == 99:
                prompt_state = options.APPLY_C
            elif char_in == 74 or char_in == 106:
                prompt_state = options.APPLY_JAVA
            elif char_in == 82 or char_in == 114:
                prompt_state = options.CHANGE_R
            elif char_in == 49:
                prompt_state = options.CHANGE_KEY1
            elif char_in == 50:
                prompt_state = options.CHANGE_KEY2
            elif char_in == 78 or char_in == 110:
                prompt_state = options.CHANGE_BENCH
            elif char_in == 66 or char_in == 98:
                prompt_state = options.BENCHMARK
            elif char_in == 81 or char_in == 113:
                prompt_state = options.QUIT
            else:
                prompt_state = options.INVALID
        if prompt_state == options.READ_FILE:
            if not prompt_status:
                prompt_status = True
                prompt = "Enter file to load below, then press [ENTER]"
                prompt_input = str()
            else:
                if char_in != 10:
                    if char_in == 263:
                        if len(prompt_input) > 0:
                            prompt_input = prompt_input[:-1]
                    elif char_in <= 255 and len(prompt_input) <= 65:
                        prompt_input += str(chr(char_in))

                else:
                    prompt_status = False
                    prompt_state = options.BASE
                    if len(prompt_input) == 0:
                        status = "File load cancelled."
                    else:
                        try:
                            file_object = open(prompt_input.encode("cp437").decode("cp437"), 'r')
                            status = "File contents loaded successfully."
                            text = file_object.readlines()[0]
                            while len(text) > 65:
                                text = text[:-1]
                        except:
                            status = "ERROR: COULD NOT LOAD FILE: " + prompt_input + "."
        elif prompt_state == options.READ_INPUT:
            if not prompt_status:
                prompt_status = True
                prompt = "Enter new text below, then press [ENTER]"
                prompt_input = str()
            else:
                if char_in != 10:
                    if char_in == 263:
                        if len(prompt_input) > 0:
                            prompt_input = prompt_input[:-1]
                    elif char_in <= 255 and len(prompt_input) <= 65:
                        if get_val(chr(char_in)) != -1:
                            prompt_input += str(get_char(get_val(chr(char_in))))

                else:
                    prompt_status = False
                    prompt_state = options.BASE
                    if len(prompt_input) == 0:
                        status = "Cancelled user input of text (empty string)."
                    else:
                        text = prompt_input.strip()
                        status = "New text loaded into memory from user input."
        elif prompt_state == options.APPLY_PYTHON:
            text = four(text, "PANTS", "HECK")
            status = "Applied Python cipher."
            prompt_state = options.BASE
        elif prompt_state == options.APPLY_C:
            buffer = create_string_buffer(len(text) + 1)
            library.four(text.encode("cp437"),
                         buffer,
                         len(text),
                         "PANTS".encode("cp437"),
                         len("PANTS".encode("cp437")),
                         "HECK".encode("cp437"),
                         len("HECK".encode("cp437"))
                         )
            text = buffer.raw.decode("cp437")
            text = text[:-1]
            status = "Applied C cipher."
            prompt_state = options.BASE
        elif prompt_state == options.APPLY_JAVA:
            text = execute_java('ciphers.java', str(1) + ' 3 ' + text + ' PANTS HECK').decode("cp437")
            status = "Applied Java cipher."
            prompt_state = options.BASE
        elif prompt_state == options.CHANGE_R:
            if not prompt_status:
                prompt_status = True
                prompt = "Enter new Rail/Rot number and then press [ENTER]"
                prompt_input = str()
            else:
                if char_in != 10:
                    if char_in == 263:
                        if len(prompt_input) > 0:
                            prompt_input = prompt_input[:-1]
                    elif char_in <= 255 and len(prompt_input) <= 65:
                        prompt_input += str(chr(char_in))

                else:
                    prompt_status = False
                    prompt_state = options.BASE
                    if len(prompt_input) == 0:
                        status = "Cancelled user input of rail/rot (empty string)."
                    else:
                        r = int(prompt_input)
                        status = "New rail/rot number loaded into memory from user input."
        elif prompt_state == options.CHANGE_KEY1:
            if not prompt_status:
                prompt_status = True
                prompt = "Enter new key1 and then press [ENTER]"
                prompt_input = str()
            else:
                if char_in != 10:
                    if char_in == 263:
                        if len(prompt_input) > 0:
                            prompt_input = prompt_input[:-1]
                    elif char_in <= 255 and len(prompt_input) <= 65:
                        if get_val(chr(char_in)) != -1:
                            prompt_input += str(get_char(get_val(chr(char_in))))

                else:
                    prompt_status = False
                    prompt_state = options.BASE
                    if len(prompt_input) == 0:
                        status = "Cancelled user input of key 1 (empty string)."
                    else:
                        key1 = prompt_input
                        status = "New key 1 loaded into memory from user input."
        elif prompt_state == options.CHANGE_KEY2:
            if not prompt_status:
                prompt_status = True
                prompt = "Enter new key2 and then press [ENTER]"
                prompt_input = str()
            else:
                if char_in != 10:
                    if char_in == 263:
                        if len(prompt_input) > 0:
                            prompt_input = prompt_input[:-1]
                    elif char_in <= 255 and len(prompt_input) <= 65:
                        if get_val(chr(char_in)) != -1:
                            prompt_input += str(get_char(get_val(chr(char_in))))

                else:
                    prompt_status = False
                    prompt_state = options.BASE
                    if len(prompt_input) == 0:
                        status = "Cancelled user input of key 2 (empty string)."
                    else:
                        key2 = prompt_input
                        status = "New key 2 number loaded into memory from user input."
        elif prompt_state == options.CHANGE_BENCH:
            if not prompt_status:
                prompt_status = True
                prompt = "Enter new benchmark number and then press [ENTER]"
                prompt_input = str()
            else:
                if char_in != 10:
                    if char_in == 263:
                        if len(prompt_input) > 0:
                            prompt_input = prompt_input[:-1]
                    elif char_in <= 255 and len(prompt_input) <= 65:
                        prompt_input += str(chr(char_in))

                else:
                    prompt_status = False
                    prompt_state = options.BASE
                    if len(prompt_input) == 0:
                        status = "Cancelled user input of bench (empty string)."
                    else:
                        bench = int(prompt_input)
                        status = "New benchmark number loaded into memory from user input."
        elif prompt_state == options.BENCHMARK:
            pass
        elif prompt_state == options.INVALID:
            status = "ERROR: Invalid menu selection!"
            prompt_state = options.BASE
        if prompt_state == options.QUIT:
            break


def rail_fence(msg: str, num_rails: int):
    if num_rails == 1:
        return msg
    else:
        rails = []
        for i in range(0, num_rails):
            rails.append([])

        cur_rail = 0
        down = True

        for i in range( 0, len(msg)):
            rails[cur_rail].append(msg[i])

            if down:
                cur_rail += 1
            else:
                cur_rail -= 1

            if cur_rail == 0:
                down = True
            elif cur_rail == (num_rails - 1):
                down = False

        buffer = ""
        for i in range(0, num_rails):
            for j in range(0, len(rails[i])):
                buffer += rails[i][j]

        return buffer


def caesar(msg: str, rotate: int):
    buffer = ""
    for letter in msg:
        val = get_val(letter)
        if val != -1:
            buffer += get_char((val + rotate) % 25)
        else:
            buffer += letter
    return buffer


def trans(msg: str, key: str):
    cols = []
    vals = []
    for i in key:
        cols.append("")
        vals.append(get_val(i))

    for i in range(0, len(msg)):
        cols[i % len(key)] += msg[i]

    buffer = ""
    for i in range(0, len(key)):
        low_val = 30
        low_index = -1
        for j in range(0, len(key)):
            if vals[j] < low_val:
                low_val = vals[j]
                low_index = j
        buffer += cols[low_index]
        vals[low_index] = 29

    return buffer


def four(msg, key1: str, key2: str):
    index = 0
    grid1set = set()
    grid1 = [list(), list(), list(), list(), list()]
    for i in key1:
        if get_val(i) not in grid1set:
            grid1set.add(get_val(i))
            grid1[int(index/5)].append(get_val(i))
            index += 1
    for i in range(0, 25):
        if i not in grid1set:
            grid1set.add(i)
            grid1[int(index / 5)].append(i)
            index += 1

    index = 0
    grid2set = set()
    grid2 = [list(), list(), list(), list(), list()]
    for i in key2:
        if get_val(i) not in grid2set:
            grid2set.add(get_val(i))
            grid2[int(index / 5)].append(get_val(i))
            index += 1
    for i in range(0, 25):
        if i not in grid2set:
            grid2set.add(i)
            grid2[int(index / 5)].append(i)
            index += 1

    val1 = 0
    val2 = 0
    buffer = ""
    for i in range(0, len(msg) - 1, 2):
        val1 = int(get_val(msg[i])/5)
        val2 = get_val(msg[i+1])%5
        buffer += get_char(grid1[val1][val2])

        val1 = get_val(msg[i]) % 5
        val2 = int(get_val(msg[i + 1]) / 5)
        buffer += get_char(grid2[val1][val2])



    if(len(msg) % 2 == 1):
        buffer += msg[len(msg) - 1]

    return buffer


def compile_java(java_file):
    subprocess.check_call(['javac', java_file])

def execute_java(java_file, stdin):
    java_class,ext = os.path.splitext(java_file)
    cmd = ['java', java_class]
    proc = subprocess.Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
    stdout,stderr = proc.communicate(stdin.encode("cp437"))
    return stdout


def get_val(cha: chr):
    ch = ord(cha)
    if 65 <= ch <= 73:
        return ch - 65
    elif 74 <= ch <= 90:
        return ch - 66
    if 97 <= ch <= 105:
        return ch - 65 - 32
    elif 106 <= ch <= 122:
        return ch - 66 - 32
    else:
        return -1


def get_char(num):
    if 0 <= num <= 7:
        return chr(65 + num)
    elif 8 <= num <= 25:
        return chr(66 + num)
    else:
        return -1


def load_cipher_lib(library_path):
    library = cdll.LoadLibrary(library_path)
    library.rail_fence.restype = None
    library.rail_fence.argtypes = [c_char_p, c_char_p, c_int8, c_int8]
    library.caesar.restype = None
    library.caesar.argtypes = [c_char_p, c_char_p, c_int8, c_int8]
    library.trans.restype = None
    library.trans.argtypes = [c_char_p, c_char_p, c_int8, c_char_p, c_int8]
    library.four.restype = None
    library.four.argtypes = [c_char_p, c_char_p, c_int8, c_char_p, c_int8, c_char_p, c_int8]
    return library


def main():
    wrapper(run_gui)
    print("Thanks for using the XOR-Cipher App; See you next time!")


if __name__ == "__main__":
    main()