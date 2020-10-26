import zipfile
import os


address =  'C:/Users/Diane_HU/Desktop/SURF/Data/ZIP/'

zip_names = os.listdir(address)
for zip_name in zip_names: 
    if zip_name[-3:]=="zip":
        zip_ref = zipfile.ZipFile(address+zip_name, 'r') 
        zip_ref.extractall('C:/Users/Diane_HU/Desktop/SURF/Data/XML/')






