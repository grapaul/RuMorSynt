import re

from MorphoGen.morphon import *


def one_to(stemmatized, gram_pos, lemma_value):
    one_to = ['а', 'ы', 'у', 'е', 'ой', 'е', 'ы', '', '', 'ам', 'ами', 'ах']
    if gram_pos == 4:
        word_form = stemmatized[0] + transform_oj_ej(stemmatized[0], one_to[gram_pos], lemma_value)
    elif gram_pos == 1 or gram_pos == 6:
        word_form = stemmatized[0] + transform_i_y(stemmatized[0], one_to[gram_pos])
    else:
        word_form = stemmatized[0] + one_to[gram_pos]
    return word_form


def one_tv(stemmatized, gram_pos, lemma_value):
    one_tv = ['а', 'ы', 'у', 'е', 'ой', 'е', 'ы', '', 'ы', 'ам', 'ами', 'ах']
    if gram_pos == 4:
        word_form = stemmatized[0] + transform_oj_ej(stemmatized[0], one_tv[gram_pos], lemma_value)
    elif gram_pos == 1 or gram_pos == 6 or gram_pos == 8:
        word_form = stemmatized[0] + transform_i_y(stemmatized[0], one_tv[gram_pos])
    else:
        word_form = stemmatized[0] + one_tv[gram_pos]
    return word_form


def one_mo(stemmatized, gram_pos, lemma_value):
    one_mo = ['я', 'и', 'ю', 'е', 'ей', 'е', 'и', 'ь', 'ь', 'ям', 'ями', 'ях']
    word_form = stemmatized[0] + one_mo[gram_pos]
    return word_form


def one_mv(stemmatized, gram_pos, lemma_value):
    one_mv = ['я', 'и', 'ю', 'е', 'ей', 'е', 'и', 'ь', 'и', 'ям', 'ями', 'ях']
    word_form = stemmatized[0] + one_mv[gram_pos]
    return word_form


def one_mo_aster(stemmatized, gram_pos, lemma_value):
    one_mo_aster = ['я', 'и', 'ю', 'е', 'ей', 'е', 'и', 'ей', 'ей', 'ям', 'ями', 'ях']
    word_form = stemmatized[0] + one_mo_aster[gram_pos]
    return word_form


def one_mv_aster(stemmatized, gram_pos, lemma_value):
    one_mv_aster = ['я', 'и', 'ю', 'е', 'ей', 'е', 'и', 'ей', 'и', 'ям', 'ями', 'ях']
    word_form = stemmatized[0] + one_mv_aster[gram_pos]
    return word_form


def two_to(stemmatized, gram_pos, lemma_value):
    two_to = ['', 'а', 'а', 'у', 'ом', 'е', 'ы', 'ов', 'ов', 'ам', 'ами', 'ах']
    if gram_pos == 4:
        word_form = stemmatized[0] + transform_om_em(stemmatized[0], two_to[gram_pos], lemma_value)
    elif gram_pos == 6:
        word_form = stemmatized[0] + transform_i_y(stemmatized[0], two_to[gram_pos])
    elif gram_pos == 7 or gram_pos == 8:
        if zero_genpl(lemma_value):
            word_form = stemmatized[0]
        else:
            word_form = stemmatized[0] + transform_ov_(stemmatized[0], two_to[gram_pos], lemma_value)
    else:
        word_form = stemmatized[0] + two_to[gram_pos]
    return word_form


def two_tv(stemmatized, gram_pos, lemma_value):
    two_tv = ['', 'а', '', 'у', 'ом', 'е', 'ы', 'ов', 'ы', 'ам', 'ами', 'ах']
    if gram_pos == 4:
        word_form = stemmatized[0] + transform_om_em(stemmatized[0], two_tv[gram_pos], lemma_value)
    elif gram_pos == 6 or gram_pos == 8:
        word_form = stemmatized[0] + transform_i_y(stemmatized[0], two_tv[gram_pos])
    elif gram_pos == 7:
        if zero_genpl(lemma_value):
            word_form = stemmatized[0]
        else:
            word_form = stemmatized[0] + transform_ov_(stemmatized[0], two_tv[gram_pos], lemma_value)
    else:
        word_form = stemmatized[0] + two_tv[gram_pos]
    return word_form


def two_toa(stemmatized, gram_pos, lemma_value):
    two_toa = ['', 'а', 'а', 'у', 'ом', 'е', 'а', 'ов', 'ов', 'ам', 'ами', 'ах']
    if gram_pos == 4:
        word_form = stemmatized[0] + transform_om_em(stemmatized[0], two_toa[gram_pos], lemma_value)
    elif gram_pos == 7 or gram_pos == 8:
        word_form = stemmatized[0] + transform_ov_(stemmatized[0], two_toa[gram_pos], lemma_value)
    else:
        word_form = stemmatized[0] + two_toa[gram_pos]
    return word_form


def two_tva(stemmatized, gram_pos, lemma_value):
    two_tva = ['', 'а', '', 'у', 'ом', 'е', 'а', 'ов', 'а', 'ам', 'ами', 'ах']
    if gram_pos == 4:
        word_form = stemmatized[0] + transform_om_em(stemmatized[0], two_tva[gram_pos], lemma_value)
    elif gram_pos == 7 and zero_genpl(lemma_value):
        word_form = stemmatized[0]
    else:
        word_form = stemmatized[0] + two_tva[gram_pos]
    return word_form


def two_yo(stemmatized, gram_pos, lemma_value):
    two_yo = ['й', 'я', 'я', 'ю', 'ем', 'е', 'и', 'ев', 'ев', 'ям', 'ями', 'ях']
    if gram_pos == 5:
        word_form = stemmatized[0] + transform_i(stemmatized[0], two_yo[gram_pos], lemma_value)
    else:
        word_form = stemmatized[0] + two_yo[gram_pos]
    return word_form


def two_yv(stemmatized, gram_pos, lemma_value):
    two_yv = ['й', 'я', 'й', 'ю', 'ем', 'е', 'и', 'ев', 'и', 'ям', 'ями', 'ях']
    if gram_pos == 5:
        word_form = stemmatized[0] + transform_i(stemmatized[0], two_yv[gram_pos], lemma_value)
    else:
        word_form = stemmatized[0] + two_yv[gram_pos]
    return word_form


def two_mo(stemmatized, gram_pos, lemma_value):
    two_mo = ['ь', 'я', 'я', 'ю', 'ем', 'е', 'и', 'ей', 'ей', 'ям', 'ями', 'ях']
    word_form = stemmatized[0] + two_mo[gram_pos]
    return word_form


def two_mv(stemmatized, gram_pos, lemma_value):
    two_mv = ['ь', 'я', 'ь', 'ю', 'ем', 'е', 'и', 'ей', 'и', 'ям', 'ями', 'ях']
    word_form = stemmatized[0] + two_mv[gram_pos]
    return word_form


