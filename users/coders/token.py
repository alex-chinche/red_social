import jwt
import hashlib

__secret_key = 'qx5FGbEPokYDK1NxmU1sPy2uIHHOUu0evbR3JSV0sNRHwPkVIW1Eehtyogv6A7GFqD7IPOJYI5Qe7qRYNeEeRBILAcfLX0zIdGYqps5RKzubpc9l13HOV7J5EGIAdTogHIdlfb8sKWF8ezffKVurmsAhUScWIeXVImBsyUK1GV7YqycXp8df7bvbSrVRQujemli8i3E2zCG6m7lvwZUx3FAUO2q5s2UghKakooPr0MllLxW5pSdPuoS9T1aQPt8N5VGyGQwLOVwwtum4h17iXIx6tyJthy9NsuHavGKKzcUFKIaxOstYKmaDZLnZIfIU27cuU8cKGyQ9Kfgw352oFF2dzxkDBCY7HN80oT5wtovU9DUP6XndpMJXBV1jQkEW0Z60AIjaYbbmyfpM'


def encode_token(email, hashed_password):
    encoded_data = jwt.encode(
        {'email': email, 'password': hashed_password}, __secret_key, algorithm='HS256')
    return encoded_data


def decode_token(token):
    decoded_data = jwt.decode(token, __secret_key, algorithms='HS256')
    return decoded_data


def hash_password(password):
    encoded_password = password.encode()
    hashed_password = hashlib.sha256(encoded_password).hexdigest()
    return hashed_password
