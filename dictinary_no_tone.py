

units_file = 'units_no_tone_deploy.txt'
def init_dictinary(dict_file):
    words_to_ids = {}
    with open(dict_file,'r') as f:
        for line in f.readlines():
            line=line.replace('\n','')
            splits=line.split(' ')
            words_to_ids[splits[0]]=int(splits[1])
    ids_to_words = dict(zip(words_to_ids.values(),words_to_ids.keys()))

    return words_to_ids,ids_to_words

dictinary_char_to_label,dictinary_label_to_char = init_dictinary(units_file)
print dictinary_char_to_label
print dictinary_label_to_char
