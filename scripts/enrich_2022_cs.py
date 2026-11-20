#!/usr/bin/env python3
"""
enrich_2022_cs.py

Fills the AI metadata fields for 2022 CS questions based on syllabus/cs_2026_syllabus.json:
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
    "2022_CS_GA_Q01": {
        "topic": "Verbal Aptitude",
        "subtopic": "Vocabulary: words, idioms, and phrases in context",
        "difficulty_level": "Easy",
        "explaination": "'Fare' denotes the price charged for a journey or conveyance, whereas 'fair' means reasonable or just. Therefore, 'The fare is too high for it to be considered fair.'",
        "question_text_latex": "The \\_\\_\\_\\_\\_\\_\\_\\_\\_ is too high for it to be considered \\_\\_\\_\\_\\_\\_\\_\\_\\_.",
        "options_latex": {
            "A": "fair / fare",
            "B": "faer / fair",
            "C": "fare / fare",
            "D": "fare / fair"
        }
    },
    "2022_CS_GA_Q02": {
        "topic": "Calculus",
        "subtopic": "Integration",
        "difficulty_level": "Easy",
        "explaination": "The area under the piecewise step function is the sum of the rectangular areas: $\\int_0^1 y(x) \\, dx = 2\\left(\\frac{1}{3} - 0\\right) + 3\\left(\\frac{3}{4} - \\frac{1}{3}\\right) + 1\\left(1 - \\frac{3}{4}\\right) = \\frac{2}{3} + 3\\left(\\frac{5}{12}\\right) + \\frac{1}{4} = \\frac{2}{3} + \\frac{5}{4} + \\frac{1}{4} = \\frac{2}{3} + \\frac{3}{2} = \\frac{13}{6}$.",
        "question_text_latex": "A function $y(x)$ is defined in the interval $[0, 1]$ on the $x$-axis as\n\\[ y(x) = \\begin{cases} 2 & \\text{if } 0 \\le x < \\frac{1}{3} \\\\ 3 & \\text{if } \\frac{1}{3} \\le x < \\frac{3}{4} \\\\ 1 & \\text{if } \\frac{3}{4} \\le x \\le 1 \\end{cases} \\]\nWhich one of the following is the area under the curve for the interval $[0, 1]$ on the $x$-axis?",
        "options_latex": {
            "A": "$5/6$",
            "B": "$6/5$",
            "C": "$13/6$",
            "D": "$6/13$"
        }
    },
    "2022_CS_GA_Q03": {
        "topic": "Quantitative Aptitude",
        "subtopic": "Numerical computation and estimation: ratios, percentages, powers, exponents and logarithms, permutations and combinations, series",
        "difficulty_level": "Medium",
        "explaination": "Since $r$ is a root of $x^2 + 2x + 6 = 0$, we have $r^2 + 2r = -6$. Pairing terms in the expression: $[(r+2)(r+5)][(r+3)(r+4)] = [r^2 + 7r + 10][r^2 + 7r + 12]$. Substituting $r^2 = -2r - 6$ yields $(5r + 4)(5r + 6) = 25r^2 + 50r + 24 = 25(r^2 + 2r) + 24 = 25(-6) + 24 = -126$.",
        "question_text_latex": "Let $r$ be a root of the equation $x^2 + 2x + 6 = 0$.\nThen the value of the expression $(r+2)(r+3)(r+4)(r+5)$ is",
        "options_latex": {
            "A": "51",
            "B": "$-51$",
            "C": "126",
            "D": "$-126$"
        }
    },
    "2022_CS_GA_Q04": {
        "topic": "Analytical Aptitude",
        "subtopic": "Logic: deduction and induction",
        "difficulty_level": "Easy",
        "explaination": "Statement 1 (\"All students are inquisitive\") and Statement 3 (\"No student is inquisitive\") are universal affirmative and universal negative statements (contraries). In classical categorical logic with a non-empty class, both statements cannot be simultaneously true.",
        "question_text_latex": "Given below are four statements:\n\\begin{itemize}[itemsep=0pt,topsep=2pt]\n\\item Statement 1: All students are inquisitive.\n\\item Statement 2: Some students are inquisitive.\n\\item Statement 3: No student is inquisitive.\n\\item Statement 4: Some students are not inquisitive.\n\\end{itemize}\nFrom the given four statements, find the two statements that CANNOT BE TRUE simultaneously, assuming that there is at least one student in the class.",
        "options_latex": {
            "A": "Statement 1 and Statement 3",
            "B": "Statement 1 and Statement 2",
            "C": "Statement 2 and Statement 4",
            "D": "Statement 3 and Statement 4"
        }
    },

    # ==================== GA 2-MARK ====================
    "2022_CS_GA_Q06": {
        "topic": "Verbal Aptitude",
        "subtopic": "Reading and comprehension",
        "difficulty_level": "Easy",
        "explaination": "The passage explicitly notes that \"In organizations with good work culture, metrics help improve outcomes.\" This directly implies that metrics are useful in organizations with good work culture.",
        "question_text_latex": "Some people believe that ``what gets measured, improves''. Some others believe that ``what gets measured, gets gamed''. One possible reason for the difference in the beliefs is the work culture in organizations. In organizations with good work culture, metrics help improve outcomes. However, the same metrics are counterproductive in organizations with poor work culture.\nWhich one of the following is the CORRECT logical inference based on the information in the above passage?",
        "options_latex": {
            "A": "Metrics are useful in organizations with poor work culture",
            "B": "Metrics are useful in organizations with good work culture",
            "C": "Metrics are always counterproductive in organizations with good work culture",
            "D": "Metrics are never useful in organizations with good work culture"
        }
    },
    "2022_CS_GA_Q07": {
        "topic": "Quantitative Aptitude",
        "subtopic": "Numerical computation and estimation: ratios, percentages, powers, exponents and logarithms, permutations and combinations, series",
        "difficulty_level": "Easy",
        "explaination": "Among all candidates who qualified, girls accounted for 60%, meaning boys accounted for the remaining $100\\% - 60\\% = 40\\%$. Because $40\\% < 60\\%$, the total number of boys who qualified is strictly less than the number of girls who qualified.",
        "question_text_latex": "In a recently conducted national entrance test, boys constituted 65\\% of those who appeared for the test. Girls constituted the remaining candidates and they accounted for 60\\% of the qualified candidates.\nWhich one of the following is the correct logical inference based on the information provided in the above passage?",
        "options_latex": {
            "A": "Equal number of boys and girls qualified",
            "B": "Equal number of boys and girls appeared for the test",
            "C": "The number of boys who appeared for the test is less than the number of girls who appeared",
            "D": "The number of boys who qualified the test is less than the number of girls who qualified"
        }
    },
    "2022_CS_GA_Q08": {
        "topic": "Quantitative Aptitude",
        "subtopic": "Elementary statistics and probability",
        "difficulty_level": "Medium",
        "explaination": "Initially, there are 3 green and 2 orange balls (total 5). If a green ball is drawn ($P(G_1) = 3/5$), 2 green and 2 orange remain, so $P(O_2|G_1) = 2/4 = 1/2$. If an orange ball is drawn ($P(O_1) = 2/5$), it is replaced, so $P(O_2|O_1) = 2/5$. By the law of total probability, $P(O_2) = \\left(\\frac{3}{5}\\right)\\left(\\frac{1}{2}\\right) + \\left(\\frac{2}{5}\\right)\\left(\\frac{2}{5}\\right) = \\frac{3}{10} + \\frac{4}{25} = \\frac{23}{50}$.",
        "question_text_latex": "A box contains five balls of same size and shape. Three of them are green coloured balls and two of them are orange coloured balls. Balls are drawn from the box one at a time. If a green ball is drawn, it is not replaced. If an orange ball is drawn, it is replaced with another orange ball.\nFirst ball is drawn. What is the probability of getting an orange ball in the next draw?",
        "options_latex": {
            "A": "$1/2$",
            "B": "$8/25$",
            "C": "$19/50$",
            "D": "$23/50$"
        }
    },
    "2022_CS_GA_Q09": {
        "topic": "Spatial Aptitude",
        "subtopic": "Transformation of shapes: translation, rotation, scaling, mirroring, assembling, and grouping",
        "difficulty_level": "Hard",
        "explaination": "In a triangle, a segment connecting two midpoints is parallel to the opposite side joining two vertices. Between segments $PR$ and $QS$, one must connect two corners and the other two midpoints. If $S$ were a corner, then $Q$ and $S$ would both be corners, leaving $P$ and $R$ as midpoints, which violates the condition that $S$ and $U$ cannot share a side while $P$ opposes corner $T$. Thus, $S$ cannot be placed at a corner.",
        "question_text_latex": "The corners and mid-points of the sides of a triangle are named using the distinct letters P, Q, R, S, T and U, but not necessarily in the same order. Consider the following statements:\n\\begin{itemize}[itemsep=0pt,topsep=2pt]\n\\item The line joining P and R is parallel to the line joining Q and S.\n\\item P is placed on the side opposite to the corner T.\n\\item S and U cannot be placed on the same side.\n\\end{itemize}\nWhich one of the following statements is correct based on the above information?",
        "options_latex": {
            "A": "P cannot be placed at a corner",
            "B": "S cannot be placed at a corner",
            "C": "U cannot be placed at a mid-point",
            "D": "R cannot be placed at a corner"
        }
    },
    "2022_CS_GA_Q10": {
        "topic": "Spatial Aptitude",
        "subtopic": "Paper folding, cutting, and patterns in 2 and 3 dimensions",
        "difficulty_level": "Medium",
        "explaination": "To partition the rectangular plot into four mutually similar subplots respecting the existing fixed ropes R1 and R2, exactly 3 additional collinear straight rope segments are needed to complete the congruent triangular and trapezoidal subdivisions.",
        "question_text_latex": "A plot of land must be divided between four families. They want their individual plots to be similar in shape, not necessarily equal in area. The land has equally spaced poles, marked as dots in the figure. Two ropes, R1 and R2, are already present and cannot be moved.\nWhat is the least number of additional straight ropes needed to create the desired plots? A single rope can pass through three poles that are aligned in a straight line.",
        "options_latex": {
            "A": "2",
            "B": "4",
            "C": "5",
            "D": "3"
        }
    },

    # ==================== CS 1-MARK ====================
    "2022_CS_CS_Q11": {
        "topic": "Algorithms",
        "subtopic": "Asymptotic worst case time and space complexity",
        "difficulty_level": "Medium",
        "explaination": "If $f(n)$ is a polynomial of degree $k$ ($f(n) = \\Theta(n^k)$), then $f(n^2) = \\Theta((n^2)^k) = \\Theta(n^{2k})$, and $(f(n))^2 = (\\Theta(n^k))^2 = \\Theta(n^{2k})$. Since both functions grow at identical polynomial rates, $f(n^2) = \\Theta((f(n))^2)$ holds.",
        "question_text_latex": "Which one of the following statements is TRUE for all positive functions $f(n)$?",
        "options_latex": {
            "A": "$f(n^2) = \\Theta((f(n))^2)$, when $f(n)$ is a polynomial",
            "B": "$f(n^2) = o((f(n))^2)$",
            "C": "$f(n^2) = \\mathcal{O}((f(n))^2)$, when $f(n)$ is an exponential function",
            "D": "$f(n^2) = \\Omega((f(n))^2)$"
        }
    },
    "2022_CS_CS_Q12": {
        "topic": "Theory of Computation",
        "subtopic": "Regular expressions and finite automata",
        "difficulty_level": "Medium",
        "explaination": "From the start state, loops on intermediate states allow repeating patterns of $ba^*a$ and $ab^*b$ before moving to an accepting state via either $ab^*$ or $ba^*$. Factoring loop paths and exit transitions yields the regular expression $(ba^*a + ab^*b)^*(ab^* + ba^*)$.",
        "question_text_latex": "Which one of the following regular expressions correctly represents the language of the finite automaton given below?",
        "options_latex": {
            "A": "$ab^*ba^* + ba^*ab^*$",
            "B": "$(ab^*b + ba^*a)^*(a + b)$",
            "C": "$(ab^*b + ba^*a)^*(a^*b + b^*a)$",
            "D": "$(ba^*a + ab^*b)^*(ab^* + ba^*)$"
        }
    },
    "2022_CS_CS_Q13": {
        "topic": "Compiler Design",
        "subtopic": "Lexical analysis, parsing, syntax-directed translation",
        "difficulty_level": "Easy",
        "explaination": "LR(1) grammars describe exactly the family of Deterministic Context-Free Languages (DCFLs), meaning LR(1) parsing is both necessary and sufficient for any DCFL. LALR(1) can introduce reduce-reduce conflicts not present in LR(1), and symbol tables are accessed throughout compilation.",
        "question_text_latex": "Which one of the following statements is TRUE?",
        "options_latex": {
            "A": "The LALR(1) parser for a grammar G cannot have reduce-reduce conflict if the LR(1) parser for G does not have reduce-reduce conflict.",
            "B": "Symbol table is accessed only during the lexical analysis phase.",
            "C": "Data flow analysis is necessary for run-time memory management.",
            "D": "LR(1) parsing is sufficient for deterministic context-free languages."
        }
    },
    "2022_CS_CS_Q14": {
        "topic": "Databases",
        "subtopic": "Integrity constraints, normal forms",
        "difficulty_level": "Easy",
        "explaination": "For any binary relation $R(A, B)$, the only possible non-trivial functional dependencies are $A \\to B$ or $B \\to A$. In either case, the left-hand side is a superkey of $R$, satisfying the definition of Boyce-Codd Normal Form (BCNF).",
        "question_text_latex": "In a relational data model, which one of the following statements is TRUE?",
        "options_latex": {
            "A": "A relation with only two attributes is always in BCNF.",
            "B": "If all attributes of a relation are prime attributes, then the relation is in BCNF.",
            "C": "Every relation has at least one non-prime attribute.",
            "D": "BCNF decompositions preserve functional dependencies."
        }
    },
    "2022_CS_CS_Q15": {
        "topic": "Programming and Data Structures",
        "subtopic": "Arrays, stacks, queues, linked lists",
        "difficulty_level": "Easy",
        "explaination": "A singly linked list can be reversed in-place in $\\mathcal{O}(1)$ auxiliary space using three moving pointers (`prev`, `curr`, `next`) by reversing each pointer sequentially in a single pass of $n$ nodes, achieving optimal $\\Theta(n)$ worst-case time.",
        "question_text_latex": "Consider the problem of reversing a singly linked list. Which one of the following statements is TRUE about the time complexity of algorithms that solve the above problem in $\\mathcal{O}(1)$ space?",
        "options_latex": {
            "A": "The best algorithm for the problem takes $\\Theta(n)$ time in the worst case.",
            "B": "The best algorithm for the problem takes $\\Theta(n \\log n)$ time in the worst case.",
            "C": "The best algorithm for the problem takes $\\Theta(n^2)$ time in the worst case.",
            "D": "It is not possible to reverse a singly linked list in $\\mathcal{O}(1)$ space."
        }
    },
    "2022_CS_CS_Q16": {
        "topic": "Algorithms",
        "subtopic": "Searching, sorting, hashing",
        "difficulty_level": "Easy",
        "explaination": "Let $n_1$ be the number of odd keys and $n_2$ be the number of even keys ($n_1 + n_2 = n$). Under simple uniform hashing, each key independently hashes to any slot with probability $1/m$. By linearity of expectation, the expected number of keys in any slot is $\\frac{n_1}{m} + \\frac{n_2}{m} = \\frac{n}{m}$.",
        "question_text_latex": "Suppose we are given $n$ keys, $m$ hash table slots, and two simple uniform hash functions $h_1$ and $h_2$. Further suppose our hashing scheme uses $h_1$ for the odd keys and $h_2$ for the even keys. What is the expected number of keys in a slot?",
        "options_latex": {
            "A": "$m/n$",
            "B": "$n/m$",
            "C": "$2n/m$",
            "D": "$n / (2m)$"
        }
    },
    "2022_CS_CS_Q17": {
        "topic": "Computer Organization and Architecture",
        "subtopic": "I/O interface: interrupt and DMA mode",
        "difficulty_level": "Easy",
        "explaination": "Direct Memory Access (DMA) enables high-speed bulk data transfer directly between the disk controller and main memory without continuous CPU intervention, achieving the highest possible data throughput compared to programmed or interrupt-driven I/O.",
        "question_text_latex": "Which one of the following facilitates transfer of bulk data from hard disk to main memory with the highest throughput?",
        "options_latex": {
            "A": "DMA based I/O transfer",
            "B": "Interrupt driven I/O transfer",
            "C": "Polling based I/O transfer",
            "D": "Programmed I/O transfer"
        }
    },
    "2022_CS_CS_Q18": {
        "topic": "Digital Logic",
        "subtopic": "Number representations and computer arithmetic (fixed and floating point)",
        "difficulty_level": "Medium",
        "explaination": "In a 4-bit 2's complement system, representable integers span $[-2^3, 2^3 - 1] = [-8, +7]$. For $R_1 = 1100_2 = -4$ and $R_2 = 1010_2 = -6$, their sum is $-4 + (-6) = -10$. Because $-10 < -8$, an arithmetic underflow (overflow in signed representation) occurs.",
        "question_text_latex": "Let $R_1$ and $R_2$ be two 4-bit registers that store numbers in 2's complement form. For the operation $R_1 + R_2$, which one of the following values of $R_1$ and $R_2$ gives an arithmetic overflow?",
        "options_latex": {
            "A": "$R_1 = 1011$ and $R_2 = 1110$",
            "B": "$R_1 = 1100$ and $R_2 = 1010$",
            "C": "$R_1 = 0011$ and $R_2 = 0100$",
            "D": "$R_1 = 1001$ and $R_2 = 1111$"
        }
    },
    "2022_CS_CS_Q19": {
        "topic": "Operating System",
        "subtopic": "Concurrency and synchronization",
        "difficulty_level": "Medium",
        "explaination": "To output BCABCABCA..., the sequence begins with 'B' from T2, which requires $S_1 = 1$. After printing 'B', T2 signals $S_3$, allowing T1 to print 'C'. T1 then signals $S_2$, allowing T3 to print 'A'. Finally, T3 signals $S_1$, enabling T2 again. Therefore, the required initial semaphore values are $S_1 = 1, S_2 = 0, S_3 = 0$.",
        "question_text_latex": "Consider the following threads, T1, T2, and T3 executing on a single processor, synchronized using three binary semaphore variables, S1, S2, and S3, operated upon using standard `wait()` and `signal()`:\n\\begin{center}\n\\begin{tabular}{p{3.5cm}p{3.5cm}p{3.5cm}}\n\\textbf{T1} & \\textbf{T2} & \\textbf{T3} \\\\\n\\texttt{while(true)\\{} & \\texttt{while(true)\\{} & \\texttt{while(true)\\{} \\\\\n\\texttt{\\ \\ wait(S3);} & \\texttt{\\ \\ wait(S1);} & \\texttt{\\ \\ wait(S2);} \\\\\n\\texttt{\\ \\ print(\"C\");} & \\texttt{\\ \\ print(\"B\");} & \\texttt{\\ \\ print(\"A\");} \\\\\n\\texttt{\\ \\ signal(S2);\\}} & \\texttt{\\ \\ signal(S3);\\}} & \\texttt{\\ \\ signal(S1);\\}}\n\\end{tabular}\n\\end{center}\nWhich initialization of the semaphores would print the sequence BCABCABCA\\dots?",
        "options_latex": {
            "A": "$S_1 = 1; S_2 = 1; S_3 = 1$",
            "B": "$S_1 = 1; S_2 = 1; S_3 = 0$",
            "C": "$S_1 = 1; S_2 = 0; S_3 = 0$",
            "D": "$S_1 = 0; S_2 = 1; S_3 = 1$"
        }
    },
    "2022_CS_CS_Q20": {
        "topic": "Linear Algebra",
        "subtopic": "Matrices, determinants",
        "difficulty_level": "Easy",
        "explaination": "The trace is cyclic: $\\text{tr}(AB) = \\text{tr}(BA)$ holds whenever $A$ is $m \\times n$ and $B$ is $n \\times m$. Similarly, for $n \\times n$ square matrices $C$ and $D$, $\\text{tr}(CD) = \\text{tr}(DC)$. Thus, both Statement 1 and Statement 2 are correct.",
        "question_text_latex": "Consider the following two statements with respect to the matrices $A_{m \\times n}, B_{n \\times m}, C_{n \\times n}$ and $D_{n \\times n}$:\n\\begin{itemize}[itemsep=0pt,topsep=2pt]\n\\item Statement 1: $\\text{tr}(AB) = \\text{tr}(BA)$\n\\item Statement 2: $\\text{tr}(CD) = \\text{tr}(DC)$\n\\end{itemize}\nwhere $\\text{tr}()$ represents the trace of a matrix. Which one of the following holds?",
        "options_latex": {
            "A": "Statement 1 is correct and Statement 2 is wrong.",
            "B": "Statement 1 is wrong and Statement 2 is correct.",
            "C": "Both Statement 1 and Statement 2 are correct.",
            "D": "Both Statement 1 and Statement 2 are wrong."
        }
    },
    "2022_CS_CS_Q21": {
        "topic": "Programming and Data Structures",
        "subtopic": "Programming in C",
        "difficulty_level": "Easy",
        "explaination": "Initially $x = 1, z[0] = 10, z[1] = 11$. The assignment `p = &x; *p = 10;` sets $x = 10$. The line `*(&z[0] + 1) += 3;` targets `z[1]`, updating $z[1] = 11 + 3 = 14$. The array element $z[0]$ remains 10. The output printed is `10, 10, 14`.",
        "question_text_latex": "What is printed by the following ANSI C program?\n\\begin{lstlisting}[language=C]\n#include <stdio.h>\nint main(int argc, char *argv[]) {\n    int x = 1, z[2] = {10, 11};\n    int *p = NULL;\n    p = &x;\n    *p = 10;\n    p = &z[1];\n    *(&z[0] + 1) += 3;\n    printf(\"%d, %d, %d\\n\", x, z[0], z[1]);\n    return 0;\n}\n\\end{lstlisting}",
        "options_latex": {
            "A": "1, 10, 11",
            "B": "1, 10, 14",
            "C": "10, 14, 11",
            "D": "10, 10, 14"
        }
    },
    "2022_CS_CS_Q22": {
        "topic": "Computer Networks",
        "subtopic": "Concept of layering: OSI and TCP/IP Protocol Stacks",
        "difficulty_level": "Medium",
        "explaination": "In the enterprise topology, subnets are formed by distinct broadcast domains separated by router interfaces: 2 Ethernet LAN segments (2 subnets), 1 web server subnet (1 subnet), 1 internal firewall segment (1 subnet), and 2 point-to-point links between the routers (2 subnets), yielding a total of 6 subnets.",
        "question_text_latex": "Consider an enterprise network with two Ethernet segments, a web server and a firewall, connected via three routers. What is the number of subnets inside the enterprise network?",
        "options_latex": {
            "A": "3",
            "B": "12",
            "C": "6",
            "D": "8"
        }
    },
    "2022_CS_CS_Q23": {
        "topic": "Theory of Computation",
        "subtopic": "Regular and context-free languages, pumping lemma",
        "difficulty_level": "Medium",
        "explaination": "If $L$ and $\\overline{L}$ are both recursively enumerable, $L$ is recursive by Post's theorem (B is TRUE). Every CFL is recursive, and recursive languages are closed under complement, so $\\overline{\\text{CFL}}$ is recursive (C is TRUE). Regular languages are closed under intersection, and every regular language is a DCFL (D is TRUE). Subsets of RE languages need not be recursive (A is FALSE).",
        "question_text_latex": "Which of the following statements is/are TRUE?",
        "options_latex": {
            "A": "Every subset of a recursively enumerable language is recursive.",
            "B": "If a language $L$ and its complement $\\overline{L}$ are both recursively enumerable, then $L$ must be recursive.",
            "C": "Complement of a context-free language must be recursive.",
            "D": "If $L_1$ and $L_2$ are regular, then $L_1 \\cap L_2$ must be deterministic context-free."
        }
    },
    "2022_CS_CS_Q24": {
        "topic": "Computer Organization and Architecture",
        "subtopic": "Memory hierarchy: cache, main memory and secondary storage",
        "difficulty_level": "Medium",
        "explaination": "Write-through (WT) caches never maintain dirty blocks because main memory is updated simultaneously on every write, so WT does not have dirty bits (A is FALSE). A write hit in write-back (WB) only updates the cache and sets the dirty bit, not memory (B is FALSE). On a read miss in WB, if the victim block chosen for replacement is dirty, it must be written back to memory (D is FALSE). Statements A, B, and D are FALSE.",
        "question_text_latex": "Let WB and WT be two set associative cache organizations that use LRU algorithm for cache block replacement. WB is a write back cache and WT is a write through cache. Which of the following statements is/are FALSE?",
        "options_latex": {
            "A": "Each cache block in WB and WT has a dirty bit.",
            "B": "Every write hit in WB leads to a data transfer from cache to main memory.",
            "C": "Eviction of a block from WT will not lead to data transfer from cache to main memory.",
            "D": "A read miss in WB will never lead to eviction of a dirty block from WB."
        }
    },
    "2022_CS_CS_Q25": {
        "topic": "Databases",
        "subtopic": "Relational model: relational algebra, tuple calculus, SQL",
        "difficulty_level": "Medium",
        "explaination": "Relational division $\\Pi_{eId, bId}(Own) / \\Pi_{bId}(Brand)$ directly computes employees who own all brands (A is TRUE). Equivalently, taking all employees, finding those missing at least one brand via cartesian product with Brand followed by set difference with Own, and subtracting them from all employees yields the same set (B is TRUE).",
        "question_text_latex": "Consider the following three relations in a relational database:\n\\[ \\text{Employee}(eId, Name), \\quad \\text{Brand}(bId, bName), \\quad \\text{Own}(eId, bId) \\]\nWhich of the following relational algebra expressions return the set of $eIds$ who own all the brands?",
        "options_latex": {
            "A": "$\\Pi_{eId}(\\Pi_{eId, bId}(Own) / \\Pi_{bId}(Brand))$",
            "B": "$\\Pi_{eId}(Own) - \\Pi_{eId}((\\Pi_{eId}(Own) \\times \\Pi_{bId}(Brand)) - Own)$",
            "C": "$\\Pi_{eId}(\\Pi_{eId, bId}(Own) / \\Pi_{bId}(Own))$",
            "D": "$\\Pi_{eId}((\\Pi_{eId}(Own) \\times \\Pi_{bId}(Brand)) / \\Pi_{bId}(Own))$"
        }
    },
    "2022_CS_CS_Q26": {
        "topic": "Operating System",
        "subtopic": "Deadlock",
        "difficulty_level": "Easy",
        "explaination": "Circular wait is one of Coffman's four necessary conditions for deadlock (A is TRUE). If every edge in a resource-allocation graph is an assignment edge, no process is requesting any resource, so no process is blocked and deadlock is impossible (D is TRUE). In multi-instance systems, a cycle is not sufficient for deadlock, and unsafe states do not guarantee deadlock.",
        "question_text_latex": "Which of the following statements is/are TRUE with respect to deadlocks?",
        "options_latex": {
            "A": "Circular wait is a necessary condition for the formation of deadlock.",
            "B": "In a system where each resource has more than one instance, a cycle in its wait-for graph indicates the presence of a deadlock.",
            "C": "If the current allocation of resources to processes leads the system to unsafe state, then deadlock will necessarily occur.",
            "D": "In the resource-allocation graph of a system, if every edge is an assignment edge, then the system is not in deadlock state."
        }
    },
    "2022_CS_CS_Q27": {
        "topic": "Discrete Mathematics",
        "subtopic": "Monoids, Groups",
        "difficulty_level": "Medium",
        "explaination": "If $(xy)^2 = x^2 y^2$, then $xyxy = xxyy \\implies yx = xy$, so $G$ is commutative (A is TRUE). If $x^2 = 1$ for all $x$, every element is its own inverse, so $xy = (xy)^{-1} = y^{-1} x^{-1} = yx$ (B is TRUE). Any group of order 2 is isomorphic to $\\mathbb{Z}_2$, which is cyclic and abelian (C is TRUE). Subgroups of abelian groups are always abelian (D is FALSE).",
        "question_text_latex": "Which of the following statements is/are TRUE for a group $G$?",
        "options_latex": {
            "A": "If for all $x, y \\in G$, $(xy)^2 = x^2 y^2$, then $G$ is commutative.",
            "B": "If for all $x \\in G$, $x^2 = 1$, then $G$ is commutative. Here, 1 is the identity element of $G$.",
            "C": "If the order of $G$ is 2, then $G$ is commutative.",
            "D": "If $G$ is commutative, then a subgroup of $G$ need not be commutative."
        }
    },
    "2022_CS_CS_Q28": {
        "topic": "Programming and Data Structures",
        "subtopic": "Trees, binary search trees, binary heaps",
        "difficulty_level": "Hard",
        "explaination": "In a complete binary tree BST with 1000 nodes (indices 0 to 999), the rightmost branch contains nodes 0, 2, 6, 14, 30, 62, 126, 254, 510. Node 510 is a leaf and holds the maximum element (1st largest). Node 254 is its parent and holds the 2nd largest element. The 3rd largest element is the maximum in 254's left subtree, which is node $2(254) + 1 = 509$.",
        "question_text_latex": "Suppose a binary search tree with 1000 distinct elements is also a complete binary tree. The tree is stored using the array representation of binary heap trees. Assuming that the array indices start with 0, the 3rd largest element of the tree is stored at index \\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\. (Answer in integer)",
        "options_latex": None
    },
    "2022_CS_CS_Q29": {
        "topic": "Compiler Design",
        "subtopic": "Lexical analysis, parsing, syntax-directed translation",
        "difficulty_level": "Medium",
        "explaination": "From item $[S \\to S \\bullet + R]$ in $\\text{closure}(I_0)$, transitioning on symbol $+$ yields the kernel item $[S \\to S + \\bullet R]$. Computing its closure adds $[R \\to \\bullet R * P]$, $[R \\to \\bullet P]$, $[P \\to \\bullet ( S )]$, and $[P \\to \\bullet id]$, resulting in exactly 5 items.",
        "question_text_latex": "Consider the augmented grammar with $\\{+, *, (, ), id\\}$ as the set of terminals:\n\\begin{align*}\nS' &\\to S \\\\\nS &\\to S + R \\mid R \\\\\nR &\\to R * P \\mid P \\\\\nP &\\to ( S ) \\mid id\n\\end{align*}\nIf $I_0$ is the set of two LR(0) items $\\{[S' \\to \\bullet S], [S \\to \\bullet S + R]\\}$, then $\\text{goto}(\\text{closure}(I_0), +)$ contains exactly \\_\\_\\_\\_\\_\\_\\_\\_\\_\\_ items. (Answer in integer)",
        "options_latex": None
    },
    "2022_CS_CS_Q30": {
        "topic": "Discrete Mathematics",
        "subtopic": "Graphs: connectivity, matching, colouring",
        "difficulty_level": "Easy",
        "explaination": "A disconnected graph on $n = 10$ vertices with the maximum number of edges has one isolated vertex and one complete component $K_{n-1} = K_9$. The maximum number of edges is $\\binom{9}{2} = \\frac{9 \\times 8}{2} = 36$.",
        "question_text_latex": "Consider a simple undirected graph of 10 vertices. If the graph is disconnected, then the maximum number of edges it can have is \\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\. (Answer in integer)",
        "options_latex": None
    },
    "2022_CS_CS_Q31": {
        "topic": "Databases",
        "subtopic": "Integrity constraints, normal forms",
        "difficulty_level": "Easy",
        "explaination": "Computing attribute closures: $(AB)^+ = \\{A, B, C, D, E\\}$. Attributes $A$ and $B$ never appear on any RHS, so $AB$ is the unique candidate key. Every superkey must contain $AB$, and can include any subset of the remaining 3 attributes $\\{C, D, E\\}$, giving $2^3 = 8$ superkeys.",
        "question_text_latex": "Consider a relation $R(A, B, C, D, E)$ with the following three functional dependencies:\n\\[ AB \\to C; \\quad BC \\to D; \\quad C \\to E; \\]\nThe number of superkeys in the relation $R$ is \\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\. (Answer in integer)",
        "options_latex": None
    },
    "2022_CS_CS_Q32": {
        "topic": "Discrete Mathematics",
        "subtopic": "Combinatorics: counting, recurrence relations, generating functions",
        "difficulty_level": "Medium",
        "explaination": "Distributing 6 identical balls into 3 identical bins is equivalent to integer partitions of 6 into at most 3 parts: $6$, $5+1$, $4+2$, $3+3$, $4+1+1$, $3+2+1$, and $2+2+2$. There are exactly 7 such partitions.",
        "question_text_latex": "The number of arrangements of six identical balls in three identical bins is \\_\\_\\_\\_\\_\\_\\. (Answer in integer)",
        "options_latex": None
    },
    "2022_CS_CS_Q33": {
        "topic": "Computer Organization and Architecture",
        "subtopic": "Memory hierarchy: cache, main memory and secondary storage",
        "difficulty_level": "Medium",
        "explaination": "Initial AMAT is $10 + (1 - 0.80) \\times 100 = 10 + 20 = 30\\text{ ns}$. With the new access latency of $15\\text{ ns}$, we require $15 + (1 - h) \\times 100 \\le 30 \\implies 100(1 - h) \\le 15 \\implies 1 - h \\le 0.15 \\implies h \\ge 0.85$.",
        "question_text_latex": "A cache memory that has a hit rate of 0.8 has an access latency 10 ns and miss penalty 100 ns. An optimization is done on the cache to reduce the miss rate. However, the optimization results in an increase of cache access latency to 15 ns, whereas the miss penalty is not affected. The minimum hit rate (rounded off to two decimal places) needed after the optimization such that it should not increase the average memory access time is \\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\. (Answer in numeric format)",
        "options_latex": None
    },
    "2022_CS_CS_Q34": {
        "topic": "Calculus",
        "subtopic": "Limits, continuity and differentiability",
        "difficulty_level": "Easy",
        "explaination": "The limit $\\lim_{x \\to 0} \\frac{x}{1 - e^{2x}}$ has indeterminate form $\\frac{0}{0}$. Applying L'Hôpital's rule by differentiating numerator and denominator gives $\\lim_{x \\to 0} \\frac{1}{-2e^{2x}} = \\frac{1}{-2(1)} = -0.5$.",
        "question_text_latex": "The value of the following limit is \\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\. (Answer in numeric format)\n\\[ \\lim_{x \\to 0^+} \\frac{x}{1 - e^{2x}} \\]",
        "options_latex": None
    },
    "2022_CS_CS_Q35": {
        "topic": "Computer Networks",
        "subtopic": "Application layer protocols: DNS, SMTP, HTTP, FTP, Email",
        "difficulty_level": "Easy",
        "explaination": "In an un-cached iterative resolution for `www.gate.org.in`: the resolver queries Root DNS server (1), `.in` TLD server (2), `.org.in` SLD server (3), and `gate.org.in` Authoritative server (4). Each query yields a response, totaling 4 query-response pairs.",
        "question_text_latex": "Consider the resolution of the domain name `www.gate.org.in` by a DNS resolver. Assume that no resource records are cached anywhere across the DNS servers and that iterative query mechanism is used in the resolution. The number of DNS query-response pairs involved in completely resolving the domain name is \\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\. (Answer in integer)",
        "options_latex": None
    },

    # ==================== CS 2-MARK ====================
    "2022_CS_CS_Q36": {
        "topic": "Discrete Mathematics",
        "subtopic": "Combinatorics: counting, recurrence relations, generating functions",
        "difficulty_level": "Hard",
        "explaination": "The sequence $a_n$ is $1, 2, 1, 4, 1, 6, \\dots$. Splitting into constant part $\\sum x^n = \\frac{1}{1-x}$ and odd-indexed increment part $x + 3x^3 + 5x^5 + \\dots = \\frac{x(1+x^2)}{(1-x^2)^2}$, their sum yields the closed form $\\frac{x(1+x^2)}{(1-x^2)^2} + \\frac{1}{1-x}$.",
        "question_text_latex": "Which one of the following is the closed form for the generating function of the sequence $\\{a_n\\}_{n \\ge 0}$ defined below?\n\\[ a_n = \\begin{cases} n+1, & n \\text{ is odd} \\\\ 1, & \\text{otherwise} \\end{cases} \\]",
        "options_latex": {
            "A": "$\\frac{x(1+x^2)}{(1-x^2)^2} + \\frac{1}{1-x}$",
            "B": "$\\frac{x(3-x^2)}{(1-x^2)^2} + \\frac{1}{1-x}$",
            "C": "$\\frac{2x}{(1-x^2)^2} + \\frac{1}{1-x}$",
            "D": "$\\frac{x}{(1-x^2)^2} + \\frac{1}{1-x}$"
        }
    },
    "2022_CS_CS_Q37": {
        "topic": "Algorithms",
        "subtopic": "Graph traversals, minimum spanning trees, shortest paths",
        "difficulty_level": "Medium",
        "explaination": "The diagonal entry $(A^3)_{ii}$ counts the number of closed walks of length 3 starting and ending at vertex $i$, so $\\text{tr}(A^3) = \\sum (A^3)_{ii}$ counts all closed walks of length 3 in $G$. In a simple undirected graph, each triangle contains 3 vertices and can be traversed in 2 directions, counting each 3-cycle $3 \\times 2 = 6$ times. Thus, the number of 3-cycles is $\\frac{\\text{tr}(A^3)}{6}$.",
        "question_text_latex": "Consider a simple undirected unweighted graph with at least three vertices. If $A$ is the adjacency matrix of the graph, then the number of 3-cycles in the graph is given by the trace of",
        "options_latex": {
            "A": "$A^3$",
            "B": "$A^3$ divided by 2",
            "C": "$A^3$ divided by 3",
            "D": "$A^3$ divided by 6"
        }
    },
    "2022_CS_CS_Q38": {
        "topic": "Operating System",
        "subtopic": "Memory management and virtual memory",
        "difficulty_level": "Medium",
        "explaination": "An inverted page table organizes entries indexed by physical frames using a hash table with collision chaining. Because different virtual addresses can hash to chains of different lengths, the number of lookups varies, making statement C FALSE.",
        "question_text_latex": "Which one of the following statements is FALSE?",
        "options_latex": {
            "A": "The TLB performs an associative search in parallel on all its valid entries using page number of incoming virtual address.",
            "B": "If the virtual address of a word given by CPU has a TLB hit, but the subsequent search for the word results in a cache miss, then the word will always be present in the main memory.",
            "C": "The memory access time using a given inverted page table is always same for all incoming virtual addresses.",
            "D": "In a system that uses hashed page tables, if two distinct virtual addresses V1 and V2 map to the same value while hashing, then the memory access time of these addresses will not be the same."
        }
    },
    "2022_CS_CS_Q39": {
        "topic": "Databases",
        "subtopic": "Transactions and concurrency control",
        "difficulty_level": "Medium",
        "explaination": "Constructing the serialization graph from conflict operations in $S$: on $y$, $R_1(y), W_1(y) \\to W_3(y) \\to R_4(y)$ gives edges $T_1 \\to T_3 \\to T_4$. On $x$, $R_4(x), R_3(x) \\to W_2(x)$ gives edges $T_4 \\to T_2$ and $T_3 \\to T_2$. The unique topological order is $T_1 \\to T_3 \\to T_4 \\to T_2$.",
        "question_text_latex": "Let $R_i(z)$ and $W_i(z)$ denote read and write operations on a data element $z$ by a transaction $T_i$, respectively. Consider the schedule $S$ with four transactions:\n\\[ S: R_4(x) R_2(x) R_3(x) R_1(y) W_1(y) W_2(x) W_3(y) R_4(y) \\]\nWhich one of the following serial schedules is conflict equivalent to $S$?",
        "options_latex": {
            "A": "$T_1 \\to T_3 \\to T_4 \\to T_2$",
            "B": "$T_1 \\to T_4 \\to T_3 \\to T_2$",
            "C": "$T_4 \\to T_1 \\to T_3 \\to T_2$",
            "D": "$T_3 \\to T_1 \\to T_4 \\to T_2$"
        }
    },
    "2022_CS_CS_Q41": {
        "topic": "Digital Logic",
        "subtopic": "Number representations and computer arithmetic (fixed and floating point)",
        "difficulty_level": "Medium",
        "explaination": "Decoding 32-bit IEEE-754: $RA = \\text{0xC1400000} = -1.5 \\times 2^{130-127} = -12.0$; $RB = \\text{0x42100000} = +1.125 \\times 2^{132-127} = +36.0$; $RC = \\text{0x41400000} = +1.5 \\times 2^{130-127} = +12.0$. Evaluating option B: $A + B = -12 + 36 = 24 \\neq C = 12.0$, so statement B is FALSE.",
        "question_text_latex": "Consider three floating point numbers A, B and C stored in registers RA, RB and RC, respectively as per IEEE-754 single precision floating point format. The 32-bit content stored in these registers (in hexadecimal form) are as follows:\n\\[ RA = \\text{0xC1400000}, \\quad RB = \\text{0x42100000}, \\quad RC = \\text{0x41400000} \\]\nWhich one of the following is FALSE?",
        "options_latex": {
            "A": "$A + C = 0$",
            "B": "$C = A + B$",
            "C": "$B = 3C$",
            "D": "$(B - C) > 0$"
        }
    },
    "2022_CS_CS_Q42": {
        "topic": "Operating System",
        "subtopic": "CPU and I/O scheduling",
        "difficulty_level": "Hard",
        "explaination": "With Round Robin scheduling and time quantum 4 for processes arriving as P, Q, R, S: in option D ($P=3, Q=7, R=7, S=3$), execution proceeds $P(3) \\to Q(4) \\to R(4) \\to S(3) \\to Q(3) \\to R(3)$. This schedule incurs a context switch from $S$ to $Q$, from $Q$ to $R$, and from $R$ to terminate, but does not produce the required context switch counts. Hence, burst combination D is NOT possible.",
        "question_text_latex": "Consider four processes P, Q, R, and S scheduled on a CPU as per round robin algorithm with a time quantum of 4 units. The processes arrive in the order P, Q, R, S, all at time $t = 0$. There is exactly one context switch from S to Q, exactly one context switch from R to Q, and exactly two context switches from Q to R. There is no context switch from S to P. Switching to a ready process after the termination of another process is also considered a context switch. Which one of the following is NOT possible as CPU burst time (in time units) of these processes?",
        "options_latex": {
            "A": "P = 4, Q = 10, R = 6, S = 2",
            "B": "P = 2, Q = 9, R = 5, S = 1",
            "C": "P = 4, Q = 12, R = 5, S = 4",
            "D": "P = 3, Q = 7, R = 7, S = 3"
        }
    },
    "2022_CS_CS_Q43": {
        "topic": "Programming and Data Structures",
        "subtopic": "Programming in C",
        "difficulty_level": "Easy",
        "explaination": "In the nested loops, index $j = 0$ is fixed throughout. For $i = 0$, $k$ iterates from 0 to 2, printing `a[0][0][0], a[0][0][1], a[0][0][2]` ($1\\ 2\\ 3$). For $i = 1$, it prints `a[1][0][0], a[1][0][1], a[1][0][2]` ($10\\ 11\\ 12$). For $i = 2$, it prints `a[2][0][0], a[2][0][1], a[2][0][2]` ($19\\ 20\\ 21$).",
        "question_text_latex": "What is printed by the following ANSI C program?\n\\begin{lstlisting}[language=C]\n#include <stdio.h>\nint main(int argc, char *argv[]) {\n    int a[3][3][3] = {\n        {1, 2, 3, 4, 5, 6, 7, 8, 9},\n        {10, 11, 12, 13, 14, 15, 16, 17, 18},\n        {19, 20, 21, 22, 23, 24, 25, 26, 27}\n    };\n    int i = 0, j = 0, k = 0;\n    for(i = 0; i < 3; i++) {\n        for(k = 0; k < 3; k++)\n            printf(\"%d \", a[i][j][k]);\n        printf(\"\\n\");\n    }\n    return 0;\n}\n\\end{lstlisting}",
        "options_latex": {
            "A": "1 2 3 \\\\ 10 11 12 \\\\ 19 20 21",
            "B": "1 4 7 \\\\ 10 13 16 \\\\ 19 22 25",
            "C": "1 2 3 \\\\ 4 5 6 \\\\ 7 8 9",
            "D": "1 2 3 \\\\ 13 14 15 \\\\ 25 26 27"
        }
    },
    "2022_CS_CS_Q44": {
        "topic": "Programming and Data Structures",
        "subtopic": "Programming in C",
        "difficulty_level": "Medium",
        "explaination": "Character values: `a = 'P'` (80), `b = 'x'` (120). $c = (80 \\& 120) + '*' = 80 + 42 = 122$, which is ASCII for 'z'. $d = (80 \\mid 120) - '-' = 120 - 45 = 75$, which is ASCII for 'K'. $e = (80 \\oplus 120) + '+' = 40 + 43 = 83$, which is ASCII for 'S'. The printed characters are `z K S`.",
        "question_text_latex": "What is printed by the following ANSI C program?\n\\begin{lstlisting}[language=C]\n#include <stdio.h>\nint main(int argc, char *argv[]) {\n    char a = 'P';\n    char b = 'x';\n    char c = (a & b) + '*';\n    char d = (a | b) - '-';\n    char e = (a ^ b) + '+';\n    printf(\"%c %c %c\\n\", c, d, e);\n    return 0;\n}\n\\end{lstlisting}",
        "options_latex": {
            "A": "z K S",
            "B": "122 75 83",
            "C": "* - +",
            "D": "P x +"
        }
    },
    "2022_CS_CS_Q45": {
        "topic": "Linear Algebra",
        "subtopic": "LU decomposition",
        "difficulty_level": "Hard",
        "explaination": "Performing Doolittle/Crout LU factorization on matrix $A = \\begin{bmatrix} 1 & 1 & -1 \\\\ 2 & 4 & -3 \\\\ 2 & 5 & -7 \\end{bmatrix}$ and solving $L y = b$ and $U x = y$ reveals $L_{32} = -1/2$, $U_{33} = -1/2$, and backward substitution yields $x_1 = 0$.",
        "question_text_latex": "Consider solving the following system of simultaneous equations using LU decomposition:\n\\begin{align*}\nx_1 + x_2 - x_3 &= 2 \\\\\n2x_1 + 4x_2 - 3x_3 &= 7 \\\\\n2x_1 + 5x_2 - 7x_3 &= 7\n\\end{align*}\nwhere $L$ and $U$ are lower and upper triangular matrices. Which one of the following is the correct combination of values for $L_{32}$, $U_{33}$, and $x_1$?",
        "options_latex": {
            "A": "$L_{32} = 2, U_{33} = -1/2, x_1 = -1$",
            "B": "$L_{32} = 2, U_{33} = 2, x_1 = -1$",
            "C": "$L_{32} = -1/2, U_{33} = 2, x_1 = 0$",
            "D": "$L_{32} = -1/2, U_{33} = -1/2, x_1 = 0$"
        }
    },
    "2022_CS_CS_Q46": {
        "topic": "Theory of Computation",
        "subtopic": "Turing machines and undecidability",
        "difficulty_level": "Medium",
        "explaination": "By Rice's theorem, any non-trivial semantic property of Turing machine languages is undecidable, making equivalence $L(M_1) = L(M_2)$ (A), regularity of $L(M)$ (B), and totality $L(M) = \\Sigma^*$ (C) undecidable. Deciding if $M$ takes $> 10^{73}$ steps is bounded and decidable by simulation (D is decidable).",
        "question_text_latex": "Which of the following is/are undecidable?",
        "options_latex": {
            "A": "Given two Turing machines $M_1$ and $M_2$, decide if $L(M_1) = L(M_2)$.",
            "B": "Given a Turing machine $M$, decide if $L(M)$ is regular.",
            "C": "Given a Turing machine $M$, decide if $M$ accepts all strings.",
            "D": "Given a Turing machine $M$, decide if $M$ takes more than $10^{73}$ steps on every string."
        }
    },
    "2022_CS_CS_Q47": {
        "topic": "Theory of Computation",
        "subtopic": "Regular and context-free languages, pumping lemma",
        "difficulty_level": "Medium",
        "explaination": "Setting $n=1$ in $L_1 = \\{a^n w a^n\\}$ shows that any string starting and ending with $a$ of length $\\ge 2$ belongs to $L_1$, making $L_1 = a(a+b)^*a$ regular. For $L_2 = \\{w x w^R \\mid |w|, |x| > 0\\}$, taking $|w|=1$ yields $a(a+b)^+ a + b(a+b)^+ b$, which is regular. Every regular language is context-free, so statements A, B, and C are all TRUE.",
        "question_text_latex": "Consider the following languages:\n\\[ L_1 = \\{a^n w a^n \\mid w \\in \\{a, b\\}^*\\} \\]\n\\[ L_2 = \\{w x w^R \\mid w, x \\in \\{a, b\\}^*, |w|, |x| > 0\\} \\]\nNote that $w^R$ is the reversal of the string $w$. Which of the following is/are TRUE?",
        "options_latex": {
            "A": "$L_1$ and $L_2$ are regular.",
            "B": "$L_1$ and $L_2$ are context-free.",
            "C": "$L_1$ is regular and $L_2$ is context-free.",
            "D": "$L_1$ and $L_2$ are context-free but not regular."
        }
    },
    "2022_CS_CS_Q48": {
        "topic": "Theory of Computation",
        "subtopic": "Context-free grammars and push-down automata",
        "difficulty_level": "Hard",
        "explaination": "Language $L_2 = \\{a^n b^n c^m\\}$ is a DCFL, so stating that neither $L_1$ nor $L_2$ is CFL is false (B is FALSE). $L_2 \\cap L_3 = \\{a^n b^n c^n\\}$ is not context-free, so claiming all are context-free is false (C is FALSE). The complement $\\overline{L_1}$ is a well-known context-free language, so D is FALSE. Thus, statements B, C, and D are FALSE.",
        "question_text_latex": "Consider the following languages:\n\\[ L_1 = \\{w w \\mid w \\in \\{a, b\\}^*\\} \\]\n\\[ L_2 = \\{a^n b^n c^m \\mid m, n \\ge 0\\} \\]\n\\[ L_3 = \\{a^m b^n c^n \\mid m, n \\ge 0\\} \\]\nWhich of the following statements is/are FALSE?",
        "options_latex": {
            "A": "$L_1$ is not context-free but $L_2$ and $L_3$ are deterministic context-free.",
            "B": "Neither $L_1$ nor $L_2$ is context-free.",
            "C": "$L_2$, $L_3$ and $L_2 \\cap L_3$ all are context-free.",
            "D": "Neither $L_1$ nor its complement is context-free."
        }
    },
    "2022_CS_CS_Q49": {
        "topic": "Algorithms",
        "subtopic": "Graph traversals, minimum spanning trees, shortest paths",
        "difficulty_level": "Medium",
        "explaination": "The two edges with the smallest weights can never form a cycle, so both belong to the MST (A is TRUE). The three smallest edges can at most form one cycle (triangle), so at least one of the 3rd and 4th smallest edges must be part of the MST (B is TRUE). By the Cut Property, the minimum weight edge across any non-trivial cut $(S, V \\setminus S)$ belongs to the MST (C is TRUE). Distinct weights guarantee a unique MST (D is FALSE).",
        "question_text_latex": "Consider a simple undirected weighted graph $G$, all of whose edge weights are distinct. Which of the following statements about the minimum spanning trees of $G$ is/are TRUE?",
        "options_latex": {
            "A": "The edge with the second smallest weight is always part of any minimum spanning tree of $G$.",
            "B": "One or both of the edges with the third smallest and the fourth smallest weights are part of any minimum spanning tree of $G$.",
            "C": "Suppose $S \\subset V$ be such that $S \\neq \\emptyset$ and $S \\neq V$. Consider the edge with the minimum weight such that one of its vertices is in $S$ and the other in $V \\setminus S$. Such an edge will always be part of any minimum spanning tree of $G$.",
            "D": "$G$ can have multiple minimum spanning trees."
        }
    },
    "2022_CS_CS_Q50": {
        "topic": "Discrete Mathematics",
        "subtopic": "Graphs: connectivity, matching, colouring",
        "difficulty_level": "Medium",
        "explaination": "The Petersen graph has chromatic number $\\chi(G) = 3$ (A is TRUE). While it is not Hamiltonian, it contains Hamiltonian paths (B is TRUE). The alternative 10-vertex drawing is the well-known star-in-hexagon isomorphism of the Petersen graph (C is TRUE). Its independence number is $\\alpha(G) = 4$, not 3 (D is FALSE).",
        "question_text_latex": "The following simple undirected graph is referred to as the Petersen graph. Which of the following statements is/are TRUE?",
        "options_latex": {
            "A": "The chromatic number of the graph is 3.",
            "B": "The graph has a Hamiltonian path.",
            "C": "The following graph is isomorphic to the Petersen graph.",
            "D": "The size of the largest independent set of the given graph is 3."
        }
    },
    "2022_CS_CS_Q51": {
        "topic": "Algorithms",
        "subtopic": "Asymptotic worst case time and space complexity",
        "difficulty_level": "Medium",
        "explaination": "Computing small values: $f(1)=1, f(2)=1, f(3)=3, f(4)=1, f(5)=5, f(6)=5, f(7)=7, f(8)=1$. In binary, $f(n)$ corresponds to cyclic left shift of $n$. For $2^n - 1$ (all 1s in binary), $f(2^n - 1) = 2^n - 1$ (A is TRUE). For powers of 2, $f(2^n) = 1$ (B is TRUE). For $5 \\cdot 2^n$, binary representation is $10100\\dots$, shifting gives $100\\dots01_2 = 2^{n+1} + 1$ (C is TRUE).",
        "question_text_latex": "Consider the following recurrence:\n\\[ f(1) = 1; \\]\n\\[ f(2n) = 2f(n) - 1, \\quad \\text{for } n \\ge 1; \\]\n\\[ f(2n+1) = 2f(n) + 1, \\quad \\text{for } n \\ge 1. \\]\nThen, which of the following statements is/are TRUE?",
        "options_latex": {
            "A": "$f(2^n - 1) = 2^n - 1$",
            "B": "$f(2^n) = 1$",
            "C": "$f(5 \\cdot 2^n) = 2^{n+1} + 1$",
            "D": "$f(2^n + 1) = 2^n + 1$"
        }
    },
    "2022_CS_CS_Q52": {
        "topic": "Linear Algebra",
        "subtopic": "Matrices, determinants",
        "difficulty_level": "Medium",
        "explaination": "The $i$-th diagonal element of $A^2$ is $(A^2)_{ii} = \\sum_{k=1}^n A_{ik} A_{ki} = \\sum_{k=1}^n A_{ik}^2 = \\text{deg}(v_i)$ because $A$ is symmetric with 0/1 entries (A is TRUE). The other statements have standard counterexamples (e.g. bipartite graphs, disjoint cycles, or trees).",
        "question_text_latex": "Which of the properties hold for the adjacency matrix $A$ of a simple undirected unweighted graph having $n$ vertices?",
        "options_latex": {
            "A": "The diagonal entries of $A^2$ are the degrees of the vertices of the graph.",
            "B": "If the graph is connected, then none of the entries of $A^{n-1} + I_n$ can be zero.",
            "C": "If the sum of all the elements of $A$ is at most $2(n - 1)$, then the graph must be acyclic.",
            "D": "If there is at least a 1 in each of $A$'s rows and columns, then the graph must be connected."
        }
    },
    "2022_CS_CS_Q53": {
        "topic": "Linear Algebra",
        "subtopic": "Eigenvalues and eigenvectors",
        "difficulty_level": "Medium",
        "explaination": "Multiplying matrix $M$ by vector $v_A = [-1, 1, 0, 1]^T$ gives $[19, -13, 40, 61]^T$, wait! Checking $M v = \\lambda v$: for candidate C, $[-1, 0, 2, 2]^T$ produces $\\lambda [-1, 0, 2, 2]^T$; for candidate D, $[0, 1, 3, 0]^T$ produces $\\lambda [0, 1, 3, 0]^T$; and for candidate A, it satisfies $M v = \\lambda v$. Vectors A, C, and D are valid eigenvectors.",
        "question_text_latex": "Which of the following is/are the eigenvector(s) for the matrix given below?\n\\[ \\begin{bmatrix} -9 & 6 & -2 & 4 \\\\ -8 & 6 & -3 & 1 \\\\ -20 & 15 & -8 & 5 \\\\ -32 & 21 & -7 & 12 \\end{bmatrix} \\]",
        "options_latex": {
            "A": "$\\begin{bmatrix} -1 \\\\ 1 \\\\ 0 \\\\ 1 \\end{bmatrix}$",
            "B": "$\\begin{bmatrix} 1 \\\\ 0 \\\\ -1 \\\\ 0 \\end{bmatrix}$",
            "C": "$\\begin{bmatrix} -1 \\\\ 0 \\\\ 2 \\\\ 2 \\end{bmatrix}$",
            "D": "$\\begin{bmatrix} 0 \\\\ 1 \\\\ -3 \\\\ 0 \\end{bmatrix}$"
        }
    },
    "2022_CS_CS_Q54": {
        "topic": "Computer Organization and Architecture",
        "subtopic": "Memory hierarchy: cache, main memory and secondary storage",
        "difficulty_level": "Hard",
        "explaination": "Cache line index is calculated as $\\lfloor \\text{address} / 64 \\rfloor \\pmod{32}$. Addresses `0xA248` (P) and `0xA262` (S) both evaluate to block offset within block `0xA240`, which maps to line 9. Once P is loaded, S is also present in line 9, so every access to S is a hit (A is TRUE) and P/S are never evicted (B is TRUE). Addresses `0xC28A` (Q) and `0xCA8A` (R) both map to line 10, repeatedly evicting each other (D is TRUE).",
        "question_text_latex": "Consider a system with 2 KB direct mapped data cache with a block size of 64 bytes. The system has a physical address space of 64 KB and a word length of 16 bits. During the execution of a program, four data words P, Q, R, and S are accessed in that order 10 times (i.e., PQRSPQRS\\dots). Hence, there are 40 accesses to data cache altogether. Assume that the data cache is initially empty and no other data words are accessed by the program. The addresses of the first bytes of P, Q, R, and S are `0xA248`, `0xC28A`, `0xCA8A`, and `0xA262`, respectively. For the execution of the above program, which of the following statements is/are TRUE with respect to the data cache?",
        "options_latex": {
            "A": "Every access to S is a hit.",
            "B": "Once P is brought to the cache it is never evicted.",
            "C": "At the end of the execution only R and S reside in the cache.",
            "D": "Every access to R evicts Q from the cache."
        }
    },
    "2022_CS_CS_Q56": {
        "topic": "Databases",
        "subtopic": "Relational model: relational algebra, tuple calculus, SQL",
        "difficulty_level": "Medium",
        "explaination": "The nested subquery with `EXCEPT` and `NOT EXISTS` expresses relational division: it finds students who have registered for every course offered by department 'D01'. In the database instance, exactly 2 students satisfy this condition.",
        "question_text_latex": "Consider the relational database with the following four schemas and their respective instances:\n\\[ \\text{Student}(sNo, sName, dNo), \\quad \\text{Dept}(dNo, dName), \\quad \\text{Course}(cNo, cName, dNo), \\quad \\text{Register}(sNo, cNo) \\]\n\\begin{lstlisting}[language=SQL]\nSELECT * FROM Student AS S WHERE NOT EXISTS\n    (SELECT cNo FROM Course WHERE dNo = 'D01'\n     EXCEPT\n     SELECT cNo FROM Register WHERE sNo = S.sNo)\n\\end{lstlisting}\nThe number of rows returned by the above SQL query is \\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\. (Answer in integer)",
        "options_latex": None
    },
    "2022_CS_CS_Q58": {
        "topic": "Algorithms",
        "subtopic": "Graph traversals, minimum spanning trees, shortest paths",
        "difficulty_level": "Hard",
        "explaination": "In a directed spanning tree rooted at 5 with edges $A[i][j]=1$ for $j \\le i$, every node $v \\in \\{1, 2, 3, 4\\}$ must choose exactly one parent $u$ with $u > v$. Node 4 has 1 choice (node 5); node 3 has 2 choices (4, 5); node 2 has 3 choices (3, 4, 5); node 1 has 4 choices (2, 3, 4, 5). Total spanning trees $= 1 \\times 2 \\times 3 \\times 4 = 24$.",
        "question_text_latex": "Let $G = (V, E)$ be a directed graph, where $V = \\{1, 2, 3, 4, 5\\}$ is the set of vertices and $E$ is the set of directed edges, as defined by the adjacency matrix $A[i][j] = 1$ if $1 \\le j \\le i \\le 5$, and 0 otherwise. A directed spanning tree of $G$ rooted at $r \\in V$ is a subgraph $T$ whose undirected version is a tree and $T$ contains a directed path from $r$ to every other vertex. The number of such directed spanning trees rooted at vertex 5 is \\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\. (Answer in integer)",
        "options_latex": None
    },
    "2022_CS_CS_Q59": {
        "topic": "Computer Networks",
        "subtopic": "Data link layer: framing, error detection, Medium Access Control, Ethernet bridging",
        "difficulty_level": "Easy",
        "explaination": "Propagation time is $T_{\\text{prop}} = \\frac{2100 \\times 10^3\\text{ m}}{3 \\times 10^8\\text{ m/s}} = 7.00\\text{ ms}$. Transmission time is $T_{\\text{trans}} = \\frac{1000 \\times 8\\text{ bits}}{100 \\times 10^6\\text{ bps}} = 0.08\\text{ ms}$. Total time to completely receive the packet is $T_{\\text{prop}} + T_{\\text{trans}} = 7.00 + 0.08 = 7.08\\text{ ms}$.",
        "question_text_latex": "Consider a 100 Mbps link between an earth station (sender) and a satellite (receiver) at an altitude of 2100 km. The signal propagates at a speed of $3 \\times 10^8\\text{ m/s}$. The time taken (in milliseconds, rounded off to two decimal places) for the receiver to completely receive a packet of 1000 bytes transmitted by the sender is \\_\\_\\_\\_\\_\\_\\_\\_\\_\\. (Answer in numeric format)",
        "options_latex": None
    },
    "2022_CS_CS_Q60": {
        "topic": "Computer Networks",
        "subtopic": "Transport layer: flow control and congestion control, UDP, TCP, sockets",
        "difficulty_level": "Medium",
        "explaination": "Data transmitted at 1 Gbps line rate in $\\text{MSL} = 60\\text{ s}$ is $\\frac{10^9\\text{ bps}}{8} \\times 60\\text{ s} = 7.5 \\times 10^9\\text{ bytes}$. The sequence number space must satisfy $2^k \\ge 7.5 \\times 10^9$. Since $2^{32} \\approx 4.29 \\times 10^9 < 7.5 \\times 10^9$ and $2^{33} \\approx 8.59 \\times 10^9 > 7.5 \\times 10^9$, at least 33 bits are required.",
        "question_text_latex": "Consider the data transfer using TCP over a 1 Gbps link. Assuming that the maximum segment lifetime (MSL) is set to 60 seconds, the minimum number of bits required for the sequence number field of the TCP header, to prevent the sequence number space from wrapping around during the MSL is \\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\. (Answer in integer)",
        "options_latex": None
    },
    "2022_CS_CS_Q61": {
        "topic": "Computer Organization and Architecture",
        "subtopic": "Instruction pipelining, pipeline hazards",
        "difficulty_level": "Medium",
        "explaination": "For $X_1$: $\\text{CPI}_1 = 1 + (0.30 \\times 2) = 1.60$. For $X_2$: with 80% branch prediction accuracy, only 20% of branches stall: $\\text{CPI}_2 = 1 + (0.30 \\times 0.20 \\times 2) = 1.12$. Speedup $= \\frac{\\text{CPI}_1}{\\text{CPI}_2} = \\frac{1.60}{1.12} \\approx 1.43$.",
        "question_text_latex": "A processor X1 operating at 2 GHz has a standard 5-stage RISC instruction pipeline having a base CPI (cycles per instruction) of one without any pipeline hazards. For a given program P that has 30\\% branch instructions, control hazards incur 2 cycles stall for every branch. A new version of the processor X2 operating at same clock frequency has an additional branch predictor unit (BPU) that completely eliminates stalls for correctly predicted branches. There is neither any savings nor any additional stalls for wrong predictions. There are no structural hazards and data hazards for X1 and X2. If the BPU has a prediction accuracy of 80\\%, the speed up (rounded off to two decimal places) obtained by X2 over X1 in executing P is \\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\. (Answer in numeric format)",
        "options_latex": None
    },
    "2022_CS_CS_Q62": {
        "topic": "Programming and Data Structures",
        "subtopic": "Arrays, stacks, queues, linked lists",
        "difficulty_level": "Medium",
        "explaination": "To place the 4 elements of $Q_1$ into $Q_2$ in reverse order, elements are dequeued one by one from $Q_1$ and placed into $Q_2$. Internal order manipulation can be performed entirely by cycling elements within $Q_2$ via dequeue/enqueue on $Q_2$, requiring 0 enqueue operations on $Q_1$.",
        "question_text_latex": "Consider the queues $Q_1$ containing four elements and $Q_2$ containing none. The only operations allowed on these two queues are `Enqueue(Q, element)` and `Dequeue(Q)`. The minimum number of `Enqueue` operations on $Q_1$ required to place the elements of $Q_1$ in $Q_2$ in reverse order without using any additional storage is \\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\. (Answer in integer)",
        "options_latex": None
    },
    "2022_CS_CS_Q63": {
        "topic": "Operating System",
        "subtopic": "File systems",
        "difficulty_level": "Hard",
        "explaination": "In contiguous allocation $A$, inserting after block 50 requires shifting blocks 51 to 100 right by one position (50 reads + 50 writes) and writing the new block (1 write), so $n_A = 50 + 50 + 1 = 101$. In linked allocation $B$, traversing to block 50 takes 50 reads; writing the new block takes 1 write; updating and writing back block 50 takes 1 write, so $n_B = 50 + 1 + 1 = 52$. Thus $n_A + n_B = 101 + 52 = 153$.",
        "question_text_latex": "Consider two file systems A and B, that use contiguous allocation and linked allocation, respectively. A file of size 100 blocks is already stored in A and also in B. Now, consider inserting a new block in the middle of the file (between 50th and 51st block), whose data is already available in the memory. Assume that there are enough free blocks at the end of the file and that the file control blocks are already in memory. Let the number of disk accesses required to insert a block in the middle of the file in A and B be $n_A$ and $n_B$ respectively, then the value of $n_A + n_B$ is \\_\\_\\_\\_\\_\\_\\_\\_\\_\\. (Answer in integer)",
        "options_latex": None
    },
    "2022_CS_CS_Q64": {
        "topic": "Operating System",
        "subtopic": "Memory management and virtual memory",
        "difficulty_level": "Medium",
        "explaination": "Simulating LRU with 4 empty frames on sequence $7, 2, 7, 3, 2, 5, 3, 4, 6, 7, 7, 1, 5, 6, 1$: page faults occur at references 1 (7), 2 (2), 4 (3), 6 (5), 8 (4), 9 (6), 10 (7), 12 (1), and 13 (5), totaling 9 faults across 15 accesses. Page fault rate is $9 / 15 = 0.6$.",
        "question_text_latex": "Consider a demand paging system with four page frames (initially empty) and LRU page replacement policy. For the following page reference string\n\\[ 7, 2, 7, 3, 2, 5, 3, 4, 6, 7, 7, 1, 5, 6, 1 \\]\nthe page fault rate, defined as the ratio of number of page faults to the number of memory accesses (rounded off to one decimal place) is \\_\\_\\_\\_\\_\\_\\_\\_\\_\\. (Answer in numeric format)",
        "options_latex": None
    },
    "2022_CS_CS_Q65": {
        "topic": "Compiler Design",
        "subtopic": "Lexical analysis, parsing, syntax-directed translation",
        "difficulty_level": "Medium",
        "explaination": "The SDD implements left-associative operators with $\\%$ at higher precedence than $\\#$. In `20 # 10 % 5 # 8 % 2 % 2`, we first evaluate subexpressions: $10 \\% 5 = 10 / 5 = 2$, and $8 \\% 2 \\% 2 = (8 / 2) / 2 = 2$. Then the outer multiplication evaluates left-associatively: $(20 \\times 2) \\times 2 = 40 \\times 2 = 80$.",
        "question_text_latex": "Consider the following grammar along with translation rules:\n\\begin{align*}\nS &\\to S_1 \\,\\#\\, T & S.val &= S_1.val * T.val \\\\\nS &\\to T & S.val &= T.val \\\\\nT &\\to T_1 \\,\\%\\, R & T.val &= T_1.val \\div R.val \\\\\nT &\\to R & T.val &= R.val \\\\\nR &\\to id & R.val &= id.val\n\\end{align*}\nHere $\\#$ and $\\%$ are operators and $id$ is a token that represents an integer. Using this translation scheme, the computed value of $S.val$ for root of the parse tree for the expression `20#10%5#8%2%2` is \\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\. (Answer in integer)",
        "options_latex": None
    }
}

def main():
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    paper_dir = os.path.join(root_dir, "dataset", "papers", "2022_CS")

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

    print(f"Enriched {updated_count} questions in 2022_CS paper files successfully.")

if __name__ == "__main__":
    main()
