import os #library has been used to get file name and use it to generate new .txt file with output

def main():
    path = input()
    if path == '' or os.path.isfile(path) == False:
        print('Something went wrong try to write correct path to file')
        main()
    else:
        createAbbreviations(path)

def getFileName(path):
    return os.path.basename(path)[:-4]

def openfile(path):
    return open(path,'r').read().splitlines(False)

def manageText(inputValue):
    if isinstance(inputValue, str): 
        inputValue = [inputValue]
    for index in range(len(inputValue)):
        for letter in inputValue[index]: #all values in the loop are decimal values of letters in ASCII table
            if(65 <= ord(letter) <= 90 or 97 <= ord(letter) <= 122):
                inputValue[index] = inputValue[index].replace(letter, letter.upper())
            elif(ord(letter) == 39):
                inputValue[index] = inputValue[index].replace(letter,'')
            else:
                inputValue[index] = inputValue[index].replace(letter,' ')
    return inputValue

def createAbbreviations(path):
    abbrevation, newList = [], []
    inputValue = manageText([line.strip() for line in openfile(path)])

    if(inputValue == ''):
        return

    for word in inputValue:
        for i in range(1,len(word)-1):
            if(word[0] != ' ' and word[i] != ' ' and word[i+1] != ' '):
                abbrevation.append(word[0]+word[i]+word[i+1])
                newList.append([word,word[0]+word[i]+word[i+1],0,i,i+1])
            for j in range(i+1,len(word)-1):
                if(word[0] != ' ' and word[i] != ' ' and word[j+1] != ' '):
                    abbrevation.append(word[0]+word[i]+word[j+1])
                    newList.append([word,word[0]+word[i]+word[j+1],0,i,j+1])
    newList = removeMultiple(newList)
    
    for element in newList:
        element = getScore(element)
    getOutput(newList, path)

def removeMultiple(abbrevation):
    dupliates, clearedList = [],[]
    for i in range(len(abbrevation)-1):
        for j in range(len(abbrevation)-1):
            if(abbrevation[i][1] == abbrevation[j+1][1] and abbrevation[i][0] != abbrevation[j+1][0]):
                dupliates.append(abbrevation[i][1])
    for abbrev in abbrevation:
        if abbrev[1] not in dupliates:
            clearedList.append(abbrev)
    return clearedList

def getScore(text):
    abbrevation, score, firstLettersIndexes, lastLettersIndexes = text[1], text.append(0), text.append([0]), [len(text[0])-1]
    
    for letter in range(len(text[0])): #get indexes of first and last letters
        if text[0][letter] == ' ':
            text[6].append(letter+1)
            lastLettersIndexes.append(letter-1)
		
    for i in range(3,5):        #text variable is a list with lists where each of it contains:
                                #[based line, abbreviation, 0, index of second letter, index of third letter, score, indexes of first letters in based line]
                                #To calculate score we need third and fourth value from each list.
        if text[i] in text[6]:   #if it's the first one
            pass
        elif text[i] in lastLettersIndexes: #if it's the last one
            if text[1][i-2] == 'E':
                text[5] += 20
            else:
                text[5] += 5
        elif (text[i])-1 in text[6]: #if it's second one
            text[5] += 1 + getLetterValue(text[0][text[i]])
        elif (text[i])-2 in text[6]: #if it's third one
            text[5] += 2  + getLetterValue(text[0][text[i]])
        else: #if it's fourth or more, but not the last one
            text[5] += 3 + getLetterValue(text[0][text[i]])

    return text

def getOutput(oldList, path):
    inputValue, my_names_with_abbr, newList = [line for line in [line.strip() for line in openfile(path)]], [], []
    
    for element in oldList:
        if element[0] not in newList:
            newList.append(element[0])
    for x in range(len(newList)):
        newList[x] = [newList[x], dict()]
    for x in range(len(newList)):
        for y in range(len(oldList)):
            if newList[x][0] == oldList[y][0]:
                if oldList[y][1] in newList[x][1] and oldList[y][5] < newList[x][1].get(oldList[y][1]):
                    newList[x][1][oldList[y][1]] = oldList[y][5]
                elif oldList[y][1] not in newList[x][1]:
                    newList[x][1][oldList[y][1]] = oldList[y][5]


    myOutput = open('{}_{}_abbrevs.txt'.format('domanski',getFileName(path)),"w+")
    for x in newList:
        my_names_with_abbr.append(x[0])

    for x in inputValue:
        y = manageText(x)[0]
        if y not in my_names_with_abbr:
            print('{}\n{}'.format(x,''))
            myOutput.writelines([x, '\n', '', '\n'])
        elif inputValue.count(x) == 1:
            print(x)
            for newListElement in newList:
                if y == newListElement[0]:
                    myAbbrevs = []
                    for dictElement in newListElement[1]:
                        #https://stackoverflow.com/questions/3282823/get-the-key-corresponding-to-the-minimum-value-within-a-dictionary
                        if newListElement[1][dictElement] == newListElement[1][min(newListElement[1],key=newListElement[1].get)]:
                            myAbbrevs.append(dictElement)
                    print(*myAbbrevs, sep=' ')
                    myOutput.writelines([x, '\n', ' '.join(myAbbrevs), '\n'])
        else:
            print('{} \n {}'.format(x,''))
            myOutput.writelines([x, '\n', ' '.join(myAbbrevs), '\n'])
    myOutput.close()
    
def getLetterValue(letter):
    dictionary = dict(x.split() for x in open('values.txt','r').read().splitlines(False))
    return int(dictionary[letter.upper()])
  
if __name__== "__main__":
  print('''=== Python assignment ===
Please, write a path to the .txt file(with extension).
Example: C:/Users/John/Desktop/example.txt or only file\'s name if it\'s in the same directory''')
  main()
