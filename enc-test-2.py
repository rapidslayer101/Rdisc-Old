import enclib as enc
import enclib as enc_old
from random import randint
import time

#timer = time.time()
#loop = 0
#while True:
#    loop += 1
#    seed_key = enc.pass_to_seed(enc.hex_gens(randint(5, 1000)))
#    seed_data = enc.seed_to_data(seed_key)
#    if loop % 100 == 0:
#        print(loop, time.time()-timer)

seed_key = enc.pass_to_seed("hello")
print(seed_key)


alpha1, alpha2, num2, seed3 = enc.seed_to_data(seed_key)
enc1 = enc.encrypt_key("hello rupert how are you", "hello")
enc2 = enc.encrypt_key("へllお るpえrt ほw あれ よう", "hello")
enc3 = enc.encrypt_key("こんにちはルパートお元気ですか", "hello")
import sys
print(f"{enc1} = {sys.getsizeof(enc1)} bytes")
print(f"{enc2} = {sys.getsizeof(enc2)} bytes")
print(f"{enc3} = {sys.getsizeof(enc3)} bytes")

# japanese converter script

def load_jap_words():
    jap_words = {}
    with open("jap_dict.txt", encoding="utf-8") as f:
        for line in f.readlines():
            eng, jap = line.replace("\n", "").split(", ")
            jap_words.update({eng: jap})
    return jap_words


jap_words = load_jap_words()
print(jap_words)
jap_dict = {'chi': 'ち', 'shi': 'し', 'tsu': 'つ',
            'fu': 'ふ', 'ha': 'は', 'he': 'へ', 'hi': 'ひ', 'ho': 'ほ', 'ka': 'か', 'ke': 'け', 'ki': 'き', 'ko': 'こ',
            'ku': 'く', 'ma': 'ま', 'me': 'め', 'mi': 'み', 'mo': 'も', 'mu': 'む', 'na': 'な', 'ne': 'ね', 'ni': 'に',
            'no': 'の', 'nu': 'ぬ', 'ra': 'ら', 're': 'れ', 'ri': 'り', 'ro': 'ろ', 'ru': 'る', 'sa': 'さ', 'se': 'せ',
            'so': 'そ', 'su': 'す', 'ta': 'た', 'te': 'て', 'to': 'と', 'wa': 'わ', 'wo': 'を', 'ya': 'や', 'yo': 'よ',
            'yu': 'ゆ', 'a': 'あ', 'e': 'え',  'i': 'い',  'n': 'ん',  'o': 'お',  'u': 'う'}
print(jap_dict)

while True:
    original_text = input()
    saved_text = original_text
    if original_text.startswith("-add "):

        jap_words.update("")

    # japanese
    jap_text_sv = original_text
    used_words = ""
    for item in jap_words:
        original_text = original_text.replace(item, jap_words[item])
        if original_text != jap_text_sv:
            used_words += f"[{jap_words[item]} - {item}] "
        jap_text_sv = original_text

    # english represented as japanese chars
    jap_text_sv = original_text
    used = ""
    for item in jap_dict:
        original_text = original_text.replace(item, jap_dict[item])
        if original_text != jap_text_sv:
            used += f"[{jap_dict[item]} - {item}] "
        jap_text_sv = original_text
    print(original_text)
    if used_words:
        print(used_words)
    if used:
        print(used)

    enc1 = enc.encrypt_key(saved_text, "hello")
    enc2 = enc.encrypt_key(original_text, "hello")
    print(f"{enc1} = {sys.getsizeof(enc1)} bytes")
    print(f"{enc2} = {sys.getsizeof(enc2)} bytes")



input()
print(enc.decrypt_key(enc.encrypt_key("1111", "hello"), "hello"))
x = enc.encrypt(1111, alpha1, alpha2, num2, seed3)
print(x)
print(enc.encrypt(b"1111", alpha1, alpha2, num2, seed3))
print(enc.decrypt(x, alpha1, alpha2, num2, seed3))

input()
enc.encrypt_file("C:/Users/rapidslayer101/Downloads/muted.quicktime", alpha1, alpha2, num2, seed3, "enc.renc")
#enc.encrypt_file("user_agents.zip", alpha1, alpha2, num2, seed3, "user_agents.renc")
#enc.encrypt_file("C:/Users/rapidslayer101/Downloads/BetterDiscord-Windows.exe", alpha1, alpha2, num2, seed3, "muted.renc")
#enc.encrypt_file("ui.exe", alpha1, alpha2, num2, seed3, "a_file.renc")
#enc.encrypt_file("gateway.txt", alpha1, alpha2, num2, seed3, "a_file.renc")

input("Now decrypt")

print(enc.decrypt_file("enc.renc", alpha1, alpha2, num2, seed3, "file.dec"))
