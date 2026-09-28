# The Task

| Laukas | Reikšmė |
|---|---|
| Užd. nr. | A11 |
| Kūnas | q=2 |
| Kodas | Tiesinis kodas C(n,k) |
| Dekodavimo algoritmas | grandininis (step-by-step) dekodavimas (p. 79) |
| Kodo parametrai | kodo ilgis n, dimensija k, generuojanti matrica G |
| Literatūra | [VO89, §3.7, p. 78–81; ir p. 73] |
| Pastabos | 4, 7, 11 |

### Pastabos

4. Jei vartotojas pageidauja, jis turi turėti galimybę suvesti generuojančią matricą pats. Jei vartotojas to nepageidauja, programa turi sugeneruoti atsitiktinę generuojančią matricą, atitinkančią vartotojo nurodytus kitus parametrus. Tai reiškia, kad programa turi realizuoti abu generuojančios matricos sudarymo būdus - ir matricos suvedimo, ir matricos atsitiktinio generavimo, - ir turi leisti pačiam vartotojui pasirinkti jam labiausiai tinkantį būdą.

7. Apie tiesinius kodus plačiau galite pasiskaityti mano konspektuose arba [Sta02, §1.1 ir §2.1-2.2] (arba [Sta96, §3.2, §4.1, §5.1-5.3]).

11. Užtenka, kad programa veiktų su standartinio pavidalo generuojančia matrica.

*source: https://emokymai.vu.lt/mod/page/view.php?id=54837*

---

# The plan

## The big idea first

Grading, roughly:

| Part | Points |
|---|---|
| Finite field (for me just bits mod 2) | 20% |
| Encoding | 20% |
| Channel | 10% |
| **Decoding (step-by-step)** | **50%** |
| Report | 10% |
| Code quality, comments | 10% |
| Scenarios 1, 2, 3 | 10% each |

So: **decoding is half the grade.** The teacher's own advice is to first get one vector working
(encode -> channel -> decode). That alone is worth ~80%. Text and images come after, only if there's time.

And it has to be **exactly** the step-by-step algorithm from [VO89], not some other decoder.

---

## Step 0 - Read and understand (before any code)

- [ ] Read [VO89] p. 73 - cosets, coset leaders, syndromes, the standard array.
- [ ] Read [VO89] §3.7, p. 78–81 - step-by-step decoding itself.
- [ ] Do one small example by hand on paper (e.g. a `[6, 3]` or `[7, 4]` code), so I know what the right answer looks like. I'll reuse it as a test later.
- [ ] Pick a language and GUI/console setup.

Things to be sure I understand:
- What a syndrome is: `s = H * r^T`.
- What a coset leader is: the lowest-weight vector in a coset.
- Why the decoder only needs the **weight** of the coset leader for each syndrome, not the leader itself.

---

## Step 1 - Bits and matrices (the "finite field" part)

Since `q = 2`, the field is just `{0, 1}` with:
- addition = XOR (`1 + 1 = 0`)
- multiplication = AND

To do:
- [ ] Vector operations: add two vectors, weight of a vector (count of 1s).
- [ ] Matrix operations: vector × matrix, matrix × vector, transpose.
- [ ] Unit tests for these - everything else depends on them.

---

## Step 2 - The code: generator matrix G and parity-check matrix H

Note 11 says standard form is enough: `G = [I_k | A]` (size `k × n`).

- [ ] Let the user enter `n` and `k` (check `0 < k < n`).
- [ ] **Option A:** user types `G` in by hand. Check it's `k × n`, only 0/1, and starts with the identity `I_k`.
- [ ] **Option B:** program generates a random `G`: identity `I_k` + random bits in `A`. (Note 4 - both options are required and the user picks one.)
- [ ] Build `H = [A^T | I_(n-k)]` (size `(n-k) × n`). For binary codes `-A^T = A^T`.
- [ ] Sanity check: `G * H^T` must be the all-zero matrix.

---

## Step 3 - Encoding

- [ ] Codeword `c = m * G`, where `m` is a message of length `k`.
- [ ] Because G is in standard form, the first `k` bits of `c` are just `m`. Easy to check.

---

## Step 4 - The channel

