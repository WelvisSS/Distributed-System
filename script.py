import sys

def search(diretorio, keyword):
    text = open(diretorio, "r") 
    d = dict() 

    for line in text:
        words = line.strip().split(" ")          
        for word in words: 
            if word in d: 
                d[word] += 1
            else: 
                d[word] = 1

    text.close()
    return d[keyword] 

args = sys.argv
diretorio, keyword = args[1], args[2]

print(search(diretorio, keyword))