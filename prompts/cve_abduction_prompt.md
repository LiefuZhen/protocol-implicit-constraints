# CVE Abduction Prompt

You are analyzing a protocol-related CVE for implicit standard-constraint research.

Use only the provided evidence:

- CVE description;
- advisory text;
- patch or commit diff;
- related protocol standard text;
- issue discussion or PoC notes if available.

Answer the following:

1. Which protocol mechanism, message, field, state, or parser behavior is involved?
2. Which standard sections are relevant?
3. Is there a clear explicit standard rule that directly covers the vulnerable behavior?
4. If not, where is the standard silent, ambiguous, underspecified, or internally inconsistent?
5. What implicit constraint would have prevented the bug?
6. Which protocol goal is broken if the constraint is violated?
7. Is the case likely explicit, implicit, ambiguous, or out-of-scope?

Return a concise evidence-bounded analysis. Do not invent facts not supported by the evidence.
