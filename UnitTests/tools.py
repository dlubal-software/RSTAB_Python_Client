def getPathToRunningRSTAB():
    '''
    Find the path to the directory where RSTAB is currently running.
    This is helpful when using server version, because it can't process relative paths.
    '''
    import psutil
    rstab9 = False
    rstab9Server = False
    path = ''

    for p in psutil.process_iter(['name', 'exe']):
        if p.info['name'] == 'RSTAB9.exe':
            idx = p.info['exe'].find('bin')
            path = p.info['exe'][:idx]
        elif p.info['name'] == 'RSTAB9Server.exe':
            idx = p.info['exe'].find('bin')
            path = p.info['exe'][:idx]
        elif p.info['name'] == 'RSTAB9.exe':
            rstab9 = True
        elif p.info['name'] == 'RSTAB9Server.exe':
            rstab9Server = True

    if rstab9 or rstab9Server:
        raise ValueError('Careful! You are running RFEM Python Client on RFEM.')
    if not path:
        raise ValueError('Is it possible that RSTAB is not runnnning?')

    return path