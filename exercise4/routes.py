from flask import render_template, request
from . import ex4_bp
from . import md5_logic
from . import cmac_logic

@ex4_bp.route('/md5', methods=['GET', 'POST'])
def md5_route():
    result_hash = None
    input_text = None
    error = None
    steps = None

    if request.method == 'POST':
        try:
            input_text = request.form.get('text', '')
            
            # Convert string input to bytes for the algorithm
            input_bytes = input_text.encode('utf-8')
            
            # Call the verbose MD5 function to get intermediate steps
            md5_res = md5_logic.md5_hash_with_steps(input_bytes, log_rounds=True)
            result_hash = md5_res.get('hash')
            steps = md5_res.get('steps')
            
        except Exception as e:
            error = f"Hashing failed: {str(e)}"

    return render_template('md5.html', result=result_hash, input_text=input_text, error=error, steps=steps)


@ex4_bp.route('/cmac', methods=['GET', 'POST'])
def cmac_route():
    result = None
    input_text = None
    key_input = None
    error = None
    steps = None

    if request.method == 'POST':
        try:
            input_text = request.form.get('text', '').strip()
            key_input = request.form.get('key', '').strip()
            # DES-CBC MAC only: fixed 8-byte output, message + key input only.
            result = cmac_logic.generate_cmac_with_steps(input_text, key_input)
            steps = result.get('steps', [])
            
        except Exception as e:
            error = f"CMAC computation failed: {str(e)}"

    return render_template(
        'cmac.html',
        result=result,
        input_text=input_text,
        key_input=key_input,
        steps=steps,
        error=error,
    )