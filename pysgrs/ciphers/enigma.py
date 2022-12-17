
class Reflector:

    wiring = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    name = None
    model = None
    date = None

    def __init__(self, state):
        self.state = state

    def __setattr__(self, name, value):
        self.__dict__[name] = value

    def encipher(self, key):
        shift = (ord(self.state) - ord('A'))
        index = (ord(key) - ord('A')) % 26
        index = (index + shift) % 26
        letter = self.wiring[index]
        output = chr(ord('A') + (ord(letter) - ord('A') + 26 - shift) % 26)
        return output

    def __eq__(self, rotor):
        return self.name == rotor.name

    def __str__(self):
        return "<Reflector state=%s name='%s' model='%s' date='%s' wiring='%s'>" % (self.state, self.name, self.model, self.date, self.wiring)


class Rotor(object):

    wiring = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    notches = ""
    name = None
    model = None
    date = None

    def __init__(self, state="A", ring="A"):

        self.right_wiring = ["0"] * 26

        for i in range(0, len(self.wiring)):
            self.right_wiring[ord(self.wiring[i]) - ord('A')] = chr(ord('A') + i)

        self.state = state
        self.ring = ring

    def __setattr__(self, name, value):
        self.__dict__[name] = value
        if name == 'wiring':
            self.right_wiring = ["0"]*26
            for i in range(0, len(self.wiring)):
                self.right_wiring[ord(self.wiring[i]) - ord('A')] = chr(ord('A') + i)

    def encipher_right(self, key):
        shift = (ord(self.state) - ord(self.ring))
        index = (ord(key) - ord('A')) % 26
        index = (index + shift) % 26
        letter = self.wiring[index]
        output = chr(ord('A') + (ord(letter) - ord('A') + 26 - shift) % 26)
        return output

    def encipher_left(self, key):
        shift = (ord(self.state) - ord(self.ring))
        index = (ord(key) - ord('A')) % 26
        index = (index + shift) % 26
        letter = self.right_wiring[index]
        output = chr(ord('A') + (ord(letter) - ord('A') + 26 - shift) % 26)
        return output

    def notch(self, offset=1):
        self.state = chr((ord(self.state) + offset - ord('A')) % 26 + ord('A'))
        notchnext = self.state in self.notches
        #return notchnext

    def is_in_turnover_pos(self):
        return chr((ord(self.state) + 1 - ord('A')) % 26 + ord('A')) in self.notches

    def __eq__(self, rotor):
        return self.name == rotor.name

    def __str__(self):
        return "<Rotor state='%s' ring='%s' name='%s' model='%s' date='%s' wiring='%s'>" % (self.state, self.ring, self.name, self.model, self.date, self.wiring)


# 1924 Rotors
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

#
# # German Railway Rotors
# ROTOR_GR_I = Rotor(wiring="JGDQOXUSCAMIFRVTPNEWKBLZYH", name="I", model="German Railway (Rocket)", date="7 February 1941")
# ROTOR_GR_II = Rotor(wiring="NTZPSFBOKMWRCJDIVLAEYUXHGQ", name="II", model="German Railway (Rocket)", date="7 February 1941")
# ROTOR_GR_III = Rotor(wiring="JVIUBHTCDYAKEQZPOSGXNRMWFL", name="III", model="German Railway (Rocket)", date="7 February 1941")
# ROTOR_GR_UKW = Reflector(wiring="QYHOGNECVPUZTFDJAXWMKISRBL", name="UTKW", model="German Railway (Rocket)", date="7 February 1941")
# ROTOR_GR_ETW = Rotor(wiring="QWERTZUIOASDFGHJKPYXCVBNML", name="ETW", model="German Railway (Rocket)", date="7 February 1941")
#
# # Swiss K Rotors
# ROTOR_I_K = Rotor(wiring="PEZUOHXSCVFMTBGLRINQJWAYDK", name="I-K", model="Swiss K", date="February 1939")
# ROTOR_II_K = Rotor(wiring="ZOUESYDKFWPCIQXHMVBLGNJRAT", name="II-K", model="Swiss K", date="February 1939")
# ROTOR_III_K = Rotor(wiring="EHRVXGAOBQUSIMZFLYNWKTPDJC", name="III-K", model="Swiss K", date="February 1939")
# ROTOR_UKW_K = Reflector(wiring="IMETCGFRAYSQBZXWLHKDVUPOJN", name="UKW-K", model="Swiss K", date="February 1939")
# ROTOR_ETW_K = Rotor(wiring="QWERTZUIOASDFGHJKPYXCVBNML", name="ETW-K", model="Swiss K", date="February 1939")
#
# # Enigma
# ROTOR_I = Rotor(wiring="EKMFLGDQVZNTOWYHXUSPAIBRCJ",notchs="R", name="I", model="Enigma 1", date="1930")
# ROTOR_II = Rotor(wiring="AJDKSIRUXBLHWTMCQGZNPYFVOE",notchs="F", name="II", model="Enigma 1", date="1930")
# ROTOR_III = Rotor(wiring="BDFHJLCPRTXVZNYEIWGAKMUSQO",notchs="W", name="III", model="Enigma 1", date="1930")
# ROTOR_IV = Rotor(wiring="ESOVPZJAYQUIRHXLNFTGKDCMWB",notchs="K", name="IV", model="M3 Army", date="December 1938")
# ROTOR_V = Rotor(wiring="VZBRGITYUPSDNHLXAWMJQOFECK",notchs="A", name="V", model="M3 Army", date="December 1938")
# ROTOR_VI = Rotor(wiring="JPGVOUMFYQBENHZRDKASXLICTW",notchs="AN", name="VI", model="M3 & M4 Naval(February 1942)", date="1939")
# ROTOR_VII = Rotor(wiring="NZJHGRCXMYSWBOUFAIVLPEKQDT",notchs="AN", name="VII", model="M3 & M4 Naval(February 1942)", date="1939")
# ROTOR_VIII = Rotor(wiring="FKQHTLXOCBJSPDZRAMEWNIUYGV",notchs="AN", name="VIII", model="M3 & M4 Naval(February 1942)", date="1939")
#


