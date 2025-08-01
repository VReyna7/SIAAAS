from file_manager.cli import CLIManager
import datetime
from file_manager.exceptions import EmptyException

cli_manager = CLIManager()
while True:
    cli_manager.menu_cli()
    try:
        dato = cli_manager.input_menu()
        if not cli_manager.selectionMenu(dato):
            break
    except EmptyException:
        print('No ingrese datos vacios')
    except Exception as x:
        print('Error no especificado: ', x)