from pysgrs.ciphers.substitution import PermutationCipher


class Wheel(PermutationCipher):

    """
    Generic Wheel object to create Rotor and Reflector
    """

    wiring = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    notches = ""
    name = None

    def __init__(self, state="A", ring="A"):
        super().__init__(permutation=self.encode_permutation(self.wiring))
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

    def actuate(self, offset=1):
        self.state = self.alphabet.symbol(self.alphabet.index(self.state) + offset)

    def to_actuate(self, key):
        return True


class Reflector(Wheel):
    pass


class Rotor(Wheel):
    pass


class Enigma:

    def __init__(self, ref, r1, r2, r3, key="AAA", plugs="", rings="AAA"):

        self.initial_key = key
        self.rings = rings
        self.plugs = plugs

        self.reflector = ref('A')
        self.rotor1 = r1(state=self.initial_key[0], ring=self.rings[0])
        self.rotor2 = r2(state=self.initial_key[1], ring=self.rings[1])
        self.rotor3 = r3(state=self.initial_key[2], ring=self.rings[2])

        plugboard_settings = [(item[0], item[1]) for item in self.plugs.split()]

        input_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        output_alphabet = [" "] * 26

        for i in range(len(input_alphabet)):
            output_alphabet[i] = input_alphabet[i]

        for k, v in plugboard_settings:
            output_alphabet[ord(k) - ord('A')] = v
            output_alphabet[ord(v) - ord('A')] = k

        self.mapping = str.maketrans(input_alphabet, "".join(output_alphabet))

    def build(self):
        pass

    def setup(self):
        pass

    def reset(self):
        pass

    def encipher(self, plaintext_in):

        ciphertext = ''

        plaintext_in_upper = plaintext_in.upper()
        plaintext = plaintext_in_upper.translate(self.mapping)

        for c in plaintext:

            if not c.isalpha():
                ciphertext += c
                continue

            self.rotor2.actuate()
            self.rotor3.actuate()

            t = self.rotor1.encipher(c)
            t = self.rotor2.encipher(t)
            t = self.rotor3.encipher(t)
            t = self.reflector.encipher(t)
            t = self.rotor3.decipher(t)
            t = self.rotor2.decipher(t)
            t = self.rotor1.decipher(t)
            ciphertext += t

        res = ciphertext.translate(self.mapping)

        fres = ""
        for idx, char in enumerate(res):
            if plaintext_in[idx].islower():
                fres += char.lower()
            else:
                fres += char

        return fres

    def decipher(self, cipher_text):
        pass

    def __str__(self):
        return "<Enigma state='%s' reflector=%s rotor1=%s rotor2=%s rotor3=%s rings='%s' plugs='%s'>" % (
            "".join([self.rotor1.state, self.rotor2.state, self.rotor3.state]),
            self.reflector, self.rotor1, self.rotor2, self.rotor3, self.rings, self.plugs
        )


# 1924 Rotors:
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
    name = "I"
    model = "German Railway (Rocket)"
    date = "7 February 1941"


class ROTOR_GR_II(Rotor):
    wiring = "NTZPSFBOKMWRCJDIVLAEYUXHGQ"
    name = "II"
    model = "German Railway (Rocket)"
    date="7 February 1941"


class ROTOR_GR_III(Rotor):
     wiring = "JVIUBHTCDYAKEQZPOSGXNRMWFL"
     name = "III"
     model = "German Railway (Rocket)"
     date = "7 February 1941"


class ROTOR_GR_UKW(Reflector):
    wiring = "QYHOGNECVPUZTFDJAXWMKISRBL"
    name = "UTKW"
    model = "German Railway (Rocket)"
    date = "7 February 1941"


class ROTOR_GR_ETW(Rotor):
    wiring = "QWERTZUIOASDFGHJKPYXCVBNML"
    name = "ETW"
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
    wiring = 'ejmzalyxvbwfcrquontspikhgd'
    name = 'UKW A'


class IM3M4_UKW_B(Reflector):
    wiring = 'yruhqsldpxngokmiebfzcwvjat'
    name = 'UKW A'


class IM3M4_UKW_C(Reflector):
    wiring = 'fvpjiaoyedrzxwgctkuqsbnmhl'
    name = 'UKW A'

