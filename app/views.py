from app import app, db
from flask import render_template, request, flash, redirect, session, url_for,abort
from .models import Users, Articles, Tests, Question, Answer,Interpretation, Rezult
import uuid
import os
from werkzeug.utils import secure_filename
from hashlib import md5
from  sqlalchemy.sql.expression import func


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


@app.route('/', methods=['GET', 'POST'])
def index():
    article_random = Articles.query.order_by(func.random()).limit(3).all()
    tests_random = Tests.query.order_by(func.random()).limit(6).all()
    return render_template("index.html",article_random=article_random,tests_random=tests_random)


@app.route('/auth', methods=['GET', 'POST'])
def auth():
    session.pop('name', None)
    if request.method == 'POST':
        email = request.form.get('email')
        password = md5(request.form.get('password').encode()).hexdigest()
        user = Users.query.filter_by(email=email,password=password).first()
        if user:
            session['name'] = Users.query.filter_by(email=email).first().email
            return redirect(url_for("index"))
        else:
            flash("Неправильная почта или пароль!", category="bad")
            return redirect(url_for("auth"))
    return render_template("auth.html")


@app.route('/reg', methods=['GET', 'POST'])
def reg():
    if request.method == 'POST':
        try:
            name = request.form.get('name')
            email = request.form.get('email')
            password = request.form.get('password')
            user = Users(name=name,email=email,password=md5(password.encode()).hexdigest())
            db.session.add(user)
            db.session.commit()
            flash("Регистрация прошла успешно!", category="ok")
            return redirect(url_for("reg"))
        except:
            flash("Произошла ошибка! Проверьте введенные данные!", category="bad")
            db.session.rollback()
            return redirect(url_for("reg"))
    return render_template("regestration.html")


@app.route('/articles', methods=['GET', 'POST'])
def articles():
    articles = Articles.query.all()
    if request.method == 'GET':
        name = request.args.get('seach')
        if name:
            name= name.capitalize()
            title = "%{}%".format(name)
            articles = Articles.query.filter(Articles.title.like(title)).all()
            return render_template("articles.html",articles=articles)
        else:
             return render_template("articles.html",articles=articles)
    return render_template("articles.html",articles=articles)


@app.route('/article/<int:id>', methods=['GET', 'POST'])
def article(id):
    article = Articles.query.get(id)
    if request.method == 'POST':
        article.title = request.form.get('title')
        article.category = request.form.get('category')
        article.text = request.form.get('ckeditor')
        article.color = request.form.get('color')
        image = request.files['image']
        if image:
            filename = secure_filename(image.filename)
            pic_name = str(uuid.uuid4()) + "_" + filename
            image.save("app/static/img/upload/" + pic_name)
            article.image_name = pic_name
        db.session.commit()
        flash("Запись обновлена!", category="ok")
        return redirect(url_for("article", id=article.id))
    return render_template("article.html",article=article)


@app.route('/delete-article/<int:id>')
def delete_article(id):
    obj = Articles.query.filter_by(id=id).first()
    db.session.delete(obj)
    db.session.commit()
    flash("Запись удалена!", category="bad")
    return redirect('/articles')


@app.route('/new-article', methods=['GET', 'POST'])
def new_article():
    pic_name =''
    if request.method == 'POST':
        title = request.form.get('title')
        category = request.form.get('category')
        color = request.form.get('color')
        image = request.files['image']
        if image:
            filename = secure_filename(image.filename)
            pic_name = str(uuid.uuid4()) + "_" + filename
            image.save("app/static/img/upload/" + pic_name)
        text = request.form.get('ckeditor')
        articles = Articles(title=title,color=color,category=category,image_name=pic_name,text=text)
        db.session.add(articles)
        db.session.commit()
        flash("Запись добавлена!", category="ok")
        return redirect(url_for("new_article"))
    return render_template("new-article.html")


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    tests = Tests.query.all()
    if not 'name' in session:
        abort(401)

    total_user = Users.query.filter_by(email=session['name']).first()
    rezult = Rezult.query.filter_by(id_user=total_user.id).all()
    rezult_test_list_id = []
    rezult_test_list = []
    interpretation_list = []

    for el in rezult:
        rezult_test_list_id.append(el.id_test)

    for el in rezult_test_list_id:
        rezult_test_list.append(Tests.query.filter_by(id=el).first())

    for el in rezult_test_list:
        interpretation_list.append(Interpretation.query.filter_by(id_test=el.id).first())

    
    return render_template("profile.html",rezult_test_list=rezult_test_list,rezult=rezult,interpretation_list=interpretation_list,zip=zip)


