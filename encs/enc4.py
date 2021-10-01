import time
from random import randint


def shorte(ctx):
    started_at = time.time()
    global prime_numbers
    counter = 0
    for i in ctx:
        counter = counter + 1

    def get_prime_number():
        prime_numbers = []
        candidate = randint(100000, 800000)
        while True:
            if candidate <= 3:
                prime_numbers.append(candidate)
                yield candidate

            is_prime = True
            for prime_num in prime_numbers:
                if candidate % prime_num == 0:
                    is_prime = False
                    break

            if is_prime:
                prime_numbers.append(candidate)
                yield candidate

            candidate += 1

    prime_numbers = get_prime_number()
    while True:
        if next(prime_numbers) > 100000:
            if randint(1, 1000) == 1:
                num = next(prime_numbers)
                break
    newnum = ""
    for i in range(counter):
        newnum = str(newnum) + str(next(prime_numbers))
    outputenc = ""
    counter = 0
    for i in ctx:
        counter = counter + 1
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        partialOne = ""
        partialTwo = ""
        newAlphabet = ""
        msg = i
        if msg in alphabet:
            key = newnum[counter:counter + 1]
            key = int(key)
            if key == 0:
                newAlphabet = alphabet
            elif key > 0:
                partialOne = alphabet[:key]
                partialTwo = alphabet[key:]
                newAlphabet = partialTwo + partialOne
            else:
                partialOne = alphabet[:(26 + key)]
                partialTwo = alphabet[(26 + key):]
                newAlphabet = partialTwo + partialOne
            encrypted = ""
            for message_index in range(0, len(msg)):
                if msg[message_index] == " ":
                    encrypted += " "
                for alphabet_index in range(0, len(newAlphabet)):
                    if msg[message_index] == alphabet[alphabet_index]:
                        encrypted += newAlphabet[alphabet_index]
            outputenc = outputenc + encrypted
        else:
            outputenc = outputenc + msg
        num = str(num).replace("0", "g").replace("1", "e").replace("2", "k").replace("3", "i").replace("4", "u")\
        .replace("5", "d").replace("6", "r").replace("7", "w").replace("8", "q").replace("9", "p")
    #print(f"Took {round(time.time() - started_at,2)}")
    return num + outputenc


def shortd(ctx):
    started_at = time.time()
    counter = 0
    for i in ctx:
        counter = counter + 1
    content = str(ctx[:6]).replace("g", "0").replace("e", "1").replace("k", "2").replace("i", "3")\
    .replace("u", "4").replace("d", "5").replace("r", "6").replace("w", "7").replace("q", "8").replace("p", "9")

    def get_prime_number():
        prime_numbers = []
        candidate = int(content)
        while True:
            if candidate <= 3:
                prime_numbers.append(candidate)
                yield candidate

            is_prime = True
            for prime_num in prime_numbers:
                if candidate % prime_num == 0:
                    is_prime = False
                    break

            if is_prime:
                prime_numbers.append(candidate)
                yield candidate

            candidate += 1

    prime_numbers = get_prime_number()
    while True:
        x = next(prime_numbers)
        if x == int(content):
            num = x
            break
    newnum = ""
    for i in range(counter):
        newnum = str(newnum) + str(next(prime_numbers))
    counter = 0
    outputend = ""
    for letter in ctx[6:]:
        counter = counter + 1
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        partialOne = ""
        partialTwo = ""
        newAlphabet = ""
        msg = letter
        if msg in alphabet:
            key = newnum[counter:counter + 1]
            key = int(key)
            key = key - key - key
            if key == 0:
                newAlphabet = alphabet
            elif key > 0:
                partialOne = alphabet[:key]
                partialTwo = alphabet[key:]
                newAlphabet = partialTwo + partialOne
            else:
                partialOne = alphabet[:(26 + key)]
                partialTwo = alphabet[(26 + key):]
                newAlphabet = partialTwo + partialOne
            encrypted = ""
            for message_index in range(0, len(msg)):
                if msg[message_index] == " ":
                    encrypted += " "
                for alphabet_index in range(0, len(newAlphabet)):
                    if msg[message_index] == alphabet[alphabet_index]:
                        encrypted += newAlphabet[alphabet_index]
            outputend = outputend + encrypted
        else:
            outputend = outputend + msg

    #print(f"Took {round(time.time() - started_at,2)}")
    return outputend