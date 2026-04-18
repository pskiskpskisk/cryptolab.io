import traceback
import exercise4.cmac_logic as c
print('HAS_CRYPTO =', getattr(c, 'HAS_CRYPTO', None))
try:
    if c.HAS_CRYPTO:
        r = c.generate_mac_with_steps('hello', None, mac_length=8, algorithm='DES-CBC')
        print('MAC', r['mac_hex'])
    else:
        print('pycryptodome not present; cannot run DES-CBC test')
except Exception as e:
    print('Error:', e)
    traceback.print_exc()
