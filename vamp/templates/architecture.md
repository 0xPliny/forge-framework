<!--
  TEMPLATE — architecture.md
  Fill every {{placeholder}}. Delete guidance comments. Paraphrase; never paste
  source. Mark anything you inferred (couldn't confirm from a file) as such.
-->
# {{project_name}} — Architecture

**Vamped:** {{date}} · **Source:** {{git_url_or_path}} · **License:** {{license}}

## What it is
{{one_paragraph_what_this_project_does_and_for_whom}}

## Stack
- **Languages:** {{languages}}
- **Frameworks / runtimes:** {{frameworks}}
- **Build / tooling:** {{build_tools}}

## High-level design
{{describe_the_layers_or_services_and_how_they_relate}}

```mermaid
{{component_diagram_boxes_and_arrows}}
```

## Key components
| Component | Responsibility | Lives in |
|---|---|---|
| {{name}} | {{what_it_owns}} | {{path}} |

## Notable design decisions
- {{decision_and_why_it_matters}}

## Extension points
Where a new developer plugs in features:
- {{extension_point}} → {{how_to_extend}}

## Ideas worth stealing
- {{the_clever_bits_you_came_here_for}}

---
**CONFIDENCE:** {{1-10}} | **REASONING:** {{why}}
**ASSUMPTIONS:** {{statement | RISK: H/M/L | IF WRONG: impact}}
