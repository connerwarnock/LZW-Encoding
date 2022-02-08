# Author: Conner Warnock
# This program takes an input txt file and compresses it using the LZW method, as well as decoding an LZW
# encoded file, and getting the longest encoded string and average length of encoded string
# October 17, 2020

import binascii
import copy

# Reads in file
file_data = []
with open("EE6743_grail_testfile.txt") as TestFile:
    for line in TestFile:
        file_data.append(line)

# Reorganize source as list of characters
temp_file_data = []
for i in range(0, len(file_data)):
    for j in range(0, len(file_data[i])):
        temp_file_data.append(file_data[i][j])
file_data = copy.deepcopy(temp_file_data)


# The word doc lists a carriage return '\r', of which none were found in the text file
# Total of 29 characters including new line, space, and end of file
source_alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',' ','\n','\x03']


# Initializes LZW table with 16-bit binary strings for the source alphabet
def initialize_lzw_table(source_alphabet):
    lzw_table = []
    lzw_table_row = []
    for i in range(0, len(source_alphabet)):
        lzw_table_row.clear()
        # Decimal Index
        lzw_table_row.append(i)
        # Dictionary Symbol
        lzw_table_row.append(source_alphabet[i])
        # Filler Space
        lzw_table_row.append('')
        lzw_table_row.append('')
        lzw_table_row.append('')
        # Binary Code
        binary_code = bin(i)
        binary_code = binary_code[2:]
        binary_code = binary_code.zfill(16)
        lzw_table_row.append(binary_code)
        lzw_table.append(lzw_table_row[:])

    return lzw_table


# Builds LZW table and encodes source
def encode(file_data, lzw_table):
    # Parse Source
    data_is_present = True
    i = 0
    while data_is_present:
        # Search for character in table
        current_symbol = file_data[i]
        next_symbol = file_data[i+1]
        dictionary_symbol = current_symbol + next_symbol
        # Check if dictionary symbol can found in LZW table
        symbol_found = True
        # Loops to find new dictionary symbol
        while symbol_found:
            print(i)
            symbol_found = False
            for k in range(0, len(lzw_table)):
                if dictionary_symbol == lzw_table[k][1]:
                    symbol_found = True
            if symbol_found:
                current_symbol = dictionary_symbol
                next_symbol = file_data[i+2]
                dictionary_symbol = current_symbol + next_symbol
                i = i + 1
            else:
                lzw_table_row = []
                lzw_table_row.append(len(lzw_table))
                lzw_table_row.append(dictionary_symbol)
                lzw_table_row.append(current_symbol)
                lzw_table_row.append(next_symbol)
                # Get decimal code of current symbol
                for k in range(0, len(lzw_table)):
                    if current_symbol == lzw_table[k][1]:
                        lzw_table_row.append(lzw_table[k][0])
                        # Convert decimal to binary code
                        binary_code = bin(lzw_table[k][0])
                        binary_code = binary_code[2:]
                        binary_code = binary_code.zfill(16)
                        lzw_table_row.append(binary_code)
                lzw_table.append(lzw_table_row[:])
                lzw_table_row.clear()
            if i == (len(file_data) - 1):
                data_is_present = False
                symbol_found = False
        i = i + 1
        if i == 60000:
            y = 0

        if i == (len(file_data) - 1):
            data_is_present = False
    # Add end of file
    lzw_table_row.append('')
    lzw_table_row.append('')
    lzw_table_row.append('')
    lzw_table_row.append('')
    lzw_table_row.append('')
    lzw_table_row.append(lzw_table[len(source_alphabet)-1][5])
    lzw_table.append(lzw_table_row[:])

    return lzw_table


# The compression will be the size of the symbol dictionary divided by the original amount of symbols
# The Lavg should be the inverse of the compression: i.e. the average bits required to represent a symbol.
# The reason frequency is unimportant is because we are using a fixed-length code. If we were using a
# variable-length code, this would be different
def get_compression_and_Lavg(lzw_table, file_data):
    compression = len(lzw_table) / len(file_data)
    print("Compression: ", compression*100, "%")
    Lavg = len(file_data) / len(lzw_table)
    print("Lavg: ", Lavg, "bits")

    return


# Finds and prints longest string (symbol) in symbol dictionary
def get_longest_string(lzw_table):
    longest_string = ''
    longest_string_length = 0
    for i in range(0, len(lzw_table)):
        string = lzw_table[i][1]
        string_length = len(string)
        if string_length > longest_string_length:
            longest_string_length = string_length
            longest_string = string
    print("Longest String: ", longest_string)
    print("Longest String Length: ", longest_string_length)

    return


# Decodes encoded data and verifies it matches the original data file
def decode(lzw_table, file_data):
    decoded_file = []
    for i in range(len(source_alphabet), len(lzw_table)):
        binary_code = lzw_table[i][5]
        # Binary to ascii
        decimal_code = int(binary_code, 2)
        current_symbol = lzw_table[decimal_code][1]
        for j in range(0, len(current_symbol)):
            decoded_file.append(current_symbol[j])
    print("Original File: ", file_data)
    print("Decoded File: ", decoded_file)
    # Verify
    verified = True
    for i in range(0, len(file_data)):
        if file_data[i] != decoded_file[i]:
            verified = False
    print("Verification Status: ", verified)

    return


lzw_table = initialize_lzw_table(source_alphabet)
lzw_table = encode(file_data, lzw_table)
print("LZW Table: ", lzw_table)
get_compression_and_Lavg(lzw_table, file_data)
get_longest_string(lzw_table)
decode(lzw_table, file_data)







