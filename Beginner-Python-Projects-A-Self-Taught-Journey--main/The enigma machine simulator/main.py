from wheels import *
from string import ascii_lowercase as alphabet

def pass_letter_through_wheel(letter, wheel):
  letter = letter.lower()
  return wheel[letter]
  
def encrypt_letter(letter):
  # wheel 1
  letter = caesar_shift(letter, key_1)
  letter = pass_letter_through_wheel(letter, w_1)
  
  # wheel 2
  letter = caesar_shift(letter, key_2)
  letter = pass_letter_through_wheel(letter, w_2)
  
  # wheel 3
  letter = caesar_shift(letter, key_3)
  letter = pass_letter_through_wheel(letter, w_3)
  
  # reflector
  letter = pass_letter_through_wheel(letter, reflector)
  
  # wheel -3
  letter = pass_letter_through_wheel(letter, w_3)
  letter = caesar_shift(letter, -key_3)
  
  # wheel -2
  letter = pass_letter_through_wheel(letter, w_2)
  letter = caesar_shift(letter, -key_2)
  
  # wheel -1
  letter = pass_letter_through_wheel(letter, w_1)
  letter = caesar_shift(letter, -key_1)
  
  return letter

def caesar_shift(letter, key):
  letter = ord(letter) - 97
  letter = (letter + key) % 26
  return chr(letter + 97)

# keys
key_1 = 6
key_2 = 19
key_3 = 21

#wheels 
w_1 = wheel_3
w_2 = wheel_4
w_3 = wheel_1

# driver
message = input("Encrypt a message: ")
print 'Original: %s' % message #not compusory anless i want to revisete the original message

encrypted_message = ''
for character in message.lower():
  if character in alphabet:
    encrypted_message += encrypt_letter(character)
  else:
    encrypted_message += character
    
print 'Encrypted message: %s' % encrypted_message

