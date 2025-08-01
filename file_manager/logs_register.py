from file_manager.models import Event
from file_manager.exceptions import InvalidEventTypeError, FileLogError

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
