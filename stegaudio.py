import wave
from colored import fg, bg, attr

color1 = fg('green')
color2 = fg('yellow')
reset = attr('reset')

try:
	file1 = open('audio.txt', 'r')
	print(' ')
	print (color1 + file1.read() + reset)
	file1.close()
except IOError:
	print('\nBanner File not found!')


def encrypt(filename, message):
	try:
		song = wave.open(filename, mode='rb')
		frame_bytes = bytearray(list(song.readframes(song.getnframes())))

		message = message + int((len(frame_bytes)-(len(message)*8*8))/8) *'#'
		bits = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8,'0') for i in message])))

		for i, bit in enumerate(bits):
    			frame_bytes[i] = (frame_bytes[i] & 254) | bit
	
		frame_modified = bytes(frame_bytes)

		newfile = input(color2 + 'Enter new filename for the encrypted audio (include wav extension) : ' + reset)
		print('\n')
		with wave.open(newfile, 'wb') as fd:
    			fd.setparams(song.getparams())
    			fd.writeframes(frame_modified)
	
		song.close()
		return 'Encryption Successful!'

	except IOError:
		return 'Incorrect Audio mode! Please select another Audio!'


def decrypt(filename):
	try:
		song = wave.open(filename, mode='rb')
		frame_bytes = bytearray(list(song.readframes(song.getnframes())))

		extracted = [frame_bytes[i] & 1 for i in range(len(frame_bytes))]
		string = "".join(chr(int("".join(map(str,extracted[i:i+8])),2)) for i in range(0,len(extracted),8))
		decoded = string.split("###")[0]


		print('Decryption Successful!')
		print('\n')
		print(color2 + 'Retrieved message :\n' + reset)
		return decoded
		song.close()

	except IOError:
		return 'Incorrect Image mode! Could not retrieve data!'
    


def Main():
	print(color1 + '-----------------WELCOME TO STEGREX AUDIO STEGANOGRAPHY-----------------\n' + reset)
	choice = input(color2 + 'Press E to Encrypt or D to Decrypt : ' + reset)
	print('\n')

	if choice.upper() == 'E':
		file1 = input(color2 + 'Enter audio filename (include wav extension) : ' + reset)
		print('\n')
		text = input(color2 + 'Enter a message to hide : ' + reset)
		print('\n')
		print(encrypt(file1, text))
		print('\n')

	elif choice.upper() == 'D':
		file1 = input(color2 + 'Enter audio filename (include extension) : ' + reset)
		print('\n')
		print(decrypt(file1))
		print('\n')


if __name__ == '__main__':
	Main()

