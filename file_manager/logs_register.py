from file_manager.models import Event, ErrorEvent, OperationEvent
from file_manager.exceptions import InvalidEventTypeError, FileLogError
import datetime
import traceback

class LogRegister:
    def __init__ (self, path = './logs.txt'):
        if not isinstance(path, str) or not path:
            raise ValueError("La ruta del log debe ser una cadena no vacía.")
        
        self.__path = path

    def register_log(self, event: Event):
        if not isinstance(event, Event):
            raise InvalidEventTypeError()

        log_string = event.to_log_string()

        try:
            with open(self.__path, 'a', encoding="UTF-8") as file:
                file.write(log_string + '\n')
        except IOError as e:
            raise FileLogError(f"Error en el archivo log, archivo: {self.__path}: {e}")  from e
    
    def safe_log(self, operation_event):
        try:
            self.register_log(operation_event)
        except InvalidEventTypeError:
            error_event = ErrorEvent(datetime.datetime.now(),'Tipo no es un evento', traceback.format_exc(), 'Event type error' )
            self.register_log(error_event)
        except TypeError:
            error_event = ErrorEvent(datetime.datetime.now(),'Tipo erroneo', traceback.format_exc(), 'Type error')
            self.register_log(error_event)
        except Exception:
            error_event = ErrorEvent(datetime.datetime.now(),'Error inesperado', traceback.format_exc(), 'Error General' )
            self.register_log(error_event)