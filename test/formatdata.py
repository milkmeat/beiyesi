import traceback
import re
import sys

#usage: python formatdata.py >training.txt
# change the 2 filenames below if you want to change the dataset
DATA_FILE, CAT_FILE = ('./SIAM2007/TrainingData.txt','./SIAM2007/TrainCategoryMatrix.csv')
DATA_FILE, CAT_FILE = ('./SIAM2007/TestData.txt','./SIAM2007/TestTruth.csv')

def getCategory(catline):
    """
    input: -1,1,-1,-1
    return a list of positions where 1 is present. (0-based index)
    """
    result = []
    parts = catline.split(',')
    for idx, val in enumerate(parts):
        if val.strip()=='1':
            result.append(str(idx))
    return result
    
def getDoc(docline):
    """
    input: 1~aa bb cc
    return docid, doctxt
    """
    idxWave = docline.find('~')
    if idxWave<0:
        raise Exception('~ is missing')
    docid = docline[:idxWave]
    doctxt = docline[idxWave+1:]
    
    sep=re.compile(r'[ _.]+') 
    docwords = sep.split(doctxt)    
    
    return docid, docwords

if __name__ == '__main__':
    if len(sys.argv)<3:
        print 'usage: python %s <DATA_FILE> <CATEGORY_FILE>" % (sys.argv[0])
    
    DATA_FILE = sys.argv[1]
    CAT_FILE = sys.argv[2]
        
    with open(DATA_FILE) as datfile:
        with open(CAT_FILE) as catfile:
            while True:
                datline = datfile.readline()
                catline = catfile.readline()
                
                if not datline or not catline:
                    if datline or catline:
                        raise  Exception('line numbers not match, using wrong file?')
                    break
                
                datline = datline.strip()
                catline = catline.strip()
                
                docid, docwords = getDoc(datline)
                categories = getCategory(catline)
                print docid, ','.join(categories), ' '.join(docwords)
