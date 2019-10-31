from bluetooth import *
from PyOBEX.client import Client
import sys


addr = sys.argv[1]
print("Searching for OBEX service on {}".format(addr))

