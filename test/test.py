txt = "  hello, my name is Peter, \nI am 26 years old "
x = txt.split()
print(x)
new_x = []
for i in x:
    i = i.replace(",", "")
    i = i.replace(".", "")
    new_x.append(i)
print(new_x)
