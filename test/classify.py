import sys
import beiyesi.classifier

clss = beiyesi.classifier.Classifier()

def removeStopWords(words):
    return filter(lambda x: not x.isupper(), words)


#clss.train(sys.stdin)
for line in sys.stdin:
    docid, labels, words = beiyesi.classifier.parseLine(line)
    words = removeStopWords(words)
    clss.trainDoc(docid, labels, words)

#print '--- trained result ---'
#print clss.shortStr()


DAT_FILE = 'test.txt'

total=0
wrong=0
for line in open(DAT_FILE):
    docid, labels, words = beiyesi.classifier.parseLine(line)
    words = removeStopWords(words)
    #print docid, labels, words

    N = len(labels)    
    if N>1:
        continue
    #if strictLabel and labels[0] not in strictLabel:
    #    continue
        
    probs = clss.classifyDoc(words)
    #print probs

    for i in range(0,N):
        if probs[i][0] not in labels:
            wrong+=1
            #print '--- explain the error ---'
            #print 'expect: label=%s,docid=%s'%(labels[0],  docid), clss.explain(labels[0],   words)
            #print 'actual: label=%s,docid=%s'%(probs[i][0],docid), clss.explain(probs[i][0], words)
            continue
    total+=1

print 'total=%d, wrong=%d, score=%f' % (total, wrong, float(total-wrong)/(total))
    
