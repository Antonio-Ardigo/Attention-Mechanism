# Training Plan: Q/K/V Attention for Non-Mathematical Thinkers
Generated: 2026-08-13 | Status: in-progress

## Learning Goal
A four-session training plan (60–75 min each, or one half-day) for teaching the Q/K/V attention mechanism to people who are smart but not mathematical: product managers, analysts, designers, executives, engineers new to ML.

## SMART Goal
Explain and apply Query-Key-Value attention intuitively to interpret transformer behavior within four sessions.

## Principle Extraction

| Principle | Statement | Formally | Prerequisites |
|-----------|-----------|---------|---------------|
| **P1 — Soft retrieval** | Attention is a *soft* lookup: every token asks a question and pulls a weighted blend of information from all other tokens, not a single exact match. | soft(query→all values) vs. `VLOOKUP(exact)` | Idea of "looking something up"; relevance/similarity |
| **P2 — Three roles (Q/K/V)** | Each token is projected into three separate roles: a Query (what it's looking for), a Key (what it advertises), and a Value (the content it delivers). | $Q=xW_Q,\ K=xW_K,\ V=xW_V$ | Words-as-vectors (embeddings); a token can play >1 role |
| **P3 — Relevance → weights** | Relevance is scored by matching Queries against Keys, then those scores are normalized into weights that add to 100%. | $w=\text{softmax}(QK^{\top}/\sqrt{d_k})$ | Similarity/dot-product intuition; percentages that sum to 1 |
| **P4 — Weighted blend of Values** | Each token's output is a weighted average of everyone's Values — a context-aware mix, not a copy of one word. | $\text{out}=wV$ | Weighted average; P3 |
| **P5 — Context reshapes meaning** | Because each token is rebuilt from relevant context, the same word gets different meaning in different sentences; multiple heads find different relationships at once. | $\text{MultiHead}=\text{concat}(head_1..head_h)W_O$ | P1–P4 combined |
| **P6 — Learned projections** | Q, K, V come from three separate weight matrices *learned* during training; their roles emerge — they are not hand-designed. | $Q=xW_Q,\ K=xW_K,\ V=xW_V$ (the $W$'s are learned) | A network has adjustable weights; a training objective (predict next token) exists |
| **P7 — Gradient = blame signal** | Training nudges each weight *opposite* its gradient, by an amount proportional to how much it contributed to the error. | $W \leftarrow W-\eta\,\partial L/\partial W$ | Notion of error/loss; "adjust to reduce mistakes"; slope/direction |
| **P8 — Positional differentiation** | Q, K, V receive *different* gradients because they sit at different positions in the computation, so they specialize despite a symmetric design. | $\partial L/\partial W_Q\!\propto\!K,\ \partial L/\partial W_K\!\propto\!Q,\ \partial L/\partial W_V\!\propto\!a$ | P6, P7, and the forward pass (P2–P4) |

## Sub-Goals

| # | Axis | Sub-Goal | Domain | Difficulty | Depth | Principle | Status | Score |
|---|------|----------|--------|-----------|-------|-----------|--------|-------|
| SG-1 | Motivation | Explain why attention lets LLMs understand context, unlocking modern AI. | ML / NLP | low | intro | — | pending | - |
| SG-2 | Core Principle | State that attention is a soft, weighted lookup over all tokens. | Attention | low | intro | P1 | pending | - |
| SG-3 | Core Principle | Distinguish the three roles Query, Key, and Value and their purposes. | Attention | low | intro | P2 | pending | - |
| SG-4 | Core Principle | Explain that matching Queries to Keys yields normalized relevance weights. | Attention | low | intro | P3 | pending | - |
| SG-5 | Core Principle | Explain each token's output as a weighted blend of all Values. | Attention | low | intro | P4 | pending | - |
| SG-6 | Core Principle | Explain how attention reshapes a word's meaning from its context. | Attention | low | intro | P5 | pending | - |
| SG-7 | Key Concept | Assign Query/Key/Value roles to words in a real sentence correctly. | Attention | medium | inter | P2 | pending | - |
| SG-8 | Key Concept | Read an attention heatmap to identify which words attend to which. | Interpretability | medium | inter | P3, P4 | pending | - |
| SG-9 | Key Concept | Explain normalization (softmax/scaling) as a competition for attention. | Attention | medium | inter | P3 | pending | - |
| SG-10 | Key Concept | Explain how attention resolves an ambiguous word like "it" to its referent. | NLP | medium | inter | P5 | pending | - |
| SG-11 | Key Concept | Explain multi-head attention as parallel finders of different relationships. | Attention | medium | inter | P5 | pending | - |
| SG-12 | Tools | Apply an attention mental model to reason about a prompt/product behavior. | Applied ML | medium | inter | P1, P5 | pending | - |
| SG-13 | Core Principle | State that Q/K/V come from three learned matrices; roles emerge from training. | Training | low | intro | P6 | pending | - |
| SG-14 | Core Principle | Explain gradient descent as nudging each weight to reduce prediction error. | Optimization | low | intro | P7 | pending | - |
| SG-15 | Core Principle | Explain that Q/K/V differ because they sit at different graph positions. | Training | low | intro | P8 | pending | - |
| SG-16 | Key Concept | Explain why random, different initialization breaks Q/K/V symmetry. | Training | medium | inter | P6, P8 | pending | - |
| SG-17 | Key Concept | Explain why Q, K, and V receive different gradient signals. | Training | medium | inter | P8 | pending | - |
| SG-18 | Key Concept | Predict what capability is lost if projections are tied or removed. | Training | medium | inter | P7, P8 | pending | - |
| SG-19 | Verification | Teach the full pipeline end-to-end, including how Q/K/V are learned. | Attention | high | adv | P1–P8 | pending | - |

## Prerequisite Graph

```
Understand Q/K/V Attention (core)
  requires:
    Word embeddings — words as lists of numbers (prerequisite) ← CHECK learner profile  [NOT CONFIRMED]
    Weighted average / percentages summing to 100% (prerequisite) ← CHECK learner profile  [NOT CONFIRMED]
    High-level idea of an LLM / transformer (prerequisite) ← partly covered by SG-1
    A network has adjustable weights tuned to reduce error (prerequisite) ← CHECK  [NOT CONFIRMED]  (training block)
    Slope / "which way reduces the mistake" intuition (prerequisite) ← CHECK  [NOT CONFIRMED]  (training block)
  rests on:
    P1 Soft retrieval (principle) → SG-2
      led to:
        P2 Three roles Q/K/V (principle) → SG-3
          led to:
            P3 Relevance → weights (principle) → SG-4
              led to:
                P4 Weighted blend of Values (principle) → SG-5
                  led to:
                    P5 Context reshapes meaning (principle) → SG-6
  rests on (training — how the projections above are learned):
    P6 Learned projections (principle) → SG-13   [needs the forward pass P2–P4 to exist]
    P7 Gradient = blame signal (principle) → SG-14
      both led to:
        P8 Positional differentiation (principle) → SG-15   [rests on P6, P7, and P2–P4]
```

**Key-Concept trace (every dependency maps to a graph edge):**
- SG-7 → P2 (SG-3)
- SG-8 → P3 (SG-4) + P4 (SG-5)
- SG-9 → P3 (SG-4)
- SG-10 → P5 (SG-6), rests on P1 (SG-2)
- SG-11 → P5 (SG-6)
- SG-12 → P1 (SG-2) + P5 (SG-6)
- SG-16 → P6 (SG-13) + P8 (SG-15)
- SG-17 → P8 (SG-15)
- SG-18 → P7 (SG-14) + P8 (SG-15)
- SG-19 → P1–P8 (SG-2 … SG-6, SG-13 … SG-15)

### ⚠ Prerequisite Warnings
- **Word embeddings** (words as vectors) is not confirmed in the learner profile — it covers Quantum Computing, a different domain. Open SG-3 with a 3-minute "words as lists of numbers" primer before testing.
- **Weighted average** is likewise unconfirmed — verify with a 60-second check before SG-5.
- **Training prerequisites (Session 5):** "a network has adjustable weights" and "which direction reduces the error" are unconfirmed. Open SG-13/SG-14 with a 2-minute "a neural net is a stack of number-knobs tuned to cut mistakes" primer. Keep gradients as *direction + size of a nudge* — no calculus required.
- These are *conceptual* prerequisites only; no math manipulation is required of the learner.

## Sequence
Strict dependency order follows the graph: **SG-1 → SG-2 → SG-3 → SG-4 → SG-5 → SG-6** (forward-pass principle chain, each rests on the prior), then the Key Concepts that apply them (**SG-7, SG-8, SG-9, SG-10, SG-11**), then the Tool (**SG-12**). The new **training block rests on the forward pass being understood**: principles **SG-13 → SG-14 → SG-15**, then Key Concepts **SG-16, SG-17, SG-18**. Verification (**SG-19**) comes last and now covers *both* the forward pass and training. Suggested session grouping:

- **Session 1 (Foundations):** SG-1, SG-2, SG-3 — *why it matters + soft lookup + the three roles*
- **Session 2 (The Mechanism):** SG-4, SG-5, SG-7 — *scoring, blending, and role-assignment practice*
- **Session 3 (Seeing It Work):** SG-6, SG-8, SG-9, SG-10 — *context, heatmaps, competition, disambiguation*
- **Session 4 (Depth):** SG-11, SG-12 — *multi-head + applied mental model*
- **Session 5 (How Q/K/V Are Learned + Capstone):** SG-13, SG-14, SG-15 (training principles) → SG-16, SG-17, SG-18 (key concepts) → **SG-19** teach-back. This is a full session on its own; if time-boxed to 60–75 min, split into **5a** (SG-13–15) and **5b** (SG-16–18 + SG-19).

Half-day option: Sessions 1–4 in the morning, Session 5 after lunch; keep SG-19 as the closing capstone.

## Session Blueprints

### SG-1: Why Attention Matters (Motivation)
- **Initial Test:** Show two translations of "The bank raised rates" vs. "We sat on the river bank." Ask the learner: *what does a language model need to get right here that a simple word-by-word dictionary cannot, and why is that hard?*
- **Pass Criteria:** Names "context / meaning depends on surrounding words" as the core problem; connects it to why older word-by-word systems failed (≥2 of 3 ideas: ambiguity, long-range links, context).
- **Estimated Depth:** introductory
- **Principle:** —
- **Exercise:** Take the sentence "She told her sister that she was proud of her." Circle every ambiguous word and, for each, list which *other* word in the sentence you'd need to look at to resolve it. (5 min; expected: "she", "her" → each needs a specific antecedent.)
- **Anticipated CTQs:**
  | CTQ | Source | Mastery Test | Common Failure Mode |
  |-----|--------|-------------|---------------------|
  | Meaning is context-dependent, not word-local | Motivation | Give an ambiguous word; learner points to disambiguating context | [overgeneralization]: "words just have fixed meanings" |
  | Long-range dependencies are the hard part | Motivation | Learner finds a link spanning many words | [missing-prerequisite]: only sees adjacent-word links |
- **Teach Topics:** The context problem in language; why bag-of-words/n-gram methods break; attention as "let every word look at every other word." Pitfall — [conflation]: confusing attention (the mechanism) with the whole transformer.
- **Final Test:** Give "I left my phone on the charger because it was dead." Ask what a model must resolve and why a fixed dictionary can't. Pass = identifies "it" → phone and the need for context.

### SG-2: Attention Is a Soft Lookup (Core Principle)
- **Principle:** P1 — Soft retrieval: attention pulls a *weighted blend* of information from all tokens, not one exact match.
- **Worked Example (foundational):**
  **Given:** A spreadsheet `VLOOKUP` that finds "Milan" and returns exactly one row: population = 1.4M. Now the sentence "I poured water from the bottle into the cup until **it** was full."
  **Step 1:** In `VLOOKUP`, the lookup is *hard* — one key matches, one value returns.
  > **Why:** Classic databases need an exact key; there's no "70% Milan, 30% Rome."
  **Step 2:** In attention, "it" doesn't match one word. It sends a query to *every* word and gets back relevance: cup ≈ high, bottle ≈ low, water ≈ medium.
  > **Why:** "full" makes the container (cup) most relevant, but nothing is excluded — it's a soft blend.
  **Result:** The information for "it" is ~70% cup + 20% water + 10% bottle — a *weighted blend*, not a single lookup. That "soft, everyone-contributes" property is the essence of attention.
- **Initial Test:** In your own words, contrast a spreadsheet `VLOOKUP` with attention using one example sentence. What does "soft" buy you?
- **Pass Criteria:** Can state the principle in own words AND apply it to a basic scenario correctly (names blend-of-many vs. exact-one).
- **Estimated Depth:** introductory
- **Exercise:** For "The trophy didn't fit in the suitcase because it was too big," estimate (as rough %) how much "it" should pull from each of {trophy, suitcase, big}. Then flip to "…too small" and re-estimate. (5–10 min; expected: "big" → trophy, "small" → suitcase.)
- **Anticipated CTQs:**
  | CTQ | Source | Mastery Test | Common Failure Mode |
  |-----|--------|-------------|---------------------|
  | Attention blends many sources, weighted | P1 | Learner gives non-zero weights to several words | [overgeneralization]: treats it as pick-the-single-best word |
  | Soft ≠ fuzzy/random — weights are principled | P1 | Learner ties weight to relevance | [conflation]: "soft" = "vague guess" |
- **Teach Topics:** Hard vs. soft lookup; "query the whole room, weighted by relevance." Pitfall — [conflation]: soft lookup vs. a probability guess of the *next* word (different thing).
- **Final Test:** Contrast a hotel keycard (opens one door) with attention (opens "a bit of every door, weighted"). Ask learner to pick which is attention and justify. Pass = correct + justifies with blend/weighting.

### SG-3: The Three Roles — Query, Key, Value (Core Principle)
- **Principle:** P2 — Three roles: each token becomes a Query (what I want), a Key (what I advertise), and a Value (the content I deliver).
- **Worked Example (foundational):**
  **Given:** A dating-app analogy for the word "it" searching a sentence.
  **Step 1:** **Query** = what "it" is looking for → "I need a concrete singular noun I refer to."
  > **Why:** The Query is the *search intent*, derived from the word plus its position.
  **Step 2:** Every other word advertises a **Key** = its "profile tagline" → "animal: I'm a living creature"; "street: I'm a place."
  > **Why:** Keys are what get *matched against* the Query — they decide relevance, not content.
  **Step 3:** Each word also holds a **Value** = the actual content it will hand over → the rich meaning of "animal."
  > **Why:** Matching uses Q vs. K; the information delivered comes from V. Match and payload are deliberately separated.
  **Result:** "it" (Query) matches "animal" (Key) strongly → so it receives "animal's" Value. One word, three jobs: seeker, advertiser, deliverer.
- **Initial Test:** *(Open with a 3-min "words as lists of numbers" primer — prerequisite not confirmed in profile.)* For the word "apple" in "I ate the red apple," describe what its Query, Key, and Value would each be responsible for.
- **Pass Criteria:** Can state the three roles in own words AND correctly assign the *purpose* of each to a basic example (search-intent / advertisement / payload).
- **Estimated Depth:** introductory
- **Exercise:** Fill a 3-column table (Query / Key / Value) for the word "Paris" in "She flew to Paris in June." Write one plain-English sentence per column describing that role's job. (5–10 min.)
- **Anticipated CTQs:**
  | CTQ | Source | Mastery Test | Common Failure Mode |
  |-----|--------|-------------|---------------------|
  | Q, K, V are three roles of the *same* token | P2 | Learner confirms one word produces all three | [missing-prerequisite]: thinks Q/K/V are three different words |
  | Keys decide match; Values deliver content | P2 | Learner routes relevance to K, payload to V | [conflation]: merges Key and Value |
  | Query = search intent, not the answer | P2 | Learner phrases Q as a "looking-for" | [conflation]: Query = the retrieved result |
- **Teach Topics:** The library analogy (Query = your search terms, Key = book spine labels, Value = book contents); one token → three projections. Pitfall — [conflation]: K vs. V; [missing-prerequisite]: forgetting all three come from one embedding.
- **Final Test:** For "dog" in "The dog barked loudly," have the learner assign the job of Q, K, and V, and explain why Key and Value are kept separate. Pass = all three purposes correct + separation rationale.

### SG-4: Relevance Becomes Weights (Core Principle)
- **Principle:** P3 — Relevance → weights: score each Query against every Key, then normalize scores into weights that add to 100%.
- **Worked Example (foundational):**
  **Given:** Query from "it"; raw match scores against Keys → animal: 8, street: 3, tired: 1.
  **Step 1:** Compare Query to each Key → similarity scores 8, 3, 1 (bigger = more relevant).
  > **Why:** A high score means the Key's advertisement matches what the Query wants (dot-product similarity, in the real math).
  **Step 2:** Turn scores into shares that sum to 100%: 8/12 = 67%, 3/12 = 25%, 1/12 = 8%.
  > **Why:** Normalizing makes weights comparable and bounded; real attention uses softmax, which pushes the top score even higher.
  **Result:** Attention weights = {animal 67%, street 25%, tired 8%}. Relevance has become a clean set of percentages.
- **Initial Test:** Given match scores {A: 6, B: 3, C: 1}, turn them into attention weights that sum to 100%, and say which word "wins" most attention.
- **Pass Criteria:** Can state the principle in own words AND correctly normalize a basic set of scores (within reason) AND name the winner.
- **Estimated Depth:** introductory
- **Exercise:** Given scores {5, 4, 1}, compute rough weights, then *double* the top score to 10 and recompute. Describe how the winner's share changed. (5 min; expected: top share grows, others shrink.)
- **Anticipated CTQs:**
  | CTQ | Source | Mastery Test | Common Failure Mode |
  |-----|--------|-------------|---------------------|
  | Weights sum to 100% | P3 | Learner's weights total 1 | [procedural-without-conceptual]: normalizes wrong / total ≠ 1 |
  | Score comes from Query–Key match | P3 | Learner ties high weight to high Q·K match | [conflation]: thinks weight comes from the Value |
  | Bigger score → disproportionately more weight | P3 | Learner notes softmax exaggerates the top | [verbal-without-formal]: "just averages" evenly |
- **Teach Topics:** Similarity as "how well do Query and Key line up"; normalization as "turn scores into a fair share of 100%"; softmax intuition (winner-take-more, not winner-take-all). Pitfall — [procedural-without-conceptual]: normalizing mechanically without knowing why shares must sum to 1.
- **Final Test:** Given {X: 9, Y: 9, Z: 2}, produce weights and explain what a near-tie between X and Y means for the blend. Pass = correct weights + interprets the tie as shared attention.

### SG-5: The Output Is a Blend of Values (Core Principle)
- **Principle:** P4 — Weighted blend: each token's output is the weighted average of all Values, using the P3 weights.
- **Worked Example (foundational):** *(60-sec weighted-average check first — prerequisite unconfirmed.)*
  **Given:** Weights {animal 67%, street 25%, tired 8%}. Represent each word's Value by one property, "animate-ness": animal = 10, street = 0, tired = 5.
  **Step 1:** Multiply each Value by its weight: 10 × 0.67 = 6.7; 0 × 0.25 = 0; 5 × 0.08 = 0.4.
  > **Why:** Each word contributes its content in proportion to how much attention it won.
  **Step 2:** Add them up: 6.7 + 0 + 0.4 = **7.1**.
  > **Why:** The sum is the new, context-aware representation of "it."
  **Result:** "it" now carries animate-ness ≈ 7.1 — strongly animate → it has effectively become "the animal." The output is a *blend*, dominated by the highest-weighted Value.
- **Initial Test:** Weights {A: 50%, B: 30%, C: 20%}; Values (one property each) {A: 4, B: 10, C: 0}. Compute the blended output and say which word dominates it.
- **Pass Criteria:** Can state the principle in own words AND correctly compute a basic weighted blend AND identify the dominant contributor.
- **Estimated Depth:** introductory
- **Exercise:** Keep Values fixed but swap the weights to {A: 10%, B: 10%, C: 80%}. Recompute the blend and describe how the "meaning" of the output shifted. (5 min; expected: output now dominated by C.)
- **Anticipated CTQs:**
  | CTQ | Source | Mastery Test | Common Failure Mode |
  |-----|--------|-------------|---------------------|
  | Output = Σ (weight × Value) | P4 | Learner computes a correct weighted sum | [procedural-without-conceptual]: averages Values ignoring weights |
  | It blends Values, not Keys | P4 | Learner uses V (not K) in the sum | [conflation]: blends the wrong role |
  | Changing weights changes meaning | P4 | Learner predicts output shift from weight change | [formal-without-intuitive]: computes but can't interpret |
- **Teach Topics:** Weighted average as "the loudest voices shape the result"; why we blend Values and not Keys; the smoothie analogy (weights = how much of each fruit). Pitfall — [conflation]: mixing Keys into the blend.
- **Final Test:** Weights {A: 20%, B: 20%, C: 60%}; Values {A: 9, B: 9, C: 1}. Compute the blend and explain why a low-Value word can still dominate if it wins the weight. Pass = correct number + interpretation.

### SG-6: Context Reshapes Meaning (Core Principle)
- **Principle:** P5 — Context reshapes meaning: because each token is rebuilt from relevant context, the same word means different things in different sentences.
- **Worked Example (foundational):**
  **Given:** The word "bank" in two sentences: (1) "I deposited money in the **bank**." (2) "We fished from the **bank** of the river."
  **Step 1:** Sentence 1 — "bank"'s Query matches "money"/"deposited" Keys highly → weights concentrate there.
  > **Why:** The finance context wins the attention competition.
  **Step 2:** The blend pulls finance-flavored Values → "bank" output ≈ *financial institution*.
  > **Why:** Output inherits whatever context it attended to.
  **Step 3:** Sentence 2 — now "river"/"fished" Keys match → blend pulls geography Values → "bank" output ≈ *riverside*.
  > **Why:** Same input word, different context, different attention, different meaning.
  **Result:** One spelling, two context-aware representations. Meaning is *produced* by attention, not stored in the word.
- **Initial Test:** Give two sentences using "light" (e.g., "turn on the light" vs. "this bag is light"). Explain, using attention, why the same word ends up meaning different things.
- **Pass Criteria:** Can state the principle in own words AND explain a fresh two-sentence example via which context each "light" attends to.
- **Estimated Depth:** introductory
- **Exercise:** Pick any homonym (spring, match, bat, crane). Write two sentences and, for each, name the 1–2 context words that would win the most attention and steer its meaning. (5–10 min.)
- **Anticipated CTQs:**
  | CTQ | Source | Mastery Test | Common Failure Mode |
  |-----|--------|-------------|---------------------|
  | Meaning is contextual, produced by attention | P5 | Learner attributes shift to attended context | [overgeneralization]: "the model just memorized both meanings" |
  | Same input token, different output vector | P5 | Learner separates spelling from representation | [conflation]: input embedding = final meaning |
- **Teach Topics:** Contextual vs. static embeddings; "a word is defined by the company it attends to." Pitfall — [conflation]: fixed dictionary embedding vs. the context-updated output.
- **Final Test:** Give "charge" in "charge the battery" vs. "charge the customer." Ask learner to trace, via attention, how meaning diverges. Pass = ties each meaning to the winning context words.

### SG-7: Assign Q/K/V Roles in a Real Sentence (Key Concept)
- **Initial Test:** For "The chef tasted the soup because it needed salt," build a small table: for the word "it," write its Query; for "soup" and "chef," write their Keys; and say whose Value "it" should mostly receive.
- **Pass Criteria:** Correctly assigns Query to "it," plausible Keys to ≥2 words, and routes the dominant Value to "soup" (the correct referent). ≥3 of 4 elements right.
- **Estimated Depth:** intermediate
- **Principle:** P2
- **Exercise:** Take a headline of your choice (≤12 words). Pick one ambiguous or pronoun word, write its Query, and list the two words whose Keys it should match most. (5–10 min.)
- **Anticipated CTQs:**
  | CTQ | Source | Mastery Test | Common Failure Mode |
  |-----|--------|-------------|---------------------|
  | Every word simultaneously has Q, K, V | P2 | Learner notes "soup" has its own Query too | [missing-prerequisite]: roles seen as exclusive |
  | Match uses Query↔Key across *different* words | P2 | Learner pairs "it"'s Q with "soup"'s K | [conflation]: matches Q to V, or a word to itself only |
  | Correct referent = highest Q·K, gets the Value | P2, P3 | Learner routes Value from the best-matching Key | [procedural-without-conceptual]: assigns roles but can't pick winner |
- **Teach Topics:** Practicing role assignment on real sentences; self-attention means every word queries every word (including itself). Pitfall — [conflation]: pairing a Query with a Value directly, skipping the Key.
- **Final Test:** For "The city council denied the protesters a permit because they feared violence," assign "they"'s Query and identify (via Keys) whether it refers to council or protesters, with justification. Pass = defensible referent + correct role routing.

### SG-8: Read an Attention Heatmap (Key Concept)
- **Initial Test:** Show a 6×6 attention heatmap (rows = query words, columns = key words) for "The dog chased the red ball." Ask: which word does "chased" attend to most, and what does a bright cell in row *i*, column *j* mean?
- **Pass Criteria:** Correctly reads ≥1 strong link from the map AND states the row/column convention (row = who is looking, column = what's being looked at) correctly.
- **Estimated Depth:** intermediate
- **Principle:** P3, P4
- **Exercise:** Given a printed heatmap, circle the brightest cell in two different rows and translate each into a plain sentence: "___ pays most attention to ___." (5 min.)
- **Anticipated CTQs:**
  | CTQ | Source | Mastery Test | Common Failure Mode |
  |-----|--------|-------------|---------------------|
  | Rows and columns are Query vs. Key | P3 | Learner states axis meaning correctly | [conflation]: reads the map transposed |
  | Brightness = weight = share of attention | P3 | Learner ties color to a percentage | [verbal-without-formal]: "bright = important" with no weight notion |
  | Each row sums to 100% | P3, P4 | Learner notes a row is a full distribution | [missing-prerequisite]: forgets rows normalize |
- **Teach Topics:** Reading attention visualizations (e.g., BertViz-style maps); rows as distributions summing to 1; diagonal = self-attention. Pitfall — [conflation]: transposing query/key axes.
- **Final Test:** Show a heatmap for "She poured the tea and drank it." Ask the learner to find where "it" attends and confirm it points to "tea," reading the axes correctly. Pass = correct link + correct axis interpretation.

### SG-9: Normalization as a Competition (Key Concept)
- **Initial Test:** Two words have match scores 5.0 and 4.9 (nearly tied). After softmax-style normalization, will attention be split ~50/50 or lopsided? Then scores become 8.0 and 1.0 — describe the split. Explain why we normalize at all.
- **Pass Criteria:** Recognizes near-ties → near-even split, large gaps → lopsided (winner-take-more), AND gives one valid reason for normalizing (weights must sum to 1 / comparable / stable).
- **Estimated Depth:** intermediate
- **Principle:** P3
- **Exercise:** Rank three scenarios by how "decisive" the attention is: {6,5,4}, {10,1,1}, {4,4,4}. Say which is most spread out and which is most winner-take-all, and why. (5 min.)
- **Anticipated CTQs:**
  | CTQ | Source | Mastery Test | Common Failure Mode |
  |-----|--------|-------------|---------------------|
  | Normalization forces weights to sum to 100% | P3 | Learner states the sum-to-1 rule | [procedural-without-conceptual]: normalizes without knowing why |
  | Softmax exaggerates the leader | P3 | Learner predicts lopsided split for a big gap | [overgeneralization]: assumes proportional/linear split |
  | Scaling (÷√d) keeps scores from exploding | P3 | Learner states scaling prevents saturation | [formal-without-intuitive]: memorizes √d with no reason |
- **Teach Topics:** Softmax as "amplify the winner, keep everyone in the race"; why raw scores are scaled before normalizing (stability); temperature intuition. Pitfall — [overgeneralization]: treating softmax as a plain proportional share.
- **Final Test:** Given scores {7, 2, 1} vs. {3, 2, 2}, say which produces a more focused (peaked) attention and explain the role of the score *gap*. Pass = identifies the {7,2,1} case + gap reasoning.

### SG-10: Attention Resolves "It" (Key Concept)
- **Initial Test:** "The lawyer questioned the witness because she was lying." Explain, step by step in attention terms (query → key match → value blend), how the model decides whether "she" is the lawyer or the witness.
- **Pass Criteria:** Walks through Query("she") → Key matches → weighted Value blend, and names a defensible referent with reasoning tied to context ("lying" ↔ witness). ≥3 pipeline steps correct.
- **Estimated Depth:** intermediate
- **Principle:** P5 (rests on P1)
- **Exercise:** Write two versions of a sentence where flipping one word flips what "it/they/she" refers to (like the trophy/suitcase pair). Explain which context word drives the switch. (5–10 min.)
- **Anticipated CTQs:**
  | CTQ | Source | Mastery Test | Common Failure Mode |
  |-----|--------|-------------|---------------------|
  | Coreference = a query finding its best key | P5, P1 | Learner frames "it"'s search as Q↔K | [missing-prerequisite]: skips the query step |
  | The referent's Value dominates "it"'s blend | P4, P5 | Learner says "it" inherits the referent's meaning | [conflation]: thinks "it" is replaced, not blended |
  | Small wording changes can flip the referent | P5 | Learner shows a flip via a context word | [overgeneralization]: "it always means the nearest noun" |
- **Teach Topics:** Coreference/Winograd-style disambiguation; nearest-noun is a heuristic, not the mechanism; the referent contributes the largest Value. Pitfall — [overgeneralization]: "it" = closest noun.
- **Final Test:** "The delivery driver waved at the cyclist as he crossed the intersection." Trace the attention decision for "he" and justify the more likely referent. Pass = pipeline steps + context-based justification.

### SG-11: Multi-Head Attention (Key Concept)
- **Initial Test:** One attention "head" tracks grammatical subject–verb links; another tracks pronoun references; a third tracks adjective–noun pairs. In "The tired old dog slowly climbed the steep stairs," what might three different heads each focus on, and why run them in parallel?
- **Pass Criteria:** Assigns ≥2 distinct, plausible relationships to different heads AND states the benefit (capture multiple relationship types simultaneously). 
- **Estimated Depth:** intermediate
- **Principle:** P5
- **Exercise:** For "The scientist who won the prize thanked her mentor," invent two heads: name what relationship each would attend to and draw the link (arrow between two words) for each. (5–10 min.)
- **Anticipated CTQs:**
  | CTQ | Source | Mastery Test | Common Failure Mode |
  |-----|--------|-------------|---------------------|
  | Heads run in parallel on the same input | P5 | Learner confirms simultaneous, not sequential | [conflation]: thinks heads are stacked layers |
  | Different heads learn different relationships | P5 | Learner assigns distinct roles to two heads | [overgeneralization]: "all heads do the same thing" |
  | Heads' outputs are combined (concatenated) | P5 | Learner states results are merged | [missing-prerequisite]: forgets recombination step |
- **Teach Topics:** Multi-head as "a committee of specialists looking at the same sentence"; heads ≠ layers; concatenate-then-combine. Pitfall — [conflation]: confusing multiple heads (parallel, one layer) with multiple layers (stacked, sequential).
- **Final Test:** In "The keys to the cabinet were left on the table," describe two heads (e.g., subject–verb agreement vs. prepositional attachment) and why parallelism helps. Pass = two distinct heads + parallelism rationale.

### SG-12: Apply the Attention Mental Model (Tools)
- **Initial Test:** A PM reports: "Our summarization feature keeps attributing a quote to the wrong person when two names appear early in the article." Using the Q/K/V mental model, diagnose *where* attention is likely going wrong and propose one prompt- or data-level thing to test — no code required.
- **Pass Criteria:** Frames the bug in attention terms (a query attending to the wrong key/referent) AND proposes ≥1 actionable, attention-informed test (e.g., clearer name proximity, disambiguating context, checking coreference). 
- **Estimated Depth:** intermediate
- **Principle:** P1, P5
- **Exercise:** Pick a real product/prompt situation you've seen (chatbot loses track of "it," wrong entity summarized). In 4 sentences, explain it as an attention-weighting problem and name one lever you'd pull. (5–10 min.)
- **Anticipated CTQs:**
  | CTQ | Source | Mastery Test | Common Failure Mode |
  |-----|--------|-------------|---------------------|
  | Product bugs map to attention behavior | P1, P5 | Learner reframes a bug as mis-weighted attention | [verbal-without-formal]: stays vague ("model is dumb") |
  | The model is not "reasoning," it's weighting context | P5 | Learner avoids anthropomorphizing | [overgeneralization]: "it just understands/decides" |
  | Interventions target what gets attended | P1 | Learner names a context/proximity lever | [procedural-without-conceptual]: proposes unrelated fix |
- **Teach Topics:** A reusable diagnostic frame — "what is each token attending to, and is that the right thing?"; translating attention intuition into prompt/design/data decisions; limits of the metaphor. Pitfall — [overgeneralization]: over-trusting the metaphor as literal mechanism.
- **Final Test:** "Our chatbot forgets which product the user asked about after a few turns." Diagnose in attention/context terms and propose one concrete mitigation. Pass = attention-framed diagnosis + actionable lever.

### SG-13: Q/K/V Are Learned, Not Designed (Core Principle)
- **Principle:** P6 — Learned projections: Q, K, V come from three weight matrices learned during training; the roles emerge.
- **Worked Example (foundational):**
  **Given:** a toy word vector x = [1, 0]. Three *randomly initialized* matrices.
  **Step 1:** $W_Q=\begin{bmatrix}0.9&0.1\\0.2&0.8\end{bmatrix}$ → Q = x·$W_Q$ = [0.9, 0.1]
  > **Why:** Q is the word seen through the "query lens" — the matrix, not the word, does the shaping.
  **Step 2:** $W_K=\begin{bmatrix}0.3&0.7\\0.6&0.4\end{bmatrix}$ → K = [0.3, 0.7]; $W_V=\begin{bmatrix}0.5&0.5\\0.1&0.9\end{bmatrix}$ → V = [0.5, 0.5]
  > **Why:** Same word, three different vectors — purely because the three matrices differ.
  **Result:** Q/K/V are not the word; they're three learned *lenses* on it. Nobody hand-codes "query = intent" — the numbers in these matrices get adjusted by training until that division of labor emerges.
- **Initial Test:** *(Open with a 2-min "a neural net is a stack of adjustable number-knobs (weights) tuned to reduce mistakes" primer — prereq not confirmed.)* In your own words: where do Q, K, and V come from, and what part is actually "learned"?
- **Pass Criteria:** Can state the principle in own words AND correctly say Q/K/V are produced by three separate learned matrices applied to the word — and that the *matrices* (not the roles) are what training sets.
- **Estimated Depth:** introductory
- **Exercise:** Given x = [2, 1] and $W_V=\begin{bmatrix}1&0\\0&1\end{bmatrix}$, compute V. Then change $W_V$ to $\begin{bmatrix}0&1\\1&0\end{bmatrix}$ and recompute. One sentence: what did "changing the matrix" do to the Value? (5 min.)
- **Anticipated CTQs:**
  | CTQ | Source | Mastery Test | Common Failure Mode |
  |-----|--------|-------------|---------------------|
  | Q/K/V are outputs of learned matrices, not fixed features | P6 | Learner names the three matrices as the learned part | [conflation]: thinks Q/K/V are hand-designed rules |
  | The roles emerge; they are not imposed | P6 | Learner says training discovers the division of labor | [overgeneralization]: "someone programmed query=intent" |
- **Teach Topics:** Three weight matrices; the "lens" metaphor; emergent specialization vs. hand-engineering. Pitfall — [conflation]: the fixed word embedding vs. its learned Q/K/V projections.
- **Final Test:** Explain why two different models, trained separately, could develop *different* Q/K/V matrices for the same vocabulary. Pass = ties it to training (random start + data), not to fixed rules.

### SG-14: Gradient Descent Nudges Each Weight (Core Principle)
- **Principle:** P7 — Gradient = blame signal: each weight is nudged *opposite* its gradient, by an amount proportional to its contribution to the error.
- **Worked Example (foundational):**
  **Given:** one weight w = 0.5. The model made a prediction; we measured the error (loss). Ask: if we raise w a little, does the error go up or down? Suppose *up* — so the gradient ∂L/∂w = +2. Learning rate η = 0.1.
  **Step 1:** Gradient sign +2 means "increasing w increases the error."
  > **Why:** The gradient is the *slope* of error-vs-this-weight — it points uphill on the mistake.
  **Step 2:** Move the opposite way: w ← w − η·(∂L/∂w) = 0.5 − 0.1×2 = **0.3**.
  > **Why:** Step downhill on the error; step size scales with the gradient — bigger blame, bigger nudge.
  **Result:** w = 0.3, and the error is now slightly lower. Repeat across *all* weights, millions of times → the network learns.
- **Initial Test:** A weight has gradient ∂L/∂w = −5 and learning rate 0.1. Which way and how far does it move, and why that direction?
- **Pass Criteria:** Can state the principle in own words AND compute w ← w + 0.5 (moves *opposite* the gradient) AND explain "downhill on the error, size proportional to blame."
- **Estimated Depth:** introductory
- **Exercise:** Two weights have gradients +1 and +10 at the same learning rate 0.1. Which one moves more, and what does that say about how much each is to blame for the current error? (5 min.)
- **Anticipated CTQs:**
  | CTQ | Source | Mastery Test | Common Failure Mode |
  |-----|--------|-------------|---------------------|
  | Weights move *opposite* the gradient | P7 | Learner subtracts (not adds) the gradient | [procedural-without-conceptual]: adds instead of subtracts |
  | Step size ∝ contribution to error | P7 | Learner predicts the bigger-gradient weight moves more | [overgeneralization]: all weights change equally |
  | Gradient = slope of loss w.r.t. that weight | P7 | Learner gives the "downhill" picture | [formal-without-intuitive]: memorizes the rule, no landscape image |
- **Teach Topics:** Loss as a landscape; gradient as steepest-*uphill* so we walk opposite; learning rate as step size. Pitfall — [procedural-without-conceptual]: sign errors that push weights the wrong way.
- **Final Test:** If a weight's gradient is ≈ 0 this step, what happens to it and why? Pass = "it barely moves — it isn't contributing to the current mistake."

### SG-15: Different Positions → Different Gradients (Core Principle)
- **Principle:** P8 — Positional differentiation: Q, K, V get different gradients because they sit at different points in the computation, so they specialize even though the design is symmetric.
- **Worked Example (foundational):**
  **Given:** a single score s = Q·K with Q = 3, K = 4 (toy scalars). Training wants s *bigger* to cut the error, so ∂L/∂s = −1.
  **Step 1:** Gradient delivered to Q = ∂L/∂s × K = −1 × 4 = **−4**.
  > **Why:** Q enters the score multiplied by K, so K *scales* Q's blame.
  **Step 2:** Gradient delivered to K = ∂L/∂s × Q = −1 × 3 = **−3**.
  > **Why:** Same-shaped formula, but K's blame is scaled by Q (= 3) — a *different number*.
  **Step 3:** V is not in the score at all; its gradient comes from the output blend (o = a·V) — a different path entirely.
  > **Why:** Different position in the computation → different gradient in *form*, not just value.
  **Result:** Q moves −4, K moves −3, V moves by something unrelated. Same starting architecture, three different nudges → the matrices drift apart and specialize.
- **Initial Test:** In s = Q·K with Q = 2, K = 5 and ∂L/∂s = +1, compute the gradient delivered to Q and to K. Why aren't they equal?
- **Pass Criteria:** Can state the principle in own words AND compute grad_Q = 5, grad_K = 2 (each = ∂L/∂s × the *other's* value) AND explain "each carries the other's value, and those values differ."
- **Estimated Depth:** introductory
- **Exercise:** Keep ∂L/∂s = 1 but set Q = 10, K = 1. Compute both gradients. Which of Q, K gets the bigger nudge, and what will that tend to do to their sizes over time? (5 min.)
- **Anticipated CTQs:**
  | CTQ | Source | Mastery Test | Common Failure Mode |
  |-----|--------|-------------|---------------------|
  | Q's gradient carries K, and K's carries Q | P8 | Learner scales each by the other's value | [conflation]: assumes both get the same gradient because the formula is symmetric |
  | V's gradient flows through a different path | P8 | Learner separates V (output) from Q/K (score) | [missing-prerequisite]: assumes all three are trained identically |
  | Different gradients → specialization over time | P8 | Learner predicts divergence | [overgeneralization]: "symmetric formula ⇒ identical result" |
- **Teach Topics:** Bilinear Q·K vs. linear V-in-output; "symmetric *shape*, asymmetric *numbers*"; why random init + different gradients guarantees divergence. Pitfall — [conflation]: symmetry of form mistaken for symmetry of outcome.
- **Final Test:** Explain to a colleague why Q and K don't collapse into the same matrix during training, even though Q·K = K·Q. Pass = cites the different gradient values (each scaled by the other's activations) plus different random starts.

### SG-16: Why Random Initialization Breaks Symmetry (Key Concept)
- **Initial Test:** An engineer initializes $W_Q$, $W_K$, $W_V$ all to the *same* values. Predict what happens to the three during training, and why the attention layer would fail to learn useful roles.
- **Pass Criteria:** States that identical init → identical gradients → the matrices stay identical forever, so no specialization; names random/different init as the fix. ≥2 of 3 ideas.
- **Estimated Depth:** intermediate
- **Principle:** P6, P8
- **Exercise:** Two weights start equal (both 0.5) and always receive the same gradient. Write what they equal after 3 updates. Then give one a different starting value and note that they now diverge. (5 min.)
- **Anticipated CTQs:**
  | CTQ | Source | Mastery Test | Common Failure Mode |
  |-----|--------|-------------|---------------------|
  | Identical init + identical gradient → permanently identical | P8 | Learner sees the update is deterministic | [missing-prerequisite]: doesn't realize both get the same nudge |
  | Random init *seeds* specialization | P6 | Learner calls randomness necessary, not just noise | [conflation]: thinks randomness is only for regularization |
  | All-zeros init is a classic failure | P6 | Learner flags dead/identical weights | [overgeneralization]: "any init works" |
- **Teach Topics:** Symmetry-breaking; the "all zeros / same seed" bug; randomness as a *feature*. Pitfall — [conflation]: init randomness confused with dropout or data shuffling.
- **Final Test:** A colleague initializes all three matrices from the *same* seed so they're identical, then trains 1000 steps — and they're still identical. Explain the mechanism. Pass = deterministic identical gradients keep them locked together.

### SG-17: Why Q, K, V Get Different Gradient Signals (Key Concept)
- **Initial Test:** Q and K both feed the score via Q·K, yet they don't end up identical — and V is trained differently still. In plain terms, explain the *gradient reason* all three stay distinct.
- **Pass Criteria:** Explains **(a)** Q's gradient is scaled by K's activations and K's by Q's (so different numbers), and **(b)** V's gradient flows through the output blend, not the score — a different path. Both halves required.
- **Estimated Depth:** intermediate
- **Principle:** P8
- **Exercise:** With ∂L/∂s = 2, Q = [1, 3], K = [2, 1] (treat elementwise for intuition): compute the nudge Q gets (∝ K) and the nudge K gets (∝ Q), and note that V is untouched by this score. (5–10 min.)
- **Anticipated CTQs:**
  | CTQ | Source | Mastery Test | Common Failure Mode |
  |-----|--------|-------------|---------------------|
  | Q-grad ∝ K and K-grad ∝ Q | P8 | Learner writes each gradient in terms of the *other* | [conflation]: symmetric algebra ⇒ symmetric gradient |
  | V-grad flows through the output, not the score | P8 | Learner routes V's gradient via o = a·V | [missing-prerequisite]: lumps V in with Q/K |
  | Distinct gradients drive distinct specialization | P8 | Learner connects gradient difference to role difference | [verbal-without-formal]: knows they differ but not *why* |
- **Teach Topics:** Bilinear-vs-linear distinction; "each of Q, K wears the other's coat in its gradient"; V's separate path. Pitfall — [conflation]: treating Q·K symmetry as gradient symmetry.
- **Final Test:** If you *swapped* which matrix is labeled "query" and which is "key" at initialization, would training still work? Explain via the gradient structure. Pass = "yes — the labels are arbitrary; the two just need to be distinct and each receives its own (different) gradient."

### SG-18: What Breaks If You Tie or Remove a Projection (Key Concept)
- **Initial Test:** To save parameters, a team sets $W_Q = W_K$ (one shared matrix for both query and key). What capability does the attention layer lose, and why? *(Hint: what does Q·K measure when Q and K come from the same matrix?)*
- **Pass Criteria:** Recognizes that tying Q = K forces a *symmetric* similarity (A attends to B exactly as B attends to A), losing *directional* relationships; names a case needing asymmetry (e.g., "it" → "animal" but not the reverse).
- **Estimated Depth:** intermediate
- **Principle:** P7, P8
- **Exercise:** Give one sentence where word A should attend to B much more than B attends to A. Explain why a single shared Q = K matrix couldn't represent that direction. (5–10 min.)
- **Anticipated CTQs:**
  | CTQ | Source | Mastery Test | Common Failure Mode |
  |-----|--------|-------------|---------------------|
  | Separate Q, K enable *directional* attention | P8 | Learner gives an asymmetric attention example | [conflation]: assumes attention is inherently symmetric |
  | Removing V leaves no content to deliver | P7 | Learner notes V carries the payload | [missing-prerequisite]: forgets V's job |
  | Fewer parameters is not free | P7 | Learner names the lost capability | [overgeneralization]: "sharing is harmless" |
- **Teach Topics:** Ablation intuition; directional vs. symmetric similarity; each matrix earns its parameters. Pitfall — [conflation]: assuming the attention weight matrix is symmetric.
- **Final Test:** A team removes $W_V$ and feeds raw embeddings as Values. What still works, what degrades, and why? Pass = scores still function, but the model loses its learned control over *what content* each word delivers.

### SG-19: Teach the Full Pipeline — Forward and Learned (Verification)
- **Initial Test:** In under 5 minutes and using one running example sentence, teach a non-technical colleague the *complete* story: **(1)** the forward pass (roles → scores → weights → blend → contextual meaning), AND **(2)** how Q/K/V are *learned* and why they end up different (random start → gradient nudges → different positions in the computation).
- **Pass Criteria:** Covers **P1–P5 in order** AND **P6–P8** (learned matrices, gradient-as-nudge, positional differentiation), with a coherent running example, no role confusion, pitched intuitively. ≥8 of 8 principles present.
- **Estimated Depth:** advanced
- **Principle:** P1–P8
- **Exercise:** Extend your 5-box forward-pass diagram with a "training loop" arrow beneath it (error → gradient → nudge each matrix), plus one caption explaining why the three matrices diverge. (5–10 min.)
- **Anticipated CTQs:**
  | CTQ | Source | Mastery Test | Common Failure Mode |
  |-----|--------|-------------|---------------------|
  | Forward pass and training are distinct but linked | P1–P8 | Learner keeps "what it does" vs. "how it's learned" separate yet connected | [conflation]: blends inference and training into one muddle |
  | Q/K/V differentiation is explained by gradients, not design | P8 | Learner cites different gradients, not hand-coding | [verbal-without-formal]: "they just are different" |
  | Explanation stays intuitive for a non-math audience | all | Colleague-level clarity, concrete example | [formal-without-intuitive]: drowns them in matrix calculus |
  | Lands both payoffs: contextual meaning + emergent specialization | P5, P8 | Learner states both "so what"s | [procedural-without-conceptual]: stops without a payoff |
- **Teach Topics:** Weaving the two narratives; the running-example discipline; teaching as the mastery test (Feynman). Pitfall — [formal-without-intuitive]: defaulting to equations for this audience.
- **Final Test:** Re-teach on a *different* sentence, then answer the colleague's question: "If nobody programmed the query/key/value roles, how did the model get them?" Pass = full pipeline on a fresh example + a correct emergence-from-training answer.

## Progress Log
(updated by /run-session)
