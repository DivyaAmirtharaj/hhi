import docx2txt
import glob

directory = glob.glob('dedoose_data/*.docx')

for file_name in directory:
    print(file_name)

    with open(file_name, 'rb') as infile:
        outfile = open(file_name[:-5]+'.txt', 'w', encoding='utf-8')
        doc = docx2txt.process(infile)

        outfile.write(doc)

    outfile.close()
    infile.close()