"""
DNA Genetic Decryption Technique
"""
from time import time
import ast

import utils
from utils import *


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


def reshape(dna_sequence, reshape_info):
    """
    Generate chromosome population.
    :param dna_sequence: a string sequence of DNA bases
    :param reshape_info: the length of each chromosome
    :return: an array of chromosomes, chromosome population
    """

    chromosome_length = int(reshape_info[0])
    chromosomes = []

    # retrieve the population
    for i in range(0, len(dna_sequence), chromosome_length):
        chromosomes.append(dna_sequence[i:i + chromosome_length])

    return chromosomes


def reverse_reshape(population):
    # convert the chromosome population back to DNA sequence
    return "".join(population)


def rotate_crossover(population, rotate_info):
    """
    Rotate every chromosome in population left / right according to probability p.
    """

    new_population = []

    # get the rotation value
    rotation_offset = int(get_pattern(rotation_offset_del, rotate_info)[0])

    rotations = get_pattern(rotation_types_del, rotate_info)[0].split("|")[:-1]

    for i in range(len(population)):
        chromosome = population[i]

        direction = rotations[i]

        if direction == "left":
            right_first = chromosome[0: len(chromosome) - rotation_offset]
            right_second = chromosome[len(chromosome) - rotation_offset:]
            new_population.append(right_second + right_first)
        elif direction == "right":
            left_first = chromosome[0: rotation_offset]
            left_second = chromosome[rotation_offset:]
            new_population.append(left_second + left_first)

    return new_population


def single_point_crossover(population, single_point_info):
    """
    Combine each two chromosomes in population by using single point crossover.
    """
    crossover_points = [int(p) for p in single_point_info.split("|") if p != '']

    new_population = []
    for i in range(0, len(population) - 1, 2):
        candidate1 = population[i]
        candidate2 = population[i + 1]

        # get the crossover_point
        crossover_point = crossover_points[int(i / 2)]

        offspring1 = candidate2[0: crossover_point] + candidate1[crossover_point:]
        offspring2 = candidate1[0: crossover_point] + candidate2[crossover_point:]
        new_population.append(offspring1)
        new_population.append(offspring2)

    # append last chromosome if odd population size
    if len(population) % 2 == 1:
        new_population.append(population[len(population) - 1])

    return new_population


def crossover(population, crossover_info):
    # get the crossover type
    crossover_type = get_pattern(crossover_type_del, crossover_info)[0]

    if crossover_type == "rotate_crossover":
        rotate_info = get_pattern(rotate_crossover_del, crossover_info)[0]
        return rotate_crossover(population, rotate_info)
    elif crossover_type == "single_point_crossover":
        single_point_info = get_pattern(single_point_crossover_del, crossover_info)[0]
        return single_point_crossover(population, single_point_info)
    elif crossover_type == "both":
        rotate_info = get_pattern(rotate_crossover_del, crossover_info)[0]
        single_point_info = get_pattern(single_point_crossover_del, crossover_info)[0]
        population = single_point_crossover(population, single_point_info)
        return rotate_crossover(population, rotate_info)


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


def mutation(population, mutation_info):
    """
    Apply mutation operator by using "complement" and "alter_dna_bases"
    """

    # extract the alteration table
    alter_dna_table = ast.literal_eval(get_pattern(mutation_table_del, mutation_info[0])[0])

    chromosomes_info = get_pattern(chromosome_del, mutation_info[0])

    new_population = []
    for i in range(len(population)):
        chromosome = population[i]
        chromosome_info = chromosomes_info[i]

        # alter back the dna bases between point1 and point2
        alter_info = get_pattern(alter_mutation_del, chromosome_info)[0]
        point1, point2 = ast.literal_eval(alter_info)
        new_chromosome = ""
        for i in range(len(chromosome)):
            if i >= point1 and i <= point2:
                new_chromosome += alter_dna_table[chromosome[i]]
            else:
                new_chromosome += chromosome[i]

        two_bases_vector = group_bases(new_chromosome)

        # last base was not converted using four_bits_to_two_dna_base_table
        # convert it to bits using dna_base_to_two_bits_table
        last_two_bits = None
        if len(new_chromosome) % 2 == 1:
            last_two_bits = utils.dna_base_to_two_bits_table[new_chromosome[-1]]

            two_bases_vector = two_bases_vector[:-1]

        bits_seq = dna_to_bits(two_bases_vector, utils.two_dna_base_to_four_bits_table)

        if last_two_bits is not None:
            bits_seq += last_two_bits

        complement_info = get_pattern(complement_mutation_del, chromosome_info)[0]
        point1, point2 = ast.literal_eval(complement_info)
        b_chromosome = complement(bits_seq, point1, point2)
        b_chromosome = group_bits(b_chromosome)
        new_chromosome = bits_to_dna(b_chromosome, utils.two_bits_to_dna_base_table)

        new_population.append(new_chromosome)

    return new_population


def dna_gdt(text, key):
    print("\nDNA-GDT is running...\n")

    rounds_no = int(get_pattern(no_rounds_del, key)[0])
    rounds = get_pattern(round_del, key)

    b_data = text
    print("Initial DNA sequence:", b_data)

    # run the algorithm "rounds_no" times
    while rounds_no > 0:
        round_info = rounds[rounds_no - 1]

        # create the chromosome population
        b_data = reshape(b_data, get_pattern(reshape_del, round_info))
        # print("Population data:", b_data)

        # apply mutation on population
        b_data = mutation(b_data, get_pattern(mutation_del, round_info))
        # print("Population data:", b_data)

        # apply crossover on population
        b_data = crossover(b_data, round_info)
        # print("Population data:", b_data)

        # decrypt data with key after reshaping it back to binary sequence and then convert it back to dna sequence
        # where decrypt = encrypt(encrypt(data, key), key) and encrypt => xor operation, because (a xor b) xor b = a
        encryption_key = get_pattern(key_del, key)[0]
        b_data = bits_to_dna(
            group_bits(
                encrypt_key(dna_to_bits(reverse_reshape(b_data), utils.dna_base_to_two_bits_table), encryption_key)),
            utils.two_bits_to_dna_base_table)
        # print("Decrypted data:", b_data)

        rounds_no -= 1

    return bin2str(dna_to_bits(b_data, utils.dna_base_to_two_bits_table)).decode()


def main():
    original_file = open(original_filename, "r")
    encrypted_file = open(encrypted_filename, "r")
    decrypted_file = open(decrypted_filename, "w")
    key_file = open(key_filename, "r")

    original_text = original_file.read()
    encrypted_text = encrypted_file.read()
    key = key_file.read()

    print("Encrypted text:", encrypted_text)
    print("Key:", key)

    # generate the encoding tables
    generate_pre_processing_tables()
    generate_mutation_tables()

    # get the decrypted text
    start = time()
    decrypted_text = dna_gdt(encrypted_text, key)
    print("Decrypted text:", decrypted_text)
    decrypted_file.write(decrypted_text)
    end = time()

    print("\nTotal execution time:", end - start)

    if original_text != decrypted_text:
        print("\nDecryption failed.")
    else:
        print("\nDecryption succeeded.")

    original_file.close()
    encrypted_file.close()
    decrypted_file.close()
    key_file.close()


if __name__ == '__main__':
    main()
