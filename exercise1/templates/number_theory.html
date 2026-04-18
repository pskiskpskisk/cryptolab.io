<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Number Theory - Ex1-B</title>
  <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
  <style>
    .algorithm-box {
      background: #f5f7fa;
      border-left: 4px solid #4f6df5;
      padding: 15px;
      margin: 15px 0;
      border-radius: 6px;
    }
    .algorithm-title {
      font-weight: bold;
      color: #4f6df5;
      margin-bottom: 8px;
    }
    .result-row {
      display: flex;
      gap: 20px;
      margin: 12px 0;
      font-size: 0.95rem;
    }
    .result-label {
      font-weight: 600;
      color: #333;
      min-width: 180px;
    }
    .result-value {
      color: #666;
      font-family: monospace;
      background: #fff;
      padding: 6px 10px;
      border-radius: 4px;
    }
  </style>
</head>
<body class="theme-ex1">
  <aside class="sidebar">
    <div class="logo">CRYPTO LAB</div>
    <nav>
      <ul>
        <li><a href="{{ url_for('root') }}">← Back to Home</a></li>
        <li style="margin-top: 20px; font-weight: bold; color: #aaa; font-size: 0.9rem;">Exercise 1-A (Classical Ciphers):</li>
        <li><a href="{{ url_for('ex1.vigenere_route') }}">Vigenere</a></li>
        <li><a href="{{ url_for('ex1.affine_route') }}">Affine</a></li>
        <li><a href="{{ url_for('ex1.playfair_route') }}">Playfair</a></li>
        <li style="margin-top: 15px; font-weight: bold; color: #aaa; font-size: 0.9rem;">Exercise 1-B (Number Theory):</li>
        <li><a href="{{ url_for('ex1.extended_euclidean_route') }}">Extended Euclidean</a></li>
        <li><a href="{{ url_for('ex1.fermat_theorem_route') }}">Fermat's Little Theorem</a></li>
      </ul>
    </nav>
  </aside>
  <main class="content">
    <header><h1>Ex1-B: Number Theory Foundations</h1></header>
    <section class="form-section">
      <form method="POST">
        <div class="form-group"><label>Integer a</label><input type="number" name="a" value="{{ request.form.get('a','') }}" required></div>
        <div class="form-group"><label>Integer b</label><input type="number" name="b" value="{{ request.form.get('b','') }}" required></div>
        <div style="display:flex; gap:10px;"><button type="submit">Compute</button></div>
      </form>

      {% if error %}<div class="error-message">{{ error }}</div>{% endif %}
      {% if result %}
        <div class="result-container">
          <h3>Results for a={{ request.form.get('a') }} and b={{ request.form.get('b') }}</h3>
          
          <!-- GCD Algorithm -->
          <div class="algorithm-box">
            <div class="algorithm-title">Euclidean Algorithm (GCD)</div>
            <div class="result-row">
              <span class="result-label">GCD(a, b):</span>
              <span class="result-value">{{ result.gcd }}</span>
            </div>
            {% if result.gcd_steps %}
            <div style="margin-top:10px; font-family:monospace; font-size:0.9rem; background:#fff; padding:8px; border-radius:6px;">
              <strong>Steps:</strong>
              <div style="margin-top:6px;">
                {% for s in result.gcd_steps %}
                  <div>a={{ s.a }}, b={{ s.b }}, q={{ s.q }}, r={{ s.r }}</div>
                {% endfor %}
              </div>
            </div>
            {% endif %}
            <p style="font-size: 0.9rem; color: #666; margin: 10px 0;">
              Computes the greatest common divisor using the iterative Euclidean algorithm.
            </p>
          </div>

          <!-- Extended Euclidean Algorithm -->
          <div class="algorithm-box">
            <div class="algorithm-title">Extended Euclidean Algorithm</div>
            <p style="font-size: 0.9rem; color: #666; margin-bottom: 10px;">
              Finds integers x and y such that: <strong>a·x + b·y = GCD(a, b)</strong>
            </p>
            <div class="result-row">
              <span class="result-label">Modular Inverse (a⁻¹ mod b):</span>
              <span class="result-value">{{ result.a_inv_mod_b }}</span>
            </div>
            <p style="font-size: 0.85rem; color: #999; margin: 8px 0;">
              If GCD(a, b) = 1, then a has a multiplicative inverse modulo b. Used in affine ciphers.
            </p>
          </div>

          <!-- Modular Exponentiation -->
          <div class="algorithm-box">
            <div class="algorithm-title">Modular Exponentiation (Fast Exponentiation)</div>
            <div class="result-row">
              <span class="result-label">a^b mod b:</span>
              <span class="result-value">{{ result.a_pow_b_mod }}</span>
            </div>
            <p style="font-size: 0.9rem; color: #666; margin: 10px 0;">Efficiently computes large powers modulo a number using binary exponentiation.</p>
            {% if result.modexp_steps %}
            <div style="margin-top:8px; font-family:monospace; background:#fff; padding:8px; border-radius:6px;">
              <strong>Steps:</strong>
              <div style="margin-top:6px;">
                {% for s in result.modexp_steps %}
                  <div>{{ s }}</div>
                {% endfor %}
              </div>
            </div>
            {% endif %}
          </div>

          <!-- Fermat's Little Theorem / Primality -->
          <div class="algorithm-box">
            <div class="algorithm-title">Fermat's Little Theorem & Miller-Rabin Primality Test</div>
            <p style="font-size: 0.9rem; color: #666; margin-bottom: 10px;">
              <strong>Fermat's Little Theorem:</strong> If p is prime and gcd(a, p) = 1, then a^(p-1) ≡ 1 (mod p)
            </p>
            <div class="result-row">
              <span class="result-label">Is a prime?</span>
              <span class="result-value" style="color: {% if result.a_prime %}#27ae60{% else %}#e74c3c{% endif %};">
                {{ "Yes ✓" if result.a_prime else "No ✗" }}
              </span>
            </div>
            <div class="result-row">
              <span class="result-label">Is b prime?</span>
              <span class="result-value" style="color: {% if result.b_prime %}#27ae60{% else %}#e74c3c{% endif %};">
                {{ "Yes ✓" if result.b_prime else "No ✗" }}
              </span>
            </div>
            <p style="font-size: 0.85rem; color: #999; margin: 8px 0;">
              Uses Miller-Rabin probabilistic test for reliable primality detection.
            </p>
            {% if result.a_prime_steps %}
            <div style="margin-top:10px; font-family:monospace; background:#fff; padding:8px; border-radius:6px;">
              <strong>Primality Steps for a:</strong>
              <div style="margin-top:6px;">
                {% for s in result.a_prime_steps %}
                  <div>{{ s }}</div>
                {% endfor %}
              </div>
            </div>
            {% endif %}
            {% if result.b_prime_steps %}
            <div style="margin-top:10px; font-family:monospace; background:#fff; padding:8px; border-radius:6px;">
              <strong>Primality Steps for b:</strong>
              <div style="margin-top:6px;">
                {% for s in result.b_prime_steps %}
                  <div>{{ s }}</div>
                {% endfor %}
              </div>
            </div>
            {% endif %}
          </div>
        </div>
      {% endif %}
    </section>
  </main>
</body>
</html>
