#import wikipedia as wp
from sklearn.feature_extraction.text import TfidfVectorizer as TV
from nltk.tokenize import RegexpTokenizer
import pymorphy2
import numpy
import wiki_good_articles as wp
from random import randint

class LemmaTokenizer(object):#выделяем слова, без цифр, без латинницы
    tokenizer = RegexpTokenizer('[а-яА-ЯЁёіІ’їЇєЄҐґЎў]{4,}')
    def __init__(self):
        self.wnl = pymorphy2.MorphAnalyzer()
    def __call__(self, doc):
        return [self.wnl.parse(w if w.find('править') == -1 else w[:-7])[0].normal_form for w in LemmaTokenizer.tokenizer.tokenize(doc)]

def make_array(num_of_pages=100, min_links=5, min_lenth=3000, max_word=1):#создаём и заполняем вектор слов
    all_pages, pages_titles = wp.give_articles(num_of_pages)
    vect = TV(tokenizer=LemmaTokenizer(), max_df=int(max_word), min_df=0)
    X_train = vect.fit_transform(all_pages)
    labels = numpy.array(vect.get_feature_names())
    Arr = X_train.A
    return pages_titles, labels, Arr




def give_wordlist(words_am, pages_title, labels, Arr):#Для одной из статей выводим характерные слова
    i = randint(0, len(pages_title)-1)
    ind = numpy.argsort(Arr[i])[-(words_am + 10):]
    l = labels[ind]
    title = pages_title[i]
    for word in l:
        if (title.lower()).find(word) != -1 or word.find(title.lower()) != -1:
            l.remove(word)
    l = l[-words_am:]
    with wp.shelve.open("articles", writeback = True) as d:
        del d[pages_title[i]]
    return title, l