def two_moa(stemmatized, gram_pos, lemma_value):
    two_moa = ['ь', 'я', 'я', 'ю', 'ем', 'е', 'я', 'ей', 'ей', 'ям', 'ями', 'ях']
    word_form = stemmatized[0] + two_moa[gram_pos]
    return word_form


def two_mva(stemmatized, gram_pos, lemma_value):
    two_mva = ['ь', 'я', 'ь', 'ю', 'ем', 'е', 'я', 'ей', 'я', 'ям', 'ями', 'ях']
    word_form = stemmatized[0] + two_mva[gram_pos]
    return word_form


def two_tos(stemmatized, gram_pos, lemma_value):
    two_tos = ['о', 'а', 'о', 'у', 'ом', 'е', 'а', '', '', 'ам', 'ами', 'ах']
    word_form = stemmatized[0] + two_tos[gram_pos]
    return word_form


def two_tvs(stemmatized, gram_pos, lemma_value):
    two_tvs = ['о', 'а', 'о', 'у', 'ом', 'е', 'а', '', 'а', 'ам', 'ами', 'ах']
    if gram_pos in [0, 2]:
        word_form = stemmatized[0] + transform_o_e(stemmatized[0], two_tvs[gram_pos], lemma_value)
    elif gram_pos == 4:
        word_form = stemmatized[0] + transform_om_em(stemmatized[0], two_tvs[gram_pos], lemma_value)
    elif gram_pos == 6:
        word_form = stemmatized[0] + transform_a_i(stemmatized[0], two_tvs[gram_pos], lemma_value)
    else:
        word_form = stemmatized[0] + two_tvs[gram_pos]
    return word_form


def two_tvs_plus(stemmatized, gram_pos, lemma_value):
    two_tvs = ['о', 'а', 'о', 'у', 'ом', 'е', 'а', '', 'а', 'ам', 'ами', 'ах']
    if gram_pos in [0, 2]:
        word_form = stemmatized[0] + transform_o_e(stemmatized[0], two_tvs[gram_pos], lemma_value)
    elif gram_pos == 4:
        word_form = stemmatized[0] + transform_om_em(stemmatized[0], two_tvs[gram_pos], lemma_value)
    elif gram_pos == 6:
        word_form = stemmatized[0] + transform_a_i(stemmatized[0], two_tvs[gram_pos], lemma_value)
    elif gram_pos == 7:
        word_form = stemmatized[1] + two_tvs[gram_pos]
    else:
        word_form = stemmatized[0] + two_tvs[gram_pos]
    return word_form


def two_mos(stemmatized, gram_pos, lemma_value):
    two_mos = ['е', 'а', 'е', 'у', 'ем', 'е', 'а', '', '', 'ам', 'ами', 'ах']
    word_form = stemmatized[0] + two_mos[gram_pos]
    return word_form


def two_mvs(stemmatized, gram_pos, lemma_value):
    two_mvs = ['е', 'я', 'е', 'ю', 'ем', 'е', 'я', 'ей', 'я', 'ям', 'ями', 'ях']
    two_tvs = ['о', 'а', 'о', 'у', 'ом', 'е', 'а', '', 'а', 'ам', 'ами', 'ах']
    two_mos = ['е', 'а', 'е', 'у', 'ем', 'е', 'а', '', '', 'ам', 'ами', 'ах']
    if if_sibil(stemmatized[0], 1) or if_ch(stemmatized[0], 1):
        if gram_pos < 6:
            word_form = stemmatized[0] + two_mos[gram_pos]
        else:
            word_form = stemmatized[0] + two_tvs[gram_pos]
    else:
        word_form = stemmatized[0] + two_mvs[gram_pos]
    return word_form


def three_o(stemmatized, gram_pos, lemma_value):
    three_o = ['ь', 'и', 'ь', 'и', 'ью', 'и', 'и', 'ей', 'ей', 'ям', 'ями', 'ях']
    two_to = ['', 'а', 'а', 'у', 'ом', 'е', 'ы', 'ов', 'ов', 'ам', 'ами', 'ах']
    if (if_sibil(stemmatized[0], 1) or if_ch(stemmatized[0], 1)) and (
            gram_pos == 9 or gram_pos == 10 or gram_pos == 11):
        word_form = stemmatized[0] + two_to[gram_pos]
    else:
        word_form = stemmatized[0] + three_o[gram_pos]
    return word_form


def three_v(stemmatized, gram_pos, lemma_value):
    three_v = ['ь', 'и', 'ь', 'и', 'ью', 'и', 'и', 'ей', 'и', 'ям', 'ями', 'ях']
    two_to = ['', 'а', 'а', 'у', 'ом', 'е', 'ы', 'ов', 'ов', 'ам', 'ами', 'ах']
    if (if_sibil(stemmatized[0], 1) or if_ch(stemmatized[0], 1)) and (
            gram_pos == 9 or gram_pos == 10 or gram_pos == 11):
        word_form = stemmatized[0] + two_to[gram_pos]
    else:
        word_form = stemmatized[0] + three_v[gram_pos]
    return word_form


def four_o(stemmatized, gram_pos, lemma_value):
    four_o = ['я', 'и', 'ю', 'и', 'ей', 'и', 'и', 'й', 'й', 'ям', 'ями', 'ях']
    word_form = stemmatized[0] + four_o[gram_pos]
    return word_form


def four_v(stemmatized, gram_pos, lemma_value):
    four_v = ['я', 'и', 'ю', 'и', 'ей', 'и', 'и', 'й', 'и', 'ям', 'ями', 'ях']
    word_form = stemmatized[0] + four_v[gram_pos]
    return word_form


def four_os(stemmatized, gram_pos, lemma_value):
    four_os = ['е', 'я', 'е', 'ю', 'ем', 'и', 'я', 'й', 'й', 'ям', 'ями', 'ях']
    word_form = stemmatized[0] + four_os[gram_pos]
    return word_form


def four_vs(stemmatized, gram_pos, lemma_value):
    four_vs = ['е', 'я', 'е', 'ю', 'ем', 'и', 'я', 'й', 'я', 'ям', 'ями', 'ях']
    word_form = stemmatized[0] + four_vs[gram_pos]
    return word_form


def two_to_soft(stemmatized, gram_pos, lemma_value):
    two_to_soft = ['', 'а', 'а', 'у', 'ом', 'е', 'ья', 'ьев', 'ьев', 'ьям', 'ьями', 'ьях']
    word_form = stemmatized[0] + two_to_soft[gram_pos]
    return word_form


def two_tv_soft(stemmatized, gram_pos, lemma_value):
    two_tv_soft = ['', 'а', '', 'у', 'ом', 'е', 'ья', 'ьев', 'ья', 'ьям', 'ьями', 'ьях']
    word_form = stemmatized[0] + two_tv_soft[gram_pos]
    return word_form


