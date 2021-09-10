import time, base64, zlib, random


def encrypt(ctx):
    global xencrypt
    xencrypt = 0
    y = 0
    hi = "0"
    ciphertextmangle = ctx
    start_time = time.time()
    for i in range(150000):
        xencrypt = xencrypt + 1
        y = y + 1
        def get_random_unicode(length):
            get_char = chr

            include_ranges = [(0x0021, 0x0021), (0x0023, 0x0026), (0x0028, 0x007E), (0x00A1, 0x00AC),
            (0x00AE, 0x00FF), (0x0100, 0x017F), (0x0180, 0x024F), (0x2C60, 0x2C7F), (0x16A0, 0x16F0),
            (0x0370, 0x0377), (0x037A, 0x037E), (0x0384, 0x038A), (0x038C, 0x038C)]

            alphabet = [get_char(code_point) for current_range in include_ranges
            for code_point in range(current_range[0], current_range[1] + 1)]
            return ''.join(random.choice(alphabet) for i in range(length))

        inp = get_random_unicode(94)

        def remove3(string):
            return string.replace("1", inp[1:2]).replace("2", inp[2:3]).replace("3", inp[3:4]).replace("4", inp[4:5]).replace("5", inp[5:6]) \
                .replace("6", inp[6:7]).replace("7", inp[7:8]).replace("8", inp[8:9]).replace("9",inp[9:10]).replace("0", inp[0:1]) \
                .replace("!", inp[10:11]).replace("£", inp[11:12]).replace("$", inp[12:13]).replace("%", inp[13:14]).replace("^", inp[14:15]).replace("&", inp[15:16]) \
                .replace("*", inp[16:17]).replace("(", inp[17:18]).replace(")", inp[18:19]).replace("-", inp[19:20]).replace("+", inp[20:21]) \
                .replace(" ", inp[21:22]).replace('=', inp[22:23]).replace("{", inp[23:24]).replace("}", inp[24:25]).replace(":", inp[25:26]) \
                .replace(";", inp[26:27]).replace("@", inp[27:28]).replace("~", inp[28:29]).replace("'", inp[29:30]).replace("#", inp[30:31]) \
                .replace("<", inp[31:32]).replace(">", inp[32:33]).replace(",", inp[33:34]).replace(".", inp[34:35]).replace("?", inp[35:36]) \
                .replace("/", inp[36:37]).replace("|", inp[37:38]).replace("\"", inp[38:39]).replace("\\", inp[39:40]).replace("a", inp[40:41]) \
                .replace("b", inp[41:42]).replace("c", inp[42:43]).replace("d", inp[43:44]).replace("e", inp[44:45]).replace("f", inp[45:46]) \
                .replace("g", inp[46:47]).replace("h", inp[47:48]).replace("i", inp[48:49]).replace("j", inp[49:50]).replace("k", inp[50:51]) \
                .replace("l", inp[51:52]).replace("m", inp[52:53]).replace("n", inp[53:54]).replace("o", inp[54:55]).replace("p", inp[55:56]) \
                .replace("q", inp[56:57]).replace("r", inp[57:58]).replace("s", inp[58:59]).replace("t", inp[59:60]).replace("u", inp[60:61]) \
                .replace("v", inp[61:62]).replace("w", inp[62:63]).replace("x", inp[63:64]).replace("y", inp[64:65]).replace("z", inp[65:66]) \
                .replace("A", inp[66:67]).replace("B", inp[67:68]).replace("B", inp[68:69]).replace("C", inp[69:70]).replace("D", inp[70:71]) \
                .replace("E", inp[71:72]).replace("F", inp[72:73]).replace("G", inp[73:74]).replace("H", inp[74:75]).replace("I", inp[75:76]) \
                .replace("J", inp[76:77]).replace("K", inp[77:78]).replace("L", inp[78:79]).replace("M", inp[79:80]).replace("N", inp[80:81]) \
                .replace("O", inp[81:82]).replace("P", inp[82:83]).replace("Q", inp[83:84]).replace("R", inp[84:85]).replace("S", inp[85:86]) \
                .replace("T", inp[86:87]).replace("U", inp[87:88]).replace("V", inp[88:89]).replace("W", inp[89:90]).replace("X", inp[90:91]) \
                .replace("Y", inp[91:92]).replace("Z", inp[92:93])

        ciphertextmangle2 = remove3(ciphertextmangle)
        possible = ciphertextmangle2
        ciphertextmangle0 = ciphertextmangle2

        def remove2(string):
            return string.replace(inp[1:2], "1").replace(inp[2:3], "2").replace(inp[3:4], "3").replace(inp[4:5],"4").replace(inp[5:6], "5") \
                .replace(inp[6:7], "6").replace(inp[7:8], "7").replace(inp[8:9], "8").replace(inp[9:10],"9").replace(inp[0:1],"0") \
                .replace(inp[10:11], "!").replace(inp[11:13], "£").replace(inp[12:14], "$").replace(inp[13:14],"%").replace(inp[14:15], "^").replace(inp[15:16], "&") \
                .replace(inp[16:17], "*").replace(inp[17:18], "(").replace(inp[18:19], ")").replace(inp[19:20],"-").replace(inp[20:21], "+") \
                .replace(inp[21:22], " ").replace(inp[22:23], '=').replace(inp[23:24], "{").replace(inp[24:25],"}").replace(inp[25:26], ":") \
                .replace(inp[26:27], ";").replace(inp[27:28], "@").replace(inp[28:29], "~").replace(inp[29:30],"'").replace(inp[30:31], "#") \
                .replace(inp[31:32], "<").replace(inp[32:33], ">").replace(inp[33:34], ",").replace(inp[34:35],".").replace(inp[35:36], "?") \
                .replace(inp[36:37], "/").replace(inp[37:38], "|").replace(inp[38:39], "\"").replace(inp[39:40],"\\").replace(inp[40:41], "a") \
                .replace(inp[41:42], "b").replace(inp[42:43], "c").replace(inp[43:44], "d").replace(inp[44:45],"e").replace(inp[45:46], "f") \
                .replace(inp[46:47], "g").replace(inp[47:48], "h").replace(inp[48:49], "i").replace(inp[49:50],"j").replace(inp[50:51], "k") \
                .replace(inp[51:52], "l").replace(inp[52:53], "m").replace(inp[53:54], "n").replace(inp[54:55],"o").replace(inp[55:56], "p") \
                .replace(inp[56:57], "q").replace(inp[57:58], "r").replace(inp[58:59], "s").replace(inp[59:60],"t").replace(inp[60:61], "u") \
                .replace(inp[61:62], "v").replace(inp[62:63], "w").replace(inp[63:64], "x").replace(inp[64:65],"y").replace(inp[65:66], "z") \
                .replace(inp[66:67], "A").replace(inp[67:68], "B").replace(inp[68:69], "B").replace(inp[69:70],"C").replace(inp[70:71], "D") \
                .replace(inp[71:72], "E").replace(inp[72:73], "F").replace(inp[73:74], "G").replace(inp[74:75],"H").replace(inp[75:76], "I") \
                .replace(inp[76:77], "J").replace(inp[77:78], "K").replace(inp[78:79], "L").replace(inp[79:80],"M").replace(inp[80:81], "N") \
                .replace(inp[81:82], "O").replace(inp[82:83], "P").replace(inp[83:84], "Q").replace(inp[84:85],"R").replace(inp[85:86], "S") \
                .replace(inp[86:87], "T").replace(inp[87:88], "U").replace(inp[88:89], "V").replace(inp[89:90],"W").replace(inp[90:91], "X") \
                .replace(inp[91:92], "Y").replace(inp[92:93], "Z")

        ciphertextmangle2 = remove2(ciphertextmangle0)
        if hi == "1":
            break
        if y == 1000:
            y = 0
            print("Trial number", xencrypt, "--- %s seconds ---" % (time.time() - start_time))

        if ciphertextmangle2 == ciphertextmangle:
            inposs = inp + possible
            code = base64.b64encode(zlib.compress(inposs.encode('utf-8'), 9))
            code = code.decode('utf-8')
            xencrypt = 0
            y = 0
            ciphertextmangle = code
            start_time = time.time()
            while True:
                xencrypt = xencrypt + 1
                y = y + 1
                for i in range(1):
                    get_random_unicode(94)

                    if __name__ == '__main__':
                        with open('KEY.txt', 'r') as i:
                            inpU = i.read()
                            inpE = zlib.decompress(base64.b64decode(inpU))
                            inp = inpE.decode()

                ciphertextmangle2 = remove3(ciphertextmangle)
                possible = ciphertextmangle2
                ciphertextmangle = ciphertextmangle2
                ciphertextmangle2 = remove2(ciphertextmangle)

                if hi == "1":
                    break
                if y == 1000:
                    y = 0
                    print("Trial number", xencrypt, "--- %s seconds ---" % (time.time() - start_time))

                if ciphertextmangle2 == code:
                    code = base64.b64encode(zlib.compress(possible.encode('utf-8'), 9))
                    code = code.decode('utf-8')

                    hi = "1"
                    break

    return code


