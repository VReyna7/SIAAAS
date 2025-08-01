import os
from file_manager.exceptions import DirNoAllowed, FileError
from typing import Optional
from file_manager.models import File

class FileManager:
    def __init__(self, path="./"):
        self.__rootpath = path
    
    @property
    def rootpath(self):
        return self.__rootpath

    @rootpath.setter
    def rootpath(self,nuevo):
        self.__rootpath = nuevo

    @property
    def fullpath(self):
        return os.path.abspath(self.__rootpath)

    def create_dir(self, nombre, extraPath: Optional[str] = None):
        #<valor_si_verdadero> if <condición> else <valor_si_falso>
        base_path = self.fullpath
        target_path = os.path.abspath(base_path+"/"+nombre) if not extraPath else os.path.abspath(os.path.join(base_path,extraPath,nombre))

        if os.path.commonpath([base_path,target_path]) == base_path:
            os.makedirs(target_path, exist_ok=True)
        else:
            raise DirNoAllowed()
    
    def create_file(self, file : File):
        path_file_ext = os.path.abspath(file.path + "/"+file.name + file.ext)

        if not os.path.exists(path_file_ext):
            raise FileError()

        with open(path_file_ext,'a'):
            pass