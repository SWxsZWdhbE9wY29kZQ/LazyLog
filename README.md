# LazyLog
Painless logger (file and terminal) for Python 3.4+

### Usage
```python
from log import Log
logger = Log() # By default the logger will log all message levels to the terminal
logger.Info("Hello World!")
> [12:00:00] INFO: Hello World!
```
we can also name the log instance for nicer formatting:
```python
logger = Log("Main")
...
> [12:00:00] Main:INFO: Hello World!
```
logging to a file is as easy as setting the message level and filepath:
```python
logger = Log("Main", fileLogLevel=Log.Level.VERBOSE, fileLogPath='./test.log')
# test.log
> [2024/06/22 12:00:00] Main:INFO: Hello World!
```
under the hood all of these settings are shared, so we can easily add multiple loggers to a project without repeating the setup:
```python
# app.py
from log import Log
from test import Test
logger = Log("Main", fileLogLevel=Log.Level.VERBOSE, fileLogPath='./test.log')
logger.Info("Hello")
Test()
# test.py
from log import Log
class Test():
  def __init__(self):
    self.logger = Log("Module")
    self.logger.Info("World!")
# test.log
> [2024/06/22 12:00:00] Main:INFO: Hello
> [2024/06/22 12:00:00] Module:INFO: World!
```
