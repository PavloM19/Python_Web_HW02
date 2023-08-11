from AddressBook import *


class Bot():
    def __init__(self):
        self.book = AddressBook()

    def __str__(self):
        out_list = []
        for record in self.book.data:  # type: ignore
            out_list.append(str(record))
        return out_list 

    def handle(self, action):
        if action == 'add':
            self.book.add() # type: ignore
        
        elif action == 'search':
            self.book.search() # type: ignore

        elif action == 'edit':
            self.book.edit() # type: ignore
        
        elif action == 'remove':
            self.book.delete() # type: ignore

        elif action == 'save':
            file_name = input("File name: ")
            Storage.save(file_name, self.book)
        
        elif action == 'load':
            file_name = input("File name: ")
            self.book = Storage.load(file_name)
        
        elif action == 'congratulate':
            print(self.book.congratulate()) # type: ignore

        elif action == 'view':
            print(self.book)

        elif action == 'exit':
            pass

        else:
            print("There is no such command!")
