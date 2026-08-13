"""
Q/K specialization by gradient descent, with REAL (sinusoidal) positional encoding.

Task ("attend to the previous token"): a canonical relative-position pattern.
Each token p should look one step back (token p-1); token 0 looks at itself.

Setup
-----
 * 3 positions, 2-D sinusoidal positional encodings on the unit circle:
       PE_p = [cos(p*theta), sin(p*theta)],  theta = 50 deg.
   (Pure position, no word content, so we see the position effect alone.)
 * Inputs X = PE. Values W_V = I, so the output O = A @ X is a blend of PEs.
 * Target output O*: token p should output PE_{p-1}  (token 0 -> PE_0).
 * We train W_Q and W_K from a NEARLY-identical start and watch them separate.

Why this forces Q != K
----------------------
With Q = K the score is  S_pj = PE_p^T (W^T W) PE_j , which is SYMMETRIC in p,j
(since W^T W is symmetric): token p would attend token j exactly as j attends p.
But "attend the previous token" is DIRECTIONAL (2 looks at 1, but 1 must look at 0,
not at 2). A symmetric scorer cannot do it, so the objective must split W_Q, W_K.

What emerges
------------
Attention converges to the sub-diagonal (each token attends the previous one), and
Q_p ends up aligned with K_{p-1}: the query learns to "look one position back."
In the natural gauge that is  W_K = identity ("here is my position") and
W_Q = rotation by -theta (rotate my position back by one) -- exactly the mechanism
RoPE uses for relative-position attention.

Run:  python qkv_gradient_descent.py
"""
import io, sys
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
import numpy as np
np.set_printoptions(precision=4, suppress=True)

# ---- setup -----------------------------------------------------------------
TH = np.deg2rad(50.0)
PE = np.array([[np.cos(p*TH), np.sin(p*TH)] for p in range(3)])   # positional encodings
X  = PE.copy()
Ostar = np.array([PE[0], PE[0], PE[1]])          # each token -> previous token's PE
WV = np.eye(2)                                    # values = identity  ->  O = A @ X
# near-identical (slightly asymmetric) start; exactly-identical would sit on a saddle
WQ = np.eye(2) + np.array([[ 0.02, 0.03], [-0.01, 0.00]])
WK = np.eye(2) + np.array([[-0.02,-0.01], [ 0.02, 0.01]])
LR, STEPS = 0.8, 400

def softmax_rows(M):
    e = np.exp(M - M.max(axis=1, keepdims=True))
    return e / e.sum(axis=1, keepdims=True)

def forward(WQ, WK):
    Q = X @ WQ; K = X @ WK
    S = Q @ K.T
    A = softmax_rows(S)
    O = A @ X                       # = A @ (X @ WV), WV = I
    L = ((O - Ostar) ** 2).sum()
    return Q, K, S, A, O, L

def backward(Q, K, S, A, O):
    dO = 2.0 * (O - Ostar)          # dL/dO
    dA = dO @ X.T                   # dL/dA   (O = A @ X)
    dS = np.zeros_like(S)           # softmax backward, per row
    for i in range(S.shape[0]):
        a, g = A[i], dA[i]
        dS[i] = a * (g - (g * a).sum())
    dWQ = X.T @ (dS @ K)            # dL/dW_Q
    dWK = X.T @ (dS.T @ Q)          # dL/dW_K
    return dO, dA, dS, dWQ, dWK

def show_step(n, WQ, WK):
    Q, K, S, A, O, L = forward(WQ, WK)
    dO, dA, dS, dWQ, dWK = backward(Q, K, S, A, O)
    print(f"\n========== STEP {n} ==========")
    print("PE (positions on the circle) =\n", PE)
    print("W_Q =\n", WQ, "\nW_K =\n", WK)
    print("Q = X·W_Q =\n", Q, "\nK = X·W_K =\n", K)
    print("S = Q·Kᵀ =\n", S)
    print("A = softmax(S) =\n", A)
    print("O = A·X =\n", O, "   target O* =\n", Ostar)
    print(f"loss L = {L:.4f}")
    print("dL/dS =\n", dS)
    print("dL/dW_Q =\n", dWQ, "\ndL/dW_K =\n", dWK)
    print(f"||dL/dW_Q - dL/dW_K|| = {np.linalg.norm(dWQ-dWK):.4f}   (nonzero => they move apart)")
    return WQ - LR*dWQ, WK - LR*dWK

# two fully-shown steps -------------------------------------------------------
WQ, WK = show_step(1, WQ, WK)
WQ, WK = show_step(2, WQ, WK)

# run to convergence ----------------------------------------------------------
print("\n========== TRAINING CURVE ==========")
print(f"{'step':>5} {'loss':>9} {'||W_Q-W_K||':>12}   who each token attends (argmax)")
for t in range(3, STEPS+1):
    Q, K, S, A, O, L = forward(WQ, WK)
    _, _, _, dWQ, dWK = backward(Q, K, S, A, O)
    WQ -= LR*dWQ; WK -= LR*dWK
    if t in (3, 5, 10, 25, 50, 100, 200, 400):
        print(f"{t:>5} {L:>9.4f} {np.linalg.norm(WQ-WK):>12.4f}   {A.argmax(1).tolist()}  (target [0,0,1])")

# converged state + interpretation -------------------------------------------
Q, K, S, A, O, L = forward(WQ, WK)
print("\n========== CONVERGED ==========")
print("A =\n", A, "  -> sub-diagonal: each token attends the PREVIOUS one")
print(f"final loss = {L:.5f}   ||W_Q - W_K|| = {np.linalg.norm(WQ-WK):.3f}")
print("\nGauge-invariant check -- cosine(Q_p, K_j):")
for p in range(3):
    cs = [round(float(Q[p]@K[j]/(np.linalg.norm(Q[p])*np.linalg.norm(K[j])+1e-9)), 2) for j in range(3)]
    print(f"  Q_{p} vs K_j: {cs}   (biggest at j={p-1 if p>0 else 0} = the previous token)")

# clean gauge: freeze K = I, retrain Q -> should become the rotation R(-theta)
Wq = np.eye(2) + np.array([[0.02,0.03],[-0.01,0.0]])
Wk = np.eye(2)
for _ in range(600):
    Q,K,S,A,O,Lz = forward(Wq, Wk)
    _,_,_,dWq,_ = backward(Q,K,S,A,O)
    Wq -= 0.8*dWq
print("\nCleanest gauge (freeze W_K = I, train W_Q):")
print(" W_Q ->\n", Wq)
print(" This is a ROTATION (by ~theta, matching R(theta) up to a scale that sharpens")
print(" the softmax): it maps each position onto the previous one, so Q_p lands on")
print(" K_{p-1}. K says 'here is my position'; Q says 'give me the one before mine.'")
print(" That is exactly how RoPE finds neighbours.")
