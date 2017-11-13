# -*- encoding: utf-8 -*-
#!/Library/Frameworks/Python.framework/Versions/3.4/bin/python3
try:
    # IMPORT MODULS
    # default moduls
    import logging
    import os
    import sys
    # custom moduls
    myfolder = os.path.dirname(os.path.abspath(__file__))
except Exception as e:
    print("IMPORT EXCEPTION!!! " + str(__name__) + "\n" + str(e))

class LogHandler():
    __instance = None
    def __new__(cls, title="title", logpath="logfile.log", log_limit_Mb=300):
        cls.logpath = logpath
        cls.log_limit_Mb = log_limit_Mb                                          # size of file, in bytes
        if cls.__instance == None:
            cls.__instance = object.__new__(cls)
            cls.logger = logging.getLogger(title)
            cls.logger.setLevel(logging.DEBUG)
            cls.fh = logging.FileHandler(cls.logpath)
            cls.fh.setLevel(logging.DEBUG)
            cls.ch = logging.StreamHandler()
            cls.ch.setLevel(logging.ERROR)
            cls.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            cls.ch.setFormatter(cls.formatter)
            cls.fh.setFormatter(cls.formatter)
            cls.logger.addHandler(cls.ch)
            cls.logger.addHandler(cls.fh)
        return cls.__instance

if "Loggerlib" in __name__:
    log_target = os.path.dirname(myfolder)
    CalLog = LogHandler(title="CalcualteManager", logpath=str(log_target) + "/systemCache/cal.log")
    GuiLog = LogHandler(title="GUIManager", logpath=str(log_target) + "/systemCache/gui.log")
    DataLog = LogHandler(title="DataManager", logpath=str(log_target) + "/systemCache/data.log")
    RuntimeLog = LogHandler(title="Runtimelib", logpath=str(log_target) + "/systemCache/runtime.log")

if __name__ == "__main__":
    loghandler = LogHandler()
    loghandler.logger.debug('debug message')
    loghandler.logger.info('info message')
    loghandler.logger.warn('warn message')
    loghandler.logger.error('error message')
    loghandler.logger.critical('critical message')
