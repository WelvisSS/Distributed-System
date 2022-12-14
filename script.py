import sys

def search(diretorio, keyword):
    text = open(diretorio, "r") 
    d = dict() 

    # Cria um dicinário com a quantidade de ocorrências de cada palavra
    for line in text:
        words = line.strip().split(" ")          
        for word in words: 
            if word in d: 
                d[word] += 1
            else: 
                d[word] = 1

    text.close()

    # Verifica se existe alguma ocorrência da chave informada
    if keyword in d.keys(): 
        return d[keyword] 
    else: 
        return 0
    

args = sys.argv
diretorio, keyword = args[1], args[2]

print(search(diretorio, keyword))