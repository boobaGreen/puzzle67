from bit import Key

# Chiave privata in esadecimale
# private_key_hex = '000000000000000000000000000000000007ccccccccccda3a10'
private_key_hex = '000000000000000000000000000000000007ccccccccccda3a10'

# Crea una chiave dal valore intero
key = Key.from_int(int(private_key_hex, 16))

# Stampa la chiave WIF
print(key.to_wif())
