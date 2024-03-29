import re
"""
    Routes
    ~~~~~~
"""


from flask import Blueprint, current_app
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import current_user
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user

from wiki.core import Processor
from wiki.web.forms import EditorForm, UserCreateForm
from wiki.web.forms import LoginForm
from wiki.web.forms import SearchForm
from wiki.web.forms import URLForm
from wiki.web.forms import TagForm
from wiki.web import current_wiki
from wiki.web import current_users
from wiki.web.user import protect
from datetime import datetime
import user

try:
    import forms
except:
    from . import forms

bp = Blueprint('wiki', __name__)


@bp.before_request
def update_activity():
    if current_user.is_authenticated:
        current_date = datetime.now().strftime("%I:%M%p %m/%d/%y")
        current_user.set('last_active', current_date)


@bp.route('/', methods=['GET', 'POST'])
@protect
def home():
    page = current_wiki.get('home')
    if page:
        return display('home')
    return render_template('home.html')


@bp.route('/index/')
@protect
def index():
    pages = current_wiki.index()
    return render_template('index.html', pages=pages)


@bp.route('/<path:url>/', methods=['GET', 'POST'])
@protect
def display(url):
    page = current_wiki.get_or_404(url)
    form = TagForm(obj=page)

    if request.method =="POST":
        newTags = request.form['newTags']

        if page.tags == '':
            page.tags = newTags
        else:
            page.tags = page.tags + ","+ newTags
        page.tags = newTags
        page.save()
        return redirect(url_for('wiki.display', url=url))

    return render_template('page.html', page=page, form=form)


@bp.route('/create/', methods=['GET', 'POST'])
@protect
def create():
    form = URLForm()
    if form.validate_on_submit():
        return redirect(url_for(
            'wiki.edit', url=form.clean_url(form.url.data)))
    return render_template('create.html', form=form)


@bp.route('/edit/<path:url>/', methods=['GET', 'POST'])
@protect
def edit(url):
    page = current_wiki.get(url)
    form = EditorForm(obj=page)
    if form.validate_on_submit():
        if not page:
            page = current_wiki.get_bare(url)
        form.populate_obj(page)
        page.save()
        flash('"%s" was saved.' % page.title, 'success')
        return redirect(url_for('wiki.display', url=url))
    return render_template('editor.html', form=form, page=page)


@bp.route('/preview/', methods=['POST'])
@protect
def preview():
    data = {}
    processor = Processor(request.form['body'])
    data['html'], data['body'], data['meta'] = processor.process()
    return data['html']


@bp.route('/move/<path:url>/', methods=['GET', 'POST'])
@protect
def move(url):
    page = current_wiki.get_or_404(url)
    form = URLForm(obj=page)
    if form.validate_on_submit():
        newurl = form.url.data
        current_wiki.move(url, newurl)
        return redirect(url_for('wiki.display', url=newurl))
    return render_template('move.html', form=form, page=page)


@bp.route('/delete/<path:url>/')
@protect
def delete(url):
    page = current_wiki.get_or_404(url)
    current_wiki.delete(url)
    flash('Page "%s" was deleted.' % page.title, 'success')
    return redirect(url_for('wiki.home'))


@bp.route('/tags/')
@protect
def tags():
    tags = current_wiki.get_tags()
    return render_template('tags.html', tags=tags)


@bp.route('/tag/<string:name>/')
@protect
def tag(name):
    tagged = current_wiki.index_by_tag(name)
    return render_template('tag.html', pages=tagged, tag=name)


