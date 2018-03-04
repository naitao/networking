
def binary_to_decimal(bits):
    decimal = 0
    for i in range(len(bits)):
        decimal += int(bits[-i-1]) * pow(2,i)
    return decimal
def checkbits(number, max):
    '''
    Input Value:
               integer like 1,2,3...
    Return Value:
               []
    '''
    if number > max:
        print("Error: please increase the quantity on max!")
        return []
    bits_list = []
    bits_locations = []    
    def decimal_to_binary(num):
        return bin(num)[2:]
        

    for i in range(pow(2, number-1), pow(2,max+1)):
        bit = bin(i)[2:]
        if bit[-number] == '1':
            bits_list.append(bin(i)[2:])
    for bits in bits_list:
        bits_locations.append(binary_to_decimal(bits))
    return bits_locations


def main():
    print(binary_to_decimal("1000111"))
    checkbits(1,5)
    checkbits(2,5)
    checkbits(3,5)
    checkbits(4,5)
    checkbits(5,5)

if __name__ == '__main__':
    main()
