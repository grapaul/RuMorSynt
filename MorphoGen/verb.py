import re

from MorphoGen.parads import find_verb_form, end_postfix
from MorphoGen.morphon import *
from MorphoGen.dictionaries import if_substring, parad_type_from_lemmas, search_tags_dict


def if_form_accept(parad, aspect, trans, grammemes, string_nf, postfix):
    part_accept = True
    if 'VerbForm=Part' in grammemes:
        part_accept = False
        if 'Voice=Act' in grammemes:
            if 'Tense=Pres' in grammemes and aspect == 'нсв':
                part_accept = True
            elif 'Tense=Past' in grammemes:
                part_accept = True
        elif 'Voice=Pass' in grammemes and trans == 'п':
            if postfix:
                part_accept = False
            elif 'Tense=Pres' in grammemes:
                if aspect == 'нсв' and parad in ['1', '2', '4', '5', '6', '12']:
                    part_accept = True
            elif 'Tense=Past' in grammemes:
                if aspect == 'св' or aspect_pair(string_nf):
                    part_accept = True
    return part_accept


def define_parad_type_verb(dict_p, string_nf, grammemes, lemmes_dict, lemmes_trie):
    form_accept = True
    found_dict = False
    postfix = False
    prefix = ''
    w_form = ''

    if string_nf[-2:] in ['ся', 'сь']:
        postfix = True
        string_nf = string_nf[:-2]

    parad_type, aspect, trans = parad_type_from_lemmas(string_nf, 'VERB', lemmes_dict)
    if not parad_type:
        string_nf, prefix = delimit_prefix(string_nf).split('|')[-1], ''.join(delimit_prefix(string_nf).split('|')[:-1])
        parad_type, aspect, trans = parad_type_from_lemmas(string_nf, 'VERB', lemmes_dict)
        if not parad_type:
            if 'Case=' in grammemes:
                grammemes_ = grammemes[: grammemes.find('Case')] + grammemes[grammemes.find('Case')+9:].strip(';')
                grammemes_ = re.sub('Number=Plur', 'Number=Sing', grammemes_)
            else:
                grammemes_ = grammemes
            w_form, n_form, found_dict = search_tags_dict(dict_p, string_nf.replace('йти', 'идти'), grammemes_)
            if not found_dict:
                parad_type, aspect, trans = if_substring(lemmes_dict, prefix + string_nf, 'VERB', lemmes_trie)
                if not parad_type:
                    parad_type = 'wrong_parad'

    if parad_type:
        form_accept = if_form_accept(parad_type, aspect, trans, grammemes, string_nf, postfix)
    return parad_type, found_dict, w_form, prefix, postfix, form_accept


def delimit_prefix(word):
    prefixes = ['в(з[оъ]?|с)', 'в[оъы]?', 'до', 'за', 'и(з[оъ]?|с)', 'над[оъ]?', 'недо', 'на', 'об[оъ]?', 'о(т[оъ]?)?',
                'под[оъ]?', 'по', 'пр(ед?|[ио])', 'ра(зъ?|с)', 'с[оъ]?', 'у']
    vowels = ['а', 'о', 'у', 'ы', 'э', 'я', 'ё', 'ю', 'и', 'е', 'ъ']
    consonants = ['б', 'в', 'г', 'д', 'ж', 'з', 'й', 'к', 'л', 'м',
                  'н', 'п', 'р', 'с', 'т', 'ф', 'х', 'ц', 'ч', 'ш', 'щ']
    delimited = []
    for pref in prefixes:
        res = re.match(re.compile(pref), word)
        if res is not None:
            prefix = res.group()
            l = len(prefix)
            if (word[l] in consonants and word[:3] not in ['отр', 'сла', 'ста']) or prefix[-1] in vowels:
                delimited.append(word[:l])
                delimited.append(delimit_prefix(word[l:]))
                return '|'.join(delimited)
    else:
        return word


