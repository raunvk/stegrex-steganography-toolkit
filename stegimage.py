from PIL import Image
import binascii
import optparse
from colored import fg, bg, attr

color1 = fg('green')
color2 = fg('yellow')
reset = attr('reset')

try:
	file1 = open('image.txt', 'r')
	print(' ')
	print (color1 + file1.read() + reset)
	file1.close()
except IOError:
	print('\nBanner File not found!')


def rgb_to_hex(r, g, b):
	return '#{:02x}{:02x}{:02x}'.format(r, g, b)


def hex_to_rgb(hexcode):
	return tuple(map(ord, hexcode[1:].decode('hex')))


def str_to_bin(message):
	binary = bin(int(binascii.hexlify(message), 16))
	return binary[2:]


def bin_to_str(binary):
	message = binascii.unhexlify('%x' % (int('0b' + binary, 2)))
	return message


def encode(hexcode, digit):
	if hexcode[-1] in ('0', '1', '2', '3', '4', '5'):
		hexcode = hexcode[:-1] + str(digit)
		return hexcode
	else:
		return None


def decode(hexcode):
	if hexcode[-1] in ('0', '1'):
		return hexcode[-1]
	else:
		return None


def encrypt(filename, message):
	img = Image.open(filename)
	binary = str_to_bin(message) + '1111111111111110'
	if img.mode in ('RGBA'):
		img = img.convert('RGBA')
		data = img.getdata()
		new_data = []
		digit = 0;

		for item in data:
			if (digit< len(binary)):
				newpix = encode(rgb_to_hex(item[0], item[1], item[2]), binary[digit])
				if newpix == None:
					new_data.append(item)

				else:
					r, g, b = hex_to_rgb(newpix)					
					new_data.append((r, g, b, 255))
					digit += 1

			else:
				new_data.append(item)

		img.putdata(new_data)
		newfile = raw_input(color2 + 'Enter new filename for the encrypted image (include png/jpeg extension) : ' + reset)
		print('\n')
		img.save(newfile, 'PNG')
		return 'Encryption Successful!'
	return 'Incorrect Image mode! Please select another Image!'




def decrypt(filename):
	img = Image.open(filename)
	binary = ''

	if img.mode in ('RGBA'):
		img = img.convert('RGBA')
		data = img.getdata()

		for item in data:
			digit = decode(rgb_to_hex(item[0], item[1], item[2]))
			if digit == None:
				pass
			else:
				binary = binary + digit
				if (binary[-16:] == '1111111111111110'):
					print('Decryption Successful!')
					print('\n')
					print(color2 + 'Retrieved message :\n' + reset)
					return bin_to_str(binary[:-16])
		return bin_to_str(binary + reset)
	return 'Incorrect Image mode! Could not retrieve data!'


def Main():
	print(color1 + '--------------------WELCOME TO STEGREX IMAGE STEGANOGRAPHY--------------------\n' + reset)
	choice = raw_input(color2 + 'Press E to Encrypt or D to Decrypt : ' + reset)
	print('\n')

	if choice.upper() == 'E':
		file1 = raw_input(color2 + 'Enter image filename (include png/jpeg extension) : ' + reset)
		print('\n')
		text = raw_input(color2 + 'Enter a message to hide : ' + reset)
		print('\n')
		print(encrypt(file1, text))
		print('\n')

	elif choice.upper() == 'D':
		file1 = raw_input(color2 + 'Enter image filename (include extension) : ' + reset)
		print('\n')
		print(decrypt(file1))
		print('\n')


if __name__ == '__main__':
	Main()

