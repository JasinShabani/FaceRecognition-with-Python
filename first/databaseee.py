

fileHandler = open("bilgiler.txt", "r")
i=0
# Get list of all lines in file
listOfLines = fileHandler.readlines()
for line in listOfLines:
    #print(line.strip())
    #print("Sayac")
    if line.strip()== str(81):
        i=i+1
        break

if i >0:
    print("Bunu alamazsin")
else:
    print("Al baba rahat rahat")


# Close file
fileHandler.close()