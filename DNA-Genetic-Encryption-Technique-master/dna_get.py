"""
DNA Genetic Encryption Technique
"""
import string
from time import time

import utils
from utils import *

# number of rounds the algorithm is run, chosen randomly
rounds_no = None

chromosome_length = None

# the key used in the decryption process
decryption_key = None


def set_globals():
    global rounds_no
    global decryption_key
    # it is better to be odd random
    rounds_no = random.randrange(3, 12, 2)
    decryption_key = ""


def encrypt_key(data, key):
    """
    Encrypt data with key: data XOR key.
    """

    # repeat key ONLY if data is longer than key and encrypt
    if len(data) > len(key):
        factor = int(len(data) / len(key))
        key += key * factor

        return bitxor(data, key)

    return bitxor(data, key)


def reshape(dna_sequence):
    """
    Generate chromosome population.
    :param dna_sequence: a string sequence of DNA bases
    :return: an array of chromosomes, chromosome population
    """
    global chromosome_length
    global decryption_key

    # choose population size and chromosome length
    divs = divisors(len(dna_sequence))
    chromosome_no = divs[random.randint(0, len(divs) - 1)]
    chromosome_length = int(len(dna_sequence) / chromosome_no)
    chromosomes = []

    decryption_key += reshape_del + str(chromosome_length) + reshape_del

    # retrieve the population
    for i in range(0, len(dna_sequence), chromosome_length):
        chromosomes.append(dna_sequence[i:i + chromosome_length])

    return chromosomes


def reverse_reshape(population):
    # convert the chromosome population back to DNA sequence
    return "".join(population)


def rotate_crossover(population):
    """
    Rotate every chromosome in population left / right according to probability p.
    """
    global chromosome_length
    global decryption_key

    new_population = []

    decryption_key += rotate_crossover_del

    # predefined rotation value, varied every round
    rotation_offset = random.randint(1, chromosome_length)

    decryption_key += rotation_offset_del + str(rotation_offset) + rotation_offset_del

    decryption_key += rotation_types_del

    for chromosome in population:

        p = random.uniform(0, 1)

        if p > 0.5:
            decryption_key += "right|"
            right_first = chromosome[0: len(chromosome) - rotation_offset]
            right_second = chromosome[len(chromosome) - rotation_offset:]
            new_population.append(right_second + right_first)
        else:
            decryption_key += "left|"
            left_first = chromosome[0: rotation_offset]
            left_second = chromosome[rotation_offset:]
            new_population.append(left_second + left_first)

    decryption_key += rotation_types_del

    decryption_key += rotate_crossover_del

    return new_population


def single_point_crossover(population):
    """
    Combine each two chromosomes in population by using single point crossover.
    """
    global decryption_key

    decryption_key += single_point_crossover_del

    new_population = []
    for i in range(0, len(population) - 1, 2):
        candidate1 = population[i]
        candidate2 = population[i + 1]

        # chromosomes have the same length
        # choose a random point
        length = len(candidate1)
        crossover_point = random.randint(0, length - 1)

        decryption_key += str(crossover_point) + "|"

        offspring1 = candidate2[0: crossover_point] + candidate1[crossover_point:]
        offspring2 = candidate1[0: crossover_point] + candidate2[crossover_point:]
        new_population.append(offspring1)
        new_population.append(offspring2)

    # append last chromosome if odd population size
    if len(population) % 2 == 1:
        new_population.append(population[len(population) - 1])

    decryption_key += single_point_crossover_del

    return new_population


def crossover(population):
    global decryption_key

    # choose crossover type according to p
    p = random.uniform(0, 1)

    if p < 0.33:
        decryption_key += crossover_type_del + "rotate_crossover" + crossover_type_del
        return rotate_crossover(population)
    elif p >= 0.33 and p < 0.66:
        decryption_key += crossover_type_del + "single_point_crossover" + crossover_type_del
        return single_point_crossover(population)
    else:
        decryption_key += crossover_type_del + "both" + crossover_type_del
        population = rotate_crossover(population)
        return single_point_crossover(population)


def complement(chromosome, point1, point2):
    """
    Flip chromosome bits between point1 and point2.
    """
    new_chromosome = ""

    for i in range(len(chromosome)):
        if i >= point1 and i <= point2:
            if chromosome[i] == '0':
                new_chromosome += '1'
            else:
                new_chromosome += '0'
        else:
            new_chromosome += chromosome[i]

    return new_chromosome


def alter_dna_bases(bases):
    """
    Alter DNA bases to another one randomly.(e.g. C->G and A->T and viceversa)
    """
    alter_dna_table = {}

    for _ in range(2):
        # choose one randomly then remove it from list
        base1 = bases[random.randint(0, len(bases) - 1)]
        bases.remove(base1)

        # choose one randomly then remove it from list
        base2 = bases[random.randint(0, len(bases) - 1)]
        bases.remove(base2)

        # assign the first to the other
        alter_dna_table[base1] = base2
        alter_dna_table[base2] = base1

    return alter_dna_table


