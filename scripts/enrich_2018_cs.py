#!/usr/bin/env python3
"""
enrich_2018_cs.py

Fills the AI metadata fields for 2018 CS questions based on syllabus/cs_2026_syllabus.json:
- topic: Canonical syllabus module
- subtopic: Granular syllabus concept
- difficulty_level: Easy | Medium | Hard
- explaination: Concise 2-3 sentence hint with embedded LaTeX formulas ($...$)
- question_text_latex: Formatted question text with proper LaTeX math ($...$)
- options_latex: Formatted options with LaTeX math ($...$) and cleaned PDF footers
"""

import os
import json

ENRICHMENTS = {
    # ==================== GA 1-MARK ====================
    "2018_CS_GA_Q01": {
        "topic": "Verbal Aptitude",
        "subtopic": "Vocabulary: words, idioms, and phrases in context",
        "difficulty_level": "Easy",
        "explaination": "\"They're\" is the contraction for \"they are\", \"their\" is the possessive pronoun, and \"there\" refers to a place. Thus, the complete sentence is: \"They're bringing their books from there.\"",
        "question_text_latex": "``From where are they bringing their books? \\_\\_\\_\\_\\_\\_\\_\\_ bringing \\_\\_\\_\\_\\_\\_\\_ books from \\_\\_\\_\\_\\_.''\n\nThe words that best fill the blanks in the above sentence are",
        "options_latex": {
            "A": "Their, they're, there",
            "B": "They're, their, there",
            "C": "There, their, they're",
            "D": "They're, there, there"
        }
    },
    "2018_CS_GA_Q02": {
        "topic": "Verbal Aptitude",
        "subtopic": "Vocabulary: words, idioms, and phrases in context",
        "difficulty_level": "Easy",
        "explaination": "The sentence contrasts an erratic or wandering investigation with an \"organized\" one. \"Meandering\" means proceeding in a winding or circuitous course without a clear direction, which fits the context precisely.",
        "question_text_latex": "``A \\_\\_\\_\\_\\_\\_\\_\\_\\_ investigation can sometimes yield new facts, but typically organized ones are more successful.''\n\nThe word that best fills the blank in the above sentence is",
        "options_latex": {
            "A": "meandering",
            "B": "timely",
            "C": "consistent",
            "D": "systematic"
        }
    },
    "2018_CS_GA_Q03": {
        "topic": "Quantitative Aptitude",
        "subtopic": "Mensuration and geometry",
        "difficulty_level": "Easy",
        "explaination": "For a square of area $d$, the side length is $s = \\sqrt{d}$ and its diagonal is $s\\sqrt{2} = \\sqrt{2d}$. Since this diagonal is the diameter of the circle, the radius is $r = \\frac{\\sqrt{2d}}{2} = \\sqrt{\\frac{d}{2}}$. Hence, the area of the circle is $\\pi r^2 = \\pi \\left(\\frac{d}{2}\\right) = \\frac{1}{2}\\pi d$.",
        "question_text_latex": "The area of a square is $d$. What is the area of the circle which has the diagonal of the square as its diameter?",
        "options_latex": {
            "A": "$\\pi d$",
            "B": "$\\pi d^2$",
            "C": "$\\frac{1}{4}\\pi d^2$",
            "D": "$\\frac{1}{2}\\pi d$"
        }
    },
    "2018_CS_GA_Q04": {
        "topic": "Quantitative Aptitude",
        "subtopic": "Numerical computation and estimation: ratios, percentages, powers, exponents and logarithms, permutations and combinations, series",
        "difficulty_level": "Easy",
        "explaination": "The required number is $\\text{LCM}(20, 42, 76) + 7$. Calculating prime factorizations: $20 = 2^2 \\times 5$, $42 = 2 \\times 3 \\times 7$, $76 = 2^2 \\times 19$. Thus $\\text{LCM} = 2^2 \\times 3 \\times 5 \\times 7 \\times 19 = 7980$. Adding the remainder 7 gives $7980 + 7 = 7987$.",
        "question_text_latex": "What would be the smallest natural number which when divided either by 20 or by 42 or by 76 leaves a remainder of 7 in each case?",
        "options_latex": {
            "A": "3047",
            "B": "6047",
            "C": "7987",
            "D": "63847"
        }
    },
    "2018_CS_GA_Q05": {
        "topic": "Quantitative Aptitude",
        "subtopic": "Numerical computation and estimation: ratios, percentages, powers, exponents and logarithms, permutations and combinations, series",
        "difficulty_level": "Easy",
        "explaination": "Examining consecutive multipliers: $2 \\times 6 = 12$, $12 \\times 5 = 60$, $60 \\times 4 = 240$, $240 \\times 3 = 720$, $720 \\times 2 = 1440$. Following this decreasing multiplier pattern, the next term is $1440 \\times 1 = 1440$, and the term after is $1440 \\times 0 = 0$.",
        "question_text_latex": "What is the missing number in the following sequence?\n\\[ 2,\\; 12,\\; 60,\\; 240,\\; 720,\\; 1440,\\; \\_\\_\\_\\_\\_,\\; 0 \\]",
        "options_latex": {
            "A": "2880",
            "B": "1440",
            "C": "720",
            "D": "0"
        }
    },
    "2018_CS_GA_Q01_v2": {
        "topic": "Discrete Mathematics",
        "subtopic": "Combinatorics: counting, recurrence relations, generating functions",
        "difficulty_level": "Easy",
        "explaination": "The generating function is $G(x) = \\sum_{n=0}^\\infty (2n + 3)x^n = 2\\sum_{n=0}^\\infty n x^n + 3\\sum_{n=0}^\\infty x^n$. Using the standard power series $\\sum_{n=0}^\\infty x^n = \\frac{1}{1-x}$ and $\\sum_{n=0}^\\infty n x^n = \\frac{x}{(1-x)^2}$, we obtain $G(x) = \\frac{2x}{(1-x)^2} + \\frac{3(1-x)}{(1-x)^2} = \\frac{3 - x}{(1-x)^2}$.",
        "question_text_latex": "Which one of the following is a closed form expression for the generating function of the sequence $\\{a_n\\}$, where $a_n = 2n + 3$ for all $n = 0, 1, 2, \\dots$?",
        "options_latex": {
            "A": "$\\frac{3}{(1-x)^2}$",
            "B": "$\\frac{3x}{(1-x)^2}$",
            "C": "$\\frac{2-x}{(1-x)^2}$",
            "D": "$\\frac{3-x}{(1-x)^2}$"
        }
    },
    "2018_CS_GA_Q02_v2": {
        "topic": "Programming and Data Structures",
        "subtopic": "Programming in C",
        "difficulty_level": "Easy",
        "explaination": "In `struct Ournode`, `char x, y, z;` are stored contiguously in memory. Since `p = {'1', '0', 'a'+2}`, `p.x = '1'`, `p.y = '0'`, and `p.z = 'c'`. Pointer `q` points to `p`; casting `q` to `(char*)` gives byte-level access where `*((char*)q + 1)` accesses `p.y` ('0') and `*((char*)q + 2)` accesses `p.z` ('c').",
        "question_text_latex": "Consider the following C program.\n\\begin{lstlisting}[language=C]\n#include <stdio.h>\nstruct Ournode {\n    char x, y, z;\n};\n\nint main() {\n    struct Ournode p = {'1', '0', 'a' + 2};\n    struct Ournode *q = &p;\n    printf(\"%c, %c\", *((char*)q + 1), *((char*)q + 2));\n    return 0;\n}\n\\end{lstlisting}\nThe output of this program is",
        "options_latex": {
            "A": "0, c",
            "B": "0, a+2",
            "C": "'0', 'p+2'",
            "D": "1, 0"
        }
    },
    "2018_CS_GA_Q04_v2": {
        "topic": "Digital Logic",
        "subtopic": "Boolean algebra",
        "difficulty_level": "Easy",
        "explaination": "Recall that $P \\oplus \\overline{P} = 1$ and $1 \\oplus Q = \\overline{Q}$. On the right-hand side of (D), $P \\odot \\overline{P} = 0$, and $0 \\odot \\overline{Q} = \\overline{0 \\oplus \\overline{Q}} = \\overline{\\overline{Q}} = Q$. Since $\\overline{Q} \\neq Q$, option (D) is NOT correct.",
        "question_text_latex": "Let $\\oplus$ and $\\odot$ denote the Exclusive OR and Exclusive NOR operations, respectively. Which one of the following is NOT CORRECT?",
        "options_latex": {
            "A": "$\\overline{P \\oplus Q} = P \\odot Q$",
            "B": "$\\overline{P \\odot Q} = P \\oplus Q$",
            "C": "$\\overline{P} \\oplus Q = P \\odot Q$",
            "D": "$(P \\oplus \\overline{P}) \\oplus Q = (P \\odot \\overline{P}) \\odot \\overline{Q}$"
        }
    },
    "2018_CS_GA_Q05_v2": {
        "topic": "Computer Organization and Architecture",
        "subtopic": "Machine instructions and addressing modes",
        "difficulty_level": "Easy",
        "explaination": "RISC (Reduced Instruction Set Computer) architectures feature load-store designs where arithmetic operations operate only on registers (I), fixed-length instruction encodings for streamlined pipelining (II), and hardwired control units for single-cycle instruction execution (III). Hence, all three characteristics I, II, and III are typical of RISC processors.",
        "question_text_latex": "Consider the following processor design characteristics.\n\\begin{enumerate}[label=\\Roman*.]\n    \\item Register-to-register arithmetic operations only\n    \\item Fixed-length instruction format\n    \\item Hardwired control unit\n\\end{enumerate}\nWhich of the characteristics above are used in the design of a RISC processor?",
        "options_latex": {
            "A": "I and II only",
            "B": "II and III only",
            "C": "I and III only",
            "D": "I, II and III"
        }
    },
    "2018_CS_GA_Q06_v2": {
        "topic": "Theory of Computation",
        "subtopic": "Regular expressions and finite automata",
        "difficulty_level": "Easy",
        "explaination": "By the subset construction algorithm, converting an $n$-state NFA to a DFA produces states that are subsets of the NFA states. Thus, the power set has $2^n$ possible states, ensuring that any equivalent minimal DFA has $k \\le 2^n$ states.",
        "question_text_latex": "Let $N$ be an NFA with $n$ states. Let $k$ be the number of states of a minimal DFA which is equivalent to $N$. Which one of the following is necessarily true?",
        "options_latex": {
            "A": "$k \\ge 2^n$",
            "B": "$k \\ge n$",
            "C": "$k \\le n^2$",
            "D": "$k \\le 2^n$"
        }
    },
    "2018_CS_GA_Q07_v2": {
        "topic": "Theory of Computation",
        "subtopic": "Regular and context-free languages, pumping lemma",
        "difficulty_level": "Easy",
        "explaination": "The set of recursively enumerable (RE) languages is closed under union, intersection, concatenation, and Kleene star, but not closed under complementation or set difference.",
        "question_text_latex": "The set of all recursively enumerable languages is",
        "options_latex": {
            "A": "closed under complementation.",
            "B": "closed under intersection.",
            "C": "a subset of the set of all context-sensitive languages.",
            "D": "an uncountable set."
        }
    },
    "2018_CS_GA_Q08_v2": {
        "topic": "Compiler Design",
        "subtopic": "Lexical analysis, parsing, syntax-directed translation",
        "difficulty_level": "Easy",
        "explaination": "Type checking verifies semantic consistency according to language type rules and is performed during semantic analysis, which occurs after syntax analysis (parsing). Therefore, the statement that type checking is done during syntax analysis is FALSE.",
        "question_text_latex": "Which one of the following statements is FALSE?",
        "options_latex": {
            "A": "Context-free grammar can be used to specify both lexical and syntax rules.",
            "B": "Type checking is done before parsing.",
            "C": "High-level language programs can be converted to intermediate code directly.",
            "D": "Arguments to a function can be passed using the program stack."
        }
    },
    "2018_CS_GA_Q09": {
        "topic": "Computer Organization and Architecture",
        "subtopic": "I/O interface: interrupt and DMA mode",
        "difficulty_level": "Easy",
        "explaination": "Upon receiving an interrupt, the processor finishes the execution of the current instruction (Q), saves the processor status and return PC onto the stack (P), loads the starting address of the ISR from the interrupt vector table (T), executes the ISR (R), and finally restores the saved status and resumes process $L$ (S). Hence the order is QPTRS.",
        "question_text_latex": "The following are some events that occur after a device controller issues an interrupt while process $L$ is under execution.\n\\begin{itemize}[leftmargin=*, nosep]\n    \\item[P.] The processor pushes the process status of $L$ on to the control stack.\n    \\item[Q.] The processor finishes the execution of the current instruction.\n    \\item[R.] The processor executes the interrupt service routine.\n    \\item[S.] The processor pops the process status of $L$ from the control stack.\n    \\item[T.] The processor fetches the new PC value from the interrupt vector.\n\\end{itemize}\nWhich one of the following is the correct order of events?",
        "options_latex": {
            "A": "Q, P, T, R, S",
            "B": "P, Q, T, R, S",
            "C": "Q, P, R, T, S",
            "D": "P, Q, R, T, S"
        }
    },
    "2018_CS_GA_Q10_v2": {
        "topic": "Operating System",
        "subtopic": "Memory management and virtual memory",
        "difficulty_level": "Medium",
        "explaination": "The effective access time is $X = (1 - p)M + pD = M + p(D - M)$. Solving for $p$ yields $p(D - M) = X - M \\implies p = \\frac{X - M}{D - M}$.",
        "question_text_latex": "Consider a process executing on an operating system that uses demand paging. The average time for a memory access in the system is $M$ units if the corresponding memory page is available in memory, and $D$ units $(D \\gg M)$ if the page needs to be fetched from the disk. If $X$ is the effective memory access time, the page fault rate $p$ is",
        "options_latex": {
            "A": "$\\frac{X - M}{D}$",
            "B": "$\\frac{X - M}{D - M}$",
            "C": "$\\frac{D - X}{D - M}$",
            "D": "$\\frac{X - M}{D + M}$"
        }
    },
    "2018_CS_GA_Q11": {
        "topic": "Databases",
        "subtopic": "ER-model",
        "difficulty_level": "Easy",
        "explaination": "In an ER diagram, a many-to-one relationship from $E_1$ to $E_2$ means each entity in $E_1$ is related to at most one entity in $E_2$. Total participation of $E_1$ requires that every entity in $E_1$ participates in at least one relationship. Combining these, every entity in $E_1$ is associated with exactly one entity in $E_2$.",
        "question_text_latex": "In an Entity-Relationship (ER) model, suppose $R$ is a many-to-one relationship from entity set $E_1$ to entity set $E_2$. Assume that $E_1$ has total participation in $R$, but $E_2$ has partial participation in $R$. Which one of the following statements is necessarily TRUE?",
        "options_latex": {
            "A": "Every entity in $E_1$ is associated with exactly one entity in $E_2$.",
            "B": "Some entity in $E_1$ is associated with more than one entity in $E_2$.",
            "C": "Every entity in $E_2$ is associated with at least one entity in $E_1$.",
            "D": "Every entity in $E_2$ is associated with at most one entity in $E_1$."
        }
    },
    "2018_CS_GA_Q12": {
        "topic": "Databases",
        "subtopic": "Relational model: relational algebra, tuple calculus, SQL",
        "difficulty_level": "Easy",
        "explaination": "Query 1 uses natural join (inner join), Query 2 uses left outer join, Query 3 uses right outer join, and Query 4 uses full outer join. A full outer join preserves all tuples from both relation $Book$ and relation $Stock$ (filling missing values with NULLs). Therefore, every tuple output by Query 1, Query 2, and Query 3 is guaranteed to appear in Query 4.",
        "question_text_latex": "Consider the following two tables and four queries in SQL.\n\\texttt{Book (isbn, bname)}\n\\texttt{Stock (isbn, copies)}\n\nQuery 1: \\texttt{SELECT B.isbn, S.copies FROM Book B INNER JOIN Stock S ON B.isbn = S.isbn;}\nQuery 2: \\texttt{SELECT B.isbn, S.copies FROM Book B LEFT OUTER JOIN Stock S ON B.isbn = S.isbn;}\nQuery 3: \\texttt{SELECT B.isbn, S.copies FROM Book B RIGHT OUTER JOIN Stock S ON B.isbn = S.isbn;}\nQuery 4: \\texttt{SELECT B.isbn, S.copies FROM Book B FULL OUTER JOIN Stock S ON B.isbn = S.isbn;}\n\nWhich one of the following statements is CORRECT?",
        "options_latex": {
            "A": "Query 1 and Query 2 always produce the same number of rows.",
            "B": "Query 2 and Query 3 always produce the same number of rows.",
            "C": "Query 1 always produces the maximum number of rows among all queries.",
            "D": "All rows from Query 1, Query 2, and Query 3 are always present in the result of Query 4."
        }
    },
    "2018_CS_GA_Q13": {
        "topic": "Computer Networks",
        "subtopic": "Concept of layering: OSI and TCP/IP Protocol Stacks",
        "difficulty_level": "Easy",
        "explaination": "UDP port numbers are 16 bits long (P-IV). Ethernet MAC addresses are 48 bits long (Q-I). The IPv6 Next Header field is 8 bits long (R-II). TCP sequence numbers are 32 bits long (S-III). Hence the correct matching is P-IV, Q-I, R-II, S-III.",
        "question_text_latex": "Match the following:\n\\begin{center}\n\\begin{tabular}{ll@{\\hspace{2cm}}ll}\n\\textbf{Field} & & \\textbf{Length in bits} & \\\\\nP. & UDP Header's Port Number & I. & 48 \\\\\nQ. & Ethernet MAC Address & II. & 8 \\\\\nR. & IPv6 Next Header & III. & 32 \\\\\nS. & TCP Header's Sequence Number & IV. & 16\n\\end{tabular}\n\\end{center}",
        "options_latex": {
            "A": "P-III, Q-I, R-II, S-IV",
            "B": "P-IV, Q-II, R-I, S-III",
            "C": "P-IV, Q-I, R-II, S-III",
            "D": "P-I, Q-IV, R-II, S-III"
        }
    },
    "2018_CS_GA_Q14": {
        "topic": "Computer Networks",
        "subtopic": "Transport layer: flow control and congestion control, UDP, TCP, sockets",
        "difficulty_level": "Medium",
        "explaination": "In TCP slow start, the congestion window (`cwnd`) increases by 1 MSS for each acknowledged segment. Consequently, when all segments in a flight are acknowledged, `cwnd` approximately doubles every round-trip time (RTT). Thus, statement (iv) is TRUE.",
        "question_text_latex": "Consider the following statements regarding the slow start phase of the TCP congestion control algorithm. Note that $cwnd$ stands for the congestion window size and $MSS$ denotes the Maximum Segment Size.\n\\begin{itemize}[leftmargin=*, nosep]\n    \\item[(i)] The $cwnd$ increases by 2 $MSS$ on every successful acknowledgement.\n    \\item[(ii)] The $cwnd$ increases by 1 $MSS$ on every successful acknowledgement.\n    \\item[(iii)] The $cwnd$ increases by 1 $MSS$ every round trip time.\n    \\item[(iv)] The $cwnd$ approximately doubles every round trip time.\n\\end{itemize}\nWhich of the following statements is/are CORRECT?",
        "options_latex": {
            "A": "(i) and (iii) only",
            "B": "(i) and (iv) only",
            "C": "(ii) and (iv) only",
            "D": "(ii) and (iii) only"
        }
    },
    "2018_CS_GA_Q15": {
        "topic": "Probability and Statistics",
        "subtopic": "Random variables",
        "difficulty_level": "Medium",
        "explaination": "On rolling two fair dice independently, the probability of a tie is $P(\\text{tie}) = \\frac{6}{36} = \\frac{1}{6}$, and the probability of someone winning (no tie) is $1 - \\frac{1}{6} = \\frac{5}{6}$. The game ends on the third roll if trials 1 and 2 are ties and trial 3 produces a winner: $P(\\text{Trial 3}) = \\left(\\frac{1}{6}\\right) \\times \\left(\\frac{1}{6}\\right) \\times \\left(\\frac{5}{6}\\right) = \\frac{5}{216} \\approx 0.0231$.",
        "question_text_latex": "Two people, $P$ and $Q$, decide to independently roll two identical dice, each with 6 faces, numbered 1 to 6. The person with the higher number wins. In case both get the same number, they repeat the roll until someone wins. The probability that the game concludes on the third roll is \\_\\_\\_\\_\\_\\_\\. (Answer in 3 decimal places)",
        "options_latex": None
    },
    "2018_CS_GA_Q16": {
        "topic": "Calculus",
        "subtopic": "Integration",
        "difficulty_level": "Easy",
        "explaination": "Substitute $u = x^2$, so $du = 2x\\,dx$. The limits transform from $x = 0 \\implies u = 0$ to $x = \\frac{\\pi}{4} \\implies u = \\frac{\\pi^2}{16} \\approx \\frac{9.8596}{16} \\approx 0.61685$ radians. The integral is $\\frac{1}{2}\\int_0^{\\pi^2/16} \\cos u \\, du = \\frac{1}{2} \\sin\\left(\\frac{\\pi^2}{16}\\right) \\approx \\frac{1}{2} \\sin(0.61685) \\approx \\frac{1}{2}(0.5784) \\approx 0.289$.",
        "question_text_latex": "The value of $\\int_0^{\\pi/4} x \\cos(x^2) \\, dx$ correct to three decimal places (assuming that $\\pi = 3.14$) is \\_\\_\\_\\_\\_\\_\\_\\_.",
        "options_latex": None
    },
    "2018_CS_GA_Q17": {
        "topic": "Linear Algebra",
        "subtopic": "Eigenvalues and eigenvectors",
        "difficulty_level": "Easy",
        "explaination": "For an outer product matrix $A = u v^T$ where $u = \\begin{bmatrix} 1 \\\\ 2 \\end{bmatrix}$ and $v = \\begin{bmatrix} 1 \\\\ 1 \\end{bmatrix}$, the rank of $A$ is 1. Its non-zero eigenvalue equals the trace of $A$, which is given by the inner product $v^T u = 1(1) + 1(2) = 3$.",
        "question_text_latex": "Consider a matrix $A = u v^T$ where $u = \\begin{bmatrix} 1 \\\\ 2 \\end{bmatrix}$ and $v = \\begin{bmatrix} 1 \\\\ 1 \\end{bmatrix}$. Note that $v^T$ denotes the transpose of $v$. The largest eigenvalue of $A$ is \\_\\_\\_\\_\\_\\_\\_\\_.",
        "options_latex": None
    },
    "2018_CS_GA_Q18": {
        "topic": "Discrete Mathematics",
        "subtopic": "Graphs: connectivity, matching, colouring",
        "difficulty_level": "Easy",
        "explaination": "The given graph contains an odd cycle, which prevents it from being 2-colorable (bipartite), meaning $\\chi(G) \\ge 3$. A valid 3-coloring can be directly constructed without any conflicts between adjacent vertices, so $\\chi(G) = 3$.",
        "question_text_latex": "The chromatic number of the graph containing a 7-cycle with a single cross-chord is \\_\\_\\_\\_\\_\\_\\_\\_.",
        "options_latex": None
    },
    "2018_CS_GA_Q19": {
        "topic": "Discrete Mathematics",
        "subtopic": "Monoids, Groups",
        "difficulty_level": "Easy",
        "explaination": "By Lagrange's Theorem, the order of any subgroup $H$ of a finite group $G$ must divide $|G| = 84$. A proper subgroup cannot equal the whole group, so $|H| < 84$. The largest proper divisor of 84 is $\\frac{84}{2} = 42$.",
        "question_text_latex": "Let $G$ be a finite group on 84 elements. The size of a largest possible proper subgroup of $G$ is \\_\\_\\_\\_\\_\\_\\_\\_.",
        "options_latex": None
    },
    "2018_CS_GA_Q20": {
        "topic": "Programming and Data Structures",
        "subtopic": "Trees, binary search trees, binary heaps",
        "difficulty_level": "Medium",
        "explaination": "In postorder traversal, the root is the last element (1). Splitting inorder $[8,6,9,4,7,2,5]$ and $[3]$ around root 1 gives left subtree nodes and right subtree node 3. Recursively constructing the unique binary tree reveals the longest leaf path: $1 \\to 2 \\to 4 \\to 6 \\to 8$ (or 9), which has 4 edges. Thus, the height in terms of edges is 4.",
        "question_text_latex": "The postorder traversal of a binary tree is $8, 9, 6, 7, 4, 5, 2, 3, 1$. The inorder traversal of the same tree is $8, 6, 9, 4, 7, 2, 5, 1, 3$. The height of a tree is the length of the longest path from the root to any leaf (in terms of number of edges). The height of the binary tree is \\_\\_\\_\\_\\_\\_\\_\\_.",
        "options_latex": None
    },
    "2018_CS_GA_Q21": {
        "topic": "Programming and Data Structures",
        "subtopic": "Recursion",
        "difficulty_level": "Medium",
        "explaination": "Function `calc(a, b)` computes $\\log_3(b)$ recursively: `calc(4, 81)` calls `calc(4, 27)` $\\to$ `calc(4, 9)` $\\to$ `calc(4, 3)`. At $b = 3$, `b <= 3` is satisfied and it returns. The variable `counter` is incremented once per invocation, resulting in exactly 4 calls.",
        "question_text_latex": "Consider the following C program:\n\\begin{lstlisting}[language=C]\n#include <stdio.h>\nint counter = 0;\n\nint calc(int a, int b) {\n    int c;\n    counter++;\n    if (b <= 3) return (a + b);\n    else {\n        c = b / 3;\n        return (calc(a, c));\n    }\n}\n\nint main() {\n    calc(4, 81);\n    printf(\"%d\", counter);\n    return 0;\n}\n\\end{lstlisting}\nThe output of this program is \\_\\_\\_\\_\\_\\_\\_\\_.",
        "options_latex": None
    },
    "2018_CS_GA_Q23": {
        "topic": "Computer Organization and Architecture",
        "subtopic": "Memory hierarchy: cache, main memory and secondary storage",
        "difficulty_level": "Medium",
        "explaination": "The DRAM has $2^{14} = 16384$ rows. Refreshing all rows takes $16384 \\times 50\\text{ ns} = 819.2\\ \\mu\\text{s}$ every $2000\\ \\mu\\text{s}$. The refresh overhead fraction is $\\frac{819.2}{2000} = 40.96\\%$. Hence, the percentage of time available for reading and writing memory is $100\\% - 40.96\\% = 59.04\\% \\approx 59\\%$.",
        "question_text_latex": "A 32-bit wide main memory unit with a capacity of 1 GB is built using $256\\text{M} \\times 4\\text{-bit}$ DRAM chips. The number of rows of memory cells in the DRAM chip is $2^{14}$. The time taken to perform one refresh operation is 50 nanoseconds. The refresh period is 2 milliseconds. The percentage of time that the memory is available for performing the normal read and write operations is \\_\\_\\_\\_\\_\\_\\_\\_\\%. (Answer in integer)",
        "options_latex": None
    },
    "2018_CS_GA_Q24": {
        "topic": "Operating System",
        "subtopic": "Deadlock",
        "difficulty_level": "Easy",
        "explaination": "For $n$ processes sharing $m$ instances of a single resource type where each process needs at most $K$ instances, deadlock is guaranteed to be avoided if $\\sum_{i=1}^n (K - 1) < m \\implies n(K - 1) \\le m - 1$. Here $n = 3$ and $m = 4$, so $3(K - 1) \\le 3 \\implies K - 1 \\le 1 \\implies K \\le 2$.",
        "question_text_latex": "Consider a system with 3 processes that share 4 instances of the same resource type. Each process can request at most $K$ instances of the resource type at any time. The largest value of $K$ that will always avoid deadlock is \\_\\_\\_\\_\\_\\_\\_\\_.",
        "options_latex": None
    },
    "2018_CS_GA_Q25": {
        "topic": "Computer Networks",
        "subtopic": "Transport layer: flow control and congestion control, UDP, TCP, sockets",
        "difficulty_level": "Medium",
        "explaination": "A 32-bit sequence number space contains $2^{32} = 4{,}294{,}967{,}296$ bytes. At a transmission rate of $1\\text{ Gbps} = \\frac{10^9}{8} = 1.25 \\times 10^8\\text{ bytes/s}$, the wrap-around time is $\\frac{2^{32}}{1.25 \\times 10^8} = \\frac{4294967296}{125000000} \\approx 34.36$ seconds $\\approx 34$ seconds.",
        "question_text_latex": "Consider a 1 Gbps network with an MTU of 1500 bytes and a 32-bit sequence number space. The minimum time (in seconds, rounded to the nearest integer) after which the sequence numbers can wrap around is \\_\\_\\_\\_\\_\\_\\_\\_.",
        "options_latex": None
    },

    # ==================== GA 2-MARK ====================
    "2018_CS_GA_Q06": {
        "topic": "Quantitative Aptitude",
        "subtopic": "Numerical computation and estimation: ratios, percentages, powers, exponents and logarithms, permutations and combinations, series",
        "difficulty_level": "Medium",
        "explaination": "Let $M$ and $W$ be eligible men and women, with $M + W = 300$. Number claiming pension is $\\frac{8}{9}M$ men and $\\frac{2}{3}W$ women. Total pension claimed $= \\frac{8}{9}M(750) + \\frac{2}{3}W(1000) = \\frac{2000}{3}M + \\frac{2000}{3}W = \\frac{2000}{3}(M + W) = \\frac{2000}{3}(300) = 2{,}00{,}000$.",
        "question_text_latex": "An old man walks in a town to distribute old age pensions. There are 300 persons in the town who are eligible for the pension. The monthly pension is Rs. 750 for each eligible man and Rs. 1000 for each eligible woman. 8/9 of the eligible men and 2/3 of the eligible women claim the pension. The total pension claimed per month is",
        "options_latex": {
            "A": "Rs. 1,50,000",
            "B": "Rs. 2,00,000",
            "C": "Rs. 2,25,000",
            "D": "Cannot be determined"
        }
    },
    "2018_CS_GA_Q07": {
        "topic": "Quantitative Aptitude",
        "subtopic": "Numerical computation and estimation: ratios, percentages, powers, exponents and logarithms, permutations and combinations, series",
        "difficulty_level": "Easy",
        "explaination": "From $p^{-x} = \\frac{1}{q}$, we have $q = p^x$. Substituting into $q^{-y} = \\frac{1}{r}$ gives $r = q^y = (p^x)^y = p^{xy}$. Then $r^{-z} = \\frac{1}{p}$ gives $p = r^z = (p^{xy})^z = p^{xyz}$. Since $p > 0$ and $p \\neq 1$, it follows that $xyz = 1$.",
        "question_text_latex": "If $p^{-x} = \\frac{1}{q}$, $q^{-y} = \\frac{1}{r}$, and $r^{-z} = \\frac{1}{p}$, what is the value of $xyz$?",
        "options_latex": {
            "A": "$-1$",
            "B": "0",
            "C": "1",
            "D": "$pqr$"
        }
    },
    "2018_CS_GA_Q08": {
        "topic": "Quantitative Aptitude",
        "subtopic": "Numerical computation and estimation: ratios, percentages, powers, exponents and logarithms, permutations and combinations, series",
        "difficulty_level": "Easy",
        "explaination": "Out of 100 invited guests, 60 are male and 40 are female. Since 80 guests attend and all 40 invited females attend, the remaining $80 - 40 = 40$ attendees must be male. Thus, the ratio of attending males to attending females is $40 : 40 = 1 : 1$.",
        "question_text_latex": "In a party, 60\\% of the invited guests are male and 40\\% are female. 80\\% of the invited guests attend the party. If all the invited female guests attend the party, what is the ratio of male guests who attended to the female guests who attended?",
        "options_latex": {
            "A": "2 : 3",
            "B": "1 : 1",
            "C": "3 : 2",
            "D": "2 : 1"
        }
    },
    "2018_CS_GA_Q10": {
        "topic": "Quantitative Aptitude",
        "subtopic": "Elementary statistics and probability",
        "difficulty_level": "Medium",
        "explaination": "The number of green faces $X$ follows a Binomial distribution $B(n=7, p=4/6=2/3)$. The mode of a binomial distribution is $\\lfloor (n+1)p \\rfloor = \\lfloor 8 \\times \\frac{2}{3} \\rfloor = \\lfloor 5.33 \\rfloor = 5$. Thus, the most likely outcome is 5 green faces and $7 - 5 = 2$ red faces.",
        "question_text_latex": "A six sided unbiased die with four green faces and two red faces is rolled seven times. Which of the following combinations is the most likely outcome of the experiment?",
        "options_latex": {
            "A": "Three green faces and four red faces",
            "B": "Four green faces and three red faces",
            "C": "Five green faces and two red faces",
            "D": "Six green faces and one red face"
        }
    },
    "2018_CS_GA_Q26": {
        "topic": "Linear Algebra",
        "subtopic": "Eigenvalues and eigenvectors",
        "difficulty_level": "Medium",
        "explaination": "A $2 \\times 2$ matrix with only one linearly independent eigenvector has geometric multiplicity 1. This implies that the algebraic multiplicity of its eigenvalue must be 2 (repeated eigenvalues, so II is true) and that $P$ is not diagonalizable (so III is true). The determinant may be non-zero (e.g., $\\begin{bmatrix} 2 & 1 \\\\ 0 & 2 \\end{bmatrix}$), so I is not necessarily true.",
        "question_text_latex": "Consider a matrix $P = \\begin{bmatrix} a & b \\\\ c & d \\end{bmatrix}$. The only linearly independent eigenvector of $P$ is $\\begin{bmatrix} 1 \\\\ 4 \\end{bmatrix}$. Consider the following statements:\n\\begin{enumerate}[label=\\Roman*.]\n    \\item $\\det(P) = 0$\n    \\item $P$ has repeated eigenvalues\n    \\item $P$ is not diagonalizable\n\\end{enumerate}\nWhich of the statements above are necessarily TRUE?",
        "options_latex": {
            "A": "I and II only",
            "B": "I and III only",
            "C": "I, II and III",
            "D": "II and III only"
        }
    },
    "2018_CS_GA_Q27": {
        "topic": "Discrete Mathematics",
        "subtopic": "Sets, relations, functions, partial orders and lattices",
        "difficulty_level": "Medium",
        "explaination": "Set $P$ (rationals) is countably infinite. Set $Q$ (functions $\\{0, 1\\} \\to \\mathbb{N}$) is equivalent to $\\mathbb{N} \\times \\mathbb{N}$, which is countable. Set $S$ (finite subsets of $\\mathbb{N}$) is countable. Set $R$ (functions $\\mathbb{N} \\to \\{0, 1\\}$) is equivalent to the power set $\\mathcal{P}(\\mathbb{N})$ and has cardinality $2^{\\aleph_0}$, which is uncountable. Hence, $P$, $Q$, and $S$ are countable.",
        "question_text_latex": "Let $\\mathbb{N}$ denote the set of all natural numbers and $\\mathbb{Q}$ denote the set of all rational numbers. Consider the following sets:\n\\begin{itemize}[leftmargin=*, nosep]\n    \\item[$P$:] The set of all rational numbers between 0 and 1.\n    \\item[$Q$:] The set of all functions from $\\{0, 1\\}$ to $\\mathbb{N}$.\n    \\item[$R$:] The set of all functions from $\\mathbb{N}$ to $\\{0, 1\\}$.\n    \\item[$S$:] The set of all finite subsets of $\\mathbb{N}$.\n\\end{itemize}\nWhich of the sets above are countable?",
        "options_latex": {
            "A": "$P$ and $Q$ only",
            "B": "$Q$ and $R$ only",
            "C": "$P$, $Q$ and $R$ only",
            "D": "$P$, $Q$ and $S$ only"
        }
    },
    "2018_CS_GA_Q28": {
        "topic": "Discrete Mathematics",
        "subtopic": "Propositional and first order logic",
        "difficulty_level": "Hard",
        "explaination": "The sentence $\\varphi$ has existential quantifiers for 3 variables ($s, t, u$) followed exclusively by universal quantifiers for the remaining variables. If a structure satisfies $\\varphi$, the submodel formed by taking the domain as the elements corresponding to $s, t, u$ will itself satisfy the sentence because any elements evaluated under universal quantifiers are chosen from this 3-element domain.",
        "question_text_latex": "Consider the first-order logic sentence\n\\[ \\varphi \\equiv \\exists s \\, \\exists t \\, \\exists u \\, \\forall v \\, \\forall w \\, \\forall x \\, \\forall y \\; \\psi(s, t, u, v, w, x, y) \\]\nwhere $\\psi(s, t, u, v, w, x, y)$ is a quantifier-free first-order logic formula using only predicate symbols and variables (no functions or constants). If $\\varphi$ has a model with a universe of elements, then $\\varphi$ is guaranteed to have a model of size at most",
        "options_latex": {
            "A": "3",
            "B": "4",
            "C": "7",
            "D": "$\\infty$"
        }
    },
    "2018_CS_GA_Q29": {
        "topic": "Programming and Data Structures",
        "subtopic": "Programming in C",
        "difficulty_level": "Medium",
        "explaination": "In `fun1`, pointers `s1` and `s2` are passed by value, so the pointer swap only alters local variables and has no effect on `str1` and `str2` in `main` (printing \"Hi Bye\"). In `fun2`, the addresses of the pointers (`char**`) are passed, so dereferencing swaps the actual pointer values `str1` and `str2` (printing \"Bye Hi\").",
        "question_text_latex": "Consider the following C program:\n\\begin{lstlisting}[language=C]\n#include <stdio.h>\n\nvoid fun1(char *s1, char *s2) {\n    char *tmp;\n    tmp = s1;\n    s1 = s2;\n    s2 = tmp;\n}\n\nvoid fun2(char **s1, char **s2) {\n    char *tmp;\n    tmp = *s1;\n    *s1 = *s2;\n    *s2 = tmp;\n}\n\nint main() {\n    char *str1 = \"Hi\", *str2 = \"Bye\";\n    fun1(str1, str2);\n    printf(\"%s %s \", str1, str2);\n    fun2(&str1, &str2);\n    printf(\"%s %s\", str1, str2);\n    return 0;\n}\n\\end{lstlisting}\nThe output of the program is",
        "options_latex": {
            "A": "Hi Bye Bye Hi",
            "B": "Hi Bye Hi Bye",
            "C": "Bye Hi Bye Hi",
            "D": "Bye Hi Hi Bye"
        }
    },
    "2018_CS_GA_Q30": {
        "topic": "Algorithms",
        "subtopic": "Graph traversals, minimum spanning trees, shortest paths",
        "difficulty_level": "Medium",
        "explaination": "In a DFS tree of an undirected graph, every non-tree edge is a back edge connecting an ancestor and a descendant, so forward and cross edges do not exist; thus statement I is necessarily true. In a BFS tree, cross edges can connect vertices at the same level ($|i - j| = 0$), so statement II is false.",
        "question_text_latex": "Let $G$ be a simple undirected graph. Let $T_D$ be a depth first search tree of $G$. Let $T_B$ be a breadth first search tree of $G$. Consider the following statements:\n\\begin{enumerate}[label=\\Roman*.]\n    \\item For every edge $(u, v)$ of $G$, if $u$ is at depth $i$ and $v$ is at depth $j$ in $T_D$, then $|i - j| \\ge 1$.\n    \\item For every edge $(u, v)$ of $G$, if $u$ is at depth $i$ and $v$ is at depth $j$ in $T_B$, then $|i - j| = 1$.\n\\end{enumerate}\nWhich of the statements above is/are necessarily TRUE?",
        "options_latex": {
            "A": "I only",
            "B": "II only",
            "C": "Both I and II",
            "D": "Neither I nor II"
        }
    },
    "2018_CS_GA_Q31": {
        "topic": "Algorithms",
        "subtopic": "Algorithm design techniques: greedy, dynamic programming and divide-and-conquer",
        "difficulty_level": "Medium",
        "explaination": "Using dynamic programming for matrix chain multiplication with dimensions $d = \\langle 2, 25, 3, 16, 1, 10 \\rangle$: calculating minimum multiplication costs reveals optimal parenthesization as $((F_1(F_2 F_3))(F_4 F_5))$, where the intermediate pairs computed first are $F_2 F_3$ and $F_4 F_5$.",
        "question_text_latex": "Assume that multiplying a matrix $G_1$ of dimension $p \\times q$ with another matrix $G_2$ of dimension $q \\times r$ requires $pqr$ scalar multiplications. Computing the product of five matrices $F_1, F_2, F_3, F_4$ and $F_5$ of dimensions $2 \\times 25$, $25 \\times 3$, $3 \\times 16$, $16 \\times 1$ and $1 \\times 10$, respectively, using the minimum number of scalar multiplications requires first computing",
        "options_latex": {
            "A": "$F_1 F_2$ and $F_3 F_4$",
            "B": "$F_2 F_3$ and $F_3 F_4$",
            "C": "$F_2 F_3$ and $F_4 F_5$",
            "D": "$F_1 F_2$ and $F_4 F_5$"
        }
    },
    "2018_CS_GA_Q32": {
        "topic": "Algorithms",
        "subtopic": "Asymptotic worst case time and space complexity",
        "difficulty_level": "Medium",
        "explaination": "For $n = 2^{40}$, the first loop `n /= 2` executes until $n = 1$, which takes $\\log_2(2^{40}) = 40$ steps, giving $j = 40$. The second loop starts with $j = 40$ and halves $j$ until $j \\le 1$: values taken by $j$ are $40 \\to 20 \\to 10 \\to 5 \\to 2 \\to 1$, incrementing `sum` exactly 5 times.",
        "question_text_latex": "Consider the following C code. Assume that \\texttt{unsigned long int} type length is 64 bits.\n\\begin{lstlisting}[language=C]\nunsigned long int fun(unsigned long int n) {\n    unsigned long int i, j = 0, sum = 0;\n    while (n > 1) {\n        j++;\n        n /= 2;\n    }\n    for (i = 0; j > 1; i++) {\n        sum += (j % 2);\n        j /= 2;\n    }\n    return sum;\n}\n\\end{lstlisting}\nThe value returned when we call \\texttt{fun(pow(2, 40))} is",
        "options_latex": {
            "A": "4",
            "B": "5",
            "C": "6",
            "D": "40"
        }
    },
    "2018_CS_GA_Q33": {
        "topic": "Digital Logic",
        "subtopic": "Number representations and computer arithmetic (fixed and floating point)",
        "difficulty_level": "Medium",
        "explaination": "The fractional portion uses 3 bits ($b_2 b_1 b_0$), so the fractional precision is $2^{-3} = 0.125$. Any representable fraction must be an integer multiple of $0.125$: $0.500 = 4 \\times 0.125$ (i) and $0.875 = 7 \\times 0.125$ (ii) are exact multiples, while $0.100$ and $0.001$ are not.",
        "question_text_latex": "Consider the unsigned 8-bit fixed point binary number representation below:\n\\[ b_7 b_6 b_5 b_4 b_3 \\, . \\, b_2 b_1 b_0 \\]\nwhere the position of the binary point is between $b_3$ and $b_2$. Which of the following decimal numbers can be represented exactly in this format?\n\\begin{enumerate}[label=(\\roman*)]\n    \\item 0.500\n    \\item 0.875\n    \\item 0.100\n    \\item 0.001\n\\end{enumerate}",
        "options_latex": {
            "A": "(i) and (ii) only",
            "B": "(i) and (iii) only",
            "C": "(i) and (ii) only",
            "D": "(i), (ii) and (iii)"
        }
    },
    "2018_CS_GA_Q34": {
        "topic": "Computer Organization and Architecture",
        "subtopic": "Memory hierarchy: cache, main memory and secondary storage",
        "difficulty_level": "Medium",
        "explaination": "Block size $= 2^{M+W}$ bytes $\\implies M+W$ offset bits. Cache size $= 2^N$ bytes, so number of lines $= 2^N / 2^{M+W} = 2^{N-M-W}$. With $K = 2^k$ lines per set, number of sets $= 2^{N-M-W-k} \\implies N-M-W-k$ set index bits. Tag bits $= P - (N-M-W-k) - (M+W) = P - N + k = P - N + \\log_2 K$.",
        "question_text_latex": "The size of the physical address space of a processor is $2^P$ bytes. The word length is $2^W$ bytes. The capacity of cache memory is $2^N$ bytes. The size of each cache block is $2^M$ words. For a $K$-way set-associative cache memory, the length (in number of bits) of the tag field is",
        "options_latex": {
            "A": "$P - N - \\log_2 K$",
            "B": "$P - N + \\log_2 K$",
            "C": "$P - N - M - W - \\log_2 K$",
            "D": "$P - N - M - W + \\log_2 K$"
        }
    },
    "2018_CS_GA_Q35": {
        "topic": "Theory of Computation",
        "subtopic": "Context-free grammars and push-down automata",
        "difficulty_level": "Medium",
        "explaination": "Language I has condition $m - n = q - p$, which can be checked by pushing $a$'s, popping for $b$'s, then pushing/popping for $c$ and $d$ on a single PDA stack (CFL). Language II is the concatenation of CFLs $L_1 = \\{a^m b^m\\}$ and $L_2 = \\{c^p d^p\\}$, hence a CFL. Languages III and IV require multi-variable dependencies across non-adjacent symbols simultaneously, which cannot be handled by a single stack (non-CFL).",
        "question_text_latex": "Consider the following languages:\n\\begin{itemize}[leftmargin=*, nosep]\n    \\item[I.] $\\{a^m b^n c^p d^q \\mid m + p = n + q, \\text{ where } m, n, p, q \\ge 0\\}$\n    \\item[II.] $\\{a^m b^n c^p d^q \\mid m = n \\text{ and } p = q, \\text{ where } m, n, p, q \\ge 0\\}$\n    \\item[III.] $\\{a^m b^n c^p d^q \\mid m = p \\text{ and } n = q, \\text{ where } m, n, p, q \\ge 0\\}$\n    \\item[IV.] $\\{a^m b^n c^p d^q \\mid m = q \\text{ and } n = p, \\text{ where } m, n, p, q \\ge 0\\}$\n\\end{itemize}\nWhich of the languages above are context-free?",
        "options_latex": {
            "A": "I and IV only",
            "B": "I and II only",
            "C": "II and III only",
            "D": "II and IV only"
        }
    },
    "2018_CS_GA_Q36": {
        "topic": "Theory of Computation",
        "subtopic": "Turing machines and undecidability",
        "difficulty_level": "Hard",
        "explaination": "Problem I (membership for unrestricted grammars) is undecidable. Problem II (testing if a TM accepts a regular language) is undecidable by Rice's theorem. Problem III (equivalence of CFGs) is undecidable. Problem IV asks whether a regular language (NFA) equals a deterministic context-free language (DPDA), which is decidable. Hence, I, II, and III are undecidable.",
        "question_text_latex": "Consider the following problems. $L(G)$ denotes the language generated by a grammar $G$. $L(M)$ denotes the language accepted by a machine $M$.\n\\begin{enumerate}[label=\\Roman*.]\n    \\item For an unrestricted grammar $G$ and a string $w$, whether $w \\in L(G)$\n    \\item Given a Turing machine $M$, whether $L(M)$ is regular\n    \\item Given two grammars $G_1$ and $G_2$, whether $L(G_1) = L(G_2)$\n    \\item Given an NFA $N$ and a DPDA $D$, whether $L(N) = L(D)$\n\\end{enumerate}\nWhich of the above problems are UNDECIDABLE?",
        "options_latex": {
            "A": "I and IV only",
            "B": "II and III only",
            "C": "III and IV only",
            "D": "I, II and III only"
        }
    },
    "2018_CS_GA_Q37": {
        "topic": "Compiler Design",
        "subtopic": "Lexical analysis, parsing, syntax-directed translation",
        "difficulty_level": "Medium",
        "explaination": "A lexical analyzer applies the longest match rule. For input `bbaacabc`, pattern $T_3 = c?(b|a)^*c$ matches prefix `bbaac` (starts without $c$, matches $(b|a)^* = bbaa$, ends with $c$), consuming `bbaac` as token $T_3$. The remaining string is `abc`, which also matches $T_3$ (starts without $c$, $(b|a)^* = ab$, ends with $c$). Hence the recognized sequence of tokens is $T_3 T_3$.",
        "question_text_latex": "A lexical analyzer uses the following patterns to recognize three tokens $T_1, T_2$, and $T_3$ over the alphabet $\\{a, b, c\\}$:\n\\[ T_1: a?(b|c)^*a \\qquad T_2: b?(a|c)^*b \\qquad T_3: c?(b|a)^*c \\]\nNote that '?' means 0 or 1 occurrence of the preceding symbol. The analyzer matches the longest prefix of the remaining input. For the input string `bbaacabc`, the token sequence generated is",
        "options_latex": {
            "A": "$T_1 T_2 T_3$",
            "B": "$T_1 T_3$",
            "C": "$T_2 T_1 T_3$",
            "D": "$T_3 T_3$"
        }
    },
    "2018_CS_GA_Q39": {
        "topic": "Operating System",
        "subtopic": "Deadlock",
        "difficulty_level": "Medium",
        "explaination": "Currently Allocated: $E = 2+0+0+1 = 3$, $F = 0+1+0+0 = 1$, $G = 1+0+1+0 = 2$. Available resources $= (6-3, 4-1, 2-2) = (3, 3, 0)$. Need matrix: $P_0(3, 3, 0)$, $P_1(1, 1, 1)$, $P_2(0, 3, 0)$, $P_3(2, 2, 1)$. Since $\\text{Need}(P_0) \\le \\text{Available}$, $P_0$ can finish, releasing its allocation $(2, 0, 1)$ to make Available $(5, 3, 1)$. Next $P_2, P_1, P_3$ can all execute. Thus, the system is in a safe state.",
        "question_text_latex": "In a system, there are three types of resources: $E, F$ and $G$. Four processes $P_0, P_1, P_2$ and $P_3$ execute concurrently. At time $t_0$, the maximum need and current allocation of resources are:\n\\begin{center}\n\\begin{tabular}{c|ccc|ccc}\n\\textbf{Process} & \\multicolumn{3}{c|}{\\textbf{Allocation}} & \\multicolumn{3}{c}{\\textbf{Max Need}} \\\\\n& $E$ & $F$ & $G$ & $E$ & $F$ & $G$ \\\\\n\\hline\n$P_0$ & 2 & 0 & 1 & 5 & 3 & 1 \\\\\n$P_1$ & 0 & 1 & 0 & 1 & 2 & 1 \\\\\n$P_2$ & 0 & 0 & 1 & 0 & 3 & 1 \\\\\n$P_3$ & 1 & 0 & 0 & 3 & 2 & 1 \\\\\n\\end{tabular}\n\\end{center}\nTotal resources are: $E = 6, F = 4, G = 2$. The system at time $t_0$ is in",
        "options_latex": {
            "A": "a safe state.",
            "B": "an unsafe state, but not in a deadlock.",
            "C": "a deadlock.",
            "D": "none of the above."
        }
    },
    "2018_CS_GA_Q40": {
        "topic": "Operating System",
        "subtopic": "Concurrency and synchronization",
        "difficulty_level": "Medium",
        "explaination": "In the standard producer-consumer problem with a buffer of size $N$, `empty` is initialized to $N$ and `full` is initialized to $0$. The producer waits on `empty` and signals `full`. Conversely, the consumer waits on `full` and signals `empty`. Comparing this with the provided code reveals that semaphore `empty` corresponds to buffer spaces and `full` corresponds to items, making $P: \\text{full}, Q: \\text{empty}, R: \\text{empty}, S: \\text{full}$.",
        "question_text_latex": "Consider the following solution to the producer-consumer synchronization problem. The shared buffer size is $N$. Three semaphores $empty, full$ and $mutex$ are used with initial values $N, 0$ and $1$, respectively.\n\\begin{lstlisting}[language=C]\n// Producer:\nwhile (1) {\n    produce();\n    wait(P);\n    wait(mutex);\n    put_item();\n    signal(mutex);\n    signal(Q);\n}\n\n// Consumer:\nwhile (1) {\n    wait(R);\n    wait(mutex);\n    remove_item();\n    signal(mutex);\n    signal(S);\n    consume();\n}\n\\end{lstlisting}\nWhich of the following choices for $P, Q, R, S$ makes the solution correct?",
        "options_latex": {
            "A": "$P: empty, Q: full, R: empty, S: full$",
            "B": "$P: empty, Q: full, R: full, S: empty$",
            "C": "$P: full, Q: empty, R: empty, S: full$",
            "D": "$P: full, Q: empty, R: full, S: empty$"
        }
    },
    "2018_CS_GA_Q41": {
        "topic": "Databases",
        "subtopic": "Relational model: relational algebra, tuple calculus, SQL",
        "difficulty_level": "Medium",
        "explaination": "Query $Q$ inner joins $r$ with $\\sigma_{B < 5}(s)$, which discards all tuples from $r$ where $B \\ge 5$. Option (C) performs a left outer join between $r$ and $\\sigma_{B < 5}(s)$, which retains all tuples from $r$ (filling missing $C$ values with NULL for $B \\ge 5$), so its result is NOT equivalent to $Q$.",
        "question_text_latex": "Consider the relations $r(A, B)$ and $s(B, C)$, where $s.B$ is a primary key and $r.B$ is a foreign key referencing $s.B$. Consider the query:\n\\[ Q: \\Pi_{A, B, C}(r \\bowtie \\sigma_{B < 5}(s)) \\]\nWhich one of the following relational algebra queries is NOT equivalent to $Q$?",
        "options_latex": {
            "A": "$\\Pi_{A, B, C}(\\sigma_{B < 5}(r) \\bowtie s)$",
            "B": "$\\sigma_{B < 5}(\\Pi_{A, B, C}(r \\bowtie s))$",
            "C": "$\\Pi_{A, B, C}(r \\,\\text{⟕}\\, \\sigma_{B < 5}(s))$",
            "D": "$\\Pi_{A, B, C}(\\sigma_{B < 5}(r \\bowtie s))$"
        }
    },
    "2018_CS_GA_Q42": {
        "topic": "Databases",
        "subtopic": "Integrity constraints, normal forms",
        "difficulty_level": "Medium",
        "explaination": "In Schema II, the functional dependencies are $rollno \\to email$ and $email \\to rollno$. The candidate keys are $\\{rollno, courseid\\}$ and $\\{email, courseid\\}$. In $email \\to rollno$, the left side is not a superkey (violating BCNF), but the right side $rollno$ is a prime attribute (satisfying 3NF). Hence Schema II is in 3NF but not in BCNF.",
        "question_text_latex": "Consider the following four relational schemas. For each schema, all non-trivial functional dependencies are listed. The underlined attributes denote candidate keys.\n\\begin{itemize}[leftmargin=*, nosep]\n    \\item[Schema I:] $R_1(A, B, C, D)$ with FDs: $A \\to B, B \\to C, C \\to D$\n    \\item[Schema II:] $R_2(\\underline{rollno}, \\underline{courseid}, email)$ with FDs: $rollno \\to email, email \\to rollno$\n    \\item[Schema III:] $R_3(A, B, C)$ with FDs: $A \\to B, B \\to C$\n    \\item[Schema IV:] $R_4(A, B, C)$ with FDs: $AB \\to C, C \\to A$\n\\end{itemize}\nWhich one of the relational schemas is in 3NF but not in BCNF?",
        "options_latex": {
            "A": "Schema I",
            "B": "Schema II",
            "C": "Schema III",
            "D": "Schema IV"
        }
    },
    "2018_CS_GA_Q43": {
        "topic": "Discrete Mathematics",
        "subtopic": "Graphs: connectivity, matching, colouring",
        "difficulty_level": "Hard",
        "explaination": "Each permutation of length 100 has 99 pairs of adjacent elements that can be swapped, so the degree of each vertex is $y = 99$. Adjacent transpositions generate the entire symmetric group $S_{100}$, meaning every permutation is reachable from any other; thus the graph is connected, giving $z = 1$ connected component. Hence $y + 10z = 99 + 10(1) = 109$.",
        "question_text_latex": "Let $G$ be a graph with $100!$ vertices, with each vertex labelled by a distinct permutation of the numbers $1, 2, \\dots, 100$. There is an edge between two vertices if and only if the permutation of one can be obtained by swapping two adjacent elements of the other. Let $y$ be the degree of a vertex in $G$ and $z$ be the number of connected components in $G$. Then $y + 10z =$ \\_\\_\\_\\_\\_\\_\\_\\_.",
        "options_latex": None
    },
    "2018_CS_GA_Q44": {
        "topic": "Probability and Statistics",
        "subtopic": "Conditional probability and Bayes theorem",
        "difficulty_level": "Medium",
        "explaination": "Using the law of total probability, the probability of high temperature in Delhi is $P(H_D) = 0.2(0.40) + 0.5(0.10) + 0.3(0.01) = 0.08 + 0.05 + 0.003 = 0.133$. By Bayes' theorem, $P(H_G \\mid H_D) = \\frac{P(H_G \\cap H_D)}{P(H_D)} = \\frac{0.08}{0.133} \\approx 0.6015$, which falls in the range $0.60$ to $0.62$.",
        "question_text_latex": "Consider Guwahati ($G$) and Delhi ($D$) whose temperatures can be classified as high ($H$), medium ($M$) and low ($L$). Let $P(H_G) = 0.2$, $P(M_G) = 0.5$, and $P(L_G) = 0.3$ be the probabilities that Guwahati has high, medium, and low temperatures, respectively. Given $P(H_D \\mid H_G) = 0.40$, $P(H_D \\mid M_G) = 0.10$, and $P(H_D \\mid L_G) = 0.01$, the conditional probability $P(H_G \\mid H_D)$ is \\_\\_\\_\\_\\_\\_\\_\\_. (Answer correct to two decimal places)",
        "options_latex": None
    },
    "2018_CS_GA_Q45": {
        "topic": "Programming and Data Structures",
        "subtopic": "Recursion",
        "difficulty_level": "Medium",
        "explaination": "In `Count(x, y)`, outer recursion on $y$ runs for $y = 1024, 1023, \\dots, 2$ ($1023$ values). For each $y$, the inner branch halves $x$ until $x = 1$: starting from $x = 1024$, this loop prints 10 times (since $\\log_2(1024) = 10$). Total prints $= 1023 \\times 10 = 10230$.",
        "question_text_latex": "Consider the following pseudo-code function where $x$ and $y$ are positive integers:\n\\begin{lstlisting}[language=C]\nCount(x, y) {\n    if (y != 1) {\n        if (x != 1) {\n            print(\"*\");\n            Count(x / 2, y);\n        } else {\n            Count(1024, y - 1);\n        }\n    }\n}\n\\end{lstlisting}\nThe total number of times `print(\"*\")` is executed for `Count(1024, 1024)` is \\_\\_\\_\\_\\_\\_\\_\\_.",
        "options_latex": None
    },
    "2018_CS_GA_Q46": {
        "topic": "Programming and Data Structures",
        "subtopic": "Trees, binary search trees, binary heaps",
        "difficulty_level": "Medium",
        "explaination": "In a min-heap of 7 elements, the root must contain the minimum element (1). The left subtree has size 3 and the right subtree has size 3. Choosing 3 elements for the left subtree from the remaining 6 elements can be done in $\\binom{6}{3} = 20$ ways. A 3-element min-heap has $\\binom{2}{1} = 2$ valid configurations. Hence, total valid min-heaps $= 20 \\times 2 \\times 2 = 80$.",
        "question_text_latex": "The number of possible min-heaps containing each value from $\\{1, 2, 3, 4, 5, 6, 7\\}$ exactly once is \\_\\_\\_\\_\\_\\_\\_\\_.",
        "options_latex": None
    },
    "2018_CS_GA_Q48": {
        "topic": "Algorithms",
        "subtopic": "Algorithm design techniques: greedy, dynamic programming and divide-and-conquer",
        "difficulty_level": "Medium",
        "explaination": "Value-to-weight ratios: Item 4 ($24/2 = 12$), Item 1 ($60/10 = 6$), Item 3 ($20/4 = 5$), Item 2 ($28/7 = 4$). The heuristic sorts by ratio and greedily takes Item 4 (wt 2, remaining 9); Item 1 does not fit ($10 > 9$); Item 3 fits (wt 4, remaining 5); Item 2 does not fit ($7 > 5$), yielding $V_{\\text{heuristic}} = 24 + 20 = 44$. The optimal 0/1 knapsack selection picks Item 1 (wt 10, val 60). Thus $V_{\\text{opt}} - V_{\\text{heuristic}} = 60 - 44 = 16$.",
        "question_text_latex": "Consider the following items with weights and values:\n\\begin{center}\n\\begin{tabular}{ccc}\n\\textbf{Item} & \\textbf{Weight} & \\textbf{Value} \\\\\n1 & 10 & 60 \\\\\n2 & 7 & 28 \\\\\n3 & 4 & 20 \\\\\n4 & 2 & 24 \\\\\n\\end{tabular}\n\\end{center}\nA knapsack has capacity 11. A greedy heuristic sorts items in decreasing order of value-to-weight ratio and picks each item that fits. Let $V_{\\text{opt}}$ and $V_{\\text{heuristic}}$ denote the optimal knapsack value and heuristic value, respectively. The value of $V_{\\text{opt}} - V_{\\text{heuristic}}$ is \\_\\_\\_\\_\\_\\_\\_\\_.",
        "options_latex": None
    },
    "2018_CS_GA_Q50": {
        "topic": "Computer Organization and Architecture",
        "subtopic": "Instruction pipelining, pipeline hazards",
        "difficulty_level": "Medium",
        "explaination": "For 100 instructions in a 5-stage pipeline without branch delays, ideal cycles $= 5 + (100 - 1) = 104$. The PO stage causes pipeline stalls when operand evaluation takes extra cycles: 40 instructions require 3 cycles (2 extra cycles $\\implies 40 \\times 2 = 80$ stall cycles) and 35 instructions require 2 cycles (1 extra cycle $\\implies 35 \\times 1 = 35$ stall cycles). Total clock cycles $= 104 + 80 + 35 = 219$.",
        "question_text_latex": "The instruction pipeline of a RISC processor has five stages: Instruction Fetch (IF), Instruction Decode (ID), Perform Operation (PO), Operand Read (OR), and Write Back (WB). Each stage takes 1 clock cycle except PO. For a sequence of 100 instructions, 40 instructions require 3 clock cycles in PO, 35 instructions require 2 clock cycles in PO, and the remaining 25 instructions require 1 clock cycle in PO. Assuming no memory stalls or branch delays, the total number of clock cycles to execute the 100 instructions is \\_\\_\\_\\_\\_\\_\\_\\_.",
        "options_latex": None
    },
    "2018_CS_GA_Q51": {
        "topic": "Computer Organization and Architecture",
        "subtopic": "Machine instructions and addressing modes",
        "difficulty_level": "Hard",
        "explaination": "A 16-bit instruction space has $2^{16} = 65536$ encodings. Type-1: 4 instructions with $3 \\times 4\\text{-bit}$ registers consume $4 \\times 2^{12} = 16384$. Type-2: 8 instructions with $2 \\times 6\\text{-bit}$ registers consume $8 \\times 2^{12} = 32768$. Type-3: 14 instructions with 4-bit and 6-bit registers consume $14 \\times 2^{10} = 14336$. Remaining encodings $= 65536 - (16384 + 32768 + 14336) = 2048$. Each Type-4 instruction uses one 6-bit register ($2^6 = 64$ encodings). Thus, maximum $N = 2048 / 64 = 32$.",
        "question_text_latex": "A processor has 16 integer registers (R0 to R15) and 64 floating point registers (F0 to F63). It uses a 16-bit instruction format. Four types of instructions are supported:\n\\begin{itemize}[leftmargin=*, nosep]\n    \\item Type-1: Opcode with three integer register operands\n    \\item Type-2: Opcode with two floating point register operands\n    \\item Type-3: Opcode with one integer and one floating point register operand\n    \\item Type-4: Opcode with one floating point register operand\n\\end{itemize}\nIf there are 4 Type-1, 8 Type-2, and 14 Type-3 instructions, the maximum number of Type-4 instructions that can be supported is \\_\\_\\_\\_\\_\\_\\_\\_.",
        "options_latex": None
    },
    "2018_CS_GA_Q52": {
        "topic": "Theory of Computation",
        "subtopic": "Regular expressions and finite automata",
        "difficulty_level": "Hard",
        "explaination": "The given automaton on alphabet $\\{0\\}$ accepts $L = \\{0, 00, 000, \\dots\\} = 0^+$. Its powers are $L^2 = \\{0^k \\mid k \\ge 2\\}$, $L^3 = \\{0^k \\mid k \\ge 3\\}$. For the language of strings accepted by the automaton, the smallest integer $k$ satisfying $L^k = L^{k+1}$ is 2.",
        "question_text_latex": "Given a language $L$, define $L^i$ as $L^0 = \\{\\varepsilon\\}$ and $L^i = L^{i-1} \\cdot L$ for $i > 0$. The order of a language $L$ is defined as the smallest $k$ such that $L^k = L^{k+1}$. Consider the finite automaton accepting $L$ over $\\{0\\}$ where states accept strings of positive length. The order of language $L$ is \\_\\_\\_\\_\\_\\_\\_\\_.",
        "options_latex": None
    },
    "2018_CS_GA_Q53": {
        "topic": "Operating System",
        "subtopic": "File systems",
        "difficulty_level": "Medium",
        "explaination": "Using Shortest Seek Time First (SSTF) starting at cylinder 80: closest is 86 (diff 6, upward), then 72 (diff 14, downward $\\implies$ reversal 1), then 116 (diff 44, upward $\\implies$ reversal 2), then 134 (diff 18, upward), then 20 (diff 114, downward $\\implies$ reversal 3), and finally 16 (diff 4, downward). Total cylinder distance $= 6 + 14 + 44 + 18 + 114 + 4 = 200$. Head movement power $= 200 \\times 0.2\\text{ mW} = 40\\text{ mW}$. Direction reversals $= 3 \\times 15\\text{ mW} = 45\\text{ mW}$. Total power consumed $= 40 + 45 = 85\\text{ mW}$.",
        "question_text_latex": "Consider a storage disk with 200 cylinders (0 to 199). Requests arrive for cylinders: 16, 20, 72, 86, 116, 134. The read/write head is currently at cylinder 80 and moving towards higher cylinder numbers. The SSTF algorithm is used. The disk arm consumes 0.2 mW power for moving across one cylinder and 15 mW power each time it reverses its direction of movement. The total power consumed (in mW) to service all requests is \\_\\_\\_\\_\\_\\_\\_\\_.",
        "options_latex": None
    },
    "2018_CS_GA_Q54": {
        "topic": "Computer Networks",
        "subtopic": "Fragmentation and IP addressing, IPv4, CIDR notation",
        "difficulty_level": "Medium",
        "explaination": "Total payload to fragment $= 4500 - 20 = 4480$ bytes. With $\\text{MTU} = 600$, maximum payload per fragment must be a multiple of 8: $\\lfloor (600 - 20) / 8 \\rfloor \\times 8 = 72 \\times 8 = 576$ bytes. Fragment 1 carries bytes 0 to 575 (offset 0). Fragment 2 carries bytes 576 to 1151 (offset $576/8 = 72$). Fragment 3 carries bytes 1152 onwards, so its fragment offset field is $\\frac{1152}{8} = 144$.",
        "question_text_latex": "Consider an IP packet with a length of 4,500 bytes that includes a 20-byte IPv4 header and a 40-byte TCP header. The packet is forwarded across an IP network with an MTU of 600 bytes. The value of the fragment offset field in the third fragment (in 8-byte units) is \\_\\_\\_\\_\\_\\_\\_\\_.",
        "options_latex": None
    }
}

GA_MODULES = {"Verbal Aptitude", "Quantitative Aptitude", "Analytical Aptitude", "Spatial Aptitude"}

def main():
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    paper_dir = os.path.join(root_dir, "dataset", "papers", "2018_CS")

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
                
                # Accurately tag section and section_code
                if enr["topic"] in GA_MODULES:
                    q["section"] = "General Aptitude"
                    q["section_code"] = "GA"
                else:
                    q["section"] = "Computer Science and Information Technology"
                    q["section_code"] = "CS"

                updated_count += 1
            else:
                print(f"Notice: No enrichment found for {qid}")

        with open(fpath, "w", encoding="utf-8") as fp:
            json.dump(data, fp, indent=2, ensure_ascii=False)

    print(f"Enriched {updated_count} questions in 2018_CS paper files successfully.")

if __name__ == "__main__":
    main()

