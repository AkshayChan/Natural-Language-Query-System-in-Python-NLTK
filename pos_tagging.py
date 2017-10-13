# File: pos_tagging.py
# Template file for Informatics 2A Assignment 2:
# 'A Natural Language Query System in Python/NLTK'

# John Longley, November 2012
# Revised November 2013 and November 2014 with help from Nikolay Bogoychev
# Revised November 2015 by Toms Bergmanis and Shay Cohen
# Revised November 2016 by Adam Lopez

# PART B: POS tagging

from statements import *

# The tagset we shall use is:
# P  A  Ns  Np  Is  Ip  Ts  Tp  BEs  BEp  DOs  DOp  AR  AND  WHO  WHICH  ?

# Tags for words playing a special role in the grammar:

function_words_tags = [('a','AR'), ('an','AR'), ('and','AND'),
     ('is','BEs'), ('are','BEp'), ('does','DOs'), ('do','DOp'), 
     ('who','WHO'), ('which','WHICH'), ('Who','WHO'), ('Which','WHICH'), ('?','?')]
     # upper or lowercase tolerated at start of question.

function_words = [p[0] for p in function_words_tags]

def unchanging_plurals():
    single = []
    plural = []
    unchange = []
    with open("sentences.txt", "r") as f:
        for line in f:
            for tag_phrase in line.split():        #Splits the sentence on whitespace
                word, tag = tag_phrase.split('|')  #Splits the tagged word on '|'
                if tag == 'NN':
                    single.append(word)
                elif tag == 'NNS':
                    plural.append(word)
    for s in single:
        if s in plural and s not in unchange:      #If tagged as both and not in output
            unchange.append(s)
    return unchange


unchanging_plurals_list = unchanging_plurals()

def noun_stem (s):
    """extracts the stem from a plural noun, or returns empty string"""    
    stem = ""
    if s in unchanging_plurals_list:               #If plural form same as singular
        stem = s
    elif re.match("[a-z]*ves$", s):
        stem = s[:-3] + "fe"
    else:                                          #Checks for all the 3s rules
        if re.match ("[a-z]*[^sxyzaeiou]s$", s) and s[-4:-2] != 'ch' and s[-4:-2] != 'sh':
            stem = s[:-1]
        elif re.match ("[a-z]*[aeiou]ys$", s):
            stem = s[:-1]
        elif re.match ("[a-z]+[^aeiou]ies$", s) and len(s) >= 3:
            stem = s[:-3] + "y"
        elif re.match ("[^aeiou]ies$", s):
            stem = s[:-1]
        elif re.match ("[a-z]*[ox]es$", s) or s[-4:] == "ches" or s[-4:] == "shes" or s[-4:] == "sses" or s[-4:] == "zzes":
            stem = s[:-2]
        elif (re.match ("[a-z]*ses$", s) or re.match("[a-z]*zes$", s)) and s[-3:] != "sses" and s[-3:] != "zzes":
            stem = s[:-1]
        elif re.match ("[a-z]*[^iosxz]es$", s) and s[-4:-2] != 'ch' and s[-4:-2] != 'sh':
            stem = s[:-1]
        else:
            stem = ""
    return stem

def tag_word (lx,wd):
    """returns a list of all possible tags for wd relative to lx"""
    taggings = []
    tagset = ["P", "A"]
    tag_verbs = ["I", "T"]

    if wd in function_words:
        for tag in function_words_tags:
            if tag[0] == wd:
                taggings.append(tag[1])

    for tag in tagset:                             #Checks if the word is tagged in the lexicon
        if wd in lx.getAll(tag):
                taggings.append(tag)


    if wd in lx.getAll("N"):                       #Only plural nouns can take us to singlur stems
        if wd in unchanging_plurals_list:
            taggings += ["Ns", "Np"]
        elif noun_stem(wd) == '':
            taggings.append("Ns")
        else:
            taggings.append("Np")
    if noun_stem(wd) in lx.getAll("N"):
        taggings.append("Np")
    for i in lx.getAll("N"):
        if noun_stem(i) == wd:
            taggings.append("Ns")
            break

    for tag in tag_verbs:
        if wd in lx.getAll(tag):                   #Only singular verbs can take us to plural stems
            if verb_stem(wd) == '':
                taggings.append(tag + "p")
            else:
                taggings.append(tag + "s")
        if verb_stem(wd) in lx.getAll(tag):
            taggings.append(tag + "s")
        for i in lx.getAll(tag):
            if verb_stem(i) == wd:
                taggings.append(tag + "p")
                break


    taggings = list(set(taggings))
    return taggings

def tag_words (lx, wds):
    """returns a list of all possible taggings for a list of words"""
    if (wds == []):
        return [[]]
    else:
        tag_first = tag_word (lx, wds[0])
        tag_rest = tag_words (lx, wds[1:])
        return [[fst] + rst for fst in tag_first for rst in tag_rest]


#noun_stem("countries")

'''
lx.add("dog", "N")
print tag_word(lx, "dogS")
lx.add("fly", "T")
lx.add("fly", "I")
print tag_word (lx, "fly")
print tag_words(lx, ["who", "which", "?", "fly"])
'''

# End of PART B.