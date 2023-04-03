import docx2txt
import glob
import os

class Processing:
    def __init__ (self):
        self.dir_name = 'dedoose_data/'
        self.dir = os.listdir(self.dir_name)
        self.new_dir = 'dedoose_data/clean_dedoose_data/'
    
    def fileClean(self):
        for file_name in self.dir:
            if file_name.endswith('.txt'):
                print(file_name)
                os.remove(os.path.join(self.dir_name, file_name))


    def fileWrite(self):
        directory = glob.glob('dedoose_data/*.docx')
        for file_name in directory:
            print(file_name)
            with open(file_name, 'rb') as infile:
                outfile_name = os.path.join(self.new_dir, file_name[len(self.dir_name):-5]+'.txt')
                print(outfile_name)
                outfile = open(outfile_name, 'w', encoding='utf-8')
                doc = docx2txt.process(infile)
                outfile.write(doc)
            outfile.close()
            infile.close()

data = Processing()
#data.fileClean()
data.fileWrite()