import collections
import traceback
import math
import operator

def parseLine(line):
    """
    return docid, labels[], words
    if it's empty line or #comment line, return None,None,None
    """
    line = line.strip()
    if not line:
        return None,None,None            
    if line[0]=='#':
        return None,None,None
    
    parts = line.split()
    docid = parts[0]
    labels = parts[1].split(',')     
    words = parts[2:]
    
    return docid, labels, words

class Classifier:

    def __init__(self, strictLabel=None):
        self.labelWordCount = {}  # the number word occurences in each label (**if a doc contains same word many times, it's only counted ONCE**):   {label : {word: count} }
        self.labelDocid = {} # the docid trained for each label:  {label: set(docids) }
        self.totalDoc = 0
        self.totalVocabulary = set()
        self.strictLabel = strictLabel


        
    def train(self, lineStream):
        """
        each line in lineStream is a doc in following format
        1. empty lines are ignored
        2. lines begin with # are comments, also ignored
        3. the first column is docid,label format, in classification label can be omitted. the rest of the line is a long string with words separated by spaces
        """
        
        for line in lineStream:
            self.trainLine(line)
            
    def trainLine(self, line):
        docid, labels, words = parseLine(line)
    
           
        if docid:
            self.trainDoc(docid, labels, words)    
                
    def trainDoc(self, docid, labels, words):
        """
        label: a string that classifies the current doc
        words: a list of separated words in this doc. (**if a doc contains same word many times, it's only counted ONCE**)
        """
        
        if self.strictLabel:
            if len(labels)>1:
                return
            if labels[0] not in self.strictLabel:
                return
        
        for label in labels:
            if label not in self.labelWordCount:
                self.labelWordCount[label] = collections.defaultdict(lambda: 0)
            if label not in self.labelDocid:
                self.labelDocid[label] = set()       
        if docid in self.labelDocid:
            return
        
        for label in labels:
            self.labelDocid[label].add(docid)
            
        for word in set(words):     # **if a doc contains same word many times, it's only counted ONCE**
            for label in labels:
                self.labelWordCount[label][word]+=1
            self.totalVocabulary.add(word)
        self.totalDoc+=1
            
    def classifyLine(self, line):
        docid, labels, words = parseLine(line)
    
        if docid:
            probabilityPerLabel = self.classifyDoc(words)
            return probabilityPerLabel
            
    def classifyDoc(self, words):
        """
        return the probability of all labels, sorted from highest to lowest
        ((label1, prob1),(label2, prob2),...)  where prob1>prob2>...
        """
            
        if not self.labelWordCount:
            return None
        assert len(self.labelWordCount) == len(self.labelDocid)
            
        probabilityPerLabel = {} #store the final probability for each class label
        for label in self.labelWordCount:
            logProb = 0.0
            counter = self.labelWordCount[label]
            for word in set(words):
                logProb += math.log( float(counter.get(word, 0)+1) / float(len(self.labelDocid[label])+len(self.totalVocabulary)) )   # the smoothing here could be wrong??
            probabilityPerLabel[label] = float(len(self.labelDocid[label]))/float(self.totalDoc) * math.exp(logProb)
        
        sorted_x = sorted(probabilityPerLabel.iteritems(), key=operator.itemgetter(1), reverse=True)
        return sorted_x

                
if __name__=='__main__':
    clss =  Classifier()
    clss.train("""
1 ham aa bb cc xx
2 ham bb cc dd yy
3 ham cc dd aa zz
4 spam xx yy zz aa
5 spam yy zz ww bb
6 spam zz ww xx cc    
    """.split('\n'))
    print clss.classifyDoc(['aa','cc'])
    
    clss =  Classifier()
    clss.train("""
1 A,B aa bb cc xx
2 A bb cc dd yy
3 B cc dd aa zz
4 X,Y xx yy zz aa
5 X yy zz ww bb
6 Y zz ww xx cc    
    """.split('\n'))
    print clss.classifyDoc(['aa','cc'])    