def two_to_(stemmatized, gram_pos, lemma_value):
    two_to_ = ['', 'а', 'а', 'у', 'ом', 'е', 'ы', 'ов', 'ов', 'ам', 'ами', 'ах']
    if gram_pos == 0:
        word_form = stemmatized[1] + two_to_[gram_pos]
    elif gram_pos == 4:
        word_form = stemmatized[0] + transform_om_em(stemmatized[0], two_to_[gram_pos], lemma_value)
    elif gram_pos == 6:
        word_form = stemmatized[0] + transform_i_y(stemmatized[0], two_to_[gram_pos])
    elif gram_pos == 7 or gram_pos == 8:
        if zero_genpl(lemma_value):
            word_form = stemmatized[0]
        else:
            word_form = stemmatized[0] + transform_ov_(stemmatized[0], two_to_[gram_pos], lemma_value)
    else:
        word_form = stemmatized[0] + two_to_[gram_pos]
    return word_form


def two_tv_(stemmatized, gram_pos, lemma_value):
    two_tv_ = ['', 'а', '', 'у', 'ом', 'е', 'ы', 'ов', 'ы', 'ам', 'ами', 'ах']
    if if_sibil(stemmatized[0], 3):
        stemmatized[0] = stemmatized[0][0:-2] + stemmatized[1][-1]
    if gram_pos == 0 or gram_pos == 2:
        word_form = stemmatized[1] + two_tv_[gram_pos]
    elif gram_pos == 4:
        word_form = stemmatized[0] + transform_om_em(stemmatized[0], two_tv_[gram_pos], lemma_value)
    elif gram_pos == 6 or gram_pos == 8:
        word_form = stemmatized[0] + transform_i_y(stemmatized[0], two_tv_[gram_pos])
    elif gram_pos == 7:
        if zero_genpl(lemma_value):
            word_form = stemmatized[1]
        else:
            word_form = stemmatized[0] + transform_ov_(stemmatized[0], two_tv_[gram_pos], lemma_value)
    else:
        word_form = stemmatized[0] + two_tv_[gram_pos]
    return word_form


def two_mo_(stemmatized, gram_pos, lemma_value):
    two_mo_ = ['ь', 'я', 'я', 'ю', 'ем', 'е', 'и', 'ей', 'ей', 'ям', 'ями', 'ях']
    if gram_pos == 0:
        word_form = stemmatized[1] + two_mo_[gram_pos]
    else:
        word_form = stemmatized[0] + two_mo_[gram_pos]
    return word_form


def two_mv_(stemmatized, gram_pos, lemma_value):
    two_mv_ = ['ь', 'я', 'ь', 'ю', 'ем', 'е', 'и', 'ей', 'и', 'ям', 'ями', 'ях']
    if gram_pos == 0 or gram_pos == 2:
        word_form = stemmatized[1] + two_mv_[gram_pos]
    else:
        word_form = stemmatized[0] + two_mv_[gram_pos]
    return word_form


def one_to_plus_o(stemmatized, gram_pos, lemma_value):
    one_to_plus_o = ['а', 'ы', 'у', 'е', 'ой', 'е', 'ы', '', '', 'ам', 'ами', 'ах']
    if gram_pos == 4:
        word_form = stemmatized[0] + transform_oj_ej(stemmatized[0], one_to_plus_o[gram_pos], lemma_value)
    elif gram_pos == 1 or gram_pos == 6:
        word_form = stemmatized[0] + transform_i_y(stemmatized[0], one_to_plus_o[gram_pos])
    elif gram_pos == 7 or gram_pos == 8:
        word_form = stemmatized[1] + one_to_plus_o[gram_pos]
    else:
        word_form = stemmatized[0] + one_to_plus_o[gram_pos]
    return word_form


def one_tv_plus_o(stemmatized, gram_pos, lemma_value):
    one_tv_plus_o = ['а', 'ы', 'у', 'е', 'ой', 'е', 'ы', '', 'ы', 'ам', 'ами', 'ах']
    if gram_pos == 4:
        word_form = stemmatized[0] + transform_oj_ej(stemmatized[0], one_tv_plus_o[gram_pos], lemma_value)
    elif gram_pos == 1 or gram_pos == 6 or gram_pos == 8:
        word_form = stemmatized[0] + transform_i_y(stemmatized[0], one_tv_plus_o[gram_pos])
    elif gram_pos == 7:
        word_form = stemmatized[1] + one_tv_plus_o[gram_pos]
    else:
        word_form = stemmatized[0] + one_tv_plus_o[gram_pos]
    return word_form


def one_to_plus(stemmatized, gram_pos, lemma_value):
    one_to_plus = ['а', 'ы', 'у', 'е', 'ой', 'е', 'ы', '', '', 'ам', 'ами', 'ах']
    if gram_pos == 4:
        word_form = stemmatized[0] + transform_oj_ej(stemmatized[0], one_to_plus[gram_pos], lemma_value)
    elif gram_pos == 1 or gram_pos == 6:
        word_form = stemmatized[0] + transform_i_y(stemmatized[0], one_to_plus[gram_pos])
    elif gram_pos == 7 or gram_pos == 8:
        word_form = stemmatized[1] + one_to_plus[gram_pos]
    else:
        word_form = stemmatized[0] + one_to_plus[gram_pos]
    return word_form


def one_tv_plus(stemmatized, gram_pos, lemma_value):
    one_tv_plus = ['а', 'ы', 'у', 'е', 'ой', 'е', 'ы', '', 'ы', 'ам', 'ами', 'ах']
    if gram_pos == 4:
        word_form = stemmatized[0] + transform_oj_ej(stemmatized[0], one_tv_plus[gram_pos], lemma_value)
    elif gram_pos == 1 or gram_pos == 6 or gram_pos == 8:
        word_form = stemmatized[0] + transform_i_y(stemmatized[0], one_tv_plus[gram_pos])
    elif gram_pos == 7:
        word_form = stemmatized[1] + one_tv_plus[gram_pos]
    elif gram_pos == 1 or gram_pos == 6 or gram_pos == 8:
        word_form = stemmatized[0] + transform_i_y(stemmatized[0], one_tv_plus[gram_pos])
    else:
        word_form = stemmatized[0] + one_tv_plus[gram_pos]
    return word_form


def one_mo_plus(stemmatized, gram_pos, lemma_value):
    one_mo_plus = ['я', 'и', 'ю', 'е', 'ей', 'е', 'и', '', '', 'ям', 'ями', 'ях']
    if gram_pos == 7 or gram_pos == 8:
        word_form = stemmatized[1] + one_mo_plus[gram_pos]
    else:
        word_form = stemmatized[0] + one_mo_plus[gram_pos]
    return word_form


def one_mv_plus(stemmatized, gram_pos, lemma_value):
    one_mv_plus = ['я', 'и', 'ю', 'е', 'ей', 'е', 'и', '', 'и', 'ям', 'ями', 'ях']
    if gram_pos == 7:
        if gen_pl_en(lemma_value):
            word_form = stemmatized[1][:-1] + one_mv_plus[gram_pos]
        else:
            word_form = stemmatized[1] + one_mv_plus[gram_pos]
    else:
        word_form = stemmatized[0] + one_mv_plus[gram_pos]
    return word_form


