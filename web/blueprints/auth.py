from flask import Blueprint, flash, render_template, redirect, url_for
from web.forms import LoginForm
from web.utils.url import redirect_back

auth_bp = Blueprint("auth", __name__)

user_password = {
    "18796360983": 111111,
}


@auth_bp.route("/login", methods=["POST", "GET"])
def login():
    """
    登录
    :return:
    """
    form = LoginForm()

    if form.validate_on_submit():
        telephone = form.telephone.data
        password = form.telephone.data
        # remember = form.remember.data

        if len(telephone) == 0:
            flash("请输入账号", "danger")
            return redirect_back()
        if len(password) == 0:
            flash('请输入密码', 'danger')
            return redirect_back()

        if telephone in user_password.keys() and user_password[telephone] == 111111:
            return redirect(url_for("search.hunt"))
    else:
        return render_template('auth/login.html', form=form)
