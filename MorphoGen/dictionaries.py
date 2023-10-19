from collections import defaultdict

from MorphoGen.trie import find_suffix


def read_gpron(inp_file):
    with open(inp_file, 'r', encoding='utf-8') as f:
        my_strings = f.readlines()
    mdict = []
    mword = []
    for l in my_strings:
        if l.find(' ') and len(l) > 1:
            mword.append(l.strip().split(' '))
        elif len(mword) >= 1 and len(mword[0]) >= 1:
            mdict.append(mword)
            mword = []
    return mdict


def read_lemmas_and_proper(file_lemmas, file_proper=None):
    lemmas_dict = defaultdict(list)
    with open(file_lemmas, 'r', encoding='utf-8') as f:
        lemmas_list = [line.strip() for line in f.readlines()]
    if file_proper is not None:
        with open(file_proper, 'r', encoding='utf-8') as f:
            proper_list = [line.strip() for line in f.readlines()]
    else:
        proper_list = []

    for lemma_line in lemmas_list + proper_list:
        lemma_line_split = lemma_line.split(';')
        if len(lemma_line_split) != 2:
            print('Error in dictionary files, 2 fields separated by ";" expected: {}'.format(lemma_line))
            exit(0)
        lemmas_dict[lemma_line_split[0]].append(lemma_line_split[1])
    return lemmas_dict


def read_file_to_list(input_file):
    with open(input_file, 'r', encoding='utf-8') as infile:
        file_list = [line.strip() for line in infile.readlines()]
    return file_list


def search_tags_dict(arr, lemma_value, grammemes):
    # TODO: переписать search_tags_dict, чтобы было прозрачнее
    norm_form = 'Not Found'
    word_form = []
    found_dict = False
    for i in range(len(arr)):
        ind_dict = -1
        if lemma_value == arr[i][0][0]:  # arr[i] = [['драть', '(VerbForm=Inf;Aspect=Imp)'], [...], ...]
            norm_form = arr[i][0][0]
            ind_dict = i
        if ind_dict >= 0:
            for k in range(len(arr[ind_dict])):  # по элементам нужной "словарной статьи"
                ind_wf = arr[ind_dict].index(arr[ind_dict][k])  # ind_wf = k ???
                for m in range(1, len(arr[ind_dict][k])):  # по тегам внутри одной словоформы (строки GPron)
                    num = 0
                    for g in grammemes.split(';'):
                        if g in arr[ind_dict][k][m]:
                            num += 1
                        if num == len(grammemes.split(';')) and num > 0:
                            word_form.append(arr[ind_dict][ind_wf][0])
                            found_dict = True
                            break
    if word_form:
        return word_form[0], norm_form, found_dict
    else:
        return '', norm_form, found_dict


def parad_type_from_lemmas(string_nf, pos, lemmes_dict):
    parad_type_variants = []
    if string_nf in lemmes_dict.keys():
        parad_type_variants = lemmes_dict[string_nf.lower()]
    if pos == 'NOUN':
        parad = ''
        noun_parad_types = ['1то', '1тв', '1мо', '1мв', '1мо*', '1мв*', '2то', '2тв', '2тоа', '2тва', '2йо', '2йв',
                            '2мо', '2мв', '2моа', '2мва', '2тос', '2твс', '2твс+о', '2твс+', '2мос', '2мвс', '3о',
                            '3в', '4о', '4в', '4ос', '4вс', '2тоь', '2твь', '2то-', '2тв-', '2мо-', '2мв-', '1то+о',
                            '1тв+о', '1то+', '1тв+', '1мо+', '1мв+', 'льня', '2цв+', '2тсь', '4вс+', '2моь', '5', '6',
                            '7', 'отчм', 'фм', 'фж', '11о', '11в', '11в+']
        if parad_type_variants:
            for parad_type in parad_type_variants:
                if parad_type.endswith('.един'):
                    parad_type = parad_type.strip()[:-5]
                    tantum = 'sing'
                elif parad_type.endswith('.множ'):
                    parad_type = parad_type.strip()[:-5]
                    tantum = 'plur'
                else:
                    parad_type = parad_type.strip()
                    tantum = 'both'
                if parad_type.replace('.един', '').replace('.множ', '') in noun_parad_types:
                    parad = parad_type
        return parad, tantum
    elif pos in 'VERB':
        parad, aspect, trans = '', '', ''
        if parad_type_variants:
            for parad_type in parad_type_variants:
                if len(parad_type.split('-')) == 3:
                    parad, aspect, trans = parad_type.split('-')
        return parad, aspect, trans
    else:
        print(string_nf, pos, '- not found in lemmas')


def if_substring(lemmes_dict, string_nf, pos, lemmes_trie):
    wl = len(string_nf)
    curr_end = ''
    node = lemmes_trie
    for i in range(wl, -1, -1):
        curr_end = string_nf[wl - i::]
        found, node = find_suffix(lemmes_trie, curr_end)
        if found:
            if i == 0:
                return ''
            break

    while len(node.children) != 0:
        node = node.children[sorted(node.children.keys())[0]]
        curr_end = node.char + curr_end

    return parad_type_from_lemmas(curr_end, pos, lemmes_dict)
