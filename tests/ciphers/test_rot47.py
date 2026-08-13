import pytest
from cipher.ciphers.rot47 import Rot47Cipher


@pytest.mark.parametrize("text, expected", [
    ("Hello World!", "w6==@ (@C=5P"),
    # r"": backslash to celowy przypadek (kod 92, w zakresie), bez r Python ostrzega o '\?'
    (r"Tu test różnych wartości, takich jak 1,2,3 lub []\?><",
     "%F E6DE Cóż?J49 H2CE@ś4:[ E2<:49 ;2< `[a[b =F3 ,.-nmk"),
    ("Oddzielnie testujemy ! oraz ~", "~55K:6=?:6 E6DEF;6>J P @C2K O"),
    ("", "")
])
def test_encrypt(text, expected):
    assert Rot47Cipher().encrypt(text) == expected


@pytest.mark.parametrize("text, expected", [
    ("w6==@ (@C=5P", "Hello World!"),
    ("","")
])
def test_decrypt(text, expected):
    assert Rot47Cipher().decrypt(text) == expected


@pytest.mark.parametrize("text", [
    "Zestaw testowy numer 2, z różnymi znakami, takimi jak ! oraz ~",
    "Możemy dodać jeszcze []{}:'|"
])
def test_decrypt_reverses_encrypt(text):
    rot47 = Rot47Cipher()
    assert rot47.decrypt(rot47.encrypt(text)) == text