# Book verification to-do

The course cites three books: *A Philosophy of Software Design* (APOSD, 2nd edition), *The Pragmatic Programmer* (TPP, 20th Anniversary Edition), and *Domain-Driven Design* (DDD).
The full books were not available when these lessons were written, so citations were checked against free, official sources only.
Every citation that still needs the full book is marked "(to verify against book)" in the lessons and listed below.

This file is generated from those marks; regenerate it after editing citations.
Never commit the books or text extracted from them: the repository and site are public.

## Sources used instead of the full books

- **TPP:** the publisher's [book page](https://pragprog.com/titles/tpp20/the-pragmatic-programmer-20th-anniversary-edition/), with the official contents list and free excerpts of Topics 9, 27, 31, and 34, and the publisher's [official tip list](https://pragprog.com/tips/) with tip numbers and pages.
- **APOSD:** the author's [book page](https://web.stanford.edu/~ouster/cgi-bin/aposd.php) and free [2nd-edition extract](https://web.stanford.edu/~ouster/cgi-bin/aposd2ndEdExtract.pdf), which contains Chapter 6, section 9.8, the comments chapter, and Chapter 21, plus his [discussion with Robert Martin](https://github.com/johnousterhout/aposd-vs-clean-code/blob/main/README.md).
- **DDD:** Evans's free [*DDD Reference*](https://www.domainlanguage.com/ddd/reference/) (Creative Commons Attribution 4.0), which summarises the patterns but gives no chapter numbers.

## Already checked against official full text

- TPP Topic 9, "DRY - The Evils of Duplication": DRY concerns knowledge and intent; the acid test is how many places one change touches; similar-looking code is not always duplicated knowledge (Day 6).
- TPP Topic 27, "Don't Outrun Your Headlights": small steps with feedback (Days 11, 19, 22).
- TPP Topic 34, "Shared State Is Incorrect State": non-atomic check-then-update, mutual exclusion, making the resource responsible for itself (Day 20).
- APOSD Chapter 6, "General-Purpose Modules are Deeper": somewhat general-purpose interfaces (Days 5, 10).
- APOSD section 9.8: splitting functions by length alone (Day 6).
- APOSD Chapter 21, "Decide What Matters" (Day 15).
- APOSD Chapter 2's three symptoms, restated in the comments chapter of the extract (Day 4); the Chapter 2 title is still listed below.
- Every TPP tip number, page, and title cited, against the official tip list.

## To verify against the book

| Day | File | Line | Book | Citation | What to check |
|---|---|---|---|---|---|
| 1 | `website/modules/01-names-that-explain-the-job.html` | 23 | APOSD | her. An AI assistant wrote its first version; it works, and now you maintain it. | Not checked: confirm the chapter number, title, and that the chapter makes this claim. |
| 1 | `week-01/day-01-names-that-explain-the-job.md` | 59 | TPP | Topic 44, "Naming Things" | Topic title confirmed in the publisher's official contents list; number counted from that list and anchored by cross-references in the free excerpts. Check the topic's content supports the claim. |
| 1 | `week-01/day-01-names-that-explain-the-job.md` | 91 | APOSD | Chapter 4 | Not checked: confirm the chapter number, title, and that the chapter makes this claim. |
| 1 | `week-01/day-01-names-that-explain-the-job.md` | 99 | DDD | Chapter 2 | Concept checked in Evans's free DDD Reference; confirm the chapter number and title, and that the chapter makes this claim. |
| 1 | `website/modules/01-names-that-explain-the-job.html` | 151 | TPP | Topic 44, “Naming Things” | Topic title confirmed in the publisher's official contents list; number counted from that list and anchored by cross-references in the free excerpts. Check the topic's content supports the claim. |
| 1 | `website/modules/01-names-that-explain-the-job.html` | 164 | APOSD | Chapter 14, “Choosing Names” | Not checked: confirm the chapter number, title, and that the chapter makes this claim. |
| 1 | `website/modules/01-names-that-explain-the-job.html` | 174 | TPP | Topic 44, “Naming Things” | Topic title confirmed in the publisher's official contents list; number counted from that list and anchored by cross-references in the free excerpts. Check the topic's content supports the claim. |
| 1 | `week-01/day-01-names-that-explain-the-job.md` | 200 | APOSD | Chapter 14, "Choosing Names." | Not checked: confirm the chapter number, title, and that the chapter makes this claim. |
| 1 | `week-01/day-01-names-that-explain-the-job.md` | 205 | TPP | Topic 44, "Naming Things" | Topic title confirmed in the publisher's official contents list; number counted from that list and anchored by cross-references in the free excerpts. Check the topic's content supports the claim. |
| 2 | `week-01/day-02-what-a-function-promises.md` | 59 | TPP | Topic 23, "Design by Contract" | Topic title confirmed in the publisher's official contents list; number counted from that list and anchored by cross-references in the free excerpts. Check the topic's content supports the claim. |
| 2 | `website/modules/02-what-a-function-promises.html` | 83 | APOSD | Chapter 4 | Not checked: confirm the chapter number, title, and that the chapter makes this claim. |
| 2 | `website/modules/02-what-a-function-promises.html` | 84 | APOSD | Chapter 4 | Not checked: confirm the chapter number, title, and that the chapter makes this claim. |
| 2 | `week-01/day-02-what-a-function-promises.md` | 96 | APOSD | Chapter 4 | Not checked: confirm the chapter number, title, and that the chapter makes this claim. |
| 2 | `week-01/day-02-what-a-function-promises.md` | 97 | APOSD | Chapter 4 | Not checked: confirm the chapter number, title, and that the chapter makes this claim. |
| 2 | `week-01/day-02-what-a-function-promises.md` | 99 | APOSD | Chapter 4 | Not checked: confirm the chapter number, title, and that the chapter makes this claim. |
| 2 | `week-01/day-02-what-a-function-promises.md` | 100 | APOSD | Chapter 4 | Not checked: confirm the chapter number, title, and that the chapter makes this claim. |
| 2 | `website/modules/02-what-a-function-promises.html` | 194 | TPP | Topic 23, “Design by Contract” | Topic title confirmed in the publisher's official contents list; number counted from that list and anchored by cross-references in the free excerpts. Check the topic's content supports the claim. |
| 2 | `website/modules/02-what-a-function-promises.html` | 207 | APOSD | interface versus implementation and Chapter 13 on useful function documentation | Not checked: confirm the chapter number, title, and that the chapter makes this claim. |
| 2 | `website/modules/02-what-a-function-promises.html` | 217 | TPP | Topic 23, “Design by Contract” | Topic title confirmed in the publisher's official contents list; number counted from that list and anchored by cross-references in the free excerpts. Check the topic's content supports the claim. |
| 2 | `week-01/day-02-what-a-function-promises.md` | 243 | APOSD | Chapter 13 | Not checked: confirm the chapter number, title, and that the chapter makes this claim. |
| 2 | `week-01/day-02-what-a-function-promises.md` | 250 | TPP | Topic 23, "Design by Contract" | Topic title confirmed in the publisher's official contents list; number counted from that list and anchored by cross-references in the free excerpts. Check the topic's content supports the claim. |
| 3 | `week-01/day-03-follow-the-data.md` | 75 | APOSD | Chapter 2, "The Nature of Complexity" | Not checked: confirm the chapter number, title, and that the chapter makes this claim. |
| 3 | `week-01/day-03-follow-the-data.md` | 76 | APOSD | Chapter 5, "Information Hiding (and Leakage)" | Not checked: confirm the chapter number, title, and that the chapter makes this claim. |
| 3 | `week-01/day-03-follow-the-data.md` | 81 | TPP | Topic 28, "Decoupling" | Topic title confirmed in the publisher's official contents list; number counted from that list and anchored by cross-references in the free excerpts. Check the topic's content supports the claim. |
| 3 | `week-01/day-03-follow-the-data.md` | 98 | APOSD | Chapter 2 | Not checked: confirm the chapter number, title, and that the chapter makes this claim. |
| 3 | `week-01/day-03-follow-the-data.md` | 99 | APOSD | Chapter 5 | Not checked: confirm the chapter number, title, and that the chapter makes this claim. |
| 3 | `week-01/day-03-follow-the-data.md` | 265 | APOSD | Chapter 5, "Information Hiding (and Leakage)" | Not checked: confirm the chapter number, title, and that the chapter makes this claim. |
| 3 | `week-01/day-03-follow-the-data.md` | 272 | TPP | Topic 28, "Decoupling" | Topic title confirmed in the publisher's official contents list; number counted from that list and anchored by cross-references in the free excerpts. Check the topic's content supports the claim. |
| 4 | `week-01/day-04-complexity-symptoms.md` | 57 | APOSD | Chapter 2, "The Nature of Complexity" | Not checked: confirm the chapter number, title, and that the chapter makes this claim. |
| 4 | `week-01/day-04-complexity-symptoms.md` | 65 | TPP | Topic 3, "Software Entropy" | Topic title confirmed in the publisher's official contents list; number counted from that list and anchored by cross-references in the free excerpts. Check the topic's content supports the claim. |
| 4 | `week-01/day-04-complexity-symptoms.md` | 71 | APOSD | Chapter 2 | Not checked: confirm the chapter number, title, and that the chapter makes this claim. |
| 4 | `week-01/day-04-complexity-symptoms.md` | 72 | TPP | Topic 8, "The Essence of Good Design" | Topic title confirmed in the publisher's official contents list; number counted from that list and anchored by cross-references in the free excerpts. Check the topic's content supports the claim. |
| 4 | `week-01/day-04-complexity-symptoms.md` | 83 | APOSD | Chapter 2 | Not checked: confirm the chapter number, title, and that the chapter makes this claim. |
| 4 | `week-01/day-04-complexity-symptoms.md` | 84 | APOSD | Chapter 2 | Not checked: confirm the chapter number, title, and that the chapter makes this claim. |
| 4 | `week-01/day-04-complexity-symptoms.md` | 85 | APOSD | Chapter 2 | Not checked: confirm the chapter number, title, and that the chapter makes this claim. |
| 4 | `week-01/day-04-complexity-symptoms.md` | 86 | APOSD | Chapter 2 | Not checked: confirm the chapter number, title, and that the chapter makes this claim. |
| 4 | `week-01/day-04-complexity-symptoms.md` | 87 | APOSD | Chapter 2 | Not checked: confirm the chapter number, title, and that the chapter makes this claim. |
| 4 | `week-01/day-04-complexity-symptoms.md` | 88 | TPP | Topic 3, "Software Entropy" | Topic title confirmed in the publisher's official contents list; number counted from that list and anchored by cross-references in the free excerpts. Check the topic's content supports the claim. |
| 4 | `week-01/day-04-complexity-symptoms.md` | 221 | APOSD | Chapter 2, "The Nature of Complexity" | Not checked: confirm the chapter number, title, and that the chapter makes this claim. |
| 4 | `week-01/day-04-complexity-symptoms.md` | 224 | TPP | Topic 3, "Software Entropy" | Topic title confirmed in the publisher's official contents list; number counted from that list and anchored by cross-references in the free excerpts. Check the topic's content supports the claim. |
| 5 | `week-01/day-05-deep-modules.md` | 56 | APOSD | Chapter 4, "Modules Should Be Deep" | Not checked: confirm the chapter number, title, and that the chapter makes this claim. |
| 5 | `week-01/day-05-deep-modules.md` | 60 | APOSD | Chapter 7, "Different Layer, Different Abstraction" | Not checked: confirm the chapter number, title, and that the chapter makes this claim. |
| 5 | `week-01/day-05-deep-modules.md` | 61 | APOSD | Chapter 8, "Pull Complexity Downwards" | Not checked: confirm the chapter number, title, and that the chapter makes this claim. |
| 5 | `week-01/day-05-deep-modules.md` | 79 | APOSD | Chapter 4 | Not checked: confirm the chapter number, title, and that the chapter makes this claim. |
| 5 | `week-01/day-05-deep-modules.md` | 80 | APOSD | Chapter 4 | Not checked: confirm the chapter number, title, and that the chapter makes this claim. |
| 5 | `week-01/day-05-deep-modules.md` | 81 | APOSD | Chapter 4 | Not checked: confirm the chapter number, title, and that the chapter makes this claim. |
| 5 | `week-01/day-05-deep-modules.md` | 82 | APOSD | Chapter 4 | Not checked: confirm the chapter number, title, and that the chapter makes this claim. |
| 5 | `week-01/day-05-deep-modules.md` | 83 | APOSD | Chapter 7 | Not checked: confirm the chapter number, title, and that the chapter makes this claim. |
| 5 | `week-01/day-05-deep-modules.md` | 222 | APOSD | Chapter 4, "Modules Should Be Deep" | Not checked: confirm the chapter number, title, and that the chapter makes this claim. |
| 6 | `week-01/day-06-split-by-information.md` | 59 | APOSD | Chapter 9, "Better Together Or Better Apart?" | Not checked: confirm the chapter number, title, and that the chapter makes this claim. |
| 6 | `week-01/day-06-split-by-information.md` | 65 | TPP | Topic 10, "Orthogonality" | Topic title confirmed in the publisher's official contents list; number counted from that list and anchored by cross-references in the free excerpts. Check the topic's content supports the claim. |
| 6 | `week-01/day-06-split-by-information.md` | 80 | TPP | Topic 10, "Orthogonality" | Topic title confirmed in the publisher's official contents list; number counted from that list and anchored by cross-references in the free excerpts. Check the topic's content supports the claim. |
| 6 | `week-01/day-06-split-by-information.md` | 82 | APOSD | Chapter 9 | Not checked: confirm the chapter number, title, and that the chapter makes this claim. |
| 6 | `week-01/day-06-split-by-information.md` | 232 | APOSD | Chapter 9, "Better Together Or Better Apart?" | Not checked: confirm the chapter number, title, and that the chapter makes this claim. |
| 6 | `week-01/day-06-split-by-information.md` | 235 | TPP | Topics 9, "DRY - The Evils of Duplication" and 10, "Orthogonality" | Topic title confirmed in the publisher's official contents list; number counted from that list and anchored by cross-references in the free excerpts. Check the topic's content supports the claim. |
| 7 | `week-01/day-07-design-it-twice.md` | 59 | APOSD | Chapter 11, "Design it Twice" | Not checked: confirm the chapter number, title, and that the chapter makes this claim. |
| 7 | `week-01/day-07-design-it-twice.md` | 63 | TPP | Topic 12, "Tracer Bullets" | Topic title confirmed in the publisher's official contents list; number counted from that list and anchored by cross-references in the free excerpts. Check the topic's content supports the claim. |
| 7 | `week-01/day-07-design-it-twice.md` | 64 | TPP | Topic 13, "Prototypes and Post-it Notes" | Topic title confirmed in the publisher's official contents list; number counted from that list and anchored by cross-references in the free excerpts. Check the topic's content supports the claim. |
| 7 | `week-01/day-07-design-it-twice.md` | 79 | APOSD | Chapter 11 | Not checked: confirm the chapter number, title, and that the chapter makes this claim. |
| 7 | `week-01/day-07-design-it-twice.md` | 80 | TPP | Topic 12, "Tracer Bullets" | Topic title confirmed in the publisher's official contents list; number counted from that list and anchored by cross-references in the free excerpts. Check the topic's content supports the claim. |
| 7 | `week-01/day-07-design-it-twice.md` | 81 | TPP | Topic 13, "Prototypes and Post-it Notes" | Topic title confirmed in the publisher's official contents list; number counted from that list and anchored by cross-references in the free excerpts. Check the topic's content supports the claim. |
| 7 | `week-01/day-07-design-it-twice.md` | 246 | APOSD | Chapter 11, "Design it Twice" | Not checked: confirm the chapter number, title, and that the chapter makes this claim. |
| 7 | `week-01/day-07-design-it-twice.md` | 249 | TPP | Topics 12, "Tracer Bullets" and 13, "Prototypes and Post-it Notes" | Topic title confirmed in the publisher's official contents list; number counted from that list and anchored by cross-references in the free excerpts. Check the topic's content supports the claim. |
| 8 | `week-02/day-08-what-each-failure-means.md` | 59 | APOSD | Chapter 10, "Define Errors Out Of Existence" | Not checked: confirm the chapter number, title, and that the chapter makes this claim. |
| 8 | `week-02/day-08-what-each-failure-means.md` | 63 | TPP | Topic 24, "Dead Programs Tell No Lies" | Topic title confirmed in the publisher's official contents list; number counted from that list and anchored by cross-references in the free excerpts. Check the topic's content supports the claim. |
| 8 | `week-02/day-08-what-each-failure-means.md` | 64 | TPP | Topic 25, "Assertive Programming" | Topic title confirmed in the publisher's official contents list; number counted from that list and anchored by cross-references in the free excerpts. Check the topic's content supports the claim. |
| 8 | `week-02/day-08-what-each-failure-means.md` | 78 | APOSD | Chapter 10 | Not checked: confirm the chapter number, title, and that the chapter makes this claim. |
| 8 | `week-02/day-08-what-each-failure-means.md` | 79 | APOSD | Chapter 10 | Not checked: confirm the chapter number, title, and that the chapter makes this claim. |
| 8 | `week-02/day-08-what-each-failure-means.md` | 80 | TPP | Topic 24, "Dead Programs Tell No Lies" | Topic title confirmed in the publisher's official contents list; number counted from that list and anchored by cross-references in the free excerpts. Check the topic's content supports the claim. |
| 8 | `week-02/day-08-what-each-failure-means.md` | 203 | APOSD | Chapter 10, "Define Errors Out Of Existence" | Not checked: confirm the chapter number, title, and that the chapter makes this claim. |
| 8 | `week-02/day-08-what-each-failure-means.md` | 206 | TPP | Topics 24, "Dead Programs Tell No Lies" and 25, "Assertive Programming" | Topic title confirmed in the publisher's official contents list; number counted from that list and anchored by cross-references in the free excerpts. Check the topic's content supports the claim. |
| 9 | `week-02/day-09-tests-are-evidence.md` | 61 | TPP | Topic 41, "Test to Code" | Topic title confirmed in the publisher's official contents list; number counted from that list and anchored by cross-references in the free excerpts. Check the topic's content supports the claim. |
| 9 | `week-02/day-09-tests-are-evidence.md` | 63 | TPP | Topic 42, "Property-Based Testing" | Topic title confirmed in the publisher's official contents list; number counted from that list and anchored by cross-references in the free excerpts. Check the topic's content supports the claim. |
| 9 | `week-02/day-09-tests-are-evidence.md` | 82 | TPP | Topic 42, "Property-Based Testing" | Topic title confirmed in the publisher's official contents list; number counted from that list and anchored by cross-references in the free excerpts. Check the topic's content supports the claim. |
| 9 | `week-02/day-09-tests-are-evidence.md` | 222 | TPP | Topics 41, "Test to Code" and 42, "Property-Based Testing" | Topic title confirmed in the publisher's official contents list; number counted from that list and anchored by cross-references in the free excerpts. Check the topic's content supports the claim. |
| 10 | `week-02/day-10-volatile-dependencies.md` | 68 | APOSD | Chapter 5, "Information Hiding (and Leakage)" | Not checked: confirm the chapter number, title, and that the chapter makes this claim. |
| 10 | `week-02/day-10-volatile-dependencies.md` | 69 | APOSD | Chapter 7, "Different Layer, Different Abstraction" | Not checked: confirm the chapter number, title, and that the chapter makes this claim. |
| 10 | `week-02/day-10-volatile-dependencies.md` | 70 | APOSD | Chapter 8, "Pull Complexity Downwards" | Not checked: confirm the chapter number, title, and that the chapter makes this claim. |
| 10 | `week-02/day-10-volatile-dependencies.md` | 73 | TPP | Topic 28, "Decoupling" | Topic title confirmed in the publisher's official contents list; number counted from that list and anchored by cross-references in the free excerpts. Check the topic's content supports the claim. |
| 10 | `week-02/day-10-volatile-dependencies.md` | 220 | APOSD | Chapters 5, 7 and 8 | Not checked: confirm the chapter number, title, and that the chapter makes this claim. |
| 11 | `week-02/day-11-refactor-under-evidence.md` | 57 | TPP | Topic 40, "Refactoring" | Topic title confirmed in the publisher's official contents list; number counted from that list and anchored by cross-references in the free excerpts. Check the topic's content supports the claim. |
| 11 | `week-02/day-11-refactor-under-evidence.md` | 58 | TPP | Topic 19, "Version Control" | Topic title confirmed in the publisher's official contents list; number counted from that list and anchored by cross-references in the free excerpts. Check the topic's content supports the claim. |
| 11 | `week-02/day-11-refactor-under-evidence.md` | 60 | APOSD | Chapter 16, "Modifying Existing Code" | Not checked: confirm the chapter number, title, and that the chapter makes this claim. |
| 11 | `week-02/day-11-refactor-under-evidence.md` | 75 | TPP | Topic 40, "Refactoring" | Topic title confirmed in the publisher's official contents list; number counted from that list and anchored by cross-references in the free excerpts. Check the topic's content supports the claim. |
| 11 | `week-02/day-11-refactor-under-evidence.md` | 79 | TPP | Topic 19, "Version Control" | Topic title confirmed in the publisher's official contents list; number counted from that list and anchored by cross-references in the free excerpts. Check the topic's content supports the claim. |
| 11 | `week-02/day-11-refactor-under-evidence.md` | 248 | TPP | Topics 40, "Refactoring" and 19, "Version Control" | Topic title confirmed in the publisher's official contents list; number counted from that list and anchored by cross-references in the free excerpts. Check the topic's content supports the claim. |
| 11 | `week-02/day-11-refactor-under-evidence.md` | 251 | APOSD | Chapter 16, "Modifying Existing Code" | Not checked: confirm the chapter number, title, and that the chapter makes this claim. |
| 12 | `week-02/day-12-language-from-examples.md` | 67 | DDD | Chapter 1, "Crunching Knowledge" | Concept checked in Evans's free DDD Reference; confirm the chapter number and title, and that the chapter makes this claim. |
| 12 | `week-02/day-12-language-from-examples.md` | 68 | DDD | Chapter 2, "Communication and the Use of Language" | Concept checked in Evans's free DDD Reference; confirm the chapter number and title, and that the chapter makes this claim. |
| 12 | `week-02/day-12-language-from-examples.md` | 69 | DDD | Chapter 3, "Binding Model and Implementation" | Concept checked in Evans's free DDD Reference; confirm the chapter number and title, and that the chapter makes this claim. |
| 12 | `week-02/day-12-language-from-examples.md` | 87 | DDD | Chapter 2 | Concept checked in Evans's free DDD Reference; confirm the chapter number and title, and that the chapter makes this claim. |
| 12 | `week-02/day-12-language-from-examples.md` | 88 | DDD | Chapter 1 | Concept checked in Evans's free DDD Reference; confirm the chapter number and title, and that the chapter makes this claim. |
| 12 | `week-02/day-12-language-from-examples.md` | 212 | DDD | Chapters 1 to 3 | Concept checked in Evans's free DDD Reference; confirm the chapter number and title, and that the chapter makes this claim. |
| 13 | `week-02/day-13-entities-values-services.md` | 53 | DDD | Chapter 5, "A Model Expressed in Software" | Concept checked in Evans's free DDD Reference; confirm the chapter number and title, and that the chapter makes this claim. |
| 13 | `week-02/day-13-entities-values-services.md` | 58 | DDD | Chapter 4, "Isolating the Domain" | Concept checked in Evans's free DDD Reference; confirm the chapter number and title, and that the chapter makes this claim. |
| 13 | `week-02/day-13-entities-values-services.md` | 59 | DDD | Chapter 6, "The Life Cycle of a Domain Object" | Concept checked in Evans's free DDD Reference; confirm the chapter number and title, and that the chapter makes this claim. |
| 13 | `week-02/day-13-entities-values-services.md` | 71 | DDD | Chapter 5 | Concept checked in Evans's free DDD Reference; confirm the chapter number and title, and that the chapter makes this claim. |
| 13 | `week-02/day-13-entities-values-services.md` | 72 | DDD | Chapter 5 | Concept checked in Evans's free DDD Reference; confirm the chapter number and title, and that the chapter makes this claim. |
| 13 | `week-02/day-13-entities-values-services.md` | 73 | DDD | Chapter 5 | Concept checked in Evans's free DDD Reference; confirm the chapter number and title, and that the chapter makes this claim. |
| 13 | `week-02/day-13-entities-values-services.md` | 224 | DDD | Chapters 4 and 6 | Concept checked in Evans's free DDD Reference; confirm the chapter number and title, and that the chapter makes this claim. |
| 14 | `week-02/day-14-context-boundaries.md` | 70 | DDD | Chapter 14, "Maintaining Model Integrity" | Concept checked in Evans's free DDD Reference; confirm the chapter number and title, and that the chapter makes this claim. |
| 14 | `week-02/day-14-context-boundaries.md` | 89 | DDD | Chapter 14 | Concept checked in Evans's free DDD Reference; confirm the chapter number and title, and that the chapter makes this claim. |
| 14 | `week-02/day-14-context-boundaries.md` | 90 | DDD | Chapter 14 | Concept checked in Evans's free DDD Reference; confirm the chapter number and title, and that the chapter makes this claim. |
| 14 | `week-02/day-14-context-boundaries.md` | 91 | DDD | Chapter 14 | Concept checked in Evans's free DDD Reference; confirm the chapter number and title, and that the chapter makes this claim. |
| 14 | `week-02/day-14-context-boundaries.md` | 231 | DDD | Chapter 14, "Maintaining Model Integrity" | Concept checked in Evans's free DDD Reference; confirm the chapter number and title, and that the chapter makes this claim. |
| 15 | `week-02/day-15-distil-the-core.md` | 60 | DDD | Chapter 15, "Distillation" | Concept checked in Evans's free DDD Reference; confirm the chapter number and title, and that the chapter makes this claim. |
| 15 | `week-02/day-15-distil-the-core.md` | 76 | DDD | Chapter 15 | Concept checked in Evans's free DDD Reference; confirm the chapter number and title, and that the chapter makes this claim. |
| 15 | `week-02/day-15-distil-the-core.md` | 77 | DDD | Chapter 15 | Concept checked in Evans's free DDD Reference; confirm the chapter number and title, and that the chapter makes this claim. |
| 15 | `week-02/day-15-distil-the-core.md` | 79 | DDD | Chapter 15 | Concept checked in Evans's free DDD Reference; confirm the chapter number and title, and that the chapter makes this claim. |
| 15 | `week-02/day-15-distil-the-core.md` | 80 | DDD | Chapter 15 | Concept checked in Evans's free DDD Reference; confirm the chapter number and title, and that the chapter makes this claim. |
| 15 | `week-02/day-15-distil-the-core.md` | 240 | DDD | Chapter 15, "Distillation" | Concept checked in Evans's free DDD Reference; confirm the chapter number and title, and that the chapter makes this claim. |
| 16 | `week-03/day-16-measurable-requirements.md` | 77 | TPP | Topic 5, "Good-Enough Software" | Topic title confirmed in the publisher's official contents list; number counted from that list and anchored by cross-references in the free excerpts. Check the topic's content supports the claim. |
| 16 | `week-03/day-16-measurable-requirements.md` | 223 | TPP | Topic 5, "Good-Enough Software" | Topic title confirmed in the publisher's official contents list; number counted from that list and anchored by cross-references in the free excerpts. Check the topic's content supports the claim. |
| 18 | `week-03/day-18-storage-trade-offs.md` | 81 | TPP | Topic 39, "Algorithm Speed" | Topic title confirmed in the publisher's official contents list; number counted from that list and anchored by cross-references in the free excerpts. Check the topic's content supports the claim. |
| 18 | `week-03/day-18-storage-trade-offs.md` | 231 | TPP | Topic 39, "Algorithm Speed" | Topic title confirmed in the publisher's official contents list; number counted from that list and anchored by cross-references in the free excerpts. Check the topic's content supports the claim. |
| 20 | `week-03/day-20-invariants-under-concurrency.md` | 69 | DDD | Chapter 6, "The Life Cycle of a Domain Object" | Concept checked in Evans's free DDD Reference; confirm the chapter number and title, and that the chapter makes this claim. |
| 20 | `week-03/day-20-invariants-under-concurrency.md` | 93 | DDD | Chapter 6 | Concept checked in Evans's free DDD Reference; confirm the chapter number and title, and that the chapter makes this claim. |
| 20 | `week-03/day-20-invariants-under-concurrency.md` | 268 | DDD | Chapter 6, "The Life Cycle of a Domain Object" | Concept checked in Evans's free DDD Reference; confirm the chapter number and title, and that the chapter makes this claim. |
| 22 | `week-04/day-22-deploy-reversibly.md` | 65 | TPP | Topic 11, "Reversibility" | Topic title confirmed in the publisher's official contents list; number counted from that list and anchored by cross-references in the free excerpts. Check the topic's content supports the claim. |
| 22 | `week-04/day-22-deploy-reversibly.md` | 66 | TPP | Topic 32, "Configuration" | Topic title confirmed in the publisher's official contents list; number counted from that list and anchored by cross-references in the free excerpts. Check the topic's content supports the claim. |
| 22 | `week-04/day-22-deploy-reversibly.md` | 83 | TPP | Topic 32, "Configuration" | Topic title confirmed in the publisher's official contents list; number counted from that list and anchored by cross-references in the free excerpts. Check the topic's content supports the claim. |
| 22 | `week-04/day-22-deploy-reversibly.md` | 84 | TPP | Topic 11, "Reversibility" | Topic title confirmed in the publisher's official contents list; number counted from that list and anchored by cross-references in the free excerpts. Check the topic's content supports the claim. |
| 22 | `week-04/day-22-deploy-reversibly.md` | 233 | TPP | Topics 11, "Reversibility" and 32, "Configuration" | Topic title confirmed in the publisher's official contents list; number counted from that list and anchored by cross-references in the free excerpts. Check the topic's content supports the claim. |
| 23 | `week-04/day-23-measure-before-optimizing.md` | 66 | APOSD | Chapter 20, "Designing for Performance" | Not checked: confirm the chapter number, title, and that the chapter makes this claim. |
| 23 | `week-04/day-23-measure-before-optimizing.md` | 73 | TPP | Topic 39, "Algorithm Speed" | Topic title confirmed in the publisher's official contents list; number counted from that list and anchored by cross-references in the free excerpts. Check the topic's content supports the claim. |
| 23 | `week-04/day-23-measure-before-optimizing.md` | 74 | APOSD | Chapter 20 | Not checked: confirm the chapter number, title, and that the chapter makes this claim. |
| 23 | `week-04/day-23-measure-before-optimizing.md` | 84 | APOSD | Chapter 20 | Not checked: confirm the chapter number, title, and that the chapter makes this claim. |
| 23 | `week-04/day-23-measure-before-optimizing.md` | 223 | APOSD | Chapter 20, "Designing for Performance" | Not checked: confirm the chapter number, title, and that the chapter makes this claim. |
| 24 | `week-04/day-24-design-for-failure.md` | 69 | APOSD | Chapter 10, "Define Errors Out Of Existence" | Not checked: confirm the chapter number, title, and that the chapter makes this claim. |
| 24 | `week-04/day-24-design-for-failure.md` | 72 | APOSD | Chapter 10 | Not checked: confirm the chapter number, title, and that the chapter makes this claim. |
| 24 | `week-04/day-24-design-for-failure.md` | 280 | APOSD | Chapter 10, "Define Errors Out Of Existence" | Not checked: confirm the chapter number, title, and that the chapter makes this claim. |

## Topics with no coverage in the books' free material

These parts rely on official documentation only, and need a book source if one exists:

- Day 16: how to measure quality (indicators, targets, percentiles).
- Day 17: comparing relational, document, and graph data models.
- Day 18: indexes and query plans.
- Day 19: schema migrations.
- Day 20: database isolation levels.
- Day 21: logging, metrics, and alerting.
- Day 24: retries, backoff, timeouts, and idempotency.
