from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from hashlib import sha256

# Simulating Blockchain Transaction with Encryption and Hashing

def generate_student_blockchain_id(student):
    """
    Simulate generating a digital identity using cryptographic methods
    like RSA encryption and hashing to ensure data integrity.
    """
    # Convert student's data into a string
    data = f"{student.full_name}-{student.email}-{student.dob}-{student.blockchain_id}"

    # Create a hash of the data to simulate immutability
    hashed_data = sha256(data.encode('utf-8')).hexdigest()

    return hashed_data

def verify_student_data(student, blockchain_id):
    """
    Verify that the blockchain ID matches the student's data integrity.
    """
    expected_hash = generate_student_blockchain_id(student)
    return expected_hash == blockchain_id
