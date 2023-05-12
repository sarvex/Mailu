from mailu import models
from mailu.ui import ui, forms, access

import flask
import flask_login


@ui.route('/admin/list', methods=['GET'])
@access.global_admin
def admin_list():
    admins = models.User.query.filter_by(global_admin=True)
    return flask.render_template('admin/list.html', admins=admins)


@ui.route('/admin/create', methods=['GET', 'POST'])
@access.global_admin
def admin_create():
    form = forms.AdminForm()
    form.admin.choices = [
        (user.email, user.email)
        for user in
        flask_login.current_user.get_managed_emails(include_aliases=False)
    ]
    if form.validate_on_submit():
        if user := models.User.query.get(form.admin.data):
            user.global_admin = True
            models.db.session.commit()
            flask.flash(f'User {user} is now admin')
            return flask.redirect(flask.url_for('.admin_list'))
        else:
            flask.flash('No such user', 'error')
    return flask.render_template('admin/create.html', form=form)


@ui.route('/admin/delete/<path:admin>', methods=['GET', 'POST'])
@access.global_admin
@access.confirmation_required("delete admin {admin}")
def admin_delete(admin):
    if user := models.User.query.get(admin):
        user.global_admin  = False
        models.db.session.commit()
        flask.flash(f'User {user} is no longer admin')
        return flask.redirect(flask.url_for('.admin_list'))
    else:
        flask.flash('No such user', 'error')
    flask.flash(f'Alias {alias} deleted')
    return flask.redirect(
        flask.url_for('.alias_list', domain_name=alias.domain.name))
