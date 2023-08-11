from datetime import datetime as dt
import re
from abc import ABC, abstractmethod


class Field(ABC):
    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def __getitem__(self):
        pass


class Name(Field):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value

    def __getitem__(self):
        return self.value


class Phone(Field):
    def __init__(self, value=''):                   
        if (type(value) is list) and len(value) > 0:
            self.value = value
        else:
            self.value = []
            while True:                 
                input_values = input("Phones(+48......... or +38..........) (multiple phones can be added with space between them. +48 pattern has 9 symbols after code): ").strip()
                try:
                    for number in input_values.split(' '):
                        if re.match('^\+48\d{9}$', number) or re.match('^\\+38\d{10}$', number) or number == '':
                            self.value.append(number)
                        else:
                            raise ValueError
                except ValueError:
                    print('Incorrect phone number format! Please provide correct phone number format.')
                else:
                    break

    def __str__(self):
        return ', '.join(self.value)

    def __getitem__(self):
        return self.value


class Birthday(Field):
    def __init__(self, value=''):
        while True:
            if value:
                self.value = value
            else:
                self.value = input("Birthday date(dd/mm/YYYY): ").strip()
            try:
                if re.match('^\d{2}/\d{2}/\d{4}$', self.value):
                    self.value = dt.strptime(self.value, "%d/%m/%Y")
                    break
                elif self.value == '':
                    break
                else:
                    raise ValueError
            except ValueError:
                print('Incorrect date! Please provide correct date format.')

    def __str__(self):
        if type(self.value) is dt:
            return self.value.strftime("%d/%m/%Y")
        else:
            return self.value 
    
    def __getitem__(self):
        return self.value
    
    def days_to_birthday(self):
        current_datetime = dt.now()
        bd = self.value.replace(year=current_datetime.year)
        if bd >= current_datetime:
            result = bd - current_datetime
        else:
            bd = self.value.replace(year=current_datetime.year + 1)
            result = bd - current_datetime
        return result.days


class Email(Field):
    def __init__(self, value=''):
        while True:
            if value:
                self.value = value
            else:
                self.value = input("Email: ")
            try:
                if re.match('^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$', self.value) or self.value == '':
                    break
                else:
                    raise ValueError
            except ValueError:
                print('Incorrect email! Please provide correct email.')

    def __str__(self):
        return self.value

    def __getitem__(self):
        return self.value


class Status(Field):
    def __init__(self, value=''):
        self.status_types = ['', 'family', 'friend', 'work']
        while True:            
            if value:
                self.value = value
            else:
                self.value = input("Type of relationship (family, friend, work): ")
            try:
                if self.value in self.status_types:
                    break
                else:
                    raise ValueError
            except ValueError:
                print('There is no such status!')

    def __str__(self):
        return self.value                

    def __getitem__(self):
        return self.value


class Note(Field):
    def __init__(self, value=''):
        if value:
            self.value = value
        else:
            self.value = input("Note: ")

    def __str__(self):
        return self.value

    def __getitem__(self):
        return self.value


class Record:
    def __init__(self, name, phones='', birthday='', email='', status='', note=''):
        self.name = Name(name)
        self.phones = Phone(phones)
        self.birthday = Birthday(birthday)
        self.email = Email(email)
        self.status = Status(status)
        self.note = Note(note)

    def __str__(self):
        out_list = []
        if self.birthday:
            str_birth = self.birthday.value.strftime("%d/%m/%Y")
        else:
            str_birth = ''
        
        if self.phones:
            str_phones = ', '.join(self.phones.value)
        else:
            str_phones = ''

        out_list.append(
            "-" * 50 + f"\nName: {self.name.value} \nPhones: {str_phones} \nBirthday: {str_birth} \nEmail: {self.email.value} \nStatus: {self.status.value} \nNote: {self.note.value}\n" + "-" * 50)
        return '\n'.join(out_list)

