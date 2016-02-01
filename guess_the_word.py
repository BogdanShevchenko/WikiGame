from flask import Flask
from flask import render_template, flash, redirect
from flask.ext.wtf import Form
from wtforms import TextField
from wtforms.validators import Required
import wiki_processor


app = Flask(__name__)
app.config.from_object('config')


class Env: #переменные окружения - создаются при запуске
    pages_titles, labels, Arr = wiki_processor.make_array()#список заголовков, список уникальных слов, рабочая таблица
    status = "new game"
    
          
class WordForm(Form): #Форма, куда вводится слово
    try_word = TextField('try_word', validators = [Required()])

@app.route('/')#Стартовая страница
def index():
    return render_template("main_page.html")


@app.route('/game', methods = ['GET', 'POST'])#Страница игры
def game():
    num_of_words = 25
    if Env.status == "new game":
        Env.page_title, word_list = wiki_processor.give_wordlist(num_of_words, Env.pages_titles, Env.labels, Env.Arr)#один заголовок, и список слов к нему
        Env.status = "wait for answer"
    
    form = WordForm()
    if form.validate_on_submit():#если форма отправлена
        flash("Ваше слово: " + form.try_word.data)
        flash("Название статьи: " + Env.page_title)
        Env.status = "new game"
        return redirect('/')
    return render_template("game.html", words = word_list, form=form)


@app.route("/help")
def hello():
    return render_template("help_page.html")

app.run()
