from flask import render_template, request
from . import ex1_bp

from .vigenere import vigenere_encrypt, vigenere_decrypt
from .affine import affine_encrypt, affine_decrypt
from .playfair import playfair_encrypt, playfair_decrypt
from .number_theory import gcd, extended_gcd, mod_inverse, modexp, is_probable_prime


@ex1_bp.route('/vigenere', methods=['GET', 'POST'])
def vigenere_route():
    result, logs, error = None, None, None
    if request.method == 'POST':
        try:
            text = request.form.get('text', '')
            key = request.form.get('key', '')
            if 'encrypt' in request.form:
                result, logs = vigenere_encrypt(text, key)
            elif 'decrypt' in request.form:
                result, logs = vigenere_decrypt(text, key)
        except Exception as e:
            error = str(e)
    return render_template('vigenere.html', result=result, logs=logs, error=error)


@ex1_bp.route('/affine', methods=['GET', 'POST'])
def affine_route():
    result, logs, error = None, None, None
    if request.method == 'POST':
        try:
            text = request.form.get('text', '')
            a = int(request.form.get('a', ''))
            b = int(request.form.get('b', ''))
            if 'encrypt' in request.form:
                result, logs = affine_encrypt(text, a, b)
            elif 'decrypt' in request.form:
                result, logs = affine_decrypt(text, a, b)
        except Exception as e:
            error = str(e)
    return render_template('affine.html', result=result, logs=logs, error=error)


@ex1_bp.route('/playfair', methods=['GET', 'POST'])
def playfair_route():
    result, logs, error = None, None, None
    if request.method == 'POST':
        try:
            text = request.form.get('text', '')
            key = request.form.get('key', '')
            if 'encrypt' in request.form:
                result, logs = playfair_encrypt(text, key)
            elif 'decrypt' in request.form:
                result, logs = playfair_decrypt(text, key)
        except Exception as e:
            error = str(e)
    return render_template('playfair.html', result=result, logs=logs, error=error)


@ex1_bp.route('/extended-euclidean', methods=['GET', 'POST'])
def extended_euclidean_route():
    result = None
    error = None
    data = {}
    if request.method == 'POST':
        try:
            a = int(request.form.get('a', '0'))
            b = int(request.form.get('b', '0'))
            
            # Extended Euclidean
            g, x, y = extended_gcd(a, b)
            data['a'] = a
            data['b'] = b
            data['gcd'] = g
            data['x'] = x
            data['y'] = y
            data['identity'] = f"{a}*{x} + {b}*{y} = {g}"
            
            # Modular inverse
            try:
                data['a_inv_mod_b'] = mod_inverse(a, b)
            except Exception as ex:
                data['a_inv_mod_b'] = str(ex)
            
            result = data
        except Exception as e:
            error = str(e)
    return render_template('extended_euclidean.html', result=result, error=error)


@ex1_bp.route('/fermat-theorem', methods=['GET', 'POST'])
def fermat_theorem_route():
    result = None
    error = None
    data = {}
    if request.method == 'POST':
        try:
            n = int(request.form.get('n', '0'))
            a = int(request.form.get('a', '2'))
            
            if n <= 1:
                raise ValueError('n must be greater than 1')
            
            # Fermat's Little Theorem test
            is_prime = is_probable_prime(n)
            
            # If prime, verify Fermat's condition with given a
            fermat_holds = None
            if n > 2 and 0 < a < n:
                fermat_result = modexp(a, n - 1, n)
                fermat_holds = (fermat_result == 1)
            
            data['n'] = n
            data['a'] = a
            data['is_prime'] = is_prime
            data['fermat_result'] = fermat_result if fermat_holds is not None else None
            data['fermat_holds'] = fermat_holds
            
            result = data
        except Exception as e:
            error = str(e)
    return render_template('fermat_theorem.html', result=result, error=error)


@ex1_bp.route('/number-theory', methods=['GET', 'POST'])
def number_theory_route():
    result = None
    error = None
    data = {}
    if request.method == 'POST':
        try:
            a = int(request.form.get('a', '0'))
            b = int(request.form.get('b', '0'))
            data['gcd'] = gcd(a, b)
            try:
                data['a_inv_mod_b'] = mod_inverse(a, b)
            except Exception as ex:
                data['a_inv_mod_b'] = str(ex)
            data['a_pow_b_mod'] = modexp(a, b, max(2, b))
            data['a_prime'] = is_probable_prime(a)
            data['b_prime'] = is_probable_prime(b)
            result = data
        except Exception as e:
            error = str(e)
    return render_template('number_theory.html', result=result, error=error)
