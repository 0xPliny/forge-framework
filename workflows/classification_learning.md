# Classification Learning System

**Status:** Implemented in v1.2 (correction capture, hints, strong-signal promotion). Weighted scoring and adaptive thresholds remain design only; see [Implementation status](#implementation-status).
**Version:** 1.2
**Purpose:** Enable FORGE to learn from user corrections to improve classification accuracy

---

## How it works today

Corrections live in the same learnings store as every other OMEGA insight
(`learnings/_index.jsonl`), so there is one store, one schema and one
retrieval path. A correction is a learning entry tagged
`classification-correction`, `from:<ORIGINAL>` and `to:<CORRECTED>`.

```bash
# The user says: "This is TRANSFORMATION, not CREATION"
python tools/forge_learn.py correct --from CREATION --to TRANSFORMATION \
  --keywords refactor,existing,module --domain web_development \
  --reason "Refactoring existing code, not building new"

# Next time a task carries those signal words:
python tools/forge_learn.py hints --keywords refactor,legacy --domain web_development
# → Past corrections suggest TRANSFORMATION (1 correction(s), weak signal).
```

`hints` counts corrections whose keywords overlap the task's keywords, in the
same domain or `general`. Three or more agreeing corrections make a **strong
signal** (the promotion rule below); the `forge-classifier` skill then uses
the suggested category and says that it came from past corrections. Fewer
than three is a weak signal: the skill names it and lowers its confidence.

---

## Overview

When a user corrects a classification (e.g., "This should be TRANSFORMATION, not CREATION"), the framework captures this correction and uses it to improve future classifications.

This document describes the conceptual design for a classification learning system that integrates with the OMEGA Loop.

---

## Problem Statement

The Problem Classifier uses keyword matching and context signals to categorize problems. However:

1. Signal words can be ambiguous (e.g., "refactor" could be TRANSFORMATION or OPTIMIZATION)
2. Domain-specific terminology may not match default patterns
3. User intent may differ from literal interpretation

**Solution:** Learn from user corrections to adjust classification weights over time.

---

## Correction Logging Format

When a user corrects a classification, capture the following data:

```yaml
classification_correction:
  # Metadata
  timestamp: "2025-01-05T12:00:00Z"
  session_id: "abc-123-def"
  
  # Original (incorrect) classification
  original_classification:
    category: "CREATION"
    confidence: 0.72
    signal_words: ["create", "new"]
    domain: "web_development"
  
  # User-provided correction
  corrected_classification:
    category: "TRANSFORMATION"
    confidence: 1.0  # User-provided corrections are 100% confident
    user_explanation: "This is refactoring existing code, not creating new"
  
  # Problem signature for pattern matching
  problem_signature:
    full_text: "Refactor the existing authentication module"
    keywords: ["refactor", "existing", "module"]
    domain: "web_development"
    complexity: "moderate"
  
  # Extracted learning
  learning:
    pattern: "When 'refactor' appears with 'existing', prefer TRANSFORMATION"
    affected_signals:
      - word: "refactor"
        category_adjustment:
          TRANSFORMATION: +0.15
          CREATION: -0.05
      - word: "existing"
        category_adjustment:
          TRANSFORMATION: +0.10
          CREATION: -0.10
```

---

## Confidence Adjustment Algorithm

### Per-Correction Adjustment

```python
def process_correction(original, corrected, problem):
    """
    Adjust classification weights based on user correction.
    
    Args:
        original: Original classification result
        corrected: User-provided correct category
        problem: Original problem text
    """
    signal_words = extract_signal_words(problem)
    
    for word in signal_words:
        # Decrease weight for original (wrong) category
        weights[word][original.category] -= 0.05
        
        # Increase weight for corrected (right) category
        weights[word][corrected.category] += 0.10
        
        # Clamp weights to [0, 1] range
        weights[word] = clamp_weights(weights[word])
    
    # Store the correction for pattern analysis
    store_correction(original, corrected, problem, signal_words)
```

### Strong Signal Promotion

When the same correction pattern appears 3+ times, promote to "strong signal":

```python
def check_strong_signals():
    """
    Identify recurring correction patterns and promote to strong signals.
    """
    patterns = group_corrections_by_pattern()
    
    for pattern, corrections in patterns.items():
        if len(corrections) >= 3:
            # Promote to strong signal (2x weight adjustment)
            for word in pattern.signal_words:
                weights[word][pattern.corrected_category] *= 2.0
                weights[word][pattern.original_category] *= 0.5
            
            # Mark pattern as strong signal
            strong_signals.add(pattern)
            
            log(f"Promoted to strong signal: {pattern}")
```

### Classification with Learned Weights

```python
def classify_with_learning(problem):
    """
    Classify problem using base rules + learned weights.
    """
    # Get base classification
    base_result = base_classifier.classify(problem)
    
    # Apply learned weight adjustments
    signal_words = extract_signal_words(problem)
    adjusted_scores = base_result.category_scores.copy()
    
    for word in signal_words:
        if word in learned_weights:
            for category, adjustment in learned_weights[word].items():
                adjusted_scores[category] += adjustment
    
    # Normalize and return
    final_category = max(adjusted_scores, key=adjusted_scores.get)
    final_confidence = calculate_confidence(adjusted_scores, final_category)
    
    return Classification(
        category=final_category,
        confidence=final_confidence,
        learned_adjustments=len([w for w in signal_words if w in learned_weights])
    )
```

---

## Integration with OMEGA Loop

Classification corrections are automatically captured as part of the OMEGA Loop's LEARN phase:

```yaml
# OMEGA Loop Learning Record
learning:
  problem: "Refactor authentication module"
  category: "TRANSFORMATION"  # Corrected from CREATION
  domain: "web_development"
  
  what_worked:
    - pattern: "Recognized 'refactor' as TRANSFORMATION signal"
      reuse_when: "User mentions refactoring existing code"
      confidence: 0.95
  
  what_failed:
    - attempt: "Initially classified as CREATION due to 'new' keyword"
      lesson: "'refactor' should override 'new' for classification"
      avoid_when: "Problem mentions refactoring or modifying existing code"
  
  classification_correction:
    original: "CREATION"
    corrected: "TRANSFORMATION"
    key_signals: ["refactor", "existing"]
    learned_weights_updated: true
```

---

## Adaptive Confidence Thresholds

The framework can adjust confidence thresholds based on historical correction rates:

### Threshold Adjustment Rules

| User Correction Rate | Confidence Threshold | Behavior |
|---------------------|---------------------|----------|
| < 5% | 0.65 | Lower threshold, trust classifications |
| 5-15% | 0.70 | Default threshold |
| 15-25% | 0.75 | Higher threshold, ask for clarification more |
| > 25% | 0.80 | Very high threshold, almost always clarify |

### Implementation

```python
def get_adaptive_threshold(domain, user_id=None):
    """
    Calculate adaptive confidence threshold based on correction history.
    """
    corrections = get_correction_history(domain, user_id)
    total_classifications = get_classification_count(domain, user_id)
    
    if total_classifications < 10:
        return 0.70  # Default threshold until enough data
    
    correction_rate = len(corrections) / total_classifications
    
    if correction_rate < 0.05:
        return 0.65
    elif correction_rate < 0.15:
        return 0.70
    elif correction_rate < 0.25:
        return 0.75
    else:
        return 0.80
```

---

## Storage Format

### File Location

```
~/.forge/
├── classification_learnings.yaml    # Correction history
├── learned_weights.yaml             # Accumulated weight adjustments
└── strong_signals.yaml              # Promoted patterns
```

### classification_learnings.yaml

```yaml
corrections:
  - timestamp: "2025-01-05T12:00:00Z"
    problem_hash: "a1b2c3d4"
    original: "CREATION"
    corrected: "TRANSFORMATION"
    signal_words: ["refactor", "existing"]
    domain: "web_development"
    
  - timestamp: "2025-01-05T14:30:00Z"
    problem_hash: "e5f6g7h8"
    original: "REPAIR"
    corrected: "OPTIMIZATION"
    signal_words: ["improve", "performance"]
    domain: "python_data"

statistics:
  total_classifications: 150
  total_corrections: 12
  correction_rate: 0.08
  last_updated: "2025-01-05T15:00:00Z"
```

### learned_weights.yaml

```yaml
signal_weights:
  refactor:
    CREATION: -0.15
    TRANSFORMATION: +0.25
    REPAIR: 0.0
    OPTIMIZATION: 0.0
    UNDERSTANDING: 0.0
    
  existing:
    CREATION: -0.20
    TRANSFORMATION: +0.15
    REPAIR: 0.0
    OPTIMIZATION: 0.0
    UNDERSTANDING: 0.0
    
  improve:
    CREATION: 0.0
    TRANSFORMATION: 0.0
    REPAIR: -0.10
    OPTIMIZATION: +0.20
    UNDERSTANDING: 0.0
```

---

## Usage Workflow

### During Classification

```
1. User states problem: "Refactor the authentication module"

2. Classifier runs:
   - Base classification: CREATION (0.72 confidence)
   - Check learned weights for signal words
   - Found: "refactor" → TRANSFORMATION +0.25
   - Adjusted classification: TRANSFORMATION (0.85 confidence)

3. If confidence < threshold:
   - Ask user: "Is this TRANSFORMATION (refactoring existing code)?"
   - User confirms or corrects

4. Log classification result
```

### After Correction

```
1. User corrects: "No, this is OPTIMIZATION, not TRANSFORMATION"

2. System captures:
   - Original: TRANSFORMATION
   - Corrected: OPTIMIZATION
   - Signal words: ["refactor", "authentication", "module"]

3. System adjusts weights:
   - "refactor" → OPTIMIZATION +0.10
   - "refactor" → TRANSFORMATION -0.05

4. System checks for strong signals:
   - If 3+ similar corrections, promote to strong signal

5. Log learning to OMEGA Loop
```

---

## Implementation status

| Capability | Status |
|---|---|
| Persist corrections | Done: `forge_learn.py correct` → `learnings/_index.jsonl` (no separate `~/.forge/` files) |
| Load learnings at classification time | Done: `forge_learn.py hints`, called by the `forge-classifier` skill |
| Strong-signal promotion (3+ corrections) | Done: `hints` reports `strong` at 3+ agreeing corrections |
| Export/import | Done by construction: the store is one JSONL file |
| Weighted signal adjustments (`learned_weights.yaml`) | Not implemented: classification is prompt-based, so there are no numeric scores to adjust |
| Adaptive confidence thresholds | Not implemented: needs classification counts, which telemetry does not yet record per correction |
| Pruning | Not implemented: the store is append-only; supersede an entry by writing a new one |

The storage format and weight algorithm sections above are the original
design and describe the not-implemented rows.

---

## Related Documents

- [problem_classifier.md](problem_classifier.md) — Classification logic
- [omega_loop.md](omega_loop.md) — Learning capture system
- [FORGE_MASTER.md](../FORGE_MASTER.md) — Master prompt
- [confidence_protocol.md](../core/confidence_protocol.md) — Confidence scoring

---

*Correction capture and hints are implemented in `tools/forge_learn.py`; weighted scoring and adaptive thresholds remain design.*

