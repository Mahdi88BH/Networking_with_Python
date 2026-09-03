f = open("file.txt", 'a')

print(f"Type of the file => {type(f)}")
print(f"is the file closed : {f.closed}")
print(f"the name of the file : {f.name}")
print(f"the mode of the file to : {f.mode}")
print(f"encoding format of the file : {f.encoding}")

f.write('\nPython') # By defualt if the file doesn't exist it will created
f.close()

f = open('file.txt', 'r')
allLines = f.readlines()

for line in allLines:
    print(line, end='')

f.close()
print("\nfile are properly closed" if f.closed else "The File are not closed yet")


# Contxt Manager Approach
with open('file.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        print(line, end='')