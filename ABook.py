from collections import UserDict
import re
from datetime import datetime


class Field:
    def __init__(self, value) -> None:
        self.value = value

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self.value)

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value


class Name(Field):
    pass


class Phone(Field):

    @staticmethod
    def verify_phone(value):
        phone = re.findall(r'\+\d{12}|0\d{9}', value)
        if not phone:
            raise ValueError

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.verify_phone(value)
        self.__value = value


class Birthday(Field):

    @staticmethod
    def verify_birthday(value):
        birthday = re.findall(r'\d{1,2}\.\d{1,2}\.\d{4}', value)
        if not birthday:
            raise ValueError
        return birthday

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.verify_birthday(value)
        self.__value = datetime.strptime(value, "%d.%m.%Y").date()


class Record:
    def __init__(self, name: Name, phone=None, birthday=None) -> None:
        self.name = Name(name)
        self.phones = []
        self.birthday = None

        if phone:
            self.add_phone(phone)

        if birthday:
            self.add_birthday(birthday)

    def __repr__(self):
        return f"{self.name}: {self.phones}, {self.birthday}"

    def add_phone(self, phone):
        phone = Phone(phone)
        return self.phones.append(phone)

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)
        return self.birthday

    def change_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone
                return f"Phone '{old_phone}' is changed"
        return f"Phone '{old_phone}' is not in AddressBook. Try again!"

    def remove_phone(self, del_phone):
        for phone in self.phones:
            if phone.value == del_phone:
                self.phones.remove(phone)
                return f"Phone '{del_phone}' is delete"
        return f"Phone '{del_phone}' is not in AddressBook. Try again!"

    def change_birthday(self, new_birth):
        self.birthday = new_birth
        return f"Date of birthday '{self.name}' is changed: '{new_birth}'"

    def remove_birthday(self):
        if self.birthday:
            self.birthday = None
            return f"Date of birthday is deleted"
        return f"This contact does not have a date of birth"

    def days_to_birthday(self):
        today = datetime.now().date()
        birthday = self.birthday.value.replace(year=today.year)
        if birthday > today:
            delta = (birthday - today).days
        else:
            delta = (birthday.replace(birthday.year + 1) - today).days
        return delta


class ABook(UserDict):
    def __init__(self, *args):
        super().__init__(*args)
        self.count = 0

    def __str__(self):
        return f"{self.data}"

    def __repr__(self):
        return f"{self.data}"

    def add_record(self, record):
        if not record.name.value in self.data:
            self.data[record.name.value] = record
            return f"New contact '{record.name.value}' is added"
        else:
            return f"This contact already exist in AddressBook"

    def iterator(self, n):
        name_in_page = list(self.data.keys())
        if self.count >= len(name_in_page):
            raise StopIteration
        result_list = name_in_page[self.count: min(self.count + n, len(name_in_page))]
        for i in result_list:
            self.count += 1
        yield result_list