@bp.route('/search/filter/', methods=['GET', 'POST'])
@protect
def advanced_search():
    form = SearchForm()
    if form.validate_on_submit():
        try:
            re.compile(".*" + form.term.data, re.IGNORECASE)
        except re.error:
            return render_template('advanced_search.html', form=form, search=None, error=True)
        if request.form.get('options') == "users":
            users = current_users.get_all_users()
            user = []
            if form.ignore_case.data:
                pattern = re.compile(".*" + form.term.data, re.IGNORECASE)
            else:
                pattern = re.compile(".*" + form.term.data)
            for x in users:
                if re.search(pattern, x.name) is not None:
                    user.append(x)
            return render_template('advanced_search.html', form=form, users=user, search=form.term.data)
        elif request.form.get('options') == "tags":
            tags = current_wiki.get_tags()
            tag = []
            if form.ignore_case.data:
                pattern = re.compile(".*" + form.term.data, re.IGNORECASE)
            else:
                pattern = re.compile(".*" + form.term.data)
            for x in tags:
                if re.search(pattern, x) is not None:
                    tag.append(x)
            return render_template('advanced_search.html', form=form, tags=tag, search=form.term.data)
        elif request.form.get('options') == "roles":
            users = current_users.get_all_users()
            roles = {}
            if form.ignore_case.data:
                pattern = re.compile(".*" + form.term.data, re.IGNORECASE)
            else:
                pattern = re.compile(".*" + form.term.data)
            for x in users:
                user_roles = x.get('roles')
                for y in range(len(user_roles)):
                    if re.search(pattern, user_roles[y]) is not None:
                        roles.setdefault(x.name, [])
                        roles[x.name].append(user_roles[y])
            return render_template('advanced_search.html', form=form, search=form.term.data, roles=roles)
        results = current_wiki.search(form.term.data, form.ignore_case.data)
        return render_template('advanced_search.html', form=form,
                               results=results, search=form.term.data)
    return render_template('advanced_search.html', form=form, search=None)



@bp.route('/user/login/', methods=['GET', 'POST'])
def user_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = current_users.get_user(form.name.data)
        user.set('authenticated', True)
        login_user(user)
        flash('Login successful.', 'success')
        return redirect(request.args.get("next") or url_for('wiki.index'))
    return render_template('login.html', form=form)



@bp.route('/user/logout/')
@login_required
def user_logout():
    current_user.set('authenticated', False)
    logout_user()
    flash('Logout successful.', 'success')
    return redirect(url_for('wiki.index'))



@bp.route('/user_manage/create/', methods=['POST'])
def user_manage_create():
    user_found = False
    password_mismatch = False
    is_admin = ['admin'] if request.form.get('is_admin') else ['']
    if current_users.get_user(request.form.get('name')) is not None:
        user_found = True
        flash('Username was taken, please try again.', 'error')
    if request.form.get('password') != request.form.get('confirm_password'):
        password_mismatch = True
        flash('Those passwords didn\'t match, please try again', 'error')
    if user_found is False and password_mismatch is False:
        current_users.add_user(name=request.form.get('name'), password=request.form.get('password'), roles=is_admin)
    return render_template('request_completed.html')


@bp.route('/user_manage/edit/', methods=['POST'])
def user_manage_edit():
    user_found = True
    password_mismatch = False
    is_admin = True if request.form.get('is_admin') else False

    if current_users.get_user(request.form.get('name')) is None:
        user_found = False
        flash('Username not found, please try again', 'error')
    if request.form.get('password') != request.form.get('confirm_password'):
        password_mismatch = True
        flash('Those passwords didn\'t match, please try again', 'error')
    if user_found is True and password_mismatch is False:
        current_users.edit_user(request.form.get('name'), request.form.get('password'), is_admin)
    return render_template('request_completed.html')


@bp.route('/user_manage/delete/', methods=['GET', 'POST'])
def user_manage_delete():
    user_found = False
    if current_users.get_user(request.form.get('name')) is None:
        user_found = True
        flash('Username not found, please try again', 'error')
    else:
        current_users.delete_user(request.form.get('name'))
    return render_template('request_completed.html')

@bp.route('/user_manage/', methods=['', 'GET'])
def management_option():
    form = forms.UserManagementForm()
    option = request.args.get('management_option')

    if request.method == 'GET':
        user_modify_form = forms.UserCreateForm()
        if request.args.get('management_option') is None:
            return render_template('user_manage.html', form=form, option_needed=True, selected=False)
        elif option == 'add_user':
            return render_template('user_manage.html', form=user_modify_form, selected=True, option_needed=False)
        elif option == 'edit_user':
            return render_template('user_manage.html', form=user_modify_form, selected=True, option_needed=False)
        elif option == 'delete_user':
            return render_template('user_manage.html', form=user_modify_form, selected=True, option_needed=False)
    else:
        return render_template('user_manage.html', form=form, option_needed=True, selected=False)



@bp.route('/user/')
def user_index():
    users = current_users.get_all_users()
    return render_template('user_index.html', users=users)


@bp.route('/user/<path:name>/')
def user_page(name):
    user = current_users.get_user(name)
    return render_template('user_profile.html', user=user)



"""
    Error Handlers
    ~~~~~~~~~~~~~~
"""


@bp.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


