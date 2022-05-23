import datetime
import threading
import time
from io import TextIOWrapper

from _pynetworktables import NetworkTable, NetworkTableEntry
from _pynetworktables._impl.structs import ConnectionInfo
from networktables import NetworkTables

connected: bool = False
log: TextIOWrapper

def main():
    global connected
    global log
    NetworkTables.initialize()
    table: NetworkTable = NetworkTables.getTable("SmartDashboard")
    xEntry: NetworkTableEntry = table.getEntry("x")
    yEntry: NetworkTableEntry = table.getEntry("y")
    zEntry: NetworkTableEntry = table.getEntry("z")
    i: int = 0
    while True:
        time.sleep(1)
        xEntry.setNumber(i)
        i += 1
        yEntry.setNumber(i)
        i += 1
        zEntry.setNumber(i)
        i += 1

if __name__ == '__main__':
    main()