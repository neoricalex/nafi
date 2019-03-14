#!/usr/bin/python
from subprocess import Popen
import sys

arquivo = sys.argv[1]
while True:
    print("\nRodando... " + arquivo)
    p = Popen("python " + arquivo, shell=True)
    p.wait()