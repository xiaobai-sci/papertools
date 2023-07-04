#!/usr/bin/env python
#-*- coding: utf-8 -*-
# Supporting Python 3 

import sys, os, re
import urllib.request # for Python 3

# Get the input file name from command line argument
try:    
    input_file = sys.argv[1]
except: 
    print("Error: specify the file to be processed!")

# Read the input file as a string
bibtexdb = open(input_file).read()

# Check if the journal list file exists, if not, download it from online source
journal_list_file = 'journalList.txt'
if not os.path.isfile(journal_list_file):
    url = "https://gist.githubusercontent.com/FilipDominec/6df14b3424e335c4a47a96640f7f0df9/raw/74876d2d5df9ed60492ef3a14dc3599a6a6a9cfc/journalList.txt"
    urllib.request.urlretrieve(url, filename=journal_list_file)

# Open the journal list file and read the rules
rulesfile = open(journal_list_file)

# Loop through the rules in reversed alphabetical order to match extended journal names first
for rule in rulesfile.readlines()[::-1]:           
    # Split the rule into pattern and replacement
    pattern, replacement = rule.strip().split(" = ")
    # Avoid mere abbreviations and single words
    if pattern != pattern.upper() and (' ' in pattern):        
        # Replace the pattern with replacement in a case-insensitive way
        repl = re.compile(re.escape(pattern), re.IGNORECASE)               
        (bibtexdb, num_subs) = repl.subn(replacement, bibtexdb)
        # Print the number of substitutions made
        if num_subs > 0:
            print(f"Replacing '{pattern}' with '{replacement}' {num_subs} times")

# Write the modified string to a new output file
output_file = 'abbreviated.bib'
with open(output_file, 'w') as outfile:
    outfile.write(bibtexdb)
    print(f"Bibtex database with abbreviated files saved into '{output_file}'")

