from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Length


class InputKeyForm(FlaskForm):
    input_key = StringField('InputKey', validators=[DataRequired()])
    submit = SubmitField('Search')


class LoginForm(FlaskForm):
    telephone = StringField('telephone', validators=[],
                             render_kw={'class': 'form-control', 'placeholder': "请输入账号"})
    password = PasswordField('password', validators=[],
                             render_kw={'class': 'form-control mb-2', "placeholder": "请输入密码"})
    remember = BooleanField('七天免登陆')
    submit = SubmitField('登录', render_kw={'class': 'form-control btn-block btn btn-primary'})