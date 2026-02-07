# Confidence Protocol

**Purpose:** Ensure every output includes explicit, honest confidence scoring with reasoning.

---

## Confidence Scale

| Score | Label | Evidence Basis |
|---|---|---|
| 9-10 | **Certain** | Multiple reliable sources agree, directly verified |
| 7-8 | **High** | Strong evidence from credible sources |
| 5-6 | **Moderate** | Evidence exists but limited or conflicting |
| 3-4 | **Low** | Mostly inference, limited direct evidence |
| 1-2 | **Speculative** | Pattern-based speculation, minimal support |

---

## Rules

1. **Never claim 9-10** without direct verification from source material
2. **Drop 2 points** for each unverified assumption in the chain
3. **Aggregate confidence** = minimum component confidence (weakest link)
4. **Always explain reasoning** for the score — never just state a number
5. **Distinguish** between "I verified this" and "I believe this"

---

## Output Format

```
CONFIDENCE: [1-10]
REASONING: [Why this score — what evidence supports it]
CAVEATS: [What could be wrong — known risks]
VERIFY: [What to check to increase confidence]
```

---

## Application

The Confidence Protocol applies to:

- **Problem classification** — How sure are we about the category?
- **Research findings** — How reliable is each finding?
- **Implementation decisions** — How confident in the approach?
- **Verification results** — How thorough was the check?
- **Documentation claims** — How accurate is each statement?

---

## Confidence Aggregation

When combining multiple components:

```
Overall Confidence = min(component_1, component_2, ..., component_n)
```

A chain is only as strong as its weakest link. If one component has confidence 4 and another has confidence 9, the aggregate is 4.

---

*Part of the FORGE Framework — https://github.com/0xPliny/forge-framework*
