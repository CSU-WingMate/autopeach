import sys
import os
import subprocess

from debug import *

# 静态语法检查(万里)

# 动态语法检查
def dynamic_grammar_check(pit_file):
    doing("dynamic grammar checking...")

    with open("test_log.txt", "w") as f:
        result = subprocess.run(["./peach", "./pits/coap.xml"], stderr=subprocess.PIPE)
        res = str(result.stderr)[2: -1].replace('"', '\\"')

        lines = res.split("\\n")
        f.write(lines[0] + "\n")
        for line in lines[1:]:
            f.write(line + "\n")

    



    if os.path.exists("test_log.txt"):
        os.remove("test_log.txt")