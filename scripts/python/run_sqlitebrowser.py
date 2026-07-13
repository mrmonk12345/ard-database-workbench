from config import DATABASE_PATH
import subprocess

SQLITEBROWSER = (
    "/home/ARO.local/collaboration/michalm_collab/"
    "trash/tools/sqlitebrowser/build/sqlitebrowser"
)

def open_sqlitebrowser(db_path):
    subprocess.Popen([SQLITEBROWSER, db_path])

open_sqlitebrowser(DATABASE_PATH)