@app.route('/tests', methods=['GET', 'POST'])
def tests():
    tests = Tests.query.all()

    if request.method == 'GET':
        title = request.args.get('seach')
        if title:
            title= title.capitalize()
            title = "%{}%".format(title)
            tests = Tests.query.filter(Tests.title.like(title)).all()
            return render_template("tests.html",tests=tests)
        else:
             return render_template("tests.html",tests=tests)

    return render_template("tests.html",tests=tests)


@app.route('/test/<int:id>', methods=['GET', 'POST'])
def test(id):
    session['testing'] = 0
    test = Tests.query.get(id)
    questions = Question.query.filter_by(id_test=test.id).all()
    questions_id_list = []
    for el in questions:
        questions_id_list.append(el.id)
    session['testing_questions'] = questions_id_list
    return render_template("test.html",test=test)


@app.route('/edit_test/<int:id>', methods=['GET', 'POST'])
def edit_test(id):
    test = Tests.query.get(id)
    questions = Question.query.filter_by(id_test=test.id).all()
    interpretation = Interpretation.query.filter_by(id_test=test.id).first()
    return render_template("test_edit.html",test=test,questions=questions, interpretation=interpretation)


@app.route('/add_interpretation/<int:id_test>', methods=['GET', 'POST'])
def add_interpretation(id_test):
    test = Tests.query.get(id_test)
    if request.method == 'POST':
        text = request.form.get('ckeditor')
        interpretation = Interpretation(text=text, id_test=test.id)
        db.session.add(interpretation)
        db.session.commit()
        flash("Интерпретация добавлена!", category="ok")
        return redirect(url_for("edit_test", id=test.id))


@app.route('/add_question/<int:id_test>', methods=['GET', 'POST'])
def add_question(id_test):
    test = Tests.query.get(id_test)
    if request.method == 'POST':
        title = request.form.get('title')
        question = Question(title=title, id_test=test.id)
        db.session.add(question)
        db.session.commit()
        flash("Вопрос добавлен!", category="ok")
        return redirect(url_for("edit_test", id=test.id))


@app.route('/edit_question/<int:id_test>/<int:id_question>', methods=['GET', 'POST'])
def edit_question(id_test, id_question):
    question = Question.query.get(id_question)
    if request.method == 'POST':
        question.title = request.form.get('title')
        db.session.commit()
        flash("Вопрос изменен!", category="ok")
        return redirect(url_for("edit_test", id=id_test))
       
    
@app.route('/delete-question/<int:id_test>/<int:id_question>')
def delete_question(id_test, id_question):
    obj = Question.query.filter_by(id=id_question).first()
    db.session.delete(obj)
    db.session.commit()
    flash("Вопрос удален!", category="bad")
    return redirect(url_for("edit_test", id=id_test))


@app.route('/delete-test/<int:id_test>')
def delete_test(id_test):
    obj = Tests.query.filter_by(id=id_test).first()
    db.session.delete(obj)
    db.session.commit()
    flash("Тест удален!", category="bad")
    return redirect(url_for("edit_test"))


