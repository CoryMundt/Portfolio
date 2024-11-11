import subprocess
import sys
from pathlib import Path
from PGfunctions import readConfig, writeConfig
venv_python = Path(sys.executable)
config = readConfig()
try:
    if config['runs'] == -1:
        config['runs'] = 0
        writeConfig()
        subprocess.run([venv_python, "CreateNewCrypto.py"])
        subprocess.run([venv_python, "BackupDatabase.py"])
        subprocess.run([venv_python, "BuildDataTables.py"])
        subprocess.run([venv_python, "DeleteTables.py"])
    else:
        subprocess.run([venv_python, "UpdateTables.py"])
        subprocess.run([venv_python, "CreateNewCrypto.py"])
        subprocess.run([venv_python, "BuildDataTables.py"])
        subprocess.run([venv_python, "DeleteTables.py"])
        subprocess.run([venv_python, "DeleteCrypto.py"])
        subprocess.run([venv_python, "BackupDatabase.py"])
except:
    print("Something went wrong, sorry about that...")
    subprocess.run([venv_python, "RestoreFromBackup.py"])