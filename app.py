# app.py
from flask import Flask, render_template, redirect, url_for

from exercise1 import ex1_bp
from exercise2 import ex2_bp
from exercise3 import ex3_bp
from exercise4 import ex4_bp

app = Flask(__name__)

app.register_blueprint(ex1_bp, url_prefix='/ex1')
app.register_blueprint(ex2_bp, url_prefix='/ex2')
app.register_blueprint(ex3_bp, url_prefix='/ex3')
app.register_blueprint(ex4_bp, url_prefix='/ex4')

# --- UPDATED ROOT ROUTE ---
@app.route('/')
def root():
    # Render the new Home Card layout
    # Render the main index page (home)
    return render_template('index.html')

@app.route('/dashboard/<ex_id>')
def exercise(ex_id):
    valid_ex = [f'ex{i}' for i in range(1, 8)]
    if ex_id not in valid_ex:
        return redirect(url_for('root'))
    
    return render_template('index.html', active_ex=ex_id)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
