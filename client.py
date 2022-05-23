import datetime
import time
from io import TextIOWrapper

from _pynetworktables import NetworkTable
from _pynetworktables._impl.structs import ConnectionInfo
from networktables import NetworkTables

connected: bool = False
log: TextIOWrapper

def onStartup(boolean: bool, connectionInfo: ConnectionInfo):
    global connected
    print(f"Connected to {connectionInfo.remote_ip}:{connectionInfo.remote_port}")
    connected = True

def onChange(source: NetworkTable, key: str, value, isNew: bool):
    global log
    if isNew: log.write(f"CREATE {source.path}/{key} WITH {value} AT {datetime.datetime.now().isoformat()}\n")
    else: log.write(f"UPDATE {source.path}/{key} WITH {value} AT {datetime.datetime.now().isoformat()}\n")

def main(robotNumber: int, tableName: str):
    global connected
    global log
    NetworkTables.initialize(server = f"10.{robotNumber // 100}.{robotNumber % 100}.42")
    NetworkTables.addConnectionListener(onStartup, immediateNotify = True)
    print("Connecting...")
    while not connected:
        time.sleep(1)

    timeStarted: str = datetime.datetime.now().isoformat()
    log = open(f"{timeStarted}.log", "w")
    log.write(f"Time: {timeStarted}\n")
    log.write(f"Team: {robotNumber}\n")
    #for key in NetworkTables.getTable(tableName).getKeys():
        #onChange(NetworkTables.getTable(tableName), key, NetworkTables.getTable(tableName).getValue(key, None), True)
    log.flush()

    NetworkTables.getTable(tableName).addEntryListener(onChange, immediateNotify = True)

    while True:
        time.sleep(0.05)
        log.flush()

if __name__ == '__main__':
    main(0, "SmartDashboard")
    log.close()