from MorphoGen.gen_morph import *

result = open('MorphoGen/diff/persons_parad.txt', 'w', encoding='utf-8')
log_mistakes = open('MorphoGen/diff/mistakes_persons.txt', 'w', encoding='utf-8')

dict_p = read_morph(input_path_morph)
lemmes_common = read_lemmas(lemmas)
lemmes_proper = read_proper()
lemmes_arr = lemmes_common + lemmes_proper
lemmes_dict = {}
for i in lemmes_arr:
    lemmes_dict[i.split(';')[0]] = i.split(';')[1]
const_list = read_constants(morph_constants)  # morph_const.txt

infile_words = 'MorphoGen/diff/PER_frequent_normalized_stress.txt'

with open(infile_words, 'r', encoding='utf8') as fin:
    words = fin.read().split('\n')
    mistakes = set()
    for word in words:
        word_nf = word
        for i in range(12):
            gram_pos = i
            parad_type, stemmatized = cut_stem(lemmes_dict, word_nf)

            if parad_type == '' and len(guess_stem_suff(word_nf)[1]) > 0:
                parad_type_by_guess, stemmatized_by_guess = guess_stem_suff(word_nf)
            else:
                parad_type_by_guess, stemmatized_by_guess = '', []

            if parad_type or parad_type_by_guess or (word_nf in const_list):
                predicted_form = generate_wf('Not found form', parad_type, stemmatized, gram_list,
                                                    word_nf, gram_pos)
                predicted_form.replace('﻿', '')
                result.write(predicted_form + '\n')

            else:
                # print('error: ' + word_nf + '\t' + str(i))
                mistakes.add(word_nf)
        if word_nf in mistakes:
            log_mistakes.write(word_nf + '\n')
        else:
            result.write('\n')

result.close()
