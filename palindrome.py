"""Pseudocode
a)Prompt user to choose the type of file
 i)Raw sequence
 ii)Fasta file format
 iii）Genbank file format

b)Prompt user to enter sequence( Option1 ) or enter file name ( Option 2 and 3 ), else invalid input

c)Modify the sequneces
i)For input sequences, the sequence will be capitalise before checking for palindrome subsequences
ii)For Fasta file format, the system will read the content of file then extract out the sequence using re module and followed by capitalise the sequences
iii)For Genbank file format, the system will read the content of file then extract out the seuqence using re module and followed by capitalise the sequences

d)The sequences stored into variable 'seq' and print the input sequences

e)Function reversecomp called and print the reverse complementary of input sequences

f)Print the complementary of input sequences.


g)Function make_palin called to find the palindromic substrings inside the input seqeuences then store them into a table. In order to find the
palindromic subsequences, the function extract out the certain length of short sequence then reverse complement it. If the reverse
complement of the short sequence match with the original short sequences, then  check the original short sequence either contain space or not
with certain pattern. If yes, the short sequences will store into the table with type 'SPACER',else the short sequences will store into the
table with type 'NORMAL'. The function will repeat until the all the palindromic subsequences found and store into the table

h)Print the table

i) Prompt user to select Y for run the program again or N to quit the program.
"""

import re
from prettytable import PrettyTable


def menu():
    print('==================================================')
    print('=            PALINDROMIC SEQUENCE PROGRAM        =')
    print('==================================================')
    print('Option1 - Raw sequences')
    print('Option2 - Fasta file format')
    print('Option3 - Genbank file format')


    user_choice = input('Option choose  :')  # Prompt user to choose the type of file
    print("--------------------------------------------------")
    if user_choice in ["1", "Option1"]:
        seq = input("Please enter your gene sequences with 'A','C','G','T' only \n").upper()# ask user to input file followed by capitalise the sequences
        return seq

    elif user_choice in ["2", "Option2"]:
        filename = input("Please input your FASTA file name:\n")  # ask user to input file
        return readFastaFile(filename)  # call readFASTAFile function to return sequence

    elif user_choice in ["3", "Option3"]:
        filename = input("Please input your GenBank file name:\n")  # ask user to input file
        return readGBFile(filename)  # call readBGFile function to return sequence

    else:  # any char except 1,2 and 3
        print('Invalid input')


def readFastaFile(filename):
    seq = ""
    fIn = open(filename)  # open file that input by the user
    lines = fIn.readlines()  # read lines from the input file and store in variable 'lines'
    for line in lines:  # in each line in variable lines
        if line.startswith('>'):  # if the line start with ">"
            pass  # no action will be taken
        else:  # if the line did not start with ">"
            line = re.sub('\n', '', line)  # substitue '\n' to nothing in that line
            seq += line  # concatenate the line into seq variable
    seq = seq.upper()  # set the sequence to upper case

    return seq  # return seq variable to the main program


def readGBFile(filename):
    seq = ""
    GB_file = open(filename, 'r')
    text = GB_file.read()  # read the input file and store in variable 'text'
    pattern = "\s+\d+\s+[a-z]{10}.+\s"  # set the pattern
    search_pattern = re.findall(pattern, text)  # stored all results that match the pattern into a list
    for i in search_pattern:  # in each line in variable search_pattern
        dna = re.sub('\s+', '', i)  # substitue any whitespace character to nothing in that line
        dna_1 = re.sub('\d+', '', dna)  # substitue any digit character to nothing in that line
        seq += dna_1
    seq = seq.upper()

    return seq


def reversecomp(seq):
    global compseq
    bases = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G', '_': '_'}  # define dictionary to store base pairs
    compseq = ""  # define empty string to store complement sequence
    for i in range(0, len(seq)):  # use for loop
        pair = seq[i]
        compseq = compseq + bases[pair]
    reverseCompseq = compseq[::-1]  # to reverse the compseq

    return reverseCompseq  # return variable reverseComp to the main program


def make_palin():
    table = PrettyTable()  # making table
    table.field_names = ["FROM", "TO", "PALINDROME", "TYPE"]  # set column names
    rc = reversecomp(seq)
    space_pattern = '_+'  # create pattern for spacer region with one or more '_'
    spacepair_pattern = '[ATGC]{3,}_+[ATGC]{3,}'  # create pattern for palindrome with spacer region with at least 3 base pair in front and back
    i = 0  # initialize i to 0 (i is the start of index of palindrome sequence to be print out later)
    for base in seq:  # for each base in the sequence
        short_seq = ""  # declare an empty string to store short sequence
        k = i  # initialize k to 0(in each for loop k will be redefine to be equal to i)
        while k < len(seq):  # while loop only run when k is smaller than length of sequence
            short_seq = short_seq + seq[k]  # concatenate base in seq to short_seq according to k(the index value)
            if len(short_seq) > 5:  # if the short_seq length is more than 5
                reverse_complement = reversecomp(
                    short_seq)  # call reversecomp function to compute reverse complement of the short_seq
                if reverse_complement == short_seq:  # if the short_seq is same as reverse complement computed
                    space = re.search(space_pattern, short_seq)  # search in short_seq the pattern of spacer region
                    if space:  # if spacer region exist in short_seq
                        PSpace = re.search(spacepair_pattern,
                                           short_seq)  # find if there are at least 3 base pair before and after the spacer region
                        if PSpace:  # if there are at least 3 base pair before and after the spacer region
                            table.add_row([i, k, short_seq,
                                           "SPACER"])  # print out index where the palindrome with spacer region found into table
                        else:
                            pass
                    else:  # if spacer region does not exist in short_seq
                        table.add_row(
                            [i, k, short_seq, "NORMAL"])  # print out index where the palindrome is found into table
                else:
                    pass
            else:
                pass
            k = k + 1  # increment of k by one when condition of while loop meet
        i = i + 1  # increment of i by one when condition of for loop meet
    print(table)


while True:  # use while loop

    # set empty variable 'seq'
    compseq = ""
    seq = menu()  # calling function menu()
    print("\nSequence                   : ", seq, "\n")  # print out the sequence from input file
    reverseCompseq = reversecomp(seq)  # call function reversecomp
    print("Complement Sequence        : ", compseq, "\n")  # print out the complementary sequence
    print("Reverse Complement Sequence: ", reverseCompseq, "\n")  # print out the reverse complementary sequence
    print("Sequence Length(include'_'): ", len(seq), " bp", "\n")  # print out the sequence length

    print("--------------------------------------------------")
    print("PALINDROMES")
    make_palin()
    print("")
    user_opt = input(
        "Enter Y to run the program again, otherwise enter N to quit the program\n")  # prompt user to choose whether run the program again or not
    if user_opt in ["y", "yes", "Y", "Yes", "YES"]:
        print("")
        pass  # while loop condtion = True
    elif user_opt in ["n", "no", "N", "No", "NO"]:
        print("\nThank you for using the program")
        print("Have a nice day ^-^")
        break  # while loop condtion = False and terminate the program
    else:  # any char except Y and N
        break  # while loop condtion = False and terminate the program



