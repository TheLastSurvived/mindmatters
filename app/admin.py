from flask_admin import AdminIndexView, expose
from flask_admin.contrib.sqlamodel import ModelView
from .models import Users, Articles, Tests, Question, Answer, Interpretation, Rezult
from app import app,db
from flask_admin import Admin
from flask import make_response,session,abort


class AdminIndex(AdminIndexView):
    @expose('/', methods=['GET', 'POST'])
    def index(self):
        if 'name' in session:
            user = Users.query.filter_by(email=session['name']).first()
            if user.root!=1:
                abort(403)
            else:
                return self.render('admin/dashboard_index.html')
        else:
            abort(401)


admin = Admin(app, name='MindMatters', template_mode='bootstrap4',index_view=AdminIndex())


class QuestionView(ModelView):
    column_display_pk = True 
    column_hide_backrefs = False
    column_list = ['id','title','id_test']


class AnswerView(ModelView):
    column_display_pk = True 
    column_hide_backrefs = False
    column_list = ['id','title','weight','id_question']


class InterpretationView(ModelView):
    column_display_pk = True 
    column_hide_backrefs = False
    column_list = ['id','text','id_test']


class RezultView(ModelView):
    column_display_pk = True 
    column_hide_backrefs = False
    column_list = ['id','total_score','date','id_test']


admin.add_view(ModelView(Users, db.session))
admin.add_view(ModelView(Articles, db.session))
admin.add_view(ModelView(Tests, db.session))
admin.add_view(QuestionView(Question, db.session))
admin.add_view(AnswerView(Answer, db.session))
admin.add_view(InterpretationView(Interpretation, db.session))
admin.add_view(RezultView(Rezult, db.session))