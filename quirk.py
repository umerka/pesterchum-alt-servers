import math
import random

colors = {
    "tags": [
        "[black]", "[blue]", "[green]", "[cyan]", "[red]", "[magenta]", "[brown]", "[lgray]",
        "[dgray]", "[lblue]", "[lgreen]", "[lcyan]", "[lred]", "[lmagenta]", "[yellow]", "[white]"
    ],
    "colors": {
        "[black]": [0, 0, 0],
        "[blue]": [0, 0, 170],
        "[green]": [0, 170, 0],
        "[cyan]": [0, 170, 170],
        "[red]": [170, 0, 0],
        "[magenta]": [170, 0, 170],
        "[brown]": [170, 85, 0],
        "[lgray]": [170, 170, 170],
        "[dgray]": [85, 85, 85],
        "[lblue]": [85, 85, 255],
        "[lgreen]": [85, 255, 85],
        "[lcyan]": [85, 255, 255],
        "[lred]": [255, 85, 85],
        "[lmagenta]": [255, 85, 255],
        "[yellow]": [255, 255, 85],
        "[white]": [255, 255, 255]
    }
}

emojis = {
    ":)" : ["ヾ(≧▽≦*)o", "o(*￣▽￣*)o", "o(*^▽^*)┛"],
    ":(" : ["＞︿＜", ".·´¯`(>▂<)´¯`·. ", "(#_<-)", "（；´д｀）ゞ"],
    ":D" : ["§(*￣▽￣*)§", "ლ(╹◡╹ლ)", "(^///^)", "(^◕.◕^)", "/ᐠ｡ꞈ｡ᐟ\\"],
    "XD" : ["< (^-^) >", "(￣︶￣*\\))"],
    ";)" : ["d=====(￣▽￣*)b", "(∩^o^)⊃━☆"],
    "OwO" : ["(❁´◡`❁)", "(⓿_⓿)" , "( •̀ ω •́ )y"],
    "UwU" : ["(～￣▽￣)~", "(^・ω・^ )", "（。＾▽＾）"],
    ">_<" : ["(^///^)", "(/≧▽≦)/", "(p≧w≦q)", "(((o(*ﾟ▽ﾟ*)o)))"],
    ">:(" : ["( ˘︹˘ )", "(╯▔皿▔)╯", "(►__◄)", "(ㆆ_ㆆ)", "（︶^︶）"],
    ":0" : ["w(ﾟДﾟ)w", "(⊙_⊙)? ", "(°ー°〃)", "┬┴┬┴┤(･_├┬┴┬┴", "(⊙_⊙;)", "◉_◉", "⚆_⚆"]
}

suits = {
    "<)=": "<c=0,0,0>♠</c>",
    "<3": "<c=255,0,0>♥</c>",
    "<>": "<c=175,100,100>♦</c>",
    "{)=": "<c=75,75,100>♣</c>"
}
""
def chunk_size_for_length(text):
    length = len(text)

    if length < 40:
        return 1
    elif length < 75:
        return 2
    else:
        return 4

def compress_hex(hex6):
    if (hex6[0] == hex6[1] and
        hex6[2] == hex6[3] and
        hex6[4] == hex6[5]):
        return hex6[0] + hex6[2] + hex6[4]
    return hex6

def rainbow(text, c, invert, chunk=1, mult=1.0):
    output = ""
    text_len = len(text)

    for i in range(0, text_len, chunk):
        group = text[i:i+chunk]

        idx = i
        r = int(math.sin(0.3 * (idx + c))     * 127 + 128)
        g = int(math.sin(0.3 * (idx + c) + 2) * 127 + 128)
        b = int(math.sin(0.3 * (idx + c) + 4) * 127 + 128)

        if invert:
            r = 255 - r
            g = 255 - g
            b = 255 - b

        r = min(int(r*mult), 255)
        g = min(int(g*mult), 255)
        b = min(int(b*mult), 255)

        hex6 = f"{r:02X}{g:02X}{b:02X}"
        small = compress_hex(hex6)

        output += f"<c=#{small}>{group}</c>"

    return output, c + text_len

def color(text, r, g, b):
    r = f"{r:02X}"
    g = f"{g:02X}"
    b = f"{b:02X}"
    hex6 = compress_hex(f"{r}{g}{b}")
    return f"<c=#{hex6}>{text}</c>"


symbols = "~`!@#$%^&*()_+{}|[]\\:\"<>?;',./"

def quirk(text):
    col = "nocol"
    invert = False
    chunksize = chunk_size_for_length(text)
    text = text.split()
    cap = True
    bold = False
    alt = False
    output = []
    i = 0
    chosen_one = random.choice(text)
    temp = ""
    temp_text = []

    for t in text:
        if t in emojis:
            temp_text.append(random.choice(emojis[t]))
        else:
            temp_text.append(t)
    
    text = temp_text;

    w = 0
    for t in text:
        T = list(t)

        if t == "[invert]":
            if invert == True:
                invert = False
            else:
                invert = True

        elif t in colors["tags"]:
            col = t

        elif t == "[rcolor]":
            col = "nocol"
        
        elif t == "[b]":
            if bold == True:
                bold = False
            else:
                bold = True

        elif t == "[a]":
            if alt == True:
                alt = False
            else:
                alt = True
        
        elif alt == True:
            colored, i = rainbow("<alt>" + t + "</alt>", i, invert, chunksize)
            output.append(colored)

        
        elif t in suits:
            output.append(suits[t])

        elif col != "nocol":
            output.append(color(t, colors["colors"][col][0], colors["colors"][col][1], colors["colors"][col][2]))

        elif cap == True:
            temp = T
            temp[0] = temp[0].upper()

            if T[-1] not in ".!?" and w == len(text)-1:
                temp.append('.')

            colored, i = rainbow(''.join(temp), i, invert, chunksize)
            output.append(colored)

            cap = False
        
        elif T[-1] not in ".!?" and w == len(text)-1:
            temp = T
            temp.append('.')
            colored, i = rainbow(''.join(temp), i, invert, chunksize)
            output.append(colored)

        elif t.isupper():
            output.append(color(t, 255, 0, 0))

        elif T[-1] == "." or T[-1] == "!" or T[-1] == "?":
            cap = True
            colored, i = rainbow(t, i, invert, chunksize)
            output.append(colored)

        elif T[0] == T[0].upper() and not t.isupper() and t not in symbols:
                output.append(color(t, 0, 0, 0))

        elif t == "i":
            colored, i = rainbow('I', i, invert, chunksize)
            output.append(colored)

        elif t == "i'll":
            colored, i = rainbow("I'll", i, invert, chunksize)
            output.append(colored)

        elif t == "i'm":
            colored, i = rainbow("I'm", i, invert, chunksize)
            output.append(colored)

        elif t == "i've":
            colored, i = rainbow("I've", i, invert, chunksize)
            output.append(colored)

        elif bold == True:
            colored, i = rainbow(t, i, invert, chunksize, 1.5)
            output.append(colored)

        elif t == chosen_one:
            colored, i = rainbow(t, i, invert, chunksize, 0.5)
            output.append(colored)

        else:
            colored, i = rainbow(t, i, invert, chunksize)
            output.append(colored)
        
        w+=1
        
    return str(" ".join(output) + "<c=100,100,100></c>")

quirk.command = "rainbowRP"

if __name__ == "__main__":
    while True:
        i = input("> ")
        if i == "exit":
            break
        else:
            print(quirk(i))
