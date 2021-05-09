import os.path

def makeDirPath(path):
    try:
        os.makedirs(path)
    except: 
        pass

def safeOpen(path, mode):
    ''' Open "path" for writing, creating any parent directories as needed.
    '''
    makeDirPath(os.path.dirname(path))
    return open(path, mode, encoding='utf=8')

def read(path):
    file = safeOpen(path, 'r')
    data = None
    try:
        data = file.read()
    finally:
        file.close()
    return data

def append(path, content):
    file = safeOpen(path, 'a')
    try:
        file.write(content)
    finally:
        file.close()

def write(path, content):
    file = safeOpen(path, 'w')
    try:
        file.write(content)
    finally:
        file.close()