from datetime import datetime as dt, timedelta
from collections import UserList
import pickle
from pathlib import Path

from info import *


class Operations(UserList):
    def add(self):
        name = input("Name: ").strip()
        # phones = Phone()
        # birthday = Birthday()
        # email = Email()
        # status = Status()
        # note = input("Note: ")
        record = Record(name)

        self.data.append(record)
        Storage.log(f"Contact {name} has been added.")

    def search(self):
        print("There are following categories: \nName \nPhones \nEmail \nStatus \nNote")
        result = []
        category = input('Search category: ').strip().lower().replace(' ', '')
        pattern = input('Search pattern: ').strip().lower().replace(' ', '')

        if category in ['name', 'phones', 'email', 'status', 'note']:
            for record in self.data:
                if category == 'name':
                    if pattern in record.name.value.lower():                        
                        result.append(record)
                        
                elif category == 'phones':
                    for phone in record.phones.value:
                        if pattern in phone:
                            result.append(record)
                            break

                elif category == 'email':
                    if pattern in record.email.value.lower():
                        result.append(record)
                        
                elif category == 'status':
                    if pattern in record.status.value.lower():
                        result.append(record)

                elif category == 'note':
                    if pattern in record.note.value.lower():
                        result.append(record)

            if not result:
                print('Nothing found!')
        else:
            print('Category entered incorrectly')

        for record in result:
            if record.birthday:
                birth = record.birthday.value.strftime("%d/%m/%Y")
            else:
                birth = ''

            result = "_" * 50 + "\n" + f"Name: {record.name.value} \nPhones: {', '.join(record.phones.value)} \nBirthday: {birth} \nEmail: {record.email.value} \nStatus: {record.status.value} \nNote: {record.note.value}\n" + "_" * 50
            print(result)

    def edit(self):
        contact_name = input('Contact name: ')
        parameter = input('Which parameter to edit(name, phones, birthday, status, email, note): ').strip()
        new_value = input("New Value: ")

        parameters = ['name', 'phones', 'birthday', 'email', 'status', 'note']

        try:
            if parameter in parameters:
                for record in self.data:
                    if record.name.value == contact_name:
                        if parameter == parameters[0]:
                            record.name = Name(new_value)

                        elif parameter == parameters[1]:
                            record.phones = Phone(new_value)
                        
                        elif parameter == parameters[2]:
                            record.birthday = Birthday(new_value)

                        elif parameter == parameters[3]:
                            record.email = Email(new_value)

                        elif parameter == parameters[4]:
                            record.status = Status(new_value)

                        elif parameter == parameters[5]:
                            record.note = Note(new_value)

                        break
                else:
                    raise NameError

            else:
                raise ValueError
            
        except ValueError:
            print('Incorrect parameter! Please provide correct parameter')
        except NameError:
            print('There is no such contact in address book!')
        else:
            Storage.log(f"Contact {contact_name} has been edited!")
            return True
        return False

    def delete(self):
        pattern = input("Remove contact name: ")
        flag = False
        for record in self.data:
            if record.name == pattern:
                self.data.remove(record)
                Storage.log(f"Contact {record.name.value} has been removed!")
                flag = True
                break

        return flag

    def __get_current_week(self):
        now = dt.now()
        current_weekday = now.weekday()
        if current_weekday < 5:
            week_start = now - timedelta(days=2 + current_weekday)
        else:
            week_start = now - timedelta(days=current_weekday - 5)
        return [week_start.date(), week_start.date() + timedelta(days=7)]

    def congratulate(self):
        result = []
        WEEKDAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        current_year = dt.now().year
        congratulate = {weekday: []  for weekday in WEEKDAYS[:5]}

        for record in self.data:
            if record.birthday:
                new_birthday = record.birthday.value.replace(year=current_year)
                birthday_weekday = new_birthday.weekday()
                if self.__get_current_week()[0] <= new_birthday.date() < self.__get_current_week()[1]:
                    if birthday_weekday < 5:
                        congratulate[WEEKDAYS[birthday_weekday]].append(record.name.value)
                    else:
                        congratulate['Monday'].append(record.name.value)

        for key, value in congratulate.items():
            if len(value):
                result.append(f"{key}: {', '.join(value)}")

        print('_' * 50 + '\n' + '\n'.join(result) + '\n' + '_' * 50)


class AddressBook(Operations):
    def __init__(self):
        super().__init__()
        self.counter = -1

    def __str__(self):
        out_list = []
        for record in self.data:
            out_list.append(str(record))
        return '\n'.join(out_list)  

    def __next__(self):
        self.counter += 1
        if self.data[self.counter].birthday:
            str_birth = self.data[self.counter].birthday.value.strftime("%d/%m/%Y")
        else:
            str_birth = ''

        if self.counter == len(self.data):
            self.counter = -1
            raise StopIteration
        
        return "_" * 50 + "\n" + f"Name: {self.data[self.counter].name.value} \nPhones: {', '.join(self.data[self.counter].phones.value)} \nBirthday: {str_birth} \nEmail: {self.data[self.counter].email.value} \nStatus: {self.data[self.counter].status.value} \nNote: {self.data[self.counter].note.value}\n" + "_" * 50

    def __iter__(self):
        return self

    def __setitem__(self, index, record):
        self.data[index] = record

    def __getitem__(self, index):
        return self.data[index]


class Storage:
    @staticmethod
    def adrbook_to_listdicts(adrbook: AddressBook):# -> list:
        out_list = []
        for rec in adrbook.data:
            rec_dict = {k: str(v) for k,v in rec.__dict__.items()}
            rec_dict['phones'] = rec_dict['phones'].split(', ') # Str -> List # type: ignore 
            out_list.append(rec_dict)
        return out_list

    @staticmethod
    def listdicts_to_adrbook(listdicts: list):# -> AddressBook:
        ab = AddressBook()
        for rec in listdicts:
            ab.data.append(Record(**rec)) #Record(*list(rec.values())))
        return ab

    @staticmethod
    def log(action):
        current_time = dt.strftime(dt.now(), '%H:%M:%S')
        current_data = dt.strftime(dt.now(), '%Y.%m.%Y') 
        message = f'[{current_data} - {current_time}] {action}' 
        log_file = Path(__file__).parent / 'logs.txt' 
        with open(log_file, 'a') as file:
            file.write(f'{message}\n')

    @staticmethod
    def save(file_name, data):
        file_name += '.bin'                            
        path_file = Path(__file__).parent / file_name 
        with open(path_file, 'wb') as file:
            pickle.dump(Storage.adrbook_to_listdicts(data), file)
        Storage.log("Addressbook has been saved!")

    @staticmethod
    def load(file_name): 
        file_name += '.bin'
        path_file = Path(__file__).parent / file_name
        if path_file.exists():
            with open(path_file, 'rb') as file:
                Storage.log("Addressbook has been loaded!")
                return Storage.listdicts_to_adrbook(pickle.load(file))
        else:
            print(f"File '{path_file}' - not found!")