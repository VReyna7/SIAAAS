from file_manager.exceptions import EmptyException, DirNoAllowed, InvalidEventTypeError, FileLogError, FileError
from file_manager.models import Event, ErrorEvent, OperationEvent
from file_manager.logs_register import LogRegister
from file_manager.file_manager import FileManager
from file_manager.models import File
import datetime
import traceback
import os

class CLIManager:
    def __init__(self):
        pass

    def menu_cli(self):
        print('Porfavor ingresar la opción de la operación a realizar')
        print('1-Crear Carpeta')
        print('2-Crear Archivo')
        print('3-Ver carpetas')
        print('4-Ver archivos')
        print('5-Cambiar root Path')
        print('6-Salir')

    def input_menu(self):    
        log_manager = LogRegister()
        try:
            datos = input()
            if not datos:
             raise EmptyException()
            
            return datos
        except TypeError as x:
            error_event = ErrorEvent(datetime.datetime.now(),'Tipo erroneo', traceback.format_exc(), 'Type error' )
            log_manager.register_log(error_event)
            print(x)
        except Exception:
            error_event = ErrorEvent(datetime.datetime.now(),'Error inesperado', traceback.format_exc(), 'Error General' )
            log_manager.register_log(error_event)
    
    def selectionMenu(self, dato):
        log_manager = LogRegister()
        if dato == '1':
            try:
                new_dir = FileManager()
                print('Ingrese el nombre de la carpeta que quiere agregar | ', end='')
                print(' Sera guardado en el path', new_dir.fullpath)
                print('Si quiere guardarlo como carpeta hija escribalo de la siguiente forma Carpeta_padre/Carpeta_nueva')
                nombre = input()
                partes_path = nombre.split('/')
                if len(partes_path) == 2:
                    extrapath, nombre = partes_path
                else:
                    extrapath = ''
                if not extrapath:
                    new_dir.create_dir(nombre)
                    print(f"Directorio creado, {new_dir.fullpath+"/"+nombre}")
                    operation_event = OperationEvent(datetime.datetime.now(),'Creación de directorio', new_dir.fullpath+"/"+nombre, "Creación")
                    input('Presione enter para continuar')
                    log_manager.safe_log(operation_event)
                else:
                    new_dir.create_dir(nombre,extrapath)
                    print(f"Directorio creado, {new_dir.fullpath+"/"+extrapath+"/"+nombre}")
                    operation_event = OperationEvent(datetime.datetime.now(),'Creación de directorio', new_dir.fullpath+"/"+extrapath+"/"+nombre, "Creación")
                    input('Presione enter para continuar')
                    log_manager.safe_log(operation_event)
            except DirNoAllowed:
                error_event = ErrorEvent(datetime.datetime.now(),'Error al crear directorio', traceback.format_exc(), 'DIR ERROR' )
                log_manager.register_log(error_event)
            except Exception:
                print('Ocurrio un error inexperado')
                error_event = ErrorEvent(datetime.datetime.now(),'Error inesperado', traceback.format_exc(), 'Error General' )
                log_manager.register_log(error_event)
            finally:
                return True
        elif dato == '2':
            try:
                file_manager = FileManager()
                print('Ingrese el nombre del archivo a crear')
                nombre_file = input().strip()
                print('Ingrese la extensión sin . (Ejemplo: txt, json)')
                ext_file = input().lstrip('.')
                print(f'Actualmente se guardara en {file_manager.fullpath}, Si desea guardarlo en otra carpeta agregue el directorio')
                print('\nEjemplop ( dir/casa ) si quiere agregar en carpetas anidadas o (dir) si es solo una carpeta.')
                dir_file = input()
                if dir_file:
                    try:
                        complete_path = os.path.abspath(os.path.join(file_manager.fullpath,dir_file))
                        file = File(nombre_file,ext_file,complete_path,0,datetime.datetime.now())
                        file_manager.create_file(file)
                        operation_event = OperationEvent(datetime.datetime.now(),'Creación de archivo', complete_path+"/"+file.name+"."+file.ext, "Creación")
                        log_manager.safe_log(error_event)
                        print('Archivo creado en ', complete_path)
                        input('presione enter para continuar')
                    except (FileError,OSError):
                        error_event = ErrorEvent(datetime.datetime.now(),'Error al crear archivo', traceback.format_exc(), 'File Error' )
                        log_manager.register_log(error_event)
                    except Exception:
                        error_event = ErrorEvent(datetime.datetime.now(),'Error inesperado al crear el archivo', traceback.format_exc(), 'File Error' )
                        log_manager.register_log(error_event)
                else:
                    file = File(nombre_file,ext_file,file_manager.fullpath,0,datetime.datetime.now())
                    try:
                        file_manager.create_file(file)
                        operation_event = OperationEvent(datetime.datetime.now(),'Creación de archivo', file_manager.fullpath+"/"+file.name+"."+file.ext, "Creación")
                        log_manager.safe_log(operation_event)
                        print('Archivo creado en ', complete_path)
                        input('presione enter para continuar')
                    except (FileError,OSError):
                        error_event = ErrorEvent(datetime.datetime.now(),'Error al crear archivo', traceback.format_exc(), 'File Error' )
                        log_manager.register_log(error_event)
                    except Exception:
                        error_event = ErrorEvent(datetime.datetime.now(),'Error inesperado al crear el archivo', traceback.format_exc(), 'File Error' )
                        log_manager.register_log(error_event)
            except Exception:
                error_event = ErrorEvent(datetime.datetime.now(),'Error inesperado al crear el archivo', traceback.format_exc(), 'File Error' )
                log_manager.register_log(error_event)
            finally:
                return True
        elif dato == '6':
            return False
