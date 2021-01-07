import re

def caesar(symbol, key):
    return chr((ord(symbol) - 65 + key)%26 + 65) 

def rotor(symbol, n, reverse=False):
    ROTORS = {0: 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
          1: 'EKMFLGDQVZNTOWYHXUSPAIBRCJ',
          2: 'AJDKSIRUXBLHWTMCQGZNPYFVOE',
          3: 'BDFHJLCPRTXVZNYEIWGAKMUSQO',}
    if reverse:
        return ROTORS[0][ROTORS[n].find(symbol)]
    else:
        return ROTORS[n][ROTORS[0].find(symbol)]
    
def reflector(symbol, n):
    REFLECTORS = {0: 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
              1: 'YRUHQSLDPXNGOKMIEBFZCWVJAT'}
    return REFLECTORS[n][REFLECTORS[0].find(symbol)]

def cypher(symbol, ref, rot1, shift1, rot2, shift2, rot3, shift3):
    left = rotor(caesar(rotor(caesar(rotor(caesar(symbol, shift3), rot3), -shift3 + shift2), rot2), -shift2 + shift1), rot1)
    end = reflector(caesar(left, -shift1), ref)
    return caesar(rotor(caesar(rotor(caesar(rotor(caesar(end, shift1), rot1, True), -shift1 + shift2), rot2, True), -shift2 + shift3), rot3, True), -shift3)

def check_pairs(pairs=""):
    cap_pairs = pairs.upper()
    for let in cap_pairs:
        if let != ' ' and cap_pairs.count(let) > 1:
            return False
    else:
        return True
    
def commutator(pairs=""):
    CONNECTIONS = {s[0]:s[1] for s in pairs.upper().split()}
    CONNECTIONS.update({s[1]:s[0] for s in pairs.upper().split()})
    return CONNECTIONS

def enigma(text, ref, rot1, shift1, rot2, shift2, rot3, shift3, pairs=""):
    if check_pairs(pairs):
        COMMUTATOR = commutator(pairs)
        THRESHOLD = {1: 17, 2: 5, 3: 22}
        cap = ''.join(elem for elem in text.upper() if elem.isalnum())
        s = ''
        for let in cap:
            if let in COMMUTATOR:
                let = COMMUTATOR[let]
            shift3 = (shift3+1)%26
            if shift3 == THRESHOLD[rot3]:
                shift2 = (shift2+1)%26
            let = cypher(let, ref, rot1, shift1, rot2, shift2, rot3, shift3)
            if let in COMMUTATOR:
                let = COMMUTATOR[let]
            s = s + let
            if shift2 == THRESHOLD[rot2]-1:
                shift2 = (shift2+1)%26
                shift1 = (shift1+1)%26
        return s
    else:
        return("Извините, невозможно произвести коммутацию")