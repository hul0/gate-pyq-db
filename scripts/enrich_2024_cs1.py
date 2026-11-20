#!/usr/bin/env python3
"""
enrich_2024_cs1.py

Fills the AI metadata fields for 2024 CS1 questions based on syllabus/cs_2026_syllabus.json:
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
    "2024_CS1_GA_Q01": {
        "topic": "Verbal Aptitude",
        "subtopic": "Vocabulary: words, idioms, and phrases in context",
        "difficulty_level": "Easy",
        "explaination": "'dry $\\to$ arid $\\to$ parched' depicts an increasing scale of lack of moisture. Similarly, 'diet $\\to$ fast $\\to$ starve' depicts an increasing scale of food restriction/deprivation, where starving represents extreme lack of nourishment.",
        "question_text_latex": "If `$\\to$' denotes increasing order of intensity, then the meaning of the words $[\\text{dry} \\to \\text{arid} \\to \\text{parched}]$ is analogous to $[\\text{diet} \\to \\text{fast} \\to \\text{\\_\\_\\_\\_\\_\\_\\_\\_}]$.\nWhich one of the given options is appropriate to fill the blank?",
        "options_latex": {
            "A": "starve",
            "B": "reject",
            "C": "feast",
            "D": "deny"
        }
    },
    "2024_CS1_GA_Q02": {
        "topic": "Quantitative Aptitude",
        "subtopic": "Numerical computation and estimation: ratios, percentages, powers, exponents and logarithms, permutations and combinations, series",
        "difficulty_level": "Easy",
        "explaination": "If $(x+y) \\propto (x-y)$, then $x+y = k(x-y)$ for some non-zero constant $k \\neq 1$. Rearranging terms gives $x(1-k) = -y(1+k) \\implies \\frac{x}{y} = \\frac{k+1}{k-1}$, which is a constant independent of $x$ and $y$.",
        "question_text_latex": "If two distinct non-zero real variables $x$ and $y$ are such that $(x+y)$ is proportional to $(x-y)$ then the value of $\\frac{x}{y}$",
        "options_latex": {
            "A": "depends on $xy$",
            "B": "depends only on $x$ and not on $y$",
            "C": "depends only on $y$ and not on $x$",
            "D": "is a constant"
        }
    },
    "2024_CS1_GA_Q03": {
        "topic": "Quantitative Aptitude",
        "subtopic": "Elementary statistics and probability",
        "difficulty_level": "Easy",
        "explaination": "Arranging the 10 sample values in ascending order: $9, 10, 11, 11, 13, 14, 15, 17, 18, 69$. Since the sample size $n = 10$ is even, the median is the arithmetic mean of the 5th and 6th values: $\\frac{13 + 14}{2} = 13.5$.",
        "question_text_latex": "Consider the following sample of numbers:\n\\[ 9, 18, 11, 14, 15, 17, 10, 69, 11, 13 \\]\nThe median of the sample is",
        "options_latex": {
            "A": "13.5",
            "B": "14",
            "C": "11",
            "D": "18.7"
        }
    },
    "2024_CS1_GA_Q04": {
        "topic": "Quantitative Aptitude",
        "subtopic": "Numerical computation and estimation: ratios, percentages, powers, exponents and logarithms, permutations and combinations, series",
        "difficulty_level": "Easy",
        "explaination": "Let the number of Rs.~1, Rs.~5, and Rs.~10 coins be $5k$, $3k$, and $13k$ respectively. The total value is $1(5k) + 5(3k) + 10(13k) = 5k + 15k + 130k = 150k$. The percentage of money in Rs.~5 coins is $\\frac{15k}{150k} \\times 100\\% = 10\\%$.",
        "question_text_latex": "The number of coins of Rs.~1, Rs.~5, and Rs.~10 denominations that a person has are in the ratio $5:3:13$. Of the total amount, the percentage of money in Rs.~5 coins is",
        "options_latex": {
            "A": "21\\%",
            "B": "$14\\frac{2}{7}\\%$",
            "C": "10\\%",
            "D": "30\\%"
        }
    },
    "2024_CS1_GA_Q05": {
        "topic": "Quantitative Aptitude",
        "subtopic": "Numerical computation and estimation: ratios, percentages, powers, exponents and logarithms, permutations and combinations, series",
        "difficulty_level": "Medium",
        "explaination": "Using logarithm rules, $\\log(p^2 + q^2) = \\log p + \\log q + 2\\log 3 = \\log(9pq) \\implies p^2 + q^2 = 9pq$. Squaring both sides yields $(p^2+q^2)^2 = p^4 + q^4 + 2p^2q^2 = 81p^2q^2$, which gives $p^4 + q^4 = 79p^2q^2$. Hence, $\\frac{p^4+q^4}{p^2q^2} = 79$.",
        "question_text_latex": "For positive non-zero real variables $p$ and $q$, if\n\\[ \\log(p^2 + q^2) = \\log p + \\log q + 2\\log 3, \\]\nthen, the value of $\\frac{p^4+q^4}{p^2q^2}$ is",
        "options_latex": {
            "A": "79",
            "B": "81",
            "C": "9",
            "D": "83"
        }
    },

    # ==================== GA 2-MARK ====================
    "2024_CS1_GA_Q06": {
        "topic": "Verbal Aptitude",
        "subtopic": "Vocabulary: words, idioms, and phrases in context",
        "difficulty_level": "Easy",
        "explaination": "'Keep one's head down' means to stay focused and avoid trouble. 'Heading out' means going forth/departing. Having a 'head for' an activity signifies natural aptitude for it, and having a cool 'head on' one's shoulders means remaining calm and composed.",
        "question_text_latex": "In the given text, the blanks are numbered (i)--(iv). Select the best match for all the blanks.\n\nSteve was advised to keep his head (i)\\_\\_\\_\\_ before heading (ii)\\_\\_\\_\\_ to bat; for, while he had a head (iii)\\_\\_\\_\\_ batting, he could only do so with a cool head (iv)\\_\\_\\_\\_ his shoulders.",
        "options_latex": {
            "A": "(i) down (ii) down (iii) on (iv) for",
            "B": "(i) on (ii) down (iii) for (iv) on",
            "C": "(i) down (ii) out (iii) for (iv) on",
            "D": "(i) on (ii) out (iii) on (iv) for"
        }
    },
    "2024_CS1_GA_Q07": {
        "topic": "Quantitative Aptitude",
        "subtopic": "Mensuration and geometry",
        "difficulty_level": "Medium",
        "explaination": "Joining the longer edges ($54\\text{ cm}$) creates a cylinder with height $h = 54\\text{ cm}$ and circumference $2\\pi r = 4\\text{ cm} \\implies r = \\frac{2}{\\pi}$, giving volume $V_{\\text{cyl}} = \\pi r^2 h = \\frac{216}{\\pi}$. The sheet area is $54 \\times 4 = 216\\text{ cm}^2$. A cube with surface area $6a^2 = 216$ has edge $a = 6\\text{ cm}$ and volume $V_{\\text{cube}} = 6^3 = 216$. Thus $\\frac{V_{\\text{cyl}}}{V_{\\text{cube}}} = \\frac{216/\\pi}{216} = \\frac{1}{\\pi}$.",
        "question_text_latex": "A rectangular paper sheet of dimensions $54\\text{ cm} \\times 4\\text{ cm}$ is taken. The two longer edges of the sheet are joined together to create a cylindrical tube. A cube whose surface area is equal to the area of the sheet is also taken.\nThen, the ratio of the volume of the cylindrical tube to the volume of the cube is",
        "options_latex": {
            "A": "$1/\\pi$",
            "B": "$2/\\pi$",
            "C": "$3/\\pi$",
            "D": "$4/\\pi$"
        }
    },
    "2024_CS1_GA_Q09": {
        "topic": "Spatial Aptitude",
        "subtopic": "Paper folding, cutting, and patterns in 2 and 3 dimensions",
        "difficulty_level": "Medium",
        "explaination": "Starting at $20 \\times 8\\text{ cm}$, the 1st fold perpendicular to the long edge yields $10 \\times 8\\text{ cm}$. The 2nd fold perpendicular to the new long edge ($10\\text{ cm}$) yields $5 \\times 8\\text{ cm}$. The 3rd fold perpendicular to the new long edge ($8\\text{ cm}$) yields $5 \\times 4\\text{ cm}$. The perimeter of this final folded sheet is $2(5 + 4) = 18\\text{ cm}$.",
        "question_text_latex": "A rectangular paper of $20\\text{ cm} \\times 8\\text{ cm}$ is folded 3 times. Each fold is made along the line of symmetry, which is perpendicular to its long edge. The perimeter of the final folded sheet (in cm) is",
        "options_latex": {
            "A": "18",
            "B": "24",
            "C": "20",
            "D": "21"
        }
    },
    "2024_CS1_GA_Q10": {
        "topic": "Spatial Aptitude",
        "subtopic": "Transformation of shapes: translation, rotation, scaling, mirroring, assembling, and grouping",
        "difficulty_level": "Medium",
        "explaination": "Reflecting each shaded cell across the diagonal axis $AB$ reveals that exactly 6 asymmetric squares must be shaded on the opposing side to achieve bilateral reflectional symmetry about line $AB$.",
        "question_text_latex": "The least number of squares to be added in the figure to make $AB$ a line of symmetry is",
        "options_latex": {
            "A": "6",
            "B": "4",
            "C": "5",
            "D": "7"
        }
    },

    # ==================== CS 1-MARK ====================
    "2024_CS1_CS_Q11": {
        "topic": "Calculus",
        "subtopic": "Limits, continuity and differentiability",
        "difficulty_level": "Medium",
        "explaination": "The functions $y = x$ and $y = x^3$ intersect at $x^3 - x = 0 \\implies x \\in \\{-1, 0, 1\\}$. The maximum function $f(x) = \\max\\{x, x^3\\}$ switches between $x$ and $x^3$ at each of these three intersection points. Because the left and right derivatives at each transition point differ ($f'(-1^-) = 3 \\neq 1 = f'(-1^+)$, $f'(0^-) = 1 \\neq 0 = f'(0^+)$, $f'(1^-) = 1 \\neq 3 = f'(1^+)$), $f(x)$ is not differentiable at $\\{-1, 0, 1\\}$.",
        "question_text_latex": "Let $f: \\mathbb{R} \\to \\mathbb{R}$ be a function such that $f(x) = \\max\\{x, x^3\\}$, where $\\mathbb{R}$ is the set of all real numbers. The set of all points where $f(x)$ is NOT differentiable is",
        "options_latex": {
            "A": "$\\{-1, 1, 2\\}$",
            "B": "$\\{-2, -1, 1\\}$",
            "C": "$\\{0, 1\\}$",
            "D": "$\\{-1, 0, 1\\}$"
        }
    },
    "2024_CS1_CS_Q12": {
        "topic": "Linear Algebra",
        "subtopic": "Eigenvalues and eigenvectors",
        "difficulty_level": "Easy",
        "explaination": "The product of all eigenvalues of a square matrix equals its determinant $\\det(A)$. In $A = \\begin{bmatrix} 1 & 2 & 3 \\\\ 4 & 5 & 6 \\\\ 7 & 8 & 9 \\end{bmatrix}$, the rows are in arithmetic progression with $R_3 - R_2 = R_2 - R_1 = [3, 3, 3]$, making the rows linearly dependent and $\\det(A) = 0$. Hence, the product of the eigenvalues is 0.",
        "question_text_latex": "The product of all eigenvalues of the matrix $\\begin{bmatrix} 1 & 2 & 3 \\\\ 4 & 5 & 6 \\\\ 7 & 8 & 9 \\end{bmatrix}$ is",
        "options_latex": {
            "A": "$-1$",
            "B": "0",
            "C": "1",
            "D": "2"
        }
    },
    "2024_CS1_CS_Q13": {
        "topic": "Digital Logic",
        "subtopic": "Number representations and computer arithmetic (fixed and floating point)",
        "difficulty_level": "Medium",
        "explaination": "In a 5-bit 2's complement representation, the range is $[-2^4, 2^4 - 1] = [-16, +15]$. Here, $A = 01010_2 = +10$ and $B = 11010_2 = -6$. The operation $A - B = 10 - (-6) = +16$, which exceeds $+15$, resulting in an arithmetic overflow.",
        "question_text_latex": "Consider a system that uses 5 bits for representing signed integers in 2's complement format. In this system, two integers $A$ and $B$ are represented as $A = 01010$ and $B = 11010$. Which one of the following operations will result in either an arithmetic overflow or an arithmetic underflow?",
        "options_latex": {
            "A": "$A + B$",
            "B": "$A - B$",
            "C": "$B - A$",
            "D": "$2 * B$"
        }
    },
    "2024_CS1_CS_Q14": {
        "topic": "Probability and Statistics",
        "subtopic": "Conditional probability and Bayes theorem",
        "difficulty_level": "Medium",
        "explaination": "By symmetry in random permutations of $\\{1, 2, \\dots, n\\}$, $P(X) = P(1 \\text{ before } 2) = 1/2$, and $P(Y) = P(3 \\text{ before } 4) = 1/2$. Because the relative order of the disjoint pair $\\{1, 2\\}$ has no bearing on the relative order of $\\{3, 4\\}$, the joint probability is $P(X \\cap Y) = 1/4 = P(X)P(Y)$, proving that $X$ and $Y$ are independent.",
        "question_text_latex": "Consider a permutation sampled uniformly at random from the set of all permutations of $\\{1, 2, 3, \\dots, n\\}$ for some $n \\ge 4$. Let $X$ be the event that 1 occurs before 2 in the permutation, and $Y$ the event that 3 occurs before 4. Which one of the following statements is TRUE?",
        "options_latex": {
            "A": "The events $X$ and $Y$ are mutually exclusive",
            "B": "The events $X$ and $Y$ are independent",
            "C": "Either event $X$ or $Y$ must occur",
            "D": "Event $X$ is more likely than event $Y$"
        }
    },
    "2024_CS1_CS_Q15": {
        "topic": "Computer Organization and Architecture",
        "subtopic": "I/O interface: interrupt and DMA mode",
        "difficulty_level": "Easy",
        "explaination": "Programmed I/O requires the CPU to stay in a busy-waiting polling loop to check device readiness, wasting processor cycles and yielding poor CPU utilization. Interrupt-driven I/O frees the CPU to execute other tasks while I/O operations are underway, providing significantly better CPU utilization. Thus, statement (C) is FALSE.",
        "question_text_latex": "Which one of the following statements is FALSE?",
        "options_latex": {
            "A": "In the cycle stealing mode of DMA, one word of data is transferred between an I/O device and main memory in a stolen cycle",
            "B": "For bulk data transfer, the burst mode of DMA has a higher throughput than the cycle stealing mode",
            "C": "Programmed I/O mechanism has a better CPU utilization than the interrupt driven I/O mechanism",
            "D": "The CPU can start executing an interrupt service routine faster with vectored interrupts than with non-vectored interrupts"
        }
    },
    "2024_CS1_CS_Q16": {
        "topic": "Computer Networks",
        "subtopic": "Concept of layering: OSI and TCP/IP Protocol Stacks",
        "difficulty_level": "Easy",
        "explaination": "Initially all caches are empty. The client must first send a DNS query (ii) to resolve the server hostname to an IP. Next, it establishes a TCP connection by sending TCP SYN (iv). Once connected, it sends an HTTP GET request for the index HTML page (i). After parsing the HTML and identifying embedded images, it sends HTTP GET requests for the images (iii).",
        "question_text_latex": "A user starts browsing a webpage hosted at a remote server. The browser opens a single TCP connection to fetch the entire webpage from the server. The webpage consists of a top-level index page with multiple embedded image objects. Assume that all caches (e.g., DNS cache, browser cache) are all initially empty. The following packets leave the user's computer in some order:\n\\begin{enumerate}[label=(\\roman*),itemsep=0pt,topsep=2pt]\n\\item HTTP GET request for the index page\n\\item DNS request to resolve the web server's name to its IP address\n\\item HTTP GET request for an image object\n\\item TCP SYN to open a connection to the web server\n\\end{enumerate}\nWhich one of the following is the CORRECT chronological order (earliest in time to latest) of the packets leaving the computer?",
        "options_latex": {
            "A": "(iv), (ii), (iii), (i)",
            "B": "(ii), (iv), (iii), (i)",
            "C": "(ii), (iv), (i), (iii)",
            "D": "(iv), (ii), (i), (iii)"
        }
    },
    "2024_CS1_CS_Q17": {
        "topic": "Algorithms",
        "subtopic": "Asymptotic worst case time and space complexity",
        "difficulty_level": "Easy",
        "explaination": "In the worst case (such as when the array is sorted or the disorder occurs at the very end), a single-pass algorithm that compares adjacent elements must traverse the entire array, performing $N-1$ comparisons. The worst-case runtime is asymptotically tight at $\\Theta(N)$, meaning it is both $\\mathcal{O}(N)$ and $\\Omega(N)$.",
        "question_text_latex": "Given an integer array of size $N$, we want to check if the array is sorted (in either ascending or descending order). An algorithm solves this problem by making a single pass through the array and comparing each element of the array only with its adjacent elements. The worst-case time complexity of this algorithm is",
        "options_latex": {
            "A": "both $\\mathcal{O}(N)$ and $\\Omega(N)$",
            "B": "$\\mathcal{O}(N)$ but not $\\Omega(N)$",
            "C": "$\\Omega(N)$ but not $\\mathcal{O}(N)$",
            "D": "neither $\\mathcal{O}(N)$ nor $\\Omega(N)$"
        }
    },
    "2024_CS1_CS_Q18": {
        "topic": "Programming and Data Structures",
        "subtopic": "Programming in C",
        "difficulty_level": "Easy",
        "explaination": "Initially $a = 6, b = 0$. In the loop, integer division $a/12 = 6/12 = 0$, so $a = 0 + 1 = 1$, and $a += b \\implies a = 1$. In subsequent iterations, $a=1 < 10$, $1/12 + 1 = 1$, so $a$ remains 1 in every iteration. The loop condition $a < 10$ remains true indefinitely, causing an infinite loop.",
        "question_text_latex": "Consider the following C program:\n\\begin{lstlisting}[language=C]\n#include <stdio.h>\nint main() {\n    int a = 6;\n    int b = 0;\n    while(a < 10) {\n        a = a / 12 + 1;\n        a += b;\n    }\n    printf(\"%d\", a);\n    return 0;\n}\n\\end{lstlisting}\nWhich one of the following statements is CORRECT?",
        "options_latex": {
            "A": "The program prints 9 as output",
            "B": "The program prints 10 as output",
            "C": "The program gets stuck in an infinite loop",
            "D": "The program prints 6 as output"
        }
    },
    "2024_CS1_CS_Q19": {
        "topic": "Programming and Data Structures",
        "subtopic": "Recursion",
        "difficulty_level": "Easy",
        "explaination": "The function `fX()` recursively reads each character before printing. As each character (`'1'`, `'2'`, `'3'`, `'4'`) is read, it is saved on the call stack before `fX()` recurses. When `\\n` is reached, recursion terminates and the characters are printed during stack unwinding in reverse (LIFO) order as `4321`.",
        "question_text_latex": "Consider the following C program:\n\\begin{lstlisting}[language=C]\n#include <stdio.h>\nvoid fX();\nint main() {\n    fX();\n    return 0;\n}\nvoid fX() {\n    char a;\n    if((a = getchar()) != '\\n')\n        fX();\n    if(a != '\\n')\n        putchar(a);\n}\n\\end{lstlisting}\nAssume that the input to the program from the command line is `1234` followed by a newline character. Which one of the following statements is CORRECT?",
        "options_latex": {
            "A": "The program will not terminate",
            "B": "The program will terminate with no output",
            "C": "The program will terminate with 4321 as output",
            "D": "The program will terminate with 1234 as output"
        }
    },
    "2024_CS1_CS_Q20": {
        "topic": "Databases",
        "subtopic": "ER-model",
        "difficulty_level": "Medium",
        "explaination": "Specification $S$ describes four distinct binary relationships among entities: Instructors teach courses, Students register for courses, Courses are allocated classrooms, and Instructors guide students. In standard ER modeling, entity sets are represented by rectangles and relationships by diamond diamonds connecting them; diagram (iv) correctly captures all four relationship sets.",
        "question_text_latex": "Let $S$ be the specification: ``Instructors teach courses. Students register for courses. Courses are allocated classrooms. Instructors guide students.'' Which one of the following ER diagrams CORRECTLY represents $S$?",
        "options_latex": {
            "A": "(i)",
            "B": "(ii)",
            "C": "(iii)",
            "D": "(iv)"
        }
    },
    "2024_CS1_CS_Q21": {
        "topic": "Databases",
        "subtopic": "File organization, indexing (e.g., B and B+ trees)",
        "difficulty_level": "Easy",
        "explaination": "In a $\\text{B}^+$ tree, every node except the root node must satisfy the minimum occupancy constraint of being at least half full ($\text{at least } \\lceil p/2 \\rceil$ child pointers). The root node is the sole exception, and is permitted to hold as few as two pointers (or one key) when non-leaf, and one key when leaf.",
        "question_text_latex": "In a $\\text{B}^+$ tree, the requirement of at least half-full (50\\%) node occupancy is relaxed for which one of the following cases?",
        "options_latex": {
            "A": "Only the root node",
            "B": "All leaf nodes",
            "C": "All internal nodes",
            "D": "Only the leftmost leaf node"
        }
    },
    "2024_CS1_CS_Q22": {
        "topic": "Databases",
        "subtopic": "Integrity constraints, normal forms",
        "difficulty_level": "Easy",
        "explaination": "A relation is in 1NF if and only if all attribute values are atomic, which explicitly forbids composite or multi-valued attributes (making (C) TRUE). 1NF places no limitation on candidate keys having multiple attributes (multi-attribute keys are fully permitted, making (A) TRUE) or the presence of foreign keys.",
        "question_text_latex": "Which of the following statements about a relation $R$ in first normal form (1NF) is/are TRUE?",
        "options_latex": {
            "A": "$R$ can have a multi-attribute key",
            "B": "$R$ cannot have a foreign key",
            "C": "$R$ cannot have a composite attribute",
            "D": "$R$ cannot have more than one candidate key"
        }
    },
    "2024_CS1_CS_Q23": {
        "topic": "Theory of Computation",
        "subtopic": "Regular and context-free languages, pumping lemma",
        "difficulty_level": "Medium",
        "explaination": "Regular languages are closed under complementation and union; since $L_1, L_2$ are regular, $\\overline{L_1}$ and $\\overline{L_2}$ are regular, so $\\overline{L_1} \\cup \\overline{L_2}$ is regular (D is TRUE). If $L_3$ is non-regular, its complement $\\overline{L_3}$ must also be non-regular, because if $\\overline{L_3}$ were regular, its complement $\\overline{\\overline{L_3}} = L_3$ would be regular, a contradiction (C is TRUE).",
        "question_text_latex": "Let $L_1, L_2$ be two regular languages and $L_3$ a language which is not regular. Which of the following statements is/are always TRUE?",
        "options_latex": {
            "A": "$L_1 = L_2$ if and only if $L_1 \\cap \\overline{L_2} = \\emptyset$",
            "B": "$L_1 \\cup L_3$ is not regular",
            "C": "$\\overline{L_3}$ is not regular",
            "D": "$\\overline{L_1} \\cup \\overline{L_2}$ is regular"
        }
    },
    "2024_CS1_CS_Q24": {
        "topic": "Operating System",
        "subtopic": "System calls, processes, threads, inter-process communication",
        "difficulty_level": "Easy",
        "explaination": "All threads of a single process share the same address space (code, global data, heap) and open files. Because they run within the same virtual address space without memory protection barriers between them, one thread can corrupt another thread's memory; hence they are by default not protected from each other (D is TRUE). Each thread maintains its own private stack and registers.",
        "question_text_latex": "Which of the following statements about threads is/are TRUE?",
        "options_latex": {
            "A": "Threads can only be implemented in kernel space",
            "B": "Each thread has its own file descriptor table for open files",
            "C": "All the threads belonging to a process share a common stack",
            "D": "Threads belonging to a process are by default not protected from each other"
        }
    },
    "2024_CS1_CS_Q25": {
        "topic": "Operating System",
        "subtopic": "System calls, processes, threads, inter-process communication",
        "difficulty_level": "Easy",
        "explaination": "In the standard process state model, a process in the Waiting (Blocked) state transitions to Ready upon event/I/O completion; it cannot transition directly to Running without CPU dispatch (B is impossible). Similarly, only a Running process can initiate an I/O request and transition to Waiting; a Ready process cannot transition directly to Waiting (C is impossible).",
        "question_text_latex": "Which of the following process state transitions is/are NOT possible?",
        "options_latex": {
            "A": "Running to Ready",
            "B": "Waiting to Running",
            "C": "Ready to Waiting",
            "D": "Running to Terminated"
        }
    },
    "2024_CS1_CS_Q26": {
        "topic": "Compiler Design",
        "subtopic": "Lexical analysis, parsing, syntax-directed translation",
        "difficulty_level": "Easy",
        "explaination": "Bottom-up parsers reduce an input string back to the start symbol by finding handles. Shift-reduce parsers and LR parsers (SLR, CLR, LALR) are bottom-up parsers. In contrast, Predictive and LL(1) parsers construct the derivation tree from the root downward and are top-down parsers.",
        "question_text_latex": "Which of the following is/are Bottom-Up Parser(s)?",
        "options_latex": {
            "A": "Shift-reduce Parser",
            "B": "Predictive Parser",
            "C": "LL(1) Parser",
            "D": "LR Parser"
        }
    },
    "2024_CS1_CS_Q27": {
        "topic": "Probability and Statistics",
        "subtopic": "Conditional probability and Bayes theorem",
        "difficulty_level": "Easy",
        "explaination": "We are given $P(A) = 0.3$, $P(B) = 0.5$, and $P(A \\cap B) = 0.1$. First, $P(A \\cup B) = P(A) + P(B) - P(A \\cap B) = 0.3 + 0.5 - 0.1 = 0.7$ (B is TRUE). Second, $P(A \\cap B^c) = P(A) - P(A \\cap B) = 0.3 - 0.1 = 0.2$ (C is TRUE). Since $P(A)P(B) = 0.15 \\neq 0.1$, the events are not independent.",
        "question_text_latex": "Let $A$ and $B$ be two events in a probability space with $P(A) = 0.3$, $P(B) = 0.5$, and $P(A \\cap B) = 0.1$. Which of the following statements is/are TRUE?",
        "options_latex": {
            "A": "The two events $A$ and $B$ are independent",
            "B": "$P(A \\cup B) = 0.7$",
            "C": "$P(A \\cap B^c) = 0.2$, where $B^c$ is the complement of the event $B$",
            "D": "$P(A^c \\cap B^c) = 0.4$, where $A^c$ and $B^c$ are the complements of the events $A$ and $B$, respectively"
        }
    },
    "2024_CS1_CS_Q28": {
        "topic": "Digital Logic",
        "subtopic": "Combinational and sequential circuits",
        "difficulty_level": "Medium",
        "explaination": "The circuit computes $Y = X \\cdot \\overline{X}$. In steady-state with no gate delays, $X \\cdot \\overline{X} = 0$, so $Y$ is always logic Zero (A is TRUE). When $X$ transitions from 0 to 1, if the inverter has a non-zero propagation delay, both inputs to the AND gate remain logic 1 for the duration of the inverter delay, producing a transient logic 1 glitch (C is TRUE).",
        "question_text_latex": "Consider the circuit shown below where the gates may have propagation delays. Assume that all signal transitions occur instantaneously and that wires have no delays. Which of the following statements about the circuit is/are CORRECT?",
        "options_latex": {
            "A": "With no propagation delays, the output $Y$ is always logic Zero",
            "B": "With no propagation delays, the output $Y$ is always logic One",
            "C": "With propagation delays, the output $Y$ can have a transient logic One after $X$ transitions from logic Zero to logic One",
            "D": "With propagation delays, the output $Y$ can have a transient logic Zero after $X$ transitions from logic One to logic Zero"
        }
    },
    "2024_CS1_CS_Q29": {
        "topic": "Computer Networks",
        "subtopic": "Transport layer: flow control and congestion control, UDP, TCP, sockets",
        "difficulty_level": "Easy",
        "explaination": "During TCP connection establishment, the initial sequence number $N_P$ is chosen pseudo-randomly to avoid cross-connection packet collisions and mitigate spoofing attacks (A is TRUE). Because a SYN packet consumes exactly 1 sequence number in the sequence space, server $Q$ acknowledges it with $N_Q = N_P + 1$ (D is TRUE).",
        "question_text_latex": "TCP client P successfully establishes a connection to TCP server Q. Let $N_P$ denote the sequence number in the SYN sent from P to Q. Let $N_Q$ denote the acknowledgement number in the SYN ACK from Q to P. Which of the following statements is/are CORRECT?",
        "options_latex": {
            "A": "The sequence number $N_P$ is chosen randomly by P",
            "B": "The sequence number $N_P$ is always 0 for a new connection",
            "C": "The acknowledgement number $N_Q$ is equal to $N_P$",
            "D": "The acknowledgement number $N_Q$ is equal to $N_P + 1$"
        }
    },
    "2024_CS1_CS_Q30": {
        "topic": "Computer Organization and Architecture",
        "subtopic": "Instruction pipelining, pipeline hazards",
        "difficulty_level": "Easy",
        "explaination": "Forwarding (bypassing) routes intermediate results directly from pipeline registers of an earlier instruction to execution inputs of a subsequent instruction (A is TRUE). While forwarding resolves many ALU data dependencies without stalls, it cannot prevent a load-use stall (where the loaded data is needed immediately in the subsequent instruction's EX stage), requiring at least one stall cycle (C is TRUE).",
        "question_text_latex": "Consider a 5-stage pipelined processor with Instruction Fetch (IF), Instruction Decode (ID), Execute (EX), Memory Access (MEM), and Register Writeback (WB) stages. Which of the following statements about forwarding is/are CORRECT?",
        "options_latex": {
            "A": "In a pipelined execution, forwarding means the result from a source stage of an earlier instruction is passed on to the destination stage of a later instruction",
            "B": "In forwarding, data from the output of the MEM stage can be passed on to the input of the EX stage of the next instruction",
            "C": "Forwarding cannot prevent all pipeline stalls",
            "D": "Forwarding does not require any extra hardware to retrieve the data from the pipeline stages"
        }
    },
    "2024_CS1_CS_Q31": {
        "topic": "Computer Networks",
        "subtopic": "Network Address Translation (NAT)",
        "difficulty_level": "Easy",
        "explaination": "When a packet leaves a private subnet through an outbound NAT gateway, the router rewrites the private Source IP address to its public external IP address (A is modified). Because the IP header fields have changed, the IPv4 Header Checksum must be recalculated and replaced (C is modified). Destination IP and Total Length are unmodified.",
        "question_text_latex": "Which of the following fields is/are modified in the IP header of a packet going out of a network address translation (NAT) device from an internal network to an external network?",
        "options_latex": {
            "A": "Source IP",
            "B": "Destination IP",
            "C": "Header Checksum",
            "D": "Total Length"
        }
    },
    "2024_CS1_CS_Q32": {
        "topic": "Discrete Mathematics",
        "subtopic": "Sets, relations, functions, partial orders and lattices",
        "difficulty_level": "Medium",
        "explaination": "A bijection from $A$ to $B$ implies $|A| = |B| = n$. A bijection from $A \\times A$ to $A \\cup B$ implies $|A \\times A| = |A \\cup B|$. We have $|A \\times A| = n^2$, and $n \\le |A \\cup B| \\le 2n$. Thus $n \\le n^2 \\le 2n$. Since $A$ is non-empty ($n \\ge 1$), dividing by $n$ gives $1 \\le n \\le 2$. This allows exactly two integer solutions: $n = 1$ (where $A = B$) and $n = 2$ (where $A \\cap B = \\emptyset$).",
        "question_text_latex": "Let $A$ and $B$ be non-empty finite sets such that there exist one-to-one and onto functions (i) from $A$ to $B$ and (ii) from $A \\times A$ to $A \\cup B$. The number of possible values of $|A|$ is \\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\. (Answer in integer)",
        "options_latex": None
    },
    "2024_CS1_CS_Q33": {
        "topic": "Compiler Design",
        "subtopic": "Lexical analysis, parsing, syntax-directed translation",
        "difficulty_level": "Medium",
        "explaination": "Precedence order is $+$ (highest, left-associative), then $-$ (right-associative), then $*$ (right-associative), then $/$ (lowest, right-associative). Evaluating $+$ first: $3+1+5 = 9$ and $7+2 = 9$. Expression becomes $9 * 2 / 9 - 4 - 7 - 6 / 2$. Evaluating $-$ right-associatively: $4 - (7 - 6) = 4 - 1 = 3$, giving $9 - 3 = 6$. The expression becomes $9 * 2 / 6 / 2$. Next $*$ gives $18 / 6 / 2$. Evaluating $/$ right-associatively: $6 / 2 = 3$, and $18 / 3 = 6$.",
        "question_text_latex": "Consider the operator precedence and associativity rules for the integer arithmetic operators given in the table below:\n\\begin{center}\n\\begin{tabular}{|c|c|c|}\n\\hline\n\\textbf{Operator} & \\textbf{Precedence} & \\textbf{Associativity} \\\\\n\\hline\n$+$ & Highest & Left \\\\\n$-$ & High & Right \\\\\n$*$ & Medium & Right \\\\\n$/$ & Low & Right \\\\\n\\hline\n\\end{tabular}\n\\end{center}\nThe value of the expression $3 + 1 + 5 * 2 / 7 + 2 - 4 - 7 - 6 / 2$ as per the above rules is \\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\. (Answer in integer)",
        "options_latex": None
    },
    "2024_CS1_CS_Q34": {
        "topic": "Discrete Mathematics",
        "subtopic": "Combinatorics: counting, recurrence relations, generating functions",
        "difficulty_level": "Easy",
        "explaination": "By Cayley's theorem, the number of spanning trees in a complete labelled graph $K_n$ on $n$ vertices is given by $n^{n-2}$. For $n = 4$ labelled vertices A, B, C, D, the number of spanning trees is $4^{4-2} = 4^2 = 16$.",
        "question_text_latex": "The number of spanning trees in a complete graph of 4 vertices labelled A, B, C, and D is \\_\\_\\_\\_\\_\\_\\_\\_\\_\\. (Answer in integer)",
        "options_latex": None
    },
    "2024_CS1_CS_Q35": {
        "topic": "Databases",
        "subtopic": "Relational model: relational algebra, tuple calculus, SQL",
        "difficulty_level": "Easy",
        "explaination": "Joining $R(A,B)$ and $S(A,C)$ on $R.A = S.A$ yields: $(10, 20, 90)$ for $A=10$, and $(30, 40, 45)$, $(30, 50, 45)$ for $A=30$. Applying selection $\\sigma_{B < C}$: $20 < 90$ is true (tuple $(10, 20, 90)$), $40 < 45$ is true (tuple $(30, 40, 45)$), and $50 < 45$ is false. Thus, exactly 2 tuples satisfy the condition.",
        "question_text_latex": "Consider the following two relations, $R(A,B)$ and $S(A,C)$:\n\\begin{center}\n\\begin{tabular}{|c|c|}\n\\multicolumn{2}{c}{$R$} \\\\\n\\hline\n$A$ & $B$ \\\\\n\\hline\n10 & 20 \\\\\n20 & 30 \\\\\n30 & 40 \\\\\n30 & 50 \\\\\n\\hline\n\\end{tabular}\n\\qquad\n\\begin{tabular}{|c|c|}\n\\multicolumn{2}{c}{$S$} \\\\\n\\hline\n$A$ & $C$ \\\\\n\\hline\n10 & 90 \\\\\n30 & 45 \\\\\n40 & 80 \\\\\n50 & 95 \\\\\n\\hline\n\\end{tabular}\n\\end{center}\nThe total number of tuples obtained by evaluating the following expression\n\\[ \\sigma_{B < C}(R \\bowtie_{R.A = S.A} S) \\]\nis \\_\\_\\_\\_\\_\\_\\_\\_\\_\\. (Answer in integer)",
        "options_latex": None
    },

    # ==================== CS 2-MARK ====================
    "2024_CS1_CS_Q36": {
        "topic": "Computer Networks",
        "subtopic": "Concept of layering: OSI and TCP/IP Protocol Stacks",
        "difficulty_level": "Medium",
        "explaination": "The file size is $10^6$ bytes split into 1000 chunks of $10^3$ bytes ($8000$ bits) each. Link transmission time for one chunk is $\\frac{8000\\text{ bits}}{10^6\\text{ bps}} = 0.008\\text{ s}$. Node P completes sending all 1000 chunks at $t = 1000 \\times 0.008 = 8.000\\text{ s}$. The last chunk arrives at router Q at $t = 8.000\\text{ s}$ and takes another $0.008\\text{ s}$ to reach R over link Q---R, completing at $8.008\\text{ s}$.",
        "question_text_latex": "Consider a network path P---Q---R between nodes P and R via router Q. Node P sends a file of size $10^6$ bytes to R via this path by splitting the file into chunks of $10^3$ bytes each. Node P sends these chunks one after the other without any wait time between the successive chunk transmissions. Assume that the size of extra headers added to these chunks is negligible, and that the chunk size is less than the MTU.\n\nEach of the links P---Q and Q---R has a bandwidth of $10^6$ bits/sec, and negligible propagation latency. Router Q immediately transmits every packet it receives from P to R, with negligible processing and queueing delays. Router Q can simultaneously receive on link P---Q and transmit on link Q---R.\n\nAssume P starts transmitting the chunks at time $t = 0$.\nWhich one of the following options gives the time (in seconds, rounded off to 3 decimal places) at which R receives all the chunks of the file?",
        "options_latex": {
            "A": "8.000",
            "B": "8.008",
            "C": "15.992",
            "D": "16.000"
        }
    },
    "2024_CS1_CS_Q37": {
        "topic": "Compiler Design",
        "subtopic": "Lexical analysis, parsing, syntax-directed translation",
        "difficulty_level": "Medium",
        "explaination": "For input \"MMLK\" with production $S \\to DHTU$: $D$ derives \"MM\" via $D \\to \\text{\"M\"} D_1 \\to \\text{\"M\"}\\text{\"M\"} D_2 \\to \\text{\"M\"}\\text{\"M\"}\\epsilon$, giving $D.val = 5 + 5 - 5 = 5$. $H$ derives \"L\" via $H \\to \\text{\"L\"} H_1 \\to \\text{\"L\"}\\epsilon$, giving $H.val = 50 - 10 = 40$. $T$ derives $\\epsilon$, giving $T.val = -5$. $U$ derives \"K\", giving $U.val = 5$. Summing attribute values yields $S.val = 5 + 40 - 5 + 5 = 45$.",
        "question_text_latex": "Consider the following syntax-directed definition (SDD):\n\\begin{align*}\nS &\\to DHTU & \\{ S.val = D.val + H.val + T.val + U.val; \\} \\\\\nD &\\to \\text{``M''} D_1 & \\{ D.val = 5 + D_1.val; \\} \\\\\nD &\\to \\epsilon & \\{ D.val = -5; \\} \\\\\nH &\\to \\text{``L''} H_1 & \\{ H.val = 5 * 10 + H_1.val; \\} \\\\\nH &\\to \\epsilon & \\{ H.val = -10; \\} \\\\\nT &\\to \\text{``C''} T_1 & \\{ T.val = 5 * 100 + T_1.val; \\} \\\\\nT &\\to \\epsilon & \\{ T.val = -5; \\} \\\\\nU &\\to \\text{``K''} & \\{ U.val = 5; \\}\n\\end{align*}\nGiven ``MMLK'' as the input, which one of the following options is the CORRECT value computed by the SDD (in the attribute $S.val$)?",
        "options_latex": {
            "A": "45",
            "B": "50",
            "C": "55",
            "D": "65"
        }
    },
    "2024_CS1_CS_Q38": {
        "topic": "Compiler Design",
        "subtopic": "Lexical analysis, parsing, syntax-directed translation",
        "difficulty_level": "Medium",
        "explaination": "Since $\\text{FIRST}(S) = \\{c, d, f\\}$ and $S \\to daT$ generates $d$, production (1) must generate $c$ and $f$. With (1) as $S \\to Rf$ where $\\text{FIRST}(R) = \\{c, \\epsilon\\}$, $\\text{FIRST}(Rf) = \\{c, f\\}$. Since $\\epsilon \\in \\text{FIRST}(T)$, production (2) must be $T \\to \\epsilon$. Production (3) as $R \\to cTR$ matches $\\text{FIRST}(R) = \\{c, \\epsilon\\}$ and $\\text{FOLLOW}(R) = \\{f\\}$, matching option (A).",
        "question_text_latex": "Consider the following grammar $G$, with $S$ as the start symbol. The grammar $G$ has three incomplete productions denoted by (1), (2), and (3).\n\\begin{align*}\nS &\\to daT \\mid (1) \\\\\nT &\\to aS \\mid bT \\mid (2) \\\\\nR &\\to (3) \\mid \\epsilon\n\\end{align*}\nThe set of terminals is $\\{a, b, c, d, f\\}$. The FIRST and FOLLOW sets of the different non-terminals are as follows:\n$$\\text{FIRST}(S) = \\{c, d, f\\}, \\quad \\text{FIRST}(T) = \\{a, b, \\epsilon\\}, \\quad \\text{FIRST}(R) = \\{c, \\epsilon\\}$$\n$$\\text{FOLLOW}(S) = \\text{FOLLOW}(T) = \\{c, f, \\$\\}, \\quad \\text{FOLLOW}(R) = \\{f\\}$$\nWhich one of the following options CORRECTLY fills in the incomplete productions?",
        "options_latex": {
            "A": "(1) $S \\to Rf$ (2) $T \\to \\epsilon$ (3) $R \\to cTR$",
            "B": "(1) $S \\to fR$ (2) $T \\to \\epsilon$ (3) $R \\to cTR$",
            "C": "(1) $S \\to fR$ (2) $T \\to cT$ (3) $R \\to cR$",
            "D": "(1) $S \\to Rf$ (2) $T \\to cT$ (3) $R \\to cR$"
        }
    },
    "2024_CS1_CS_Q39": {
        "topic": "Compiler Design",
        "subtopic": "Intermediate code generation",
        "difficulty_level": "Medium",
        "explaination": "Leaders are instructions that start a basic block: $L_1$ (first instruction), targets of conditional/unconditional jumps ($L_4, L_{11}, L_3$), and instructions immediately following jumps ($L_{10}, L_{13}, L_{15}$). This gives 7 leaders: $\\{L_1, L_4, L_{10}, L_{11}, L_3, L_{13}, L_{15}\\}$, forming 7 basic blocks. The block starting at $L_4$ contains lines $L_4$ through $L_9$, which has 6 instructions, the maximum in any block.",
        "question_text_latex": "Consider the following pseudo-code:\n\\begin{lstlisting}\nL1:  t1 = -1\nL2:  t2 = 0\nL3:  t3 = 0\nL4:  t4 = 4 * t3\nL5:  t5 = 4 * t2\nL6:  t6 = t5 * M\nL7:  t7 = t4 + t6\nL8:  t8 = a[t7]\nL9:  if t8 <= max goto L11\nL10: t1 = t8\nL11: t3 = t3 + 1\nL12: if t3 < M goto L4\nL13: t2 = t2 + 1\nL14: if t2 < N goto L3\nL15: max = t1\n\\end{lstlisting}\nWhich one of the following options CORRECTLY specifies the number of basic blocks and the number of instructions in the largest basic block, respectively?",
        "options_latex": {
            "A": "6 and 6",
            "B": "6 and 7",
            "C": "7 and 7",
            "D": "7 and 6"
        }
    },
    "2024_CS1_CS_Q40": {
        "topic": "Operating System",
        "subtopic": "Concurrency and synchronization",
        "difficulty_level": "Medium",
        "explaination": "Initially $a=b=1$. Let statements be $T_1: [S_1: a=a+1, S_2: b=b+1]$ and $T_2: [S_3: b=2b, S_4: a=2a]$. Executing $T_1$ then $T_2$ yields $a=2, b=2 \\to b=4, a=4 \\implies (4, 4)$. Executing $T_2$ then $T_1$ yields $b=2, a=2 \\to a=3, b=3 \\implies (3, 3)$. Executing $S_1, S_3, S_4, S_2$ yields $a=2 \\to b=2 \\to a=4 \\to b=3 \\implies (4, 3)$. No valid interleaving can produce $(a=3, b=4)$.",
        "question_text_latex": "Consider the following two threads T1 and T2 that update two shared variables `a` and `b`. Assume that initially $a = b = 1$. Though context switching between threads can happen at any time, each statement of T1 or T2 is executed atomically without interruption.\n\\begin{center}\n\\begin{tabular}{p{4cm}p{4cm}}\n\\textbf{T1} & \\textbf{T2} \\\\\n\\texttt{a = a + 1;} & \\texttt{b = 2 * b;} \\\\\n\\texttt{b = b + 1;} & \\texttt{a = 2 * a;}\n\\end{tabular}\n\\end{center}\nWhich one of the following options lists all the possible combinations of values of `a` and `b` after both T1 and T2 finish execution?",
        "options_latex": {
            "A": "$(a = 4, b = 4)$; $(a = 3, b = 3)$; $(a = 4, b = 3)$",
            "B": "$(a = 3, b = 4)$; $(a = 4, b = 3)$; $(a = 3, b = 3)$",
            "C": "$(a = 4, b = 4)$; $(a = 4, b = 3)$; $(a = 3, b = 4)$",
            "D": "$(a = 2, b = 2)$; $(a = 2, b = 3)$; $(a = 3, b = 4)$"
        }
    },
    "2024_CS1_CS_Q41": {
        "topic": "Programming and Data Structures",
        "subtopic": "Trees, binary search trees, binary heaps",
        "difficulty_level": "Medium",
        "explaination": "Applying standard bottom-up max-heap construction (Floyd's algorithm) to $[82, 101, 90, 11, 111, 75, 33, 131, 44, 93]$ of length 10: non-leaf nodes are heapified from index 5 down to 1. The maximum element 131 bubbles up to index 1 (root), its left child becomes 111 (index 2), and right child becomes 90 (index 3).",
        "question_text_latex": "An array $[82, 101, 90, 11, 111, 75, 33, 131, 44, 93]$ is heapified. Which one of the following options represents the first three elements in the heapified array?",
        "options_latex": {
            "A": "82, 90, 101",
            "B": "82, 11, 93",
            "C": "131, 11, 93",
            "D": "131, 111, 90"
        }
    },
    "2024_CS1_CS_Q42": {
        "topic": "Algorithms",
        "subtopic": "Asymptotic worst case time and space complexity",
        "difficulty_level": "Medium",
        "explaination": "Dividing $T(n) = \\sqrt{n} T(\\sqrt{n}) + n$ by $n$ gives $\\frac{T(n)}{n} = \\frac{T(\\sqrt{n})}{\\sqrt{n}} + 1$. Defining $S(n) = \\frac{T(n)}{n}$ yields $S(n) = S(\\sqrt{n}) + 1$. Substituting $n = 2^{2^k}$ gives $S(2^{2^k}) = S(2^{2^{k-1}}) + 1 = \\Theta(k) = \\Theta(\\log \\log n)$. Therefore, $T(n) = n S(n) = \\Theta(n \\log \\log n)$.",
        "question_text_latex": "Consider the following recurrence relation:\n\\[ T(n) = \\begin{cases} \\sqrt{n} T(\\sqrt{n}) + n & \\text{for } n > 1, \\\\ 1 & \\text{for } n = 1. \\end{cases} \\]\nWhich one of the following options is CORRECT?",
        "options_latex": {
            "A": "$T(n) = \\Theta(n \\log \\log n)$",
            "B": "$T(n) = \\Theta(n \\log n)$",
            "C": "$T(n) = \\Theta(n^2 \\log n)$",
            "D": "$T(n) = \\Theta(n^2 \\log \\log n)$"
        }
    },
    "2024_CS1_CS_Q43": {
        "topic": "Programming and Data Structures",
        "subtopic": "Trees, binary search trees, binary heaps",
        "difficulty_level": "Medium",
        "explaination": "In a binary min-heap, every parent is strictly smaller than its children, so the maximum element cannot be an internal node and must reside at one of the leaf nodes. In a complete binary tree of $n = 105$ nodes, the number of leaf nodes is $\\lceil n/2 \\rceil = \\lceil 105/2 \\rceil = 53$. Hence, there are 53 possible index locations for the maximum element.",
        "question_text_latex": "Consider a binary min-heap containing 105 distinct elements. Let $k$ be the index (in the underlying array) of the maximum element stored in the heap. The number of possible values of $k$ is",
        "options_latex": {
            "A": "53",
            "B": "52",
            "C": "27",
            "D": "1"
        }
    },
    "2024_CS1_CS_Q44": {
        "topic": "Databases",
        "subtopic": "Integrity constraints, normal forms",
        "difficulty_level": "Medium",
        "explaination": "By Armstrong's decomposition axiom, $(X, Y) \\to (Z, W)$ implies $(X, Y) \\to Z$ (B is TRUE). By Armstrong's transitivity axiom, $X \\to Y$ and $Y \\to Z$ implies $X \\to Z$ (D is TRUE). By pseudotransitivity, $(X, Y) \\to Z$ and $W \\to Y$ implies $(X, W) \\to Z$ (C is TRUE). Decomposing the left-hand side determinant is invalid in general (A is FALSE).",
        "question_text_latex": "The symbol $\\to$ indicates functional dependency in the context of a relational database. Which of the following options is/are TRUE?",
        "options_latex": {
            "A": "$(X, Y) \\to (Z, W)$ implies $X \\to (Z, W)$",
            "B": "$(X, Y) \\to (Z, W)$ implies $(X, Y) \\to Z$",
            "C": "$((X, Y) \\to Z \\text{ and } W \\to Y)$ implies $(X, W) \\to Z$",
            "D": "$(X \\to Y \\text{ and } Y \\to Z)$ implies $X \\to Z$"
        }
    },
    "2024_CS1_CS_Q45": {
        "topic": "Algorithms",
        "subtopic": "Graph traversals, minimum spanning trees, shortest paths",
        "difficulty_level": "Hard",
        "explaination": "In a BFS tree $T$, any edge $(u, w)$ in $G$ must connect vertices whose BFS levels differ by at most 1 (i.e., $\\text{level}(w) \\le \\text{level}(u) + 1$). A forward-edge in a DFS tree goes from ancestor $u$ to descendant $w$ with $\\text{level}(w) \\ge \\text{level}(u) + 2$. If such an edge existed in $G$, BFS would explore $w$ directly from $u$ at depth $\\text{level}(u) + 1$, contradicting the structure of $T$. Hence, no forward-edges can exist in $G$ with respect to $T$ (C is TRUE).",
        "question_text_latex": "Let $G$ be a directed graph and $T$ a depth first search (DFS) spanning tree in $G$ that is rooted at a vertex $v$. Suppose $T$ is also a breadth first search (BFS) tree in $G$, rooted at $v$. Which of the following statements is/are TRUE for every such graph $G$ and tree $T$?",
        "options_latex": {
            "A": "There are no back-edges in $G$ with respect to the tree $T$",
            "B": "There are no cross-edges in $G$ with respect to the tree $T$",
            "C": "There are no forward-edges in $G$ with respect to the tree $T$",
            "D": "The only edges in $G$ are the edges in $T$"
        }
    },
    "2024_CS1_CS_Q46": {
        "topic": "Databases",
        "subtopic": "Transactions and concurrency control",
        "difficulty_level": "Medium",
        "explaination": "Examining data item conflicts: on item $y$, $w_3(y)$ in $T_3$ precedes both $r_2(y)$ and $w_2(y)$ in $T_2$, creating a precedence conflict edge $T_3 \\to T_2$. Transaction $T_1$ only accesses $z$ and has no conflicting operations with $T_2$ or $T_3$. Any serial schedule preserving $T_3$ before $T_2$ is conflict equivalent to $S$, namely $T_1 T_3 T_2$, $T_3 T_1 T_2$, and $T_3 T_2 T_1$.",
        "question_text_latex": "Consider the following read-write schedule $S$ over three transactions $T_1, T_2$, and $T_3$, where the subscripts in the schedule indicate transaction IDs:\n\\[ S: r_1(z); w_1(z); r_2(x); r_3(y); w_3(y); r_2(y); w_2(x); w_2(y); \\]\nWhich of the following transaction schedules is/are conflict equivalent to $S$?",
        "options_latex": {
            "A": "$T_1 T_2 T_3$",
            "B": "$T_1 T_3 T_2$",
            "C": "$T_3 T_2 T_1$",
            "D": "$T_3 T_1 T_2$"
        }
    },
    "2024_CS1_CS_Q47": {
        "topic": "Digital Logic",
        "subtopic": "Minimization",
        "difficulty_level": "Easy",
        "explaination": "The maxterm representation is the product of maxterms not in the minterm list: $\\prod(0, 1, 2, 4)$ (A is TRUE). Grouping minterms $\\Sigma(3, 5, 6, 7)$ on a 3-variable K-map: pairs are $(3, 7) \\implies YZ$, $(5, 7) \\implies XZ$, and $(6, 7) \\implies XY$, giving minimal SOP $F(X, Y, Z) = XY + YZ + XZ$ (B is TRUE).",
        "question_text_latex": "Consider a Boolean expression given by $F(X, Y, Z) = \\sum(3, 5, 6, 7)$. Which of the following statements is/are CORRECT?",
        "options_latex": {
            "A": "$F(X, Y, Z) = \\prod(0, 1, 2, 4)$",
            "B": "$F(X, Y, Z) = XY + YZ + XZ$",
            "C": "$F(X, Y, Z)$ is independent of input $Y$",
            "D": "$F(X, Y, Z)$ is independent of input $X$"
        }
    },
    "2024_CS1_CS_Q48": {
        "topic": "Programming and Data Structures",
        "subtopic": "Programming in C",
        "difficulty_level": "Medium",
        "explaination": "In each loop iteration, $x_{k+1} = 2x_k + y$. Solving this linear recurrence yields $x_y = 2^y x_0 + y(2^y - 1) = 2^y(x_0 + y) - y$. For $x=20, y=20$: $x_{20} = 2^{20}(40) - 20 > 2^{20}$ (B is TRUE). For $x=10, y=20$: $x_{20} = 2^{20}(30) - 20 > 2^{20}$ (D is TRUE). For $y=10, x=20$: $x_{10} = 2^{10}(30) - 10 = 30710 > 2^{10}$, so (A) and (C) are false.",
        "question_text_latex": "Consider the following C function definition:\n\\begin{lstlisting}[language=C]\nint f(int x, int y) {\n    for (int i = 0; i < y; i++) {\n        x = x + x + y;\n    }\n    return x;\n}\n\\end{lstlisting}\nWhich of the following statements is/are TRUE about the above function?",
        "options_latex": {
            "A": "If the inputs are $x=20, y=10$, then the return value is greater than $2^{20}$",
            "B": "If the inputs are $x=20, y=20$, then the return value is greater than $2^{20}$",
            "C": "If the inputs are $x=20, y=10$, then the return value is less than $2^{10}$",
            "D": "If the inputs are $x=10, y=20$, then the return value is greater than $2^{20}$"
        }
    },
    "2024_CS1_CS_Q49": {
        "topic": "Linear Algebra",
        "subtopic": "System of linear equations",
        "difficulty_level": "Medium",
        "explaination": "The solution space of the homogeneous system $Ax = 0$ is the null space of $A$, whose dimension is $\\text{nullity}(A) = m - \\text{rank}(A)$. Since $\\text{rank}(A) \\le n$, we have $\\text{nullity}(A) \\ge m - n$. This guarantees the existence of at least $m - n$ linearly independent solutions (A is TRUE). The nullity can exceed $m-n$ when $\\text{rank}(A) < n$, so (B) is not universally true.",
        "question_text_latex": "Let $A$ be any $n \\times m$ matrix, where $m > n$. Which of the following statements is/are TRUE about the system of linear equations $Ax = 0$?",
        "options_latex": {
            "A": "There exist at least $m-n$ linearly independent solutions to this system",
            "B": "There exist $m-n$ linearly independent vectors such that every solution is a linear combination of these vectors",
            "C": "There exists a non-zero solution in which at least $m-n$ variables are 0",
            "D": "There exists a solution in which at least $n$ variables are non-zero"
        }
    },
    "2024_CS1_CS_Q50": {
        "topic": "Theory of Computation",
        "subtopic": "Regular expressions and finite automata",
        "difficulty_level": "Medium",
        "explaination": "States $p$ and $q$ are distinguishable if there exists a string $w$ such that exactly one of $\\delta(p, w)$ or $\\delta(q, w)$ is an accepting state. In DFA $M$, states 3 and 4 have identical transition behavior and both are non-accepting, making them equivalent/indistinguishable, so claiming they are distinguishable is FALSE (B is FALSE). Similarly, states 2 and 5 are equivalent, so claiming they are distinguishable is FALSE (C is FALSE).",
        "question_text_latex": "Consider the 5-state DFA $M$ accepting the language $L(M) \\subset (0 + 1)^*$ shown below. For any string $w \\in (0 + 1)^*$ let $n_0(w)$ be the number of 0's in $w$ and $n_1(w)$ be the number of 1's in $w$.\nWhich of the following statements is/are FALSE?",
        "options_latex": {
            "A": "States 2 and 4 are distinguishable in $M$",
            "B": "States 3 and 4 are distinguishable in $M$",
            "C": "States 2 and 5 are distinguishable in $M$",
            "D": "Any string $w$ with $n_0(w) = n_1(w)$ is in $L(M)$"
        }
    },
    "2024_CS1_CS_Q51": {
        "topic": "Discrete Mathematics",
        "subtopic": "Graphs: connectivity, matching, colouring",
        "difficulty_level": "Medium",
        "explaination": "A proper $k$-coloring partitions the $n$ vertices into $k$ independent sets. By the Pigeonhole Principle, at least one of these independent sets has size $\\ge \\lceil n/k \\rceil \\ge n/k$ (B is TRUE). In addition, every pair of color classes must have at least one edge between them (otherwise those two colors could be merged, yielding a $(k-1)$-coloring), requiring at least $\\binom{k}{2} = \\frac{k(k-1)}{2}$ edges (C is TRUE).",
        "question_text_latex": "The chromatic number of a graph is the minimum number of colours used in a proper colouring of the graph. Let $G$ be any graph with $n$ vertices and chromatic number $k$. Which of the following statements is/are always TRUE?",
        "options_latex": {
            "A": "$G$ contains a complete subgraph with $k$ vertices",
            "B": "$G$ contains an independent set of size at least $n/k$",
            "C": "$G$ contains at least $k(k-1)/2$ edges",
            "D": "$G$ contains a vertex of degree at least $k$"
        }
    },
    "2024_CS1_CS_Q52": {
        "topic": "Discrete Mathematics",
        "subtopic": "Monoids, Groups",
        "difficulty_level": "Medium",
        "explaination": "For $\\square$: $a \\square b = ab$, which is associative since $(ab)c = a(bc)$ (B is TRUE). Distributivity of $\\square$ over $\\diamond$: $a \\square (b \\diamond c) = a(b + 2c) = ab + 2ac$. Comparing with $(a \\square b) \\diamond (a \\square c) = (ab) \\diamond (ac) = ab + 2(ac) = ab + 2ac$; both sides match identically, so $\\square$ distributes over $\\diamond$ (D is TRUE). For $\\diamond$: $(a \\diamond b) \\diamond c = a + 2b + 2c \\neq a + 2b + 4c = a \\diamond (b \\diamond c)$, so $\\diamond$ is not associative.",
        "question_text_latex": "Consider the operators $\\diamond$ and $\\square$ defined by $a \\diamond b = a + 2b$, $a \\square b = ab$, for positive integers. Which of the following statements is/are TRUE?",
        "options_latex": {
            "A": "Operator $\\diamond$ obeys the associative law",
            "B": "Operator $\\square$ obeys the associative law",
            "C": "Operator $\\diamond$ over the operator $\\square$ obeys the distributive law",
            "D": "Operator $\\square$ over the operator $\\diamond$ obeys the distributive law"
        }
    },
    "2024_CS1_CS_Q53": {
        "topic": "Computer Organization and Architecture",
        "subtopic": "Memory hierarchy: cache, main memory and secondary storage",
        "difficulty_level": "Medium",
        "explaination": "In a write-through cache (WTC), main memory is updated simultaneously on every cache write, meaning cache lines are never dirty and no eviction ever triggers a write-back to memory (B is TRUE). In a write-back cache (WBC), when a clean block receives a write hit, its dirty bit is set from 0 to 1 to indicate modification (C is TRUE).",
        "question_text_latex": "Consider two set-associative cache memory architectures: WBC, which uses the write back policy, and WTC, which uses the write through policy. Both of them use the LRU (Least Recently Used) block replacement policy. The cache memory is connected to the main memory. Which of the following statements is/are TRUE?",
        "options_latex": {
            "A": "A read miss in WBC never evicts a dirty block",
            "B": "A read miss in WTC never triggers a write back operation of a cache block to main memory",
            "C": "A write hit in WBC can modify the value of the dirty bit of a cache block",
            "D": "A write miss in WTC always writes the victim cache block to main memory before loading the missed block to the cache"
        }
    },
    "2024_CS1_CS_Q54": {
        "topic": "Computer Organization and Architecture",
        "subtopic": "Memory hierarchy: cache, main memory and secondary storage",
        "difficulty_level": "Easy",
        "explaination": "Disk capacity $= 512\\text{ GB} = 512 \\times 2^{30}\\text{ bytes} = 2^{39}$ bytes. One cylinder comprises 32 surfaces $\\times 4096$ sectors/track $\\times 1024$ bytes/sector $= 2^5 \\times 2^{12} \\times 2^{10} = 2^{27}$ bytes. Number of cylinders $= \\frac{2^{39}}{2^{27}} = 2^{12} = 4096$.",
        "question_text_latex": "Consider a 512 GB hard disk with 32 storage surfaces. There are 4096 sectors per track and each sector holds 1024 bytes of data. The number of cylinders in the hard disk is \\_\\_\\_\\_\\_\\_\\_\\_\\_\\. (Answer in integer)",
        "options_latex": None
    },
    "2024_CS1_CS_Q55": {
        "topic": "Computer Organization and Architecture",
        "subtopic": "Instruction pipelining, pipeline hazards",
        "difficulty_level": "Medium",
        "explaination": "Baseline runtime is $100\\text{ ns}$, with $90\\text{ ns}$ parallelizable and $10\\text{ ns}$ serial. On $p$ cores, the parallel portion takes $\\frac{90}{p}\\text{ ns}$ with core overhead of $10(p-1)\\text{ ns}$. Total execution time $T(p) = 10 + \\frac{90}{p} + 10(p-1) = \\frac{90}{p} + 10p$. Evaluating: $T(1) = 100\\text{ ns}$, $T(2) = 65\\text{ ns}$, $T(3) = 60\\text{ ns}$, $T(4) = 62.5\\text{ ns}$. The time is minimized at $p = 3$ cores.",
        "question_text_latex": "The baseline execution time of a program on a 2 GHz single core machine is 100 nanoseconds (ns). The code corresponding to 90\\% of the execution time can be fully parallelized. The overhead for using an additional core is 10 ns when running on a multicore system. Assume that all cores in the multicore system run their share of the parallelized code for an equal amount of time.\nThe number of cores that minimize the execution time of the program is \\_\\_\\_\\_\\_\\_\\_\\_\\. (Answer in integer)",
        "options_latex": None
    },
    "2024_CS1_CS_Q56": {
        "topic": "Computer Organization and Architecture",
        "subtopic": "Memory hierarchy: cache, main memory and secondary storage",
        "difficulty_level": "Medium",
        "explaination": "Total CPI is given by $\\text{CPI} = \\text{CPI}_{\\text{ideal}} + (\\text{I-miss rate} \\times \\text{penalty}) + (\\text{Data-instruction fraction} \\times \\text{D-miss rate} \\times \\text{penalty}) = 2 + (0.02 \\times 100) + (0.25 \\times 0.08 \\times 100) = 2 + 2 + 2 = 6$. For a perfect cache with no misses, $\\text{CPI}_{\\text{perfect}} = \\text{CPI}_{\\text{ideal}} = 2$. Speedup $= \\frac{6}{2} = 3.00$.",
        "question_text_latex": "A given program has 25\\% load/store instructions. Suppose the ideal CPI (cycles per instruction) without any memory stalls is 2. The program exhibits 2\\% miss rate on instruction cache and 8\\% miss rate on data cache. The miss penalty is 100 cycles.\nThe speedup (rounded off to two decimal places) achieved with a perfect cache (i.e., with NO data or instruction cache misses) is \\_\\_\\_\\_\\_\\_\\_\\_\\_\\. (Answer in numeric format)",
        "options_latex": None
    },
    "2024_CS1_CS_Q57": {
        "topic": "Operating System",
        "subtopic": "System calls, processes, threads, inter-process communication",
        "difficulty_level": "Medium",
        "explaination": "Initially 1 process with $x=3$. Iteration 1 ($x=3$): `fork()` creates 1 child (total 2 processes); both print \"hello\" (2 prints) and decrement $x$ to 2. Iteration 2 ($x=2$): each of the 2 processes forks (total 4 processes); all 4 print \"hello\" (4 prints) and decrement $x$ to 1. Iteration 3 ($x=1$): each of the 4 processes forks (total 8 processes); all 8 print \"hello\" (8 prints) and decrement $x$ to 0, whereupon the loop ends. Total prints $= 2 + 4 + 8 = 14$.",
        "question_text_latex": "Consider the following code snippet using the `fork()` and `wait()` system calls. Assume that the code compiles and runs correctly, and that the system calls run successfully without any errors.\n\\begin{lstlisting}[language=C]\nint x = 3;\nwhile(x > 0) {\n    fork();\n    printf(\"hello\");\n    wait(NULL);\n    x--;\n}\n\\end{lstlisting}\nThe total number of times the `printf` statement is executed is \\_\\_\\_\\_\\_\\_\\_\\. (Answer in integer)",
        "options_latex": None
    },
    "2024_CS1_CS_Q58": {
        "topic": "Computer Networks",
        "subtopic": "Routing protocols: shortest path, flooding, distance vector and link state routing",
        "difficulty_level": "Medium",
        "explaination": "Using longest prefix match for each host address: 10.1.1.16 matches /24 (R1); 10.1.1.72 matches /24 and 10.1.1.64/26 (R3); 10.1.1.132 matches /24 and 10.1.1.128/25 (R2); 10.1.1.191 matches /24 and 10.1.1.128/25 (R2); 10.1.1.205 matches /24, /25, and 10.1.1.192/26 (R4). Thus, 2 hosts (10.1.1.132 and 10.1.1.191) match router R2. Total packets forwarded via R2 $= 2 \\times 20 = 40$.",
        "question_text_latex": "Consider the entries shown below in the forwarding table of an IP router. Each entry consists of an IP prefix and the corresponding next hop router for packets whose destination IP address matches the prefix. The notation ``/N'' in a prefix indicates a subnet mask with the most significant $N$ bits set to 1.\n\\begin{center}\n\\begin{tabular}{|l|c|}\n\\hline\n\\textbf{Prefix} & \\textbf{Next hop router} \\\\\n\\hline\n10.1.1.0/24 & R1 \\\\\n10.1.1.128/25 & R2 \\\\\n10.1.1.64/26 & R3 \\\\\n10.1.1.192/26 & R4 \\\\\n\\hline\n\\end{tabular}\n\\end{center}\nThis router forwards 20 packets each to 5 hosts. The IP addresses of the hosts are 10.1.1.16, 10.1.1.72, 10.1.1.132, 10.1.1.191, and 10.1.1.205. The number of packets forwarded via the next hop router R2 is \\_\\_\\_\\_\\_\\_\\_\\. (Answer in integer)",
        "options_latex": None
    },
    "2024_CS1_CS_Q59": {
        "topic": "Theory of Computation",
        "subtopic": "Context-free grammars and push-down automata",
        "difficulty_level": "Medium",
        "explaination": "In a Chomsky Normal Form (CNF) grammar, every production is either $A \\to BC$ or $A \\to a$. Deriving a string of length $n$ requires $n-1$ non-terminal splitting steps ($A \\to BC$) followed by $n$ terminal production steps ($A \\to a$), totaling $2n-1$ steps. For $w = a^{30}b^{30}c^{30}$, the length is $n = 90$, so the number of derivation steps is $2(90) - 1 = 179$.",
        "question_text_latex": "Let $G = (V, \\Sigma, S, P)$ be a context-free grammar in Chomsky Normal Form with $\\Sigma = \\{a, b, c\\}$ and $V$ containing 10 variable symbols including the start symbol $S$. The string $w = a^{30}b^{30}c^{30}$ is derivable from $S$. The number of steps (application of rules) in the derivation $S \\Rightarrow^* w$ is \\_\\_\\_\\_\\_\\_\\_\\_\\_\\. (Answer in integer)",
        "options_latex": None
    },
    "2024_CS1_CS_Q60": {
        "topic": "Discrete Mathematics",
        "subtopic": "Graphs: connectivity, matching, colouring",
        "difficulty_level": "Easy",
        "explaination": "A DFS traversal of an undirected graph with $V$ vertices and $k$ connected components produces a spanning forest containing $k$ trees. A tree with $v_i$ vertices contains $v_i - 1$ edges, so the total number of tree edges in the forest is $\\sum (v_i - 1) = V - k$. Given $V = 100$ and $E = 40$, we have $40 = 100 - k \\implies k = 60$ connected components.",
        "question_text_latex": "The number of edges present in the forest generated by the DFS traversal of an undirected graph $G$ with 100 vertices is 40. The number of connected components in $G$ is \\_\\_\\_\\_\\_\\_\\_\\_\\_\\. (Answer in integer)",
        "options_latex": None
    },
    "2024_CS1_CS_Q61": {
        "topic": "Theory of Computation",
        "subtopic": "Regular expressions and finite automata",
        "difficulty_level": "Medium",
        "explaination": "The total number of binary strings of length $\\le 5$ is $\\sum_{i=0}^5 2^i = 1+2+4+8+16+32 = 63$. Language $L(r) = 0^* + 1^*$ contains $\\epsilon$ and $0^k, 1^k$ for each length $k \\in \\{1..5\\}$ (11 strings). Language $L(s) = 01^* + 10^*$ contains $01^{k-1}$ and $10^{k-1}$ for each length $k \\in \\{1..5\\}$. At $k=1$, $0$ and $1$ overlap with $L(r)$; for $k \\in \\{2..5\\}$, the $4 \\times 2 = 8$ strings are disjoint from $L(r)$. Thus, $|L(r) \\cup L(s)| = 11 + 8 = 19$. The number of strings in neither language is $63 - 19 = 44$.",
        "question_text_latex": "Consider the following two regular expressions over the alphabet $\\{0,1\\}$:\n\\[ r = 0^* + 1^* \\]\n\\[ s = 01^* + 10^* \\]\nThe total number of strings of length less than or equal to 5, which are neither in $r$ nor in $s$, is \\_\\_\\_\\_\\_\\_\\_\\_\\_\\. (Answer in integer)",
        "options_latex": None
    },
    "2024_CS1_CS_Q62": {
        "topic": "Operating System",
        "subtopic": "Memory management and virtual memory",
        "difficulty_level": "Easy",
        "explaination": "With page size $2\\text{ KB} = 2048\\text{ bytes}$, virtual address $2500$ has virtual page number $\\lfloor 2500 / 2048 \\rfloor = 1$ and offset $2500 \\pmod{2048} = 452$. Page 1 maps to frame 3. The physical address is $(\\text{frame } 3 \\times 2048) + \\text{offset } 452 = 6144 + 452 = 6596$.",
        "question_text_latex": "Consider a memory management system that uses a page size of 2 KB. Assume that both the physical and virtual addresses start from 0. Assume that the pages 0, 1, 2, and 3 are stored in the page frames 1, 3, 2, and 0, respectively. The physical address (in decimal format) corresponding to the virtual address 2500 (in decimal format) is \\_\\_\\_\\_\\_\\_\\_\\_\\_\\. (Answer in integer)",
        "options_latex": None
    },
    "2024_CS1_CS_Q63": {
        "topic": "Probability and Statistics",
        "subtopic": "Conditional probability and Bayes theorem",
        "difficulty_level": "Easy",
        "explaination": "Let $R_1, R_2$ be the events of drawing red balls on the first and second draws without replacement. The conditional probability that both are red given the first is red is $P(R_1 \\cap R_2 \\mid R_1) = P(R_2 \\mid R_1)$. Given that 1 red ball is already drawn, 9 red balls remain out of $9 + 15 = 24$ total balls, so $P(R_2 \\mid R_1) = \\frac{9}{24} = \\frac{3}{8} = 0.375$.",
        "question_text_latex": "A bag contains 10 red balls and 15 blue balls. Two balls are drawn randomly without replacement. Given that the first ball drawn is red, the probability (rounded off to 3 decimal places) that both balls drawn are red is \\_\\_\\_\\_\\_\\_\\_\\_\\_\\. (Answer in numeric format)",
        "options_latex": None
    },
    "2024_CS1_CS_Q65": {
        "topic": "Computer Networks",
        "subtopic": "Fragmentation and IP addressing, IPv4, CIDR notation",
        "difficulty_level": "Medium",
        "explaination": "The datagram has 20 bytes IP header and 1400 bytes data. Link 1 has $\\text{MTU} = 542$ bytes (max data per fragment is $\\lfloor (542-20)/8 \\rfloor \\times 8 = 520$ bytes), producing 3 fragments with data sizes 520, 520, and 360 bytes. Link 2 has $\\text{MTU} = 360$ bytes (max data is $\\lfloor (360-20)/8 \\rfloor \\times 8 = 336$ bytes). At router Q, fragment 1 (520 bytes) is fragmented into 2 ($336 + 184$), fragment 2 (520 bytes) is fragmented into 2 ($336 + 184$), and fragment 3 (360 bytes) is fragmented into 2 ($336 + 24$). Total fragments delivered at the receiver $= 2 + 2 + 2 = 6$.",
        "question_text_latex": "Consider sending an IP datagram of size 1420 bytes (including 20 bytes of IP header) from a sender to a receiver over a path of two links with a router between them. The first link (sender to router) has an MTU (Maximum Transmission Unit) size of 542 bytes, while the second link (router to receiver) has an MTU size of 360 bytes. The number of fragments that would be delivered at the receiver is \\_\\_\\_\\_\\_\\_\\_\\_\\. (Answer in integer)",
        "options_latex": None
    }
}

def main():
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    paper_dir = os.path.join(root_dir, "dataset", "papers", "2024_CS1")

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

    print(f"Enriched {updated_count} questions in 2024_CS1 paper files successfully.")

if __name__ == "__main__":
    main()