def lnya(stemmatized, gram_pos, lemma_value):
    one_mv_plus = ['я', 'и', 'ю', 'е', 'ей', 'е', 'и', 'ь', 'и', 'ям', 'ями', 'ях']
    if gram_pos == 7:
        word_form = stemmatized[1]
    else:
        word_form = stemmatized[0] + one_mv_plus[gram_pos]
    return word_form


def two_cv_plus(stemmatized, gram_pos, lemma_value):
    two_tvs = ['о', 'а', 'о', 'у', 'ом', 'е', 'а', '', 'а', 'ам', 'ами', 'ах']
    two_cv_plus = ['е', 'а', 'е', 'у', 'ем', 'е', 'а', '', 'а', 'ам', 'ами', 'ах']
    if gram_pos == 0 or gram_pos == 2 or gram_pos == 4:
        if if_e(lemma_value, 1):
            word_form = stemmatized[0] + two_cv_plus[gram_pos]
        else:
            word_form = stemmatized[0] + two_tvs[gram_pos]
    elif gram_pos == 7:
        word_form = stemmatized[1] + two_cv_plus[gram_pos]
    else:
        word_form = stemmatized[0] + two_cv_plus[gram_pos]
    return word_form


def two_ts_soft(stemmatized, gram_pos, lemma_value):
    two_tv_soft = ['', 'а', 'о', 'у', 'ом', 'е', 'ья', 'ьев', 'ья', 'ьям', 'ьями', 'ьях']
    two_tvs = ['о', 'а', 'о', 'у', 'ом', 'е', 'а', '', 'а', 'ам', 'ами', 'ах']
    if gram_pos == 0:
        word_form = stemmatized[0] + two_tvs[gram_pos]
    else:
        word_form = stemmatized[0] + two_tv_soft[gram_pos]
    return word_form


def four_vs_plus(stemmatized, gram_pos, lemma_value):
    four_vs_plus = ['е', 'я', 'е', 'ю', 'ем', 'е', 'я', 'ий', 'я', 'ям', 'ями', 'ях']
    if gram_pos == 7:
        word_form = stemmatized[1] + four_vs_plus[gram_pos]
    else:
        word_form = stemmatized[0] + four_vs_plus[gram_pos]
    return word_form


def two_mo_soft(stemmatized, gram_pos, lemma_value):
    two_mo_soft = ['', 'я', 'я', 'ю', 'ем', 'е', 'ья', 'ьев', 'ьев', 'ьям', 'ьями', 'ьях']
    if gram_pos == 0:
        word_form = stemmatized[1] + two_mo_soft[gram_pos]
    else:
        word_form = stemmatized[0] + two_mo_soft[gram_pos]
    return word_form


def five(stemmatized, gram_pos, lemma_value):
    two_tos = ['о', 'а', 'о', 'у', 'ом', 'е', 'а', '', '', 'ам', 'ами', 'ах']
    two_to_ = ['', 'а', 'а', 'у', 'ом', 'е', 'ы', 'ов', 'ов', 'ам', 'ами', 'ах']
    if gram_pos == 0:
        word_form = stemmatized[1] + two_to_[gram_pos]
    elif gram_pos < 6 and gram_pos > 0:
        word_form = stemmatized[0] + two_to_[gram_pos]
    else:
        word_form = stemmatized[2] + two_tos[gram_pos]
    return word_form


def six(stemmatized, gram_pos, lemma_value):
    six = ['', '', '', '', '', '', 'е', '', '', 'ам', 'ами', 'ах']
    two_to_ = ['', 'а', 'а', 'у', 'ом', 'е', 'ы', 'ов', 'ов', 'ам', 'ами', 'ах']
    if gram_pos < 6:
        word_form = stemmatized[0] + two_to_[gram_pos]
    else:
        word_form = stemmatized[1] + six[gram_pos]
    return word_form


def seven(stemmatized, gram_pos, lemma_value):
    seven = ['я', 'и', 'ю', 'е', 'ей', 'е', 'и', 'ей', 'и', 'ям', 'ями', 'ях']
    if gram_pos == 7:
        word_form = stemmatized[1] + seven[gram_pos]
    else:
        word_form = stemmatized[0] + seven[gram_pos]
    return word_form


def otchm(stemmatized, gram_pos, lemma_value):
    two_to = ['', 'а', 'а', 'у', 'ом', 'е', 'ы', 'ов', 'ов', 'ам', 'ами', 'ах']
    two_mo = ['ь', 'я', 'я', 'ю', 'ем', 'е', 'и', 'ей', 'ей', 'ям', 'ями', 'ях']
    if gram_pos == 4:
        word_form = stemmatized[0] + two_mo[gram_pos]
    else:
        word_form = stemmatized[0] + two_to[gram_pos]
    return word_form


def surn_m(stemmatized, gram_pos, lemma_value):
    surn_m = ['', 'а', 'а', 'у', 'ым', 'е', 'ы', 'ых', 'ых', 'ым', 'ыми', 'ых']
    word_form = stemmatized[0] + surn_m[gram_pos]
    return word_form


def surn_f(stemmatized, gram_pos, lemma_value):
    surn_f = ['а', 'ой', 'у', 'ой', 'ой', 'ой', 'ы', 'ых', 'ых', 'ым', 'ыми', 'ых']
    word_form = stemmatized[0] + surn_f[gram_pos]
    return word_form


def find_form(string_parad, stemmatized, gram_pos, lemma_value):
    forms = {
        '1то': one_to,
        '1тв': one_tv,
        '1мо': one_mo,
        '1мв': one_mv,
        '1мо*': one_mo_aster,
        '1мв*': one_mv_aster,
        '2то': two_to,
        '2тв': two_tv,
        '2тоа': two_toa,
        '2тва': two_tva,
        '2йо': two_yo,
        '2йв': two_yv,
        '2мо': two_mo,
        '2мв': two_mv,
        '2моа': two_moa,
        '2мва': two_mva,
        '2тос': two_tos,
        '2твс': two_tvs,
        '2твс+о': two_tvs_plus,
        '2твс+': two_tvs_plus,
        '2мос': two_mos,
        '2мвс': two_mvs,
        '3о': three_o,
        '3в': three_v,
        '4о': four_o,
        '4в': four_v,
        '4ос': four_os,
        '4вс': four_vs,
        '2тоь': two_to_soft,
        '2твь': two_tv_soft,
        '2то-': two_to_,
        '2тв-': two_tv_,
        '2мо-': two_mo_,
        '2мв-': two_mv_,
        '1то+о': one_to_plus_o,
        '1тв+о': one_tv_plus_o,
        '1то+': one_to_plus,
        '1тв+': one_tv_plus,
        '1мо+': one_mo_plus,
        '1мв+': one_mv_plus,
        'льня': lnya,
        '2цв+': two_cv_plus,
        '2тсь': two_ts_soft,
        '4вс+': four_vs_plus,
        '2моь': two_mo_soft,
        '5': five,
        '6': six,
        '7': seven,
        'отчм': otchm,
        'фм': surn_m,
        'фж': surn_f
    }
    return forms[string_parad](stemmatized, gram_pos, lemma_value) if string_parad in forms.keys() else 'error_in_parads.py'


