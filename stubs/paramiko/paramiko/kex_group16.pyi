"""
Standard SSH key exchange ("kex" if you wanna sound cool).  Diffie-Hellman of
4096 bit key halves, using a known "p" prime and "g" generator.
"""

from paramiko.kex_group14 import KexGroup14SHA256

class KexGroup16SHA512(KexGroup14SHA256): ...
