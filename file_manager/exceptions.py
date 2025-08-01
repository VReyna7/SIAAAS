class LogRecordError(Exception):
    pass

class InvalidEventTypeError(LogRecordError):
    def __init__(self, message = 'El objeto proporcionado no es una instancia'):
        self.message = message
        super().__init__(self.message)

class FileLogError(LogRecordError):
     def __init__(self, message = 'Error con archivo log'):
        self.message = message
        super().__init__(self.message)

class FileManagerError(Exception):
    pass

class DirNoAllowed(FileManagerError):
    def __init__(self, message = "Directorio no permitido"):
        self.message = message
        super().__init__(self.message)

class FileError(FileManagerError):
    def __init__(self,message = "Problemas al crear el archivo"):
        self.message = message
        super().__init__(message)

class CLIError(Exception):
    pass

class EmptyException:
      def __init__(self,message = "El dato no puede estar vacio"):
        self.message = message
        super().__init__(message)
