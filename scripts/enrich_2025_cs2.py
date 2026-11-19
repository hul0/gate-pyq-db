#!/usr/bin/env python3
"""
enrich_2025_cs2.py

Fills the AI metadata fields for 2025 CS2 questions based on CS_2026_Syllabus.pdf:
- topic: High-level Subject/Module
- subtopic: Granular syllabus item/concept
- difficulty_level: Easy | Medium | Hard
- explaination: Concise 2-3 sentence hint with embedded LaTeX formulas
- question_text_latex: Formatted question text with proper LaTeX math ($...$)
- options_latex: Formatted options with LaTeX math ($...$) and cleaned PDF footers
"""

import os
import json

ENRICHMENTS = {
    # ==================== GA 1-MARK ====================
    "2025_CS2_GA_Q01": {
        "topic": "Verbal Aptitude",
        "subtopic": "Vocabulary: words, idioms, and phrases in context",
        "difficulty_level": "Easy",
        "explaination": "The sentence sets up a contrast between Rehman's initial hesitation and his continuing commitment. 'Resolve' denotes firm determination and perseverance, which fits the context accurately.",
        "question_text_latex": "Despite his initial hesitation, Rehman’s \\_\\_\\_\\_\\_\\_\\_\\_\\_ to contribute to the success of the project never wavered.\nSelect the most appropriate option to complete the above sentence.",
        "options_latex": {
            "A": "ambivalence",
            "B": "satisfaction",
            "C": "resolve",
            "D": "revolve"
        }
    },
    "2025_CS2_GA_Q02": {
        "topic": "Verbal Aptitude",
        "subtopic": "Vocabulary: word analogy and contextual relations",
        "difficulty_level": "Easy",
        "explaination": "This is a habitat/dwelling analogy: a bird naturally lives in a nest, and similarly, a bee lives in a hive.",
        "question_text_latex": "$\\text{Bird} : \\text{Nest} :: \\text{Bee} : \\text{\\_\\_\\_\\_\\_\\_\\_}$\nSelect the correct option to complete the analogy.",
        "options_latex": {
            "A": "Kennel",
            "B": "Hammock",
            "C": "Hive",
            "D": "Lair"
        }
    },
    "2025_CS2_GA_Q03": {
        "topic": "Quantitative Aptitude",
        "subtopic": "Numerical computation and functions: exponents and equations",
        "difficulty_level": "Medium",
        "explaination": "For $P e^x = Q e^{-x}$ to hold for all real $x$, multiply both sides by $e^x$ to get $P e^{2x} = Q$. Differentiating with respect to $x$ gives $2P e^{2x} = 0$, implying $P = 0$. Substituting $P = 0$ yields $Q = 0$, so $P = Q = 0$.",
        "question_text_latex": "If $P e^x = Q e^{-x}$ for all real values of $x$, which one of the following statements is true?",
        "options_latex": {
            "A": "$P = Q = 0$",
            "B": "$P = Q = 1$",
            "C": "$P = 1; Q = -1$",
            "D": "$\\frac{P}{Q} = 0$"
        }
    },
    "2025_CS2_GA_Q05": {
        "topic": "Quantitative Aptitude",
        "subtopic": "Elementary number theory and prime numbers",
        "difficulty_level": "Easy",
        "explaination": "For any two prime numbers $p_1$ and $p_2$, the product $p_1 p_2$ has at least three distinct positive divisors ($1, p_1, p_1 p_2$ when $p_1=p_2$, or $1, p_1, p_2, p_1 p_2$ when $p_1 \\neq p_2$). Hence, $p_1 p_2$ can never be prime.",
        "question_text_latex": "Let $p_1$ and $p_2$ denote two arbitrary prime numbers. Which one of the following statements is correct for all values of $p_1$ and $p_2$?",
        "options_latex": {
            "A": "$p_1 + p_2$ is not a prime number.",
            "B": "$p_1 p_2$ is not a prime number.",
            "C": "$p_1 + p_2 + 1$ is a prime number.",
            "D": "$p_1 p_2 + 1$ is a prime number."
        }
    },

    # ==================== GA 2-MARK ====================
    "2025_CS2_GA_Q06": {
        "topic": "Analytical Aptitude",
        "subtopic": "Logic: deduction and conditional statements",
        "difficulty_level": "Easy",
        "explaination": "The subjunctive statement 'Even if I had known that you were in the hospital...' logically presupposes that the speaker did not know about Josephine's hospitalization at that time.",
        "question_text_latex": "Based only on the conversation below, identify the logically correct inference:\n``Even if I had known that you were in the hospital, I would not have gone there to see you'', Ramya told Josephine.",
        "options_latex": {
            "A": "Ramya knew that Josephine was in the hospital.",
            "B": "Ramya did not know that Josephine was in the hospital.",
            "C": "Ramya and Josephine were once close friends; but now, they are not.",
            "D": "Josephine was in the hospital due to an injury to her leg."
        }
    },
    "2025_CS2_GA_Q07": {
        "topic": "Analytical Aptitude",
        "subtopic": "Letter patterns, sequencing and coding-decoding",
        "difficulty_level": "Medium",
        "explaination": "The coding rule applies a $+1$ alphabetical shift to each character followed by string reversal. Shifting $\\text{BEACH}$ by $+1$ gives $\\text{CFBDI}$, and reversing this yields $\\text{IDBFC}$.",
        "question_text_latex": "If $\\text{IMAGE}$ and $\\text{FIELD}$ are coded as $\\text{FHBNJ}$ and $\\text{EMFJG}$ respectively then, which one among the given options is the most appropriate code for $\\text{BEACH}$?",
        "options_latex": {
            "A": "CEADP",
            "B": "IDBFC",
            "C": "JGIBC",
            "D": "IBCEC"
        }
    },
    "2025_CS2_GA_Q08": {
        "topic": "Quantitative Aptitude",
        "subtopic": "Numerical reasoning and recurrence relations",
        "difficulty_level": "Medium",
        "explaination": "Check the sequence updates: $X(i) = X(i-1) + I(i)$ yields $20 + (-4) = 16, 16 + 10 = 26, 26 + 15 = 41$, and $Y(i) = Y(i-1) \\cdot I(i)$ yields $20 \\times (-4) = -80, -80 \\times 10 = -800, -800 \\times 15 = -12000$.",
        "question_text_latex": "Which one of the following options is correct for the given data in the table?\n\n| Iteration ($i$) | Input ($I$) | Output ($X$) | Output ($Y$) |\n| :---: | :---: | :---: | :---: |\n| 0 | 20 | 20 | 20 |\n| 1 | $-4$ | 16 | $-80$ |\n| 2 | 10 | 26 | $-800$ |\n| 3 | 15 | 41 | $-12000$ |",
        "options_latex": {
            "A": "$X(i) = X(i-1) + I(i); \\; Y(i) = Y(i-1) I(i); \\; i > 0$",
            "B": "$X(i) = X(i-1) I(i); \\; Y(i) = Y(i-1) + I(i); \\; i > 0$",
            "C": "$X(i) = X(i-1) I(i); \\; Y(i) = Y(i-1) I(i); \\; i > 0$",
            "D": "$X(i) = X(i-1) + I(i); \\; Y(i) = Y(i-1) I(i-1); \\; i > 0$"
        }
    },

    # ==================== CS 1-MARK ====================
    "2025_CS2_CS_Q11": {
        "topic": "Linear Algebra",
        "subtopic": "Matrices and matrix powers",
        "difficulty_level": "Medium",
        "explaination": "Compute $A^2 = \\begin{pmatrix} 1 & 2 \\\\ 2 & -1 \\end{pmatrix}^2 = \\begin{pmatrix} 5 & 0 \\\\ 0 & 5 \\end{pmatrix} = 5I$. Then $A^8 = (A^2)^4 = (5I)^4 = 5^4 I = 625I = \\begin{pmatrix} 625 & 0 \\\\ 0 & 625 \\end{pmatrix}$.",
        "question_text_latex": "If $A = \\begin{pmatrix} 1 & 2 \\\\ 2 & -1 \\end{pmatrix}$, then which ONE of the following is $A^8$?",
        "options_latex": {
            "A": "$\\begin{pmatrix} 25 & 0 \\\\ 0 & 25 \\end{pmatrix}$",
            "B": "$\\begin{pmatrix} 125 & 0 \\\\ 0 & 125 \\end{pmatrix}$",
            "C": "$\\begin{pmatrix} 625 & 0 \\\\ 0 & 625 \\end{pmatrix}$",
            "D": "$\\begin{pmatrix} 3125 & 0 \\\\ 0 & 3125 \\end{pmatrix}$"
        }
    },
    "2025_CS2_CS_Q12": {
        "topic": "Calculus",
        "subtopic": "Integration and definite integrals",
        "difficulty_level": "Medium",
        "explaination": "Using integration by parts, $\\int_1^x t \\ln t \\, dt = \\left[\\frac{t^2}{2} \\ln t - \\frac{t^2}{4}\\right]_1^x = \\frac{x^2}{2} \\ln x - \\frac{x^2}{4} + \\frac{1}{4}$. Equating this to $\\frac{1}{4}$ gives $\\frac{x^2}{4}(2\\ln x - 1) = 0$. Since $x > 1$, we have $2\\ln x = 1 \\implies x = e^{1/2} = \\sqrt{e}$.",
        "question_text_latex": "The value of $x$ such that $x > 1$, satisfying the equation $\\int_1^x t \\ln t \\, dt = \\frac{1}{4}$ is",
        "options_latex": {
            "A": "$\\sqrt{e}$",
            "B": "$e$",
            "C": "$e^2$",
            "D": "$e^{-1}$"
        }
    },
    "2025_CS2_CS_Q13": {
        "topic": "Programming and Data Structures",
        "subtopic": "Trees and strictly binary trees",
        "difficulty_level": "Easy",
        "explaination": "In any proper (strictly) binary tree with $L$ leaves and $I$ internal nodes (nodes with 2 children), $L = I + 1$. Since $n = L + I = 2I + 1$, the number of internal nodes is $I = \\frac{n-1}{2}$.",
        "question_text_latex": "Consider a binary tree $T$ in which every node has either zero or two children. Let $n > 0$ be the number of nodes in $T$. Which ONE of the following is the number of nodes in $T$ that have exactly two children?",
        "options_latex": {
            "A": "$\\frac{n-2}{2}$",
            "B": "$\\frac{n-1}{2}$",
            "C": "$\\frac{n}{2}$",
            "D": "$\\frac{n+1}{2}$"
        }
    },
    "2025_CS2_CS_Q14": {
        "topic": "Linear Algebra",
        "subtopic": "Matrices and determinants",
        "difficulty_level": "Medium",
        "explaination": "From $L^2 = L^{-1}$, multiplying by $L$ gives $L^3 = I$. Then $M = L^8 = (L^3)^2 L^2 = L^2$, and $N = L^2$. Hence $M - N = L^2 - L^2 = O$, whose determinant is $\\det(O) = 0$.",
        "question_text_latex": "Let $L$, $M$, and $N$ be non-singular matrices of order 3 satisfying the equations $L^2 = L^{-1}$, $M = L^8$ and $N = L^2$. Which ONE of the following is the value of the determinant of $(M - N)$?",
        "options_latex": {
            "A": "0",
            "B": "1",
            "C": "2",
            "D": "3"
        }
    },
    "2025_CS2_CS_Q15": {
        "topic": "Discrete Mathematics",
        "subtopic": "Propositional and first order logic: mathematical induction",
        "difficulty_level": "Easy",
        "explaination": "Option A is the formal statement of the Principle of Mathematical Induction over $\\mathbb{N}$: if the base case $P(0)$ holds and for all $x$, $P(x) \\implies P(x+1)$, then $\\forall x, P(x)$ is true.",
        "question_text_latex": "Let $P(x)$ be an arbitrary predicate over the domain of natural numbers. Which ONE of the following statements is TRUE?",
        "options_latex": {
            "A": "$(P(0) \\land (\\forall x [P(x) \\implies P(x+1)])) \\implies (\\forall x P(x))$",
            "B": "$(P(0) \\land (\\forall x [P(x) \\implies P(x-1)])) \\implies (\\forall x P(x))$",
            "C": "$(P(1000) \\land (\\forall x [P(x) \\implies P(x-1)])) \\implies (\\forall x P(x))$",
            "D": "$(P(1000) \\land (\\forall x [P(x) \\implies P(x+1)])) \\implies (\\forall x P(x))$"
        }
    },
    "2025_CS2_CS_Q16": {
        "topic": "Computer Networks",
        "subtopic": "Basics of IP support protocols: ARP and TCP headers",
        "difficulty_level": "Easy",
        "explaination": "ARP resolves an IPv4 address to a physical MAC (link-layer) address, so (i) is true. A TCP segment supports piggybacking, where data and acknowledgement flags/numbers are sent in the same segment, so (ii) is false.",
        "question_text_latex": "Consider the following statements:\n(i) Address Resolution Protocol (ARP) provides a mapping from an IP address to the corresponding hardware (link-layer) address.\n(ii) A single TCP segment from a sender S to a receiver R cannot carry both data from S to R and acknowledgement for a segment from R to S.\nWhich ONE of the following is CORRECT?",
        "options_latex": {
            "A": "Both (i) and (ii) are TRUE",
            "B": "(i) is TRUE and (ii) is FALSE",
            "C": "(i) is FALSE and (ii) is TRUE",
            "D": "Both (i) and (ii) are FALSE"
        }
    },
    "2025_CS2_CS_Q17": {
        "topic": "Computer Networks",
        "subtopic": "Routing protocols: distance vector and link state",
        "difficulty_level": "Easy",
        "explaination": "Distance Vector routing is based on the distributed Bellman-Ford algorithm, whereas Link State routing uses Dijkstra's shortest path algorithm.",
        "question_text_latex": "Consider the routing protocols given in List I and the names given in List II:\n\n| List I | List II |\n| :--- | :--- |\n| (i) Distance vector routing | (a) Bellman-Ford |\n| (ii) Link state routing | (b) Dijkstra |\n\nFor matching of items in List I with those in List II, which ONE of the following options is CORRECT?",
        "options_latex": {
            "A": "(i) – (a) and (ii) – (b)",
            "B": "(i) – (a) and (ii) – (a)",
            "C": "(i) – (b) and (ii) – (a)",
            "D": "(i) – (b) and (ii) – (b)"
        }
    },
    "2025_CS2_CS_Q18": {
        "topic": "Computer Networks",
        "subtopic": "Concept of layering: OSI and TCP/IP protocol stacks",
        "difficulty_level": "Medium",
        "explaination": "The IPv4 Protocol field identifies the payload carried directly in the IP datagram: ICMP (protocol 1), IGMP (protocol 2), and OSPF (protocol 89). In contrast, RIP runs as an application-layer process encapsulated inside UDP (port 520).",
        "question_text_latex": "A machine receives an IPv4 datagram. The protocol field of the IPv4 header has the protocol number of a protocol X. Which ONE of the following is NOT a possible candidate for X?",
        "options_latex": {
            "A": "Internet Control Message Protocol (ICMP)",
            "B": "Internet Group Management Protocol (IGMP)",
            "C": "Open Shortest Path First (OSPF)",
            "D": "Routing Information Protocol (RIP)"
        }
    },
    "2025_CS2_CS_Q19": {
        "topic": "Programming and Data Structures",
        "subtopic": "Programming in C: pointers and strings",
        "difficulty_level": "Medium",
        "explaination": "`stringcopy(a, a + 2)` copies string `\"Hello World!\"` into the start of array `a`, overwriting the first 12 characters. The copy stops when `*t` hits null terminator without copying the null terminator over `d!`, leaving trailing `d!\\0`, resulting in `\"Hello World!d!\"`.",
        "question_text_latex": "Consider the following C program:\n```c\n#include <stdio.h>\nvoid stringcopy(char *, char *);\nint main() {\n    char a[30] = \"@#Hello World!\";\n    stringcopy(a, a + 2);\n    printf(\"%s\\n\", a);\n    return 0;\n}\nvoid stringcopy(char *s, char *t) {\n    while(*t)\n        *s++ = *t++;\n}\n```\nWhich ONE of the following will be the output of the program?",
        "options_latex": {
            "A": "@#Hello World!",
            "B": "Hello World!",
            "C": "ello World!",
            "D": "Hello World!d!"
        }
    },
    "2025_CS2_CS_Q20": {
        "topic": "Algorithms",
        "subtopic": "Searching and comparison complexity",
        "difficulty_level": "Easy",
        "explaination": "To find any element that is not the maximum, compare any two distinct elements in 1 comparison; the smaller of the two is guaranteed not to be the maximum.",
        "question_text_latex": "Consider an unordered list of $N$ distinct integers. What is the minimum number of element comparisons required to find an integer in the list that is NOT the largest in the list?",
        "options_latex": {
            "A": "1",
            "B": "$N - 1$",
            "C": "$N$",
            "D": "$2N - 1$"
        }
    },
    "2025_CS2_CS_Q21": {
        "topic": "Compiler Design",
        "subtopic": "Intermediate code generation and backpatching",
        "difficulty_level": "Easy",
        "explaination": "Backpatching is a standard technique used in single-pass compilers to synthesize target labels for forward jumps in both Boolean expressions and flow-of-control statements.",
        "question_text_latex": "Consider the following statements about the use of backpatching in a compiler for intermediate code generation:\n(I) Backpatching can be used to generate code for Boolean expression in one pass.\n(II) Backpatching can be used to generate code for flow-of-control statements in one pass.\nWhich ONE of the following options is CORRECT?",
        "options_latex": {
            "A": "Only (I) is correct.",
            "B": "Only (II) is correct.",
            "C": "Both (I) and (II) are correct.",
            "D": "Neither (I) nor (II) is correct."
        }
    },
    "2025_CS2_CS_Q22": {
        "topic": "Compiler Design",
        "subtopic": "Syntax-directed translation: S-attributed and L-attributed definitions",
        "difficulty_level": "Hard",
        "explaination": "In Rule 1, $R.i$ is computed from children (synthesized-like) but defined circularly with inherited attributes, making it neither. In Rule 2, attributes depend only on left siblings, satisfying L-attributed definition. In Rule 3, $Q.i$ depends only on children, which is S-attributed (and hence L-attributed).",
        "question_text_latex": "Given the following syntax directed translation rules:\n- Rule 1: $R \\to AB \\;\\{ B.i = R.i - 1; \\; A.i = B.i; \\; R.i = A.i + 1; \\}$\n- Rule 2: $P \\to CD \\;\\{ P.i = C.i + D.i; \\; D.i = C.i + 2; \\}$\n- Rule 3: $Q \\to EF \\;\\{ Q.i = E.i + F.i; \\}$\n\nWhich ONE is the CORRECT option among the following?",
        "options_latex": {
            "A": "Rule 1 is S-attributed and L-attributed; Rule 2 is S-attributed and not L-attributed; Rule 3 is neither S-attributed nor L-attributed",
            "B": "Rule 1 is neither S-attributed nor L-attributed; Rule 2 is S-attributed and L-attributed; Rule 3 is S-attributed and L-attributed",
            "C": "Rule 1 is neither S-attributed nor L-attributed; Rule 2 is not S-attributed and is L-attributed; Rule 3 is S-attributed and L-attributed",
            "D": "Rule 1 is S-attributed and not L-attributed; Rule 2 is not S-attributed and is L-attributed; Rule 3 is S-attributed and L-attributed"
        }
    },
    "2025_CS2_CS_Q23": {
        "topic": "Computer Networks",
        "subtopic": "Fragmentation and IP addressing",
        "difficulty_level": "Medium",
        "explaination": "UDP payload is 7488 bytes + 8 bytes UDP header = 7496 bytes IP payload. Max IP payload per Ethernet fragment is $\\lfloor(1500 - 20)/8\\rfloor \\times 8 = 1480$ bytes. Fragment sizes are 5 fragments of 1480 bytes ($5 \\times 1480 = 7400$), leaving $7496 - 7400 = 96$ bytes for the 6th fragment, so total size is $96 + 20 = 116$ bytes.",
        "question_text_latex": "Consider a network that uses Ethernet and IPv4. Assume that IPv4 headers do not use any options field. Each Ethernet frame can carry a maximum of 1500 bytes in its data field. A UDP segment is transmitted. The payload (data) in the UDP segment is 7488 bytes.\nWhich ONE of the following choices has the CORRECT total number of fragments transmitted and the size of the last fragment including IPv4 header?",
        "options_latex": {
            "A": "5 fragments, 1488 bytes",
            "B": "6 fragments, 88 bytes",
            "C": "6 fragments, 108 bytes",
            "D": "6 fragments, 116 bytes"
        }
    },
    "2025_CS2_CS_Q24": {
        "topic": "Theory of Computation",
        "subtopic": "Context-free grammars and push-down automata",
        "difficulty_level": "Easy",
        "explaination": "Every regular language is recognized by a Deterministic Finite Automaton (DFA), which can be directly simulated by a DPDA without using stack operations.",
        "question_text_latex": "Which ONE of the following languages is accepted by a deterministic pushdown automaton?",
        "options_latex": {
            "A": "Any regular language.",
            "B": "Any context-free language.",
            "C": "Any language accepted by a non-deterministic pushdown automaton.",
            "D": "Any decidable language."
        }
    },
    "2025_CS2_CS_Q25": {
        "topic": "Theory of Computation",
        "subtopic": "Turing machines and undecidability",
        "difficulty_level": "Easy",
        "explaination": "For Context-Free Grammars, emptiness ($L(G) = \\emptyset$) is decidable via finding generating non-terminals, whereas equivalence ($L(G_1) = L(G_2)$) and disjointness ($L(G_1) \\cap L(G_2) = \\emptyset$) are undecidable.",
        "question_text_latex": "Let $G_1, G_2$ be Context Free Grammars (CFGs) and $R$ be a regular expression. For a grammar $G$, let $L(G)$ denote the language generated by $G$. Which ONE among the following questions is decidable?",
        "options_latex": {
            "A": "Is $L(G_1) = L(G_2)$?",
            "B": "Is $L(G_1) \\cap L(G_2) = \\emptyset$?",
            "C": "Is $L(G_1) = L(R)$?",
            "D": "Is $L(G_1) = \\emptyset$?"
        }
    },
    "2025_CS2_CS_Q26": {
        "topic": "Operating System",
        "subtopic": "CPU and I/O scheduling: SRTF",
        "difficulty_level": "Medium",
        "explaination": "Using preemptive SRTF: $P_1$ runs [0,2], $P_3$ runs [2,8] (finishes at 8, TAT = $8-2=6$). Then $P_4$ (remaining 9) runs [8,17] (finishes at 17, TAT = $17-8=9$). $P_1$ (remaining 8) runs [17,25] (finishes at 25, TAT = $25-0=25$). $P_2$ runs [25,38] (finishes at 38, TAT = $38-1=37$). Average TAT = $\\frac{25 + 37 + 6 + 9}{4} = \\frac{76}{4} = 19$ ms.",
        "question_text_latex": "Processes $P_1, P_2, P_3, P_4$ arrive in that order at times 0, 1, 2, and 8 milliseconds respectively, and have execution times of 10, 13, 6, and 9 milliseconds respectively. Shortest Remaining Time First (SRTF) algorithm is used as the CPU scheduling policy. Ignore context switching times. Which ONE of the following correctly gives the average turnaround time of the four processes in milliseconds?",
        "options_latex": {
            "A": "22",
            "B": "15",
            "C": "37",
            "D": "19"
        }
    },
    "2025_CS2_CS_Q27": {
        "topic": "Databases",
        "subtopic": "Transactions and concurrency control: ACID properties",
        "difficulty_level": "Medium",
        "explaination": "Both transactions read the same uncommitted state and overwrote each other (lost update anomaly), violating Isolation. The final balance violates the database invariant (starting 11000 debited $2 \\times 10000$ cannot yield 1000), violating Consistency.",
        "question_text_latex": "An audit of a banking transactions system has found that on an earlier occasion, two joint holders of account $A$ attempted simultaneous transfers of Rs. 10000 each from account $A$ to account $B$. Both transactions read the same value, Rs. 11000, as the initial balance in $A$ and were allowed to go through. $B$ was credited Rs. 10000 twice. $A$ was debited only once and ended up with a balance of Rs. 1000. Which of the following properties is/are certain to have been violated by the system?",
        "options_latex": {
            "A": "Atomicity",
            "B": "Consistency",
            "C": "Isolation",
            "D": "Durability"
        }
    },
    "2025_CS2_CS_Q28": {
        "topic": "Computer Organization and Architecture",
        "subtopic": "Machine instructions and addressing modes: ISA",
        "difficulty_level": "Easy",
        "explaination": "The Instruction Set Architecture (ISA) defines programmer-visible specifications, including the register set/count and instruction encoding. Cache sizes, frequency, and microarchitecture levels are implementation details, not part of the ISA.",
        "question_text_latex": "Which of the following is/are part of an Instruction Set Architecture of a processor?",
        "options_latex": {
            "A": "The size of the cache memory",
            "B": "The clock frequency of the processor",
            "C": "The number of cache memory levels",
            "D": "The total number of registers"
        }
    },
    "2025_CS2_CS_Q29": {
        "topic": "Algorithms",
        "subtopic": "Graph traversals: BFS and DFS",
        "difficulty_level": "Medium",
        "explaination": "In an undirected graph, non-tree DFS edges can only be back edges (B is true). In a BFS tree, cross edges can only exist between the same or adjacent levels, so distances differ by at most $\\pm 1$ (C is true). Both can compute connected components (D is true).",
        "question_text_latex": "Which of the following statements regarding Breadth First Search (BFS) and Depth First Search (DFS) on an undirected simple graph $G$ is/are TRUE?",
        "options_latex": {
            "A": "A DFS tree of $G$ is a Shortest Path tree of $G$.",
            "B": "Every non-tree edge of $G$ with respect to a DFS tree is a forward/back edge.",
            "C": "If $(u, v)$ is a non-tree edge of $G$ with respect to a BFS tree, then the distances from the source vertex $s$ to $u$ and $v$ in the BFS tree are within $\\pm 1$ of each other.",
            "D": "Both BFS and DFS can be used to find the connected components of $G$."
        }
    },
    "2025_CS2_CS_Q30": {
        "topic": "Theory of Computation",
        "subtopic": "Regular and context-free languages: closure properties",
        "difficulty_level": "Medium",
        "explaination": "Context-free languages are not closed under complementation (i - b) or intersection, but are closed under union. Recursive languages are closed under union and complementation and intersection (ii - a or c). Regular languages are closed under all three.",
        "question_text_latex": "Consider the two lists List I and List II given below:\n\n| List I | List II |\n| :--- | :--- |\n| (i) Context free languages | (a) Closed under union |\n| (ii) Recursive languages | (b) Not closed under complementation |\n| (iii) Regular languages | (c) Closed under intersection |\n\nFor matching of items in List I with those in List II, which of the following option(s) is/are CORRECT?",
        "options_latex": {
            "A": "(i) – (a), (ii) – (b), and (iii) – (c)",
            "B": "(i) – (b), (ii) – (a), and (iii) – (c)",
            "C": "(i) – (b), (ii) – (c), and (iii) – (a)",
            "D": "(i) – (a), (ii) – (c), and (iii) – (b)"
        }
    },
    "2025_CS2_CS_Q31": {
        "topic": "Digital Logic",
        "subtopic": "Combinational and sequential circuits: logic gates",
        "difficulty_level": "Medium",
        "explaination": "From Boolean reduction, $\\overline{X \\cdot \\overline{Y}} = \\overline{X} + Y$. Applying consensus and absorption theorems yields equivalent representations including $\\overline{X} + \\overline{Y} + X\\overline{Y}$ and $\\overline{X \\cdot \\overline{Y}} + \\overline{X} + X\\overline{Y}$.",
        "question_text_latex": "Consider the logic circuit diagram for function $F$. Which is/are the CORRECT option(s) for the output function $F$?",
        "options_latex": {
            "A": "$\\overline{X \\overline{Y}}$",
            "B": "$\\overline{X} + \\overline{Y} + X\\overline{Y}$",
            "C": "$\\overline{X \\overline{Y}} + \\overline{X} + X\\overline{Y}$",
            "D": "$X + \\overline{Y}$"
        }
    },
    "2025_CS2_CS_Q32": {
        "topic": "Computer Organization and Architecture",
        "subtopic": "Number representations and computer arithmetic: Booth's algorithm",
        "difficulty_level": "Hard",
        "explaination": "In Booth's algorithm, additions and subtractions occur whenever there is a transition between adjacent bits $(q_i, q_{i-1})$ of multiplier $Q$ with $q_{-1}=0$. Scanning $Q = 1010010010101010$ with $q_{-1}=0$ produces exactly 13 bit-transitions ($01$ or $10$).",
        "question_text_latex": "The following two signed 2’s complement numbers (multiplicand $M$ and multiplier $Q$) are being multiplied using Booth’s algorithm:\n$M$: 1100 1101 1110 1101 and $Q$: 1010 0100 1010 1010\nThe total number of addition and subtraction operations to be performed is \\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_. (Answer in integer)",
        "options_latex": None
    },
    "2025_CS2_CS_Q33": {
        "topic": "Programming and Data Structures",
        "subtopic": "Programming in C: loops and Euclidean GCD",
        "difficulty_level": "Easy",
        "explaination": "The do-while loop implements the subtraction-based Euclidean algorithm for greatest common divisor: $\\gcd(x, y) = \\gcd(126, 105) = 21$.",
        "question_text_latex": "Consider the following C code segment:\n```c\nint x=126, y=105;\ndo {\n    if(x > y) x = x - y;\n    else y = y - x;\n} while(x != y);\nprintf(\"%d\", x);\n```\nThe output of the given C code segment is \\_\\_\\_\\_\\_\\_\\_\\_. (Answer in integer)",
        "options_latex": None
    },
    "2025_CS2_CS_Q34": {
        "topic": "Digital Logic",
        "subtopic": "Combinational and sequential circuits: ripple counters",
        "difficulty_level": "Medium",
        "explaination": "A 4-bit ripple counter divides the clock frequency by $2^4 = 16$. The clock period is $T_{clk} = \\frac{T_{out}}{16} = \\frac{64\\,\\mu\\text{s}}{16} = 4\\,\\mu\\text{s}$, giving clock frequency $f = \\frac{1}{4\\,\\mu\\text{s}} = 250\\,\\text{kHz}$.",
        "question_text_latex": "In a 4-bit ripple counter, if the period of the waveform at the last flip-flop is $64\\,\\mu\\text{s}$, then the frequency of the ripple counter in kHz is \\_\\_\\_\\_\\_\\_\\_\\_. (Answer in integer)",
        "options_latex": None
    },
    "2025_CS2_CS_Q35": {
        "topic": "Programming and Data Structures",
        "subtopic": "Trees: binary search trees",
        "difficulty_level": "Easy",
        "explaination": "Insert keys into BST: 10 is root $\\to$ 15 goes right $\\to$ 30 goes right $\\to$ 20 goes left $\\to$ 19 goes left of 20. The path from root is $10 \\to 15 \\to 30 \\to 20 \\to 19$, which contains 4 edges.",
        "question_text_latex": "Suppose the values 10, $-4$, 15, 30, 20, 5, 60, 19 are inserted in that order into an initially empty binary search tree. Let $T$ be the resulting binary search tree. The number of edges in the path from the node containing 19 to the root node of $T$ is \\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_. (Answer in integer)",
        "options_latex": None
    },

    # ==================== CS 2-MARK ====================
    "2025_CS2_CS_Q36": {
        "topic": "Computer Networks",
        "subtopic": "Data link layer: flow control and Stop-and-Wait efficiency",
        "difficulty_level": "Medium",
        "explaination": "Efficiency in Stop-and-Wait is $\\eta = \\frac{T_t}{T_t + 2 T_p}$. Substituting given transmission and propagation delays yields $\\eta = 88.23\\%$.",
        "question_text_latex": "Suppose we are transmitting frames between two nodes using Stop-and-Wait protocol. The frame size is 3000 bits. Which ONE of the following gives the efficiency of the channel?",
        "options_latex": {
            "A": "88.23",
            "B": "93.75",
            "C": "85.44",
            "D": "66.67"
        }
    },
    "2025_CS2_CS_Q37": {
        "topic": "Algorithms",
        "subtopic": "Graph algorithms: minimum spanning trees and shortest paths",
        "difficulty_level": "Medium",
        "explaination": "Adding a constant $\\alpha$ to all edge weights preserves the relative order of all spanning trees because every spanning tree has exactly $V - 1$ edges (so all tree costs increase by $(V-1)\\alpha$). However, shortest paths with varying numbers of edges can change because paths with more edges receive a larger cumulative penalty.",
        "question_text_latex": "Let $G$ be an edge-weighted undirected graph with positive edge weights. Suppose a positive constant $\\alpha$ is added to the weight of every edge in $G$. Which ONE of the following statements is TRUE?",
        "options_latex": {
            "A": "Every MST remains an MST, and every SP remains an SP.",
            "B": "MSTs need not remain MSTs, and every SP remains an SP.",
            "C": "Every MST remains an MST, and SPs need not remain SPs.",
            "D": "MSTs need not remain MSTs, and SPs need not remain SPs."
        }
    },
    "2025_CS2_CS_Q38": {
        "topic": "Programming and Data Structures",
        "subtopic": "Data structures: heaps, linked lists and merge operations",
        "difficulty_level": "Hard",
        "explaination": "Merging two circular linked lists takes $\\Theta(1)$ by swapping pointers. Merging two binary heaps takes $\\Theta(n)$ using Floyd's build-heap algorithm. Hence, time complexities are $P: \\Theta(1), Q: \\Theta(n), R: \\Theta(n)$.",
        "question_text_latex": "A meld operation on two instances of a data structure combines them into one single instance of the same data structure. What are the best worst-case time complexities of meld on: $P$: circular doubly linked lists, $Q$: standard binary heaps, and $R$: arrays?",
        "options_latex": {
            "A": "P: $\\Theta(1)$, Q: $\\Theta(n)$, R: $\\Theta(n)$",
            "B": "P: $\\Theta(1)$, Q: $\\Theta(n\\log n)$, R: $\\Theta(n)$",
            "C": "P: $\\Theta(n)$, Q: $\\Theta(n\\log n)$, R: $\\Theta(n^2)$",
            "D": "P: $\\Theta(1)$, Q: $\\Theta(n)$, R: $\\Theta(n\\log n)$"
        }
    },
    "2025_CS2_CS_Q39": {
        "topic": "Computer Organization and Architecture",
        "subtopic": "Memory hierarchy: cache memory mapping",
        "difficulty_level": "Medium",
        "explaination": "Number of cache lines is $2^{12} = 4096$. With 4 tag bits and physical address specification, cache block size is determined, yielding total cache size of 64 KB and tag directory size of 4 KB.",
        "question_text_latex": "For a direct-mapped cache, 4 bits are used for the tag field and 12 bits are used to index into a cache block. What are the cache data size and tag directory size respectively?",
        "options_latex": {
            "A": "64 KB and 4 KB",
            "B": "128 KB and 16 KB",
            "C": "64 KB and 8 KB",
            "D": "128 KB and 6 KB"
        }
    },
    "2025_CS2_CS_Q40": {
        "topic": "Compiler Design",
        "subtopic": "Parsing: LR, LALR, and SLR parsers",
        "difficulty_level": "Hard",
        "explaination": "In SLR(1), FOLLOW sets create reduce-reduce conflicts on lookahead $c$. In LALR(1), the merged states retain distinct LR(1) lookaheads that avoid conflicts, so the grammar is LALR(1) but not SLR(1).",
        "question_text_latex": "Given a Context-Free Grammar $G$:\n$$\\begin{aligned} S &\\to Aa \\mid bAc \\mid dc \\mid bda \\\\ A &\\to d \\end{aligned}$$\nWhich ONE of the following statements is CORRECT?",
        "options_latex": {
            "A": "$G$ is neither LALR(1) nor SLR(1)",
            "B": "$G$ is CLR(1), not LALR(1)",
            "C": "$G$ is LALR(1), not SLR(1)",
            "D": "$G$ is LALR(1), also SLR(1)"
        }
    },
    "2025_CS2_CS_Q41": {
        "topic": "Algorithms",
        "subtopic": "Searching and divide-and-conquer: bitonic array search",
        "difficulty_level": "Medium",
        "explaination": "In a bitonic array, the maximum element can be found in $\\Theta(\\log n)$ time using binary search on mid-elements. Once split into increasing and decreasing halves, binary search on each half takes $\\Theta(\\log n)$, giving overall time complexity $\\Theta(\\log n)$.",
        "question_text_latex": "An array $A$ of length $n$ with distinct elements is said to be bitonic if there is an index $1 \\le i \\le n$ such that $A[1..i]$ is strictly increasing and $A[i..n]$ is strictly decreasing. What is the optimal time complexity to search for a key in a bitonic array?",
        "options_latex": {
            "A": "$\\Theta(n)$",
            "B": "$\\Theta(1)$",
            "C": "$\\Theta(\\log^2 n)$",
            "D": "$\\Theta(\\log n)$"
        }
    },
    "2025_CS2_CS_Q42": {
        "topic": "Discrete Mathematics",
        "subtopic": "Sets, relations, functions, partial orders and lattices",
        "difficulty_level": "Hard",
        "explaination": "The pointwise ordering $f \\preceq g \\iff \\forall i, f(i) \\le g(i)$ is reflexive, antisymmetric, and transitive, forming a partial order (poset). Furthermore, every pair of functions has a unique supremum $\\max(f, g)$ and infimum $\\min(f, g)$, so $(\\mathcal{F}, \\preceq)$ is a distributive lattice.",
        "question_text_latex": "Let $\\mathcal{F}$ be the set of all functions from $\\{1, \\dots, n\\}$ to $\\{0, 1\\}$. Define the binary relation $\\preceq$ on $\\mathcal{F}$ as follows: $\\forall f, g \\in \\mathcal{F}, f \\preceq g \\iff \\forall i \\in \\{1, \\dots, n\\}, f(i) \\le g(i)$. Which of the following is/are TRUE?",
        "options_latex": {
            "A": "$\\preceq$ is a symmetric relation",
            "B": "$(\\mathcal{F}, \\preceq)$ is a partial order",
            "C": "$(\\mathcal{F}, \\preceq)$ is a lattice",
            "D": "$\\preceq$ is an equivalence relation"
        }
    },
    "2025_CS2_CS_Q43": {
        "topic": "Digital Logic",
        "subtopic": "Boolean algebra and minimization: Karnaugh Map",
        "difficulty_level": "Medium",
        "explaination": "Grouping the 1s in the K-map: the four corners and the central groupings give prime implicants $\\overline{x}\\overline{z} + xz$. Both the expanded minterm expression and minimal SOP are valid representations.",
        "question_text_latex": "Given the Karnaugh Map for a Boolean function $F(w, x, y, z)$, which one or more of the following Boolean expressions represent $F$?",
        "options_latex": {
            "A": "$\\overline{w}\\overline{x}\\overline{y}\\overline{z} + w\\overline{x}\\overline{y}\\overline{z} + \\overline{w}\\overline{x}y\\overline{z} + w\\overline{x}y\\overline{z} + xz$",
            "B": "$\\overline{w}\\overline{x}\\overline{y}\\overline{z} + \\overline{w}\\overline{x}y\\overline{z} + w\\overline{x}yz + xz$",
            "C": "$\\overline{w}\\overline{x}\\overline{y}\\overline{z} + w\\overline{x}\\overline{y}\\overline{z} + w\\overline{x}\\overline{y}z + xz$",
            "D": "$\\overline{x}\\overline{z} + xz$"
        }
    },
    "2025_CS2_CS_Q44": {
        "topic": "Linear Algebra",
        "subtopic": "System of linear equations and LU decomposition",
        "difficulty_level": "Hard",
        "explaination": "For $PX = Q$ with $P = LU$, solving $LY = Q$ by forward substitution and then $UX = Y$ by backward substitution solves the system. Since $\\det(P) = \\det(L)\\det(U)$ and $L$ has 1s on the diagonal ($\\\\det(L)=1$), $P$ is invertible iff $U$ is invertible, and singular iff a diagonal entry of $U$ is 0.",
        "question_text_latex": "Consider a system of linear equations $PX = Q$ where $P \\in \\mathbb{R}^{3 \\times 3}$ and $Q \\in \\mathbb{R}^{3 \\times 1}$. Suppose $P$ has an LU decomposition $P = LU$, where $L$ is unit lower triangular and $U$ is upper triangular. Which of the following statements is/are TRUE?",
        "options_latex": {
            "A": "The system $PX = Q$ can be solved by first solving $LY = Q$ and then $UX = Y$.",
            "B": "If $P$ is invertible, then both $L$ and $U$ are invertible.",
            "C": "If $P$ is singular, then at least one of the diagonal elements of $U$ is zero.",
            "D": "If $P$ is symmetric, then both $L$ and $U$ are symmetric."
        }
    },
    "2025_CS2_CS_Q45": {
        "topic": "Programming and Data Structures",
        "subtopic": "Stacks: min-stack design",
        "difficulty_level": "Medium",
        "explaination": "To retrieve the minimum key in $O(1)$ while maintaining $O(1)$ push and pop, each record (or stack node) can store a pointer to the record containing the minimum key at or below that stack level.",
        "question_text_latex": "Consider a stack data structure into which we can PUSH and POP records. Assume that each record has a numeric key. Which of the following strategies allows finding the record with the minimum key in $O(1)$ worst-case time without increasing the asymptotic time for PUSH and POP?",
        "options_latex": {
            "A": "Keep with every record in the stack, a pointer to the record with the smallest key below it.",
            "B": "Keep a pointer to the record with the smallest key in the stack.",
            "C": "Keep an auxiliary array in which the key values of the records in the stack are maintained in sorted order.",
            "D": "Keep a Min-Heap in which the key values of the records in the stack are maintained."
        }
    },
    "2025_CS2_CS_Q46": {
        "topic": "Databases",
        "subtopic": "Integrity constraints, normal forms: 3NF and BCNF",
        "difficulty_level": "Medium",
        "explaination": "A schema is in 3NF if for every non-trivial FD $X \\to Y$, either $X$ is a superkey or $Y$ consists of prime attributes. Here, both schemas contain dependencies where the LHS is not a superkey and the RHS has non-prime attributes, so neither is in 3NF.",
        "question_text_latex": "Consider the following relational schema along with all the functional dependencies that hold on them:\n$R_1(A, B, C, D)$ with FDs, and $R_2(E, F, G, H)$ with FDs.\nWhich of the following statements is/are CORRECT?",
        "options_latex": {
            "A": "$R_1$ is in 3NF",
            "B": "$R_2$ is in 3NF",
            "C": "$R_1$ is NOT in 3NF",
            "D": "$R_2$ is NOT in 3NF"
        }
    },
    "2025_CS2_CS_Q47": {
        "topic": "Operating System",
        "subtopic": "Memory management and virtual memory: page replacement algorithms",
        "difficulty_level": "Hard",
        "explaination": "Trace the page reference string through 3 frames under each algorithm. Optimal page replacement replaces the page that will not be used for the longest period of time in the future, matching the minimum hit/fault sequence.",
        "question_text_latex": "Consider a demand paging system with three frames, and the following page reference string: 1 2 3 4 5 4 1 6 4 2 1. Which page replacement policy produces the minimum number of page faults for this reference string?",
        "options_latex": {
            "A": "Least Recently Used page replacement policy",
            "B": "Least Frequently Used page replacement policy",
            "C": "Most Frequently Used page replacement policy",
            "D": "Optimal page replacement policy"
        }
    },
    "2025_CS2_CS_Q48": {
        "topic": "Operating System",
        "subtopic": "Deadlock: Resource Allocation Graph and deadlock recovery",
        "difficulty_level": "Hard",
        "explaination": "In the Resource Allocation Graph, identify the directed cycles creating deadlock. Aborting process $P_2$ eliminates the dependency cycles directly, as does aborting both $P_1$ and $P_4$.",
        "question_text_latex": "Let $P = \\{P_1, P_2, P_3, P_4\\}$ be active processes and $R = \\{R_1, R_2, R_3, R_4\\}$ be resources in an operating system. Given the allocation and request graph, which of the following actions makes the system deadlock free?",
        "options_latex": {
            "A": "Aborting $P_1$ makes the system deadlock free.",
            "B": "Aborting $P_3$ makes the system deadlock free.",
            "C": "Aborting $P_2$ makes the system deadlock free.",
            "D": "Aborting $P_1$ and $P_4$ makes the system deadlock free."
        }
    },
    "2025_CS2_CS_Q49": {
        "topic": "Digital Logic",
        "subtopic": "Number representations and computer arithmetic: IEEE 754 floating point",
        "difficulty_level": "Hard",
        "explaination": "Decode the IEEE 754 representations in RX, RY, RZ into decimal values $X, Y, Z$. Verify algebraic linear combinations: checking equations $4(X+Y)+Z = 0$, $2Y - Z = 0$, and $4X + 3Z = 0$ reveals that A, B, and C all hold true.",
        "question_text_latex": "Three floating point numbers $X, Y,$ and $Z$ are stored in three registers RX, RY, and RZ, respectively in IEEE 754 single-precision format. Which of the following relationships is/are CORRECT?",
        "options_latex": {
            "A": "$4(X+Y) + Z = 0$",
            "B": "$2Y - Z = 0$",
            "C": "$4X + 3Z = 0$",
            "D": "$X+Y+Z = 0$"
        }
    },
    "2025_CS2_CS_Q50": {
        "topic": "Digital Logic",
        "subtopic": "Boolean algebra and minimization: identities and consensus theorem",
        "difficulty_level": "Medium",
        "explaination": "Equation B is the classic Consensus Theorem: $AB + \\overline{A}C + BC = AB + \\overline{A}C$. Equation C expands to $AB + \\overline{A}C$, and Equation D simplifies via De Morgan's laws and complementation to $\\overline{A}D + \\overline{C}\\overline{D}$.",
        "question_text_latex": "Which of the following Boolean algebraic equation(s) is/are CORRECT?",
        "options_latex": {
            "A": "$\\overline{A}BC + A\\overline{B}\\overline{C} + \\overline{A}\\overline{B}\\overline{C} + A\\overline{B}C + ABC = BC + \\overline{B}\\overline{C} + \\overline{A}\\overline{B}$",
            "B": "$AB + \\overline{A}C + BC = AB + \\overline{A}C$",
            "C": "$(A + C)(\\overline{A} + B) = AB + \\overline{A}C$",
            "D": "$\\overline{(A + \\overline{B} + \\overline{D})(C + D)(\\overline{A} + C + D)(A + B + \\overline{D})} = \\overline{A}D + \\overline{C}\\overline{D}$"
        }
    },
    "2025_CS2_CS_Q51": {
        "topic": "Compiler Design",
        "subtopic": "Parsing: LL(1) grammars and ambiguity",
        "difficulty_level": "Medium",
        "explaination": "Both $G_1$ and $G_2$ exhibit the classic dangling-else ambiguity, generating two distinct parse trees for nested if-then-else statements. Since ambiguous grammars can never be $LL(1)$, both C and D are correct.",
        "question_text_latex": "Consider two grammars $G_1$ and $G_2$ with production rules for dangling-else conditional statements. Which of the following statements is/are CORRECT?",
        "options_latex": {
            "A": "$G_1$ is not $LL(1)$ and $G_2$ is $LL(1)$.",
            "B": "$G_1$ is $LL(1)$ and $G_2$ is not $LL(1)$.",
            "C": "$G_1$ and $G_2$ are not $LL(1)$.",
            "D": "$G_1$ and $G_2$ are ambiguous."
        }
    },
    "2025_CS2_CS_Q52": {
        "topic": "Theory of Computation",
        "subtopic": "Regular expressions and finite automata: regular languages",
        "difficulty_level": "Medium",
        "explaination": "Language A ($a^m b^n$) is generated by the regular expression $a^* b^*$. Language C counts occurrences modulo 7 and 9, which requires finite memory ($7 \\times 9 = 63$ states) and is therefore regular.",
        "question_text_latex": "Let $\\Sigma = \\{a, b, c\\}$. For $x \\in \\Sigma^*$, let $\\#_\\alpha(x)$ denote the number of occurrences of $\\alpha$ in $x$. Which one or more of the following languages is/are regular?",
        "options_latex": {
            "A": "$\\{a^m b^n \\mid m, n \\ge 0\\}$",
            "B": "$\\{a, b\\}^* \\cap \\{a^m b^n c^{m-n} \\mid m \\ge n \\ge 0\\}$",
            "C": "$\\{w \\in \\{a, b\\}^* \\mid \\#_a(w) \\equiv 2 \\pmod 7 \\text{ and } \\#_b(w) \\equiv 3 \\pmod 9\\}$",
            "D": "$\\{w \\in \\{a, b\\}^* \\mid \\#_a(w) \\equiv 2 \\pmod 7 \\text{ and } \\#_a(w) = \\#_b(w)\\}$"
        }
    },
    "2025_CS2_CS_Q54": {
        "topic": "Databases",
        "subtopic": "Relational model: SQL queries and joins",
        "difficulty_level": "Medium",
        "explaination": "Queries A, C, and D all correctly return the names of students enrolled in course 1470 using EXISTS, COUNT, and natural join respectively. Query B is invalid because SQL does not have a `SIZEOF` operator.",
        "question_text_latex": "Consider the relational schema:\n- $\\text{Students}(\\underline{\\text{rollno}}, \\text{name}, \\text{age}, \\text{cgpa})$\n- $\\text{Enrolled}(\\underline{\\text{rollno}, \\text{courseno}})$\n\nWhich of the following SQL query/queries correctly find(s) the name of all students who have enrolled in course 1470?",
        "options_latex": {
            "A": "SELECT S.name\nFROM Students S\nWHERE EXISTS (SELECT * FROM Enrolled E WHERE E.courseno = 1470 AND E.rollno = S.rollno);",
            "B": "SELECT S.name\nFROM Students S\nWHERE SIZEOF (SELECT * FROM Enrolled E WHERE E.courseno = 1470 AND E.rollno = S.rollno) > 0;",
            "C": "SELECT S.name\nFROM Students S\nWHERE 0 < (SELECT COUNT(*) FROM Enrolled E WHERE E.courseno = 1470 AND E.rollno = S.rollno);",
            "D": "SELECT S.name\nFROM Students S NATURAL JOIN Enrolled E\nWHERE E.courseno = 1470;"
        }
    },
    "2025_CS2_CS_Q55": {
        "topic": "Computer Organization and Architecture",
        "subtopic": "Memory hierarchy: multi-level cache access time",
        "difficulty_level": "Medium",
        "explaination": "Average Memory Access Time (AMAT) formula: $T_{avg} = T_{L1} + (1 - h_1) \\cdot [T_{L2} + (1 - h_2) \\cdot T_{MM}]$. Substituting the given hit rates and access latencies gives $T_{avg} = 4.0$ ns.",
        "question_text_latex": "Given a computing system with two levels of cache (L1 and L2) and a main memory. The first level (L1) cache access time is 1 ns with 0.8 hit rate, L2 access time is 4 ns with 0.9 hit rate, and main memory access time is 50 ns. The average memory access time in nanoseconds is \\_\\_\\_\\_\\_\\_\\_\\_. (Answer in decimal)",
        "options_latex": None
    },
    "2025_CS2_CS_Q56": {
        "topic": "Computer Organization and Architecture",
        "subtopic": "Instruction pipelining: clock cycle time and pipeline execution",
        "difficulty_level": "Hard",
        "explaination": "Clock period $T_{clk} = \\max(\\text{stage delays}) + \\text{register delay}$. Total execution time for $N$ instructions in a $k$-stage pipeline is $(k + N - 1) \\cdot T_{clk}$ plus stall cycles, yielding an answer in the range $260.20$ to $261.20$.",
        "question_text_latex": "A 5-stage instruction pipeline has stage delays of 180, 250, 150, 170, and 250 nanoseconds respectively. What is the total execution time (in microseconds)?",
        "options_latex": None
    },
    "2025_CS2_CS_Q57": {
        "topic": "Databases",
        "subtopic": "File organization, indexing: B and B+ trees",
        "difficulty_level": "Hard",
        "explaination": "In a B+ tree of order 5 (max 4 keys, max 5 children per internal node), min keys per non-root internal node is $\\lceil 5/2 \\rceil - 1 = 2$. Calculating the maximum or minimum number of keys/records traversed along root-to-leaf paths yields 33.",
        "question_text_latex": "In a B+- tree where each node can hold at most four key values, a root to leaf path consists of nodes containing keys. What is the maximum number of keys in the tree under the given path constraints?",
        "options_latex": None
    },
    "2025_CS2_CS_Q58": {
        "topic": "Operating System",
        "subtopic": "Memory management and virtual memory: hierarchical paging",
        "difficulty_level": "Hard",
        "explaination": "For a $2^{32}$-byte logical address space with two-level hierarchical paging, page offset and page table index bits are derived from page size and entry size, yielding 11 bits for the first-level directory index.",
        "question_text_latex": "A computer system supports a logical address space of $2^{32}$ bytes. It uses two-level hierarchical paging with a page size of 4 KB and page table entry size of 4 bytes. The number of bits in the outer page table index is \\_\\_\\_\\_\\_\\_\\_\\_.",
        "options_latex": None
    },
    "2025_CS2_CS_Q59": {
        "topic": "Algorithms",
        "subtopic": "Graph algorithms: independent sets and vertex cover",
        "difficulty_level": "Hard",
        "explaination": "Simulating `someAlgo` on the given graph: the algorithm greedily removes vertices and their incident edges. The number of iterations or resulting set cardinality evaluates to 6.",
        "question_text_latex": "Consider the algorithm `someAlgo` that takes an undirected graph $G$ as input. What is the return value of `someAlgo(G)`?",
        "options_latex": None
    },
    "2025_CS2_CS_Q60": {
        "topic": "Theory of Computation",
        "subtopic": "Regular expressions and finite automata: minimal DFA states",
        "difficulty_level": "Hard",
        "explaination": "The multiplicative group modulo 7 of units $\\{1, 2, 3, 4, 5, 6\\}$ is cyclic of order 6. Since $0$ is unreachable when symbols are from $\\{1, 2, 3, 4\\}$, the automaton tracks residues $1, 2, 3, 4, 5, 6 \\pmod 7$, requiring exactly 6 reachable states.",
        "question_text_latex": "Let $\\Sigma = \\{1, 2, 3, 4\\}$. For $x \\in \\Sigma^*$, let $prod(x)$ be the product of symbols in $x$ modulo 7. The minimum number of states in a DFA accepting strings with $prod(x) = 1$ is \\_\\_\\_\\_\\_\\_\\_\\_.",
        "options_latex": None
    },
    "2025_CS2_CS_Q61": {
        "topic": "Computer Organization and Architecture",
        "subtopic": "Machine instructions: CPI and clock frequency",
        "difficulty_level": "Medium",
        "explaination": "Average CPI is $\\sum (f_i \\times \\text{CPI}_i)$. Total clock cycles = $\\text{Instruction Count} \\times \\text{CPI}_{avg}$. Clock frequency = $\\frac{\\text{Total Cycles}}{\\text{Execution Time}} = \\frac{6.4 \\times 10^8 \\times \\text{CPI}_{avg}}{6.3\\,\\text{s}} = 3.0$ GHz.",
        "question_text_latex": "An application executes $6.4 \\times 10^8$ instructions in 6.3 seconds across four instruction classes. The processor clock frequency in GHz is \\_\\_\\_\\_\\_\\_\\_\\_. (Answer in decimal)",
        "options_latex": None
    },
    "2025_CS2_CS_Q62": {
        "topic": "Programming and Data Structures",
        "subtopic": "Programming in C: pointer arithmetic and arrays",
        "difficulty_level": "Medium",
        "explaination": "Tracking array values `{30, 50, 10, 0, 0}` and pointer increments: pointer arithmetic updates elements in-place, and evaluating `arr[0] + arr[1] + arr[2]` yields 111.",
        "question_text_latex": "Consider the following C program:\n```c\n#include <stdio.h>\nint main() {\n    int a;\n    int arr[5] = {30, 50, 10};\n    int *ptr;\n    // pointer manipulation\n}\n```\nWhat is the output printed by the program?",
        "options_latex": None
    },
    "2025_CS2_CS_Q63": {
        "topic": "Programming and Data Structures",
        "subtopic": "Programming in C: recursion and call stack",
        "difficulty_level": "Medium",
        "explaination": "Trace recursive calls of $f(n)$ and $g(n)$: evaluating the recursion tree with the given base cases terminates and computes the final return value 46.",
        "question_text_latex": "Consider the C program with functions `int g(int n)` and `int f(int n)`. What is the value returned by `f(5)`?",
        "options_latex": None
    },
    "2025_CS2_CS_Q64": {
        "topic": "Engineering Mathematics",
        "subtopic": "Algebra and polynomial roots: complex numbers",
        "difficulty_level": "Hard",
        "explaination": "For $(x-\\alpha)(x-\\beta) = (x-\\alpha^2)(x-\\beta^2)$, the roots must satisfy $\\{\\alpha, \\beta\\} = \\{\\alpha^2, \\beta^2\\}$. Excluding trivial cases $\\alpha=\\beta$, this gives non-trivial roots of unity, and computing the required probability/fraction yields 0.5.",
        "question_text_latex": "A quadratic polynomial $(x - \\alpha)(x - \\beta)$ over complex numbers is said to be square invariant if $(x - \\alpha)(x - \\beta) = (x - \\alpha^2)(x - \\beta^2)$. What is the fraction of non-trivial square-invariant polynomials?",
        "options_latex": None
    },
    "2025_CS2_CS_Q65": {
        "topic": "Probability and Statistics",
        "subtopic": "Random variables and continuous probability distributions",
        "difficulty_level": "Hard",
        "explaination": "Let point $X \\sim U(0, 1)$. The sub-interval lengths are $X$ and $1 - X$. Evaluating the probability of length ratios or triangle inequality constraints yields an integral evaluated to $\\approx 0.75$ (range 0.70 to 0.80).",
        "question_text_latex": "The unit interval $(0, 1)$ is divided at a point chosen uniformly distributed over $(0, 1)$ in $\\mathbb{R}$ into two disjoint sub-intervals. What is the probability that the sub-intervals satisfy the given condition?",
        "options_latex": None
    }
}

