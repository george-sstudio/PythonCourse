# Exercise 10.2: Rewrite three vague requests as briefs

Each request below is the kind of thing people really type. Rewrite each as a brief using the template in [AI_PLAYBOOK.md §2](../../../AI_PLAYBOOK.md#2-the-brief-template).

Rules for this exercise:

- Use the real course data (see `data/README.md`, or your context card from 10.1).
- **At least three checks per brief**, including one *trap case* that would expose a common mistake.
- Don't write any code. Writing the brief is the exercise.

When you're done, compare with `solutions/ex10_2_briefs_model.md`. Yours can be different and still good. Check whether you caught the same traps.

---

## Request A

> "Find all the cities near rivers."

Things to decide: *how* near? which cities (all 1,251 places, or only big ones)? which rivers (`River` only, or `Lake Centerline` too)? output as what? in which CRS will you measure?

**Your brief:**

```text
## Goal

## Context

## Inputs

## Output

## Rules

## Checks

## How I want the answer
```

---

## Request B

> "Colour the countries by how rich they are."

Things to decide: rich = GDP per person? how many classes, and which method? what happens to `gdp_md = -99`? which palette? saved as a QML?

**Your brief:**

```text
## Goal

## Context

## Inputs

## Output

## Rules

## Checks

## How I want the answer
```

---

## Request C

> "Make a map of the terrain from my DEM."

Things to decide: which products (hillshade, tints, contours)? which CRS for the analysis, and why? contour interval? styling? where do the files go? what proves it worked?

**Your brief:**

```text
## Goal

## Context

## Inputs

## Output

## Rules

## Checks

## How I want the answer
```
