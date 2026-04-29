
tup=(1,5.25,'kum','bhikshapathi')

print(tup)

#tup[1]=85 It wont support because its Immutable


mylist=[tup]
print(mylist)

address={
    "Hno":"1-110",
    "city": "Hyderabad",
    "country": "India",
}

list=['QA','Automation']
tuple=('Selenium','Playwright')

d={
    "Name":"Bhikshapathi",
    "age":34,
    "city":"Hyderabad",
}

print(d)
d["address"]=address
print(d)
d["list"]=list
print(d)

d["tuple"]=tuple
print(d)

print(d["tuple"])
print(d["address"])