def find_adj_form(string_parad, stemmatized, gram_pos, grammemes):
    adj_y = ['ый', 'ого', 'ый', 'ому', 'ым', 'ом', 'ая', 'ой', 'ую', 'ой', 'ой', 'ой', 'ое', 'ого', 'ое', 'ому', 'ым',
             'ом', 'ые', 'ых', 'ые', 'ым', 'ыми', 'ых', '', 'а', 'о', 'ы', 'ее']
    adj_y_soft = ['ий', 'его', 'ий', 'ему', 'им', 'ем', 'яя', 'ей', 'юю', 'ей', 'ей', 'ей', 'ее', 'его', 'ее', 'ему',
                  'им', 'ем', 'ие', 'их', 'ие', 'им', 'ими', 'их', 'ь', 'я', 'е', 'и', 'ее']
    adj_y_soft_velar = ['ий', 'ого', 'ий', 'ому', 'им', 'ом', 'ая', 'ой', 'ую', 'ой', 'ой', 'ой', 'ое', 'ого', 'ое',
                        'ому', 'им', 'ом', 'ие', 'их', 'ие', 'им', 'ими', 'их', '', 'а', 'о', 'и', 'е']
    adj_y_o = ['ой', 'ого', 'ой', 'ому', 'ым', 'ом', 'ая', 'ой', 'ую', 'ой', 'ой', 'ой', 'ое', 'ого', 'ое', 'ому', 'ым',
               'ом', 'ые', 'ых', 'ые', 'ым', 'ыми', 'ых', '', 'а', 'о', 'ы', 'ее']
    adj_possess = ['', 'а', '', 'у', 'ым', 'ом', 'а', 'ой', 'у', 'ой', 'ой', 'ой', 'о', 'а', 'о', 'у', 'ым',
             'ом', 'ы', 'ых', 'ы', 'ым', 'ыми', 'ых', '', 'а', 'о', 'ы', 'ее']
    adj_y_soft_possess = ['ий', 'ьего', 'ий', 'ьему', 'ьим', 'ьем', 'ья', 'ьей', 'ью', 'ьей', 'ьей', 'ьей', 'ье', 'ьего', 'ье', 'ьему',
                  'ьим', 'ьем', 'ьи', 'ьих', 'ьи', 'ьим', 'ьими', 'ьих', 'ий', 'ья', 'ье', 'ьи', 'ее']

    word_form = 'Not Found Adj'
    if (gram_pos == 2 or gram_pos == 20) and 'Animacy=Anim' in grammemes:
        if string_parad == 'adj_y':
            word_form = stemmatized[0] + adj_y[gram_pos - 1]
        elif string_parad == 'adj_y_soft':
            word_form = stemmatized[0] + adj_y_soft[gram_pos - 1]
        elif string_parad == 'adj_y_soft_possess':
            word_form = stemmatized[0] + adj_y_soft[gram_pos - 1]
        elif string_parad == 'adj_y_o':
            word_form = stemmatized[0] + transform_y_i_total(stemmatized[0], adj_y_o[gram_pos - 1])
        elif string_parad == 'adj_y_soft_velar':
            word_form = stemmatized[0] + adj_y_soft_velar[gram_pos - 1]
        elif string_parad == 'adj_possess':
            word_form = stemmatized[1] + adj_possess[gram_pos - 1]

    elif (gram_pos == 2 or gram_pos == 20) and 'Animacy=Inan' in grammemes:
        if string_parad == 'adj_y':
            word_form = stemmatized[0] + adj_y[gram_pos - 2]
        elif string_parad == 'adj_y_soft':
            word_form = stemmatized[0] + adj_y_soft[gram_pos - 2]
        elif string_parad == 'adj_y_soft_possess':
            word_form = stemmatized[0] + adj_y_soft[gram_pos - 2]
        elif string_parad == 'adj_y_o':
            word_form = stemmatized[0] + transform_y_i_total(stemmatized[0], adj_y_o[gram_pos - 2])
        elif string_parad == 'adj_y_soft_velar':
            word_form = stemmatized[0] + adj_y_soft_velar[gram_pos - 2]
        elif string_parad == 'adj_possess':
            word_form = stemmatized[1] + adj_possess[gram_pos - 2]



    elif gram_pos in [6,8,25] and (if_sibil(stemmatized[0], 1) or if_ch(stemmatized[0], 1)):
        if string_parad == 'adj_y' or string_parad == 'adj_y_soft':
            word_form = stemmatized[0] + adj_y[gram_pos]
        elif string_parad == 'adj_y_o':
            word_form = stemmatized[0] + adj_y_o[gram_pos]
        elif string_parad == 'adj_y_soft_velar':
            word_form = stemmatized[0] + adj_y_soft_velar[gram_pos]
        elif string_parad == 'adj_possess':
            word_form = stemmatized[1] + adj_possess[gram_pos]
        elif string_parad == 'adj_y_soft_possess':
            word_form = stemmatized[0] + adj_y_soft_possess[gram_pos]
    elif gram_pos != 24:
        if string_parad == 'adj_y':
            if if_c(stemmatized[0], 1) and gram_pos in [1,3,5,7,9,10,11,12,13,14,15,17,26]:
                word_form = stemmatized[0] + adj_y_soft[gram_pos]
            else:
                word_form = stemmatized[0] + adj_y[gram_pos]
        elif string_parad == 'adj_y_soft':
            if gram_pos == 26 and stemmatized[0] == 'хорош':
                word_form = 'хорошо'
            else:
                word_form = stemmatized[0] + adj_y_soft[gram_pos]
        elif string_parad == 'adj_y_o':
            word_form = stemmatized[0] + transform_y_i_total(stemmatized[0], adj_y_o[gram_pos])
        elif string_parad == 'adj_y_soft_velar':
            if gram_pos == 28:
                stem = transform_dent_to_sib(stemmatized[0])
                stem = transform_vel_to_sib(stem)
                word_form = stem + adj_y_soft_velar[gram_pos]
            else:
                word_form = stemmatized[0] + adj_y_soft_velar[gram_pos]
        elif string_parad == 'adj_possess':
            word_form = stemmatized[1] + adj_possess[gram_pos]
        elif string_parad == 'adj_y_soft_possess':
                word_form = stemmatized[0] + adj_y_soft_possess[gram_pos]
    elif gram_pos == 24 and len(stemmatized) > 1:
        if string_parad == 'adj_y':
            word_form = stemmatized[1] + adj_y[gram_pos]
        elif string_parad == 'adj_y_soft':
            word_form = stemmatized[1] + adj_y_soft[gram_pos]
        elif string_parad == 'adj_y_o':
            word_form = stemmatized[1] + adj_y_o[gram_pos]
        elif string_parad == 'adj_y_soft_velar':
            word_form = stemmatized[1] + adj_y_soft_velar[gram_pos]
        elif string_parad == 'adj_possess':
            word_form = stemmatized[1] + adj_possess[gram_pos]
        elif string_parad == 'adj_y_soft_possess':
            word_form = stemmatized[0] + adj_y_soft_possess[gram_pos]
    elif gram_pos == 24 and len(stemmatized) == 1:
        if string_parad == 'adj_y':
            word_form = stemmatized[0] + adj_y[gram_pos]
        elif string_parad == 'adj_y_soft':
            if if_sibil(stemmatized[0], 1):
                word_form = stemmatized[0] + adj_y[gram_pos]
            else:
                word_form = stemmatized[0] + adj_y_soft[gram_pos]
        elif string_parad == 'adj_y_o':
            word_form = stemmatized[0] + adj_y_o[gram_pos]
        elif string_parad == 'adj_y_soft_velar':
            word_form = stemmatized[0] + adj_y_soft_velar[gram_pos]

    return (word_form)


