# Example: Building a React Component with FORGE

This walkthrough demonstrates using FORGE to build a React component from scratch.

---

## The Problem

> "Create a notification filter component that lets users filter notifications by priority (high, medium, low) and shows a count of filtered items."

---

## Step 1: CLASSIFY

```bash
forge classify "Create a React notification filter component with priority filtering"
```

**Results:**

```
Category:   CREATION          Confidence: 95%
Domain:     web_development   Confidence: 92%
Framework:  R-I-S-E           Confidence: 90%
Complexity: moderate          Confidence: 82%

Rationale:
- "Create" signals CREATION category
- "React component" signals web_development domain
- New component creation → R-I-S-E for thorough design
```

**Decision:** Use R-I-S-E with web_development domain module.

---

## Step 2: Load Domain Module

```bash
forge module load web_development
```

Standards enforced:

- TypeScript for all code
- Functional components with hooks
- Error handling for async operations
- Accessible components with ARIA

---

## Step 3: Execute R-I-S-E Framework

### Phase 1: RESEARCH

**What do I know?**

- Filtering notifications by priority
- Three priority levels: high, medium, low
- Need to show count of filtered items
- React component architecture

**What don't I know?**

- Notification data structure
- UI/UX requirements (dropdown, buttons, checkboxes?)
- Does it need to be controlled or uncontrolled?
- Parent component integration

**Assumptions:**

```typescript
// Assuming notification shape:
interface Notification {
  id: string;
  title: string;
  message: string;
  priority: 'high' | 'medium' | 'low';
  timestamp: Date;
  read: boolean;
}
```

**Research Checklist:**

- [x] Understand notification data structure
- [x] Know priority levels
- [x] Count display requirement noted
- [ ] UI pattern decision needed (assuming filter buttons)

---

### Phase 2: IDENTIFY

**Requirements:**

| Requirement | Type | Priority |
|-------------|------|----------|
| Filter by priority | Functional | Must |
| Show filtered count | Functional | Must |
| TypeScript types | Non-functional | Must |
| Accessible | Non-functional | Must |
| Performant (memoized) | Non-functional | Should |

**Patterns Identified:**

1. **Container/Presentation Split** - Separate logic from UI
2. **Controlled Filter State** - Parent owns filter state for lifting if needed
3. **useMemo for Filtering** - Avoid recalculating on every render

**Risks:**

- Performance with large notification lists → Use useMemo
- Accessibility → Use proper ARIA labels and roles
- State management → Keep simple, lift if needed later

**Alternative Approaches:**

1. **Buttons for each priority** (simple, clear) ← Selected
2. **Dropdown multi-select** (compact, less visible)
3. **Checkboxes** (flexible, but more cluttered)

---

### Phase 3: SYNTHESIZE

**Selected Approach:** Button toggle filters

**Architecture:**

```
NotificationFilter/
├── NotificationFilter.tsx      # Container (logic)
├── FilterButton.tsx            # Presentation
├── types.ts                    # TypeScript interfaces
└── NotificationFilter.test.tsx # Tests
```

**Interface Design:**

```typescript
// Props for the component
interface NotificationFilterProps {
  notifications: Notification[];
  onFilterChange?: (filtered: Notification[]) => void;
}

// Internal state
type PriorityFilter = Set<'high' | 'medium' | 'low'>;
```

**Implementation Plan:**

1. Create types.ts with interfaces
2. Create FilterButton.tsx (presentation)
3. Create NotificationFilter.tsx (container with logic)
4. Add accessibility attributes
5. Write tests

---

### Phase 4: EXECUTE

**Step 1: types.ts**

```typescript
// src/components/NotificationFilter/types.ts

export type Priority = 'high' | 'medium' | 'low';

export interface Notification {
  id: string;
  title: string;
  message: string;
  priority: Priority;
  timestamp: Date;
  read: boolean;
}

export interface NotificationFilterProps {
  /** Array of notifications to filter */
  notifications: Notification[];
  /** Callback when filtered notifications change */
  onFilterChange?: (filtered: Notification[]) => void;
  /** CSS class name for styling */
  className?: string;
}

export interface FilterButtonProps {
  /** Priority level this button filters */
  priority: Priority;
  /** Whether this filter is currently active */
  isActive: boolean;
  /** Number of notifications matching this priority */
  count: number;
  /** Click handler */
  onClick: () => void;
}
```

**Step 2: FilterButton.tsx**