def stemmatize_verb(string_nf, parad_type, postfix):
    stemmatized = []

    if postfix:
        string_nf = string_nf.replace('ся', '').replace('сь', '')
    wl = len(string_nf)

    if parad_type:
        if parad_type in ['1', '7']:
            stemmatized.append(string_nf[:wl - 2])
        elif parad_type == '2':
            stemmatized.append(string_nf[:wl - 4])
            stemmatized.append(string_nf[:wl - 2])
        elif parad_type in ['3', '4', '5', '6', '10', '11', '12', '14м', '14н', '15']:
            if parad_type == '14м':
                stemmatized.append(delimit_prefix(''.join((string_nf[:wl - 3], 'м'))))
            elif parad_type == '14н':
                stemmatized.append(delimit_prefix(''.join((string_nf[:wl - 3], 'н'))))
            elif parad_type == '11':
                stemmatized.append(delimit_prefix(''.join((string_nf[:wl - 3], 'ь'))))
            elif parad_type == '12':
                if string_nf[wl - 3] == 'ы':
                    stemmatized.append(''.join((string_nf[:wl - 3], 'о')))
                elif string_nf[wl - 3] == 'и':
                    stemmatized.append(''.join((string_nf[:wl - 3], 'е')))
                else:
                    stemmatized.append(string_nf[:wl - 2])
            elif parad_type == '15':
                stemmatized.append(''.join((string_nf[:wl - 2], 'н')))
            else:
                stemmatized.append(string_nf[:wl - 3])
            stemmatized.append(string_nf[:wl - 2])
        elif parad_type == '7б':
            stemmatized.append(''.join((string_nf[:-3], 'б')))
            stemmatized.append(string_nf[:-3])
        elif parad_type == '7д':
            stemmatized.append(''.join((string_nf[:wl - 3], 'д')))
            stemmatized.append(string_nf[:wl - 3])
        elif parad_type == '7т':
            stemmatized.append(''.join((string_nf[:wl - 3], 'т')))
            stemmatized.append(string_nf[:wl - 3])
        elif parad_type == '8г':
            stemmatized.append(''.join((string_nf[:wl - 2], 'г')))
            stemmatized.append(''.join((string_nf[:wl - 2], 'ж')))
        elif parad_type == '8к':
            stemmatized.append(''.join((string_nf[:wl - 2], 'к')))
            stemmatized.append(''.join((string_nf[:wl - 2], 'ч')))
        elif parad_type == '9':
            stemmatized.append(delimit_prefix(''.join((string_nf[:wl - 5], string_nf[wl - 4]))))
            stemmatized.append(string_nf[:wl - 3])
        elif parad_type == '13':
            stemmatized.append(string_nf[:wl - 4])
            stemmatized.append(string_nf[:wl - 2])
        elif parad_type == '16':
            stemmatized.append(''.join((string_nf[:wl - 2], 'в')))
            stemmatized.append(string_nf[:wl - 2])
    return stemmatized


'''
0 - VerbForm=Inf;Aspect=(Perf|Imp)
1 - Tense=(Pres|Fut);VerbForm=Fin;Mood=Ind;Person=1;Number=Sing;Aspect=(Perf|Imp)
2 - Tense=(Pres|Fut);VerbForm=Fin;Mood=Ind;Person=2;Number=Sing;Aspect=(Perf|Imp)
3 - Tense=(Pres|Fut);VerbForm=Fin;Mood=Ind;Person=3;Number=Sing;Aspect=(Perf|Imp)
4 - Tense=(Pres|Fut);VerbForm=Fin;Mood=Ind;Person=1;Number=Plur;Aspect=(Perf|Imp)
5 - Tense=(Pres|Fut);VerbForm=Fin;Mood=Ind;Person=2;Number=Plur;Aspect=(Perf|Imp)
6 - Tense=(Pres|Fut);VerbForm=Fin;Mood=Ind;Person=3;Number=Plur;Aspect=(Perf|Imp)
7 - Tense=Past;VerbForm=Fin;Mood=Ind;Gender=Masc;Number=Sing;Aspect=(Perf|Imp)
8 - Tense=Past;VerbForm=Fin;Mood=Ind;Gender=Fem;Number=Sing;Aspect=(Perf|Imp)
9 - Tense=Past;VerbForm=Fin;Mood=Ind;Gender=Neut;Number=Sing;Aspect=(Perf|Imp)
10 - Tense=Past;VerbForm=Fin;Mood=Ind;Number=Plur;Aspect=(Perf|Imp)
11 - VerbForm=Fin;Mood=Imp;Person=2;Number=Sing;Aspect=(Perf|Imp)
12 - VerbForm=Fin;Mood=Imp;Person=2;Number=Plur;Aspect=(Perf|Imp)
13 - VerbForm=Fin;Mood=Imp;Person=1;Number=Plur;Aspect=(Perf|Imp)
14 - Tense=Pres;VerbForm=Conv;Aspect=(Perf|Imp)
15 - Tense=Past;VerbForm=Conv;Aspect=(Perf|Imp)
16 - VerbForm=Part;Tense=Pres;Voice=Act
17 - VerbForm=Part;Tense=Pres;Voice=Pass
18 - VerbForm=Part;Tense=Past;Voice=Act
19 - VerbForm=Part;Tense=Past;Voice=Pass
'''


