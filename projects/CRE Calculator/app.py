from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_session import Session
from calculate import calculate_result

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Step 1: Choose reactor
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        reactor_type = request.form['reactor']
        # Handle unimplemented reactor types
        session['reactor_type'] = reactor_type
        return redirect(url_for('choose_reversibility'))
    return render_template('reactor.html')

# Step 2: Choose reversibility
@app.route('/choose_reversibility', methods=['GET', 'POST'])
def choose_reversibility():
    if request.method == 'POST':
        session['reversibility'] = request.form['reversible']
        return redirect(url_for('parameters'))
    return render_template('rev.html')

# Step 3: Input general parameters
@app.route('/parameters', methods=['GET', 'POST'])
def parameters():
    if request.method == 'POST':
        try:
            for key, value in request.form.items():
                session[key] = value
            return redirect(url_for('choose_temp'))
        except Exception as e:
            flash(f"Error processing parameters: {str(e)}")
            return render_template('parameters.html')
    return render_template('parameters.html')

# Step 4: Choose isothermal or non-isothermal
@app.route('/choose_temp', methods=['GET', 'POST'])
def choose_temp():
    if request.method == 'POST':
        session['thermal'] = request.form['thermal']
        
        if session['thermal'] != 'isothermal':
            return redirect(url_for('parameter2'))
        else:
            return redirect(url_for('result'))
    return render_template('temp.html')

# Step 5: If isothermal, get more input
@app.route('/parameter2', methods=['GET', 'POST'])
def parameter2():
    if request.method == 'POST':
        try:
            for key, value in request.form.items():
                session[key] = value
            return redirect(url_for('result'))
        except Exception as e:
            flash(f"Error processing parameters: {str(e)}")
            return render_template('parameter2.html')
    return render_template('parameter2.html')

# Step 6: Render result
@app.route('/result')
def result():
    try:
        data = {key: value for key, value in session.items()}
        result = calculate_result(data, session)
        return render_template(
            'result.html',
            product=result.get('product'),
            outputFactors=result.get('outputFactors'),
            plot_url=result.get('plot_url'),
            plot_ca=result.get('plot_ca'),
            plot_cb=result.get('plot_cb'),
            plot_cc=result.get('plot_cc'),
            plot_cd=result.get('plot_cd'),
            plot_T=result.get('plot_T'),
            plot_k=result.get('plot_k'),
            plot_Keq=result.get('plot_Keq'),

        )
    except Exception as e:
        flash(f"Error calculating results: {str(e)}")
        return redirect(url_for('index'))

# Error pages
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)
