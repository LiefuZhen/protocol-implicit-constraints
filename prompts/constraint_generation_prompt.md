# Constraint Generation Prompt

You are generating candidate implicit constraints for a target protocol standard.

Inputs:

- target protocol standard excerpts;
- entity index, if available;
- reviewed or seed constraint-generation directions;
- protocol goals and relevant messages/fields/states.

Process:

1. Locate suspicious standard positions: boundary silence, cross-reference conflict, ambiguous capability scope, and purpose-mechanism gaps.
2. For each position, identify the matching generation direction.
3. Generate a concrete candidate implicit constraint.
4. Bind the constraint to an explicit protocol goal.
5. Assign strength:
   - `L1`: logically necessary for the bound protocol goal;
   - `L2`: convention or best practice, not enough by itself for defect judgment.
6. Record `spec_ref`, `statement`, `condition`, `expected_behavior`, and `violation_pattern`.

Do not claim a candidate is a confirmed bug. Candidate constraints require independent review and implementation validation.
