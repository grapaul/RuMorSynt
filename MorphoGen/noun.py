import re

from MorphoGen.parads import find_form
from MorphoGen.morphon import *
from MorphoGen.dictionaries import search_tags_dict, parad_type_from_lemmas, if_substring

lemmes_trie = None


def throw_prefix(lemmes_dict, string_nf):
    parad_type, tantum = '', ''
    prefixes = [
        'авиа', 'авто', 'агро', 'аква', 'анти', 'аэро', 'био', 'вибро', 'видео', 'водо', 'газо', 'гидро', 'гипер',
        'гос', 'кино', 'контр', 'макро', 'мета', 'микро', 'моно', 'мото', 'не', 'орг', 'пара', 'поли', 'полу',
        'радио', 'спец', 'стерео', 'суб', 'супер', 'теле', 'тепло', 'термо', 'фото', 'электро'
    ]
    for prefix in prefixes:
        if string_nf.startswith(prefix):
            if string_nf[len(prefix) - 1:].lower() in lemmes_dict:
                parad_type, tantum = parad_type_from_lemmas(string_nf[len(prefix) - 1:].lower(), 'NOUN', lemmes_dict)
    return parad_type, tantum


def define_parad_type(dict_p, string_nf, gram_list, lemmes_dict, lemmes_trie):
    w_form, n_form, found_dict = search_tags_dict(dict_p, string_nf, gram_list)
    parad_type = ''
    noun_types = ['1то', '1тв', '1мо', '1мв', '1мо*', '1мв*', '2то', '2тв', '2тоа', '2тва', '2йо', '2йв', '2мо', '2мв',
                  '2моа','2мва', '2тос', '2твс', '2твс+о', '2твс+', '2мос', '2мвс', '3о', '3в', '4о', '4в', '4ос',
                  '4вс', '2тоь', '2твь', '2то-', '2тв-', '2мо-', '2мв-', '1то+о', '1тв+о', '1то+', '1тв+', '1мо+',
                  '1мв+', 'льня', '2цв+', '2тсь', '4вс+', '2моь', '5', '6', '7', 'отчм', 'фм', 'фж']
    # TODO: убрать двойную проверку на noun_types – оставить здесь или в parad_type_from_lemmas

    if string_nf.lower() in lemmes_dict:
        parad_type, tantum = parad_type_from_lemmas(string_nf.lower(), 'NOUN', lemmes_dict)
    if parad_type == '':
        parad_type = guess_parad_by_suff(string_nf)
        tantum = 'both'
    if parad_type == '':
        parad_type, tantum = throw_prefix(lemmes_dict, string_nf)
    if parad_type == '' and not string_nf.endswith('ий') and not string_nf.endswith('ый') and not string_nf.endswith('ой'):
        parad_type, tantum = if_substring(lemmes_dict, string_nf, 'NOUN', lemmes_trie)
    if parad_type.replace('.един', '').replace('.множ', '') not in noun_types:
        parad_type = ''
    return w_form, found_dict, parad_type, tantum


