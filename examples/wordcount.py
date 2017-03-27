from __future__ import print_function
from pyspark import SparkContext

import sys

if __name__ == "__main__":

    if len(sys.argv) != 3:
        print("Usage: wordcount  ", file=sys.stderr)
        exit(-1)

    sc = SparkContext(appName="WordCount")
    text_file = sc.textFile(sys.argv[1])

    counts = text_file.flatMap(lambda line: line.split(" ")).map(lambda word: (word, 1)).reduceByKey(lambda a, b: a + b)
    
    counts.saveAsTextFile(sys.argv[2])
    
    sc.stop()
