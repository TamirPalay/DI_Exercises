import asyncio
from googletrans import Translator

async def main():
    # Use an async context manager for the Translator
    async with Translator() as translator:
        french_words= ["Bonjour", "Au revoir", "Bienvenue", "A bientôt"] 
        english_words= await translator.translate(french_words, src='fr', dest='en')
        frenchDict = {french: english.text for french, english in zip(french_words, english_words)}
        print(frenchDict)


asyncio.run(main())
