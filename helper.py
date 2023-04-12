import docx2txt
import glob
import os
import re

class Processing:
    def __init__ (self):
        self.dir_name = 'dedoose_data/'
        self.dir = os.listdir(self.dir_name)
        self.new_dir = 'dedoose_data/clean_dedoose_data/'
        self.justice_dir = 'dedoose_data/e_justice/'
    
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

    def fileProcess(self, directory):
        for file_name in os.listdir(directory):
            f = open(self.new_dir+file_name, 'r')
            file_content = f.read()
            outfile_name = os.path.join(self.justice_dir, file_name)
            file_content = re.sub(r'\n\s*\n', '\n', file_content)
            match = re.search(r'JUSTICE AND ACCOUNTABILITY(.*)NARRATIVES AND MEMORIALIZATION', file_content, re.DOTALL)
            if match:
                output_text = match.group(1).strip()
                with open(outfile_name, 'w', encoding='utf-8') as f:
                    f.write(output_text)
                    print(outfile_name)
    
    def fileRead(self):
        f = open('dedoose_data/e_justice/001 ZY.txt', 'r')
        for line in f.readlines():
            print(line)
   
section_start = 'JUSTICE AND ACCOUNTABILITY'
section_end = 'NARRATIVES AND MEMORIALIZATION'
data = Processing()
#data.fileProcess('dedoose_data/clean_dedoose_data/')
#data.fileWrite()
#data.fileRead()