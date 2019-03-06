from flask import render_template, flash, redirect, url_for, request
from app import app
from app.forms import ModuleForm, ModuleFileForm
from app.MCpMC.pmcmodules import PmcModules
from app.MCpMC.simumodules import simu
from werkzeug import secure_filename
from app.MCpMC.plot_module import plot_module

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    file = ModuleFileForm()
    form = ModuleForm()
    if file.validate_on_submit():
        text = file.file.data.stream.read().decode("utf-8")
        form.text.data = text
        return render_template('index.html', title='MCpMC', file=file, form=form, result=None, text=text)
    if form.validate_on_submit():
        nb_run = form.nb_run.data
        len_run = form.len_run.data
        text = form.text.data
        if nb_run is None:
            nb_run = 10000
        if len_run is None:
            len_run = 100

        valu = form.params.data;
        if valu == "":
            estimated_reward, estimated_variance, pmc = simu(text, nb_run, len_run)
        else:
            try:
                estimated_reward, estimated_variance, pmc = simu(text, nb_run, len_run, eval(valu))
            except NameError as e:
                raise Exception("Forme non valide des parametres (dict).") from  e
        #flash('reward={}, variance={}'.format(estimated_reward, estimated_variance))
        #return redirect('/index')
        result = plot_module(pmc, estimated_reward, estimated_variance, nb_run)
        return render_template('index.html', title='MCpMC', file=file, form=form, result=result.decode('utf8'), reward=estimated_reward, variance=estimated_variance, text=text)

    result = None
    text = None
    return render_template('index.html', title='MCpMC', file=file, form=form, result=result, text=text)