```typescript
// src/components/NotificationFilter/FilterButton.tsx

import React from 'react';
import { FilterButtonProps, Priority } from './types';

const PRIORITY_LABELS: Record<Priority, string> = {
  high: 'High',
  medium: 'Medium',
  low: 'Low',
};

const PRIORITY_COLORS: Record<Priority, string> = {
  high: 'bg-red-500 hover:bg-red-600',
  medium: 'bg-yellow-500 hover:bg-yellow-600',
  low: 'bg-green-500 hover:bg-green-600',
};

/**
 * Button component for filtering notifications by priority.
 */
export const FilterButton: React.FC<FilterButtonProps> = ({
  priority,
  isActive,
  count,
  onClick,
}) => {
  const baseClasses = 'px-4 py-2 rounded-lg font-medium transition-all duration-200';
  const activeClasses = isActive
    ? `${PRIORITY_COLORS[priority]} text-white`
    : 'bg-gray-200 text-gray-600 hover:bg-gray-300';

  return (
    <button
      type="button"
      onClick={onClick}
      className={`${baseClasses} ${activeClasses}`}
      aria-pressed={isActive}
      aria-label={`Filter ${PRIORITY_LABELS[priority]} priority notifications. ${count} items.`}
    >
      {PRIORITY_LABELS[priority]}
      <span className="ml-2 px-2 py-0.5 bg-white/20 rounded-full text-sm">
        {count}
      </span>
    </button>
  );
};
```

**Step 3: NotificationFilter.tsx**

```typescript
// src/components/NotificationFilter/NotificationFilter.tsx

import React, { useState, useMemo, useCallback, useEffect } from 'react';
import { FilterButton } from './FilterButton';
import { NotificationFilterProps, Priority, Notification } from './types';

const ALL_PRIORITIES: Priority[] = ['high', 'medium', 'low'];

/**
 * Component for filtering notifications by priority level.
 * 
 * @example
 * ```tsx
 * <NotificationFilter
 *   notifications={notifications}
 *   onFilterChange={(filtered) => setVisible(filtered)}
 * />
 * ```
 */
export const NotificationFilter: React.FC<NotificationFilterProps> = ({
  notifications,
  onFilterChange,
  className = '',
}) => {
  // Track which priorities are active (all active by default)
  const [activeFilters, setActiveFilters] = useState<Set<Priority>>(
    new Set(ALL_PRIORITIES)
  );

  // Memoize count per priority to avoid recalculation
  const countByPriority = useMemo(() => {
    const counts: Record<Priority, number> = { high: 0, medium: 0, low: 0 };
    notifications.forEach((n) => {
      counts[n.priority]++;
    });
    return counts;
  }, [notifications]);

  // Memoize filtered notifications
  const filteredNotifications = useMemo(() => {
    if (activeFilters.size === ALL_PRIORITIES.length) {
      return notifications; // All active = no filtering needed
    }
    return notifications.filter((n) => activeFilters.has(n.priority));
  }, [notifications, activeFilters]);

  // Notify parent when filtered results change
  useEffect(() => {
    onFilterChange?.(filteredNotifications);
  }, [filteredNotifications, onFilterChange]);

  // Toggle a priority filter
  const handleToggle = useCallback((priority: Priority) => {
    setActiveFilters((prev) => {
      const next = new Set(prev);
      if (next.has(priority)) {
        // Don't allow deselecting all
        if (next.size > 1) {
          next.delete(priority);
        }
      } else {
        next.add(priority);
      }
      return next;
    });
  }, []);

  // Total filtered count for display
  const totalFiltered = filteredNotifications.length;
  const totalAll = notifications.length;

  return (
    <div className={`flex flex-col gap-4 ${className}`} role="group" aria-label="Notification priority filters">
      {/* Filter Buttons */}
      <div className="flex gap-2">
        {ALL_PRIORITIES.map((priority) => (
          <FilterButton
            key={priority}
            priority={priority}
            isActive={activeFilters.has(priority)}
            count={countByPriority[priority]}
            onClick={() => handleToggle(priority)}
          />
        ))}
      </div>

      {/* Count Display */}
      <p className="text-sm text-gray-600" aria-live="polite">
        Showing <span className="font-semibold">{totalFiltered}</span> of{' '}
        <span className="font-semibold">{totalAll}</span> notifications
      </p>
    </div>
  );
};

export default NotificationFilter;
```

