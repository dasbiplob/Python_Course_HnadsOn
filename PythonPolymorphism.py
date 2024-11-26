class Person:
    def __init__(self, name, country):
        self.name = name
        self.country = country
    def speak(self):
        print("Hello, my name is {} and I am from {}.".format(self.name, self.country))
        
        
class Student(Person):
    def __init__(self, name, country, major):
        super().__init__(name, country)
        self.major = major
        
    def speak(self):
        print("Hello, my name is {} and I am a {} major.".format(self.name, self.major))

person = Person("Biplob","Filand")
student = Student("Rishab", "Canada", "Computer Science")

person.speak()
student.speak()
