import os
import pathlib

import MorphoGen.adjective as mg_adj
import MorphoGen.noun as mg_noun
import MorphoGen.verb as mg_verb
import MorphoGen.trie as mg_trie
import MorphoGen.morphon
from MorphoGen.tag_filter import *
from MorphoGen.dictionaries import *


class GenMorphApi:
    def __init__(self, dict_dir=None, gpron_path=None, lemmas_path=None, constants_path=None):
        if dict_dir is None:
            dict_dir = os.path.join(str(pathlib.Path(__file__).resolve().parent), 'dictis')

        self.morphon_obj = MorphoGen.morphon.MorphonDicts()
        self.morphon_obj.load(dict_dir)

        # TODO - потом надо будет закончить рефакторинг, избавиться от этого глобального объекта.
        MorphoGen.morphon.morphon_obj = self.morphon_obj

        if gpron_path is None:
            gpron_path = os.path.join(dict_dir, 'GPron.txt')

        if lemmas_path is None:
            lemmas_path = os.path.join(dict_dir, 'lemmas.txt')
        proper_names_path = os.path.join(dict_dir, 'loc_pers_lemmas.txt')

        if constants_path is None:
            constants_path = os.path.join(dict_dir, 'morph_const.txt')

        self.dict_p = read_gpron(gpron_path)
        self.lemmas_dict = read_lemmas_and_proper(lemmas_path, proper_names_path)
        self.const_list = read_file_to_list(constants_path)

        self.lemmes_trie = mg_trie.TrieNode('*')
        for i in self.lemmas_dict.keys():
            mg_trie.add(self.lemmes_trie, i)

    def produce(self, lemma_value, tags, debug=False, test_output=False):

        # copy tags into the set for standardization
        tags_copied_set = set()
        for tag in tags:
            tags_copied_set.add(tag)

        tags_copied_set, lemma_value = self.clarify_lemma(tags_copied_set, lemma_value)
        tags_copied_set = self.filter_tags(tags_copied_set, lemma_value)

        grammemes = ';'.join(tags_copied_set)
        pos, gram_pos = def_pos_index(grammemes)

        if pos == 'VERB':
            parad_type, found_dict, word_form, prefix, postfix, form_accept = mg_verb.define_parad_type_verb(self.dict_p, lemma_value,
                                                                                                             grammemes, self.lemmas_dict,
                                                                                                             self.lemmes_trie)
            stemmatized = mg_verb.stemmatize_verb(lemma_value, parad_type, postfix)
            if test_output is False:
                return mg_verb.generate_verb_wf(parad_type, stemmatized, prefix, postfix, gram_pos, grammemes, word_form,
                                            found_dict, form_accept, debug=debug)
            else:
                return mg_verb.generate_verb_wf(parad_type, stemmatized, prefix, postfix, gram_pos, grammemes, word_form,
                                            found_dict, form_accept, debug=debug), pos, parad_type

        elif pos == 'NOUN':
            word_form, found_dict, parad_type, tantum = mg_noun.define_parad_type(self.dict_p, lemma_value, grammemes,
                                                                          self.lemmas_dict, self.lemmes_trie)
            stemmatized = mg_noun.stemmatize(lemma_value, parad_type)
            if test_output is False:
                return mg_noun.generate_wf(found_dict, word_form, parad_type, tantum, grammemes, stemmatized, lemma_value,
                                       self.const_list, gram_pos, debug=debug)
            else:
                return mg_noun.generate_wf(found_dict, word_form, parad_type, tantum, grammemes, stemmatized, lemma_value,
                                       self.const_list, gram_pos, debug=debug), pos, parad_type
                                       
        elif pos == 'NUM':
            word_form = search_tags_dict(self.dict_p, lemma_value, grammemes)[0]
            if test_output is False:
                return word_form
            else:
                return word_form, pos, ''

        elif pos == 'ADJ':
            word_form_exception = search_tags_dict(self.dict_p, lemma_value, grammemes)[0]
            if word_form_exception:
                if debug:
                    print('\tFound adj WFs: ' + word_form_exception)
                if test_output:
                    return word_form_exception, pos, ''
                else:
                    return word_form_exception
            else:
                parad_type, stemmatized = mg_adj.guess_adj_stem(lemma_value)
                if test_output:
                    return mg_adj.generate_adj_wf(gram_pos, grammemes, parad_type, stemmatized, debug=debug), pos, parad_type
                else:
                    return mg_adj.generate_adj_wf(gram_pos, grammemes, parad_type, stemmatized, debug=debug)

        elif pos == 'PART':
            parad_type, found_dict, word_form, prefix, postfix, form_accept = mg_verb.define_parad_type_verb(self.dict_p, lemma_value,
                                                                                                             grammemes, self.lemmas_dict,
                                                                                                             self.lemmes_trie)
            stemmatized = mg_verb.stemmatize_verb(lemma_value, parad_type, postfix)

            norm_form = mg_verb.generate_verb_wf(parad_type, stemmatized, prefix, postfix, gram_pos, grammemes,
                                                 word_form, found_dict, form_accept, debug=False)
            gram_pos = mg_adj.def_tag_pos_adj(grammemes)
            parad_type, stemmatized = mg_adj.guess_adj_stem(norm_form)
            if test_output is False:
                return mg_adj.generate_adj_wf(gram_pos, grammemes, parad_type, stemmatized, debug=debug)
            else:
                return mg_adj.generate_adj_wf(gram_pos, grammemes, parad_type, stemmatized, debug=debug), pos, parad_type

        return None

    def filter_tags(self, tags, lemma_value):  # убирает лишние теги из входного запроса
        animacy = ['Anim', 'Inan']
        tense = ['Pres', 'Fut', 'Past']
        voice = ['Act', 'Pass']
        aspect = ['Imp', 'Perf']
        case = ['Nom', 'Gen', 'Dat', 'Acc', 'Ins', 'Loc', 'Voc']
        gender = ['Masc', 'Fem', 'Neut']
        mood = ['Ind', 'Imp']
        number = ['Sing', 'Plur']
        person = ['1', '2', '3']

        # для всех частей речи: удаляем род для множественного числа
        if 'Number=Plur' in tags:
            remove_tags('Gender', tags, gender)

        if 'Pos=VERB' in tags:
            tags = remove_tags('Aspect', tags, aspect)

            # меняем тег времени на Tense=Pres
            if 'Tense=Fut' in tags:
                tags = remove_tags('Tense', tags, tense)
                tags.add('Tense=Pres')

            # удаление падежа для НЕпричастий
            if "VerbForm=Part" not in tags:
                tags = remove_tags('Case', tags, case)
                # удаление рода для прошедшего времени
                if 'Tense=Past' not in tags:
                    tags = remove_tags('Gender', tags, gender)

            # удаление числа, наклонения, рода и лица для деепричастий
            if 'VerbForm=Conv' in tags:
                tags = remove_tags('Number', tags, number)
                tags = remove_tags('Mood', tags, mood)
                tags = remove_tags('Gender', tags, gender)
                tags = remove_tags('Person', tags, person)

            if not check_tag('VerbForm', tags, ['Fin', 'Part', 'Conv']):
                tags.add('VerbForm=Inf')

            elif 'VerbForm=Fin' in tags:
                if not check_tag('Mood', tags, mood):
                    tags.add('Mood=Ind')
                if not check_tag('Number', tags, number):
                    tags.add('Number=Sing')
                if not check_tag('Tense', tags, tense) and 'Mood=Ind' in tags:
                    tags.add('Tense=Pres')
                if not check_tag('Person', tags, person) and 'Tense=Pres' in tags:
                    tags.add('Person=3')
                if not check_tag('Gender', tags, gender) and 'Tense=Past' in tags and 'Number=Plur' not in tags:
                    tags.add('Gender=Masc')

            elif 'VerbForm=Conv' in tags:
                if not check_tag('Tense', tags, tense):
                    tags.add('Tense=Pres')

            elif 'VerbForm=Part' in tags:
                if not check_tag('Case', tags, case):
                    tags.add('Case=Nom')
                if not check_tag('Number', tags, number):
                    tags.add('Number=Sing')
                if not check_tag('Gender', tags, gender) and 'Number=Plur' not in tags:
                    tags.add('Gender=Masc')
                if not check_tag('Tense', tags, tense):
                    tags.add('Tense=Pres')
                if not check_tag('Voice', tags, voice):
                    tags.add('Voice=Act')

        elif 'Pos=ADJ' in tags:
            # любые теги прилагательных при Degree=Cmp
            if 'Degree=Cmp' in tags:
                tags = {'Pos=ADJ', 'Degree=Cmp'}

            elif 'Variant=Short' in tags:
                tags = remove_tags('Case', tags, case)

                # добавляем род, если нет
                if not check_tag('Gender', tags, gender) and 'Number=Plur' not in tags:
                    tags.add('Gender=Masc')

            else:
                # добавляем число, если нет
                if not check_tag('Number', tags, number):
                    tags.add('Number=Sing')

                # добавляем род, если нет
                if not check_tag('Gender', tags, gender) and 'Number=Plur' not in tags:
                    tags.add('Gender=Masc')
                elif check_tag('Gender', tags, gender) and 'Number=Plur' in tags:
                    tags = remove_tags('Gender', tags, gender)

                # добавляем падеж, если нет
                if not check_tag('Case', tags, case):
                    tags.add('Case=Nom')

        elif 'Pos=NOUN' in tags:
            # убираем род для существительных
            tags = remove_tags('Gender', tags, gender)

            # добавляем число, если нет
            if not check_tag('Number', tags, number):
                tags.add('Number=Sing')

            # добавляем падеж, если нет
            if not check_tag('Case', tags, case):
                tags.add('Case=Nom')

        elif 'Pos=NUM' in tags:
            if not check_tag('Case', tags, case):
                tags.add('Case=Nom')

            if lemma_value in ['один', 'одна']:
                # одушевленность для числительного один
                if ('Case=Acc' not in tags or 'Gender=Masc' not in tags) and 'Number=Plur' not in tags:
                    tags = remove_tags('Animacy', tags, animacy)

            elif lemma_value in ['два', 'оба']:
                # удаляем число для числительного два
                tags = remove_tags('Number', tags, number)

                # одушевленность для числительного два
                if 'Case=Acc' not in tags:
                    tags = remove_tags('Animacy', tags, animacy)

                # род для числительного два
                if lemma_value == 'два' and not check_tag('Case', tags, ['Nom', 'Acc']):
                    tags = remove_tags('Gender', tags, gender)

            # любые теги кроме падежа для числительных 3,4
            elif lemma_value in ['три', 'четыре', 'двое', 'трое',
                                 'четверо', 'пятеро', 'шестеро',
                                 'семеро', 'восьмеро', 'девятеро',
                                 'десятеро', 'одиннадцатеро', 'двенадцатеро']:
                if 'Case=Acc' in tags and 'Animacy=Anim' in tags:
                    tags = {'Pos=NUM', 'Case=Acc', 'Animacy=Anim'}
                elif 'Case=Acc' in tags and 'Animacy=Inan' in tags:
                    tags = {'Pos=NUM', 'Case=Acc', 'Animacy=Inan'}
                elif 'Case=Acc' in tags and 'Animacy=Anim' not in tags and 'Animacy=Inan' not in tags:
                    tags = {'Pos=NUM', 'Case=Acc', 'Animacy=Inan'}
                else:
                    current_case = None
                    for c in case:
                        if 'Case=' + c in tags:
                            current_case = c
                            break
                    if current_case:
                        tags = {'Pos=NUM', 'Case=' + current_case}
                    else:
                        tags = {'Pos=NUM'}
                tags = remove_tags('Number', tags, number)

            # любые теги кроме падежа для "больших" числительных
            elif lemma_value not in ['один', 'два', 'три', 'четыре']:
                for i in case:
                    if ('Case=' + i) in tags:
                        tags = {'Pos=NUM', 'Case=' + i}

            if lemma_value == 'один' and 'Case=Acc' in tags and 'Gender=Masc' in tags and not check_tag('Animacy', tags, animacy):
                tags.add('Animacy=Inan')
            elif lemma_value != 'один' and 'Case=Acc' in tags and not check_tag('Animacy', tags, animacy):
                tags.add('Animacy=Inan')

        return tags

    def clarify_lemma(self, tags, lemma_value):  # правит нормформы, где постеги могут ошибиться и т.п. (тысяча,...)
        num_nouns = ['одна', 'одно', 'тысяча', 'тысяч', 'тысячи', 'миллион', 'миллиона', 'миллионов', 'миллион',
                     'миллиона', 'миллионов',
                     'миллиард', 'миллиарда', 'миллиардов', 'триллион', 'триллиона', 'триллионов', 'септиллион',
                     'септиллиона', 'септиллионов', 'квадриллион', 'квадриллиона', 'квадриллионов']
        if lemma_value in num_nouns:
            if 'Pos=NUM' in tags:
                tags.remove('Pos=NUM')
                tags.add('Pos=NOUN')
            if lemma_value in ['тысяч', 'тысячи']:
                lemma_value = 'тысяча'
            elif lemma_value in ['миллиона', 'миллионов']:
                lemma_value = 'миллион'
            elif lemma_value in ['миллиарда', 'миллиардов']:
                lemma_value = 'миллиард'
            elif lemma_value in ['триллиона', 'триллионов']:
                lemma_value = 'триллион'
            elif lemma_value in ['септиллиона', 'септиллионов']:
                lemma_value = 'септиллион'
            elif lemma_value in ['квадриллиона', 'квадриллионов']:
                lemma_value = 'квадриллион'
        elif lemma_value in ['две', 'обе']:
            if lemma_value == 'две':
                lemma_value = 'два'
            elif lemma_value == 'обе':
                lemma_value = 'оба'
        elif lemma_value in ['одна', 'одно']:
            lemma_value = 'один'

        return tags, lemma_value


if __name__ == '__main__':
    g = GenMorphApi(dict_dir='./MorphoGen/dictis')
    form = g.produce(lemma_value="синий", tags="Plur;Acc;Inan".split(';'))
    print(form)