**Step 4: Tests**

```typescript
// src/components/NotificationFilter/NotificationFilter.test.tsx

import { render, screen, fireEvent } from '@testing-library/react';
import { NotificationFilter } from './NotificationFilter';
import { Notification } from './types';

const mockNotifications: Notification[] = [
  { id: '1', title: 'High 1', message: '', priority: 'high', timestamp: new Date(), read: false },
  { id: '2', title: 'High 2', message: '', priority: 'high', timestamp: new Date(), read: false },
  { id: '3', title: 'Medium', message: '', priority: 'medium', timestamp: new Date(), read: false },
  { id: '4', title: 'Low', message: '', priority: 'low', timestamp: new Date(), read: false },
];

describe('NotificationFilter', () => {
  it('renders all filter buttons', () => {
    render(<NotificationFilter notifications={mockNotifications} />);
    
    expect(screen.getByRole('button', { name: /High/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Medium/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Low/i })).toBeInTheDocument();
  });

  it('shows correct counts per priority', () => {
    render(<NotificationFilter notifications={mockNotifications} />);
    
    expect(screen.getByRole('button', { name: /High.*2/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Medium.*1/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Low.*1/i })).toBeInTheDocument();
  });

  it('shows total count initially', () => {
    render(<NotificationFilter notifications={mockNotifications} />);
    
    expect(screen.getByText(/Showing 4 of 4/i)).toBeInTheDocument();
  });

  it('filters when clicking a button', () => {
    const onFilterChange = jest.fn();
    render(
      <NotificationFilter 
        notifications={mockNotifications} 
        onFilterChange={onFilterChange}
      />
    );
    
    // Click to deselect "high"
    fireEvent.click(screen.getByRole('button', { name: /High/i }));
    
    // Should show 2 of 4 (medium + low)
    expect(screen.getByText(/Showing 2 of 4/i)).toBeInTheDocument();
  });

  it('has accessible button states', () => {
    render(<NotificationFilter notifications={mockNotifications} />);
    
    const highButton = screen.getByRole('button', { name: /High/i });
    expect(highButton).toHaveAttribute('aria-pressed', 'true');
  });
});
```

---

## Step 4: VERIFY

```bash
forge verify src/components/NotificationFilter/ --domain web_development
```

**Layer 1 (Formal):**

```
✓ TypeScript compiles: 0 errors
✓ ESLint: 0 errors, 0 warnings
```

**Layer 2 (Testing):**

```
✓ 5 tests passing
✓ Coverage: 94%
```

**Layer 3 (Statistical):**

```
✓ No performance regression
✓ Bundle size: +2.1 KB
```

**Standards Check:**

```
✓ WEB-REQ-001: TypeScript types present
✓ WEB-REQ-002: Functional component with hooks
✓ WEB-REQ-003: Error handling present
✓ WEB-REQ-004: Accessible with ARIA labels
```

**Result: VERIFIED ✓**

---

## Step 5: OMEGA Learn

```yaml
learning_record:
  problem_category: "CREATION"
  domain: "web_development"
  framework_used: "R-I-S-E"
  
  successful_patterns:
    - pattern: "Container/Presentation Split"
      description: "Separated FilterButton (presentation) from NotificationFilter (logic)"
      why_effective: "Made testing easier, components reusable"
    - pattern: "useMemo for Derived State"
      description: "Memoized counts and filtered results"
      why_effective: "Avoids unnecessary recalculations"
  
  iterations_needed: 1
  time_to_solution: 35
  
  quality_achieved:
    completeness: 0.98
    accuracy: 0.97
    consistency: 0.94
```

---

## Summary

| Phase | Action | Time |
|-------|--------|------|
| RESEARCH | Understood requirements, made assumptions | 5 min |
| IDENTIFY | Found patterns, assessed risks, chose approach | 8 min |
| SYNTHESIZE | Designed architecture, planned implementation | 5 min |
| EXECUTE | Built types, components, tests | 15 min |
| VERIFY | Ran verification pipeline | 2 min |

**Total Time:** 35 minutes
**Quality Score:** 96%
**Coverage:** 94%

---

## Key Takeaways

1. **R-I-S-E is thorough for new creation** - Research phase caught missing requirements early
2. **Patterns speed development** - Container/Presentation split made testing trivial
3. **useMemo prevents performance issues** - Worth adding early for lists
4. **Accessibility from the start** - ARIA labels added during development, not retrofitted
