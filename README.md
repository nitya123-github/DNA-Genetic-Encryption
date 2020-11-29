# DNA GENETIC ENCRYPTION 
<h3> COMPLETED A RESEARCH PAPER AND ATTACHED IT IN FOLDER AS "DNA-FINAL DOC" </h3>
In this project we implement a DNA-Genetic Encryption Technique (D-GET) in order to make the DNA SEQUENCE more secure and less predictable.

<h3> TOOLS USED: </h3>

PYTHON

<h3> MODULES: </h3>

Pre processing,
Encryption,
Re shaping,
Cross over,
Mutation,

<h3>ABSTRACT: </h3>

In this technique,we take binaries of any type of digital data and convert it to DNA sequencing, reshape, encrypt, crossover, mutate and then reshape. The main stages of D-GET are repeated three times or more. Transmit the encrypted data in text/image format file. In other side, the receiver uses the D-GET to decrypt the received data and reshape it to original format. This Technique  multiple key sequences to increase the degree of diffusion and confusion, which makes resulting cipher data difficult to decipher and makes to realize a perfect secrecy system. Experimental results demonstrate that proposed technique has multilayer protection stages against different attacks and higher level of security based on the multi-stages and genetic operations. And a symentric key cryptography is implemented in this project.And also a random key will be generated.Decrypted data are acceptable because of there is absolutely difference between it and secret data. 

<h3> ARCHITECTURE DIAGRAM: </h3>
 
 ![dna](https://user-images.githubusercontent.com/53599318/99866986-d4071c00-2bdb-11eb-9a57-fbf35ead9adf.jpg)

<h3> STAGES: </h3>

<h3>Pre-processing Stage:</h3>  

After reading secret data, this data must be preparing depending into its type. In case text file, it is converted into ASCII values. Group them into 8-bits Binary data. Every two adjacent bits are transferred to the four bases; adenine (A), cytosine (C), guanine (G) and thymine (T), found in DNA

<h3>Encryption stage: </h3>

After conversion binary data to DNA sequencing then encrypt using key. The key may be DNA sequence or binary string. The key has variable length. If one or both of data and DNA sequence key DNA sequence, it will convert to binary form then, perform an exclusive OR operation on the corresponding elements of them and convert back to DNA sequence. 

<h3>Reshaping Stage: </h3>

After Encryption, A basic genetic algorithm is 
composed of three operators; reproduction, crossover and mutation. To produce genetic material that pass to the next operation and iteration in the form of chromosome population, the Reshaping stage is used. In this stage, first number and length of chromosome are determined. These values may be constant are varied for every round. Reshape it by align the DNA sequence into rows to construct parents’ chromosomes (chromosome population) with pre-defined length.

<h3>Crossover Stage:</h3>

After constructing parents’ chromosomes, the next operation is crossover. There are two types of crossover. These may be sequentially used in technique rounds. In the first one, the parents are selected in the mating pool. A single-point crossover point is selected between the first and last bits of the parents’ chromosomes then, creating two new offspring by exchanging the heads of parent1 and parent2. Consequently the offspring containportions of the DNA codes of both parents

<h3>Mutation Stage:</h3>

After crossover process, the chromosomes are 
subjected to mutation. Mutation is the alteration of string elements. Two types of mutation are used. In the first one, convert data to binary vector and define two mutation points between the first and last bits then complement bits in between i.e. single point mutation changes a 1 to a 0, and vice versa. In the second mutation type, convert each four bits to two bases of DNA (1010 -> CG). After conversion, reshape it to DNA bases vector and define two points between the first and last bases then alter DNA bases to another one (i.e., C -> G). 

INPUT: A normal text 

OUTPUT:  Encryption and decryption of data using DNA-Genetic Encryption Technique  

<h3> EVALUATION RESULTS: </h3>

The D-GET is implemented in the AMD Athlon(tm) II X2 220 Processor, 2.80GHz and 4 GB RAM on Windows 8.1 64-BIT operating system. We conduct experiments to test the efficacy of the proposed technique and run it with various types of secret data. 
Using all manner of cryptanalytic, mathematical and brute-force attacks,  cryptanalysts attack any encrypted data to discover its contents. A successful encryption technique against them should be robust. So, there are some features that need to be achieved. Here There is no relationship between, before encryption, sensitive data values and, after encryption, encrypted data values. Encryption should be blended around the various hidden data components so that nothing in its original position is presented. 

![dna2](https://user-images.githubusercontent.com/53599318/99867007-f6993500-2bdb-11eb-96f6-4fbc7a878cf5.jpg)

<h3> CONCLUSIONS: </h3>

D-GET is implemented in this project. The D-GET, based on multi-iteration and genetic activities, is a more stable encryption technique. Operations, encryption, rotation, crossover, mutation, and reshapes that improve the standard of encryption are also included. D-GET operations and modifications to the original data size and format. In addition, the negligible relationship in both the hidden data and its encrypted data decreases the possibilities of cryptanalysis and breaking the cypher. In addition, the technique has multilayer defence phases that achieve confidentiality and provide data with more security, productivity and robustness and protects against detection. We would standardise D-GET in future work and try to minimise transmission

