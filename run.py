import os
from subprocess import call, Popen

# Popen("cmd")
# Popen("python setup.py install")

path = os.path.abspath(os.getcwd())
path += "\\adventure\\__main__.py"
print(path)
if __name__ == '__main__':
    call(["Python", path])
