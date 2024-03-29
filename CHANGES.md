# Changes

## To do

 - [ ] Add Braille alphabet
 - [ ] Assess the needs to create SubstitutionCypher class
 - [ ] Make Shape cyphers standards about shape selection and create an _apply method
 - [ ] Consider the need to create a Message object (CypherMessage and ClearMessage) holding necessary properties
   (as alphabet, shape, separators, specials chars, etc.) and helping to discriminate among forms (str, block, vector and matrix)
 - [ ] Challenge your library against previous SGRS quiz with answers
 - [ ] Properly document function as soon as you fixed the interface
 - [ ] Raise error or warning if parse cannot consume completely the string
 - [ ] Add Autokey Cypher (https://en.wikipedia.org/wiki/Autokey_cipher)
 - [ ] Add Chao Cypher (https://en.wikipedia.org/wiki/Chaocipher)
 - [ ] Add Hill Cypher (https://en.wikipedia.org/wiki/Hill_cipher)  
 - [ ] Add Code Breakers:
    - Documentations 
    - https://www.guballa.de/implementierung-eines-vigenere-solvers
    - https://gitlab.com/guballa/SubstitutionBreaker/-/tree/development/subbreaker
    - https://www.guballa.de/vigenere-solver
 - [ ] Make you library compliant with pycipher interface (https://github.com/jameslyons/pycipher)
 - [ ] Check out how it then breaks codes: https://github.com/jameslyons/python_cryptanalysis
 - [ ] Consider the option to create KeyCipher and move key to it in order to make RotationCipher keyless
 - [ ] Remove pandas dependency whenever possible, use it only for use output
 - [ ] Do make performance improvements as Breaker will need it
 - [ ] Replace by key, add initial and random perturb sample in Cypher to make LocalSearch more generic

## PySGRS v0.0.x

- [x] `v0.0.24`: **`2020-12-11`**: `add`: Created Hill Climbing Breaker for Permutation Cypher 
- [x] `v0.0.23`: **`2020-12-10`**: `update`: Starting TDD for Breakers 
- [x] `v0.0.22`: **`2020-12-09`**: `add`: Preparing background for cipher breaking
  - [x] Added Key Space GenericGenerator and Cipher GenericFactory;
  - [x] Added Generic Breaker as backbone for BruteForce, HillClimbing and Genetic;
  - [x] Added missing Gutenberg Project license in books directory.
- [x] `v0.0.21`: **`2020-12-08`**: `add+updated`: Added n-grams object for statistical crypto-analysis
  - [x] **Breaking change** Refactored complete namespace to modernize names to cipher instead of cypher
- [x] `v0.0.20`: **`2020-12-07`**: `add`: Added key size coincidence helper
- [x] `v0.0.19`: **`2020-12-06`**: `update`: Changed Alphabet O(1) indexer from dictionnary (requires Python3.7+) 
- [x] `v0.0.18`: **`2020-12-06`**: `add+update`: Updated Cyphers model and added Cypher
  - [x] Refactored Cypher model to make distinction between Functional, Stream, Alphabet and IntegerAlphabet cyphers;
  - [x] Added non constrained Alphabet encipher (making Alphabet encode/decode mapped to encipher/decipher);
- [x] `v0.0.17`: **`2020-12-06`**: `add`: Added new tools for Crypto Analysis:
  - [x] Created cleanser for accents, punctuation and special chars, added tests;
  - [x] Create Frequency Analyser, added public domain french books.
- [x] `v0.0.16`: **`2020-12-05`**: `add`: Added parser for Morse and Bacon Cyphers without separator
  - [x] Created iterator to consume string with variable length symbols;
- [x] `v0.0.15`: **`2020-12-02`**: `update`: Refactored Shape encipher to include more cyphers
- [x] `v0.0.14`: **`2020-11-30`**: `add`: Added ASCII alphabet
  - [x] Prevent using non natural alphabet on encipher requiring it;
  - [x] Added toolbox: Shaper, ModularArithmetic, Frequency;
- [x] `v0.0.13`: **`2020-11-30`**: `add`: Added Pipeline encipher for encipher composition
- [x] `v0.0.12`: **`2020-11-30`**: `updated`: Added Alphabet index types
  - [x] Distinction among alphabet index type is made by inheritance;
  - [x] Added `is_monotonic` function for indices;
  - [x] Added properties to check index symbols for string based index alphabet;
  - [x] Added new unit tests for alphabet;
- [x] `v0.0.11`: **`2020-11-30`**: `add`: Added Base Cyphers:
  - [x] Added Base16, Base32, Base64 and Base85 Cyphers;
  - [x] Added URLQuote Cypher;
  - [x] Refactored Cypher namespace and inheritance;
- [x] `v0.0.10`: **`2020-11-30`**: `add+update`: Refactored Alphabet:
  - [x] Added Morse and Bacon alphabets;
  - [x] Added Alphabet unit tests;
  - [x] Updated Alphabet index (mixed index types allowed);
- [x] `v0.0.9`: **`2020-11-29`**: `add`: Added Transposition encipher
- [x] `v0.0.8`: **`2020-11-28`**: `add`: Added Polybe alphabet
- [x] `v0.0.7`: **`2020-11-28`**: `add`: Added Substitution cyphers:
  - [x] Added Permutation encipher
  - [x] Added Affine encipher
- [x] `v0.0.6`: **`2020-11-28`**: `update`: Normalized Alphabet and StreamCypher: 
  - [x] Stream Cypher is now tolerant to illegal or lower case symbols;
  - [x] Alphabet are more friendly, added magic function for indexing and `in` operator;
  - [x] Refactored exceptions namespace.
- [x] `v0.0.5`: **`2020-11-27`**: `add`: Uniformization and update of Stream Cypher:
  - [x] Refactored namespace, added unit tests;
  - [x] Added Vigenere encipher;
  - [x] Added Substitution cyphers (Rotation, Caesar).
- [x] `v0.0.4`: **`2020-11-27`**: `update`: Starting package for SGRS support.
- [x] `v0.0.3`: **`2019-03-27`**: `add`: Initial release.
