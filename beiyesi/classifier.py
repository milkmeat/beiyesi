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

    def __init__(self, strictLabel=None, doubleWord=False):
        """
        strictLabel: if provided, the classifier only accepts the test data with just 1 label which is specified by strictLabel (multi-label items are ignored). 
        doubleWord: generate double word from the original word stream. e.g. a b c -> a, b, a b, c, b c
        """
        self.labelWordCount = {}  # the number word occurences in each label (**if a doc contains same word many times, it's only counted ONCE**):   {label : {word: count} }
        self.labelDocid = {} # the docid trained for each label:  {label: set(docids) }
        self.totalDoc = 0
        self.totalVocabulary = set()
        self.strictLabel = strictLabel
        self.doubleWord = doubleWord

    def __str__(self):
        return """
labelWordCount: %s,
labelDocid: %s,
totalDoc: %d,
totalVocabulary: %s,
strictLabel: %s,
doubleWord: %s
        """ % (
        self.labelWordCount, 
        self.labelDocid, 
        self.totalDoc, 
        self.totalVocabulary, 
        self.strictLabel, 
        self.doubleWord
        )

    def shortStr(self):
        result = ''
        for k,v in self.labelDocid.iteritems():
            result+= ','+k+':'+str(len(v))  
        return result

    def getWordStream(self, words):
        if not self.doubleWord:
            for word in set(words):
                yield word
        else:    
            seen=set()
            prevWord = None
            for word in words:
                if not prevWord:
                    prevWord = word
                    yield word
                else:
                    doubleWord = "%s %s" % (prevWord, word)
                    for w in (word, doubleWord):
                        if w not in seen:
                            print 'yielding',w 
                            seen.add(w)
                            yield w
                    prevWord = word
            
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
                self.labelWordCount[label] = {}
            if label not in self.labelDocid:
                self.labelDocid[label] = set()       
        if docid in self.labelDocid:
            return
        
        for label in labels:
            self.labelDocid[label].add(docid)
            
        for word in self.getWordStream(words):     # **if a doc contains same word many times, it's only counted ONCE**
            for label in labels:
                self.labelWordCount[label][word]= self.labelWordCount[label].get(word,0)+1
            self.totalVocabulary.add(word)
        self.totalDoc+=1
            
    def classifyLine(self, line):
        docid, labels, words = parseLine(line)
    
        if docid:
            probabilityPerLabel = self.classifyDoc(words)
            return probabilityPerLabel

    def getLabelWordProb(self, label, word):
        return float( self.labelWordCount[label].get(word, 0)+1) / float(len(self.labelDocid[label])+len(self.totalVocabulary))
            
    def getLabelPriorProb(self, label):
        return float(len(self.labelDocid[label])+len(self.labelDocid))/((self.totalDoc)+len(self.totalVocabulary)*len(self.labelDocid))

    def getWordsProb4Doc(self, label, words):
        """ return [(word, prob)], not sorted """
        result = []
        for word in self.getWordStream(words):
            result.append( (word, self.getLabelWordProb(label, word)) )
        return result

    def getLabelDocProb(self, label, words):
        logProb = 1
        for word, prob in self.getWordsProb4Doc(label, words):
            logProb *= prob    
        logProb *= self.getLabelPriorProb(label) 
        return logProb

    def explain(self, label, words):
        """
        explain the probability that [words] can be in label,
        return finalprob, priorProb, [(word, wordProb)...(order from high to low)]
        """
        wordsprob = self.getWordsProb4Doc(label, words)
        wordsprob.sort(lambda a, b: cmp(a[1], b[1]), reverse=True)
        return self.getLabelDocProb(label, words), self.getLabelPriorProb(label), wordsprob


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
            probabilityPerLabel[label] = self.getLabelDocProb(label, words)

        
        sorted_x = sorted(probabilityPerLabel.iteritems(), key=operator.itemgetter(1), reverse=True)
        return sorted_x

                
if __name__=='__main__':

    trainLineStream2 = """
1 A,B aa bb cc xx
2 A bb cc dd yy
3 B cc dd aa zz
4 X,Y xx yy zz aa
5 X yy zz ww bb
6 Y zz ww xx cc    
    """.split('\n')
    clss =  Classifier()
    clss.train(trainLineStream2)
    print clss.classifyDoc(['aa','cc'])

    trainLineStream1 = """
1 ham aa bb cc xx
2 ham bb cc dd yy
3 ham cc dd aa zz
4 spam xx yy zz aa
5 spam yy zz ww bb
6 spam zz ww xx cc    
    """.split('\n')
    
    clss =  Classifier()
    clss.train(trainLineStream1)
    words = ['aa','cc']
    print clss.classifyDoc(words)
    print clss.shortStr()
    
    print clss
    print 'ham  explained:',clss.explain('ham', words)
    print 'spam explained', clss.explain('spam', words)


    print '---- test for doubleWord ----'
    clss =  Classifier(doubleWord=True)
    clss.train(trainLineStream1)
    words = ['aa','cc']
    print clss.classifyDoc(words)
    print clss.shortStr()
    print clss
