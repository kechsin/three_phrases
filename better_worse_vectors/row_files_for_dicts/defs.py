import nltk
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer as wnl
import collections as coll
from string import punctuation
import json

def to_lemmas(text) -> list:
    """Принимает на вход строку-текст, убирает пунктуацию,
    приводит к нижнему регистру, приводит к списку начальных форм"""
    lemmas = []
    text = text.replace("\n", " ")
    tokens = [word.lower().strip(punctuation) for word in text.split(" ")]
    tokens = [word for word in tokens if word != '']
    # на всякий случай проверяем, чтобы не было пустых слов, получившихся
    # из-за двух пробельных символов подряд
    lemmas = [str(wnl().lemmatize(word)) for word in tokens]
    return lemmas

def create_measure_dict(better_list, worse_list):
    better_dict = coll.Counter(better_list)
    worse_dict = coll.Counter(worse_list)

    set_better = set(better_dict.keys())
    set_worse = set(worse_dict.keys())

    common = set_worse & set_better
    worses = set_worse - set_better
    betters = set_better - set_worse

    measure_dict = {}
    for k, v in better_dict.items():
        if k in betters:
            measure_dict[k] = 1
        elif k in common:
            measure_dict[k] = round((v - worse_dict[k]) / (v + worse_dict[k]), 3)
    for k, v in worse_dict.items():
        if k in worses:
            measure_dict[k] = -1
    return measure_dict

with open("main_ch.txt", "r", encoding="UTF-8") as g:
    good_list = to_lemmas(g.read())

with open("minor_ch.txt", "r", encoding="UTF-8") as b:
    bad_list = to_lemmas(b.read())

gb_dict = create_measure_dict(good_list, bad_list)

with open("good.txt", "r", encoding="UTF-8") as im:
    imp_list = to_lemmas(im.read())

with open("bad.txt", "r", encoding="UTF-8") as no:
    not_imp_list = to_lemmas(no.read())

pr_dict = create_measure_dict(imp_list, not_imp_list)

with open('gb_dict.json', 'w') as outfile1:
    json.dump(gb_dict, outfile1, ensure_ascii=False)

with open('pr_dict.json', 'w') as outfile2:
    json.dump(pr_dict, outfile2, ensure_ascii=False)
