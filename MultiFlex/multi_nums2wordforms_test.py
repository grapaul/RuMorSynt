import argparse
from MultiFlex.multi_nums2wordforms import *

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='MGIterateTest')
    parser.add_argument('--lemma2change', type=str, default='двадцать четыре', help='lemma for generation')
    parser.add_argument('--gram', type=str, default='Case=Ins', help='gramform for generation')
    parser.add_argument('--test', type=str, default='MultiFlex/test_obligatory.txt', help='test content')
    parser.add_argument('--debug', type=bool, default=True)
    args = parser.parse_args()
    lemma_value = args.lemma2change.replace('Ё', 'Е').replace('ё', 'е')
    tags = args.gram
    tst = args.test
    dbg = args.debug

    if dbg:
        wf_list = lemma_value.split(' ')
        new_wf_list = make_inflect(wf_list, tags)
        print('Input=\t' + str(lemma_value) + ';\tTags=\t' + tags)
        print('\tOutput=' + str(new_wf_list))

    else:
        wrt = open('MultiFlex/test_results.txt', 'w', encoding='utf-8')
        all_lines = 0
        success_lines = 0
        ftest = open(tst, "r", encoding='utf-8')
        tst_lines = ftest.read().split('\n')

        for l in tst_lines:
            if len(l) > 3:
                tags = l.split('\t')[1]
                tags = tags.replace('Nom', 'Case=Nom').replace('Acc', 'Case=Acc').replace('Gen', 'Case=Gen').replace('Dat', 'Case=Dat').replace('Ins', 'Case=Ins').replace('Loc', 'Case=Loc')
                tags = tags.replace('Sing', 'Number=Sing').replace('Plur', 'Number=Plur')
                tags = tags.replace('Anim', 'Animacy=Anim').replace('Inan', 'Animacy=Inan')
                tags = tags.replace('Masc', 'Gender=Masc').replace('Fem', 'Gender=Fem').replace('Neut', 'Gender=Neut')
                wf_list = l.split('\t')[0].split(' ')
                wf_list_expected = l.split('\t')[2].split(' ')
                new_wf_list = make_inflect(wf_list, tags)
                i = 0
                for w in new_wf_list:
                    if w == wf_list_expected[new_wf_list.index(w)]:
                        i += 1
                if i == len(new_wf_list):
                    success_lines += 1
                    wrt.write('Input=\t' + str(l.split('\t')[0].split(' ')) + ';\tTags=\t' + tags + '\n')
                    wrt.write('\tOutput Success=' + str(new_wf_list) + '\n\n')
                else:
                    wrt.write('Input=\t' + str(l.split('\t')[0].split(' ')) + ';\tTags=\t' + tags + '\n')
                    wrt.write('\tExpected=' + str(wf_list_expected) + '\n')
                    wrt.write('\tOutput Fail=' + str(new_wf_list) + '\n\n')

                all_lines += 1
        prcnt_correct = success_lines/all_lines
        wrt.write('\tCaptured=' + str(prcnt_correct) + ';\toverall tests =' + str(all_lines) + '\n\n')
        print('\tCaptured=' + str(prcnt_correct) + ';\toverall tests =' + str(all_lines) + '\n\n')
        wrt.close()
        if tst == 'MultiFlex/test_obligatory.txt':
            if prcnt_correct != 1:
                exit(1)


#    for nwf in new_wf_list:
#        wrt.write(wf_list[new_wf_list.index(nwf)] + '\t' + nwf + '\t' + tags + '\n')
#        print(wf_list[new_wf_list.index(nwf)] + '\t' + nwf + '\t' + tags + '\n')

