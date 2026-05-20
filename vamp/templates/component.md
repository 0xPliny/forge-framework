<!--
  TEMPLATE — components/<module>.md  (one per major module/directory)
  Paraphrase responsibilities and interfaces. Signatures OK; no implementation bodies.
-->
# Component: {{module_name}}

**Path:** `{{relative_path}}`

## Responsibility
{{what_this_module_owns_in_one_or_two_sentences}}

## Public surface
Interfaces other parts of the system rely on (signatures only):
- `{{signature}}` — {{what_it_does}}

## Depends on
- **Internal:** {{other_modules}}
- **External:** {{libraries_and_why}}

## Used by
{{which_parts_of_the_system_call_into_this}}

## How to extend
{{where_and_how_youd_add_to_this_module}}

---
**CONFIDENCE:** {{1-10}} | **REASONING:** {{why}}