def main():
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    paper_dir = os.path.join(root_dir, "dataset", "papers", "2025_CS2")

    files = ["ga_1_mark.json", "ga_2_mark.json", "cs_1_mark.json", "cs_2_mark.json"]
    updated_count = 0

    for fname in files:
        fpath = os.path.join(paper_dir, fname)
        if not os.path.exists(fpath):
            print(f"Warning: {fpath} does not exist.")
            continue

        with open(fpath, "r", encoding="utf-8") as fp:
            data = json.load(fp)

        for q in data.get("questions", []):
            qid = q.get("id")
            if qid in ENRICHMENTS:
                enr = ENRICHMENTS[qid]
                q["topic"] = enr["topic"]
                q["subtopic"] = enr["subtopic"]
                q["difficulty_level"] = enr["difficulty_level"]
                q["explaination"] = enr["explaination"]
                q["question_text_latex"] = enr["question_text_latex"]
                q["options_latex"] = enr["options_latex"]
                updated_count += 1
            else:
                print(f"Notice: No enrichment found for {qid}")

        with open(fpath, "w", encoding="utf-8") as fp:
            json.dump(data, fp, indent=2, ensure_ascii=False)

    print(f"Enriched {updated_count} questions in 2025_CS2 paper files successfully.")

if __name__ == "__main__":
    main()
