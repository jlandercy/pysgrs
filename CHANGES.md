# Changes

## To do

 - [ ] Add Braille alphabet
 - [ ] Prevent using non natural alphabet on cypher requiring it
 - [ ] Create iterator to consume string with variable length symbols (Morse)
 - [ ] Create parametric cleanser (can be disabled) to remove accents and uniformize special chars ('´)
 - [ ] Frequentist analyst

## PySGRS v0.0.x

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
