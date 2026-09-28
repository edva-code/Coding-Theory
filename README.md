# Coding Theory / Error-Correcting Code

Lab work for the Coding Theory course (VU). My task number is **A11**.

## What the program does

The program shows how an error-correcting code protects data sent over a noisy channel.
It does three things with a message:

1. **Encodes** it with a binary linear code `C[n, k]`.
2. **Sends** it through a noisy channel, where every bit can get flipped with probability `pe`.
3. **Decodes** what came out of the channel using **step-by-step decoding**, fixing the errors if there aren't too many of them.

## My task (A11)

| What | Value |
|---|---|
| Field | `q = 2` (just bits, 0 and 1, all math is mod 2) |
| Code | Linear code `C[n, k]` |
| Decoding algorithm | Step-by-step decoding (p. 79) |
| Code parameters | Length `n`, dimension `k`, generator matrix `G` |
| Literature | [VO89] Vanstone & van Oorschot, *An Introduction to Error Correcting Codes with Applications*, §3.7, p. 78–81 and p. 73 |
| Notes that apply | 4, 7, 11 |

What the notes mean for me:

- **Note 4** - the user can either type in the generator matrix `G` themselves, or let the program generate a random one for the given `n` and `k`. Both options must exist.
- **Note 7** - background reading on linear codes (lecture notes or [Sta02, §1.1, §2.1–2.2]).
- **Note 11** - it's enough to support `G` in **standard form**, `G = [I_k | A]`. This makes things much easier.

## The user can

- Set `n`, `k`, the matrix `G` (typed in or random) and the error probability `pe` (at least 0.0001 precision).
- **Scenario 1 - a single vector:** type a vector of length `k`, see it encoded, see what the channel did to it (how many errors and where), edit the received vector by hand if wanted, then see the decoded result.
- **Scenario 2 - text:** type some text (can be multiple lines). See it side by side: original, sent without coding, and sent with coding.
- **Scenario 3 - image:** pick a 24-bit `.bmp` image. See it side by side the same way: original, without coding, with coding.

## How step-by-step decoding works (short version)

1. From `G = [I_k | A]` build the parity-check matrix `H = [A^T | I_(n-k)]`.
2. Make a table: for every possible syndrome, store the **weight of its coset leader** (the smallest number of errors that would produce that syndrome).
3. Take the received vector `r` and go through its bits one by one:
   - Flip the bit.
   - If the flip makes the coset leader weight of the syndrome **smaller**, keep the flip. Otherwise, undo it.
   - Stop as soon as the syndrome is all zeros.
4. Because `G` is in standard form, the first `k` bits of the corrected vector are the original message.

The full plan and progress are in [documentation.md](documentation.md).
