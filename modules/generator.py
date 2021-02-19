from random import SystemRandom, sample
from ast import literal_eval
from os import path
from datetime import datetime
from json import dumps
from string import ascii_lowercase, ascii_uppercase, digits, punctuation

# Password Generator Class => I am aware that it is very simple, suggestions to make it more complex would be appreciated
# Or even if it does not need to be more complex, just tips that can make this code more efficient would be nice
class passwordGenerator():

    """ Test Doc """

    def __init__(self, length = int, options = list, save = bool): 
        # Is it possible to set the expected variable types?
        # So that length must be an integer, options must be a list and save must be a boolean, without __exceptionHandler()?
        self.length = length # Integer
        self.options = options # List of booleans [True, True, False, False] for lower & upper case letters, but not digits and punc.
        self.save = save # Boolean
        self.__exceptionHandler()

    def __str__(self):
        return self.__generate()

    def __generate(self):
        opts = self.__determineOptions()
        password = ''.join(SystemRandom().choice(opts) for i in range(self.length))
        self.__savePassword(password) # Saves generated password
        return password
    
    def __determineOptions(self):
        optionsSelected = ''

        # Input list should be input as [Lower, Upper, Digits, Punctuation]. Each value will be a boolean
        if self.options[0]:
            optionsSelected += ascii_lowercase
        if self.options[1]:
            optionsSelected += ascii_uppercase
        if self.options[2]:
            optionsSelected += digits
        if self.options[3]:
            optionsSelected += punctuation
            
        return optionsSelected

    # Honestly I added this because in future i want to make a password vault/storage app
    # But when I do that I'm obviously not going to use JSON and plaintext...
    # And I will not store the save function in this class
    def __savePassword(self, generatedPassword):
        if self.save:
            if path.exists('passwords.json') == False:
                temp_db = {}
                f = open("passwords.json", 'x+')
                f.write(dumps(temp_db))
                f.close()

            with open("passwords.json", "r") as file:    
                for line in file:
                    record = line

            temp_db = literal_eval(record)
            temp_db[f"{datetime.now().strftime('%d/%m/%Y')}, at {datetime.now().strftime('%H:%M:%S')}"] = generatedPassword
            
            f = open("passwords.json","w")
            f.write(dumps(temp_db))
            f.close()
        
        else:
            pass

    # Checks if inputted variables are the correct types
    def __exceptionHandler(self):
        if isinstance(self.length, int) == False:
            raise TypeError(f"Please input an integer, not a {type(self.length)}")
        else:
            if self.length < 8:
                self.length = 8

            elif self.length > 50:
                self.length = 50

        if isinstance(self.options, list):
            for item in self.options:
                if isinstance(item, bool) == False:
                    raise ValueError("Incorrect value input, must be either 'True' or 'False' ie a boolean.")

            if len(self.options) != 4:
                if len(self.options) > 4:
                    raise IndexError(f"List is too long, it must contain 4 boolean values, not {len(self.options)}!")
                else:
                    raise IndexError(f"List is too short, it must contain 4 boolean values, not {len(self.options)}!")
            
            if self.options.count(True) == 0:
                raise Exception("Please enter at least 1 'True' value!")

        else:
            raise TypeError(f"Please input a list, not a {type(self.options)}")

        if isinstance(self.save, bool) == False:
            raise TypeError(f"Please input a boolean value, ie True or False, not {type(self.save)}") 