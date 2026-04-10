# MECHANIZED_THEOREM_MAP

This file maps the current mechanized kernel to the existing theorem family and law surfaces.

| Kernel ID | Mechanized kernel theorem | Primary law sources | Theorem-set relation | Mechanized witness |
|---|---|---|---|---|
| K1 | Verdict universe / totality core | `SPEC/PRIMITIVE_LAW.md`, `SPEC/ADMISSION_SEMANTICS.md` | `T1`, `T-AD-1`, `T-IMP-1` | `mechanized_kernel/checker.py` exhaustive state-space |
| K2 | Verification necessity core | `SPEC/VERIFICATION_LAW.md`, `SPEC/ADMISSION_SEMANTICS.md` | `T5`, `T-VF-3`, `T-IMP-2` | `mechanized_kernel/checker.py` exhaustive state-space |
| K3 | Fail-closed core | `SPEC/PRIMITIVE_LAW.md`, `SPEC/ADMISSION_SEMANTICS.md`, `SPEC/REFUSAL_ALGEBRA.md` | `T2`, `T-FC-1..T-FC-6` core witness subset | `mechanized_kernel/checker.py` exhaustive state-space |
| K4 | Admission biconditional core | `SPEC/ADMISSION_SEMANTICS.md` | `T-AD-2`, `T-AD-3`, `T-AD-4` core witness subset | `mechanized_kernel/checker.py` exhaustive state-space |
| K5 | No-bypass core | `SPEC/PRIMITIVE_LAW.md`, `SPEC/PERMIT_ALGEBRA.md`, `SPEC/SPEC/PRIMITIVE_EQUIVALENCE.md` | `T-NB-1..T-NB-5` core witness subset | `mechanized_kernel/checker.py` exhaustive state-space |
| K6 | Canonicalization determinism/idempotence subset core | `SPEC/CANONICALIZATION_LAW.md` | `T-C14N-1`, `T-C14N-2`, `T-C14N-7`, subset witness for `T-C14N-8` | `mechanized_kernel/checker.py` + canonicalization corpus |

Exactness note: the current map is intentionally a kernel map. It does not imply whole-family mechanization of each theorem family.
