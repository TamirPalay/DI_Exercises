'''This challenge is about Biology that will put emphasis on your knowledge of classes, inheritance and polymorphism.

Build a DNA object. DNA is composed of chromosomes which is itself composed of Genes.
A Gene is a single value 0 or 1, it can mutate (flip).
A Chromosome is a series of 10 Genes. It also can mutate, meaning a random number of genes can randomly flip (1/2 chance to flip).
A DNA is a series of 10 chromosomes, and it can also mutate the same way Chromosomes can mutate.

Implement these classes as you see fit.

Create a new class called Organism that accepts a DNA object and an environment parameter that sets the probability for its DNA to mutate.

Instantiate a number of Organism and let them mutate until one gets to a DNA which is only made of 1s. Then stop and record the number of generations (iterations) it took.'''
import random


class DNA:
    def __init__(self, chromosomes):
        if len(chromosomes) != 10:
            raise ValueError("A DNA must have exactly 10 chromosomes.")
        self.chromosomes = chromosomes
    
    def mutate(self, mutation_probability):
        for chromosome in self.chromosomes:
            if random.random() < mutation_probability:
                chromosome.mutate()
    
    def print_dna(self):
        for i, chromosome in enumerate(self.chromosomes):
            gene_values = [gene.value for gene in chromosome.genes]
            print(f"  Chromosome {i + 1}: {gene_values}")

class Gene:
    def __init__(self, value):
        if value not in (0, 1):
            raise ValueError("Gene value must be 0 or 1.")
        self.value = value
    def mutate(self):
        self.value = 1 - self.value  # Flip between 0 and 1

class Chromosome:
    def __init__(self, genes):
        if len(genes) != 10:
            raise ValueError("A chromosome must have exactly 10 genes.")
        self.genes = genes
    def mutate(self):
        for gene in self.genes:
            if random.random() < 0.5:  
                gene.mutate()

class Organism:
    def __init__(self, dna, environment_mutation_probability):
        self.dna = dna
        self.environment_mutation_probability = environment_mutation_probability
    def mutate(self):
        self.dna.mutate(self.environment_mutation_probability)

#Test the implementation
def main():
    # Create a DNA with only 2 zeros (guaranteed quick convergence)
    chromosomes = []
    zero_count = 0
    for i in range(10):
        genes = []
        for j in range(10):
            if zero_count < 2:
                genes.append(Gene(0))
                zero_count += 1
            else:
                genes.append(Gene(1))
        chromosomes.append(Chromosome(genes))
    dna = DNA(chromosomes)
    print("Initial DNA:")
    dna.print_dna()
    
    # Create an organism with HIGH mutation probability (1.0 = always mutate)
    organism = Organism(dna, environment_mutation_probability=1.0)
    print("\nOrganism created with mutation probability of 1.0.\n")
    generations = 0
    
    while True:
        organism.mutate()
        generations += 1
        print(f"Generation {generations}:")

        
        if all(gene.value == 1 for chromosome in organism.dna.chromosomes for gene in chromosome.genes):
            print(f"\nOrganism reached optimal DNA in {generations} generations.")
            break

if __name__ == "__main__":
    main()