def stemmatize(string_nf, parad_type):
    wl = len(string_nf)
    stemmatized = []
    if parad_type in ['1то', '1тв', '1мо', '1мв', '1мо*', '1мв*', '2йо', '2йв', '2мо', '2мв', '2моа', '2мва',
                      '2тос', '2твс', '2мос', '2мвс', '2тсь', '3о', '3в', '4о', '4в', '4ос', '4вс', 'фж']:
        stemmatized.append("".join((string_nf[:wl - 1])))
    elif parad_type in ['2то', '2тв', '2тоь', '2твь', '2тоа', '2тва', 'фм']:
        stemmatized.append(string_nf)
    elif parad_type in ['2мо-', '2мв-']:
        stemmatized.append("".join((string_nf[:wl - 3], string_nf[wl - 2:wl - 1])))
        stemmatized.append(string_nf[:wl - 1])
    elif parad_type in ['2то-', '2тв-']:  # пока первый if только для -ек
        if if_kgx(string_nf, 1) and if_e(string_nf, 2) and if_ch(string_nf, 3):
            stemmatized.append("".join((string_nf[:wl - 2], string_nf[wl - 1:])))
        elif if_kgx(string_nf, 1) and if_e(string_nf, 2):
            stemmatized.append("".join((string_nf[:wl - 2], 'ь', string_nf[wl - 1:])))
        elif if_c(string_nf, 1) and if_e(string_nf, 2) and if_vowel(string_nf, 3):
            stemmatized.append("".join((string_nf[:wl - 2], 'й', string_nf[wl - 1:])))
        elif string_nf.endswith('лец'):
            stemmatized.append("".join((string_nf[:wl - 2], 'ь', string_nf[wl - 1:])))
        else:
            stemmatized.append("".join((string_nf[:wl - 2], string_nf[wl - 1:])))
        stemmatized.append(string_nf)

    elif parad_type in ['1то+о', '1тв+о']:
        stemmatized.append("".join((string_nf[:wl - 1])))
        if if_vowel(string_nf, 3):
            stemmatized.append("".join((string_nf[:wl - 1])))
        elif (if_sibil(string_nf, 3) or if_ch(string_nf, 3) or (if_c(string_nf, 2))) and not string_nf.endswith('на'):
            stemmatized.append("".join((string_nf[:wl - 2], 'е', string_nf[wl - 2:wl - 1])))
        elif if_soft(string_nf, 3) or if_j(string_nf, 3):
            stemmatized.append("".join((string_nf[:wl - 3], 'е', string_nf[wl - 2:wl - 1])))
        elif (not if_sibil(string_nf, 3)) and string_nf.endswith('на'):
            stemmatized.append("".join((string_nf[:wl - 2], 'е', string_nf[wl - 2:wl - 1])))
        else:
            stemmatized.append("".join((string_nf[:wl - 2], 'о', string_nf[wl - 2:wl - 1])))

    elif parad_type in ['1то+', '1тв+']:
        stemmatized.append("".join((string_nf[:wl - 1])))
        if if_soft(string_nf, 3):
            stemmatized.append("".join((string_nf[:wl - 3], 'е', string_nf[wl - 2:wl - 1])))
        else:
            stemmatized.append("".join((string_nf[:wl - 2], 'е', string_nf[wl - 2:wl - 1])))

    elif parad_type == '2твс+о':
        stemmatized.append("".join((string_nf[:wl - 1])))
        stemmatized.append("".join((string_nf[:wl - 2], 'о', string_nf[wl - 2:wl - 1])))

    elif parad_type == '2твс+':
        stemmatized.append("".join((string_nf[:wl - 1])))
        if if_soft(string_nf, 3):
            stemmatized.append("".join((string_nf[:wl - 3], 'е', string_nf[wl - 2:wl - 1])))
        elif if_j(string_nf, 3):
            stemmatized.append("".join((string_nf[:wl - 3], 'и', string_nf[wl - 2:wl - 1])))
        else:
            stemmatized.append("".join((string_nf[:wl - 2], 'е', string_nf[wl - 2:wl - 1])))

    elif parad_type == '1мо+':
        stemmatized.append("".join((string_nf[:wl - 1])))
        if if_l(string_nf, 2):
            stemmatized.append("".join((string_nf[:wl - 2], 'е', string_nf[wl - 2:wl - 1], 'ь')))
        else:
            stemmatized.append("".join((string_nf[:wl - 2], 'е', string_nf[wl - 2:wl - 1])))
    elif parad_type in ['льня', '1мв+']:
        stemmatized.append("".join((string_nf[:wl - 1])))
        if if_l(string_nf, 2) or (if_n(string_nf, 2) and not if_soft(string_nf, 3) and not if_j(string_nf, 3)):
            stemmatized.append("".join((string_nf[:wl - 2], 'е', string_nf[wl - 2:wl - 1], 'ь')))
        else:
            stemmatized.append("".join((string_nf[:wl - 3], 'е', string_nf[wl - 2:wl - 1])))
    elif parad_type == '2цв+':
        stemmatized.append("".join((string_nf[:wl - 1])))
        if string_nf.endswith('ице'):
            stemmatized.append("".join((string_nf[:wl - 3], 'и', string_nf[wl - 2:wl - 1])))
        elif if_c(string_nf, 2) and not if_soft(string_nf, 3):
            stemmatized.append("".join((string_nf[:wl - 2], 'е', string_nf[wl - 2:wl - 1])))
        else:
            stemmatized.append("".join((string_nf[:wl - 3], 'е', string_nf[wl - 2:wl - 1])))
    elif parad_type in ['4вс+', '7']:
        stemmatized.append("".join((string_nf[:wl - 1])))
        stemmatized.append("".join((string_nf[:wl - 2])))
    elif parad_type == '2моь':
        stemmatized.append("".join((string_nf[:wl - 1])))
        stemmatized.append(string_nf)
    elif parad_type in ['4в', '11о']:
        stemmatized.append("".join((string_nf[:wl - 1])))
    elif parad_type == '5':
        stemmatized.append("".join((string_nf[:wl - 2], string_nf[wl - 1:])))
        stemmatized.append(string_nf)
        stemmatized.append("".join((string_nf[:wl - 4], 'ят')))
    elif parad_type == '6':
        stemmatized.append(string_nf)
        stemmatized.append("".join((string_nf[:wl - 2])))
    elif parad_type == 'отчм':
        stemmatized.append(string_nf)
    elif parad_type == '11в':
        stemmatized.append("".join((string_nf[:wl - 1])))
        if if_k(string_nf, 2) and not if_vowel(string_nf, 3):
            stemmatized.append("".join((string_nf[:wl - 2], 'о', string_nf[wl - 2:wl - 1])))
    elif parad_type == '11в+':
        stemmatized.append("".join((string_nf[:wl - 1])))
        stemmatized.append("".join((string_nf[:wl - 2], 'е', string_nf[wl - 2:wl - 1])))

    return stemmatized


