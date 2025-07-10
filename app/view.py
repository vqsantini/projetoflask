from app import app, db
from flask import render_template, url_for, request, redirect
from app.forms import contatoForm, Contato

@app.route ('/')
def homepage():
    usuario = 'santini'
    idade = 26

    context = {
        'usuario': usuario,
        'idade': idade
    }
    return render_template('index.html', context=context)

@app.route('/contato/', methods=['GET','POST'])
def contato():
    form=contatoForm()
    context = {}
    if form.validate_on_submit():
        form.save()
        return redirect(url_for('homepage'))
    return render_template('contato.html', context=context, form=form)

@app.route('/contato/lista/')
def contatoLista():
    if request.method == 'GET':
        pesquisa = request.args.get('pesquisa', '')
    dados = Contato.query.order_by('nome') 
    if pesquisa != '':
        dados = dados.filter_by(nome=pesquisa)
    context = {'dados': dados.all()}
    return render_template('contato_lista.html', context=context)