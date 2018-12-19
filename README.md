# distribute-python-on-windows
Telling how to distribute python app on win32 platform.


## Usage

> python3 -m distwin -h

```
> cd example/
> python3 -m distwin -b 64 -e app:main
............
> cd dist/
> run.bat

for example:

$ cd example
$ python3 -m distwin -b 64 -e app:main -p for_import,for_import_package bottle
INFO    2018-12-20 01:51:47: [find] shiv.exe at 'D:\Python3\scripts\shiv.exe'
DEBUG   2018-12-20 01:51:48: [find] the latest python-64-bit release .
DEBUG   2018-12-20 01:51:48: [ignore] file dist\python-3.7.1-embed-amd64\python.exe exists.
DEBUG   2018-12-20 01:51:48: refreshing site-packages folder: site-packages.
DEBUG   2018-12-20 01:51:48: copy ['app', 'for_import', 'for_import_package'] into site-packages
DEBUG   2018-12-20 01:51:48: copy app.py
DEBUG   2018-12-20 01:51:48: copy for_import.py
DEBUG   2018-12-20 01:51:48: copy for_import_package
Looking in indexes: https://pypi.douban.com/simple/
Collecting bottle
  Downloading https://pypi.doubanio.com/packages/47/f1/666d2522c8eda26488315d7ee8882d848710b23d408ed4ced35d750d6e20/bottle-0.12.16-py3-none-any.whl (89kB)
Installing collected packages: bottle
Successfully installed bottle-0.12.16
DEBUG   2018-12-20 01:51:49: remove folder: site-packages
INFO    2018-12-20 01:51:49: dist success, cd into `dist` folder and run the file `run.bat`.
```

## TODO

1. support `-i` mode