async def decrypt(ctx):
    ciphertextmangleunedit1 = ctx
    with open('KEY.txt', 'r') as i:
        inpU = i.read()
        inpE = zlib.decompress(base64.b64decode(inpU))
        inp = inpE.decode()

    ciphertextmangleunedit1 = zlib.decompress(base64.b64decode(ciphertextmangleunedit1))
    time.sleep(0.05)
    ciphertextmangleunedit = ciphertextmangleunedit1.decode()
    time.sleep(0.05)
    ciphertextmangle = " " + ciphertextmangleunedit

    def remove2(string):
        return string.replace(inp[1:2], "1").replace(inp[2:3], "2").replace(inp[3:4], "3").replace(inp[4:5],"4").replace(inp[5:6], "5") \
            .replace(inp[6:7], "6").replace(inp[7:8], "7").replace(inp[8:9], "8").replace(inp[9:10], "9").replace(inp[0:1], "0") \
            .replace(inp[10:11], "!").replace(inp[11:13], "£").replace(inp[12:14], "$").replace(inp[13:14],"%").replace(inp[14:15], "^").replace(inp[15:16], "&") \
            .replace(inp[16:17], "*").replace(inp[17:18], "(").replace(inp[18:19], ")").replace(inp[19:20],"-").replace(inp[20:21], "+") \
            .replace(inp[21:22], " ").replace(inp[22:23], '=').replace(inp[23:24], "{").replace(inp[24:25],"}").replace(inp[25:26], ":") \
            .replace(inp[26:27], ";").replace(inp[27:28], "@").replace(inp[28:29], "~").replace(inp[29:30],"'").replace(inp[30:31], "#") \
            .replace(inp[31:32], "<").replace(inp[32:33], ">").replace(inp[33:34], ",").replace(inp[34:35],".").replace(inp[35:36], "?") \
            .replace(inp[36:37], "/").replace(inp[37:38], "|").replace(inp[38:39], "\"").replace(inp[39:40],"\\").replace(inp[40:41], "a") \
            .replace(inp[41:42], "b").replace(inp[42:43], "c").replace(inp[43:44], "d").replace(inp[44:45],"e").replace(inp[45:46], "f") \
            .replace(inp[46:47], "g").replace(inp[47:48], "h").replace(inp[48:49], "i").replace(inp[49:50],"j").replace(inp[50:51], "k") \
            .replace(inp[51:52], "l").replace(inp[52:53], "m").replace(inp[53:54], "n").replace(inp[54:55],"o").replace(inp[55:56], "p") \
            .replace(inp[56:57], "q").replace(inp[57:58], "r").replace(inp[58:59], "s").replace(inp[59:60],"t").replace(inp[60:61], "u") \
            .replace(inp[61:62], "v").replace(inp[62:63], "w").replace(inp[63:64], "x").replace(inp[64:65],"y").replace(inp[65:66], "z") \
            .replace(inp[66:67], "A").replace(inp[67:68], "B").replace(inp[68:69], "B").replace(inp[69:70],"C").replace(inp[70:71], "D") \
            .replace(inp[71:72], "E").replace(inp[72:73], "F").replace(inp[73:74], "G").replace(inp[74:75],"H").replace(inp[75:76], "I") \
            .replace(inp[76:77], "J").replace(inp[77:78], "K").replace(inp[78:79], "L").replace(inp[79:80],"M").replace(inp[80:81], "N") \
            .replace(inp[81:82], "O").replace(inp[82:83], "P").replace(inp[83:84], "Q").replace(inp[84:85],"R").replace(inp[85:86], "S") \
            .replace(inp[86:87], "T").replace(inp[87:88], "U").replace(inp[88:89], "V").replace(inp[89:90],"W").replace(inp[90:91], "X") \
            .replace(inp[91:92], "Y").replace(inp[92:93], "Z")

    ciphertextmangle2 = remove2(ciphertextmangle)
    ciphertextmangleunedit1 = ciphertextmangle2[1:]
    ciphertextmangleunedit = zlib.decompress(base64.b64decode(ciphertextmangleunedit1))
    ciphertextmangleunedit1 = ciphertextmangleunedit.decode()
    inp = ciphertextmangleunedit1[0:94]
    ciphertextmangle0 = ciphertextmangleunedit1[94:]
    ciphertextmangle2 = remove2(ciphertextmangle0)

    return ciphertextmangle2