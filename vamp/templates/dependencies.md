<!--
  TEMPLATE — dependencies.md
  Explain WHY each dependency is here, not just that it exists. Group sensibly.
-->
# {{project_name}} — Dependencies

**Manifests found:** {{package_json_requirements_cargo_etc}}

## Runtime
| Dependency | Role in the system | Swappable? |
|---|---|---|
| {{name}} | {{why_its_used}} | {{yes/no — what it'd take}} |

## Dev / build / test
| Dependency | Role |
|---|---|
| {{name}} | {{why}} |

## External services & infra
- {{db_apis_queues_cloud_and_what_they_provide}}

## Coupling notes
{{which_deps_are_load_bearing_vs_peripheral_and_any_lock_in}}

---
**CONFIDENCE:** {{1-10}} | **REASONING:** {{why}}