@app.route('/new-test', methods=['GET', 'POST'])
def new_test():
    pic_name =''
    if request.method == 'POST':
        title = request.form.get('title')
        category = request.form.get('category')
        text = request.form.get('ckeditor')
        color = request.form.get('color')
        image = request.files['image']
        if image:
            filename = secure_filename(image.filename)
            pic_name = str(uuid.uuid4()) + "_" + filename
            image.save("app/static/img/upload/" + pic_name)
        test = Tests(title=title,category=category,image_name=pic_name,text=text,color=color)
        db.session.add(test)
        db.session.commit()
        flash("Запись добавлена!", category="ok")
        return redirect(url_for("new_test"))
    return render_template("new_test.html")


@app.route('/add_answer/<int:id_question>test_id<int:id_test>', methods=['GET', 'POST'])
def add_answer(id_question,id_test):
    test = Tests.query.get(id_test)
    question = Question.query.filter_by(id=id_question).first()
    answer = Answer.query.filter_by(id_question=id_question).all()
    if request.method == 'POST':
        title = request.form.get('title')
        weight = request.form.get('weight')
        ans = Answer(title=title, weight=weight, id_question=id_question)
        db.session.add(ans)
        db.session.commit()
        flash("Ответ добавлен!", category="ok")
        return redirect(url_for("add_answer", id_question=id_question, id_test=test.id))
    return render_template("add_answer.html",answer=answer,question=question,test=test)


@app.route('/delete-answer/<int:id_question>/<int:id_answer>/<int:id_test>')
def delete_answer(id_question, id_answer,id_test):
    test = Tests.query.get(id_test)
    obj = Answer.query.filter_by(id=id_answer).first()
    db.session.delete(obj)
    db.session.commit()
    flash("Ответ удален!", category="bad")
    return redirect(url_for("add_answer", id_question=id_question, id_test=test.id))


@app.route('/edit_answer/<int:id_question>/<int:id_answer>', methods=['GET', 'POST'])
def edit_answer(id_question, id_answer):
    question = Question.query.get(id_question)
    answer = Answer.query.get(id_answer)
    if request.method == 'POST':
        answer.title = request.form.get('title')
        answer.weight = request.form.get('weight')
        db.session.commit()
        flash("Ответ изменен!", category="ok")
        return redirect(url_for("add_answer", id_question=id_question, id_test=question.id_test))

#нужно сделать переход к следующему вопросу через сессии и списки
@app.route('/testing/id<int:id_test>question<int:id_question>', methods=['GET', 'POST'])
def testing(id_test,id_question):
    test = Tests.query.get(id_test)
    question_id_list = session['testing_questions']
    try:
        question = Question.query.filter_by(id=session['testing_questions'][0],id_test=test.id).first()
        answers = Answer.query.filter_by(id_question=id_question).all()
    
        if request.method == 'POST':
            answer = request.form.get('answer')
            session['testing'] += int(answer)
            session['testing_questions'].pop(0)
            return redirect(url_for("testing", id_test=id_test, id_question=session['testing_questions'][0]))
        
    except IndexError:     
        total_score = session['testing']
        session.pop('testing', None)
        session.pop('testing_questions', None)
        return redirect(url_for("result_testing", total_score=total_score, id_test=id_test))
        
    return render_template("testing.html", question=question,answers=answers,test=test)


@app.route('/result_testing/<int:total_score><int:id_test>')
def result_testing(total_score,id_test):
    test = Tests.query.get(id_test)
    interpretation = Interpretation.query.filter_by(id_test=test.id).first()
    if 'name' in session:
        total_user = Users.query.filter_by(email=session['name']).first()
        rezult = Rezult(total_score=total_score, id_test=id_test, id_user=total_user.id)
        db.session.add(rezult)
        db.session.commit()
        flash("Результат записан!", category="ok")
    return render_template("rezult.html",total_score=total_score,interpretation=interpretation)


@app.context_processor
def inject_user():
    def get_user_name():
        if 'name' in session:
            return Users.query.filter_by(email=session['name']).first()
    return dict(active_user=get_user_name())


@app.route('/logout')
def logout():
    session.pop('name', None)
    return redirect('/')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(403)
def forbidded(e):
    return render_template('403.html'), 403


@app.errorhandler(401)
def forbidded(e):
    return render_template('401.html'), 401