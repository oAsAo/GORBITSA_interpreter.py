import fileinput
import re

COMMANDS = {"G" : "x = Memory[adress]",
            "O" : "Memory[adress] = x",
            "R" : "x = listen()",
            "B" : "PC = PC if x else adress",
            "I" : "x = (x+adress)%256",
            "T" : "shout(x)",
            "S" : "x = adress",
            "A" : "x = (x+Memory[adress])%256",
            "r" : "Memory[adress] = listen()",
            "i" : "Memory[adress] = (Memory[adress]+x)%256",
            "t" : "shout(Memory[adress])",
            "s" : "x = x^Memory[adress]"}

# READING CODE FROM A FILE
code = ""
for line in fileinput.input():
    code += line
fileinput.close()

# CHOOSE MODE
def setExecute(matchobj):
    global execute
    execute = True if matchobj[0]=="EXECUTE" else False
    return ""
def chooseIO(matchobj):
    global IOMode
    IOMode = {"DEC":0,"ENC":1,"HEX":2}[matchobj[0][1:]]
    return ""

execute = True # if true execute else compile
IOMode = 0 # 0-DEC, 1-ENC, 2-HEX

code = re.sub(r"^(EXECUTE|COMPILE)", setExecute, code)
code = re.sub(r"^-(DEC|ENC|HEX)", chooseIO, code)

# CLEARING THE CODE A BIT, DELETING COMMENTS ETC.
# REGEX MAGIC
MemLabels = dict()
def updateMemLabels(matchobj):
    item, key = matchobj[0][1:-1].split(":")
    MemLabels[key] = item
    return ""
code = re.sub(r"#[^\n\r]*[\n\r]", "", code) # removing comments
code = re.sub(r"\[\d+:\w+\]", updateMemLabels, code) # reading MemLabels
code = re.sub(r"\[\w+\]",lambda x: MemLabels[x[0][1:-1]],code) # replacing MemLabels(calls)

code_new = ""
last_legal = False

instruction = 0
ids2Adresses = dict()
in_label = in_label2 = False

for i, char in enumerate(code):
    if char == "{":
        in_label = in_label2 = True
        matchobj = re.match(r"\{[-_\w]+:[-_\w]+\}", code[i:])
        if matchobj:
            key = matchobj[0][1:-1].split(":")[1]
            ids2Adresses[key] = str(instruction)
        else:
            in_label = False
    if in_label or in_label2:
        if char == "}":
            in_label2 = False
            if in_label:
                in_label = False
                continue
        if in_label:
            continue
    
    code_new += char
    if in_label2: continue
    matchobj = re.match(r"[GORBITSAgorbitsa][\s\d\{]", code[i:])
    if matchobj: instruction += 1
    
code = code_new
code = code.strip()
code = re.sub(r"\s+", " ", code) # replace any sequence of whitespaces with space

# REPLACING LABELS
for label_id in ids2Adresses.keys():
    code = code.replace("{:"+label_id+"}",ids2Adresses[label_id])

# CODE IS NOW A LIST
code = code.split(" ")

# DEFINE INPUT/OUTPUT
def listen():
    global InputStream
    while not InputStream:
        InputStream += input()
    if IOMode == 0:
        x = int(InputStream)
        InputStream = ""
    elif IOMode == 1:
        x = ord(InputStream[0])%128
        InputStream = InputStream[1:]
    else:
        x = int(InputStream[:2], 16)
        InputStream = InputStream[2:]
    return x
def shout(x):
    if IOMode == 0:
        print(x)
    elif IOMode == 1:
        print(chr(x), end="")
    else:
        print("{:0>2x}".format(x))

# SETTING SHIT UP
Memory = [0 for i in range(256)]
x = PC = 0
code = code + ["" for i in range(256-len(code))]
InputStream = ""

# INTERPRETING CODE
while True:
    if not execute: break # don't run the programm in "COMPILE" mode
    
    line = code[PC]
    
    PC = (PC+1)%256
    if line == "": break # continue/break
    command = line[0]
    if command not in ("R","T"):
        adress = int(line[1:])
        adress = adress%256
    
    try:
        exec(COMMANDS[command])
    except KeyError:
        exec(COMMANDS[command.upper()].replace("adress","Memory[adress]"))

if not execute:
    print(" ".join(code).strip())
    input()
