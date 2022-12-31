from pysgrs.ciphers.substitution import PermutationCipher


class Wheel(PermutationCipher):

    """
    Generic Wheel object to create Rotor and Reflector
    """

    wiring = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    notches = ""
    name = None

    def __init__(self, state="A", ring="A", alphabet=None):
        super().__init__(permutation=self.encode_permutation_using_alphabet(self.wiring), alphabet=alphabet)
        self.state = state
        self.ring = ring

    def encipher(self, key, strict=False, quite=True):
        shift = (
           self.alphabet.index(key)
           + self.alphabet.index(self.state)
           + self.alphabet.index(self.ring)
        ) % self.alphabet.size
        symbol = self.alphabet.symbol(shift)
        return super().encipher(symbol, strict=strict, quite=quite)

    def decipher(self, key, strict=False, quite=True):
        shift = (
           self.alphabet.index(key)
           + self.alphabet.index(self.state)
           + self.alphabet.index(self.ring)
        ) % self.alphabet.size
        symbol = self.alphabet.symbol(shift)
        return super().decipher(symbol, strict=strict, quite=quite)

    def __str__(self):
        return "<%s:%s state='%s' ring='%s' wiring='%s'>" % (
            self.__class__.__bases__[0].__name__, self.name, self.state, self.ring, self.wiring
        )

    def __repr__(self):
        return "<%s:%s state='%s'>" % (
            self.__class__.__bases__[0].__name__, self.name, self.state
        )

    def actuate(self, offset=1):
        self.state = self.alphabet.symbol((self.alphabet.index(self.state) + offset) % self.alphabet.size)

    @property
    def to_propagate(self):
        return self.state in self.notches


class Reflector(Wheel):
    pass


class Rotor(Wheel):
    pass


# Commercial Rotors (since 1924):
class ROTOR_IC(Rotor):
    wiring = "DMTWSILRUYQNKFEJCAZBPGXOHV"
    name = "IC"
    model = "Commercial Enigma A, B"
    date = "1924"


class ROTOR_IIC(Rotor):
    wiring = "HQZGPJTMOBLNCIFDYAWVEUSRKX"
    name = "IIC"
    model = "Commercial Enigma A, B"
    date = "1924"


class ROTOR_IIIC(Rotor):
    wiring = "UQNTLSZFMREHDPXKIBVYGJCWOA"
    name = "IIIC"
    model = "Commercial Enigma A, B"
    date="1924"


# German Railway Rotors
class ROTOR_GR_I(Rotor):
    wiring = "JGDQOXUSCAMIFRVTPNEWKBLZYH"
    name = "GR-I"
    model = "German Railway (Rocket)"
    date = "7 February 1941"


class ROTOR_GR_II(Rotor):
    wiring = "NTZPSFBOKMWRCJDIVLAEYUXHGQ"
    name = "GR-II"
    model = "German Railway (Rocket)"
    date="7 February 1941"


class ROTOR_GR_III(Rotor):
     wiring = "JVIUBHTCDYAKEQZPOSGXNRMWFL"
     name = "GR-III"
     model = "German Railway (Rocket)"
     date = "7 February 1941"


class REFLECTOR_GR_UKW(Reflector):
    wiring = "QYHOGNECVPUZTFDJAXWMKISRBL"
    name = "GR-UTKW"
    model = "German Railway (Rocket)"
    date = "7 February 1941"


class ROTOR_GR_ETW(Rotor):
    wiring = "QWERTZUIOASDFGHJKPYXCVBNML"
    name = "GR-ETW"
    model = "German Railway (Rocket)"
    date = "7 February 1941"


# Swiss K Rotors
class ROTOR_I_K(Rotor):
    wiring = "PEZUOHXSCVFMTBGLRINQJWAYDK"
    name = "I-K"
    model = "Swiss K"
    date = "February 1939"


class ROTOR_II_K(Rotor):
    wiring = "ZOUESYDKFWPCIQXHMVBLGNJRAT"
    name = "II-K"
    model = "Swiss K"
    date = "February 1939"


class ROTOR_III_K(Rotor):
    wiring = "EHRVXGAOBQUSIMZFLYNWKTPDJC"
    name = "III-K"
    model = "Swiss K"
    date = "February 1939"


class ROTOR_UKW_K(Reflector):
    wiring = "IMETCGFRAYSQBZXWLHKDVUPOJN"
    name = "UKW-K"
    model = "Swiss K"
    date = "February 1939"


class ROTOR_ETW_K(Rotor):
    wiring = "QWERTZUIOASDFGHJKPYXCVBNML"
    name="ETW-K"
    model="Swiss K"
    date="February 1939"


