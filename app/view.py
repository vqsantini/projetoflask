from app import app, db
from flask import render_template, url_for, request, redirect
from app.forms import ContatoForm, UserForm, LoginForm, PostForm, PostComentarioForm
from app.models import Contato, User, Post, PostComentarios
from app import bcrypt
from flask_login import login_user, logout_user, current_user, login_required

@app.route ('/', methods=['GET','POST'])
def homepage():

    idade = 26
    form = LoginForm()

    if form.validate_on_submit():
        user = form.login()
        login_user(user, remember=True)

    context = {
        'idade': idade
    }
    return render_template('index.html', context=context, form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = form.login()
        login_user(user, remember=True)
        return redirect(url_for('homepage'))
    return render_template('login_user.html', form=form)

@app.route('/sair/')
def logout():
    logout_user()
    return redirect(url_for('homepage'))

@app.route('/contato/', methods=['GET','POST'])
def cadastroContato():
    form = ContatoForm()
    context = {}
    if form.validate_on_submit():
        form.save()
        return redirect(url_for('homepage'))
    return render_template('cadastro_contato.html', context=context, form=form)

@app.route('/contato/lista/')
def contatoLista():
    if request.method == 'GET':
        pesquisa = request.args.get('pesquisa', '')
    dados = Contato.query.order_by('nome')

    if pesquisa != '':
        dados = dados.filter_by(nome=pesquisa)

    context = {'dados': dados.all()}
    return render_template('contato_lista.html', context=context)

@app.route('/contato/<int:id>')
def contatoDetalhes(id):
    obj = Contato.query.get(id)
    return render_template('contato_detalhes.html', obj = obj)

@app.route('/cadastrousuario', methods=['GET', 'POST'])
def cadastroUsuario():
    form = UserForm()
    if form.validate_on_submit():
        user = form.save()
        login_user(user, remember=True)
        return redirect(url_for('homepage'))
    return render_template('cadastro_usuario.html',form=form)

@app.route('/post/novo', methods=['GET', 'POST'])
@login_required
def PostNovo():
    form = PostForm()
    if form.validate_on_submit():
        form.save(current_user.id)
        return redirect(url_for('homepage'))
    return render_template('post_novo.html', form=form)

@app.route('/post/lista')
@login_required
def PostLista():
    posts = Post.query.all()
    print(current_user.posts)
    return render_template('post_lista.html', posts=posts)

@app.route('/post/<int:id>', methods=['GET', 'POST'])
@login_required
def PostComentarios(id):
    post = Post.query.get(id)
    form = PostComentarioForm()
    if form.validate_on_submit():
        form.save(current_user.id, id)
        return redirect(url_for('PostComentarios', id=id))
    return render_template('post.html', post=post, form=form)

@app.route('/contato/excluir/<int:id>', methods=['POST'])
@login_required
def excluirContato(id):
    obj = Contato.query.get_or_404(id)
    db.session.delete(obj)
    db.session.commit()
    return redirect(url_for('contatoLista')) 