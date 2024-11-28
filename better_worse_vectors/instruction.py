import nltk
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer as wnl
from string import punctuation
import torch
from torch.utils.data import DataLoader
import pandas as pd
import pickle
import json
# здесь импорты, включая нужные для работы с датафреймами

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

def better_worse_vectorise(text, vec_dict, n): -> str
    """Принимает на вход целый текст, сохраняет вектор строкой, 
    чтобы его "разбить", нужно сплитить по ';' """
    measures = []
    lemmas = to_lemmas(text)
    for lemma in lemmas:
        if vec_dict.get(lemma) is not None:
            measures.append(vec_dict[lemma])
        else:
            measures.append(0.0)
    mn = list(sorted(measures, key=lambda x: abs(x), reverse=True))
    while len(mn) < n:
        mn.append(0.0)
    return ";".join(str(m) for m in mn[0:n])

with open('gb_dict.json', 'r') as json_file1:
    gb_dict = json.load(json_file1)

with open('pr_dict.json', 'r') as json_file2:
    pr_dict = json.load(json_file2)


# и вот этим кодом можно удобно пробежаться по датасету и сделать новые векторизованные столбцы:
new_df['gb_vector'] = new_df.apply(lambda x: better_worse_vectorise(x.text, gb_dict, 15), axis=1)
new_df['pr_vector'] = new_df.apply(lambda x: better_worse_vectorise(x.text, pr_dict, 15), axis=1)
