#==============================================================================
#TARGET NAME EXTRACTOR
#==============================================================================

# import relevant modules and data
#==============================================================================
import re
import os
from csv import reader
from var.target_variables import target_names, bad_words

#start list of to store target occurences
target_list = []

def find_target():
    #matching is case insensitive
#    target_names=[t.lower() for t in target_names]

    # Read file indicating where "References" start
    ref_start = {}
    if os.path.exists("./output/ref_start.tsv"):
        with open("./output/ref_start.tsv") as fin:
            for doc in fin:
                docid, sentid = doc.split("\t")
                ref_start[docid.strip()] = sentid.strip()
    else:
        print "No references file found! Continuing without reference filtering."

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

            #the rest are comma-delimited lists
            wordidx=[l for l in reader([tmp[0][1:-1]])][0]
            wordidx=[int(w) for w in wordidx]
            words=[l for l in reader([tmp[1][1:-1]])][0]
            poses=[l for l in reader([tmp[2][1:-1]])][0]
            ners=[l for l in reader([tmp[3][1:-1]])][0]
            lemmas=[l for l in reader([tmp[4][1:-1]])][0]
            dep_paths=[l for l in reader([tmp[5][1:-1]])][0]
            dep_parents=[l for l in reader([tmp[6][1:-1]])][0]
            dep_parents=[int(d) for d in dep_parents]

            #build list of target occurences for this document
            targets = []

            #sentence string
            sent = ' '.join(words)

            #loop through all the target names
            for name in target_names:
                #starting index of all matches for a target_name in the joined sentence
                matches=[m.start() for m in re.finditer(name,sent.lower())]

                if matches:
                        #if at least one match is found, count number of spaces backward to arrive at word index
                        indices = [sent[0:m].count(' ') for m in matches]
                        #remove double hits (i.e. stromatolitic-thrombolitic)
                        indices = list(set(indices))
                        #target_name spans its starting word index to the number of words in the phrase
                        target_word_idx = [[i,i+len(name.split(' '))] for i in indices]

                        #initialize other data about a found target_name
                        target_pose=[]
                        target_path=[]
                        target_parent=[]
                        target_adj=[]

                        for span in target_word_idx:
                         #poses, paths and parents can be found at same indices of a target_name find
                         target_word = ' '.join(words[span[0]:span[1]])

                         if target_word.lower() not in bad_words:
                             target_children=[]
                             target_pose = poses[span[0]:span[1]]
                             target_path = dep_paths[span[0]:span[1]]
                             target_parent = dep_parents[span[0]:span[1]]

                               #children of each component of a target_name
                             for span_idx in range(span[0], span[1]):
                                 children = [j for j,i in enumerate(dep_parents) if i==span_idx+1]
                                 target_children.append(children)

                                 #gather adjectives of target word
                                 for c in children:
                                     if poses[c]=='JJ':
                                         target_adj.append(words[c])

                               #convert parent_ids to Pythonic ids
                             target_parent = [i-1 for i in target_parent]

                               #add finds to a local variable
#                             target_list.append('\t'.join([docid, sentid, target_word, str(span[0]),str(span[1]), str(target_adj), sent]))
                             target_list.append(
                                     {"docid" : docid,
                                         "sentid" : sentid,
                                         "target_word" : target_word,
                                         "start_idx" : span[0],
                                         "end_idx" : span[1],
                                         "adjectives" : target_adj,
                                         "sentence" : sent}
                                     )

    #write the output as tab-separated values
    with open('./output/output.tsv', 'w') as f:
        f.write("\t".join(target_list[0].keys()))
        f.write("\n")
        for i in target_list:
            f.write("\t".join([i["docid"], i["sentid"], i["target_word"], str(i["start_idx"]), str(i["end_idx"]), str(i["adjectives"]), i["sentence"]]))
            f.write('\n')
    return target_list

if __name__ == '__main__':
    find_targets()
