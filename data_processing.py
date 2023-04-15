import os
import re
import glob
import docx2txt

class Preprocessing:
    def __init__(self) -> None:
        self.raw_data_dir = 'dedoose_data/'
        self.processed_data_dir = 'processed_dedoose_data/'

    def doc2text(self):
        directory = glob.glob(self.raw_data_dir+'*docx')
        for file_name in directory:
            with open(file_name, 'rb') as infile:
                outfile_name = os.path.join(self.processed_data_dir, file_name[len(self.raw_data_dir):-5]+'.txt')
                outfile = open(outfile_name, 'w', encoding='utf-8')
                doc = docx2txt.process(infile)
                doc = re.sub(r'\n\s*\n', '\n', doc)
                outfile.write(doc)
            outfile.close()
            infile.close()

