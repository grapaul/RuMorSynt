import pymorphy2
import os

from MultiFlex.num_list import *
from MultiFlex.t_soft_noun import *
from MultiFlex.ti_verb import *
from MultiFlex.get_number import *
from MorphoGen import GenMorphApi


g = GenMorphApi()
morph = pymorphy2.MorphAnalyzer()


def find_pos(wf):
    if wf in num_list:
        pos = 'NUM'
    elif (wf.find('ся') != -1 and wf.find('ся') == len(wf) - 2) or (wf.find('ть') != -1 and wf.find('ть') == len(wf) - 2 and wf not in t_soft_noun) or (wf in ti_verb):
        pos = 'VERB'
    elif wf[-2:] in ['ый', 'ий', 'ий', 'ой']:
        pos = 'ADJ'
    else:
        pos = 'NOUN'
    return pos


def correct_quant_noun(wf):
    if wf in ['тысячи', 'тысяч']:
        wf = 'тысяча'
    elif wf in ['миллиона', 'миллионов']:
        wf = 'миллион'
    elif wf in ['миллиарда', 'миллиардов']:
        wf = 'миллиард'
    elif wf in ['триллиона', 'триллионов']:
        wf = 'триллион'
    elif wf in ['биллиона', 'биллионов']:
        wf = 'биллион'
    return wf


def modify_fraction(wf):
    ord_nom_masc = ['первый', 'второй', 'третий', 'четвертый', 'пятый', 'шестой', 'седьмой', 'восьмой', 'девятый',
                    'десятый', 'одиннадцатый', 'двенадцатый', 'тринадцатый', 'четырнадцатый', 'пятнадцатый',
                    'шестнадцатый', 'семнадцатый', 'восемнадцатый', 'девятнадцатый', 'двадцатый', 'тридцатый',
                    'сороковой', 'пятидесятый', 'шестидесятый', 'семидесятый', 'восьмидесятый', 'девяностый', 'сотый',
                    'двухсотый', 'трехсотый', 'четырехсотый', 'пятисотый', 'шестисотый', 'семисотый', 'восьмисотый',
                    'девятисотый']
    ord_nom_fem = ['первая', 'вторая', 'третья', 'четвертая', 'пятая', 'шестая', 'седьмая', 'восьмая', 'девятая',
                   'десятая', 'одиннадцатая', 'двенадцатая', 'тринадцатая', 'четырнадцатая', 'пятнадцатая',
                   'шестнадцатая', 'семнадцатая', 'восемнадцатая', 'девятнадцатая', 'двадцатая', 'тридцатая',
                   'сороковая', 'пятидесятая', 'шестидесятая', 'семидесятая', 'восьмидесятая', 'девяностая', 'сотая',
                   'двухсотая', 'трехсотая', 'четырехсотая', 'пятисотая', 'шестисотая', 'семисотая', 'восьмисотая',
                   'девятисотая']
    ord_gen = ['первых', 'вторых', 'третьих', 'четвертых', 'пятых', 'шестых', 'седьмых', 'восьмых', 'девятых',
               'десятых', 'одиннадцатых', 'двенадцатых', 'тринадцатых', 'четырнадцатых', 'пятнадцатых', 'шестнадцатых',
               'семнадцатых', 'восемнадцатых', 'девятнадцатых', 'двадцатых', 'тридцатых', 'сороковых', 'пятидесятых',
               'шестидесятых', 'семидесятых', 'восьмидесятых', 'девяностых', 'сотых', 'двухсотых', 'трехсотых',
               'четырехсотых', 'пятисотых', 'шестисотых', 'семисотых', 'восьмисотых', 'девятисотых']
    ord_nom_pl = ['первые', 'вторые', 'третьи', 'четвертые', 'пятые', 'шестые', 'седьмые', 'восьмые', 'девятые',
                   'десятые', 'одиннадцатые', 'двенадцатые', 'тринадцатые', 'четырнадцатые', 'пятнадцатые',
                   'шестнадцатые', 'семнадцатые', 'восемнадцатые', 'девятнадцатые', 'двадцатые', 'тридцатые',
                   'сороковые', 'пятидесятые', 'шестидесятые', 'семидесятые', 'восьмидесятые', 'девяностые', 'сотые',
                   'двухсотые', 'трехсотые', 'четырехсотые', 'пятисотые', 'шестисотые', 'семисотые', 'восьмисотые',
                   'девятисотые']

    for o in ord_nom_fem:
        if wf == o:
            wf = ord_nom_masc[ord_nom_fem.index(o)]
    for o in ord_gen:
        if wf == o:
            wf = ord_nom_masc[ord_gen.index(o)]

    if wf == 'целая' or wf == 'целых':
        wf = 'целый'
    return wf

