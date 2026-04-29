from collections import Counter

str = 'QA Automation Engineer'
print(str)

# Split by Spaces

var = str.split(' ')
print(var)

str1 = 'Engineering'
print(var[2] in str1)
print(str1[0:8] == var[0])

print(str1[::-1])

str5 = str1[0:8]+var[0]+var[1]
print(str5)


##### Char count from String
#char_count = Counter(str1)
#print(char_count)

x = { }

for c in str1:
    x[c] =x.get(c,0)+1

print(x)