__author__ = 'jidziak'

import types

class ObiektyDodawalne:
    CALLABLES = (types.FunctionType, types.MethodType)
    def __init__(self):
        self.fields = []
        self.values = []
        self.types = []
    def __add__(self, obj2):
        for key, value in self.__dict__.items():
            if not isinstance(value, ObiektyDodawalne.CALLABLES):
                if not key in ('values', 'fields', 'types'):
                    self.fields.append(key)
                    self.values.append(value)
                    self.types.append(type)
            for key, value in obj2.__dict__.items():
                if not isinstance(value, ObiektyDodawalne.CALLABLES):
                    if not key in ('values', 'fields', 'types'):
                        if not key in self.fields:
                            self.fields.append(key)
                            self.values.append(value)
                            self.types.append(type)
    def test(self):
        for key, value in self.__dict__.items():
            if not isinstance(value, ObiektyDodawalne.CALLABLES):
                if not key in ('values', 'fields', 'types'):
                self.fields.append(key)
        print(key, value, value.__class__.__name__)


class Osoba(ObiektyDodawalne):
    def __init__(self):
        ObiektyDodawalne.__init__(self)
        self.gender = "Woman"
        self.age = 67

class Student(Osoba):
    def __init__(self):
        Osoba.__init__(self)
        self.subject = "Math"
        self.level = [1,2]

class Pracownik(Osoba):
    def __init__(self):
        Osoba.__init__(self)
        self.status = "Professor"
        self.level = 2

x = Student()
y = Pracownik()

x+y
y+x