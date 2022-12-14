import os
import numpy as np
import zipfile as zf

def split_txt(file_path, clients, numpy=False):
    result_dir = './split_result'

    if not os.path.exists(result_dir):
        os.makedirs(result_dir)

    with open(file_path, "r") as file:
        words = file.read().split()

        if numpy:
            # With Numpy
            split = np.array_split(words, clients)
            
            for i in range(len(split)):
                result = ''
                for word in split[i]:
                    result += word + ' '

                with open(f"{result_dir}/res_file{i}.txt", "w") as res_file:
                    res_file.write(result)

        else:
            # Without Numpy
            jump = int(len(words)/(clients))+1

            for i in range(0, len(words), jump):
                result = ''
                for j in range(jump):
                    if(i+j) < len(words):
                        result += words[i+j] + " "
                    
                    with open(f"{result_dir}/res_file{int(i/jump)}.txt", "w") as res_file:
                        res_file.write(result)


def create_zips(split_path, script):
    split_files = os.listdir(split_path)
    
    print(split_files)
    
    result_dir = './zips'

    if not os.path.exists(result_dir):
        os.makedirs(result_dir)

    for i in range(len(split_files)):
        zipfile = zf.ZipFile(f'{result_dir}/parte{i}.zip', 'w', zf.ZIP_DEFLATED)
        zipfile.write(script)
        zipfile.write(split_path+'/'+split_files[i], split_files[i])
        zipfile.close()
        

if __name__ == '__main__':
    split_txt('livro.txt', 3)
    create_zips('./split_result', './script.py')