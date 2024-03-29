"""
    Forms
    ~~~~~
"""
from flask_wtf import Form
from wtforms import BooleanField
from wtforms import TextField
from wtforms import SelectField
from wtforms import TextAreaField
from wtforms import PasswordField
from wtforms import StringField
from wtforms.validators import InputRequired
from wtforms.validators import ValidationError

from wiki.core import clean_url
from wiki.web import current_wiki
from wiki.web import current_users


class URLForm(Form):
    url = TextField('', [InputRequired()])

    def validate_url(form, field):
        if current_wiki.exists(field.data):
            raise ValidationError('The URL "%s" exists already.' % field.data)

    def clean_url(self, url):
        return clean_url(url)


class SearchForm(Form):
    term = TextField('', [InputRequired()])
    ignore_case = BooleanField(
        description='Ignore Case',
        # FIXME: default is not correctly populated
        default=True)


class EditorForm(Form):
    title = TextField('', [InputRequired()])
    body = TextAreaField('', [InputRequired()])
    tags = TextField('')

class TagForm(Form):
    newTags = TextField('', [InputRequired()])

class LoginForm(Form):
    name = TextField('', [InputRequired()])
    password = PasswordField('', [InputRequired()])

    def validate_name(form, field):
        user = current_users.get_user(field.data)
        if not user:
            raise ValidationError('This username does not exist.')

    def validate_password(form, field):
        user = current_users.get_user(form.name.data)
        if not user:
            return
        if not user.check_password(field.data):
            raise ValidationError('Username and password do not match.')


class UserCreateForm(Form):
    name = TextField('', [InputRequired()])
    password = PasswordField('', [InputRequired()])
    confirm_password = PasswordField('', [InputRequired()])
    is_admin = BooleanField()

    def validate_name(form, field):
        user = current_users.get_user(field.data)
        if user:
            raise ValidationError('This username already exists.')

    def validate_password(form, field):
        user = current_users.get_user(form.name.data)
        if not user:
            return
        if not user.check_password(field.data):
            raise ValidationError('Username and password do not match.')


class UserManagementForm(Form):
    management_option = SelectField('Select an Option', choices=[('add_user', 'Add a User Account'),
                                                                 ('edit_user', 'Edit a User Account'),
                                                                 ('delete_user', 'Delete a User Account')])
    def invalid_name(self):
        raise ValidationError('This username does not exist.')
    # REMOVED AND USED THE UserCreateForm
    # username = StringField('', [InputRequired()])
    # active = SelectField("Is User Active?", choices=[('true', 'Yes'), ('false', 'False')])
    # password = PasswordField('', [InputRequired()])
    # confirm_password = PasswordField('', [InputRequired()])
    # roles = StringField("Add Roles")
