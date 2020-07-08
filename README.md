# GORBITSA_interpreter.py
GORBITSA is a novelty esoteric programming language created by David Barr (aka javidx9) as a programming challenge for One Lone Coder community.
This repository contains interpreter for "ROM version" of it, which is written in python.

Read about the esolang itself on https://esolangs.org/wiki/GORBITSA

To execute your GORBITSA program run it with the GORBITSA_interpreter.py

Additional syntax supported:
1) (EXECUTE/COMPILE)-(DEC/HEX/ENC) in the beggining of the file
EXECUTE will actually execute the program(default)
COMPILE will output program, striped of all the additional syntax

DEC will set I/O mode to decimal(default)
HEX will set I/O mode to hexadecimal
ENC will set I/O mode to ASCII encoding

Those all are valid:
""
"EXECUTE"
"COMPILE"
"EXECUTE-DEC"
"COMPILE-DEC"
"EXECUTE-HEX"
"COMPILE-HEX"
"EXECUTE-ENC"
"COMPILE-ENC"

2) 1 line comments after "#" character

3) Memory labels(constants)
[memory location here:name here] to define
[name here] to call

4) Instruction labels(as in assembly)
{comment here(must contain at least 1 char):name here} to define
{:name here} to call
