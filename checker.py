import hashlib
import base58

def sha256(data):
    """Compute SHA-256 hash of the input data."""
    return hashlib.sha256(data).digest()

def ripemd160(data):
    """Compute RIPEMD-160 hash of the input data."""
    ripemd = hashlib.new('ripemd160')
    ripemd.update(data)
    return ripemd.digest()

def public_key_to_address(public_key_hex):
    """Convert a public key to a Bitcoin address."""
    # Step 1: Convert hex public key to bytes
    public_key_bytes = bytes.fromhex(public_key_hex)

    # Step 2: Perform SHA-256 on the public key
    sha256_result = sha256(public_key_bytes)

    # Step 3: Perform RIPEMD-160 on the SHA-256 result
    ripemd160_result = ripemd160(sha256_result)

    # Step 4: Add network byte (0x00 for mainnet)
    network_byte = b'\x00' + ripemd160_result

    # Step 5: Compute checksum
    checksum = sha256(sha256(network_byte))[:4]

    # Step 6: Append checksum to the network byte
    address_bytes = network_byte + checksum

    # Step 7: Convert to Base58Check
    address = base58.b58encode(address_bytes)

    return address.decode('utf-8')

# Example usage
public_key_hex ='KwDiBf89QgGbjEhKnhXJuH7LrciVrZi3qbc13cncibGLg5Gvft2L'
bitcoin_address = public_key_to_address(public_key_hex)
print("Bitcoin Address:", bitcoin_address)
