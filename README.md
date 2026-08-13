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
- **[emergence-of-qkv.html](emergence-of-qkv.html)** — a self-contained interactive artefact: a live gradient widget (`∂L/∂Q ∝ K`, `∂L/∂K ∝ Q`), a forward/backward computation graph, and a **runnable training-dynamics chart** built on a real 2-token gradient descent. Watch the query and key lenses diverge on a *directional* task while staying identical on a *symmetric* one.
  → **[View it live](https://raw.githack.com/Antonio-Ardigo/Attention-Mechanism/main/emergence-of-qkv.html)** (rendered via raw.githack; GitHub serves raw `.html` as plain text).

## Who it's for

Product managers, analysts, designers, executives, and engineers new to ML. No prerequisites.

## Format

4 × 60–75 minute sessions, or one half-day workshop. Each session includes a talk track, a group activity, a check for understanding, and facilitator notes on the misconceptions that come up.
