#List
thisList = ["Apple","Mac",2]
print(thisList[0])
print(thisList[2])

for list in thisList:
    print(list)



#Tupples

my_tuple = (1, 2, "three", [4, 5])
print(my_tuple[0])   # OUTPUT 1
print(my_tuple[2])   # OUTPUT "three"98 
print(my_tuple[3][1]) # OUTPUT 4


#Dictionaries
my_dict = {"name":"Biplob","country":"Finland","project":"l2c"}
print(my_dict["name"])

for dict in my_dict:
    print(my_dict["country"])



#Sets
my_set = {1, 2, 3, 4, 5}
other_set = {3, 4, 5, 6, 7}
print(my_set.union(other_set)) 
print(my_set.intersection(other_set)) 
print(my_set.difference(other_set)) 




#Calss
class Person :
    def __init__(self, name, country):
        self.name = name
        self.country = country
person = Person("Rishab", "Canada")
print(person.name)   # OUTPUT "Rishab"
print(person.country)    # OUTPUT "Canada"


#inheritance
class Student(Person):
    def __init__(self, name, country, major):
        super().__init__(name, country)
        self.major = major

student = Student("Rishab", "Canada", "Computer Science")
print(student.name)   # OUTPUT "Rishab"
print(student.country)    # OUTPUT "Canada"
print(student.major)  # OUTPUT "Computer Science"
