languages = ['Python', 'Go', 'JavaScript']

# for loop
for language in languages:
    print(language)



#while Loop
i=1
n=5
while i<=n:
    print(i)
    i=i+1


#Functions

def add_numbers(num1,num2):
    sum = num1+num2
    print('The sum is',sum)

add_numbers(5,4)


import math
print(math.sqrt(16))




f = open("90DaysOfDevOps.txt", "r")
print(f.read())
f.close()



try:
  f = open("90DaysOfDevOps.txt")
  try:
    f.write("Python is great")
  except:
    print("Something went wrong when writing to the file")
finally:
    print('Finllay Stopped')
