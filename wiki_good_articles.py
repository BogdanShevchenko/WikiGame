import wikipedia as wp
import random
import warnings
import shelve

exclude_t = ['VIAF','Россия','ISO','UTC+3','Страна', 'Москва', "Викисклад", "Викитека", 'Викисловарь']
warnings.filterwarnings("ignore")
wp.set_lang("ru")
articles_file = shelve.open("articles", writeback = True)
def give_articles(num, min_links=5, min_lenth=3000, max_word=1, exclude_titles=exclude_t):
    all_pages = []
    pages_title = []
    for i in articles_file:
        if len(pages_title)<num:
            pages_title.append(i)
            all_pages.append(articles_file[i])
        
    while len(all_pages) < num:
        try:
            new_rand = wp.random(pages=1)
            lnk = wp.WikipediaPage(new_rand).links
            if len(lnk) > min_links:
                temp_title = random.choice(lnk)
                temp_content = wp.WikipediaPage(temp_title).content
                if len(temp_title.split()) <= max_word and not(temp_title.isdigit()) and not(temp_title in exclude_titles) and not(temp_title in pages_title) and len(temp_content) > min_lenth:#
                    all_pages.append(temp_content)
                    pages_title.append(temp_title)
                    articles_file[temp_title] = temp_content
                    print("page loaded... ", end = " ")
        except (wp.exceptions.WikipediaException, KeyError, ValueError):
            pass
    return(all_pages, pages_title)


def simple_giver(num, min_links=5, min_lenth=3000, max_word=1, exclude_titles=exclude_t):
    all_pages = []
    pages_title = []
    while len(all_pages) < num_of_pages:
        try:
            temp_title = wp.random(pages=1)
            temp_content = wp.WikipediaPage(temp_title).content
            pages_title.append(temp_title)
            all_pages.append(temp_content)
            print("page loaded... ", end = " ")
        except (wp.exceptions.WikipediaException, KeyError, ValueError):
            pass
    return(all_pages, pages_title)




