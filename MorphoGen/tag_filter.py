from .verb import def_tag_pos_part, def_tag_pos_verb
from .adjective import def_tag_pos_adj
from .noun import def_tag_pos_noun


def remove_tags(tag, input_set, values):
    return input_set - {tag + '=' + x for x in values}


def check_tag(tag, input_set, values):
    for t in [tag + '=' + x for x in values]:
        if t in input_set:
            return True
    return False


def def_pos_index(grammemes):
    if 'Pos=' in grammemes:
        if 'Pos=VERB' in grammemes:
            if 'VerbForm=Part' in grammemes:
                pos = 'PART'
                index = def_tag_pos_part(grammemes)
            else:
                pos = 'VERB'
                index = def_tag_pos_verb(grammemes)
        elif 'Pos=NOUN' in grammemes:
            pos = 'NOUN'
            index = def_tag_pos_noun(grammemes)
        elif 'Pos=ADJ' in grammemes:
            pos = 'ADJ'
            index = def_tag_pos_adj(grammemes)
        elif 'Pos=NUM' in grammemes:
            pos = 'NUM'
            index = 'not_available'
        else:
            pos = 'OTHER'
            index = -1

    else:
        if 'VerbForm=' in grammemes:
            if 'VerbForm=Part' in grammemes:
                pos = 'PART'
                index = def_tag_pos_part(grammemes)
            else:
                pos = 'VERB'
                index = def_tag_pos_verb(grammemes)
        elif 'Form=' in grammemes or 'Gender=' in grammemes or 'G=' in grammemes:
            pos = 'ADJ'
            index = def_tag_pos_adj(grammemes)
        elif 'Case=' in grammemes:
            pos = 'NOUN'
            index = def_tag_pos_noun(grammemes)
        else:
            pos = 'OTHER'
            index = -1
    return pos, index
