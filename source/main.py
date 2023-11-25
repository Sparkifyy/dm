import os
from pathlib import Path

class dm:

  data = {}

  def w(self, k, v):
    self.data[k] = v

  def r(self, k):
    back = self.data.get(k)
    return back

  def d(self, k):
    del self.data[k]

dm = dm()

h = """
write - Writes an entry to data
read -  Reads from an entry
list - Lists all entries
del - Deletes an entry
backup - Backups current data
load - Loads current backup
erase - Erases current data
search - Searches for an key with the specified value
info - Shows key info
"""

def s():
  print(" ")

try:
  with open('data.sparkdm', 'r') as filedb:
      for line in filedb:
          key, value = line.strip().split(": ")
          if key not in dm.data:
              dm.w(key, value)
except FileNotFoundError:
  with open('data.sparkdm', 'w') as filedb:
      filedb.write("made: true")
except Exception as e:
  print(f"An error occurred: {e}")

while True:
  with open('data.sparkdm', 'w') as filedb:
    for key in dm.data:
        value = dm.r(key)
        filedb.write(f"{key}: {value}\n")
  ask = input("Command > ")
  if ask == "write":
    ask = input("Key name > ")
    ask2 = input("Key value > ")
    dm.w(ask, ask2)
    print("Succesfully written to database!")
    s()
  elif ask == "read":
    ask = input("Key name > ")
    try:
      res = dm.r(ask)
      print("Value: " + res)
    except:
      print("Key not found!")
    s()
  elif ask == "list":
    for line in dm.data:
      print(line + ": " + dm.r(line))
    s()
  elif ask == "del":
    ask = input("Key name > ")
    try:
      dm.d(ask)
      print("Succesfully deleted key!")
    except:
      print("Invalid key!")
    s()
  elif ask == "backup":
    with open('backupdata.sparkdm', 'w') as filedb:
      for key in dm.data:
          value = dm.r(key)
          filedb.write(f"{key}: {value}\n")
    print("Created backup! use the 'load' command to load the backup!")
    s()
  elif ask == "load":
    try:
      with open('backupdata.sparkdm', 'r') as filedb:
        for line in filedb:
          key, value = line.strip().split(": ")
          if key not in dm.data:
            dm.w(key, value)
      os.remove('backupdata.sparkdm')
      print("Succesfully loaded backup! The backup was deleted, make sure to make a new one")
    except:
      print("No backup found!")
    s()
  elif ask == "erase":
    backup = Path("backupdata.sparkdm")
    if backup.exists():
      dm.data = {}
      os.remove("data.sparkdm")
      print("Succes!")
    else:
      print("Are you sure? no backup is found?")
      ask = input("Continue? (y/n) > ")
      if ask == "y":
        os.remove("data.sparkdm")
      else:
        print("Aborted!")
    s()
  elif ask == "help":
    print("List of commands:")
    print(h)
  elif ask == "search":
    value_to_search = input("Enter the value to search for: ")
    found_keys = [key for key, value in dm.data.items() if value == value_to_search]
    if found_keys:
      print(f"Keys with the specified value: {', '.join(found_keys)}")
    else:
      print("No keys found with the specified value.")
    s()
  elif ask == "dupe":
    key = input("Key name > ")
    val = dm.r(key)
    dm.w(key + "_c", val)
    s()
  elif ask == "info":
    key = input("Key name > ")
    if key in dm.data:
      if len(key) >= 2 and key[-2:] == '_c':
        print(f"Key {key} is a copy.")
        val = dm.r(key)
        print(f"Value of the key is {val}")
      else:
        print("Key isn't a copy.")
        val = dm.r(key)
        print(f"Value of the key is {val}")
    else:
      print("Key not found!")
    s()
  else:
    print("Unknown command! Run 'help' for a list of commands!")
