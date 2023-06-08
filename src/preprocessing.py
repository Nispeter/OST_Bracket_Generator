import re

with open('input.txt','r') as file:
    data = file.read()

pattern = r'(?<=\d\.-\s).*'
strings = re.findall(pattern,data)


with open('output.txt','w') as file:
    for string in strings: 
        file.write(string + '\n')