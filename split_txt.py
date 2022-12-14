import numpy as np

def split_txt(file_path, clients, numpy=False):
    with open(file_path, "r") as file:
        words = file.read().split()

        if numpy:
            # With Numpy
            split = np.array_split(words, clients)
            
            for i in range(len(split)):
                result = ''
                for word in split[i]:
                    result += word + ' '

                with open(f"res_file{i}.txt", "w") as res_file:
                    res_file.write(result)

        else:
            # Without Numpy
            jump = int(len(words)/(clients))+1

            for i in range(0, len(words), jump):
                result = ''
                for j in range(jump):
                    if(i+j) < len(words):
                        result += words[i+j] + " "
                    
                    with open(f"res_file{i/jump}.txt", "w") as res_file:
                        res_file.write(result)

if __name__ == '__main__':
    split_txt('livro.txt', 3, numpy=True)