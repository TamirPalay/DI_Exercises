import os
import random
import json
def get_words_from_file(file_path):
    with open(file_path, 'r') as file:
        words = file.read().split()
    return words
# __file__ is the current script's path
script_dir = os.path.dirname(__file__)
full_path = os.path.join(script_dir, 'words.txt')

def get_random_sentence(n):
    words= get_words_from_file(full_path)
    sentence=""
    for i in range(n):
        random_word = random.choice(words)
        sentence += random_word + " "
    return sentence.lower()

def __main__():
    print("This function generates a random sentence based on the number of words you specify.\nThe words are taken from a file called 'words.txt' located in the same directory as this script.")
    n = int(input("Enter the number of words in the sentence: "))
    if isinstance(n, int) and n>=2 and n<=20:
        random_sentence = get_random_sentence(n)
        print("Random Sentence:\n", random_sentence)
    else:
        print("The number of words must be a numeric value between 2 and 20.")
    
    ##Exercise 2

    sampleJson = """{ 
    "company":{ 
        "employee":{ 
            "name":"emma",
            "payable":{ 
                "salary":7000,
                "bonus":800
            }
        }
    }
    }"""
    data = json.loads(sampleJson)
    print("Salary:", data["company"]["employee"]["payable"]["salary"])
    data["company"]["employee"]["birth_date"] = "1992-07-15"

    with open("sample.json", 'w') as file_obj:
        json.dump(data, file_obj, indent=4)

    print(data)

if __name__ == "__main__":
    __main__()


        