from bit import Key

# Your private key
private_key_hex = "2832ed74f2b5e35ee"

# Create a key object from the private key
key = Key.from_int(int(private_key_hex, 16))

# Get the corresponding address
address = key.address
print(f"Derived address: {address}")
