# Attention Mechanism — Training Materials

Teaching materials for explaining the Q/K/V attention mechanism to non-technical audiences.

## Contents

Two complementary plans for the same audience — pick by how you like to run a class:

- **[TRAINING-PLAN.md](TRAINING-PLAN.md)** — a *facilitator's* workshop plan: talk tracks, group activities, checks for understanding, and notes on the misconceptions that come up. Best for running a live session. No math required; one optional formula box for the person who asks.
- **[TTT-TRAINING-PLAN.md](TTT-TRAINING-PLAN.md)** — a *Test-Teach-Test* plan: the same content decomposed into 19 assessment-driven sub-goals with principle extraction, per-concept blueprints, worked examples, CTQ mastery criteria, and pass thresholds. Best for self-paced learning or tracking mastery. **Session 5** covers how Q/K/V are actually *trained* — random initialization, gradient-as-blame, and why Q, K, and V receive different gradients and therefore specialize.

Both are built around one idea:

> Nobody teaches attention what to pay attention to. It is a side effect of being repeatedly graded on one thing: predicting the next word.

## Deep dive — how the Q/K/V roles *emerge*

A focused unit on the single most counter-intuitive point: nobody assigns the query/key/value roles — they are pulled apart by differently-shaped gradients, and only when the task rewards asymmetry.

- **[ROLE-EMERGENCE-PLAN.md](ROLE-EMERGENCE-PLAN.md)** — a tight TTT plan (5 core principles, 13 sub-goals) exclusively on emergence: learned projections → gradient-as-blame → symmetry breaking → positional differentiation → emergent roles. No calculus; gradients taught as "direction + size of a nudge."
- **[emergence-of-qkv.html](emergence-of-qkv.html)** — a self-contained interactive explainer (four widgets). Builds from "what is a word vector" and "what is the score matrix S" up through all five principles, then goes deep on the questions this repo kept getting asked:
  - **where the Q/K/V idea comes from** (soft dictionary lookup; the Bahdanau → memory-networks → Transformer lineage; reasoned vs. stumbled-upon);
  - **why Q and K are *not* interchangeable** even though `Q·K` is commutative — the transpose argument with indices, and the wiring asymmetry (`Q_A` feeds only token A's output, `K_A` feeds everyone's), with a click-to-see row/column widget;
  - **how position is encoded** — one-hot toy vs. real sinusoidal / RoPE positional encodings;
  - an **interactive gradient-descent exercise** on a real positional task ("attend to the previous token") where you step through the math and watch `‖W_Q−W_K‖` climb as query and key specialize into a *position shifter* and a *position label*.
  → **[View it live](https://raw.githack.com/Antonio-Ardigo/Attention-Mechanism/main/emergence-of-qkv.html)** (rendered via raw.githack; GitHub serves raw `.html` as plain text).
- **[qkv_gradient_descent.py](qkv_gradient_descent.py)** — the runnable reference for the exercise: full forward + backward pass with sinusoidal positional encodings, printing every intermediate and the query/key divergence. `python qkv_gradient_descent.py`.

## The math track — attention worked out step by step

Everything above deliberately avoids math. This is the other track, for readers who want the arithmetic.

- **[attention-math.html](attention-math.html)** — a self-contained interactive explainer following the line of Luis Serrano's [*"The math behind Attention: Keys, Queries, and Values matrices"*](https://www.youtube.com/watch?v=UPtG_38Oq8o) (Serrano.Academy, ~33 min): the same order, the same worked example, with the arithmetic made playable. Eleven steps from *"two sentences, one word"* to the assembled formula, with six live figures:
  - a **similarity lab** — drag two vectors and watch dot product, cosine, and scaled dot product move apart, which is what motivates dividing by `√d`;
  - a **pairwise similarity grid** and a **softmax lab** where the `√d` divisor visibly controls whether attention compares or just picks;
  - **the apple, moved** — *apple* sits at cosine ≈0.77 from both *orange* and *phone*, and slides toward whichever one is in the sentence, computed live rather than animated by hand;
  - **direction, and what tying costs** — the score matrix with `W_Q` and `W_K` independent, then tied, showing the mirror gap collapse to exactly zero;
  - **the same words, three spaces** — one word set under the embedding, K/Q, and V projections.
  - It closes with **what the video leaves out**: positional encoding, causal masking, residuals and normalisation, the `K·Qᵀ` vs `Q·Kᵀ` notation trap, and why attention weights are not an explanation.
  → **[View it live](https://raw.githack.com/Antonio-Ardigo/Attention-Mechanism/main/attention-math.html)**

On Q versus K the two artefacts approach the same fact from different directions and are worth reading together: `emergence-of-qkv.html` argues it from the wiring, while `attention-math.html` argues it from the bilinear form — since only the product `M = W_Q W_Kᵀ` affects the scores, and `M` is not symmetric, attention is directional; tying the two matrices would make `M` symmetric and destroy that.

## Sourcing

Material that cites a video is checked against a retrieved transcript rather than recollection.

- **[tools/fetch_transcript.py](tools/fetch_transcript.py)** — fetches timestamped captions with [yt-dlp](https://github.com/yt-dlp/yt-dlp), with an optional local [faster-whisper](https://github.com/SYSTRAN/faster-whisper) fallback. See [tools/README.md](tools/README.md).
- **[sources/index.md](sources/index.md)** — the citation table: what was consulted, by whom, and when. Transcripts themselves are git-ignored, since they are the video author's work; see [sources/README.md](sources/README.md).

## Who it's for

The non-technical plans assume no prerequisites — product managers, analysts, designers, executives, and engineers new to ML. The math track assumes vectors, matrix multiplication, and comfort reading a formula.

## Format

The workshop plan runs as 4 × 60–75 minute sessions or one half-day, each session with a talk track, a group activity, a check for understanding, and facilitator notes. The TTT plans are self-paced. The two HTML explainers are read on your own, in a browser, in any order.
