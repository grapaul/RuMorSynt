import os
import argparse

from timeit import default_timer as timer
from morphological_analyzer.analyzer import Analyzer
import nltk
import tag_cleaning
from tag_cleaning import tag_clean
from nltk import tag, word_tokenize
from nltk.tag import pos_tag


def tokenize(inp_text):
    for line in inp_text:
        sentences = nltk.sent_tokenize(line, language="russian")
        for sentence in sentences:
            n = pos_tag(word_tokenize(sentence), lang='rus')
            tag_clean(n)
            cp = nltk.RegexpParser(grammar)
            result = cp.parse(n)



if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='MLT')
    parser.add_argument('--input', type=str, default=os.path.join('/mnt/sda/Data/7_Vsachina/Jobs/MTS/NewPlat/Morph/ML_Postagger/PG/txt.txt'), help='Path to input text file')
    parser.add_argument('--output', type=str, default=os.path.join('/mnt/sda/Data/7_Vsachina/Jobs/MTS/NewPlat/Morph/ML_Postagger/PG/out.txt'), help='Output file path')

    args = parser.parse_args()
    input_path = args.input
    output_path = args.output

    print('Loading ML tagger models...')
    if False:
        tagger = Analyzer(models_names=models_names,
                           path_to_models='/home/inkoziev/mts/morph_analyzer/morph_analyzer/models/indent_x5_models/', \
                           path_to_fasttext='/home/inkoziev/mts/morph_analyzer/morph_analyzer/package/cc.ru.300.bin',
                           prediction_template=prediction_template, models_variant=1)
        tagger.load_models()
    else:
        path_to_config = '/mnt/sda/Data/7_Vsachina/Jobs/MTS/NewPlat/Morph/ML_Postagger/bert/config.json'
        path_to_model = '/mnt/sda/Data/7_Vsachina/Jobs/MTS/NewPlat/Morph/ML_Postagger/bert/pytorch_model.bin'
        path_to_normal_forms_dict = '/mnt/sda/Data/7_Vsachina/Jobs/MTS/NewPlat/Morph/ML_Postagger/morph_analyzer/bert_package/analyzer_package/morphological_analyzer/normal_forms.json'
        tagger = Analyzer(path_to_model, path_to_config, path_to_normal_forms_dict, normalform_required=True)

    start = timer()

    with open(output_path, 'w', encoding='utf-8') as wrt:
        with open(input_path, 'r', encoding='utf-8') as inp:
            sents = inp.readlines()
            for s in sents:
                tokens = s.replace(',','').replace(':','').replace(';','').replace('\n', '').split(' ')
                tagsets = tagger.predict(tokens)
                wrt.write(tagsets.replace('\n\n', '\n') + '\n\n')

    end = timer()
    elapsed_sec = (end - start)
    print('elapsed time={} sec'.format(elapsed_sec))

