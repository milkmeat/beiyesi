import sys
import beiyesi.classifier

strictLabel=['1','2']
clss = beiyesi.classifier.Classifier(strictLabel=strictLabel)
clss.train(sys.stdin)

DAT_FILE = 'test.txt'

correct=0
wrong=0
for line in open(DAT_FILE):
    docid, labels, words = beiyesi.classifier.parseLine(line)
    #print docid, labels, words

    N = len(labels)    
    if N>1:
        continue
    if labels[0] not in strictLabel:
        continue
        
    probs = clss.classifyDoc(words)
    #print probs

    for i in range(0,N):
        if probs[i][0] not in labels:
            wrong+=1
            continue
    correct+=1

print 'correct=%d, wrong=%d, score=%f' % (correct, wrong, float(correct)/(correct+wrong))
    
