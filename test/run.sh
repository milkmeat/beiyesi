#!/bin/sh


if [ ! -d "SIAM2007" ]; then
    unzip SIAM2007.zip
    cd SIAM2007
    unzip TestData.zip
    cd ..
fi

python formatdata.py ./SIAM2007/TrainingData.txt  ./SIAM2007/TrainCategoryMatrix.csv > training.txt
python formatdata.py ./SIAM2007/TestData.txt  ./SIAM2007/TestTruth.csv > test.txt 

cat training.txt | python classify.py 
