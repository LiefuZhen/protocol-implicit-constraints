# Direction Generation Prompt

You are abstracting reusable constraint-generation directions from reviewed CVE abduction records.

Given a set of CVE abduction records, cluster them by:

- the shape of the standard defect;
- where the analyst should look in a standard;
- how an implicit constraint can be inferred.

Do not cluster primarily by vulnerability impact, CWE, implementation language, or affected project.

For each proposed direction, produce:

- `direction_id`;
- `direction_name`;
- standard-defect shape;
- where to look in a new standard;
- reverse-inference rule;
- example CVE records that motivated it;
- boundary with nearby directions;
- review risks.

Mark the output as a candidate direction set requiring human review.
