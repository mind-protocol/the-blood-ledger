# Graph Validation

Rules for maintaining graph integrity during mutations.

---

## Rules

1. **New clusters must connect** — At least one link to an existing node
2. **No orphaned nodes** — Every node must have at least one link
3. **Partial persistence** — Valid items persisted; invalid items rejected with feedback

---

## Valid Mutation

```yaml
nodes:
  - type: character
    id: char_wulfric
    name: Wulfric

links:
  - type: belief
    character: char_wulfric    # NEW node
    narrative: narr_oath       # EXISTING node
    heard: 1.0
```

New node `char_wulfric` connects to existing `narr_oath` via belief link.

---

## Invalid Mutation

```yaml
nodes:
  - type: character
    id: char_wulfric
    name: Wulfric
  # No links — char_wulfric would be orphaned
```

---

## Error Handling

```python
result = write.apply(path="mutations/scene_001.yaml")

if result.errors:
    for error in result.errors:
        print(f"{error.item}: {error.message}")
        print(f"  Fix: {error.fix}")

print(f"Persisted: {result.persisted}")
print(f"Rejected: {result.rejected}")
```

---

## Error Types

| Error | Message | Fix |
|-------|---------|-----|
| `orphaned_node` | `char_wulfric has no links` | Add at least one link connecting this node |
| `disconnected_cluster` | `New nodes [char_a, char_b] not connected to graph` | Add link from cluster to existing node |
| `missing_target` | `Link references non-existent node: narr_unknown` | Create the target node first, or fix the ID |
| `invalid_type` | `Invalid character type: warrior` | Check `SCHEMA.md` for allowed values |
| `invalid_field` | `Unknown field: foo on character` | Check `SCHEMA.md` for valid fields |
| `missing_required` | `narrative.content is required` | Add the required field |
| `db_connection` | `Cannot connect to FalkorDB` | `docker run -p 6379:6379 falkordb/falkordb` |

---

## Partial Persistence

Valid items are always persisted. Invalid items are rejected individually:

```python
result = write.apply(path="mutations/batch.yaml")

# result.persisted = ["char_aldric", "narr_oath", "link_belief_1"]
# result.rejected = [
#   {"item": "char_wulfric", "error": "orphaned_node", "fix": "Add link..."}
# ]
```

The engine persists everything it can, then reports what failed and why.
