# import os 
  
# cmd = 'python -c "import teste2; teste2.imprimir()"' 

# os.system(cmd)

with open('./Client/txt0.txt', 'r') as arquivo:
    result = int(arquivo.read().strip())    
    print(result)