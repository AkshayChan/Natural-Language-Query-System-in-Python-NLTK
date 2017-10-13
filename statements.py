# File: statements.py
# Template file for Informatics 2A Assignment 2:
# 'A Natural Language Query System in Python/NLTK'

# John Longley, November 2012
# Revised November 2013 and November 2014 with help from Nikolay Bogoychev
# Revised November 2015 by Toms Bergmanis and Shay Cohen
# Revised November 2016 by Adam Lopez

# PART A: Processing statements

def add(lst,item):
    if (item not in lst):
        lst.insert(len(lst),item)


class Lexicon:
    """stores known word stems of various part-of-speech categories"""
    
    def __init__(self):
        self.num = []
    
    def add(self, stem, cat):
        self.num.append((stem, cat))
    
    def getAll(self,cat):
        output = []
        for i in self.num:
            if i[1] == cat and i[0] not in output:
                output.append(i[0])
        return output
        


class FactBase:
    
    def __init__(self):
        self.unaryFacts = []
        self.binaryFacts = []
    
    def addUnary(self, sym, pred):
        self.unaryFacts.append((sym, pred))
    
    def addBinary(self, sym, pred1, pred2):
        self.binaryFacts.append((sym, pred1, pred2))
    
    def queryUnary(self, sym, pred):
        return (sym, pred) in self.unaryFacts
    
    def queryBinary(self, sym, pred1, pred2):
        return (sym, pred1, pred2) in self.binaryFacts

vb = []
vbz = []

import re
from nltk.corpus import brown

for (word, tag) in brown.tagged_words():
    if tag == "VB":
        vb.append(word)
    if tag == "VBZ":
        vbz.append(word)

def verb_stem(s):
    stem = ""
    """extracts the stem from the 3sg form of a verb, or returns empty string"""
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
    elif s == "has":
        stem = "have"
    elif re.match ("[a-z]*[^iosxz]es$", s) and s[-4:-2] != 'ch' and s[-4:-2] != 'sh':
        stem = s[:-1]
    else:
        stem = ""
    #if ((stem, "VB") in brown.tagged_words() and (s, "VBZ") in brown.tagged_words()):
    #return stem
    #else:
    #return ""
    if (stem in vb and s in vbz):
        return stem
    else:
        return ""


def add_proper_name (w,lx):
    """adds a name to a lexicon, checking if first letter is uppercase"""
    if ('A' <= w[0] and w[0] <= 'Z'):
        lx.add(w,'P')
        return ''
    else:
        return (w + " isn't a proper name")


def process_statement (lx,wlist,fb):
    """analyses a statement and updates lexicon and fact base accordingly;
       returns '' if successful, or error message if not."""
    # Grammar for the statement language is:
    #   S  -> P is AR Ns | P is A | P Is | P Ts P
    #   AR -> a | an
    # We parse this in an ad hoc way.
    msg = add_proper_name (wlist[0],lx)
    if (msg == ''):
        if (wlist[1] == 'is'):
            if (wlist[2] in ['a','an']):
                lx.add (wlist[3],'N')
                fb.addUnary ('N_'+wlist[3],wlist[0])
            else:
                lx.add (wlist[2],'A')
                fb.addUnary ('A_'+wlist[2],wlist[0])
        else:
            stem = verb_stem(wlist[1])
            if (len(wlist) == 2):
                lx.add (stem,'I')
                fb.addUnary ('I_'+stem,wlist[0])
            else:
                msg = add_proper_name (wlist[2],lx)
                if (msg == ''):
                    lx.add (stem,'T')
                    fb.addBinary ('T_'+stem,wlist[0],wlist[2])
    return msg


lx = Lexicon()
fb = FactBase()
'''
verb_stem("cats")
a = process_statement(lx, ["John","is","a","duck"], fb)
print a

fb.addBinary("loves","John","mango")
print fb.binary
print fb.unary
"""
#lx.add("XYZ","A")
#lx.add("XYZ","A")
#print lx.getAll("A")
'''

# End of PART A.

