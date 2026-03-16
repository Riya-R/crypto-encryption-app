import streamlit as st

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Cryptography Studio",
    page_icon="🔐",
    layout="centered"
)

# ---------------- BACKGROUND IMAGE ----------------
page_bg = """
<style>
[data-testid="stAppViewContainer"] {
background-image: url("https://images.unsplash.com/photo-1550751827-4bd374c3f58b");
background-size: cover;
background-position: center;
background-repeat: no-repeat;
}

[data-testid="stHeader"]{
background: rgba(0,0,0,0);
}

.block-container{
background-color: rgba(0,0,0,0.75);
padding: 2rem;
border-radius: 10px;
}

h1, h2, h3, p, label {
color: white !important;
}
</style>
"""

st.markdown(page_bg, unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.title("🔐 Cryptography Encryption Studio")
st.write("Interactive platform to demonstrate classical encryption and decryption techniques.")

# ---------------- ALGORITHM SWITCH ----------------
algorithm = st.radio(
    "Choose Encryption Technique",
    ["Caesar Cipher", "Vigenere Cipher", "Rail Fence Cipher"],
    horizontal=True
)

# ---------------- INPUT TEXT ----------------
text = st.text_area("Enter Plaintext / Ciphertext")

# ---------------- KEY INPUT ----------------
key = None

if algorithm == "Caesar Cipher":
    key = st.number_input("Enter Shift Key", value=3)

elif algorithm == "Vigenere Cipher":
    key = st.text_input("Enter Keyword").upper()

elif algorithm == "Rail Fence Cipher":
    key = st.number_input("Enter Number of Rails", min_value=2, value=3)

# ---------------- CAESAR FUNCTIONS ----------------
def caesar_encrypt(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            result += chr((ord(char.upper()) - 65 + shift) % 26 + 65)
        else:
            result += char
    return result


def caesar_decrypt(text, shift):
    return caesar_encrypt(text, -shift)

# ---------------- VIGENERE FUNCTIONS ----------------
def vigenere_encrypt(text, key):

    if len(key) == 0:
        return None

    result = ""
    j = 0

    for char in text.upper():
        if char.isalpha():
            shift = ord(key[j % len(key)]) - 65
            result += chr((ord(char) - 65 + shift) % 26 + 65)
            j += 1
        else:
            result += char

    return result


def vigenere_decrypt(text, key):

    if len(key) == 0:
        return None

    result = ""
    j = 0

    for char in text.upper():
        if char.isalpha():
            shift = ord(key[j % len(key)]) - 65
            result += chr((ord(char) - 65 - shift) % 26 + 65)
            j += 1
        else:
            result += char

    return result

# ---------------- RAIL FENCE FUNCTIONS ----------------
def rail_fence_encrypt(text, rails):

    fence = [[] for _ in range(rails)]

    rail = 0
    direction = 1

    for char in text:
        fence[rail].append(char)
        rail += direction

        if rail == rails - 1 or rail == 0:
            direction *= -1

    result = ""

    for row in fence:
        result += "".join(row)

    return result


def rail_fence_decrypt(cipher, rails):

    fence = [['\n' for i in range(len(cipher))]
             for j in range(rails)]

    direction_down = None
    row, col = 0, 0

    for i in range(len(cipher)):

        if row == 0:
            direction_down = True
        if row == rails - 1:
            direction_down = False

        fence[row][col] = '*'
        col += 1

        if direction_down:
            row += 1
        else:
            row -= 1

    index = 0

    for i in range(rails):
        for j in range(len(cipher)):
            if fence[i][j] == '*' and index < len(cipher):
                fence[i][j] = cipher[index]
                index += 1

    result = []
    row, col = 0, 0

    for i in range(len(cipher)):

        if row == 0:
            direction_down = True
        if row == rails - 1:
            direction_down = False

        if fence[row][col] != '*':
            result.append(fence[row][col])
            col += 1

        if direction_down:
            row += 1
        else:
            row -= 1

    return "".join(result)

# ---------------- BUTTONS ----------------
col1, col2 = st.columns(2)

with col1:

    if st.button("Encrypt"):

        if text.strip() == "":
            st.error("⚠️ Please enter text first.")

        elif algorithm == "Caesar Cipher":

            result = caesar_encrypt(text, key)
            st.success("Encrypted Text: " + result)

        elif algorithm == "Vigenere Cipher":

            if key == "":
                st.error("⚠️ Please enter a keyword.")
            else:
                result = vigenere_encrypt(text, key)
                st.success("Encrypted Text: " + result)

        elif algorithm == "Rail Fence Cipher":

            result = rail_fence_encrypt(text, key)
            st.success("Encrypted Text: " + result)

with col2:

    if st.button("Decrypt"):

        if text.strip() == "":
            st.error("⚠️ Please enter text first.")

        elif algorithm == "Caesar Cipher":

            result = caesar_decrypt(text, key)
            st.info("Decrypted Text: " + result)

        elif algorithm == "Vigenere Cipher":

            if key == "":
                st.error("⚠️ Please enter a keyword.")
            else:
                result = vigenere_decrypt(text, key)
                st.info("Decrypted Text: " + result)

        elif algorithm == "Rail Fence Cipher":

            result = rail_fence_decrypt(text, key)
            st.info("Decrypted Text: " + result)

# ---------------- FOOTER ----------------
st.write("---")
st.write("Created for CNS Lab CIA by **Kiera Dcosta 🩷 and Riya Gawde 🩷**")