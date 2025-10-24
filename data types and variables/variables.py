#a=10       #Here a is variable and 10 is data stored in the variable and the data type is Int

#z = "End"   #Here z is variable and "End" is data stored in the variable and the data type is string

name = "Shadow"

value = 0

print(type(name))

print(name)

#Declaring variables in python

a=g=k = "Mango"

x,y = 55, 77

y,x = x,y   #By redeclaring the variable's position we can switch the variable's stored value

print(x,y)

print(k)

print(a)

# Concatenation of variables

print (x+y) # Int + int

print(x+a) # int + string - TypeError: unsupported operand type(s) for +: 'int' and 'str'

#Identifying the datatype of the variable by using the type function

print(type(a))

print(type(x))

# Deleting the variable by del function

del k
