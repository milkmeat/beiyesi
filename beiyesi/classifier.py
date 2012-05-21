import collections
import traceback
import math

class Classifier:

    def __init__(self):
        self.labelWordCount = {}  # the number word occurences in each label (**if a doc contains same word many times, it's only counted ONCE**):   {label : {word: count} }
        self.labelDocid = {} # the docid trained for each label:  {label: set(docids) }
        self.totalDoc = 0
        
    def train(self, lineStream):
        """
        each line in lineStream is a doc in following format
        1. empty lines are ignored
        2. lines begin with # are comments, also ignored
        3. the first column is docid,label format, in classification label can be omitted. the rest of the line is a long string with words separated by spaces
        """
        
        for line in lineStream:
            line = line.strip()
            if not line:
                continue            
            if line[0]=='#':
                continue
            
            try:
                parts = line.split()
                docid, label = parts[0].split(',')
            except:
                print 'wrong format:', line
                traceback.print_exc()
        
            if label:
                self.trainDoc(docid, label, parts[1:])
                
    def trainDoc(self, docid, label, words):
        """
        label: a string that classifies the current doc
        words: a list of separated words in this doc. (**if a doc contains same word many times, it's only counted ONCE**)
        """
        
        if label not in self.labelWordCount:
            self.labelWordCount[label] = collections.defaultdict(lambda: 0)
        if label not in self.labelDocid:
            self.labelDocid[label] = set()       
        if docid in self.labelDocid:
            return

        self.labelDocid[label].add(docid)
        for word in set(words):     # **if a doc contains same word many times, it's only counted ONCE**
            self.labelWordCount[label][word]+=1
        self.totalDoc+=1
            
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
                logProb += math.log( float(counter.get(word, 0)+1) / float(len(self.labelDocid[label])*2) )   # the smoothing here could be wrong??
            probabilityPerLabel[label] = float(len(self.labelDocid[label]))/float(self.totalDoc) * math.exp(logProb)
        return probabilityPerLabel

                
if __name__=='__main__':
    clss =  Classifier()
    clss.train("""
1,ham aa bb cc xx
2,ham bb cc dd yy
21,ham cc dd aa zz
3,spam xx yy zz aa
4,spam yy zz ww bb
5,spam zz ww xx cc    
    """.split('\n'))
    
    print clss.classifyDoc(['aa','cc'])