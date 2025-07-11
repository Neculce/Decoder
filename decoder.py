from pwn import *
from textwrap import wrap
import binascii
import re 

host = 'https://decoderunner-e5ec5618a9ab24da.deploy.phreaks.fr/'
port = 443 
conn = remote(host, port, ssl=True)

x=1

conn.recvuntil(b'Good Luck!')
conn.recvline()
conn.recvline()
conn.recvline()


def cipherident(hint):  #function to identify cipher based on hints
    match hint: 
        case b"hint: He can't imagine finding himself in CTF 150 years later..." : 
            baudot()

        case b'hint: Hendrix would have had it...' :
            guitar()

        case b'hint: 1337 ...' :
            leet()

        case b'hint: A code based on pairs of dots and dashes. Think of a mix of Morse code and numbers... (AZERTYUIO)':
            morbit()

        case b'hint: what is this charabia ???':
            latingib()

        case b'hint: Born in 1462 in Germany...':
            tritemius()

        case b'hint: It looks like Morse code, but ...':
            wabun()

        case b'hint: Did you realy see slumdog millionaire ?':
            shankar()

        case b'hint: He can snap his toes, and has already counted to infinity twice ...':
            chucknorris()

        case _ : 
            milsign(hint)

for x in range (100):

    hint = conn.recvline()
    cipherident(hint)


