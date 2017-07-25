#==============================================================================
#DOCUMENT OF INTERST EXTRACTOR
# Extracts the list of documents + terms matching a specified pattern.
# If a list of lists of words is passed in, it will require an AND across lists
# e.g. [[a], [b, c]] as targets means that a document will be included if (a AND b)
#   OR (a AND c) occur in the document
#
#==============================================================================

# import relevant modules and data
#==============================================================================
import re
import os
from csv import reader

#start list of to store target occurences
target_list=['\t'.join(['docid','sentid','target','start_idx','end_idx','adjectives','sentence'])]

#define target word(s)
with open('./var/target_variables.txt') as fid:
    target_variables = fid.readlines()

for i in target_variables:
    exec i

#matching is case insensitive
if isinstance(target_names[0], list):
    extra_logic = True
    target_names_original = target_names
    target_names = [item for sub in target_names_original for item in sub]
    target_names=[t.lower() for t in target_names]
else:
    extra_logic = False
    target_names=[t.lower() for t in target_names]


ref_start = {}
if os.path.exists("./output/ref_start.tsv"):
    with open("./output/ref_start.tsv") as fin:
        for doc in fin:
            docid, sentid = doc.split("\t")
            ref_start[docid.strip()] = sentid.strip()
else:
    print "No references file found! Continuing without reference filtering."

doc_targets = {}

#load and loop through data
with open('./input/sentences_nlp352','r') as fid:
    for r in fid:
        #file is table delimited
        row=r.replace('\n','').split('\t')
        #first three items are integers/strings
        docid=row[0]
        sentid=row[1]
        if docid in ref_start and int(sentid) > int(ref_start[docid]) : continue
        tmp=row[2:]

        words=[l for l in reader([tmp[1][1:-1]])][0]

        #sentence string
        sent = ' '.join(words)

        #loop through all the target names
        for name in target_names:
            #starting index of all matches for a target_name in the joined sentence
            matches=[(m.start(), m.end()) for m in re.finditer(name,sent.lower())]

            if matches:
                for match in matches:
                    if docid in doc_targets:
                        doc_targets[docid].append(sent[match[0]:match[1]])
                    else:
                        doc_targets[docid] = [sent[match[0]:match[1]]]

with open('./output/matching_documents.txt', 'w') as f:
    for doc, targets_found in doc_targets.iteritems():
        if extra_logic:
            hits = [False for i in range(len(target_names_original))]
            for sub in range(len(target_names_original)):
                for term in target_names_original[sub]:
                    if term.lower() in targets_found:
                        hits[sub] = True
        else:
            hits = [True]

        if all(hits):
            f.write("%s\t%s\n" % (doc, targets_found))
