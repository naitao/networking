import argparse
from networking.checkbits import checkbits
from networking.checkbits import binary_to_decimal


def encode(input_str):
    '''
    - This method can convert un-fixed bi-digit with checksum bits, in which you need to
      define the checksum bits number on size. Default checksum bits are 5 bits: 1th,2th,4th,8th,16th
    - The convertion is from source code to hamming code, which will follow
      the rules like below (You can refer to the Lecture8 slides of Gavin):
    	p1_bit = [1,3,5,7,9,11,13,15,17,19...]
    	p2_bit = [2,3,6,7,10,11,14,15,18,19...]
    	p4_bit = [4,5,6,7,12,13,14,15,20...]
    	p8_bit = [8,9,10,11,12,13,14,15...]
    	p16_bit = [16,17,18,19,20...]
        ...
    - Return Value:
			Hamming code string like "010010011..."
    '''

    # The size of checksum bits, default is 5
    size = 5
    for i in range(len(input_str)):
        if input_str[i].isdigit() and input_str[i] not in '23456789':
            bit_str = input_str
            break
        elif input_str[i].isdigit() or \
            (input_str[i].isalpha() and input_str[i].lower() in 'abcdef'):
            bit_str = bin(int(input_str,16))[2:]
            print("Binary bit: " + bit_str)
            break
    checksum_dict = {}
    for i in range(1, size+1):
        checksum_dict[pow(2,i-1)-1] = checkbits(i, size)

    necessary_check_bits = []
    for n in range(size):
        necessary_check_bits.append(pow(2,n))

    length = len(bit_str)
    if length <= 0 or length > pow(2, size)-1:
        return None

    encoded_bits = [''] * (pow(2, size+1)-1)
    for i in necessary_check_bits:
        encoded_bits[i-1] = 'x'
    for i in range(length):
        for j in range(len(encoded_bits)):
            if encoded_bits[j] == '':
                encoded_bits[j] = bit_str[i]
                break

    # Cut empty bits from list
    for m in range(len(encoded_bits)):
        if encoded_bits[m] is '':
            break
        elif encoded_bits[m] == 'x' and encoded_bits[m+1] is '':
            break
    encoded_bits = encoded_bits[:m]


    for i in range(len(encoded_bits)):
        if encoded_bits[i] == 'x':
            bit_count = 0
            for n in checksum_dict[i]:
                if n not in necessary_check_bits and n <= len(encoded_bits):
                    bit_count += int(encoded_bits[n-1])
            # insert checksum bits with calculated digit (0 or 1)
            encoded_bits[i] = str(bit_count % 2)

    # Convert list to string
    new_bits_str = ''
    for i in range(len(encoded_bits)):
        if encoded_bits[i] is '':
            break
        new_bits_str = new_bits_str + encoded_bits[i]
   
    return new_bits_str

def decode(new_bits_str):
    '''
    - This method is only focusing on bits
      from 000(3 bits) to 11111111111111111111 (20bits)
    - This function will check whether a hamming code is valid, in which the
      checking method will follow the rules like below:
    	p1_bit = [1,3,5,7,9,11,13,15,17,19]
    	p2_bit = [2,3,6,7,10,11,14,15,18,19]
    	p4_bit = [4,5,6,7,12,13,14,15,20]
    	p8_bit = [8,9,10,11,12,13,14,15]
    	p16_bit = [16,17,18,19,20]
    - Return Value:
      			boolean, error_bits
    '''
    checksum_valid = True
    # The size of checksum bits, default is 5
    size = 5
    for i in range(len(new_bits_str)):
        if new_bits_str[i].isdigit() and new_bits_str[i] not in '23456789':
            bits_str = new_bits_str
            break
        elif new_bits_str[i].isdigit() or \
            (new_bits_str[i].isalpha() and new_bits_str[i].lower() in 'abcdef'):
            bits_str = bin(int(new_bits_str,16))[2:]
            print("Binary bit: " + bits_str)
            break
    checksum_dict = {}
    for i in range(1, size+1):
        checksum_dict[pow(2,i-1)-1] = checkbits(i, size)

    length = len(bits_str)
    if length <= 2  or length > pow(2, size)+size:
        print("Warning: Out of the range!")
        return False

    necessary_check_bits = []
    for n in range(size):
        necessary_check_bits.append(pow(2,n))
    encoded_bits = []
    for i in range(length):
        encoded_bits.append(int(bits_str[i]))
    
    error_bits = ''
    for checksum_bit in necessary_check_bits:
        count = 0
        if checksum_bit > length:
            break
        for bit_n in checksum_dict[checksum_bit-1]:
            if bit_n > length:
                break
            count += encoded_bits[bit_n-1]
        if count % 2 != 0:
            error_bits = '1' + error_bits
            #print("Error check with {}th checksum bit".format(checksum_bit))
            checksum_valid = False
        else:
            error_bits = '0' + error_bits
    return checksum_valid, error_bits
        

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--encode', action="store", dest="encode", help="encode from a normal code to a hamming code")
    parser.add_argument('--decode', action="store", dest="decode", help="decode and make sure there's no error in a hamming code")
    args = parser.parse_args()
    if args.encode != None:
        print("The hamming code is: " +  encode(args.encode))
    elif args.decode != None:
        result = decode(args.decode)
        print("The validation is: ", decode(args.decode))
        if not result[0]:
            print("Bit number: {}".format(binary_to_decimal(result[1])))
    else:
        pass


if __name__ == '__main__':
	main()
