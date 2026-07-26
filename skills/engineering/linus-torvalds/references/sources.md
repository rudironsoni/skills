# Linus Torvalds: References and Sources

Primary sources for the Linus Torvalds style and philosophy.

---

## Essential Reading

### Linux Kernel Coding Style

The canonical reference for Torvalds' coding preferences.

- **Document:** `Documentation/process/coding-style.rst` in the Linux kernel source
- **Key topics:** Indentation, braces, naming, functions, comments, macros
- **Notable quote:** "Tabs are 8 characters... There are heretic movements that try to make indentations 4 (or even 2!) characters deep, and that is akin to trying to define the value of PI to be 3."

**Online version:**
https://www.kernel.org/doc/html/latest/process/coding-style.html

---

## LKML (Linux Kernel Mailing List) Posts

The authentic voice of Torvalds in code review. Searchable archives:

- **LKML Archive:** https://lkml.org/
- **Torvalds' posts:** https://lkml.org/lkml/author/2/

### Famous Threads

**"What the f*ck is wrong with you?" (NVIDIA)**
- Context: NVIDIA's lack of Linux support
- Quote: "NVIDIA has been the single worst company we've ever dealt with"
- Demonstrates: Technical frustration with closed systems

**"This breaks userspace"**
- Recurring theme in kernel development
- The #1 rule of kernel development
- Search: "breaks userspace" + site:lkml.org

**C++ Rants**
- "C++ is a horrible language"
- Why kernel is C-only
- Object-oriented abstractions considered harmful for systems code

**"The Art of Subtlety"**
- Sarcasm and intensity escalation patterns
- "I'll let you think about just how stupid that comment was"
- "Congratulations, you seem to have found a whole new way of screwing up"

---

## Books

### "Just for Fun: The Story of an Accidental Revolutionary" (2001)

**Authors:** Linus Torvalds and David Diamond

- Autobiography of Torvalds
- Origin story of Linux
- Philosophy on open source
- The "Just for Fun" development philosophy

### "The Art of Unix Programming" by Eric S. Raymond

- Not written by Torvalds, but aligns with his philosophy
- Unix design principles that Linux embodies
- "Do one thing well" philosophy
- Textuality, transparency, hackability

### "C Programming Language" (K&R) by Kernighan and Ritchie

- Torvalds references "the prophets Kernighan and Ritchie"
- K&R brace style is his preference
- Simplicity and clarity principles

---

## Talks and Interviews

### TED Talk: "The Mind Behind Linux" (2016)

- **URL:** https://www.ted.com/talks/linus_torvalds_the_mind_behind_linux
- Covers: Open source philosophy, Git creation, technical decision-making

### "Linus Torvalds on Git" (Google Tech Talk, 2007)

- Origin story of Git
- Why distributed version control matters
- "Content-addressable filesystem with a VCS user interface"

### "Linus Torvalds' Greatest Taboo" (2018)

- Discusses social interactions in technical communities
- Explains his communication style
- Why technical honesty matters more than politeness

---

## Git Documentation

### Git README (2005)

The original Git announcement by Torvalds:

> "Git - the stupid content tracker"

- Minimalist philosophy
- "Stupid" as a feature, not a bug
- Content-addressable design

### Git Commit Messages

Torvalds' own commit message style in the Git repository:

```
commit 1da177e4c3f41524e886b7f1b8a0c1fc7321cac2
Author: Linus Torvalds <torvalds@ppc970.osdl.org>
Date:   Sat Apr 16 15:20:36 2005 -0700

    Linux-2.6.12-rc2

    Initial git repository build. I'm not bothering with the full history,
    even though we have it. We can create a separate "historical" git
    archive of that later if we want to, and in the meantime it's about
    3.2GB when imported into git - space that would just make the git
    repo unusable for people for 4GB directory+filesystem limits.
```

---

## Key Concepts and Their Origins

| Concept | Origin | Source |
|---------|--------|--------|
| "Data structures first" | Interview/quote | Widely attributed to Torvalds |
| "Never break userspace" | Kernel development rule | LKML, kernel documentation |
| "Tabs are 8 characters" | Linux Coding Style | `coding-style.rst` |
| "K&R are right" | Linux Coding Style | `coding-style.rst` |
| "Show me the code" | Famous quote | Various interviews |
| "Given enough eyeballs" | "Linus's Law" from The Cathedral and the Bazaar | ESR's book, popularized by Torvalds |
| "Talk is cheap" | Famous quote | Various interviews |
| "I'm not a nice person" | TED Talk | 2016 TED interview |

---

## Related Resources

### The Cathedral and the Bazaar

**Author:** Eric S. Raymond (1997)

- "Linus's Law": "Given enough eyeballs, all bugs are shallow"
- Contrasts cathedral (closed) vs bazaar (open) development
- Linux as the exemplar of bazaar development

### The Mythical Man-Month

**Author:** Fred Brooks

- Brooks's Law: "Adding manpower to a late software project makes it later"
- Complexity and communication overhead
- Relevant to Torvalds' preference for small, focused changes

---

## Search Terms for Research

To find more authentic Torvalds quotes and patterns:

- `site:lkml.org "Linus Torvalds" "breaks userspace"`
- `site:lkml.org "Linus Torvalds" "makes my eyes bleed"`
- `site:lkml.org "Linus Torvalds" "pure and utter garbage"`
- `site:lkml.org "Linus Torvalds" "data structures"`
- `site:lkml.org "Linus Torvalds" "Christ people"`
- `site:lkml.org "Linus Torvalds" "what the f*ck"`

---

## License Note

The Linux kernel is released under the GNU General Public License v2 (GPLv2). LKML posts are generally considered public domain or fair use for educational purposes. The style and philosophy documented here are derived from publicly available sources.
