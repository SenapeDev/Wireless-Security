SAE is the authentication protocol introduced in WPA3, replacing the Pre-Shared Key (PSK) handshake used in WPA2. It's based on the **Dragonfly Key Exchange**, a variant of Diffie-Hellman that adds mutual authentication.

## SAE glossary
- **Password Element (PE):** A point on an elliptic curve derived deterministically from the password and both MAC addresses. Never transmitted. Both sides compute it independently.
- **r:** A secret random integer generated fresh every session by each peer. Never transmitted, discarded after the handshake. This is the core ephemeral secret.
- **m:** A random blinding mask, also generated fresh every session. Its only job is to hide `r` in the commit message. Never transmitted.
- **scalar:** The commit value `(r + m) mod order`. Transmitted. Looks random to an observer because `m` is unknown.
- **element:** The commit value `-(m * PE)`. Transmitted. Looks random because `m` is unknown and PE is never revealed.
- **K:** The shared secret both sides independently compute from each other's commit values. Never transmitted. If both sides used the same password, they get the same K.
- **confirm:** An HMAC token proving "I computed the same K as you". Transmitted. This is how both sides verify the handshake succeeded.
- **order:** The size of the elliptic curve group. Scalar arithmetic is done mod this number.

## Step by step, simply

### Setup (not transmitted, done locally)
Both sides independently compute the same PE from public inputs:

```
PE = map_to_curve(password, MAC_client, MAC_ap)
```

### Commit phase (both sides do this simultaneously)
Each side generates fresh random secrets and builds a blinded commit:

```
r = random()
m = random()

scalar  = (r + m) mod order
element = -(m * PE)

send(scalar, element)
```

At this point neither side has proven anything yet. They've only exchanged blinded values.

### Key computation (done locally after receiving peer's commit)
Each side uses its own `r` and the peer's transmitted values to compute K:

```
K = r * (peer_scalar * PE + peer_element)
```

If both used the same password (same PE), the math converges and both get the same K. If passwords differ, K values are different and unrelated.

### Confirm phase
Each side proves it got the same K, without revealing K itself:

```
my_confirm = HMAC(K, my_scalar, peer_scalar, my_element, peer_element)
send(my_confirm)

verify(peer_confirm == HMAC(K, peer_scalar, my_scalar, peer_element, my_element))
```

If both confirms match, authentication is successful.


## Pseudo example
```
-- SETUP (local, never transmitted) --

Alice:  PE = map_to_curve("hunter2", MAC_alice, MAC_bob)  →  point G7
Bob:    PE = map_to_curve("hunter2", MAC_alice, MAC_bob)  →  point G7  (same)


-- COMMIT PHASE --

Alice picks:  r=41, m=17
Alice sends:  scalar_A  = (41+17) mod order  =  58
              element_A = -(17 * G7)          =  point X3

Bob picks:    r=92, m=35
Bob sends:    scalar_B  = (92+35) mod order  =  127
              element_B = -(35 * G7)          =  point X9


-- KEY COMPUTATION (local) --

Alice computes:  K = 41 * (127 * G7 + X9)
Bob computes:    K = 92 * (58  * G7 + X3)

-- both arrive at the same K because the math cancels out --
-- an attacker sees only 58, X3, 127, X9 -- useless without r --


-- CONFIRM PHASE --

Alice sends:  confirm_A = HMAC(K, 58, 127, X3, X9)
Bob sends:    confirm_B = HMAC(K, 127, 58, X9, X3)

Both verify each other's confirm. They match. Done.
```