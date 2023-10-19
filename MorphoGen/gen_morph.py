import argparse

from MorphoGen.gen_morph_api import GenMorphApi


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='MGenerate')
    parser.add_argument('--input_gpron', type=str, default='MorphoGen/dictis/GPron.txt',
                        help='morphology for Pronouns')
    parser.add_argument('--input_lemmas', type=str, default='MorphoGen/dictis/lemmas.txt',
                        help='morphology for Lemmas')
    parser.add_argument('--morph_const', type=str, default='MorphoGen/dictis/morph_const.txt',
                        help='morphological constants')
    parser.add_argument('--lemma', type=str, default='гелий', help='lemma for generation')
    parser.add_argument('--gram', type=str, default='Pos=NOUN;Case=Ins', help='gramform for generation')

    args = parser.parse_args()

    lemma_value = args.lemma.replace('Ё', 'Е').replace('ё', 'е')

    g = GenMorphApi(dict_dir='./MorphoGen/dictis', gpron_path=args.input_gpron, lemmas_path=args.input_lemmas,
                    constants_path=args.morph_const)
    form = g.produce(lemma_value, args.gram.split(';'), debug=True)
    print('form={}'.format(form))
