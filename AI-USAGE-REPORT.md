# AI-USAGE-REPORT.md

## Overview

This report reflects on how AI was used while planning and building this repository. The goal was not to hide AI usage, but to document where it helped, where it needed correction, and what remained the student's responsibility. The project itself is intentionally small: a URL shortener with a minimal frontend, local persistence, expiration support, and tests. That size made it a good candidate for observing AI workflow closely because the codebase stayed understandable while still containing enough moving parts to reveal both the strengths and the weaknesses of AI assistance.

The most important lesson is that AI was useful as a force multiplier, not as an unquestionable author. The workflow only became productive when each AI-generated idea was filtered through explicit product scope, architecture choices, test expectations, and manual review. Without that, the generated output would have looked complete while still containing hidden quality issues. In other words, the practical value of AI did not come from blind generation. It came from generating fast, reviewing hard, and integrating selectively.

## 1. What AI did and what I did

AI was most helpful during the structuring phase. It accelerated the creation of the repository skeleton, turned the assignment requirements into a concrete checklist, proposed a project topic that was small enough for the lab, and suggested an architecture that separated HTTP concerns from business logic. It also helped produce first drafts of planning documents such as the project definition, stack comparison, and architecture explanation. That meant the blank-page cost at the beginning of the assignment became much smaller.

AI also helped generate implementation scaffolding. For example, it proposed a service-oriented structure with a repository layer and domain model instead of writing everything inside request handlers. That pattern was helpful because it naturally supported testing. AI was also good at drafting repetitive but necessary code such as JSON serialization helpers, small HTTP response helpers, and frontend wiring for form submission and list refresh. It quickly translated the feature checklist into initial code shapes.

My own role was strongest in selection, correction, and boundary-setting. I chose the topic, constrained the scope, decided that zero-dependency Python was safer than a framework in an empty environment, and kept the project focused on features that could be explained during review. I also had to decide what not to build. That included skipping authentication, advanced analytics, and deployment features. Those omissions mattered because AI tends to over-expand when the prompt is not tightly bounded.

I also took responsibility for verification. Business rules such as expiration behavior, click counting, deletion, collision handling, and URL validation needed tests and human reasoning. AI could draft candidate implementations, but I still had to check whether the rules were internally consistent. For example, whether expired links should redirect or fail had to be defined intentionally. The code had to reflect those definitions in one place, and the tests had to prove it.

Finally, the reflective documents were not something I could responsibly outsource entirely. AI can draft a polished explanation, but the truthfulness requirement in the lab means the report must distinguish between polished language and actual understanding. The content here therefore treats AI as an assistant used to accelerate phrasing and structure, while the responsibility for honest claims remains with the human.

## 2. Hallucination examples and how they were corrected

The first hallucination risk appeared around the assignment PDF itself. Automated extraction did not initially provide clean readable content. Several tools either failed, produced binary garbage, or dropped parts of the document. If accepted as-is, that could have caused the repository structure to drift away from the teacher's actual requirements. The correction was to keep iterating on extraction methods, decode embedded font maps, and confirm the readable pages before implementation decisions were made. The lesson was that "the tool returned text" is not enough; the content itself must be checked for plausibility and completeness.

The second hallucination risk was architectural overreach. AI often defaults to modern frameworks such as FastAPI, React, or Express even when the environment is empty and dependency installation may not be feasible. That is a subtle kind of hallucination: not a fake fact, but a poor assumption disguised as a reasonable recommendation. The correction was to compare three stack options against the actual environment and choose the one with the lowest execution risk. That review prevented the repository from becoming dependent on unavailable packages.

Another example involved generated repository requirements. Some code-style sections in the PDF were harder to decode than the plain text sections. AI could easily have "filled in the gaps" with invented filenames or folders that looked standard but did not actually correspond to the assignment. The correction was to anchor the structure to explicit pass conditions found in the readable parts of the document: `PROJECT.md`, `ARCHITECTURE.md`, `STACK-COMPARISON.md`, `CLAUDE.md`, ADRs, AI logs, slash commands, tests, and reflection files. Where exact formatting remained uncertain, I chose conservative naming that aligned with visible requirements rather than fabricating exotic structure.

These examples show that hallucination is not limited to obviously false code. It can also appear as confident assumptions, premature simplification, or invented completeness. The defense was to slow down and verify before integration.

