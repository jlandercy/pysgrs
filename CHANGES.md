# Changes

## To do

 - [ ] Add Bacon,
 - [ ] Add Braille
 - [ ] Add Morse
 - [ ] Improve test for symbols
 - [ ] Prevent using non natural alphabet on cypher requiring it
 - [ ] Create iterator to consume string with variable length symbols (Morse)
 - [ ] Create parametric cleanser (can be disabled) to remove accents and uniformize special chars ('´)
 - [ ] Add Transposition Cypher (matrix swam row/column)
 - [ ] Add Polybe Square alphabet
 - [ ] Frequentist analyst

## PySGRS v0.0.x

- [x] `v0.0.7`: **`2020-11-28`**: `add`: Added Substitution Cyphers:
  - [x] Added Permutation Cypher
  - [x] Added Affine Cypher
- [x] `v0.0.6`: **`2020-11-28`**: `update`: Normalized BaseAlphabet and Stream Cypher: 
  - [x] Stream Cypher is now tolerant to illegal symbols and lower case symbols;
  - [x] BaseAlphabet is simpler to use, added magic function for indexing and in operator;
  - [x] Refactored BaseAlphabet exceptions.
- [x] `v0.0.5`: **`2020-11-27`**: `add`: Uniformization and update of Stream Cypher:
  - [x] Refactored Namespace and unit tests;
  - [x] Added Vigenere Cypher Cypher;
  - [x] Added Substitution Cyphers (Rotation, Caesar).
- [x] `v0.0.4`: **`2020-11-27`**: `update`: Starting package for SGRS support.
- [x] `v0.0.3`: **`2019-03-27`**: `add`: Initial release.
