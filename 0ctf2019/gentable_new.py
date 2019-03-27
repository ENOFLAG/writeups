import subprocess
import hashlib
import datetime
import sys


CHARS = ''.join([chr(i) for i in range(0x20, 0x7F)])

def treehash(teststr, trees):
    counterlist = ""
    for tree in trees:
        counterlist += get_counters(teststr, tree)
    return hashlib.md5(counterlist.encode("ascii")).hexdigest()


def get_counters(teststr, tree):

    with open("flag", "w") as flag:
        flag.write(teststr)
        flag.close()

    sanitize_process = subprocess.Popen("./sanitize", stdin=subprocess.PIPE, stdout=subprocess.PIPE, universal_newlines=True)
    #a = sanitize_process.stdout.readline()
    inputstr = tree + "\n" + "4" + "\n" + "0" + "\n" + "1" + "\n" + "2" + "\n" +"3" + "\n"
    sanitize_process.stdin.write(inputstr)
    sanitize_process.stdin.flush()
    output = sanitize_process.stdout.readline()
    sanitize_process.wait()
    return output

def gettrees():
    trees = []
    for c in CHARS:
        trees.append(c * 27) 
    return trees

def create_table():
    #print(f"target : {target}")
    table = []
    trees = gettrees()
    for i in CHARS:
        string = i + "lag"
        print(string)
        table.append((i,  treehash(string, trees)))

    return table

if __name__ == "__main__":
    table = create_table()
    with open(f"table2/table_new2.table", "w") as tablefile:
        for row in table:
            tablefile.write(str(row) + "\n")
        tablefile.close()
    print(table)