def mutation(population):
    """
    Apply mutation operator by using "complement" and "alter_dna_bases"
    """
    global decryption_key

    bases = ['A', 'C', 'G', 'T']
    alter_dna_table = alter_dna_bases(bases)

    decryption_key += mutation_table_del + str(alter_dna_table) + mutation_table_del

    new_population = []
    for chromosome in population:
        decryption_key += chromosome_del

        # apply the complement
        b_chromosome = dna_to_bits(chromosome, utils.dna_base_to_two_bits_table)
        decryption_key += complement_mutation_del
        point1 = random.randint(0, len(b_chromosome) - 1)
        point2 = random.randint(point1, len(b_chromosome) - 1)
        decryption_key += "(%s, %s)" % (point1, point2)
        decryption_key += complement_mutation_del
        b_chromosome = complement(b_chromosome, point1, point2)

        # convert each 4 bits in chromosome to two dna bases using four_bits_to_two_dna_base_table
        four_bits_vector = group_bits(b_chromosome, 4)

        last_dna_base = None
        # if the last element is of length 2, don't convert it
        if len(four_bits_vector[len(four_bits_vector) - 1]) == 2:
            last_dna_base = utils.two_bits_to_dna_base_table[four_bits_vector[len(four_bits_vector) - 1]]

            # convert only the 4 bits elements
            four_bits_vector = four_bits_vector[:-1]

        dna_seq = bits_to_dna(four_bits_vector, utils.four_bits_to_two_dna_base_table)
        if last_dna_base is not None:
            dna_seq += last_dna_base

        # and then alter the dna bases between point1 and point2
        decryption_key += alter_mutation_del
        point1 = random.randint(0, len(dna_seq) - 1)
        point2 = random.randint(point1, len(dna_seq) - 1)
        decryption_key += "(%s, %s)" % (point1, point2)
        decryption_key += alter_mutation_del
        new_chromosome = ""
        for i in range(len(dna_seq)):
            if i >= point1 and i <= point2:
                new_chromosome += alter_dna_table[dna_seq[i]]
            else:
                new_chromosome += dna_seq[i]

        new_population.append(new_chromosome)

        decryption_key += chromosome_del

    return new_population


def dna_get(text, key):
    global rounds_no
    global decryption_key

    print("\nDNA-GET is running...\n")

    # binarize data and convert it to dna sequence
    b_data1 = binarized_data(text)
    dna_seq = bits_to_dna(b_data1, utils.two_bits_to_dna_base_table)
    # print(dna_seq)

    # there is no need for first reshape like in the pseudocode because my reverse_reshape can work on dna_seq, too
    # i.e. ("".join("ACGT") -> "ACGT")

    b_data2 = dna_seq
    print("Initial DNA sequence:", dna_seq)

    decryption_key += no_rounds_del + str(rounds_no) + no_rounds_del

    # run the algorithm "rounds_no" times
    while rounds_no > 0:
        decryption_key += round_del

        # encrypt data with key after reshaping it back to binary sequence and then convert it back to dna sequence
        b_data2 = bits_to_dna(
            group_bits(encrypt_key(dna_to_bits(reverse_reshape(b_data2), utils.dna_base_to_two_bits_table), key)),
            utils.two_bits_to_dna_base_table)
        # print("Encrypted data:", b_data2)

        # create the chromosome population
        b_data2 = reshape(b_data2)
        # print("Population data:", b_data2)

        # apply crossover on population
        decryption_key += crossover_del
        b_data2 = crossover(b_data2)
        decryption_key += crossover_del
        # print("Population data:", b_data2)

        # apply mutation on population
        decryption_key += mutation_del
        b_data2 = mutation(b_data2)
        decryption_key += mutation_del
        # print("Population data:", b_data2)

        rounds_no -= 1

        decryption_key += round_del

    return reverse_reshape(b_data2)


def main():
    global decryption_key

    original_file = open(original_filename, "w")

    text = "In computer science and operations research, a genetic algorithm (GA) is a metaheuristic inspired by the " \
           "process of natural selection that belongs to the larger class of evolutionary algorithms (EA)."

    # used for evaluate performance to generate random text of any length
    # text = ''.join(
    #    random.SystemRandom().choice(string.ascii_letters + string.digits + string.punctuation + string.whitespace) for
    #    _ in range(5000))

    print("Text:", text)

    original_file.write(text)

    # generate random key(it can have any length, could be the length of the plaintext)
    # in this case, I used 128 bit key
    key = str2bin(''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(16)))

    print("Key:", len(key), key)

    # set initial values of global variables
    set_globals()

    # append the key first
    decryption_key += key_del + key + key_del

    # generate the encoding tables
    generate_pre_processing_tables()
    generate_mutation_tables()

    # get the ciphertext
    start = time()
    encrypted_text = dna_get(text, key)
    print("Final DNA sequence:", encrypted_text)
    end = time()

    print("\nTotal execution time:", end - start)

    key_file = open(key_filename, "w")
    encrypted_file = open(encrypted_filename, "w")

    # save the encryption to a file to be used in the decryption process
    encrypted_file.write(encrypted_text)

    # save key to a file to be read in the decryption process
    key_file.write(decryption_key)

    encrypted_file.close()
    original_file.close()
    key_file.close()


if __name__ == '__main__':
    main()