def baudot():
    output = conn.recvline()
    output.replace('cipher: ','') #delete initial word 
    
    encoded = output
    encoded = encoded.split(" ")
    output =""

    state = 0 #state of the translator, 0 is alpha dict, 1 is numeric dict. Default is 0 since baudot starts with chars
        
    alpha = [ "null", " ", "Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "A", "S", "D", "F", "G", "H", "J", "K", "L", "Z", "X", "C", "V", "B", "N", "M", "CaRetCR", "LineFeed"]
    numeric = [ "null", " ", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "BELL", "$", "!", "&", "#", "`", "(", ")", '"', "/", ":", ";", "?", ",", ".", "CaRetCR", "LineFeed"]
    value = [ "00000", "00100", "10111", "10011", "00001", "01010", "10000", "10101", "00111", "00110", "11000", "10110", "00011", "00101", "01001", "01101", "11010", "10100", "01011", "01111", "10010", "10001", "11101", "01110", "11110", "11001", "01100", "11100", "01000", "00010"] 

    for code in encoded :
        if code == "11011":
            state = 1
        if code == "11111":
            state = 0
        
        if state == 0 :
            output = output + alpha[value.index(code)]
        else :   
            output = output + numeric[value.index(code)]


    conn.sendline(output.lower())

def guitar():

    output = conn.recvline()
    output.replace('cipher: ','') #delete initial word 
    output.split(" ")

    # Mapping of standard tuning (E A D G B E) to note names
    NOTE_MAP = {
    'E': ['E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B', 'C', 'C#', 'D', 'D#'],
    'A': ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#'],
    'D': ['D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B', 'C', 'C#'],
    'G': ['G', 'G#', 'A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#'],
    'B': ['B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#'],
    'E2': ['E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B', 'C', 'C#', 'D', 'D#']
    }

    def decode_chord(encoded_chord):
        standard_tuning = ['E', 'A', 'D', 'G', 'B', 'E2']  # EADGBE
        notes = []
    
        for i, fret in enumerate(encoded_chord):
            if fret == 'x':
                continue  # Muted string
            fret = int(fret)
            note = NOTE_MAP[standard_tuning[i]][fret % 12]  # Get the note at the fret
            notes.append(note)
    
        return notes[0] if notes else "?"  # Return the first note as the root letter

    # print and call function
    def out_song(chords):
        decoded_word = "".join(decode_chord(chord) for chord in chords)
        conn.sendline("".join(decoded_word).lower())

def leet():
    output = conn.recvline()
    output.replace('cipher: ','') #delete initial word 
    
    leet_dict = {
    'A': ['4', '@', '/\\', '^', 'Д'],
    'B': ['8', '13', '|3', 'ß', 'P>', 'I3'],
    'C': ['(', '<', '[', '{'],
    'D': ['|)', '|}', '|]'],
    'E': ['3', '&', '£', '€', '[-'],
    'F': ['|=', 'ph', 'ƒ'],
    'G': ['6', '9', '&', '(_+'],
    'H': ['#', '|-|', '[-]', ']-[', '}{'],
    'I': ['1', '!', '|', 'eye'],
    'J': ['_|', '_/', '¿'],
    'K': ['|<', '|{', '|X'],
    'L': ['1', '|', '£', '7'],
    'M': ['|\\/|', '/\\/\\', '^^', '(V)', '[V]'],
    'N': ['|\\|', '/\\/', '^/', '|V'],
    'O': ['0', '()', '[]', '{}', '<>'],
    'P': ['|*', '|o', '|>', '|°', '9'],
    'Q': ['0_', 'O,', '(,)', 'kw'],
    'R': ['|2', '12', '.-', '|^'],
    'S': ['5', '$', '§', 'z', 'ehs'],
    'T': ['7', '+', '-|-', '1'],
    'U': ['|_|', '\\_/', 'v'],
    'V': ['\\/', '|/', '\\|'],
    'W': ['\\/\\/', 'vv', '\\^/', '\\|/'],
    'X': ['><', '}{', ')('],
    'Y': ['`/', '\\|/', '¥'],
    'Z': ['2', '7_', '%', '>_']
    }

    # Create reverse lookup dictionary
    reverse_leet_dict = {}
    for letter, leet_variants in leet_dict.items():
        for variant in leet_variants:
            reverse_leet_dict[variant] = letter

    # Sort patterns by length (longest first) to handle multi-character replacements first
    sorted_patterns = sorted(reverse_leet_dict.keys(), key=len, reverse=True)

    # Create regex pattern to match leetspeak symbols
    leet_regex = re.compile('|'.join(re.escape(pattern) for pattern in sorted_patterns))

    def leet_to_text(leet_str): 
        """Convert leetspeak to normal text."""
        conn.sendline(leet_regex.sub(lambda match: reverse_leet_dict[match.group(0)], leet_str).lower())
    
    leet_to_text(output)


def morbit():
    message = conn.recvline()
    message.replace('cipher: ','') #delete initial word 
    key_dict = [ "0", "..", "./", "/-", "//", "-.", "--", "/.", "-/", ".-"]

    morse_to_text_dict = {
        '.-': 'A',    '-...': 'B',  '-.-.': 'C',  '-..': 'D',   '.': 'E',  
        '..-.': 'F',  '--.': 'G',   '....': 'H',  '..': 'I',    '.---': 'J',  
        '-.-': 'K',   '.-..': 'L',  '--': 'M',    '-.': 'N',    '---': 'O',  
        '.--.': 'P',  '--.-': 'Q',  '.-.': 'R',   '...': 'S',   '-': 'T',  
        '..-': 'U',   '...-': 'V',  '.--': 'W',   '-..-': 'X',  '-.--': 'Y',  
        '--..': 'Z', '':' '
    }

    morse_result = ""

    for i in range(0,len(message)):
        morse_result = morse_result + key_dict[int(message[int(i)])]
    morse_result = morse_result.split("/")
    
    output = ""
    for i in morse_result:
        output = output + morse_to_text_dict[i]
    conn.sendline(output.lower())


def latingib():
    message = conn.recvline()
    message.replace('cipher: ','') #delete initial word 

    conn.sendling(message[:-2][::-1].lower())


def tritemius():
    message = conn.recvline()
    message.replace('cipher: ','').upper() #delete initial word 

    alphabet = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
    output=""
    shift = 3

    for i in message:
        output = output + alphabet[(alphabet.index(i) - shift)%26] 
        shift = shift + 1
    conn.sendline(output.lower())

def wabun():
    output = conn.recvline()
    output.replace('cipher: ','') #delete initial word 

    alphabet = ["i","ro","ha","ni","ho","he","to","chi","ri","nu","ru","wo","wa","ka","yo","ta","re","so","tsu","ne","na","ra","mu","u","wi","no","o","ku","ya","ma","ke","fu","ko","e","te","a","sa","ki","yu","me","mi","shi","we","hi","mo","se","su","n"]
    morse = [".-",".-.-","-...","-.-.","-..",".","..-..","..-.","--.","....","-.--.",".---","-.-",".-..","--","-.","---","---.",".--.","--.-",".-.","...","-","..-",".-..-","..--",".-...","...-",".--","-..-","-.--","--..","----","-.---",".-.--","--.--","-.-.-","-.-..","-..--","-...-","..-.-","--.-.",".--..","--..-","-..-.",".---.","---.-",".-.-."]

    message = message.split (" ")

    for i in message:
        if i in morse:
            message[message.index(i)] = alphabet[morse.index(i)]
    conn.sendline("".join(message))


def shankar():

    output = ""
    alphabet = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
    substitute = ["D","F","G","H","J","K","L","M","N","U","O","P","Q","R","S","T","I","V","W","X","Y","Z","B","A","C","E"]

    message = conn.recvline()
    message.replace('cipher: ','') #delete initial word 

    for i in range(0, len(message)):
        output = output + substitute[alphabet.index(message[i])]

    conn.sendline(output.lower())
    

def chucknorris():
    encoded = conn.recvline()
    encoded.replace('cipher: ','') #delete initial word 
    encoded = encoded.split (" ")

    binary = ''
    output = ''
    response = ''

    word = 0
    counter = 0

    for i in range(0, len(encoded)):    #so anyway, i started blasting
        if (i%2 == 0):
            word = len(encoded[i])%2
        if (i%2 == 1):
            counter = len(encoded[i])
            for j in range(0,counter):
                binary = binary + str(word)

    output = wrap(binary,7)
    for i in range(0,len(output)):
        output[i] = '0' + output[i]
        response = response + chr(int(output[i],2))

    conn.sendline(response.lower())


def milsign(hint):
    x = hint.split (" ")
    for each in x :
        response = response + x[0]
    conn.sendline(response.lower())



