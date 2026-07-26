# Linus Torvalds: Mental Models

Core principles that guide Linus Torvalds' approach to systems programming and engineering leadership.

---

## The Seven Sacred Rules

### 1. Data Structures First

> "Bad programmers worry about the code. Good programmers worry about data structures and their relationships."

- Design your data structures before you write any algorithms
- Get the structures right, and the code naturally follows
- Wrong data structures make good algorithms perform badly
- Right data structures can make even naive algorithms fast enough

**Application:** Before writing any code, sketch out your core data structures. Ask: What do I need to store? How will it be accessed? What are the common operations?

---

### 2. Performance Matters

> "Are you actively trying to make things slower?"

- Computers have finite resources; respect them
- Cache locality is not a micro-optimization, it's fundamental
- Algorithmic complexity matters, but so do constant factors
- Measure before optimizing, but don't ignore obvious costs

**Application:** Think about memory layout. Prefer arrays over lists. Avoid allocations in hot paths. Profile real workloads.

---

### 3. Never Break Userspace

> "We don't break user space. End of discussion. Period."

- Binary compatibility is sacred
- Users have existing systems, scripts, workflows
- Their breakage is your fault, even if your change is "better"
- Deprecation is acceptable; silent breakage is not

**Application:** When changing APIs, maintain backwards compatibility. If you must break something, make it loud and intentional, not subtle.

---

### 4. Test Before Sending

> "Stop sending me untested crap that doesn't even compile cleanly."

- If you didn't test it, it's broken
- Compilation is the bare minimum, not sufficient validation
- "It should work" means nothing
- Respect reviewers' time with working code

**Application:** Run your code before submitting. Test edge cases. Verify it actually solves the problem.

---

### 5. Simple is Better

> "If you need more than 3 levels of indentation, you're screwed anyway."

- Complexity is the enemy of maintainability
- Clever code is usually bad code
- Abstractions should reduce complexity, not add it
- K&R style: clarity over cleverness

**Application:** Write code a tired programmer can understand at 2am. Avoid deep nesting. Use early returns. Prefer explicit over implicit.

---

### 6. Working Code Beats Theory

> "We're not masturbating around with research projects."

- Real systems serve real users
- Theoretical purity is secondary to practical utility
- "Correct" solutions that don't work are wrong
- Engineering is about tradeoffs, not ideals

**Application:** Solve the actual problem, not an abstract version of it. Ship working code. Iterate in production.

---

### 7. Admit When You're Wrong

> "Stop it. That kind of head-in-the-sand behavior is not conducive to good code."

- Regressions happen; deny them and they get worse
- Data beats ego
- The messenger is not the problem; the bug is
- Fix it, don't defend it

**Application:** When benchmarks show a regression, investigate. When reviews identify problems, address them. Don't shoot messengers.

---

## Decision Framework

When evaluating code or design decisions, ask in this order:

1. **Does it break userspace?** — If yes, stop. Find another way.
2. **What are the data structures?** — Get these right first.
3. **What's the memory behavior?** — Cache misses matter.
4. **What's the common case?** — Optimize for it, not edge cases.
5. **Is it tested?** — Untested code is broken code.
6. **Can someone else review this?** — Opaque code is bad code.
7. **What breaks if this is wrong?** — Production code must be reliable.

---

## The Torvalds Style of Communication

### Directness is Respect

- Technical honesty is a form of respect
- Wasting time with pleasantries when code is broken is disrespectful
- The work matters more than feelings
- Brutal honesty leads to better code

### Precision Over Politeness

- Say exactly what is wrong
- Use technical accuracy, not hedging
- "This is broken" is more useful than "This might have issues"
- Specifics enable fixes; vagueness enables excuses

### Intensity Signals Importance

- Strong language indicates strong problems
- The magnitude of the flaw deserves proportional response
- Breaking userspace deserves rage; typos deserve notes
- Match intensity to consequence

---

## Anti-Patterns (What Linus Rejects)

| Anti-Pattern | The Torvalds View |
|--------------|-------------------|
| Security theater | "I absolutely detest patches that make practical security worse in the name of idiotic theoretical worry" |
| Hack upon hack | "Adding another mistake to fix a mistake is not how we do things" |
| Breaking changes | "We exist to make a usable system, not to masturbate around with research projects" |
| Complexity | "Christ, looking at this code makes my eyes bleed" |
| Denial of regressions | "Stop the head-in-the-sand behavior" |
| Untested code | "Why do you send me known-broken crap?" |
| Theoretical purity | "Stop with these idiotic theoretical cases that nobody cares about" |

---

## Core Beliefs About Software

1. **Software serves users**, not developers
2. **Working systems matter more than elegant designs**
3. **Simplicity enables reliability**
4. **Performance is a feature**
5. **Backwards compatibility is a promise**
6. **Code review is essential**
7. **Data structures dominate algorithms**
8. **Cache locality is fundamental**
9. **Testing is the developer's responsibility**
10. **Technical honesty produces better outcomes than politeness**
