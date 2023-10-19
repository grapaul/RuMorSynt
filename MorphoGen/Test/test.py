from MorphoGen.Test.autotest import *

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='MGenerate')
    parser.add_argument('--input_morph', type=str, default='MorphoGen/dictis/GPron.txt', help='morphology for Pronouns')
    parser.add_argument('--input_lemmas', type=str, default='MorphoGen/dictis/lemmas.txt', help='morphology for Lemmas')
    parser.add_argument('--morph_const', type=str, default='MorphoGen/dictis/morph_const.txt', help='morphological constants')

    args = parser.parse_args()
    input_path_morph = args.input_morph
    lemmas_path = args.input_lemmas
    morph_constants_path = args.morph_const

    g = MorphoGen.gen_morph_api.GenMorphApi(dict_dir='./MorphoGen/dictis', gpron_path=args.input_morph,
                                            lemmas_path=args.input_lemmas, constants_path=args.morph_const)

    not_found = open('MorphoGen/Test/not_found.txt', 'w', encoding='utf-8')
    log_mistakes = open('MorphoGen/Test/log_mistakes.txt', 'w', encoding='utf-8')
    log_mistakes.write('Lemma\tGenerated form\tCorrect form\tParad.type\tTags\n')

    print('Process words beginning with: [enter the pattern]')
    filter_string = input()

    if False:
        correct_wf_count, wf_count, not_found_form = process_test(g, 'MorphoGen/dictis/allNOUNS.txt',
                                                                  not_found, log_mistakes, filter=filter_string)
    else:
        correct_wf_count, wf_count, not_found_form = process_test(g, 'MorphoGen/dictis/allVERBS.txt',
                                                                  not_found, log_mistakes, filter=filter_string)

    wf_count -= len(not_found_form)
    print('Correct word forms rate: {}% ({}/{})'.format(round((100 * correct_wf_count / wf_count), 2), correct_wf_count, wf_count))
    print('Not found words: {}'.format(len(not_found_form)))

    not_found.close()
    log_mistakes.close()
