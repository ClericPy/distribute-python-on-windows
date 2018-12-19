# distribute-python-on-windows v0.0.1
Telling how to distribute python app on win32 platform.


## Install

> pip install distwin -U

## Usage

> python3 -m distwin -h

### for example:

```powershell
> python3 -m distwin -b 64 -e app:main -p for_import,for_import_package bottle
    INFO    2018-12-20 01:59:22: [find] shiv.exe at 'D:\Python3\scripts\shiv.exe'
    DEBUG   2018-12-20 01:59:23: [find] the latest python-64-bit release .
    DEBUG   2018-12-20 01:59:23: [downloading] python from https://www.python.org/ftp/python/3.7.1/python-3.7.1-embed-amd64.zip.
    DEBUG   2018-12-20 01:59:26: download python zip file (6879900) success in 2 seconds.
    DEBUG   2018-12-20 01:59:26: unzip python file to dist\python-3.7.1-embed-amd64 success
    DEBUG   2018-12-20 01:59:26: refreshing site-packages folder: site-packages.
    DEBUG   2018-12-20 01:59:26: copy ['app', 'for_import', 'for_import_package'] into site-packages
    DEBUG   2018-12-20 01:59:26: copy app.py
    DEBUG   2018-12-20 01:59:26: copy for_import.py
    DEBUG   2018-12-20 01:59:26: copy for_import_package
    Collecting bottle
    Using cached https://files.pythonhosted.org/packages/47/f1/666d2522c8eda26488315d7ee8882d848710b23d408ed4ced35d750d6e20/bottle-0.12.16-py3-none-any.whl
    Installing collected packages: bottle
    Successfully installed bottle-0.12.16
    DEBUG   2018-12-20 01:59:28: removing folder: site-packages
    INFO    2018-12-20 01:59:28: dist success, cd into `dist` folder and run the file `run.bat`.
> cd dist
> run.bat

    1/5 success pip install bottle, version:  0.12.16
    2/5 using python located from: E:\github\distribute-python-on-windows\example\dist\python-3.7.1-embed-amd64\python.exe
    3/5 test import package ok.
    4/5 test finished.
    5/5 press enter to continue...

```

## TODO

1. support `-i` mode