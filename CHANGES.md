# Changes

## To do

 - [ ] Add Braille alphabet
 - [ ] Create iterator to consume string with variable length symbols (Morse)
 - [ ] Create parametric cleanser (can be disabled) to remove accents and uniformize special chars ('´)

 - [ ] Iterate all smallest rectangle able to contains text
 - [ ] Assess the needs to create ReversibleCypher class
 - [ ] Need a good and well designed toolbox for iterators, number theory (gcd, modinv)
 - [ ] Column and row shuffling
 - [ ] Pandas manipulations, reshape, squeeze
 - [ ] Create a factory for frequency mapping

## PySGRS v0.0.x

- [x] `v0.0.14`: **`2020-11-30`**: `add`: Added ASCII alphabet
  - [x] Prevent using non natural alphabet on cypher requiring it;
  - [x] Added toolbox: Shaper, ModularArithmetic, Frequency;
- [x] `v0.0.13`: **`2020-11-30`**: `add`: Added Pipeline cypher for cypher composition
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
- [x] `v0.0.9`: **`2020-11-29`**: `add`: Added Transposition cypher
- [x] `v0.0.8`: **`2020-11-28`**: `add`: Added Polybe alphabet
- [x] `v0.0.7`: **`2020-11-28`**: `add`: Added Substitution cyphers:
  - [x] Added Permutation cypher
  - [x] Added Affine cypher
- [x] `v0.0.6`: **`2020-11-28`**: `update`: Normalized Alphabet and StreamCypher: 
  - [x] Stream Cypher is now tolerant to illegal or lower case symbols;
  - [x] Alphabet are more friendly, added magic function for indexing and `in` operator;
  - [x] Refactored exceptions namespace.
- [x] `v0.0.5`: **`2020-11-27`**: `add`: Uniformization and update of Stream Cypher:
  - [x] Refactored namespace, added unit tests;
  - [x] Added Vigenere cypher;
  - [x] Added Substitution cyphers (Rotation, Caesar).
- [x] `v0.0.4`: **`2020-11-27`**: `update`: Starting package for SGRS support.
- [x] `v0.0.3`: **`2019-03-27`**: `add`: Initial release.