def end_postfix(ending, postfix):
    if postfix:
        if ending == '' or ending[-1] in ['ь', 'т', 'м', 'л', 'й', 'г', 'к']:
            postfix = 'ся'
        else:
            postfix = 'сь'
        if ending == 'в':
            return "вшись"
    else:
        postfix = ''
    return ending + postfix


def v1(stemmatized, gram_pos, postfix):
    end = ['ть', 'ю', 'ешь', 'ет', 'ем', 'ете', 'ют', 'л', 'ла', 'ло', 'ли', 'й', 'йте', 'ем', 'я', 'в', 'ющий', 'емый', 'вший', 'нный']
    word_form = stemmatized[0] + end_postfix(end[gram_pos], postfix)
    return word_form


def v2(stemmatized, gram_pos, postfix):
    end = ['ть', 'ю', 'ешь', 'ет', 'ем', 'ете', 'ют', 'л', 'ла', 'ло', 'ли', 'й', 'йте', 'ем', 'я', 'в', 'ющий', 'емый', 'вший', 'нный']
    if (gram_pos <= 6 and gram_pos != 0) or gram_pos in [11, 12, 13, 14, 16, 17]:
        if if_sibil(stemmatized[0], 2) or if_ch(stemmatized[0], 2) or if_c(stemmatized[0], 2):
            word_form = re.sub('е$', 'у', re.sub('о$', 'у', stemmatized[0])) + end_postfix(end[gram_pos], postfix)
        else:
            word_form = re.sub('е$', 'ю', re.sub('о$', 'у', stemmatized[0])) + end_postfix(end[gram_pos], postfix)
    else:
        word_form = stemmatized[1] + end_postfix(end[gram_pos], postfix)
    return word_form


def v3(stemmatized, gram_pos, postfix):
    end = ['уть', 'у', 'ешь', 'ет', 'ем', 'ете', 'ут', 'л', 'ла', 'ло', 'ли', 'и', 'ите', 'ем', '*', 'в', 'ущий', '*', 'увший', 'утый']
    if gram_pos <= 6 or gram_pos in [13, 16, 18, 19]:
        word_form = stemmatized[0] + end_postfix(end[gram_pos], postfix)
    elif gram_pos in [11, 12]:
        if stemmatized[0][-2] in ['а', 'о', 'у', 'ы', 'э', 'я', 'ё', 'ю', 'и', 'е']:
            if stemmatized[0].startswith('вы'):
                if len(stemmatized[0]) > 3:
                    ending = 'и'
                else:
                    ending = 'ь'
            # elif len(stemmatized[0]) > 3:
            #     ending = 'ь'
            else:
                if (stemmatized[0] + end_postfix(end[0], postfix)).endswith('тянуть'):
                    ending = 'и'
                else:
                    ending = 'ь'
            word_form = stemmatized[0] + \
                        end_postfix(transform_verb_ending(stemmatized[0], end[gram_pos].replace('и', ending)), postfix)
        else:
            word_form = stemmatized[0] + end_postfix(end[gram_pos], postfix)
    else:
        if if_short_past(stemmatized[0] + end_postfix(end[0], postfix)):
            if gram_pos == 7:
                word_form = stemmatized[1][:-2] + end_postfix('', postfix)
            elif gram_pos in [8, 9, 10]:
                word_form = stemmatized[1][:-2] + end_postfix(end[gram_pos], postfix)
            else:
                word_form = stemmatized[1] + end_postfix(end[gram_pos], postfix)
        else:
            word_form = stemmatized[1] + end_postfix(end[gram_pos], postfix)
    return word_form


def v4(stemmatized, gram_pos, postfix):
    end = ['ить', 'ю', 'ишь', 'ит', 'им', 'ите', 'ят', 'л', 'ла', 'ло', 'ли', 'и', 'ите', 'им', 'я', 'в', 'ящий', 'имый', 'вший', 'енный']
    if gram_pos <= 6 or gram_pos in [11, 12, 13, 14, 16, 17, 19]:
        if gram_pos in [1, 19]:
            stem = transform_dent_to_sib(stemmatized[0])
            if if_labial_1(stemmatized[0], 1):
                word_form = stem + 'л' + end_postfix(end[gram_pos], postfix)
            else:
                word_form = stem + end_postfix(transform_verb_ending(stem, end[gram_pos]), postfix)
        elif gram_pos in [11, 12]:
            if if_imper_ite(stemmatized[0] + 'ить'):
                vowels = ['а', 'о', 'у', 'ы', 'э', 'я', 'ё', 'ю', 'и', 'е']
                if stemmatized[0][-1] in vowels:
                    ending = 'й'
                else:
                    if stemmatized[0][-2] not in vowels:
                        ending = 'и'
                    else:
                        ending = 'ь'
                word_form = stemmatized[0] + \
                            end_postfix(transform_verb_ending(stemmatized[0], end[gram_pos].replace('и', ending)), postfix)
            else:
                word_form = stemmatized[0] + end_postfix(transform_verb_ending(stemmatized[0], end[gram_pos]), postfix)
        else:
            word_form = stemmatized[0] + end_postfix(transform_verb_ending(stemmatized[0], end[gram_pos]), postfix)
    else:
        word_form = stemmatized[1] + end_postfix(end[gram_pos], postfix)
    return word_form