def guess_parad_by_suff(string_nf):
    parad_type = ''
    wl = len(string_nf)
    ###женский род  ###

    if string_nf.endswith('ия'):
        parad_type = '4в'

    elif string_nf.endswith('ья'):
        parad_type = '7'

    elif string_nf.endswith('льня') or string_nf.endswith('рня'):
        parad_type = 'льня'

    elif string_nf.endswith('ость'):
        parad_type = '3в'

    ### мужской род ###

    elif string_nf.endswith('енок') and wl > 5 \
            and string_nf not in ['валенок', 'застенок', 'кленок', 'оттенок', 'подстенок',
                                                               'простенок', 'расценок', 'хренок', 'черенок']:
        parad_type = '5'

    elif string_nf.endswith('ин'):
        parad_type = '6'

    elif string_nf.endswith('ист') or string_nf.endswith('фил') or string_nf.endswith('фоб') or \
            string_nf.endswith('олог') and string_nf not in ['каталог', 'некролог', 'диалог', 'монолог',
                                                         'эпилог', 'полог', 'пролог']:
        parad_type = '2то'

    elif string_nf.endswith('изм') or string_nf.endswith('инг') or string_nf.endswith('метр') or \
            string_nf.endswith('скоп'):
        parad_type = '2тв'

    #    elif string_nf.find('лец') == wl - 3: #потом оставить здесь, пока в cut_stem '2то-'
    #        parad_type = '2то-'

    ### средний род ###

    elif string_nf.endswith('ие'):
        parad_type = '4вс'

    elif string_nf.endswith('ство'):
        parad_type = '2твс'

    ### имена собственные ###

    elif string_nf.endswith('ич'):
        parad_type = 'отчм'

    elif string_nf.endswith('вна') or string_nf.endswith('чна') or string_nf.endswith('шна'):
        parad_type = '1то'

    return parad_type


def def_tag_pos_noun(grammemes):
    cases = {
        'Nom': 0,
        'Gen': 1,
        'Acc': 2,
        'Dat': 3,
        'Ins': 4,
        'Loc': 5
    }
    numbers = {
        'Sing': 0,
        'Plur': 6
    }
    case = re.findall('(Nom|Gen|Acc|Dat|Ins|Loc)', grammemes.replace('Gender', ''))
    number = re.findall('(Sing|Plur)', grammemes)
    if len(case) > 0 and len(number) > 0:
        case = case[0]
        number = number[0]
        if case in cases and number in numbers:
            return cases[case] + numbers[number]
    return -1


def generate_wf(found_dict, word_form, parad_type, tantum, grammemes, stemmatized, lemma_value, const_list, gram_pos, debug=False):
    if tantum == 'sing' and gram_pos > 5:
        gram_pos -= 6
    elif tantum == 'plur' and gram_pos < 6:
        gram_pos += 6
    if found_dict and len(word_form) > 0:
        if debug:
            print(
                '\tgram_pos=\t' + str(gram_pos) + '\t\tgrammemes=\t' + str(grammemes) + '\n' + '\tstemmatized=\t'
                + str(stemmatized))
            print('\tFound WF in dict: ' + str(word_form))
    elif lemma_value in const_list:
        word_form = lemma_value
        if debug:
            print(
                '\tgram_pos=\t' + str(gram_pos) + '\t\tgrammemes=\t' + str(
                        grammemes) + '\n' + '\tstemmatized=\t' + str(
                        stemmatized))
            print('\tFound WF in constants: ' + lemma_value)
    elif parad_type:
        word_form = find_form(parad_type, stemmatized, gram_pos, lemma_value)
        if debug:
            print(
                '\tgram_pos=\t' + str(gram_pos) + '\t\tgrammemes=\t' + str(grammemes) + '\n' + '\tstemmatized=\t'
                + str(stemmatized) + '\t\tdecl_type=\t' + str((parad_type + '/' + tantum).replace('/both', '')))
            print('\tFound WF in lemmas: ' + word_form)

    return word_form
