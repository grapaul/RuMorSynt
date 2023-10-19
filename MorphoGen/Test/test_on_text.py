import pymorphy2
from MorphoGen.gen_morph import *

morph = pymorphy2.MorphAnalyzer()

input_file = 'MorphoGen/Test/news_500.txt'
tt_not_found = open('MorphoGen/Test/tt_not_found1.txt', 'w', encoding='utf-8')
tt_log_mistakes = open('MorphoGen/Test/tt_log_mistakes1.txt', 'w', encoding='utf-8')

dict_p = read_morph(input_path_morph)
lemmes_common = read_lemmas(lemmas)
lemmes_proper = read_proper()
lemmes_arr = lemmes_common + lemmes_proper
lemmes_dict = {}
for i in lemmes_arr:
    lemmes_dict[i.split(';')[0]] = i.split(';')[1]
const_list = read_constants(morph_constants)  # morph_const.txt

with open(input_file,'r',encoding='utf8') as fin:
    paragraphs = fin.readlines()

nouns_list = []
forms_to_gen = dict()

for paragraph in paragraphs:
    sentences = paragraph.split('. ')
    for sentence in sentences:
        words = [x.strip(',').strip('"').strip('\n').strip('.').strip('«').strip('»').strip('(').strip(')')
                 for x in sentence.split(' ')]
        for word in words:
            parsing_list = morph.parse(word)
            for parsing in parsing_list[:1]: # берется только первый вариант разбора
                tag = parsing.tag
                if 'NOUN' in tag:
                    word_form = parsing.word.replace('ё','е')
                    norm_form = parsing.normal_form.replace('ё','е')
                    nouns_list.append(norm_form)
                    forms_to_gen[norm_form] = []
                    case = tag.case.replace('nomn','Nom').replace('accs','Acc').replace('gent','Gen').replace('datv','Dat').replace('ablt','Ins').replace('loct','Loc').replace('loc2','Loc')
                    number = tag.number.replace('sing','Sing').replace('plur','Plur')
                    tag_formatted = 'Case=' + case + ';' + 'Number=' + number
                    forms_to_gen[norm_form].append([word_form,tag_formatted])

forms_to_gen = sorted(forms_to_gen.items(), key=lambda x: len(x[1]))

# for elem in forms_to_gen:
#     print(elem)

not_found_form = set()
mistakes = dict()
wf_count = 0
correct_wf_count = 0

for elem in forms_to_gen:
    word_nf = elem[0]
    for form in elem[1]:
        wf_count += 1
        gram_list = form[1]
        w_form, norm_form, found_dict = search_tags_dict(dict_p, word_nf, gram_list)
        parad_type, stemmatized = cut_stem(lemmes_dict, word_nf)
        if not parad_type and len(word_nf) > 4:
            parad_type_adj, stemmatized_adj = guess_adj_stem(word_nf)  # adj
        else:
            parad_type_adj, stemmatized_adj = '', []
        if len(guess_stem_suff(word_nf)[1]) > 0:
            parad_type_by_guess, stemmatized_by_guess = guess_stem_suff(word_nf)
        else:
            parad_type_by_guess, stemmatized_by_guess = '', []

        gram_pos = def_tag_pos(gram_list)
        # print('{}, fd - {}, pt - {}, ptg - {}, pta - {}, cl - {}'.format(word_nf, found_dict, parad_type, parad_type_by_guess,
        #                                                                  parad_type_adj, (word_nf in const_list)))

        if found_dict or parad_type or parad_type_by_guess or (word_nf in const_list):
            predicted_form = generate_wf(found_dict, word_form, parad_type, gram_list,
                                                stemmatized, word_nf,
                                                const_list, gram_pos)
        elif parad_type_adj:
            predicted_form = generate_adj_wf_silent(gram_list, parad_type_adj, stemmatized_adj)
        else:
            predicted_form = '\tNot Found:\t'

        if predicted_form in ['\tNot Found:\t', '\tNot Found1:\t', '\tNot Found2:\t']:
            if word_nf not in not_found_form:
                not_found_form.add(word_nf)
        elif predicted_form != form[0]:
            mistakes[word_nf] = predicted_form + '\t' + form[0] + '\t' + gram_list
        else:
            correct_wf_count += 1

mistakes_sort = sorted(mistakes.items(), key=lambda x: x[0][::-1])
for elem in mistakes_sort:
    tt_log_mistakes.write(elem[0] + '\t' + elem[1] + '\n')

for w in sorted(not_found_form, key= lambda x: x[::-1]):
    tt_not_found.write(w + '\n')

print('Correct word forms rate: {}%'.format(round((100*correct_wf_count/wf_count),2)))
print('Correct word forms rate (without not found words): {}%'.format(round((100*correct_wf_count/(wf_count-len(not_found_form))),2)))

tt_not_found.close()
tt_log_mistakes.close()