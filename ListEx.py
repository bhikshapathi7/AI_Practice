list =[1,2.5,9,7,'us','pa',9.12]

print(list)
print(type(list))

# Print Perticular index value

print(list[5])

# Print index value from last
print(list[-4])

# Print some part value from list
print(list[1:6])

#Insert values at perticular position
list.insert(3,'bk')
print(list)

list[4]= 'uspa'
print(list)

#Insert values at the end
list.append('krithik')
print(list)

#Reverse of list
#list.reverse()
reverseList = list[::-1]
print(reverseList)