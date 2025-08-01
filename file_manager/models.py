import datetime

class Directory:
    def __init__(self, name, path, date_create, timestamp):
        self.__name = name
        self.__path = path
        self.__date_create = date_create
        self.__date_update = timestamp

class File: 
    def __init__(self, name, ext, path, size, timestamp):
        self.name = name
        self.ext = ext
        self.path = path
        self.size = size
        self.timestap = timestamp 


class Event: 
    def __init__(self, description, tipo, timestamp:datetime):
        if not isinstance(timestamp, datetime.datetime):
            raise TypeError("timestamp debe ser un objeto datetime")
        self.__tipo = tipo
        self.__descripcion = description
        self.__timestamp : datetime = timestamp

    def to_log_string(self):
        return f"\n[{self.__timestamp.isoformat()} | {self.__tipo} {self.__descripcion}]"

class ErrorEvent (Event):
    def __init__(self, timestamp, description, stack_trace, error_message):
        if not isinstance(timestamp, datetime.datetime):
            raise TypeError("timestamp debe ser un objeto datetime")
        self.__error_message = error_message
        self.__stack_trace = stack_trace
        full_description = (
            f"{description} | Error: {error_message} | "
            f"Trace: {stack_trace[:500].replace('\n', ' ')}..."
        )
        super().__init__(full_description, 'ERROR', timestamp)
    
    @property
    def error_message(self):
        return self.__error_message

    @error_message.setter
    def error_message(self, nuevo_valor):
        if not nuevo_valor.strip():
            raise ValueError("El error no puede estar vacio")
        self.__error_message = nuevo_valor


class OperationEvent (Event):
    def __init__(self, timestamp, description, affected_path, operation_type):
        if not isinstance(timestamp, datetime.datetime):
            raise TypeError("timestamp debe ser un objeto datetime")
        self.operation_type = operation_type
        self.affected_path = affected_path
        full_description = f"{description} | Operation: {operation_type} | Path: {affected_path}"
        super().__init__(full_description, 'FILE_OPERATION', timestamp)