def v5(stemmatized, gram_pos, postfix):
    end = ['ть', 'ю', 'ишь', 'ит', 'им', 'ите', 'ят', 'л', 'ла', 'ло', 'ли', 'и', 'ите', 'им', 'я', 'в', 'ящий', 'имый', 'вший', 'нный']
    if gram_pos == 1:
        stem = transform_dent_to_sib(stemmatized[0])
        if if_labial_2(stemmatized[0], 1):
            word_form = stem + 'л' + end_postfix(transform_verb_ending(stem, end[gram_pos]), postfix)
        else:
            word_form = stem + end_postfix(transform_verb_ending(stem, end[gram_pos]), postfix)
    elif gram_pos == 6:
        word_form = stemmatized[0] + end_postfix(transform_verb_ending(stemmatized[0], end[gram_pos]), postfix)
    elif (gram_pos < 6 and gram_pos != 0) or gram_pos in [13, 16, 17]:
        word_form = stemmatized[0] + end_postfix(end[gram_pos], postfix)
    elif gram_pos in [11, 12]:
        if stemmatized[0][-1] in ['а', 'о', 'у', 'ы', 'э', 'я', 'ё', 'ю', 'и', 'е']:
            word_form = stemmatized[0] + \
                        end_postfix(transform_verb_ending(stemmatized[0], end[gram_pos].replace('и', 'й')), postfix)
        elif if_imper_ite(stemmatized[1] + end_postfix(end[0], postfix)):
            word_form = stemmatized[0] + \
                        end_postfix(transform_verb_ending(stemmatized[0], end[gram_pos].replace('и', 'ь')), postfix)
        else:
            word_form = stemmatized[0] + end_postfix(end[gram_pos], postfix)
    elif gram_pos == 14:
        word_form = stemmatized[0] + end_postfix(transform_verb_ending(stemmatized[0], end[gram_pos]), postfix)
    else:
        word_form = stemmatized[1] + end_postfix(end[gram_pos], postfix)
    return word_form


def v6(stemmatized, gram_pos, postfix):
    end = ['ть', 'ю', 'ешь', 'ет', 'ем', 'ете', 'ют', 'л', 'ла', 'ло', 'ли', 'и', 'ите', 'ем', 'я', 'в', 'ющий', 'емый', 'вший', 'нный']
    if (gram_pos <= 6 and gram_pos != 0) or gram_pos in [11, 12, 13, 14, 16, 17]:
        stem = transform_dent_to_sib(stemmatized[0])
        stem = transform_vel_to_sib(stem)
        if gram_pos in [11, 12]:
            if stemmatized[0][-1] in ['а', 'о', 'у', 'ы', 'э', 'я', 'ё', 'ю', 'и', 'е']:
                word_form = stemmatized[0] + \
                            end_postfix(transform_verb_ending(stemmatized[0], end[gram_pos].replace('и', 'й')), postfix)
            else:
                word_form = stem + end_postfix(end[gram_pos], postfix)
        elif if_labial_3(stemmatized[0], 1):
            word_form = stem + 'л' + end_postfix(end[gram_pos], postfix)
        else:
            word_form = stem + end_postfix(transform_verb_ending(stem, end[gram_pos]), postfix)
    else:
        word_form = stemmatized[1] + end_postfix(end[gram_pos], postfix)
    return word_form


def v7(stemmatized, gram_pos, postfix):
    end = ['ти', 'у', 'ешь', 'ет', 'ем', 'ете', 'ут', '', 'ла', 'ло', 'ли', 'и', 'ите', 'ем', 'я', 'ши', 'ущий', 'омый', 'ший', 'енный']
    if gram_pos == 0:
        if if_inf_t_ending(stemmatized[0] + 'ть'):
            word_form = stemmatized[0] + end_postfix('ть', postfix)
        else:
            word_form = stemmatized[0] + end_postfix(end[gram_pos], postfix)
    else:
        if gram_pos in [11, 12] and stemmatized[0].endswith('лез'):
            word_form = stemmatized[0] + end_postfix(end[gram_pos].replace('и', 'ь'), postfix)
        else:
            word_form = stemmatized[0] + end_postfix(end[gram_pos], postfix)
    return word_form


def v7b(stemmatized, gram_pos, postfix):
    end = ['сти', 'у', 'ешь', 'ет', 'ем', 'ете', 'ут', '', 'ла', 'ло', 'ли', 'и', 'ите', 'ем', 'я', 'я', 'ущий', 'омый', 'ший', 'енный']
    if gram_pos != 0:
        word_form = stemmatized[0] + end_postfix(end[gram_pos], postfix)
    else:
        word_form = stemmatized[1] + end_postfix(end[gram_pos], postfix)
    return word_form


def v7d(stemmatized, gram_pos, postfix):
    end = ['сти', 'у', 'ешь', 'ет', 'ем', 'ете', 'ут', 'л', 'ла', 'ло', 'ли', 'и', 'ите', 'ем', 'я', 'я', 'ущий', 'омый', 'ший', 'енный']
    if (gram_pos <= 6 and gram_pos != 0) or gram_pos >= 11:
        word_form = stemmatized[0] + end_postfix(end[gram_pos], postfix)
    elif gram_pos == 0:
        if if_inf_t_ending(stemmatized[1] + 'сть'):
            word_form = stemmatized[1] + end_postfix('сть', postfix)
        else:
            word_form = stemmatized[1] + end_postfix(end[gram_pos], postfix)
    else:
        word_form = stemmatized[1] + end_postfix(end[gram_pos], postfix)
    return word_form


def v7t(stemmatized, gram_pos, postfix):
    end = ['сти', 'у', 'ешь', 'ет', 'ем', 'ете', 'ут', 'л', 'ла', 'ло', 'ли', 'и', 'ите', 'ем', 'я', 'я', 'ущий', 'омый', 'ший', 'енный']
    if (gram_pos <= 6 and gram_pos != 0) or gram_pos >= 11:
        word_form = stemmatized[0] + end_postfix(end[gram_pos], postfix)
    elif gram_pos == 0:
        if if_inf_t_ending(stemmatized[1] + 'сть'):
            word_form = stemmatized[1] + end_postfix('сть', postfix)
        else:
            word_form = stemmatized[1] + end_postfix(end[gram_pos], postfix)
    else:
        word_form = stemmatized[1] + end_postfix(end[gram_pos], postfix)
    return word_form


def v8g(stemmatized, gram_pos, postfix):
    end = ['чь', 'у', 'ешь', 'ет', 'ем', 'ете', 'ут', '', 'ла', 'ло', 'ли', 'и', 'ите', 'ем', '*', 'ши', 'ущий', '*', 'ший', 'енный']
    if gram_pos == 1 or (gram_pos >= 6 and gram_pos not in [13, 19]):
        word_form = stemmatized[0] + end_postfix(end[gram_pos], postfix)
    elif gram_pos == 0:
        word_form = stemmatized[0][:-1] + end_postfix(end[gram_pos], postfix)
    else:
        word_form = stemmatized[1] + end_postfix(end[gram_pos], postfix)
    return word_form


def v8k(stemmatized, gram_pos, postfix):
    end = ['чь', 'у', 'ешь', 'ет', 'ем', 'ете', 'ут', '', 'ла', 'ло', 'ли', 'и', 'ите', 'ем', '*', 'ши', 'ущий', '*', 'ший', 'енный']
    if gram_pos == 1 or (gram_pos >= 6 and gram_pos not in [13, 19]):
        word_form = stemmatized[0] + end_postfix(end[gram_pos], postfix)
    elif gram_pos == 0:
        word_form = stemmatized[0][:-1] + end_postfix(end[gram_pos], postfix)
    else:
        word_form = stemmatized[1] + end_postfix(end[gram_pos], postfix)
    return word_form


