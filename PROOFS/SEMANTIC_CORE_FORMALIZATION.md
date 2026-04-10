# SEMANTIC_CORE_FORMALIZATION

This file formalizes the abstract semantic kernel used by the current mechanized-kernel pass.

## Abstract state

A kernel state is a total Boolean tuple:

`S = (p, b, m, v, r, sh, bd, c, a, w, f, op)`

where:
- `p` = primitive valid
- `b` = bundle valid
- `m` = manifest satisfied
- `v` = verification succeeded
- `r` = request valid
- `sh` = shape satisfied
- `bd` = bounds satisfied
- `c` = contract satisfied
- `a` = action binding satisfied
- `w` = witness satisfied
- `f` = no fail-closed trigger
- `op` = official positive path

## Admission reducer

`Admit(S) = ALLOW` iff:

`p ∧ b ∧ m ∧ v ∧ r ∧ sh ∧ bd ∧ c ∧ a ∧ w ∧ f ∧ op`

otherwise:

`Admit(S) = REFUSAL`

## Verification reducer

`Verify(S) = VERIFIED` iff:

`p ∧ b ∧ m ∧ v ∧ f`

otherwise:

`Verify(S) = NOT_VERIFIED`

## Permit possibility reducer

`PermitPossible(S)` iff:

`Admit(S) = ALLOW ∧ op`

## Mechanized finite domain

The checker exhaustively enumerates all `2^12 = 4096` states of the abstract kernel.

## Canonicalization subset

The checker separately evaluates a concrete canonicalization subset over:
- two semantically equal request fixtures
- one semantically distinct request fixture

and checks:
- equal-pair byte equality
- equal-pair digest equality
- distinct-pair byte inequality
- idempotence on canonicalized output

## Exact limit

This formalization is a mechanized semantic kernel used for preparation and partial discharge. It is not a full mechanization of every theorem family or every implementation surface.
