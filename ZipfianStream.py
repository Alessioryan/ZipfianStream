
import random as rand
from scipy.stats import poisson

# Define the phonemes
default_natural_classes = {
    "C": ['p', 'b', 't', 'd', 'k', 'g', 'f', 'v', 'θ', 'ð', 's', 'z', 'ʃ', 'ʒ', 'h', 'm', 'n', 'ŋ', 'l', 'ɹ', 'j', 'w', 'ɲ', 'q' ,'x', 'ʈ', 'ʁ', 'ɣ', 'θ'],
    "V": ['ʌ', 'æ', 'ɑ', 'ɒ', 'ɔ', 'ə', 'ɛ', 'ɪ', 'i', 'ɨ', 'ʊ', 'u', 'y'],
    "T": ['p', 'b', 't', 'd', 'k', 'g', 'q', 'ʈ'],
    "F": ['f', 'v', 'θ', 'ð', 's', 'z', 'ʃ', 'ʒ', 'h', 'x', 'ɣ', 'θ'],
    "N": ['m', 'n', 'ŋ', 'ɲ'],
    "J": ['l', 'ɹ', 'j', 'w', 'ʁ'],
    "O": ['p', 'b', 't', 'd', 'k', 'g', 'q', 'f', 'v', 'θ', 'ð', 's', 'z', 'ʃ', 'ʒ', 'h', 'x', 'ʈ', 'ɣ', 'θ']
}

# Define a default inventory
default_inventory = [val for sublist in default_natural_classes.values() for val in sublist]

# Zipfian Choice
def zipfian_choice(natural_class):
    total_weight = 0
    for i in range(len(natural_class)):
        total_weight += 1 / (i+1)
    rand_weight = rand.uniform(0, total_weight)
    weight_sum = 0
    for i in range(len(natural_class)):
        weight_sum += 1 / (i+1)
        if weight_sum >= rand_weight:
            return natural_class[i]


# The main class
class ZipfianStream:

    # Constructor
    # Syllable structure must be correctly defined
    def __init__(self, inventory=default_inventory, ordered=False, syllable_structure="CV(C)", natural_classes=default_natural_classes, average_syllables_per_word=2.0, optional_component_probability=0.5):
        # Set up the inventory
        self.inventory = inventory
        if not ordered:
            rand.shuffle(self.inventory)

        # Set up the syllable structure
        self.syllable = [] # List of (natural class, is required)
        required = True
        for char in syllable_structure:
            if char == '(':
                required = False
            elif char == ')':
                required = True
            else:
                self.syllable.append((char, required))

        # Natural classes
        self.natural_classes = natural_classes

        # The average number of words per syllable
        self.average_syllables_per_word = average_syllables_per_word

        # The probability of optional components showing up
        self.optional_component_probability = optional_component_probability


    # Generate a random letter Zipfianly given a natural class (represented as a letter)
    # The Zipfian distribution is based only on the relevant phonemes
    def make_letter(self, natural_class_letter):
        natural_class = self.natural_classes[natural_class_letter]
        relevant_phonemes = [phoneme for phoneme in self.inventory if phoneme in natural_class]
        return zipfian_choice(relevant_phonemes)

    # Create a syllable
    def make_syllable(self):
        syllable = ""
        for component in self.syllable:
            if not component[1] and rand.random() > self.optional_component_probability: # If is not required and skipped with prob 50%
                continue
            syllable += self.make_letter(component[0])
        return syllable

    # Make a word of random length described by Poisson(1) + 1
    def make_word(self):
        distribution = poisson(mu=(self.average_syllables_per_word - 1) )
        num_syllables = distribution.rvs(1) + 1
        word = ""
        for _ in range(num_syllables[0]):
            word += self.make_syllable()
        return word

    # Makes n words of a given length
    def make_sentence(self, length):
        return " ".join([self.make_word() for _ in range(length)])

    # Make paragraph of n sentences
    def make_paragraph(self, num_sentences, sentence_length):
        return "\n".join([self.make_sentence(sentence_length) for _ in range(num_sentences)])



# Main method
def main():
    print(That_one_tiktoker_stream.make_paragraph(10, 10) )
    print(That_one_tiktoker_stream.inventory)

# Friends
Ella_stream = ZipfianStream(inventory=['p', 'm', 'v', 't', 'n', 's', 'ɹ', 'l', 'ʃ', 'ʒ', 'ʈ', 'k', 'ɲ', 'x', 'ŋ', 'q', 'i', 'y', 'ɛ', 'æ', 'ə', 'u', 'ɔ', 'ɑ'],
                            syllable_structure="C(J)V(J)(N)(O)",
                            average_syllables_per_word=1.2,
                            optional_component_probability=0.2)

That_one_tiktoker_stream = ZipfianStream(inventory=['x', 'ɣ', 'q', 'ʁ', 'p', 'n', 'ŋ', 't', 'k', 'l', 'θ', 'g', 'i', 'y', 'u', 'ɑ', 'ə'],
                                         ordered=True,
                                         syllable_structure="C(J)V(C)",
                                         average_syllables_per_word=2,
                                         optional_component_probability=0.1)

if __name__ == '__main__':
    main()