Binary symmetric channel with error probability `pe` (`0 <= pe <= 1`, precision at least 0.0001).

- [ ] For every bit: draw a random number `a` from `[0, 1]`. If `a < pe`, flip the bit.
- [ ] Return the received vector **and** the list of positions that got flipped (scenario 1 needs to show that).
- [ ] Create the random generator **once** when the program starts, not every time a vector is sent. Otherwise errors come in identical chunks and the channel isn't really random.

---

## Step 5 - Step-by-step decoding (the most important part)

### 5a. Build the syndrome -> coset leader weight table (done once per code)

There are `2^(n-k)` possible syndromes. For each one I need the weight of its coset leader.

Simple way to fill it:
- [ ] Start with the zero vector: syndrome `0` -> weight `0`.
- [ ] Go through all error vectors of weight 1, then weight 2, then 3, ...
- [ ] For each one compute its syndrome. If that syndrome isn't in the table yet, store it with the current weight.
- [ ] Stop when all `2^(n-k)` syndromes have a weight.

(Since we go by increasing weight, the first vector we hit for each syndrome is automatically a coset leader.)

### 5b. Decode one received vector `r`

```
for i = 1 .. n:
    s = syndrome(r)
    if s == 0: stop, r is a codeword
    w = weight_table[s]
    flip bit i of r
    if weight_table[syndrome(r)] < w:
        keep the flip
    else:
        flip it back
```

Then the decoded message = first `k` bits of `r`.

- [ ] Implement the table.
- [ ] Implement the loop.
- [ ] Double-check against the book that this matches [VO89] p. 79 exactly (order of positions, stopping condition).
- [ ] Test with the hand-done example from Step 0.
- [ ] Test: 0 errors -> nothing changes. Errors within what the code can fix -> fixed. Too many errors -> may decode wrong (that's expected, not a bug).

---

## Step 6 - Scenario 1: a single vector (do this before text/images!)

The user:
- [ ] types a message of length `k` (program checks the length and that it's only 0/1),
- [ ] sees the encoded vector,
- [ ] sees what came out of the channel + how many errors and at which positions,
- [ ] **can edit** the received vector by hand before decoding (to test specific error patterns),
- [ ] sees the decoded result.

**Checkpoint:** if this works correctly, the most valuable part (~80%) is done. Commit, back up.

---

## Step 7 - Scenario 2: text

- [ ] User types text (multiple lines allowed).
- [ ] Turn text into bytes -> bits -> split into chunks of length `k`.
- [ ] The last chunk may be too short - pad it with zeros. How many zeros were added is "service info": keep it aside, don't send it through the channel.
- [ ] **Without code:** send the raw bits through the channel, rebuild text.
- [ ] **With code:** encode each chunk, send, decode, rebuild text.
- [ ] Show all three at the same time: original, without code, with code.

---

## Step 8 - Scenario 3: image

- [ ] User picks a 24-bit `.bmp` file. Show it.
- [ ] Keep the **header** untouched (service info) - if it gets corrupted the image won't even open.
- [ ] Take only the pixel data -> bits -> chunks of length `k` (pad like in text).
- [ ] Same two runs as text: without code and with code.
- [ ] Show all three images side by side.

Reuse the text code here as much as possible - the only real difference is skipping the header.

---

## Step 9 - Cleanup and report

- [ ] Clean code, split into clear modules:
  - bit vectors / matrices
  - code (G, H, encoding)
  - channel
  - decoder (step-by-step)
  - text/image splitting and joining
  - UI
- [ ] Comments where things aren't obvious.
- [ ] Write the report: what's implemented, what isn't, how to run it, which libraries were used, how the decoder works, where each part lives in the code, a few test runs/screenshots.

---

## Order at a glance

1. Read the book (p. 73, p. 78–81) + hand example
2. Bit/matrix operations
3. G (typed / random) and H
4. Encoding
5. Channel
6. **Step-by-step decoder** <- most points
7. Scenario 1 (single vector) <- checkpoint, ~80% done
8. Scenario 2 (text)
9. Scenario 3 (image)
10. Cleanup + report

---

## Progress log

| Date | What I did |
|---|---|
| | |
