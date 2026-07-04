import sys
from cipher.core.buffer import Buffer
from cipher.facade import Facade
from cipher.cli.manager import Manager
from cipher.cli.menu import Menu
from cipher.storage.file_handler import FileHandler

def main() -> None:
    buffer = Buffer()
    filehandler = FileHandler()
    facade = Facade(buffer, filehandler)
    menu = Menu()
    manager = Manager(menu, facade)
    sys.stdout.reconfigure(encoding="utf-8")
    manager.run()

if __name__ == "__main__":
    main()
    