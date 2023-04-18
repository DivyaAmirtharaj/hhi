import os
import re
import glob
import docx2txt
import logging
from database import Database
import re

class Preprocessing:
    def __init__(self) -> None:
        logging.basicConfig(filename='example.log', level=logging.DEBUG)
        self.raw_data_dir = 'dedoose_data/'
        self.processed_data_dir = 'processed_dedoose_data/'
        try:
            os.makedirs(self.processed_data_dir)
        except Exception as e:
            logging.info(e)
        
        self.database = Database()
        self.database.delete_table()
        self.database.create_table()

    def create_text_files(self):
        try:
            directory = glob.glob(self.raw_data_dir+'*docx')
        except:
            logging.info(e)
        if not directory:
            return False
        for file_name in directory:
            try:
                with open(file_name, 'rb') as infile:
                    outfile_name = os.path.join(self.processed_data_dir, file_name[len(self.raw_data_dir):-5]+'.txt')
                    outfile = open(outfile_name, 'w', encoding='utf-8')
                    doc = docx2txt.process(infile)
                    doc = re.sub(r'\n\s*\n', '\n', doc)
                    outfile.write(doc)
                outfile.close()
                infile.close()
            except Exception as e:
                logging.info(e)
        return True

    def init_tables(self):
        files = os.listdir(self.processed_data_dir)
        if len(files) > 0:
            for filename in files:
                self.database.add_users(filename[:-4])
            example_file = os.path.join(self.processed_data_dir, files[0])
            with open(example_file, "r") as file:
                prev_line = ''
                number_pattern = r'^[A-Z]\d{2}'
                lines = file.readlines()
                section = ''
                for line in lines:
                    if re.search(r'[A-Z]00', line):
                        sentence = (prev_line.strip()).split('\t')
                        section = sentence[0]
                    prev_line = line
                    if re.search(number_pattern, line): # check if the line matches the pattern
                        question_number = line[0:3]
                        question_pattern = re.compile(f"{question_number}(.*?)({question_number})")
                        question = (re.search(question_pattern, line)).group(1).strip()
                        self.database.add_questions(question_number, question, section)
        else:
            return False

if __name__ == '__main__':
    pre = Preprocessing()
    #pre.create_text_files()
    pre.init_tables()

    