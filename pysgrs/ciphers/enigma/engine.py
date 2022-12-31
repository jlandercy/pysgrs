from pysgrs.alphabets.basic import BasicAlphabet
from pysgrs.ciphers.enigma.rotors import *


class Engine:

    def reset(self):
        self.rotors_ = []
        for index, rotor in enumerate(self.rotors):
            self.rotors_.append(
                rotor(
                    state=self.rotor_states[index],
                    ring=self.rotor_rings[index],
                    alphabet=self.alphabet
                )
            )
        self.reflector_ = self.reflector(state=self.reflector_state, ring=self.reflector_ring)

    def __init__(
        self,
        rotors=(ROTOR_I, ROTOR_II, ROTOR_III),
        reflector=ROTOR_Reflector_A,
        rotor_rings="AAA", rotor_states="ABC",
        reflector_ring="A", reflector_state="A",
        plugs="AV BS CG DL FU HZ IN KM OW RX",
        alphabet=BasicAlphabet(),
        name="Enigma (default)"
    ):

        # Alphabet:
        self.alphabet = alphabet

        # Naming:
        self.name = name

        # Wheel Factory:
        self.rotors = rotors
        self.reflector = reflector
        self.rotor_rings = rotor_rings
        self.rotor_states = rotor_states
        self.reflector_ring = reflector_ring
        self.reflector_state = reflector_state

        # Plugboard:
        self.plugs = plugs

        # Actual wheels:
        self.rotors_ = None
        self.reflector_ = None

        # Set machine:
        self.reset()

        # Plugboard:
        self.plugboard = PermutationCipher(
            permutation=PermutationCipher.encode_permutation_using_letter_pairs(self.plugs.split(" "))
        )

    def encipher(self, plaintext_in):

        plaintext = plaintext_in.upper()

        # Encode character...
        ciphertext = ''
        for c in plaintext:

            # Encode only known character:
            if not c.isalpha():
                ciphertext += c
                continue

            t = c

            # Plugboard (in):
            t = self.plugboard.encipher(t)

            # Actuate rotors:
            self.rotors_[0].actuate()
            for index in range(len(self.rotors_) - 1):
                if self.rotors_[index].to_propagate:
                    self.rotors_[index + 1].actuate()

            # Direct rotor ciphering:
            for index in reversed(range(len(self.rotors_))):
                t = self.rotors_[index].encipher(t)

            # Reflection:
            t = self.reflector_.encipher(t)

            # Reverse rotor ciphering:
            for index in range(len(self.rotors_)):
                t = self.rotors_[index].decipher(t)

            # Plugboard (out):
            t = self.plugboard.decipher(t)

            ciphertext += t

        # Encode character [...] preserving case:
        fres = ""
        for idx, char in enumerate(ciphertext):
            if plaintext_in[idx].islower():
                fres += char.lower()
            else:
                fres += char

        return fres

    def decipher(self, cipher_text):
        return self.encipher(cipher_text)

    def __str__(self):
        return "<Engine:%s rotors=%s reflector=%s plugs='%s'>" % (self.name, self.rotors_, repr(self.reflector_), self.plugs)


# Basic Enigma Machine:
Enigma = Engine()
