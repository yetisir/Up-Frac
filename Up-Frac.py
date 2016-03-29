#copy modelData modules from UDEC to HOMOGENIZE
import os
import sys
if __name__ == '__main__':
    os.system('cls')
    
    clargs = sys.argv
    if len(clargs) >= 2:
        fileName = clargs[1]

    os.system('python ostrichHomogenize.py' + fileName)
    os.system('python createOstrichInput.py ' + fileName)
