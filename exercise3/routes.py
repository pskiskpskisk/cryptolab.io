from flask import render_template, request
from . import ex3_bp

# Import RSA logic
from .rsa_cipher import (
    fermat_primality_test as rsa_prime_test, 
    generate_keys_with_steps, 
    encrypt_string, 
    decrypt_string
)

# Import Diffie-Hellman logic
from .dh_cipher import (
    fermat_primality_test as dh_prime_test,
    is_primitive_root,
    generate_public_key,
    compute_shared_secret
)

# ==========================================
#  RSA ROUTE
# ==========================================
@ex3_bp.route('/rsa', methods=['GET', 'POST'])
def rsa_route():
    # Initialize variables to None (No defaults)
    p = q = e = n = d = message = None
    key_steps = enc_steps = dec_steps = None
    ciphertext = decrypted_msg = None
    error = None
    
    # State flags
    keys_generated = False
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        try:
            # --- STEP 1: GENERATE KEYS ---
            if action == 'generate':
                p = request.form.get('p')
                q = request.form.get('q')
                
                if not p or not q:
                    raise ValueError("Please enter both Prime P and Prime Q.")
                
                p = int(p)
                q = int(q)

                # Generate Keys
                key_data = generate_keys_with_steps(p, q)
                
                # Extract results to pass back to template
                e, n = key_data['public']
                d, _ = key_data['private'] # n is same
                key_steps = key_data['steps']
                keys_generated = True

            # --- STEP 2: ENCRYPT MESSAGE ---
            elif action == 'encrypt':
                # Get the keys from the form (user might have edited them, or they were hidden)
                n = int(request.form.get('n'))
                e = int(request.form.get('e'))
                d = int(request.form.get('d'))
                message = request.form.get('message')
                
                # We need p and q just to re-render the form inputs, though not used for encryption
                p = request.form.get('p')
                q = request.form.get('q')

                if not message:
                    raise ValueError("Please enter a message to encrypt.")

                public_key = (e, n)
                private_key = (d, n)

                # Encrypt
                ciphertext, enc_steps = encrypt_string(message, public_key)
                
                # Decrypt
                decrypted_msg, dec_steps = decrypt_string(ciphertext, private_key)
                
                keys_generated = True # Keep the bottom section open

        except ValueError as ve:
            error = str(ve)
        except Exception as err:
            error = f"An error occurred: {str(err)}"

    return render_template('rsa.html', 
                           p=p, q=q, 
                           n=n, e=e, d=d,
                           message=message,
                           key_steps=key_steps,
                           enc_steps=enc_steps,
                           dec_steps=dec_steps,
                           ciphertext=ciphertext,
                           decrypted_msg=decrypted_msg,
                           keys_generated=keys_generated,
                           error=error)


@ex3_bp.route('/dh', methods=['GET', 'POST'])
def dh_route():
    result = None
    error = None
    
    # No default values
    p = g = a = b = None

    if request.method == 'POST':
        try:
            p_in = request.form.get('p')
            g_in = request.form.get('g')
            a_in = request.form.get('a')
            b_in = request.form.get('b')

            if not all([p_in, g_in, a_in, b_in]):
                raise ValueError("All fields are required.")

            p = int(p_in)
            g = int(g_in)
            a = int(a_in)
            b = int(b_in)

            # 1. Validate Prime P
            if not dh_prime_test(p):
                raise ValueError(f"Error: {p} is not a prime number.")

            # 2. Validate Primitive Root G
            if not is_primitive_root(g, p):
                raise ValueError(f"Error: {g} is NOT a primitive root modulo {p}.")

            # 3. Calculate Keys
            public_A = generate_public_key(p, g, a)
            public_B = generate_public_key(p, g, b)
            secret_Alice = compute_shared_secret(public_B, a, p)
            secret_Bob = compute_shared_secret(public_A, b, p)

            result = {
                'public_A': public_A,
                'public_B': public_B,
                'secret_Alice': secret_Alice,
                'secret_Bob': secret_Bob,
                'success': (secret_Alice == secret_Bob)
            }

        except Exception as e:
            error = str(e)

    return render_template('dh.html', result=result, error=error,
                           p=p, g=g, a=a, b=b)