## 3. Security and license attention

One security-sensitive area was URL validation. AI-generated code often accepts any string that looks vaguely like a URL. That can lead to malformed redirects, confusing runtime errors, or abuse if unsafe schemes are allowed. The code here therefore validates that the URL has an `http` or `https` scheme before accepting it. That is not a full production-grade security solution, but it is an intentional safety improvement over naive storage.

Another security concern is redirect behavior. A URL shortener is an open redirect system by nature, which means misuse is always possible. AI-generated code might implement redirection without documenting that tradeoff. Here the mitigation is mostly educational: keep the project local, clearly define the feature scope, and note that production use would require stronger controls such as abuse prevention, authentication, rate limiting, and reputation checks.

A third concern is persistence integrity. If repository writes are not atomic enough, JSON data could be corrupted on interruption. The implementation writes complete serialized content rather than appending fragments, which reduces but does not eliminate risk. AI might omit this nuance because the application still "works" in the happy path. Human review is what surfaces the operational caveat.

On the license side, using the Python standard library avoided dependency license complexity almost entirely. That was another reason the selected stack fit the assignment well. AI often recommends packages because they are convenient, but every external dependency also carries license, update, and trust implications. Choosing no third-party runtime dependencies simplified both compliance and explanation.

## 4. What AI made faster

AI was especially effective at speeding up first drafts. It transformed the assignment into a repository plan quickly, generated documentation skeletons, proposed folder layout, and created consistent naming across files. It also accelerated repetitive implementation steps such as model serialization, test case enumeration, frontend event handling, and markdown boilerplate. Without AI, the same repository would still be possible, but the startup cost and documentation burden would have been noticeably higher.

AI also improved throughput in the "what should exist" stage. Instead of manually deciding every file from scratch, I could validate and refine suggestions. That turns authoring into curation, which is faster when the suggestions are decent. The biggest productivity win was not that AI wrote perfect code; it was that it kept momentum high by ensuring the project never stayed blank for long.

## 5. What AI made slower

AI slowed things down whenever verification became expensive. Extracting the assignment from the PDF is a good example. Multiple tool paths failed or produced poor output, which meant extra work was needed just to obtain reliable requirements. In those moments, AI did not reduce effort; it increased the number of possible paths to investigate.

AI also slows down work if its suggestions are too broad for the actual task. Framework-heavy proposals, overengineered abstractions, or extra features can create review overhead larger than the time saved. I had to reject complexity several times and keep the project aligned with the lab's actual grading criteria. That pruning process is slower than writing directly when the AI output is miscalibrated.

Another place AI can be slower is in explanation drift. It tends to produce polished statements that sound complete before the details are truly checked. If accepted too early, that creates cleanup work later because the documents and implementation stop matching. Keeping them synchronized requires deliberate discipline.

## 6. Managing skill atrophy risk

The main skill atrophy risk is letting AI become the thinker while the human becomes a copy-paste operator. I tried to manage that by keeping the codebase small enough to explain end to end. The service layer, repository behavior, and test cases are all understandable without framework magic. That design choice matters because a student should be able to describe how request handling, validation, persistence, and redirects work without needing the AI present.

I also treated tests as a skill-preservation mechanism. Writing or reviewing edge cases forces close contact with the real behavior of the system. Even if AI drafts some test scenarios, the human still has to decide what the correct behavior should be. That pushes understanding back into the human rather than leaving it in the generated text.

A second mitigation is honest documentation. Writing down where AI helped and where it was wrong prevents the illusion that the work was fully self-generated. That honesty is educational: it reveals which skills are still strong, which areas depended on AI suggestions, and where more independent practice is needed.

Finally, if this were done over several real days rather than one constrained session, I would explicitly set aside periods of "AI-off" review where I explain the code to myself, rewrite a small part unaided, or derive a feature flow from memory. That would be the strongest direct defense against skill atrophy.

## Conclusion

AI was valuable in this lab because it accelerated structure, drafting, and scaffolding. It was risky when assumptions went unverified, when environmental constraints were ignored, or when polished text gave a false sense of completeness. The project therefore reinforces the course principle: verify, do not trust blindly. Good AI-assisted software construction is not passive acceptance. It is active collaboration with deliberate human control over scope, truthfulness, and quality.
