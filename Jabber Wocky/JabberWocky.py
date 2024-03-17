# atob
def text_to_binary(inputFileLocation, outputFileLocation):
    with open(inputFileLocation, 'r') as file:
        content = file.read()
        bitString = ''.join(format(ord(char), '08b') for char in content)

    # saving bitString to out file named  bit-wright.txt
    with open(outputFileLocation, 'w') as file:
        file.write(bitString)
    return bitString


# btoa
def binary_to_text(binary_bits, outputFileLocation):
    # taking 8-bits as binary string
    byte_grps = [binary_bits[i:i + 8] for i in range(0, len(binary_bits), 8)]
    # Converting 8-bits to its decimal equivalent and then to corresponding character
    text = ''.join(chr(int(byte, 2)) for byte in byte_grps)

    with open(outputFileLocation, 'w') as file:
        file.write(text)
    return text


def integer_to_binary(n, length):
    binary = bin(n)[2:]
    if len(binary) < length:
        binary = '0' * (length - len(binary)) + binary
    return binary


def integer_from_binary(binary):
    decimal = 0
    power = 0
    for bit in reversed(binary):
        if bit == '1':
            decimal += 2 ** power
        power += 1
    return decimal


class JabberWocky:

    def __init__(self):
        pass  # default constructor

    def Jabber(self, inputData):
        i = 0
        lookUpTable = {0: ''}  # initialize the look-up table to have an entry for entry string
        num_of_bits = 0
        encoded_string = ''

        # to iterate over all bits in the inputData
        while i < len(inputData):
            prefix = ''
            length_of_bits = 0

            for j in range(i, len(inputData)):  # looking for longest possible new prefix
                if inputData[i:j + 1] in lookUpTable.values():
                    prefix = inputData[i:j + 1]
                    length_of_bits = list(lookUpTable.keys())[list(lookUpTable.values()).index(prefix)]

            # when at the End of file

            # to find next after the prefix
            if i + len(prefix) < len(inputData):
                current_bit_string = inputData[i + len(prefix)]
                if num_of_bits == 0:
                    encoded_string += str(current_bit_string)
                else:
                    encoded_string += integer_to_binary(length_of_bits, num_of_bits) + str(current_bit_string)
                lookUpTable[max(lookUpTable) + 1] = prefix + current_bit_string
            elif i + len(prefix) == len(inputData):
                encoded_string += integer_to_binary(length_of_bits, num_of_bits)
            else:
                break
            # Increment num_of_bits if no of items in lookUpTable to match index value with max bits needed to
            # represent it
            if (len(lookUpTable) - 1) & ((len(lookUpTable) - 1) - 1) == 0:
                num_of_bits += 1
            i += len(prefix) + 1

        print(lookUpTable)
        return encoded_string

    def Wocky(self, encodedDataBits):
        lookUpTable = {0: ''}
        num_of_bits = 0
        decoded_string = ''
        i = 0
        while i < len(encodedDataBits):
            if i + num_of_bits == len(encodedDataBits):
                current_bit_string = integer_from_binary(encodedDataBits[i:i + num_of_bits])
                if current_bit_string in lookUpTable:
                    temp = lookUpTable[current_bit_string]
                    decoded_string += temp
                    break
            elif i + num_of_bits + 1 > len(encodedDataBits):
                break
            else:
                current_bit_string = integer_from_binary(encodedDataBits[i:i + num_of_bits])
                b = encodedDataBits[i + num_of_bits]
                if current_bit_string in lookUpTable:
                    temp = lookUpTable[current_bit_string]
                    decoded_string += (temp + str(b))
                    lookUpTable[len(lookUpTable)] = temp + str(b)
                if len(lookUpTable) - 1 & (len(lookUpTable) - 1) - 1 == 0:
                    num_of_bits += 1
                    i += num_of_bits
                else:
                    i += num_of_bits + 1
        return decoded_string


# Part 1
inputFilePath = 'wright.txt'
# output file location after atob operation
outputFilePath = 'bit-wright.txt'
# output file location after btoa operation
outputFilePath2 = "ascii-wright.txt"
atob_output = text_to_binary(inputFilePath, outputFilePath)
binary_to_text(atob_output, outputFilePath2)


# Part 2
jabberwocky = JabberWocky()
with open('bit-wright_2.txt', 'r') as file:
    data = file.read()

jabber = jabberwocky.Jabber(data)
# writing output of jabber to a file
with open('zap-wright.txt', 'w') as file:
    file.write(jabber)

wocky = jabberwocky.Wocky(jabber)
# writing output of wocky to a file
with open('kapow-wright.txt', 'w') as file:
    file.write(wocky)

# Sample files
inputFilePath_sample = 'Hollow_Men.txt'
# output file location after atob operation
outputFilePath_sample = 'bit-hollow.txt'
# output file location after jabber operation
outputFilePath2_sample = "zap-hollow.txt"
# output file location after wocky operation
outputFilePath3_sample = "kapow-hollow.txt"
# output file location after btoa operation
outputFilePath4_sample = "out.txt"

# atob operation on Hollow_Men.txt and store output in bit-hollow.txt
_atob_output_sample = text_to_binary(inputFilePath_sample, outputFilePath_sample)
_jabberwocky = JabberWocky()
_jabber = _jabberwocky.Jabber(_atob_output_sample)
# writing output of jabber to file zap-hollow.txt
with open(outputFilePath2_sample, 'w') as file:
    file.write(_jabber)

_wocky = _jabberwocky.Wocky(_jabber)
# writing output of wocky to file kapow-hollow.txt
with open(outputFilePath3_sample, 'w') as file:
    file.write(_wocky)

# writing output of btoa to file out.txt
binary_to_text(_wocky, outputFilePath4_sample)