def def_tag_pos_verb(grammemes):
    pos = -1
    if 'VerbForm=Inf' in grammemes:
        pos = 0
    elif 'VerbForm=Fin' in grammemes:
        if 'Mood=Imp' in grammemes:
            if '2' in grammemes and 'Sing' in grammemes:
                pos = 11
            elif '2' in grammemes and 'Plur' in grammemes:
                pos = 12
            elif 'Person=1' in grammemes and 'Number=Plur' in grammemes:
                pos = 13
        else:
            if 'Past' in grammemes:
                if 'Plur' in grammemes:
                    pos = 10
                else:
                    if 'Masc' in grammemes:
                        pos = 7
                    if 'Fem' in grammemes:
                        pos = 8
                    if 'Neut' in grammemes:
                        pos = 9
            elif 'Pres' in grammemes or 'Fut' in grammemes:
                if '1' in grammemes and 'Sing' in grammemes:
                    pos = 1
                if '2' in grammemes and 'Sing' in grammemes:
                    pos = 2
                if '3' in grammemes and 'Sing' in grammemes:
                    pos = 3
                if '1' in grammemes and 'Plur' in grammemes:
                    pos = 4
                if '2' in grammemes and 'Plur' in grammemes:
                    pos = 5
                if '3' in grammemes and 'Plur' in grammemes:
                    pos = 6
    elif 'VerbForm=Conv' in grammemes:
        if 'Pres' in grammemes:
            pos = 14
        if 'Past' in grammemes:
            pos = 15
    elif 'VerbForm=Part' in grammemes:
        if 'Pres' in grammemes:
            if 'Act' in grammemes:
                pos = 16
            if 'Pass' in grammemes:
                pos = 17
        if 'Past' in grammemes:
            if 'Act' in grammemes:
                pos = 18
            if 'Pass' in grammemes:
                pos = 19
    return pos


def def_tag_pos_part(grammemes):
    pos = -1
    if 'Tense=Pres' in grammemes:
        if 'Voice=Act' in grammemes:
            pos = 16
        elif 'Voice=Pass' in grammemes:
            pos = 17
    elif 'Tense=Past' in grammemes:
        if 'Voice=Act' in grammemes:
            pos = 18
        elif 'Voice=Pass' in grammemes:
            pos = 19
    return pos


def transform_prefix(word_form, prefix):
    consonants = ['б', 'в', 'г', 'д', 'ж', 'з', 'й', 'к', 'л', 'м', 'н',
                  'п', 'р', 'с', 'т', 'ф', 'х', 'ц', 'ч', 'ш', 'щ']
    vowels = ['а', 'о', 'у', 'ы', 'э', 'я', 'ё', 'ю', 'и', 'е']
    map_prefix = {
        'в': 'во',
        'вс': 'взо',
        'вз': 'взо',
        'ис': 'изо',
        'из': 'изо',
        'над': 'надо',
        'о': 'обо',
        'об': 'обо',
        'от': 'ото',
        'под': 'подо',
        'рас': 'разо',
        'раз': 'разо',
        'с': 'со'
    }
    if prefix:
        # добавление огласовки, если выпала беглая гласная (кроме "брать", "есть", "идти", "стать")
        if word_form[:2] not in ['бр', 'ес', 'ид', 'ст'] and word_form[1] not in vowels:
            if prefix in map_prefix.keys():
                return map_prefix[prefix] + word_form
        # удаление огласовки, если вставлена беглая гласная (кроме "брать", "шел", "шедший")
        elif word_form[:3] not in ['бер', 'ним', 'шед', 'шел'] and word_form[1] in vowels:
            if len(prefix) > 1 and prefix in map_prefix.values() and prefix[-3:] != 'про':
                return prefix[:-1] + word_form
        if word_form[:2] == 'ид':
            word_form = word_form.replace('идти', 'йти')
            if prefix[-1] != 'и':
                word_form = word_form.replace('ид', 'йд')
            elif word_form != 'йти':
                word_form = word_form[1:]
        elif word_form[:3] == 'ним':
            if prefix[-1] in vowels:
                if prefix[-1] == 'и':
                    word_form = word_form[2:]
                else:
                    word_form = 'й' + word_form[2:]
    return prefix + word_form


def generate_verb_wf(parad_type, stemmatized, prefix, postfix, gram_pos, grammemes, word_form, found_dict, form_accept, debug=False):
    if form_accept:
        if found_dict and len(word_form) > 0:
            word_form = transform_prefix(word_form, prefix)
            word_form = end_postfix(word_form, postfix)
            if debug:
                print('\tgram_pos=\t' + str(gram_pos) + '\t\tgrammemes=\t' + str(grammemes) + '\n' + '\tstemmatized=\t'
                      + str(stemmatized))
                print('\tFound WF in dict: ' + str(word_form))
        elif parad_type:
            word_form = find_verb_form(parad_type, stemmatized, gram_pos, postfix)
            if debug:
                print('\tgram_pos=\t' + str(gram_pos) + '\t\tgrammemes=\t' + str(grammemes) + '\n' + '\tstemmatized=\t'
                      + str([x.replace('|', '') for x in stemmatized]) + '\t\tdecl_type=\t' + str(parad_type))
                print('\tFound Verb WF in lemmas: ' + word_form)
    else:
        word_form = 'Verb Not Found'
    return word_form
