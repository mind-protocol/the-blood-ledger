# Moment Links

## CHARACTER -> MOMENT (SAID)

Purpose: Who produced the moment (speech or action).

## MOMENT -> PLACE (AT)

Purpose: Where the moment occurred.

## MOMENT -> MOMENT (THEN)

Purpose: Canonical order of moments.

Attributes:
```yaml
tick: integer
player_caused: boolean
```

## MOMENT -> TARGET (ATTACHED_TO)

Purpose: Binding for visibility and relevance.

Attributes:
```yaml
strength: float
presence_required: boolean
persistent: boolean
dies_with_target: boolean
```

## MOMENT -> MOMENT (CAN_LEAD_TO)

Purpose: Conversation transitions.

Attributes:
```yaml
trigger: enum [click, wait, auto]
require_words: string[]
weight_transfer: float
wait_ticks: integer
bidirectional: boolean
consumes_origin: boolean
```

## MOMENT -> TARGET (REFERENCES)

Purpose: Named entities referenced in text.

Attributes:
```yaml
strength: float
```

## MOMENT -> TARGET (TARGETS)

Purpose: Action target (use with action moments).

## MOMENT -> TARGET (ANSWERED_BY)

Purpose: Question moment -> answer node.

Attributes:
```yaml
tick: integer
```

## MOMENT -> CHARACTER (THREATENS)

Purpose: Threat indicator for auto-pause.

Attributes:
```yaml
threat_type: enum [physical, social, emotional]
severity: float
```