def find_animacy(lemma):
    an = 'Inan'
    with open(os.path.join(os.path.dirname(__file__), 'lemmas4animacy.txt'), 'r', encoding='utf-8') as f:
        my_strings = f.readlines()
    lemma_anim = []
    for l in my_strings:
        lemma_anim.append(l.split(';')[0])
    if lemma in lemma_anim:
        an = 'Anim'
    return an

def correct_ord_nump(i, pos_all, list_of_taglists, wf_list):
    for n in range(0, i):
        if ('Pos=NUM' in list_of_taglists[n]):
            list_of_taglists[n] = {'Pos=NUM', 'Case=Nom'}
        elif ('Pos=NOUN' in list_of_taglists[n]):
            list_of_taglists[n] = {'Pos=NOUN', 'Case=Nom'}

    return list_of_taglists


def correct_nump(i, pos_all, list_of_taglists, wf_list):
    gender = ['Masc', 'Fem', 'Neut']
    number = ['Sing', 'Plur']
    case = ['Nom', 'Acc', 'Gen', 'Dat', 'Ins', 'Loc']

    n_pos = pos_all[i:].index('NOUN') + i if 'NOUN' in pos_all[i:] else i
    taglist = list_of_taglists[n_pos]

    last_num = i
    for l in range(i, n_pos):
        if 'NUM' == pos_all[l]:
            last_num = l

    wf_num = wf_list[last_num]

    if n_pos > i and wf_list[n_pos] == modify_fraction(wf_list[n_pos]):
        if wf_num not in ['один', 'одна', 'два', 'две', 'три', 'четыре']:
            taglist.discard('Number=Sing')
            taglist.add('Number=Plur')
            for c in case:
                if ('Case=' + c) in taglist and c in ['Nom', 'Acc']:
                    taglist.remove('Case=' + c)
                    taglist.add('Case=Gen')
        elif wf_num in ['два', 'две', 'три', 'четыре']:
            p = morph.parse(correct_quant_noun(wf_list[n_pos]))[0]
            for c in case:
                if (('Case=' + c) in taglist) and ((c == 'Nom') or (c == 'Acc' and ('inan' in p.tag and find_animacy(wf_list[n_pos]) == 'Inan'))):
                    taglist.remove('Case=' + c)
                    taglist.add('Case=Gen_count')
                    if ('Number=Plur') in taglist:
                        taglist.remove('Number=Plur')
                    taglist.add('Number=Sing')

                elif ('Case=' + c) in taglist and ((c in ['Gen', 'Dat', 'Ins', 'Loc']) or (c == 'Acc' and ('anim' in p.tag or 'ANim' in p.tag)) or (find_animacy(wf_list[n_pos]) == 'Anim')):
                    if ('Number=Sing') in taglist:
                        taglist.remove('Number=Sing')
                    taglist.add('Number=Plur')
            if 'Case=Gen_count' in taglist:
                taglist.remove('Case=Gen_count')
                taglist.add('Case=Gen')

        list_of_taglists[n_pos] = taglist

    return list_of_taglists


def correct_fraction(i, k, list_of_taglists, wf_list):
    gender = ['Masc', 'Fem', 'Neut']
    case = ['Nom', 'Acc', 'Gen', 'Dat', 'Ins', 'Loc']

    list_of_taglists[i].discard('Pos=NOUN')
    list_of_taglists[i].add('Pos=ADJ')

    if wf_list[i][-1:] == 'х':
        list_of_taglists[i].discard('Number=Sing')
        list_of_taglists[i].add('Number=Plur')
        list_of_taglists[i].add('Gender=Fem')
        if 'Case=Nom' in list_of_taglists[i] or 'Case=Acc' in list_of_taglists[i]:
            for c in ['Nom', 'Acc']:
                list_of_taglists[i].discard("Case=" + c)
            list_of_taglists[i].add('Case=Gen')

    elif wf_list[i][-1:] == 'я':
        list_of_taglists[i].discard('Number=Plur')
        list_of_taglists[i].add('Number=Sing')
        list_of_taglists[i].add('Gender=Fem')

