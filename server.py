import random
import string
import time

from _pynetworktables import NetworkTable, NetworkTableEntry
from networktables import NetworkTables

def main():
    NetworkTables.initialize()
    table: NetworkTable = NetworkTables.getTable("SmartDashboard")
    booleanEntry: NetworkTableEntry = table.getEntry("b")
    doubleEntry: NetworkTableEntry = table.getEntry("d")
    stringEntry: NetworkTableEntry = table.getEntry("s")
    rawEntry: NetworkTableEntry = table.getEntry("r")
    booleanArrayEntry: NetworkTableEntry = table.getEntry("b[]")
    doubleArrayEntry: NetworkTableEntry = table.getEntry("d[]")
    stringArrayEntry: NetworkTableEntry = table.getEntry("s[]")
    while True:
        time.sleep(1)
        booleanEntry.setBoolean(not booleanEntry.getBoolean(True))
        doubleEntry.setDouble(doubleEntry.getDouble(0) + 1)
        stringEntry.setString(str(int(stringEntry.setString("0")) + 1))
        rawEntry.setRaw(random.randbytes(32))

        bArr = booleanArrayEntry.getRaw([])
        bArr.append(False if random.random() < 0.5 else True)
        booleanArrayEntry.setBooleanArray(bArr)

        dArr = doubleArrayEntry.getRaw([])
        dArr.append(random.randint(0, 2^31-1))
        doubleArrayEntry.setDoubleArray(dArr)

        sArr = stringArrayEntry.getRaw([])
        sArr.append(''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(64)))
        stringArrayEntry.setStringArray(sArr)

if __name__ == '__main__':
    main()