# Enigma:
class ROTOR_I(Rotor):
    wiring = "EKMFLGDQVZNTOWYHXUSPAIBRCJ"
    notches = "R"
    name = "I"
    model = "Enigma 1"
    date = "1930"


class ROTOR_II(Rotor):
    wiring = "AJDKSIRUXBLHWTMCQGZNPYFVOE"
    notches = "F"
    name = "II"
    model = "Enigma 1"
    date = "1930"


class ROTOR_III(Rotor):
    wiring = "BDFHJLCPRTXVZNYEIWGAKMUSQO"
    notches = "W"
    name = "III"
    model = "Enigma 1"
    date = "1930"


class ROTOR_IV(Rotor):
    wiring = "ESOVPZJAYQUIRHXLNFTGKDCMWB"
    notches = "K"
    name = "IV"
    model = "M3 Army"
    date = "December 1938"


class ROTOR_V(Rotor):
    wiring = "VZBRGITYUPSDNHLXAWMJQOFECK"
    notches = "A"
    name = "V"
    model = "M3 Army"
    date = "December 1938"


class ROTOR_VI(Rotor):
    wiring = "JPGVOUMFYQBENHZRDKASXLICTW"
    notches = "AN"
    name = "VI"
    model = "M3 & M4 Naval(February 1942)"
    date = "1939"


class ROTOR_VII(Rotor):
    wiring = "NZJHGRCXMYSWBOUFAIVLPEKQDT"
    notches = "AN"
    name = "VII"
    model = "M3 & M4 Naval(February 1942)"
    date = "1939"


class ROTOR_VIII(Rotor):
    wiring = "FKQHTLXOCBJSPDZRAMEWNIUYGV"
    notches = "AN"
    name = "VIII"
    model = "M3 & M4 Naval(February 1942)"
    date = "1939"


# Miscelaneous & Reflectors
class ROTOR_Beta(Rotor):
    wiring = "LEYJVCNIXWPBQMDRTAKZGFUHOS"
    name = "Beta"
    model = "M4 R2"
    date = "Spring 1941"


class ROTOR_Gamma(Rotor):
     wiring = "FSOKANUERHMBTIYCWLQPZXVGJD"
     name = "Gamma"
     model = "M4 R2"
     date = "Spring 1941"


class ROTOR_ETW(Rotor):
    wiring = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    name = "ETW"
    model = "Enigma 1"


class ROTOR_Reflector_A(Reflector):
    wiring = "EJMZALYXVBWFCRQUONTSPIKHGD"
    name = "Reflector A"


class ROTOR_Reflector_B(Reflector):
    wiring = "YRUHQSLDPXNGOKMIEBFZCWVJAT"
    name = "Reflector B"


class ROTOR_Reflector_C(Reflector):
    wiring = "FVPJIAOYEDRZXWGCTKUQSBNMHL"
    name = "Reflector C"


class ROTOR_Reflector_B_Thin(Reflector):
    wiring = "ENKQAUYWJICOPBLMDXZVFTHRGS"
    name = "Reflector_B_Thin"
    model = "M4 R1 (M3 + Thin)"
    date = "1940"


class ROTOR_Reflector_C_Thin(Reflector):
    wiring = "RDOBJNTKVEHMLFCWZAXGYIPSUQ"
    name = "Reflector_C_Thin"
    model = "M4 R1 (M3 + Thin)"
    date = "1940"


# https://github.com/cryptii/cryptii/blob/main/src/Encoder/Enigma.js

class IM3M4_R1(Rotor):
    wiring = 'EKMFLGDQVZNTOWYHXUSPAIBRCJ'
    notches = 'Q'
    name = 'I'


class IM3M4_R2(Rotor):
    wiring = 'AJDKSIRUXBLHWTMCQGZNPYFVOE'
    notches = 'E'
    name = 'II'


class IM3M4_R3(Rotor):
    wiring = 'BDFHJLCPRTXVZNYEIWGAKMUSQO'
    notches = 'V'
    name = 'III'


class IM3M4_UKW_A(Reflector):
    wiring = 'EJMZALYXVBWFCRQUONTSPIKHGD'
    name = 'UKW A'


class IM3M4_UKW_B(Reflector):
    wiring = 'YRUHQSLDPXNGOKMIEBFZCWVJAT'
    name = 'UKW A'


class IM3M4_UKW_C(Reflector):
    wiring = 'FVPJIAOYEDRZXWGCTKUQSBNMHL'
    name = 'UKW A'

