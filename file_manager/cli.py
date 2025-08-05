from file_manager.exceptions import EmptyException, DirNoAllowed, InvalidEventTypeError, FileLogError, FileError
from file_manager.models import Event, ErrorEvent, OperationEvent
from file_manager.logs_register import LogRegister
from file_manager.file_manager import FileManager
from file_manager.models import File
import datetime
import traceback
import os
import time

class CLIManager:
    def __init__(self):
        pass

    def menu_cli(self):
        print('Porfavor ingresar la opción de la operación a realizar')
        print('1-Crear Carpeta')
        print('2-Crear Archivo')
        print('3-Ver carpetas y archivos de un directorio')
        print('4-Cambiar root Path')
        print('5-Salir')

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
        file_manager = FileManager()
        if dato == '1':
            try:
                print('Ingrese el nombre de la carpeta que quiere agregar | ', end='')
                print(' Sera guardado en el path', file_manager.fullpath)
                print('Si quiere guardarlo como carpeta hija escribalo de la siguiente forma Carpeta_padre/Carpeta_nueva')
                nombre = input()
                partes_path = nombre.split('/')
                if len(partes_path) == 2:
                    extrapath, nombre = partes_path
                else:
                    extrapath = ''
                if not extrapath:
                    file_manager.create_dir(nombre)
                    print(f"Directorio creado, {file_manager.fullpath+"/"+nombre}")
                    operation_event = OperationEvent(datetime.datetime.now(),'Creación de directorio', file_manager.fullpath+"/"+nombre, "Creación")
                    input('Presione enter para continuar')
                    log_manager.safe_log(operation_event)
                else:
                    file_manager.create_dir(nombre,extrapath)
                    print(f"Directorio creado, {file_manager.fullpath+"/"+extrapath+"/"+nombre}")
                    operation_event = OperationEvent(datetime.datetime.now(),'Creación de directorio', file_manager.fullpath+"/"+extrapath+"/"+nombre, "Creación")
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
        elif dato == '3':
            try:
                print(f'Si quiere listar los archivos de {file_manager.fullpath} solo presione enter')
                print(f'Por otro lado si quiere ver listar las carpetas de otro directorio más especifico use "nombreCarpeta" o "NombreCarpta/SubCarpeta')
                extrapath = input()
                if not extrapath:
                    listdir = file_manager.list_dir(file_manager.fullpath)
                else:
                    listdir = file_manager.list_dir(os.path.abspath(os.path.join(file_manager.fullpath, extrapath)))
                
                if len(listdir) > 0: 
                    i = 0
                    for dir in listdir:
                        if i % 3 == 0:
                           time.sleep(1) 
                        print(dir)
                        i += 1
                else:
                    print('No se encuentron archivos o carpetas \n')

            except Exception:
                error_event = ErrorEvent(datetime.datetime.now(),'Error inesperado al listar el archivo', traceback.format_exc(), 'List dir Error' )
                log_manager.register_log(error_event)
            finally:
                return True
        elif dato == '4':
            print('Ingrese el nuevo path de forma completa, absoluta')
            new_path = input()
            file_manager.fullpath = new_path
        elif dato == '5':
            return False
