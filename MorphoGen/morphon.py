import os


class MorphonDicts:
    def __init__(self):
        self.sib = None
        self.zgpl = None
        self.t_end = None
        self.imper_ite = None
        self.genplen = None
        self.adjpos = None
        self.asppair = None
        self.short_past = None

    def load(self, dict_dir):
        with open(os.path.join(dict_dir, 'sib_e_ending.txt'), 'r', encoding='utf-8') as f:
            my_strings = f.readlines()
        self.sib = []
        for l in my_strings:
            self.sib.append(l.replace('\n', ''))

        with open(os.path.join(dict_dir, 'zero_genpl.txt'), 'r', encoding='utf-8') as f:
            my_strings = f.readlines()
        self.zgpl = []
        for l in my_strings:
            self.zgpl.append(l.replace('\n', ''))

        with open(os.path.join(dict_dir, 'inf_t_ending.txt'), 'r', encoding='utf-8') as f:
            my_strings = f.readlines()
        self.t_end = []
        for l in my_strings:
            self.t_end.append(l.replace('\n', ''))

        with open(os.path.join(dict_dir, 'imper_ite.txt'), 'r', encoding='utf-8') as f:
            my_strings = f.readlines()
        self.imper_ite = []
        for l in my_strings:
            self.imper_ite.append(l.replace('\n', ''))

        with open(os.path.join(dict_dir, 'gen_pl_en.txt'), 'r', encoding='utf-8') as f:
            my_strings = f.readlines()
        self.genplen = []
        for l in my_strings:
            self.genplen.append(l.replace('\n', ''))

        with open(os.path.join(dict_dir, 'adj_possess.txt'), 'r', encoding='utf-8') as f:
            my_strings = f.readlines()
        self.adjpos = []
        for l in my_strings:
            self.adjpos.append(l.replace('\n', ''))

        with open(os.path.join(dict_dir, 'with_aspect_pair.txt'), 'r', encoding='utf-8') as f:
            my_strings = f.readlines()
        self.asppair = []
        for l in my_strings:
            self.asppair.append(l.replace('\n', ''))

        with open(os.path.join(dict_dir, 'type3_short_past.txt'), 'r', encoding='utf-8') as f:
            my_strings = f.readlines()
        self.short_past = []
        for l in my_strings:
            self.short_past.append(l.replace('\n', ''))

    def check_sibil_list(self, lemma):
        is_sibil = False
        for s in self.sib:
            s = s.lower()
            if lemma == s:
                is_sibil = True
        return is_sibil

    def zero_genpl(self, lemma):
        is_zgpl = False
        if lemma in self.zgpl:
            is_zgpl = True
        return is_zgpl

    def inf_t_ending(self, lemma):
        is_t_end = False
        if lemma in self.t_end:
            is_t_end = True
        return is_t_end

    def imp_ite(self, lemma):
        is_ite = False
        if lemma in self.imper_ite:
            is_ite = True
        return is_ite

    def gen_pl_en(self, lemma):
        is_gplen = False
        if lemma in self.genplen:
            is_gplen = True
        return is_gplen

    def adj_possess(self, lemma):
        is_adj_pos = False
        if lemma in self.adjpos:
            is_adj_pos = True
        return is_adj_pos

    def aspect_pair(self, lemma):
        has_aspect_pair = False
        if lemma in self.asppair:
            has_aspect_pair = True
        return has_aspect_pair

    def if_short_past(self, lemma):
        is_short_past = False
        if lemma in self.short_past:
            is_short_past = True
        return is_short_past


# Когда-нибудь будущем надо избавиться от этого глобального объекта со списками и
# работать с локальным экземпляром класса MorphonDicts
# Сейчас предполагается, что загрузчик GenMorphApi его создаст и проинициализирует словарные списки
morphon_obj = None


def check_sibil_list(lemma):
    return morphon_obj.check_sibil_list(lemma)


def zero_genpl(lemma):
    return morphon_obj.zero_genpl(lemma)


def if_inf_t_ending(lemma):
    return morphon_obj.inf_t_ending(lemma)


def if_imper_ite(lemma):
    return morphon_obj.imp_ite(lemma)


def gen_pl_en(lemma):
    return morphon_obj.gen_pl_en(lemma)


def adj_possess(lemma):
    return morphon_obj.adj_possess(lemma)


def aspect_pair(lemma):
    return morphon_obj.aspect_pair(lemma)


def if_short_past(lemma):
    return morphon_obj.if_short_past(lemma)


def if_c(stem, i):
    sound = 'ц'
    h_search = False
    if len(stem) > 1:
        if sound == stem[len(stem) - i]:
            h_search = True
    return h_search


def if_e(stem, i):
    sound = 'е'
    h_search = False
    if len(stem) > 1:
        if sound == stem[len(stem) - i]:
            h_search = True
    return h_search


def if_u(stem, i):
    sound = 'у'
    h_search = False
    if len(stem) > 1:
        if sound == stem[len(stem) - i]:
            h_search = True
    return h_search


def if_i(stem, i):
    sound = 'и'
    h_search = False
    if len(stem) > 1:
        if sound == stem[len(stem) - i]:
            h_search = True
    return h_search


def if_y(stem, i):
    sound = 'ы'
    h_search = False
    if len(stem) > 1:
        if sound == stem[len(stem) - i]:
            h_search = True
    return h_search


def if_ja(stem, i):
    sound = 'я'
    h_search = False
    if len(stem) > 1:
        if sound == stem[len(stem) - i]:
            h_search = True
    return h_search


def if_o(stem, i):
    sound = 'о'
    h_search = False
    if len(stem) > 1:
        if sound == stem[len(stem) - i]:
            h_search = True
    return h_search