#    print('num0=\t\t', str(wf_list[i]))
#    print('taglist0=\t', str(taglist))
#    print('wf0=\t\t', str(wf_list[n_pos]))

    l = i - 1
    while find_pos(wf_list[l]) == 'NUM' and l >= k:
        for c in case:
            list_of_taglists[l].discard('Case=' + c)
        list_of_taglists[l].add('Case=Nom')
        l = l - 1

    while find_pos(wf_list[l]) == 'NUM' and l >= 0:
        if wf_list[l] in ['один', 'одна', 'два', 'две']:
            for g in gender:
                list_of_taglists[l].discard("Gender=" + g)
            list_of_taglists[l].add('Gender=Fem')
        l = l - 1

    wf_list[i] = modify_fraction(wf_list[i])
    return list_of_taglists


def correct_np(i, pos_all, list_of_taglists, wf_list):
    animacy = ['Anim', 'Inan']
    gender = ['Masc', 'Fem', 'Neut']
    number = ['Sing', 'Plur']
    case = ['Nom', 'Acc', 'Gen', 'Dat', 'Ins', 'Loc']

    n_pos = pos_all[i:].index('NOUN') + i if 'NOUN' in pos_all[i:] else i
    p = morph.parse(correct_quant_noun(wf_list[n_pos]))[0]
    taglist = list_of_taglists[n_pos] if n_pos > i else list_of_taglists[i]

    if n_pos > i and 'NOUN' in p.tag:
        for g in gender:
            if ('Gender=' + g) in taglist and ('Gender=' + g) in list_of_taglists[i]:
                list_of_taglists[i].remove('Gender=' + g)
        if 'masc' in p.tag:
            list_of_taglists[i].add('Gender=Masc')
        elif 'femn' in p.tag:
            list_of_taglists[i].add('Gender=Fem')
        elif 'neut' in p.tag:
            list_of_taglists[i].add('Gender=Neut')
        for a in animacy:
            list_of_taglists[i].discard('Animacy=' + a)
        if ('anim' in p.tag or 'ANim' in p.tag or find_animacy(wf_list[n_pos]) == 'Anim') and 'Case=Acc' in list_of_taglists[i]:
            list_of_taglists[i].add('Animacy=Anim')
        elif 'inan' in p.tag and 'Case=Acc' in list_of_taglists[i]:
            list_of_taglists[i].add('Animacy=Inan')
        for c in case:
            list_of_taglists[i].discard('Case=' + c)
            if ('Case=' + c) in list_of_taglists[n_pos]:
                list_of_taglists[i].add('Case=' + c)

        if wf_list[i] == 'один':
                list_of_taglists[i].add('Number=Sing')
        elif 'два' in wf_list[:i]:
                list_of_taglists[i].add('Number=Plur')
        else:
            list_of_taglists[i].discard('Number=Sing')
            list_of_taglists[i].discard('Number=Plur')
            for n in number:
                if ('Number=' + n) in list_of_taglists[n_pos]:
                    list_of_taglists[i].add('Number=' + n)

    return list_of_taglists


def correct_twop(i, pos_all, list_of_taglists, wf_list):
    animacy = ['Anim', 'Inan']
    gender = ['Masc', 'Fem', 'Neut']

    n_pos = pos_all[i:].index('NOUN') + i if 'NOUN' in pos_all[i:] else i
    p = morph.parse(correct_quant_noun(wf_list[n_pos]))[0]
    taglist = list_of_taglists[n_pos] if n_pos > i else list_of_taglists[i]
    for g in gender: # ('Gender=' + g) in taglist  and ('Gender=' + g) in list_of_taglists[i]
        if (pos_all[n_pos] == 'NOUN' or 'NOUN' in p.tag):
            if 'masc' in p.tag and 'Gender=Masc' not in taglist:
                list_of_taglists[i].discard('Gender=' + g)
                list_of_taglists[i].add('Gender=Masc')
            elif 'femn' in p.tag and 'Gender=Fem' not in taglist:
                list_of_taglists[i].discard('Gender=' + g)
                list_of_taglists[i].add('Gender=Fem')
            elif 'neut' in p.tag and 'Gender=Neut' not in taglist:
                list_of_taglists[i].discard('Gender=' + g)
                list_of_taglists[i].add('Gender=Neut')

    for a in animacy:
        list_of_taglists[i].discard('Animacy=' + a)
    if ('anim' in p.tag  or 'ANim' in p.tag or find_animacy(wf_list[n_pos]) == 'Anim') and 'Case=Acc' in list_of_taglists[i]:
        list_of_taglists[i].add('Animacy=Anim')
    elif 'inan' in p.tag and 'Case=Acc' in list_of_taglists[i]:
        list_of_taglists[i].add('Animacy=Inan')

    return list_of_taglists