class ROTOR_I(Rotor):
    wiring = "EKMFLGDQVZNTOWYHXUSPAIBRCJ"
    notches = "R"
    name = "I"
    model = "Enigma 1"
    date="1930"


class ROTOR_II(Rotor):
    wiring = "AJDKSIRUXBLHWTMCQGZNPYFVOE"
    notches = "F"
    name="II"
    model="Enigma 1"
    date="1930"


class ROTOR_III(Rotor):
    wiring = "BDFHJLCPRTXVZNYEIWGAKMUSQO"
    notchs = "W"
    name = "III"
    model = "Enigma 1"
    date="1930"


# # misc & reflectors
# ROTOR_Beta = Rotor(wiring="LEYJVCNIXWPBQMDRTAKZGFUHOS", name="Beta", model="M4 R2", date="Spring 1941")
# ROTOR_Gamma = Rotor(wiring="FSOKANUERHMBTIYCWLQPZXVGJD", name="Gamma", model="M4 R2", date="Spring 1941")
# ROTOR_Reflector_A = Reflector(wiring="EJMZALYXVBWFCRQUONTSPIKHGD", name="Reflector A")
# ROTOR_Reflector_B = Reflector(wiring="YRUHQSLDPXNGOKMIEBFZCWVJAT", name="Reflector B")
# ROTOR_Reflector_C = Reflector(wiring="FVPJIAOYEDRZXWGCTKUQSBNMHL", name="Reflector C")
# ROTOR_Reflector_B_Thin = Reflector(wiring="ENKQAUYWJICOPBLMDXZVFTHRGS", name="Reflector_B_Thin", model="M4 R1 (M3 + Thin)", date="1940")
# ROTOR_Reflector_C_Thin = Reflector(wiring="RDOBJNTKVEHMLFCWZAXGYIPSUQ", name="Reflector_C_Thin", model="M4 R1 (M3 + Thin)", date="1940")
# ROTOR_ETW = Rotor(wiring="ABCDEFGHIJKLMNOPQRSTUVWXYZ", name="ETW", model="Enigma 1")


class ROTOR_Reflector_A(Reflector):
    wiring = "EJMZALYXVBWFCRQUONTSPIKHGD"
    name = "Reflector A"


class Enigma:

    def __init__(self, ref, r1, r2, r3, key="AAA", plugs="", ring="AAA"):

        self.reflector = ref('A')
        self.rotor1 = r1(state=key[0], ring=ring[0])
        self.rotor2 = r2(state=key[1], ring=ring[1])
        self.rotor3 = r3(state=key[2], ring=ring[2])

        plugboard_settings= [(item[0], item[1]) for item in plugs.split()]

        alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        alpha_out = [" "] * 26

        for i in range(len(alpha)):
            alpha_out[i] = alpha[i]

        for k, v in plugboard_settings:
            alpha_out[ord(k)-ord('A')] = v
            alpha_out[ord(v)-ord('A')] = k

        self.transtab = str.maketrans(alpha, "".join(alpha_out))

    def encipher(self, plaintext_in):

        ciphertext = ''

        plaintext_in_upper = plaintext_in.upper()
        plaintext = plaintext_in_upper.translate(self.transtab)

        for c in plaintext:

            if not c.isalpha():
                ciphertext += c
                continue

            if self.rotor2.is_in_turnover_pos():
                self.rotor2.notch()
                self.rotor3.notch()

            if self.rotor1.is_in_turnover_pos():
                self.rotor2.notch()

            self.rotor1.notch()

            t = self.rotor1.encipher_right(c)
            t = self.rotor2.encipher_right(t)
            t = self.rotor3.encipher_right(t)
            t = self.reflector.encipher(t)
            t = self.rotor3.encipher_left(t)
            t = self.rotor2.encipher_left(t)
            t = self.rotor1.encipher_left(t)
            ciphertext += t

        res = ciphertext.translate(self.transtab)

        fres = ""
        for idx, char in enumerate(res):
            if plaintext_in[idx].islower():
                fres += char.lower()
            else:
                fres += char

        return fres

    def __str__(self):
        return "<Enigma reflector=%s rotor1=%s rotor2=%s rotor3=%s>" % (self.reflector, self.rotor1, self.rotor2, self.rotor3)