def if_ch(stem, i):
    sound = 'ч'
    h_search = False
    if len(stem) > 1:
        if sound == stem[len(stem) - i]:
            h_search = True
    return h_search


def if_sibil(stem, i):
    sounds = 'шжщ'
    h_search = False
    if len(stem) > 1:
        for l in sounds:
            if l == stem[len(stem) - i]:
                h_search = True
    return h_search


def if_vowel(stem, i):
    sounds = 'уеыаоэяию'
    h_search = False
    if len(stem) > 1:
        for l in sounds:
            if l == stem[len(stem) - i]:
                h_search = True
    return h_search


def if_soft(stem, i):
    sound = 'ь'
    h_search = False
    if sound == stem[len(stem) - i]:
        h_search = True
    return h_search


def if_kgx(stem, i):
    sounds = 'кгх'
    h_search = False
    if len(stem) > 1:
        for l in sounds:
            if l == stem[len(stem) - i]:
                h_search = True
    return h_search


def if_k(stem, i):
    sound = 'к'
    h_search = False
    if len(stem) > 1:
        if sound == stem[len(stem) - i]:
            h_search = True
    return h_search


def if_n(stem, i):
    sound = 'н'
    h_search = False
    if len(stem) > 1:
        if sound == stem[len(stem) - i]:
            h_search = True
    return h_search


def if_j(stem, i):
    sound = 'й'
    h_search = False
    if len(stem) > 1:
        if sound == stem[len(stem) - i]:
            h_search = True
    return h_search


def if_l(stem, i):
    sound = 'л'
    h_search = False
    if len(stem) > 1:
        if sound == stem[len(stem) - i]:
            h_search = True
    return h_search


def if_labial_1(stem, i):
    sounds = 'пбмвф'
    h_search = False
    if len(stem) > 1:
        for l in sounds:
            if l == stem[len(stem) - i]:
                h_search = True
    return h_search


def if_labial_2(stem, i):
    sounds = 'пбмв'
    h_search = False
    if len(stem) > 1:
        for l in sounds:
            if l == stem[len(stem) - i]:
                h_search = True
    return h_search


def if_labial_3(stem, i):
    sounds = 'пбм'
    h_search = False
    if len(stem) > 1:
        for l in sounds:
            if l == stem[len(stem) - i]:
                h_search = True
    return h_search


def if_liquid(stem, i):
    sounds = 'нлр'
    h_search = False
    if len(stem) > 1:
        for l in sounds:
            if l == stem[len(stem) - i]:
                h_search = True
    return h_search


def transform_i_y(stem, inflection):
    if (if_sibil(stem, 1) or if_ch(stem, 1) or if_kgx(stem, 1)):
        inflection = 'и'
    return inflection


def transform_y_i_total(stem, inflection):
    if (if_sibil(stem, 1) or if_ch(stem, 1) or if_kgx(stem, 1)) and len(inflection) > 0:
        if inflection[0] == 'ы':
            inflection = "".join(('и', inflection[1:]))
    return inflection


def transform_i(stem, inflection, lemma_value):
    wl = len(lemma_value)
    if lemma_value.find('ий') == wl - 2:
        inflection = 'и'
    return inflection


def transform_oj_ej(stem, inflection, lemma):
    if (if_sibil(stem, 1) or if_c(stem, 1) or if_ch(stem, 1)) and check_sibil_list(lemma):
        inflection = 'ей'
    return inflection


def transform_o_e(stem, inflection, lemma):
    wl = len(lemma)
    if (check_sibil_list(lemma) and (if_sibil(stem, 1) or if_c(stem, 1) or if_ch(stem, 1))) or (
            lemma.find('ще') == (wl - 2) and wl > 3) \
            or (lemma.find('це') == (wl - 2) and wl > 3):
        inflection = 'е'
    return inflection


def transform_om_em(stem, inflection, lemma):
    wl = len(lemma)
    if (check_sibil_list(lemma) and (if_sibil(stem, 1) or if_c(stem, 1) or if_ch(stem, 1))) or (
            lemma.find('ще') == (wl - 2) and wl > 3) \
            or (lemma.find('це') == (wl - 2) and wl > 3):
        inflection = 'ем'
    return inflection


def transform_ov_(stem, inflection, lemma):
    if if_sibil(stem, 1) or if_ch(stem, 1):
        inflection = 'ей'
    elif if_c(stem, 1) and check_sibil_list(lemma):
        inflection = 'ев'
    return inflection


def transform_a_i(stem, inflection, lemma):
    if if_k(stem, 1) and if_o(lemma, 1):
        inflection = 'и'
    return inflection


def transform_verb_ending(stem, inflection):
    if if_sibil(stem, 1) or if_ch(stem, 1):
        if inflection[0] == 'я':
            inflection = ''.join(('а', inflection[1:]))
        elif inflection[0] == 'ю':
            inflection = ''.join(('у', inflection[1:]))
    return inflection


def transform_dent_to_sib(stem):
    changes = {
        'ск': 'щ',
        'ст': 'щ',
        'т': 'ч',
        'д': 'ж',
        'с': 'ш',
        'з': 'ж',
        'к': 'ч',
        'г': 'ж'
    }
    if stem[-2:] in changes.keys():
        stem = ''.join((stem[:-2], changes[stem[-2:]]))
    if stem[-1] in changes.keys():
        stem = ''.join((stem[:-1], changes[stem[-1]]))
    return stem


def transform_vel_to_sib(stem):
    changes = {
        'х': 'ш'
    }
    if stem[-1] in changes.keys():
        stem = ''.join((stem[:-1], changes[stem[-1]]))
    return stem
