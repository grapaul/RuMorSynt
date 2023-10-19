import re
from MorphoGen.morphon import *
from MorphoGen.parads import find_adj_form


def guess_adj_stem(string_nf):
    stemmatized = []
    parad_type = ''
    wl = len(string_nf)
    stemmatized.append("".join((string_nf[:wl - 2])))
    if string_nf.rfind('ов') == wl - 2 or string_nf.rfind('ев') == wl - 2 or string_nf.rfind('ин') == wl - 2 or string_nf.rfind('ын') == wl - 2:
        stemmatized.append("".join(string_nf))
    if not if_vowel(string_nf, 4) and wl > 4:
        if if_soft(string_nf, 4):
            stemmatized.append("".join((string_nf[:wl - 4], 'е', string_nf[wl - 3])))
        elif string_nf == "полный" or string_nf == "неполный" or string_nf == "смешной" or string_nf == "несмешной":
            stemmatized.append("".join((string_nf[:wl - 3], 'о', string_nf[wl - 3])))
        elif not if_soft(string_nf, 4) and if_n(string_nf, 3):
            if if_j(string_nf, 4):
                stemmatized.append("".join((string_nf[:wl - 4], 'е', string_nf[wl - 3])))
            else:
                stemmatized.append("".join((string_nf[:wl - 3], 'е', string_nf[wl - 3])))
        elif not if_soft(string_nf, 4) and if_k(string_nf, 3):
            stemmatized.append("".join((string_nf[:wl - 3], 'о', string_nf[wl - 3])))

    if string_nf.rfind('ый') == wl - 2 and wl > 3:
        parad_type = 'adj_y'
    elif string_nf.rfind('ий') == wl - 2 and if_kgx(string_nf, 3) and wl > 3:
        parad_type = 'adj_y_soft_velar'
    elif string_nf.rfind('ий') == wl - 2 and not if_kgx(string_nf, 3) and wl > 3 and adj_possess(string_nf):
        parad_type = 'adj_y_soft_possess'
    elif string_nf.rfind('ий') == wl - 2 and not if_kgx(string_nf, 3) and wl > 3:
        parad_type = 'adj_y_soft'
    elif string_nf.rfind('ой') == wl - 2 and wl > 3:
        parad_type = 'adj_y_o'
    elif string_nf.rfind('ов') == wl - 2 or string_nf.rfind('ев') == wl - 2 or string_nf.rfind('ин') == wl - 2 or string_nf.rfind('ын') == wl - 2:
        parad_type = 'adj_possess'

    #    if parad_type:
    #        print('Предположено прилагательное\t'+ parad_type + ';\tоснова\t' + str(stemmatized))
    return (parad_type, stemmatized)


def def_tag_pos_adj(grammemes):
    pos = -1
    cases = {
        '=Nom': 0,
        '=Gen': 1,
        '=Acc': 2,
        '=Dat': 3,
        '=Ins': 4,
        '=Loc': 5
    }

    # выделяем падеж из grammemes
    case = re.findall('(=Nom|=Gen|=Acc|=Dat|=Ins|=Loc)', grammemes)
    if len(case) > 0:
        case = case[0]
    elif 'Cmp' not in grammemes and 'Short' not in grammemes:
        return pos

    # находим соответствующий pos
    if 'Short' in grammemes:
        if 'Masc' in grammemes and 'Sing' in grammemes:
            pos = 24
        elif 'Fem' in grammemes and 'Sing' in grammemes:
            pos = 25
        elif 'Neut' in grammemes and 'Sing' in grammemes:
            pos = 26
        elif 'Plur' in grammemes:
            pos = 27

    elif 'Sing' in grammemes:
        if 'Masc' in grammemes:
            pos = 0 + cases[case]
        elif 'Fem' in grammemes:
            pos = 6 + cases[case]
        elif 'Neut' in grammemes:
            pos = 12 + cases[case]

    elif 'Plur' in grammemes and 'Gender' not in grammemes:
        pos = 18 + cases[case]

    elif 'Cmp' in grammemes:
        pos = 28

    return pos


def generate_adj_wf(gram_pos, grammemes, parad_type_adj, stemmatized_adj, debug=False):
    if debug:
        print('\tgram_pos=\t' + str(gram_pos))

    word_form = find_adj_form(parad_type_adj, stemmatized_adj, gram_pos, grammemes)

    if debug:
        print('\tparad_type_adj=\t' + parad_type_adj + '\tstemmatized_adj=\t' + str(stemmatized_adj))
        print('\tFound adj WFs: ' + word_form)

    return word_form


def generate_adj_wf_silent(grammemes, parad_type_adj, stemmatized_adj):
    gram_pos = def_tag_pos_adj(grammemes)
    word_form = find_adj_form(parad_type_adj, stemmatized_adj, gram_pos, grammemes)
    return word_form
