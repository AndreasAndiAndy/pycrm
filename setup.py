from cx_Freeze import setup, Executable
  
#python setup.py build  
  
setup(name = "builder" ,
      version = "0.1" ,
      description = "" ,
      executables = [Executable("__init__.py",base = "Win32GUI")])