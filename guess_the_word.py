from flask import Flask
from flask import render_template, flash, redirect
from flask.ext.wtf import Form
from wtforms import TextField
from wtforms.validators import Required
import wiki_processor
import logging

app = Flask(__name__)
app.config.from_object('config')
logging.basicConfig(level=logging.INFO, filename = 'mylog.log', format = '%(levelname)-8s [%(asctime)s]  %(message)s')
logging.info( 'Step1:start' )

class Env: #переменные окружения - создаются при запуске
    pages_titles, labels, Arr = wiki_processor.make_array()#список заголовков, список уникальных слов, рабочая таблица
    logging.info( 'Step2:creation of word vector' )
    status = "new game"
    
          
class WordForm(Form): #Форма, куда вводится слово
    try_word = TextField('try_word', validators = [Required()])

@app.route('/')#Стартовая страница
def index():
    logging.info( 'Step3:creation of start page' )
    return render_template("main_page.html")


@app.route('/game', methods = ['GET', 'POST'])#Страница игры
def game():
    num_of_words = 25
    form = WordForm()
    logging.info( 'Step4:creation of form' )
    if Env.status == "new game":
        logging.info( 'Step5: word list creation' )
        Env.page_title, Env.word_list = wiki_processor.give_wordlist(num_of_words, Env.pages_titles, Env.labels, Env.Arr)#один заголовок, и список слов к нему
        logging.info( 'Step5.3: word list reseived' )
        Env.status = "wait for answer"


    if form.validate_on_submit():#если форма отправлена
        logging.info( 'Step6: form is submitted' )
        flash("Ваше слово: " + form.try_word.data)
        flash("Название статьи: " + Env.page_title)
        Env.status = "new game"
        logging.info( 'redirecting to main page' )
        return redirect('/')
    return render_template("game.html", words = Env.word_list, form=form)


@app.route("/help")
def hello():
    return render_template("help_page.html")

app.run()
