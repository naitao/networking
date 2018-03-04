import argparse


def encode(bit_str):
    '''
    - This method is only focusing on bits
      from 0(1 bit) to 111111111111111 (15bits)
    - The convertion is from source code to hamming code, which will follow
      the rules like below:
    	p1_bit = [1,3,5,7,9,11,13,15,17,19]
    	p2_bit = [2,3,6,7,10,11,14,15,18,19]
    	p4_bit = [4,5,6,7,12,13,14,15,20]
    	p8_bit = [8,9,10,11,12,13,14,15]
    	p16_bit = [16,17,18,19,20]
    - Return Value:
			Hamming code string like "010010011..."
    '''

    checksum_dict = {
                     0: [1,3,5,7,9,11,13,15,17,19],
                     1: [2,3,6,7,10,11,14,15,18,19],
                     3: [4,5,6,7,12,13,14,15,20],
                     7: [8,9,10,11,12,13,14,15],
                     15: [16,17,18,19,20]
                    }

    necessary_check_bits = [1,2,4,8,16]

    length = len(bit_str)
    if length <= 0 or length > 15:
        return None
    p1 = p2 = p4 = p8 = p16 = 'x'
    encoded_bits = [p1,p2,'',p4,'','','',p8,'','','','','','','',p16,'','','','']
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
        # check if the point has arrived to the end of the list
        #if encoded_bits[i] is '':
        #    break
        #elif encoded_bits[i] == 'x' and encoded_bits[i+1] is '':
        #    break

        if encoded_bits[i] == 'x':
            bit_count = 0
            for n in checksum_dict[i]:
                if n not in necessary_check_bits and n <= len(encoded_bits):
                    bit_count += int(encoded_bits[n-1])
            # insert checksum bits with calculated digit (0 or 1)
            encoded_bits[i] = str(bit_count % 2)

    # convert list to string
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
      			True or False
    '''
    checksum_valid = True
    checksum_dict = {
                     1: [1,3,5,7,9,11,13,15,17,19],
                     2: [2,3,6,7,10,11,14,15,18,19],
                     4: [4,5,6,7,12,13,14,15,20],
                     8: [8,9,10,11,12,13,14,15],
                     16: [16,17,18,19,20]
                    }

    necessary_check_bits = [1,2,4,8,16]
    length = len(new_bits_str)
    if length <= 2  or length > 20:
        print("Warning: Out of the range!")
        return False
    encoded_bits = []
    for i in range(length):
        encoded_bits.append(int(new_bits_str[i]))

    for checksum_bit in necessary_check_bits:
        count = 0
        if checksum_bit > length:
            break
        for bit_n in checksum_dict[checksum_bit]:
            if bit_n > length:
                break
            count += encoded_bits[bit_n-1]
        if count % 2 != 0:
            print("Error check with {}th checksum bit".format(checksum_bit))
            checksum_valid = False
    return checksum_valid
        

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--encode', help="encode from a code")
    parser.add_argument('--decode', help="decode and make sure there's no error")
    args = parser.parse_args()
    if args.encode != None:
        print("The hamming code is: " +  encode(args.encode))
    elif args.decode != None:
        
        print("The validation is: ", decode(args.decode))
    else:
        pass


if __name__ == '__main__':
	main()