def vowel_prefix(stem):
    prefixes = {
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
    l = len(stem.split('|'))
    if l > 1:
        init_prefix, init_stem = '|'.join(stem.split('|')[:-1]), stem.split('|')[-1]
        last_prefix = init_prefix.split('|')[-1]
        if last_prefix in prefixes.keys():
            return ''.join(init_prefix.split('|')[:-1]) + prefixes[last_prefix] + init_stem
        else:
            return ''.join(init_prefix.split('|')[:-1]) + last_prefix + init_stem
    else:
        return stem


def v9(stemmatized, gram_pos, postfix):
    end = ['еть', 'у', 'ешь', 'ет', 'ем', 'ете', 'ут', '', 'ла', 'ло', 'ли', 'и', 'ите', 'ем', '*', 'ев', 'ущий', '*', 'ший', 'тый']
    if (gram_pos <= 6 and gram_pos != 0) or gram_pos in [11, 12, 13, 16]:
        # word_form = stemmatized[0] + end_postfix(end[gram_pos], postfix)
        word_form = vowel_prefix(stemmatized[0]) + end_postfix(end[gram_pos], postfix)
    else:
        word_form = stemmatized[1] + end_postfix(end[gram_pos], postfix)
    return word_form


def v10(stemmatized, gram_pos, postfix):
    end = ['оть', 'ю', 'ешь', 'ет', 'ем', 'ете', 'ют', 'л', 'ла', 'ло', 'ли', 'и', 'ите', 'ем', 'я', 'в', 'ющий', '*', 'вший', 'тый']
    if gram_pos <= 6 or (gram_pos >= 11 and gram_pos not in [15, 18, 19]):
        word_form = stemmatized[0] + end_postfix(end[gram_pos], postfix)
    else:
        word_form = stemmatized[1] + end_postfix(end[gram_pos], postfix)
    return word_form


def v11(stemmatized, gram_pos, postfix):
    end = ['ть', 'ю', 'ешь', 'ет', 'ем', 'ете', 'ют', 'л', 'ла', 'ло', 'ли', 'ей', 'ейте', 'ем', 'я', 'в', 'ющий', '*', 'вший', 'тый']
    if (gram_pos <= 6 and gram_pos != 0) or gram_pos in [13, 14, 16]:
        word_form = vowel_prefix(stemmatized[0]) + end_postfix(end[gram_pos], postfix)
    elif gram_pos in [11, 12]:
        word_form = stemmatized[0].replace('|', '')[:-1] + end_postfix(end[gram_pos], postfix)
    else:
        word_form = stemmatized[1] + end_postfix(end[gram_pos], postfix)
    return word_form


def v12(stemmatized, gram_pos, postfix):
    end = ['ть', 'ю', 'ешь', 'ет', 'ем', 'ете', 'ют', 'л', 'ла', 'ло', 'ли', 'й', 'йте', 'ем', 'я', 'в', 'ющий', 'емый', 'вший', 'тый']
    if (gram_pos <= 6 and gram_pos != 0) or gram_pos in [11, 12, 13, 14, 16, 17]:
        word_form = stemmatized[0] + end_postfix(end[gram_pos], postfix)
    else:
        word_form = stemmatized[1] + end_postfix(end[gram_pos], postfix)
    return word_form


def v13(stemmatized, gram_pos, postfix):
    end = ['вать', 'ю', 'ешь', 'ет', 'ем', 'ете', 'ют', 'л', 'ла', 'ло', 'ли', 'й', 'йте', 'ем', 'я', 'в', 'ющий', 'емый', 'вший', '*']
    if gram_pos <= 6 or gram_pos in [13, 16]:
        word_form = stemmatized[0] + end_postfix(end[gram_pos], postfix)
    else:
        word_form = stemmatized[1] + end_postfix(end[gram_pos], postfix)
    return word_form


def v14m(stemmatized, gram_pos, postfix):
    end = ['ть', 'у', 'ешь', 'ет', 'ем', 'ете', 'ут', 'л', 'ла', 'ло', 'ли', 'и', 'ите', 'ем', '*', 'в', 'ущий', '*', 'вший', 'тый']
    if (gram_pos <= 6 and gram_pos != 0) or gram_pos in [11, 12, 13, 16]:
        word_form = vowel_prefix(stemmatized[0]) + end_postfix(end[gram_pos], postfix)
    else:
        word_form = stemmatized[1] + end_postfix(end[gram_pos], postfix)
    return word_form


def v14n(stemmatized, gram_pos, postfix):
    end = ['ть', 'у', 'ешь', 'ет', 'ем', 'ете', 'ут', 'л', 'ла', 'ло', 'ли', 'и', 'ите', 'ем', '*', 'в', 'ущий', '*', 'вший', 'тый']
    if (gram_pos <= 6 and gram_pos != 0) or gram_pos in [11, 12, 13, 16]:
        word_form = vowel_prefix(stemmatized[0]) + end_postfix(end[gram_pos], postfix)
    else:
        word_form = stemmatized[1] + end_postfix(end[gram_pos], postfix)
    return word_form


def v15(stemmatized, gram_pos, postfix):
    end = ['ть', 'у', 'ешь', 'ет', 'ем', 'ете', 'ут', 'л', 'ла', 'ло', 'ли', 'ь', 'ьте', 'ем', '*', 'в', '*', '*', 'вший', 'тый']
    if (gram_pos <= 6 and gram_pos != 0) or (gram_pos >= 11 and gram_pos < 14):
        word_form = stemmatized[0] + end_postfix(end[gram_pos], postfix)
    else:
        word_form = stemmatized[1] + end_postfix(end[gram_pos], postfix)
    return word_form


def v16(stemmatized, gram_pos, postfix):
    end = ['ть', 'у', 'ешь', 'ет', 'ем', 'ете', 'ут', 'л', 'ла', 'ло', 'ли', 'и', 'ите', 'ем', 'я', '', 'ущий', '*', 'ший', 'тый']
    if (gram_pos <= 6 and gram_pos != 0) or (gram_pos >= 11 and gram_pos != 19):
        word_form = stemmatized[0] + end_postfix(end[gram_pos], postfix)
    else:
        word_form = stemmatized[1] + end_postfix(end[gram_pos], postfix)
    return word_form


def find_verb_form(parad_type, stemmatized, gram_pos, postfix):
    forms = {
        '1': v1,
        '2': v2,
        '3': v3,
        '4': v4,
        '5': v5,
        '6': v6,
        '7': v7,
        '7б': v7b,
        '7д': v7d,
        '7т': v7t,
        '8г': v8g,
        '8к': v8k,
        '9': v9,
        '10': v10,
        '11': v11,
        '12': v12,
        '13': v13,
        '14м': v14m,
        '14н': v14n,
        '15': v15,
        '16': v16
    }
    return forms[parad_type](stemmatized, gram_pos, postfix) if parad_type in forms.keys() else 'error_in_parads.py'