def correct_tags(list_of_taglists, wf_list):
    ord_nom_masc = ['первый', 'второй', 'третий', 'четвертый', 'пятый', 'шестой', 'седьмой', 'восьмой', 'девятый',
                        'десятый', 'одиннадцатый', 'двенадцатый', 'тринадцатый', 'четырнадцатый', 'пятнадцатый',
                        'шестнадцатый', 'семнадцатый', 'восемнадцатый', 'девятнадцатый', 'двадцатый', 'тридцатый',
                        'сороковой', 'пятидесятый', 'шестидесятый', 'семидесятый', 'восьмидесятый', 'девяностый',
                        'сотый', 'двухсотый', 'трехсотый', 'четырехсотый', 'пятисотый', 'шестисотый', 'семисотый',
                        'восьмисотый', 'девятисотый']

    pos_all = []
    for wfl in wf_list:
        pos_all.append(find_pos(correct_quant_noun(wfl)))

    if wf_list[len(wf_list) - 1] in ord_nom_masc:
        complex_ordinal = True
    else:
        complex_ordinal = False
    if complex_ordinal:
        correct_ord_nump(len(wf_list) - 1, pos_all, list_of_taglists, wf_list)

    for idx, pos in enumerate(pos_all):
        pos_after_num = pos_all[idx + 1] if idx < len(pos_all) - 1 else idx
        if pos == 'NUM' and pos_after_num != 'NUM':
            list_of_taglists = correct_nump(idx, pos_all, list_of_taglists, wf_list)
#    print('After NumP\t', str(list_of_taglists))

    for idx, wf in enumerate(wf_list):
        if find_pos(wf) == 'ADJ':
            list_of_taglists = correct_np(idx, pos_all, list_of_taglists, wf_list)

        elif wf == 'один':
            list_of_taglists = correct_np(idx, pos_all, list_of_taglists, wf_list)

        elif wf == 'одна':
            wf_list[idx] = 'один'
            list_of_taglists = correct_np(idx, pos_all, list_of_taglists, wf_list)

        elif wf in ['два', 'две', 'три', 'четыре']:
            wf_list[idx] = 'два' if wf == 'две' else wf
            list_of_taglists = correct_twop(idx, pos_all, list_of_taglists, wf_list)
#    print('After NP\t', str(list_of_taglists))

    for idx, wf in reversed(list(enumerate(wf_list))):
        if wf != modify_fraction(wf):
            k = idx
            for n in range(0, idx - 1):
                if wf_list[n] in numeral_to_number and wf_list[n + 1] in numeral_to_number and int(to_number(wf_list[n])) < int(to_number(wf_list[n + 1])):
                    k = n + 1
            correct_fraction(idx, k, list_of_taglists, wf_list)

    return list_of_taglists


def inflect_similar_case(wf_list, taglist, g):
    taglist = taglist.replace('Pos=NOUN', '').replace('Pos=ADJ', '').replace('Pos=VERB', '').replace('Pos=NUM', '')
    list_of_taglists = []
    for wf in wf_list:
        cur_taglist = 'Pos=' + find_pos(wf) + ';' + taglist
        cur_taglist = cur_taglist.replace(';;', ';')
        cur_taglist = cur_taglist[:len(cur_taglist) - 1] if cur_taglist[len(cur_taglist) - 1] == ';' else cur_taglist
        new_tagset = set({})
        for i in cur_taglist.split(';'):
            new_tagset.add(i)
        list_of_taglists.append(new_tagset)

    new_tagset_list = correct_tags(list_of_taglists, wf_list)

    new_wf_list = []
    for idx, wf in enumerate(wf_list):
        new_wf = g.produce(wf.replace('Ё', 'Е').replace('ё', 'е'), new_tagset_list[idx], debug=False)
        new_wf = new_wf if new_wf else 'to_be_announced'

        new_wf_list.append(new_wf)

    return (new_wf_list)


def make_inflect(wf_list, taglist):
    new_wf_list = inflect_similar_case(wf_list, taglist, g)
    return (new_wf_list)
