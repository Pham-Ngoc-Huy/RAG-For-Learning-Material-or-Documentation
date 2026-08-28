# Embedder

Bring `chunks` to `vector` as output to compare the similarity by cosine equation

## 1. what is an embedding?

> You convert text into a vector - an array of floats that represents meaning in mathematical space.

```
"black holes warp spacetime"  →  [0.12, -0.83, 0.44, 0.91, ...]  (768 dims)
"gravity bends light"         →  [0.11, -0.79, 0.41, 0.88, ...]  (768 dims)
"my cat likes tuna"           →  [0.95,  0.23, -0.67, 0.02, ...]  (768 dims)
```

Similar meaning -> vectors point in similar directions -> high cosine similarity

This is how retrieval works -> use question gets embedded, then you find the chunks whose vectors are closest to it

## 2. How it works:
