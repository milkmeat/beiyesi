beiyesi
=======

"beiyesi" is a bayesian text classifier in python.

# Installation
execute
> sudo python setup.py install

Initiate a python object

    >>> import beiyesi
    >>> clss = beiyesi.classifier.Classifier()

# Usage

## Data File Format
each line is a doc, like below
> docid label1,label2 word1 word2 word3

+ docid is a string that uniquely identifies a doc. Multiple docs with the same docid are ignored except the first one.
+ A doc can have one or more labels, separated by comma. ( no spaces around the comma)
+ The rest of the line is a list of words separated by spaces

## Training the classifier
The classifier should be fed with a list of docs that are already labeled

    >>> clss.trainLine("1 ham aa bb cc")
    >>> clss.trainLine("2 spam xx yy zz")

## Classify an unknown doc

    >>> words = ['aa','cc']
    >>> print clss.classifyDoc(words) 
    [('ham', 0.017492711370262388), ('spam', 0.0043731778425655969)]

As the classification result, the probability for each label is returned in a list. In the order of highest probability first. So x[0][0] is the name of the most possible label, x[0][1] is its probability

## Explain how the probability is calculated

    >>> clss.explain('ham', words)
    (0.017492711370262388, 0.21428571428571427, [('aa', 0.2857142857142857), ('cc', 0.2857142857142857)])

It explains that for the given doc "words", how its probablity of being label "ham" is calculated.
+ The first float 0.017492711370262388 is the final result as returned by classifyDoc
+ The second float 0.21428571428571427 is the prior probablity of label "ham"
+ The last list \[('aa', 0.2857142857142857), ('cc', 0.2857142857142857)] shows that for each word in the doc, the probablity that it contributes to the result. In the order of highest probablity word first.

# Math
I am going to skip explaining the bayesian algorithm here. [Naive Bayes classifier in 50 lines](http://ebiquity.umbc.edu/blogger/2010/12/07/naive-bayes-classifier-in-50-lines/) is a good article I refered to.

## Smoothing
I implemented the "add-one-smoothing" as described by the article above.

# Examples

I downloaded the test data set from [SIAM2007](http://web.eecs.utk.edu/events/tmw07/). You can apply beiyesi to it following the next steps.

1. Enter the test directory

     cd beiyesi/test

2. Following script converts the data set to our format. Then runs the tests.

    ./run.sh    

    total=3083, wrong=2398, score=0.222186

It doesn't do well on this data set. But it's still ok for my personal projects. So your miles may very depending on the data you need to process.
    
