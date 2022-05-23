import datetime
import socket
import time
from io import TextIOWrapper

from _pynetworktables import NetworkTable, NetworkTablesInstance
from _pynetworktables._impl.structs import ConnectionInfo
from networktables import NetworkTables
Type = NetworkTablesInstance.EntryTypes

connected: bool = False
log: TextIOWrapper

def convertEntryType(entryType: Type) -> str:
    match entryType:
        case Type.BOOLEAN:
            return "BOOLEAN"
        case Type.DOUBLE:
            return "DOUBLE"
        case Type.STRING:
            return "STRING"
        case Type.RAW:
            return "RAW"
        case Type.BOOLEAN_ARRAY:
            return "BOOLEAN_ARRAY"
        case Type.DOUBLE_ARRAY:
            return "DOUBLE_ARRAY"
        case Type.STRING_ARRAY:
            return "STRING_ARRAY"

def onStartup(boolean: bool, connectionInfo: ConnectionInfo):
    global connected
    print(f"Connected to {connectionInfo.remote_ip}:{connectionInfo.remote_port}")
    connected = True

def onChange(source: NetworkTable, key: str, value, isNew: bool):
    global log
    entryType: str = convertEntryType(source.getEntry(key).getType())
    if isNew: log.write(f"CREATE {source.path}/{key} WITH {str(value)} AT {datetime.datetime.now().isoformat()} AS {entryType}\n")
    else: log.write(f"UPDATE {source.path}/{key} WITH {str(value)} AT {datetime.datetime.now().isoformat()} AS {entryType}\n")

def main(robotNumber: int, tableName: str, dev: bool):
    global connected
    global log
    ip: str = socket.gethostbyname(socket.gethostname()) if dev else f"10.{robotNumber // 100}.{robotNumber % 100}.2"
    NetworkTables.initialize(server = ip)
    NetworkTables.addConnectionListener(onStartup, immediateNotify = True)
    print("Connecting...")
    while not connected:
        time.sleep(1)

    timeStarted: str = datetime.datetime.now().isoformat()
    log = open(f"{timeStarted}.log", "w")
    log.write(f"TIME {timeStarted}\n")
    log.write(f"TEAM {robotNumber}\n")
    #for key in NetworkTables.getTable(tableName).getKeys():
        #onChange(NetworkTables.getTable(tableName), key, NetworkTables.getTable(tableName).getValue(key, None), True)
    log.flush()

    NetworkTables.getTable(tableName).addEntryListener(onChange, immediateNotify = True)

    while True:
        time.sleep(0.05)
        log.flush()

if __name__ == '__main__':
    main(0, "SmartDashboard", True)
    log.close()