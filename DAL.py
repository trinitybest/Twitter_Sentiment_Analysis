"""
Author: TH
Date: 02/08/2016
"""

import re
import csv

# regex for Pleasantness
regexp = re.compile(r'Pleasantness')
# regex for Activation
regexa = re.compile(r'\s+Activation\s+')
# regex for Imagery
regexi = re.compile(r'\s+Imagery\s+')
# regex for words found from dictionary
regexf = re.compile(r'^Words\s+')
# regex for Deviation
#regexd = re.compile(r'\s+Deviation:\s+')
pleasantness = []
p_deviation = []
activation = []
a_deviation = []
imagery = []
i_deviation = []
words_from_dict = []
with open('DAL/result.txt') as f:
    for line in f:
        #print(line)
        if regexp.match(line):
            
            ple = re.findall(r'\d+.\d+', line)
            pleasantness.append(ple[0])
            p_deviation.append(ple[1])
        
        #print(regexa.match(line))
        if regexa.match(line):
            act = re.findall(r'\d+.\d+', line)
            activation.append(act[0])
            a_deviation.append(act[1])
        if regexi.match(line):
            img = re.findall(r'\d+.\d+', line)
            imagery.append(img[0])
            i_deviation.append(img[1])
        if regexf.match(line):
            #print(line)
            wrd = re.findall(r'\d+', line)
            #print(wrd)
            words_from_dict.append(wrd[0])
raw_words = []
words = []
with open('DAL/Full-DAL.csv') as f:
    reader = csv.reader(f)
    raw_words = list(reader)
for word in raw_words:
    words.append(word[0].strip())
print(len(words))
print(len(pleasantness))
print(len(p_deviation))
print(len(activation))
print(len(a_deviation))
print(len(imagery))
print(len(i_deviation))
print(len(words_from_dict))

result_file = open('DAL/DAL-Full-List.csv', 'w')
wr = csv.writer(result_file, lineterminator='\n')
wr.writerow(['word', 'Pleasantness', 'P_Deviation', 'Activation', 'A_Deviation', 'Imagery', 'I_Deviation', 'Words found from dictionary'])
for x in range(0, len(words)):
    wr.writerow([words[x], pleasantness[x], p_deviation[x], activation[x], a_deviation[x], imagery[x], i_deviation[x], words_from_dict[x]])