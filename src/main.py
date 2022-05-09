from os import listdir
from random import randrange
import hashlib
import pandas as pd
from datetime import datetime

nft_dataframe: pd.DataFrame = None
df_path = './assets/dataset/nft_dataframe.xlsx'

class NFT:
    def __init__(self):
        self.__images_path = './assets/images'
        self.__images_collection = [
            [1111,2222,3333,4444,555,6666,777,888,9],
            [1,2,3,4,5,6,7],
            [19,41,543,52,43,6,1,64,514,431,43],
            [5,4,1,3,5,6,7,421,414,43],
            [3,6,7,14,5,7,1343,4]
        ]
        self.__randomize_collection()

    # Read images folder and set __images_collection list
    def __set_collection(self):
        number = None
        for f in listdir(self.__images_path):
            # Check the extension
            if f[f.rfind('.',):len(f)].lower() != '.txt': continue

            # Check if the number is a new number
            if f[:f.find('.')] != number: 
                number = f[:f.find('.')]
                self.__images_collection.append([])

            # Append file to __images_collection
            self.__images_collection[-1].append(f)

    # Randomize an item
    def __randomize_item(self, item_list):
        return item_list[randrange(0, len(item_list))]

    # Randomize a collection
    def __randomize_collection(self):
        return list(map(self.__randomize_item, self.__images_collection))

    # Generate new art
    def generate(self):
        image_list = self.__randomize_collection()
        sha = hashlib.sha256()
        for i in image_list:
            sha.update(str(i).encode())
        date = datetime.now()
        # Return (date, image_list, hash code)
        return (date, image_list, sha.hexdigest())

def open_dataset():
    try:
        global nft_dataframe
        nft_dataframe = pd.DataFrame(pd.read_excel(df_path))
    except Exception as e:
        if e.args[1] == 'No such file or directory':
            nft_dataframe = pd.DataFrame(columns=['NUMBER', 'CREATION DATE', 'COLLECTION', 'HASH'])
            nft_dataframe.to_excel(df_path)
            print(f'A new excel file was created ({df_path})')
    
    print(f'Dataset loaded ({df_path})')

def append_dataset(creation_date, collection, hash):
    global nft_dataframe
    if (nft_dataframe == None): open_dataset()

    collection_str = ''
    for index, c in enumerate(collection):
        collection_str += str(c)
        if index < len(collection)-1: collection_str += chr(10)

    data = {
        'NUMBER': len(nft_dataframe),
        'CREATION DATE': creation_date,
        'COLLECTION': collection_str,
        'HASH': hash
    }
    dataframe = pd.DataFrame(data, index=[0])
    nft_dataframe = pd.concat([nft_dataframe, dataframe], ignore_index=True)
    nft_dataframe.to_excel(df_path, index=False)

if __name__ == '__main__':
    nft = NFT().generate()

    append_dataset(nft[0], nft[1], nft[2])
    