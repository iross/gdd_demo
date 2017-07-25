#==============================================================================
# DEFINE TARGET VARIABLES
#==============================================================================

#each string in this list will define a regular expression search
#   EXAMPLE:    [r'\b' + 'ooid' + r'\b', r'\b' + 'ooids' + r'\b']
#               will find all instances of 'ooid' or 'ooids' bound by a non-alphanumeric character
target_names = ['stromatol',r'\b' + 'Gamuza Formation' + r'\b']

# also accepts lists of lists -- if provided, it will also dump a list of documents
#    which include at least one term from each 'set'
#target_names = [['Holocene'], ["South America", "Southern Ocean", "Eastern Pacific", "Western Atlantic"], ["temperature", "precipitation", "moisture"]]

#an optional list of false hits. Leave as empty list if you require none.
bad_words = ['non-stromatolitic','nonstromatolitic','non-stromatolite']
