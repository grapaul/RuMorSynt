import re
import argparse

import MorphoGen.gen_morph_api


case_pattern = re.compile('Case=\w{3}')
number_pattern = re.compile('Number=\w{4}')
gender_pattern = re.compile('(G=[^;)]+)[);]')
animacy_pattern = re.compile('Animacy=\w{4}')
short_pattern = re.compile('Form=Short')


def extract_case(tag_line):
    m = re.findall(case_pattern, tag_line)
    if m:
        return m[0]
    else:
        return '<<UNK_CASE>>'


def extract_number(tag_line):
    m = re.findall(number_pattern, tag_line)
    if m:
        return m[0]
    else:
        return '<<UNK_NUMBER>>'


def extract_tags_noun(tag_line):
    m = re.findall(gender_pattern, tag_line)
    a = re.findall(animacy_pattern, tag_line)

    if 'Short' in tag_line:
        if len(m) > 0:
            return [re.findall(short_pattern, tag_line)[0], extract_number(tag_line), m[0]]
        return [re.findall(short_pattern, tag_line)[0], extract_number(tag_line)]
    if len(m) > 0 and len(a) == 0 and 'Number=Plur' not in tag_line:
        return [m[0], extract_case(tag_line), extract_number(tag_line)]
    elif len(m) > 0 and len(a) > 0 and 'Number=Plur' not in tag_line:
        return [m[0], extract_case(tag_line), extract_number(tag_line), a[0]]
    elif len(a) > 0 and 'Number=Plur' in tag_line:
        return [extract_case(tag_line), extract_number(tag_line), a[0]]

    return [extract_case(tag_line), extract_number(tag_line)]


def extract_tags_verb(tag_line):
    aspect_pattern = re.compile('Aspect=\w{3,4}')
    verbform_pattern = re.compile('VerbForm=\w{3,4}')
    number_pattern = re.compile('Number=\w{4}')
    mood_pattern = re.compile('Mood=\w{3}')
    tense_pattern = re.compile('Tense=\w{3,4}')
    gender_pattern = re.compile('Gender=\w{3,4}')
    person_pattern = re.compile('Person=[123]')

    tag_list = []
    m_aspect = re.findall(aspect_pattern, tag_line)
    if m_aspect:
        aspect = m_aspect[0]
    else:
        print('Отсутствует "{}" в строке с тегами "{}"'.format(aspect_pattern.pattern, tag_line))
        exit(0)

    tag_list.append(aspect)
    verbform = re.findall(verbform_pattern, tag_line)[0]
    tag_list.append(verbform)
    if verbform in ['VerbForm=Fin', 'VerbForm=Conv']:
        m_tense = re.findall(tense_pattern, tag_line)
        if m_tense:
            tense = m_tense[0]
            tag_list.append(tense)
        else:
            tense = ''
        if verbform == 'VerbForm=Fin':
            m_number = re.findall(number_pattern, tag_line)
            if m_number:
                number = m_number[0]
                tag_list.append(number)

            mood = re.findall(mood_pattern, tag_line)[0]
            tag_list.append(mood)

            m_person = re.findall(person_pattern, tag_line)
            if m_person:
                person = m_person[0]
                tag_list.append(person)

            if tense == 'Tense=Past':
                m_gender = re.findall(gender_pattern, tag_line)
                if m_gender:
                    gender = m_gender[0]
                    tag_list.append(gender)
    return tag_list


def process_test(api, path: str, not_found, log_mistakes, debug=False, filter=''):

    len_filter = len(filter)

    with open(path, 'r', encoding='utf-8') as fin:
        lemmas = re.split('\n ?\n ?\n ?', fin.read())
        wf_count = 0
        correct_wf_count = 0
        not_found_form = set()
        for l in lemmas:
            word_nf = l.split('\n')[0].split(' ')[0]
            if word_nf != '' and word_nf[-2:] != 'ие' and word_nf[-1] != 'ы' \
                    and word_nf != '﻿' and word_nf.islower() and '-' not in word_nf:
                if word_nf[:len_filter] == filter:
                    for line in l.split('\n'):
                        if len(line) > 3:
                            word_form = line.split(' ')[0]
                            if word_form[-2:] not in ['ою', 'ею', 'ши'] and \
                                    word_form[-3:] not in ['мте', 'вши', 'рши'] and word_form[-5:] not in ['мтесь', 'вшись', 'ршись']:
                                tags = line.split(' ')[1:]
                                for wf_tag in tags:
                                    if wf_tag and 'Mood=Imp;Person=1' not in wf_tag:
                                        wf_count += 1
                                        all_tags = wf_tag.strip('(').strip(')').split(';')

                                        predicted_form, pos, parad_type = api.produce(word_nf, all_tags, debug=debug, test_output=True)

                                        if predicted_form is None:
                                            if word_nf not in not_found_form:
                                                not_found_form.add(word_nf)
                                                not_found.write(word_nf + '\n')
                                        elif predicted_form != word_form and word_nf[0].islower():
                                                log_mistakes.write('\t'.join((word_nf, predicted_form, word_form,
                                                                                  pos, parad_type, wf_tag)) + '\n')
                                        else:
                                            correct_wf_count += 1
    return correct_wf_count, wf_count, not_found_form


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='MGenerate')
    parser.add_argument('--input_morph', type=str, default='MorphoGen/dictis/GPron.txt', help='morphology for Pronouns')
    parser.add_argument('--input_lemmas', type=str, default='MorphoGen/dictis/lemmas.txt', help='morphology for Lemmas')
    parser.add_argument('--morph_const', type=str, default='MorphoGen/dictis/morph_const.txt', help='morphological constants')

    args = parser.parse_args()
    input_path_morph = args.input_morph
    lemmas_path = args.input_lemmas
    morph_constants_path = args.morph_const

    not_found = open('MorphoGen/Test/not_found.txt', 'w', encoding='utf-8')
    log_mistakes = open('MorphoGen/Test/log_mistakes.txt', 'w', encoding='utf-8')
    log_mistakes.write('Lemma\tGenerated form\tCorrect form\tPOS\tTags\n')

    g = MorphoGen.gen_morph_api.GenMorphApi(dict_dir='./MorphoGen/dictis', gpron_path=args.input_morph,
                                            lemmas_path=args.input_lemmas, constants_path=args.morph_const)

    correct_wf_count, wf_count, not_found_form = process_test(g, 'MorphoGen/Test/autotest.txt', not_found, log_mistakes)

    print('Correct word forms rate: {}% ({}/{})'.format(round(100 * correct_wf_count / wf_count, 4), correct_wf_count,
                                                        wf_count))

    not_found.close()
    log_mistakes.close()

    assert correct_wf_count == wf_count
