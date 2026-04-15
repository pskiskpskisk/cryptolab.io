from flask import render_template, request
from . import ex2_bp
from . import des_cipher
from . import aes_cipher

@ex2_bp.route('/des', methods=['GET', 'POST'])
def des_route():
    result, logs, key_logs, error, mode_label = None, None, None, None, None
    mode = 'ECB'
    
    # We pass the static S-Boxes for visualization
    s_boxes = des_cipher.S_BOXES
    
    if request.method == 'POST':
        try:
            text = request.form.get('text', '')
            key = request.form.get('key', '')
            mode = request.form.get('mode', 'ECB')
            
            if 'encrypt' in request.form:
                result, logs, key_logs = des_cipher.des_encrypt(text, key, mode)
                mode_label = f"Ciphertext ({mode})"
            elif 'decrypt' in request.form:
                result, logs, key_logs = des_cipher.des_decrypt(text, key, mode)
                mode_label = f"Plaintext ({mode})"
        except Exception as e:
            error = str(e)
            
    return render_template('des.html', result=result, logs=logs, key_logs=key_logs, error=error, mode_label=mode_label, mode=mode, s_boxes=s_boxes)

@ex2_bp.route('/aes', methods=['GET', 'POST'])
def aes_route():
    result, logs, key_logs, error, mode_label = None, None, None, None, None
    mode = 'ECB'
    
    if request.method == 'POST':
        try:
            text = request.form.get('text', '')
            key = request.form.get('key', '')
            mode = request.form.get('mode', 'ECB')
            
            if 'encrypt' in request.form:
                result, logs, key_logs = aes_cipher.aes_encrypt(text, key, mode)
                mode_label = f"Ciphertext ({mode})"
            elif 'decrypt' in request.form:
                result, logs, key_logs = aes_cipher.aes_decrypt(text, key, mode)
                mode_label = f"Plaintext ({mode})"
        except Exception as e:
            error = str(e)
            
    return render_template('aes.html', result=result, logs=logs, key_logs=key_logs, error=error, mode_label=mode_label, mode=mode)