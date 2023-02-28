'''Creates a pseudo random string generator'''

import random

class Randomizer:

    def create_seed(self, phrase, salt=''):
        """Create random seeds that will later be combined
        for the randomization

            :param phrase: Password or main secret key to serve as seed
            :param salt: Additional string char to add to the generation of randomness
            :return: Integer seed that will prime the randomizer function
        """

        rand_upper_bound = 999
        subseed_collection = []
        final_seed = 0
        volatile_seed = 0

        for char in str(salt) + phrase:
            random.seed(ord(char) + volatile_seed)
            volatile_seed = random.randint(0, rand_upper_bound)
            subseed_collection.append(volatile_seed)

        for i in subseed_collection:
            final_seed += i

        return final_seed


    def create_random_str(self, phrase_seed, salt='', str_length=15):
        """
        Create a random string using the unicode characters, initial phrase is
        needed as seed

            :param phrase_seed: Password or main secret key to serve as seed
            :param salt: Additional string char to add to the generation of randomness
            :param str_length: Length of string to be generated
            :return: Phrase with random characters, with no spaces
        """
        seed = self.create_seed(phrase_seed, salt)
        random.seed(seed)
        ucode = [33, 126]
        random_string = ''

        for i in range(str_length):
            random_string += chr(random.randint(ucode[0], ucode[1]))

        return random_string

