# Training Plan: How Q/K/V Roles Emerge
Generated: 2026-08-13 | Status: in-progress

## Learning Goal
Exclusively on how Q/K/V roles emerge, create .html artefact with example and graph, push.

## SMART Goal
Explain how Query/Key/Value roles emerge from training, not design, and teach it.

## Principle Extraction

| Principle | Statement | Formally | Prerequisites |
|-----------|-----------|---------|---------------|
| **P1 — Learned projections** | Q, K, V are three separate learned matrices applied to the *same* token; no role is hand-assigned. | $Q=xW_Q,\ K=xW_K,\ V=xW_V$ (the $W$'s are learned) | Matrix×vector as a "lens"; a network has learnable weights |
| **P2 — Symmetry breaking** | Identical parameters receive identical gradients and never differentiate; different (random) starts are required to specialize. | $W_Q=W_K\Rightarrow \partial L/\partial W_Q=\partial L/\partial W_K$ | Determinism of the update rule; P1 |
| **P3 — Gradient = blame** | Each weight moves *opposite* its gradient, by an amount proportional to its share of the error. | $W\leftarrow W-\eta\,\partial L/\partial W$ | Notion of loss; slope / "which way reduces the mistake" |
| **P4 — Positional differentiation** | Q, K, V sit at different positions in the computation, so they receive structurally different gradients and specialize. | $\partial L/\partial W_Q\!\propto\!K,\ \partial L/\partial W_K\!\propto\!Q,\ \partial L/\partial W_V\!\propto\!a$ | P1, P3; the forward pass (score → softmax → blend) |
| **P5 — Emergent roles** | "Query / key / value" meaning is a *side effect* of minimizing next-token loss, discovered by the optimizer, not specified. | $\{W_Q,W_K,W_V\}=\arg\min_W L$ | P1–P4 combined |

## Sub-Goals

| # | Axis | Sub-Goal | Domain | Difficulty | Depth | Principle | Status | Score |
|---|------|----------|--------|-----------|-------|-----------|--------|-------|
| SG-1 | Motivation | Appreciate that no engineer assigns Q/K/V roles; they arise from training. | ML / Training | low | intro | — | pending | - |
| SG-2 | Core Principle | State that Q/K/V come from three learned matrices, not hand-design. | Training | low | intro | P1 | pending | - |
| SG-3 | Core Principle | Explain why identical parameters never differentiate (symmetry breaking). | Training | low | intro | P2 | pending | - |
| SG-4 | Core Principle | Explain gradient descent as nudging each weight to reduce error. | Optimization | low | intro | P3 | pending | - |
| SG-5 | Core Principle | Explain that graph position gives Q/K/V different gradients. | Training | low | intro | P4 | pending | - |
| SG-6 | Core Principle | Explain that roles emerge as a side effect of minimizing loss. | Training | low | intro | P5 | pending | - |
| SG-7 | Key Concept | Show why Q's gradient carries K and K's carries Q. | Training | medium | inter | P4 | pending | - |
| SG-8 | Key Concept | Trace one full training step for a toy Q/K example end-to-end. | Training | high | adv | P3, P4 | pending | - |
| SG-9 | Key Concept | Explain why V trains through a different path than Q and K. | Training | medium | inter | P4 | pending | - |
| SG-10 | Key Concept | Predict how tying or removing a projection collapses the roles. | Training | medium | inter | P2, P4 | pending | - |
| SG-11 | Key Concept | Read a specialization-over-training graph and interpret divergence. | Interpretability | medium | inter | P5 | pending | - |
| SG-12 | Tools | Use a probe to verify whether an attention head actually specialized. | Interpretability | medium | inter | P5 | pending | - |
| SG-13 | Verification | Teach the full emergence story end-to-end using the graph. | Training | high | adv | P1–P5 | pending | - |

## Prerequisite Graph

```
How Q/K/V Roles Emerge (core)
  requires:
    Forward pass of attention — scores → softmax → blend (prerequisite) ← CHECK  [covered by companion plan TTT-TRAINING-PLAN, Sessions 1–4]
    A network has learnable weights + a next-token loss (prerequisite) ← CHECK  [NOT CONFIRMED]
    Matrix×vector as a "lens"; slope/direction intuition (prerequisite) ← CHECK  [NOT CONFIRMED]
  rests on:
    P1 Learned projections (principle) → SG-2
      led to:
        P3 Gradient = blame (principle) → SG-4        [the training mechanism]
          led to:
            P2 Symmetry breaking (principle) → SG-3   [needs P1 + P3]
              led to:
                P4 Positional differentiation (principle) → SG-5   [needs P1, P3]
                  led to:
                    P5 Emergent roles (principle) → SG-6
```

**Key-Concept trace (every dependency maps to a graph edge):**
- SG-7 → P4 (SG-5)
- SG-8 → P3 (SG-4) + P4 (SG-5)
- SG-9 → P4 (SG-5)
- SG-10 → P2 (SG-3) + P4 (SG-5)
- SG-11 → P5 (SG-6)
- SG-12 → P5 (SG-6)
- SG-13 → P1–P5 (SG-2 … SG-6)

### ⚠ Prerequisite Warnings
- **Forward pass of attention** (scores → softmax → weighted blend of Values) is assumed known. It is *not* re-taught here — this plan is exclusively about *emergence*. It is fully covered by the companion `TTT-TRAINING-PLAN.md` (Sessions 1–4) in the same repo; run those first if the forward pass is shaky.
- **Learnable weights + a next-token loss** and **slope/direction intuition** are unconfirmed in the learner profile (which covers Quantum Computing). Open SG-2/SG-4 with a 2-minute "a neural net is number-knobs tuned to cut mistakes" primer.
- These are *conceptual* prerequisites only; no calculus is required — gradients are taught as "direction + size of a nudge."

## Sequence
Strict dependency order: **SG-1 → SG-2 → SG-4 → SG-3 → SG-5 → SG-6** (note P3 gradient-mechanism precedes P2 symmetry-breaking, since "identical gradients" only makes sense once "gradient" is defined). Then the Key Concepts that apply them: **SG-7 → SG-8 → SG-9 → SG-10 → SG-11**, then the Tool **SG-12**, then Verification **SG-13** last. Suggested single-session flow (≈75 min): principles as a 25-min block, SG-7/SG-8 as the numeric core (20 min), SG-9/SG-10/SG-11 with the HTML graph (20 min), SG-13 teach-back (10 min). The HTML artefact (`emergence-of-qkv.html`) supports SG-5, SG-7, SG-11, and SG-13.

## Session Blueprints

### SG-1: Nobody Assigns the Roles (Motivation)
- **Initial Test:** A colleague says, "So the engineers decided that this matrix is the *query* and that one is the *key*, right?" You have to correct them. In 3 sentences, explain what is actually true and why the mistaken picture is tempting.
- **Pass Criteria:** States that the three matrices start interchangeable and *become* query/key/value through training; names the tempting-but-wrong idea (hand-assignment). ≥2 of 2 ideas.
- **Estimated Depth:** introductory
- **Principle:** —
- **Exercise:** Write the single sentence you'd put on a slide to capture "roles are emergent, not designed." Compare it to: *"Nobody teaches attention what to pay attention to — it's a side effect of being graded on predicting the next word."* (5 min.)
- **Anticipated CTQs:**
  | CTQ | Source | Mastery Test | Common Failure Mode |
  |-----|--------|-------------|---------------------|
  | Roles are emergent, not assigned | Motivation | Learner denies hand-design | [overgeneralization]: "engineers programmed the roles" |
  | Emergence is driven by one objective | Motivation | Learner names next-token loss | [missing-prerequisite]: no notion of a training objective |
- **Teach Topics:** The surprise of emergence; one objective, many behaviors; framing for the rest of the plan. Pitfall — [overgeneralization]: attributing design intent to learned structure.
- **Final Test:** A product exec asks, "If we don't like how a head behaves, can we just re-label the query matrix?" Explain why that misunderstands where the behavior comes from. Pass = ties behavior to trained weights + objective, not labels.

### SG-2: Q/K/V Are Learned, Not Designed (Core Principle)
- **Principle:** P1 — Learned projections: Q, K, V are three learned matrices applied to the same token; no role is hand-assigned.
- **Worked Example (foundational):**
  **Given:** a toy word vector x = [1, 0] and three *randomly initialized* matrices.
  **Step 1:** $W_Q=\begin{bmatrix}0.9&0.1\\0.2&0.8\end{bmatrix}$ → Q = x·$W_Q$ = [0.9, 0.1].
  > **Why:** Q is the word seen through the "query lens" — the *matrix* does the shaping, not the word.
  **Step 2:** $W_K=\begin{bmatrix}0.3&0.7\\0.6&0.4\end{bmatrix}$ → K = [0.3, 0.7]; $W_V=\begin{bmatrix}0.5&0.5\\0.1&0.9\end{bmatrix}$ → V = [0.5, 0.5].
  > **Why:** Same word, three different vectors — purely because the three matrices differ.
  **Result:** Q/K/V are not the word; they're three learned *lenses*. Nothing labels one "the query" — the numbers in the matrices are what training adjusts.
- **Initial Test:** *(Open with a 2-min "a neural net is number-knobs tuned to cut mistakes" primer.)* In your own words: where do Q, K, and V come from, and what part is actually "learned"?
- **Pass Criteria:** Can state the principle in own words AND say Q/K/V are produced by three separate learned matrices, and that the *matrices* are the learned part.
- **Estimated Depth:** introductory
- **Exercise:** Given x = [2, 1] and $W_Q=\begin{bmatrix}1&0\\0&0\end{bmatrix}$, compute Q. Then change the bottom-right entry to 1 and recompute. One sentence on what the matrix "chose" to keep. (5 min.)
- **Anticipated CTQs:**
  | CTQ | Source | Mastery Test | Common Failure Mode |
  |-----|--------|-------------|---------------------|
  | Q/K/V are outputs of learned matrices | P1 | Learner names the matrices as the learned part | [conflation]: Q/K/V are fixed features of the word |
  | Roles emerge; not imposed | P1 | Learner says training sets the numbers | [overgeneralization]: "query = intent was programmed" |
- **Teach Topics:** Three matrices; the "lens" metaphor; embedding vs. projection. Pitfall — [conflation]: the word vector confused with its Q/K/V projections.
- **Final Test:** Explain why two separately trained models could grow *different* Q/K/V matrices for the same words. Pass = ties it to random start + data, not fixed rules.

### SG-3: Identical Twins Never Differentiate (Core Principle)
- **Principle:** P2 — Symmetry breaking: identical parameters get identical gradients and never differentiate; different random starts are required.
- **Worked Example (foundational):**
  **Given:** two scalar weights $w_q = w_k = 0.5$ that, by the update rule, always receive the *same* gradient g each step (η = 0.1).
  **Step 1:** Step 1 update: both become $0.5 - 0.1g$. Still equal.
  > **Why:** The update is deterministic — same value in, same gradient, same value out.
  **Step 2:** Repeat 1000 steps: still identical. Now restart with $w_q = 0.5,\ w_k = 0.7$.
  > **Why:** Different starting values → the gradient each sees now differs (it depends on the *other*) → they drift apart.
  **Result:** Sameness is a trap: identical init locks the two together forever. Random, *different* init is what lets query and key ever become different things.
- **Initial Test:** An engineer sets $W_Q$ and $W_K$ to exactly the same values to "keep things clean," then trains. Predict what the two matrices look like after training, and why.
- **Pass Criteria:** Can state the principle in own words AND predict they stay identical (no specialization), citing identical gradients from identical values.
- **Estimated Depth:** introductory
- **Exercise:** Two weights start at 0.5 and always get the same gradient +1 (η=0.1). Write their values after 3 steps. Then change one start to 0.6 and describe qualitatively what changes. (5 min.)
- **Anticipated CTQs:**
  | CTQ | Source | Mastery Test | Common Failure Mode |
  |-----|--------|-------------|---------------------|
  | Identical value → identical gradient → stays identical | P2 | Learner traces the deterministic update | [missing-prerequisite]: doesn't see the update is deterministic |
  | Random init is necessary, not cosmetic | P2 | Learner calls different starts a requirement | [conflation]: init randomness = dropout/other noise |
- **Teach Topics:** Symmetry-breaking; the classic "all-zeros / same-seed" bug; randomness as a feature. Pitfall — [conflation]: symmetry-break randomness vs. data shuffling.
- **Final Test:** A colleague seeds all three matrices identically and is puzzled they never specialize after a week of training. Explain the mechanism. Pass = deterministic identical gradients keep them locked.

### SG-4: Gradient Descent Nudges Each Weight (Core Principle)
- **Principle:** P3 — Gradient = blame: each weight is nudged *opposite* its gradient, by an amount proportional to its contribution to the error.
- **Worked Example (foundational):**
  **Given:** one weight w = 0.5. If we raise w a little, the error goes *up* → gradient ∂L/∂w = +2. Learning rate η = 0.1.
  **Step 1:** Sign +2 means "increasing w increases error."
  > **Why:** The gradient is the slope of error-vs-weight; it points *uphill* on the mistake.
  **Step 2:** Move opposite: w ← 0.5 − 0.1×2 = **0.3**.
  > **Why:** Walk downhill; step size scales with the gradient — bigger blame, bigger nudge.
  **Result:** w = 0.3, error slightly lower. Repeat over all weights, millions of times → learning.
- **Initial Test:** A weight has gradient ∂L/∂w = −5, η = 0.1. Which direction and how far does it move, and why?
- **Pass Criteria:** Can state the principle in own words AND compute w ← w + 0.5 (opposite the gradient) AND explain "downhill, size ∝ blame."
- **Estimated Depth:** introductory
- **Exercise:** Two weights have gradients +1 and +10 at η = 0.1. Which moves more, and what does that say about their blame for the current error? (5 min.)
- **Anticipated CTQs:**
  | CTQ | Source | Mastery Test | Common Failure Mode |
  |-----|--------|-------------|---------------------|
  | Weights move opposite the gradient | P3 | Learner subtracts, not adds | [procedural-without-conceptual]: sign flipped |
  | Step size ∝ contribution to error | P3 | Learner predicts bigger-gradient moves more | [overgeneralization]: all weights change equally |
- **Teach Topics:** Loss as a landscape; gradient as steepest-uphill; learning rate as step size. Pitfall — [formal-without-intuitive]: memorizing the rule without the downhill picture.
- **Final Test:** If a weight's gradient ≈ 0 this step, what happens to it and why? Pass = "barely moves — not contributing to the current mistake."

### SG-5: Different Positions → Different Gradients (Core Principle)
- **Principle:** P4 — Positional differentiation: Q, K, V get different gradients because they sit at different points in the computation, so they specialize.
- **Worked Example (foundational):**
  **Given:** a single score s = Q·K with Q = 3, K = 4. Training wants s *bigger* to cut error → ∂L/∂s = −1.
  **Step 1:** Gradient to Q = ∂L/∂s × K = −1 × 4 = **−4**.
  > **Why:** Q enters the score multiplied by K, so K *scales* Q's blame.
  **Step 2:** Gradient to K = ∂L/∂s × Q = −1 × 3 = **−3**.
  > **Why:** Same-shaped formula, but K's blame is scaled by Q (= 3) — a different number.
  **Step 3:** V is not in the score; its gradient flows through the output blend (o = a·V), a different path.
  > **Why:** Different position → different gradient in *form*, not just value.
  **Result:** Q moves −4, K moves −3, V moves by something unrelated → the three drift apart and specialize.
- **Initial Test:** In s = Q·K with Q = 2, K = 5 and ∂L/∂s = +1, compute the gradient to Q and to K. Why aren't they equal?
- **Pass Criteria:** Can state the principle in own words AND compute grad_Q = 5, grad_K = 2 (each = ∂L/∂s × the *other's* value) AND explain the asymmetry.
- **Estimated Depth:** introductory
- **Exercise:** Keep ∂L/∂s = 1 but set Q = 10, K = 1. Compute both gradients; say which gets the bigger nudge and what that does over time. (5 min.)
- **Anticipated CTQs:**
  | CTQ | Source | Mastery Test | Common Failure Mode |
  |-----|--------|-------------|---------------------|
  | Q-grad carries K; K-grad carries Q | P4 | Learner scales each by the other | [conflation]: symmetric formula ⇒ same gradient |
  | V's gradient is a different path | P4 | Learner separates V (output) from Q/K (score) | [missing-prerequisite]: assumes all trained alike |
- **Teach Topics:** Bilinear Q·K vs. linear V-in-output; "symmetric shape, asymmetric numbers." Pitfall — [conflation]: symmetry of form vs. symmetry of outcome.
- **Final Test:** Explain why Q and K don't collapse into one matrix even though Q·K = K·Q. Pass = different gradient values (each scaled by the other) + different starts.

### SG-6: Roles Are a Side Effect of the Loss (Core Principle)
- **Principle:** P5 — Emergent roles: "query/key/value" meaning is a side effect of minimizing next-token loss, discovered by the optimizer, not specified.
- **Worked Example (foundational):**
  **Given:** a tiny task with two "sentences." In sentence A, word 1 must attend to word 2; in sentence B, word 2 must attend to word 1 (opposite directions).
  **Step 1:** A single shared matrix (Q = K) can only make symmetric matches — it can't prefer 1→2 without also making 2→1.
  > **Why:** With Q = K, the score for (1 looks at 2) equals the score for (2 looks at 1).
  **Step 2:** To lower the loss on *both* sentences, the optimizer is forced to make $W_Q \neq W_K$ — a "looking" lens distinct from an "advertising" lens.
  > **Why:** Only distinct Q and K can express *direction*, which the task rewards.
  **Result:** The query and key *roles* were never assigned — they appeared because they are the arrangement that minimizes the loss. Emergence = the optimizer's solution.
- **Initial Test:** In one paragraph, explain to a skeptic what "the roles emerge" actually means, using the idea that a single objective *forces* useful structure.
- **Pass Criteria:** Can state the principle in own words AND explain that distinct roles appear because they minimize the loss (not because they were designed).
- **Estimated Depth:** introductory
- **Exercise:** Name one real relationship a head might need to be *directional* about (e.g., verb→subject, pronoun→antecedent), and say why a symmetric matcher would fail it. (5 min.)
- **Anticipated CTQs:**
  | CTQ | Source | Mastery Test | Common Failure Mode |
  |-----|--------|-------------|---------------------|
  | Roles = the loss-minimizing arrangement | P5 | Learner ties roles to the objective | [overgeneralization]: "roles are arbitrary" |
  | The optimizer discovers, doesn't receive, the roles | P5 | Learner denies external assignment | [conflation]: emergence = randomness |
- **Teach Topics:** Emergence as constrained optimization; directionality as the thing that forces distinctness; "pressure creates structure." Pitfall — [conflation]: emergent ≠ random/uncontrolled.
- **Final Test:** Explain why, across many trained models, heads reliably specialize into *similar* jobs even though nobody coordinates them. Pass = same objective + same data pressures → convergent solutions.

### SG-7: Why Q's Gradient Carries K (Key Concept)
- **Initial Test:** Q and K both feed the score via Q·K, yet they don't end up identical. In plain terms, give the *gradient reason* — what is Q's nudge scaled by, and what is K's scaled by?
- **Pass Criteria:** States Q's gradient ∝ K and K's gradient ∝ Q, and that because Q ≠ K the two nudges differ, so they diverge. Both halves.
- **Estimated Depth:** intermediate
- **Principle:** P4
- **Exercise:** With ∂L/∂s = 2, Q = [1, 3], K = [2, 1] (elementwise for intuition), compute the nudge Q gets (∝ K) and the nudge K gets (∝ Q). Which entry of each moves most? (5–10 min.)
- **Anticipated CTQs:**
  | CTQ | Source | Mastery Test | Common Failure Mode |
  |-----|--------|-------------|---------------------|
  | Q-grad ∝ K, K-grad ∝ Q | P4 | Learner writes each gradient via the other | [conflation]: symmetric algebra ⇒ symmetric gradient |
  | Distinct gradients drive distinct specialization | P4 | Learner links gradient gap to role gap | [verbal-without-formal]: knows they differ, not why |
- **Teach Topics:** "Each wears the other's coat in its gradient"; why swapping the query/key labels at init still works (labels are arbitrary). Pitfall — [conflation]: Q·K = K·Q mistaken for equal gradients.
- **Final Test:** If you *swapped* the query and key labels at initialization, would training still succeed? Explain via the gradient structure. Pass = "yes — they just need to be distinct and each gets its own gradient."

### SG-8: Trace One Training Step (Key Concept)
- **Initial Test:** Toy setup: input fixed, Q = 3, K = 4, target score T = 20, current s = Q·K = 12, loss L = ½(s−T)², η = 0.01. Compute ∂L/∂s, the gradient to Q and to K, and the updated Q and K after one step. State whether Q and K are now different.
- **Pass Criteria:** ∂L/∂s = s−T = −8; grad_Q = −8×4 = −32; grad_K = −8×3 = −24; Q ← 3 − 0.01×(−32) = 3.32; K ← 4 − 0.01×(−24) = 4.24. ≥4 of 5 values correct and notes Q ≠ K, moving apart.
- **Estimated Depth:** advanced
- **Principle:** P3, P4
- **Exercise:** Redo the step with T = 6 (so s is *too high*). Recompute ∂L/∂s, both gradients, and the updates. Which way do Q and K move now, and why? (5–10 min.)
- **Anticipated CTQs:**
  | CTQ | Source | Mastery Test | Common Failure Mode |
  |-----|--------|-------------|---------------------|
  | ∂L/∂s = s − T | P3 | Learner computes the error signal | [procedural-without-conceptual]: guesses the sign |
  | Chain to each weight uses the other's value | P4 | Learner multiplies by K then by Q | [conflation]: uses the same multiplier for both |
  | Update subtracts η×gradient | P3 | Learner applies the update correctly | [procedural-without-conceptual]: adds the gradient |
- **Teach Topics:** The full forward→loss→backward→update loop on one number; sign discipline; why one step already separates Q and K. Pitfall — [procedural-without-conceptual]: mechanical steps with wrong signs.
- **Final Test:** Same toy, but now K is frozen (not trainable). After one step, has Q still moved? Has the score improved? Explain. Pass = Q still updates (its gradient exists), score improves, but K stays fixed.

### SG-9: V Trains on a Different Path (Key Concept)
- **Initial Test:** Explain why the Value matrix $W_V$ is *not* trained by the same gradient as Q and K — trace, in words, where V's gradient comes from instead.
- **Pass Criteria:** States V never enters the score (Q·K); its gradient flows from the output blend o = a·V, weighted by the attention weights a — a structurally different path. ≥2 of 2 ideas.
- **Estimated Depth:** intermediate
- **Principle:** P4
- **Exercise:** In o = a·V with a = 0.8 (attention weight this word received) and ∂L/∂o = 2, compute the gradient pressure on V. Then set a = 0.05 and recompute — what does low attention do to V's learning signal? (5–10 min.)
- **Anticipated CTQs:**
  | CTQ | Source | Mastery Test | Common Failure Mode |
  |-----|--------|-------------|---------------------|
  | V's gradient ∝ attention weight a | P4 | Learner scales V's update by a | [missing-prerequisite]: lumps V with Q/K |
  | Low attention → weak learning signal for that V | P4 | Learner notes small a → small nudge | [overgeneralization]: "all Values learn equally" |
  | Q/K shape *where* to look; V shapes *what* is delivered | P4 | Learner splits the two jobs | [conflation]: merges routing and content |
- **Teach Topics:** Two circuits — the routing circuit (Q, K) and the content circuit (V); why V only learns where it gets attended. Pitfall — [conflation]: treating V like another key.
- **Final Test:** A word is almost never attended to during training. What happens to *its* Value representation and why? Pass = it gets little gradient, so its V is poorly shaped.

### SG-10: What Breaks If You Tie or Remove a Projection (Key Concept)
- **Initial Test:** To save parameters a team sets $W_Q = W_K$ (shared). What capability is lost, and why? *(Hint: what can Q·K express when Q and K are the same matrix?)*
- **Pass Criteria:** Recognizes tying forces *symmetric* attention (A→B equals B→A), losing *directional* relationships; gives a case needing asymmetry (pronoun→antecedent). 
- **Estimated Depth:** intermediate
- **Principle:** P2, P4
- **Exercise:** Give one sentence where A should attend to B far more than B attends to A, and explain why a shared Q=K matrix cannot represent that direction. (5–10 min.)
- **Anticipated CTQs:**
  | CTQ | Source | Mastery Test | Common Failure Mode |
  |-----|--------|-------------|---------------------|
  | Separate Q, K enable directional attention | P4 | Learner gives an asymmetric example | [conflation]: assumes attention is symmetric |
  | Removing V leaves nothing to deliver | P4 | Learner notes V carries content | [missing-prerequisite]: forgets V's job |
  | Fewer parameters isn't free | P2 | Learner names the lost capability | [overgeneralization]: "sharing is harmless" |
- **Teach Topics:** Ablation intuition; directional vs. symmetric similarity; each matrix earns its parameters. Pitfall — [conflation]: assuming the attention weight matrix is symmetric.
- **Final Test:** A team removes $W_V$ and feeds raw embeddings as Values. What still works, what degrades? Pass = scores still route, but the model loses learned control of delivered content.

### SG-11: Read a Specialization Graph (Key Concept)
- **Initial Test:** Using `emergence-of-qkv.html`, look at the divergence chart. Two curves start together: one is "different random init," one is "identical init." Say which curve rises, which stays flat, and what each proves about emergence.
- **Pass Criteria:** Correctly identifies the different-init curve as rising (Q and K specialize) and the identical-init curve as flat (symmetry never breaks), and states the takeaway that specialization requires broken symmetry. 
- **Estimated Depth:** intermediate
- **Principle:** P5
- **Exercise:** In the HTML, drag the learning-rate slider up and down and describe how the divergence curve changes shape (speed of specialization). One sentence on what a too-high rate does. (5–10 min.)
- **Anticipated CTQs:**
  | CTQ | Source | Mastery Test | Common Failure Mode |
  |-----|--------|-------------|---------------------|
  | Rising curve = growing role difference | P5 | Learner reads the axis meaning | [verbal-without-formal]: "the line goes up" with no meaning |
  | Flat curve = symmetry never broke | P2, P5 | Learner ties flat to identical init | [conflation]: flat = "training failed generally" |
  | The graph shows emergence, not proof of meaning | P5 | Learner states one thing it does NOT prove | [overgeneralization]: "the graph proves the head learned grammar" |
- **Teach Topics:** Reading a training-dynamics chart; divergence/cosine-distance as a specialization proxy; what a metric can and cannot claim. Pitfall — [overgeneralization]: over-reading a curve as semantic proof.
- **Final Test:** Given a divergence curve that rises then *plateaus*, interpret the plateau. Pass = the roles have settled into a stable specialization (the loss stopped pushing them apart).

### SG-12: Probe Whether a Head Specialized (Tools)
- **Initial Test:** You suspect a particular attention head does "pronoun → antecedent." Without reading any weights, describe a concrete test using inputs and attention maps that would give evidence for or against it.
- **Pass Criteria:** Proposes an input-driven probe (e.g., minimal sentence pairs where the antecedent flips) AND names what pattern in the attention map would confirm/deny — with a caveat that it's evidence, not proof. 
- **Estimated Depth:** intermediate
- **Principle:** P5
- **Exercise:** Design one minimal pair (two sentences differing in one word that flips the referent) and state the attention pattern you'd expect if the head really tracks antecedents. (5–10 min.)
- **Anticipated CTQs:**
  | CTQ | Source | Mastery Test | Common Failure Mode |
  |-----|--------|-------------|---------------------|
  | Behavior is probed by inputs, not decreed | P5 | Learner uses controlled inputs | [procedural-without-conceptual]: inspects raw weights hoping for a label |
  | Evidence ≠ proof of a clean role | P5 | Learner states the caveat | [overgeneralization]: "one example proves the head's job" |
  | Roles can be distributed / polysemantic | P5 | Learner allows a head to do several things | [conflation]: one head = exactly one human concept |
- **Teach Topics:** Minimal-pair probing; attention-map reading; polysemantic heads; the limits of interpretability claims. Pitfall — [overgeneralization]: clean one-head-one-job stories.
- **Final Test:** Your probe shows the "antecedent" head *also* fires on subject–verb links. What does that tell you about emergent roles? Pass = roles are emergent and need not match tidy human categories.

### SG-13: Teach the Emergence Story (Verification)
- **Initial Test:** In under 5 minutes, using `emergence-of-qkv.html` (the worked example and the divergence graph), teach a non-technical colleague *why* Q/K/V roles emerge: start random → gradients differ by position → symmetry breaks → roles settle as the loss-minimizing arrangement.
- **Pass Criteria:** Covers P1–P5 in order, uses the numeric example (Q=3,K=4 → grads −4,−3) and the graph (rising vs. flat curve), no role confusion, pitched intuitively. ≥5 of 5 principles present and correctly linked.
- **Estimated Depth:** advanced
- **Principle:** P1–P5
- **Exercise:** Sketch a 4-box story diagram: *random start → different gradients → symmetry breaks → roles emerge*, one caption each, and mark where V's separate path sits. (5–10 min.)
- **Anticipated CTQs:**
  | CTQ | Source | Mastery Test | Common Failure Mode |
  |-----|--------|-------------|---------------------|
  | Emergence is a causal chain, not a slogan | P1–P5 | Learner sequences the four causes | [verbal-without-formal]: "they just emerge" |
  | The numeric example grounds the claim | P4 | Learner shows −4 vs −3 concretely | [formal-without-intuitive]: abstract only |
  | The graph illustrates, does not prove semantics | P5 | Learner adds the caveat | [overgeneralization]: graph = semantic proof |
- **Teach Topics:** Weaving example + graph into one narrative; teaching as the mastery test (Feynman). Pitfall — [formal-without-intuitive]: reciting gradients without the "so what."
- **Final Test:** Re-teach on a fresh framing and answer: "If nobody assigned the roles, why do different models learn the *same* roles?" Pass = full causal chain + convergence-under-shared-pressure answer.

## Progress Log
(updated by /run-session)
