<!--
  TEMPLATE — setup.md
  Reconstruct how to install/configure/run from scratch. Commands must be real
  (derived from the manifests/scripts you found), copy-paste ready, and ordered.
-->
# {{project_name}} — Setup & Run

## Prerequisites
- {{runtime_versions_eg_node_20_python_3_11}}
- {{system_deps_or_services_eg_postgres_docker}}

## Install
```bash
{{install_commands}}
```

## Configure
- **Env vars:** {{required_vars_and_what_they_do}}
- **Config files:** {{files_to_copy_or_edit_eg_.env.example}}

## Run
```bash
{{run_commands}}
```

## Test
```bash
{{test_commands}}
```

## Common entry points
- {{path}} — {{what_it_starts}}

---
**CONFIDENCE:** {{1-10}} | **REASONING:** {{why}}
**ASSUMPTIONS:** {{anything_inferred_about_setup_that_wasnt_explicitly_documented}}
