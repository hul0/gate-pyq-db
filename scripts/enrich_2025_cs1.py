#!/usr/bin/env python3
"""
enrich_2025_cs1.py

Fills the AI metadata fields for 2025 CS1 questions based on syllabus/cs_2026_syllabus.json:
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
    "2025_CS1_GA_Q01": {
        "topic": "Verbal Aptitude",
        "subtopic": "Basic English grammar: tenses, articles, adjectives, prepositions, conjunctions, verb-noun agreement",
        "difficulty_level": "Easy",
        "explaination": "'Younger' begins with a consonant sound (/j/), requiring the indefinite article 'a'. 'University' also begins with a consonant sound (/juː/), taking 'a'. 'Honorable' has a silent 'h' and begins with a vowel sound (/ɒ/), requiring 'an'. Hence, the sequence is a; a; an.",
        "question_text_latex": "Ravi had \\_\\_\\_\\_\\_\\_ younger brother who taught at \\_\\_\\_\\_\\_\\_ university. He was widely regarded as \\_\\_\\_\\_\\_\\_ honorable man.\nSelect the option with the correct sequence of articles to fill in the blanks.",
        "options_latex": {
            "A": "a; a; an",
            "B": "the; an; a",
            "C": "a; an; a",
            "D": "an; an; a"
        }
    },
    "2025_CS1_GA_Q02": {
        "topic": "Verbal Aptitude",
        "subtopic": "Vocabulary: words, idioms, and phrases in context",
        "difficulty_level": "Easy",
        "explaination": "'Myopic' literally means nearsighted, and metaphorically refers to lacking foresight or being shortsighted by focusing only on immediate considerations rather than long-term outcomes.",
        "question_text_latex": "The CEO’s decision to downsize the workforce was considered myopic because it sacrificed long-term stability to accommodate short-term gains.\nSelect the most appropriate option that can replace the word ``myopic'' without changing the meaning of the sentence.",
        "options_latex": {
            "A": "visionary",
            "B": "shortsighted",
            "C": "progressive",
            "D": "innovative"
        }
    },
    "2025_CS1_GA_Q03": {
        "topic": "Quantitative Aptitude",
        "subtopic": "Elementary statistics and probability",
        "difficulty_level": "Easy",
        "explaination": "Let $n$ be the number of students. The total increase in marks after correction is $42 - 24 = 18$. The increase in average is $31.4 - 30.8 = 0.6$. Therefore, $0.6 \\times n = 18$, giving $n = \\frac{18}{0.6} = 30$ students.",
        "question_text_latex": "The average marks obtained by a class in an examination were calculated as 30.8. However, while checking the marks entered, the teacher found that the marks of one student were entered incorrectly as 24 instead of 42. After correcting the marks, the average becomes 31.4. How many students does the class have?",
        "options_latex": {
            "A": "25",
            "B": "28",
            "C": "30",
            "D": "32"
        }
    },
    "2025_CS1_GA_Q04": {
        "topic": "Analytical Aptitude",
        "subtopic": "Logic: deduction and induction",
        "difficulty_level": "Easy",
        "explaination": "Since R is the mother of Q and S is the daughter of Q, R is definitely the grandmother of S (statement 1 is true). P is the brother of Q, so P is the maternal/paternal uncle of Q's children S and T (statement 2 is true). The genders and number of other children of R and Q are not specified, so (3) and (4) cannot be established.",
        "question_text_latex": "Consider the relationships among P, Q, R, S, and T:\n\\begin{itemize}\n\\item P is the brother of Q.\n\\item S is the daughter of Q.\n\\item T is the sister of S.\n\\item R is the mother of Q.\n\\end{itemize}\nThe following statements are made based on the relationships given above:\n(1) R is the grandmother of S.\n(2) P is the uncle of S and T.\n(3) R has only one son.\n(4) Q has only one daughter.\nWhich one of the following options is correct?",
        "options_latex": {
            "A": "Both (1) and (2) are true.",
            "B": "Both (1) and (3) are true.",
            "C": "Only (3) is true.",
            "D": "Only (4) is true."
        }
    },

    # ==================== GA 2-MARK ====================
    "2025_CS1_GA_Q06": {
        "topic": "Verbal Aptitude",
        "subtopic": "Reading and comprehension",
        "difficulty_level": "Easy",
        "explaination": "The passage explicitly states: 'the pocket-knife, for instance the type of all human tools, the infant of the sword.' Statement C directly reflects this verbatim description.",
        "question_text_latex": "``I put the brown paper in my pocket along with the chalks, and possibly other things. I suppose every one must have reflected how primeval and how poetical are the things that one carries in one's pocket: the pocket-knife, for instance the type of all human tools, the infant of the sword. Once I planned to write a book of poems entirely about the things in my pocket. But I found it would be too long: and the age of the great epics is past.''\n(From G.K. Chesterton's ``A Piece of Chalk'')\n\nBased only on the information provided in the above passage, which one of the following statements is true?",
        "options_latex": {
            "A": "The author of the passage carries a mirror in his pocket to reflect upon things.",
            "B": "The author of the passage had decided to write a poem on epics.",
            "C": "The pocket-knife is described as the infant of the sword.",
            "D": "Epics are described as too inconvenient to write."
        }
    },
    "2025_CS1_GA_Q08": {
        "topic": "Quantitative Aptitude",
        "subtopic": "Elementary statistics and probability",
        "difficulty_level": "Medium",
        "explaination": "The probability of rolling a 6 is $p = \\frac{1}{6}$, and not rolling a 6 is $q = \\frac{5}{6}$. Using the binomial distribution for $n = 3$ trials with $k = 1$ success, $P(X = 1) = \\binom{3}{1} \\left(\\frac{1}{6}\\right)^1 \\left(\\frac{5}{6}\\right)^2 = 3 \\times \\frac{1}{6} \\times \\frac{25}{36} = \\frac{75}{216}$.",
        "question_text_latex": "A fair six-faced dice, with the faces labelled `1', `2', `3', `4', `5', and `6', is rolled thrice. What is the probability of rolling `6' exactly once?",
        "options_latex": {
            "A": "$\\frac{75}{216}$",
            "B": "$\\frac{1}{6}$",
            "C": "$\\frac{1}{18}$",
            "D": "$\\frac{25}{216}$"
        }
    },
    "2025_CS1_GA_Q10": {
        "topic": "Quantitative Aptitude",
        "subtopic": "Numerical computation and estimation: ratios, percentages, powers, exponents and logarithms, permutations and combinations, series",
        "difficulty_level": "Easy",
        "explaination": "This is a multichoose problem (combination with repetition), where $r = 3$ scoops are chosen from $n = 4$ flavors. The number of ways is given by the stars and bars formula $\\binom{n + r - 1}{r} = \\binom{4 + 3 - 1}{3} = \\binom{6}{3} = \\frac{6 \\times 5 \\times 4}{3 \\times 2 \\times 1} = 20$.",
        "question_text_latex": "A shop has 4 distinct flavors of ice-cream. One can purchase any number of scoops of any flavor. The order in which the scoops are purchased is inconsequential. If one wants to purchase 3 scoops of ice-cream, in how many ways can one make that purchase?",
        "options_latex": {
            "A": "4",
            "B": "20",
            "C": "24",
            "D": "48"
        }
    },

    # ==================== CS 1-MARK ====================
    "2025_CS1_CS_Q11": {
        "topic": "Computer Organization and Architecture",
        "subtopic": "I/O interface: interrupt and DMA mode",
        "difficulty_level": "Easy",
        "explaination": "When an asynchronous interrupt arrives, the processor first finishes the execution of the current instruction (iii). Next, it saves the current program counter (and processor state) onto the stack (i). Finally, it loads the starting address of the interrupt service routine into the program counter (ii).",
        "question_text_latex": "Suppose a program is running on a non-pipelined single processor computer system. The computer is connected to an external device that can interrupt the processor asynchronously. The processor needs to execute the interrupt service routine (ISR) to serve this interrupt. The following steps (not necessarily in order) are taken by the processor when the interrupt arrives:\n\\begin{enumerate}[label=(\\roman*)]\n\\item The processor saves the content of the program counter.\n\\item The program counter is loaded with the start address of the ISR.\n\\item The processor finishes the present instruction.\n\\end{enumerate}\nWhich ONE of the following is the CORRECT sequence of steps?",
        "options_latex": {
            "A": "(iii), (i), (ii)",
            "B": "(i), (iii), (ii)",
            "C": "(i), (ii), (iii)",
            "D": "(iii), (ii), (i)"
        }
    },
    "2025_CS1_CS_Q12": {
        "topic": "Compiler Design",
        "subtopic": "Lexical analysis, parsing, syntax-directed translation",
        "difficulty_level": "Easy",
        "explaination": "The symbol table is actively used throughout all phases of the compiler, including semantic analysis, intermediate code generation, code optimization, and target code generation for type checking, memory allocation, and address resolution. Thus, claiming it is not required after parsing is false.",
        "question_text_latex": "Which ONE of the following statements is FALSE regarding the symbol table?",
        "options_latex": {
            "A": "Symbol table is responsible for keeping track of the scope of variables.",
            "B": "Symbol table can be implemented using a binary search tree.",
            "C": "Symbol table is not required after the parsing phase.",
            "D": "Symbol table is created during the lexical analysis phase."
        }
    },
    "2025_CS1_CS_Q13": {
        "topic": "Compiler Design",
        "subtopic": "Data flow analyses: constant propagation, liveness analysis, common sub expression elimination",
        "difficulty_level": "Easy",
        "explaination": "Live variable analysis determines whether the value in a variable could be read along some execution path before being redefined. This information is directly used in register allocation and assignment to construct interference graphs and allocate registers efficiently.",
        "question_text_latex": "Which ONE of the following techniques used in compiler code optimization uses live variable analysis?",
        "options_latex": {
            "A": "Run-time function call management",
            "B": "Register assignment to variables",
            "C": "Strength reduction",
            "D": "Constant folding"
        }
    },
    "2025_CS1_CS_Q14": {
        "topic": "Operating System",
        "subtopic": "Memory management and virtual memory",
        "difficulty_level": "Medium",
        "explaination": "With a page size of $2048 = 2^{11}$ bytes, the page offset requires 11 bits. The 32-bit logical address is split into page number and page offset, so the page number has $32 - 11 = 21$ bits. Hence, the page table contains at most $2^{21}$ entries.",
        "question_text_latex": "Consider a demand paging memory management system with 32-bit logical address, 20-bit physical address, and page size of 2048 bytes. Assuming that the memory is byte addressable, what is the maximum number of entries in the page table?",
        "options_latex": {
            "A": "$2^{21}$",
            "B": "$2^{20}$",
            "C": "$2^{22}$",
            "D": "$2^{24}$"
        }
    },
    "2025_CS1_CS_Q15": {
        "topic": "Databases",
        "subtopic": "Transactions and concurrency control",
        "difficulty_level": "Medium",
        "explaination": "Transaction $T_1$ writes to item $Y$ ($W_1(Y)$). Subsequently, both $T_2$ and $T_3$ read uncommitted data item $Y$ ($R_2(Y)$ and $R_3(Y)$) written by $T_1$ before $T_1$ commits. When $T_1$ aborts, a cascading rollback is triggered, requiring both $T_2$ and $T_3$ to be rolled back.",
        "question_text_latex": "A schedule of three database transactions $T_1, T_2$, and $T_3$ is shown. $R_i(A)$ and $W_i(A)$ denote read and write of data item $A$ by transaction $T_i$, $i= 1,2,3$. The transaction $T_1$ aborts at the end. Which other transaction(s) will be required to be rolled back?\n\\[ R_1(X) \\; W_1(Y) \\; R_2(X) \\; R_2(Y) \\; R_3(Y) \\; ABORT(T_1) \\]",
        "options_latex": {
            "A": "Only $T_2$",
            "B": "Only $T_3$",
            "C": "Both $T_2$ and $T_3$",
            "D": "Neither $T_2$ nor $T_3$"
        }
    },
    "2025_CS1_CS_Q16": {
        "topic": "Computer Networks",
        "subtopic": "Concept of layering: OSI and TCP/IP Protocol Stacks",
        "difficulty_level": "Easy",
        "explaination": "The Network layer is responsible for packet routing across networks ((a)-(I)). The Transport layer provides end-to-end communication services between hosts ((b)-(III)). The Data Link layer handles framing, flow control, and physical error handling ((c)-(II)).",
        "question_text_latex": "Identify the ONE CORRECT matching between the OSI layers and their corresponding functionalities as shown.\n\n\\begin{tabular}{ll}\n\\textbf{OSI Layers} & \\textbf{Functionalities} \\\\\n(a) Network layer & (I) Packet routing \\\\\n(b) Transport layer & (II) Framing and error handling \\\\\n(c) Datalink layer & (III) Host to host communication\n\\end{tabular}",
        "options_latex": {
            "A": "(a)-(I), (b)-(II), (c)-(III)",
            "B": "(a)-(I), (b)-(III), (c)-(II)",
            "C": "(a)-(II), (b)-(I), (c)-(III)",
            "D": "(a)-(III), (b)-(II), (c)-(I)"
        }
    },
    "2025_CS1_CS_Q17": {
        "topic": "Discrete Mathematics",
        "subtopic": "Sets, relations, functions, partial orders and lattices",
        "difficulty_level": "Medium",
        "explaination": "If the composition $f \\circ g: A \\to C$ is surjective, $f$ must be surjective, but $g$ is not required to be either injective or surjective. For example, if $C$ is a singleton $\\{c\\}$ and $B = \\{b_1, b_2\\}$, $g$ can map all of $A$ to $b_1$ where $f(b_1) = c$, leaving $b_2$ uncovered (not onto) and having many collisions (not one-to-one).",
        "question_text_latex": "$g(\\cdot)$ is a function from $A$ to $B$, $f(\\cdot)$ is a function from $B$ to $C$, and their composition defined as $f(g(\\cdot))$ is a mapping from $A$ to $C$.\nIf $f(\\cdot)$ and $f(g(\\cdot))$ are onto (surjective) functions, which ONE of the following is TRUE about the function $g(\\cdot)$?",
        "options_latex": {
            "A": "$g(\\cdot)$ must be an onto (surjective) function.",
            "B": "$g(\\cdot)$ must be a one-to-one (injective) function.",
            "C": "$g(\\cdot)$ must be a bijective function, that is, both one-to-one and onto.",
            "D": "$g(\\cdot)$ is not required to be a one-to-one or onto function."
        }
    },
    "2025_CS1_CS_Q18": {
        "topic": "Algorithms",
        "subtopic": "Graph traversals, minimum spanning trees, shortest paths",
        "difficulty_level": "Easy",
        "explaination": "Since the minimum spanning tree $T$ is a subgraph of $G$ ($E(T) \\subseteq E(G)$), every path between $u$ and $v$ in $T$ is also a valid path in $G$. Thus, the shortest path distance in $G$ cannot exceed that in $T$, guaranteeing $d_1(u, v) \\le d_2(u, v)$.",
        "question_text_latex": "Let $G$ be any undirected graph with positive edge weights, and $T$ be a minimum spanning tree of $G$. For any two vertices, $u$ and $v$, let $d_1(u, v)$ and $d_2(u, v)$ be the shortest distances between $u$ and $v$ in $G$ and $T$, respectively. Which ONE of the options is CORRECT for all possible $G, T, u$ and $v$?",
        "options_latex": {
            "A": "$d_1(u, v) = d_2(u, v)$",
            "B": "$d_1(u, v) \\le d_2(u, v)$",
            "C": "$d_1(u, v) \\ge d_2(u, v)$",
            "D": "$d_1(u, v) \\ne d_2(u, v)$"
        }
    },
    "2025_CS1_CS_Q19": {
        "topic": "Theory of Computation",
        "subtopic": "Context-free grammars and push-down automata",
        "difficulty_level": "Easy",
        "explaination": "From the rules, $A$ generates $a^+$ (any $a^n$ with $n \\ge 1$) and $B$ generates $b^+$ (any $b^n$ with $n \\ge 1$). Thus, $aaB$ produces $a^2b^n$ ($n \\ge 1$), and $Abb$ produces $a^nb^2$ ($n \\ge 1$). Therefore, $L(G) = \\{a^2b^n \\mid n \\ge 1\\} \\cup \\{a^nb^2 \\mid n \\ge 1\\}$.",
        "question_text_latex": "Consider the following context-free grammar $G$, where $S, A$, and $B$ are the variables (non-terminals), $a$ and $b$ are the terminal symbols, $S$ is the start variable, and the rules of $G$ are described as:\n\\[ S \\to aaB \\mid Abb \\]\n\\[ A \\to a \\mid aA \\]\n\\[ B \\to b \\mid bB \\]\nWhich ONE of the languages $L(G)$ is accepted by $G$?",
        "options_latex": {
            "A": "$L(G) = \\{a^2b^n \\mid n \\ge 1\\} \\cup \\{a^nb^2 \\mid n \\ge 1\\}$",
            "B": "$L(G) = \\{a^nb^{2n} \\mid n \\ge 1\\} \\cup \\{a^{2n}b^n \\mid n \\ge 1\\}$",
            "C": "$L(G) = \\{a^nb^n \\mid n \\ge 1\\}$",
            "D": "$L(G) = \\{a^{2n}b^{2n} \\mid n \\ge 1\\}$"
        }
    },
    "2025_CS1_CS_Q20": {
        "topic": "Algorithms",
        "subtopic": "Asymptotic worst case time and space complexity",
        "difficulty_level": "Medium",
        "explaination": "Dividing both sides by $2^n$ yields $\\frac{T(n)}{2^n} = \\frac{T(n-1)}{2^{n-1}} + n$. Letting $S(n) = \\frac{T(n)}{2^n}$, we have $S(n) = S(n-1) + n = S(0) + \\sum_{i=1}^n i = 1 + \\frac{n(n+1)}{2} = \\Theta(n^2)$. Multiplying back gives $T(n) = \\Theta(n^2 2^n)$.",
        "question_text_latex": "Consider the following recurrence relation:\n\\[ T(n) = 2T(n-1) + n2^n \\quad \\text{for } n > 0, \\; T(0) = 1. \\]\nWhich ONE of the following options is CORRECT?",
        "options_latex": {
            "A": "$T(n) = \\Theta(n^2 2^n)$",
            "B": "$T(n) = \\Theta(n 2^n)$",
            "C": "$T(n) = \\Theta((\\log n)^2 2^n)$",
            "D": "$T(n) = \\Theta(4^n)$"
        }
    },
    "2025_CS1_CS_Q21": {
        "topic": "Databases",
        "subtopic": "File organization, indexing (e.g., B and B+ trees)",
        "difficulty_level": "Medium",
        "explaination": "With maximum key capacity of 3 keys per node, the targeted leaf node containing keys $[20, 21, 22]$ is already full. Inserting 23 causes this leaf node to overflow and split, propagating a split upward to the already-saturated root, which creates a new root node and increases tree height.",
        "question_text_latex": "Consider a $B^+$ tree with 5 nodes, in which a node can store at most 3 key values. The value 23 is now inserted in the $B^+$ tree. Which of the following option(s) is/are CORRECT?",
        "options_latex": {
            "A": "None of the nodes will split.",
            "B": "At least one node will split and redistribute.",
            "C": "The total number of nodes will remain same.",
            "D": "The height of the tree will increase."
        }
    },
    "2025_CS1_CS_Q22": {
        "topic": "Computer Networks",
        "subtopic": "Transport layer: flow control and congestion control, UDP, TCP, sockets",
        "difficulty_level": "Easy",
        "explaination": "In TCP 3-way handshaking: Packet 1 (Client to Server) sends a SYN segment with flag $[\\text{SYN}=1, \\text{ACK}=0]$; Packet 2 (Server to Client) responds with $[\\text{SYN}=1, \\text{ACK}=1]$; Packet 3 (Client to Server) completes setup with $[\\text{SYN}=0, \\text{ACK}=1]$. Hence, P1 has SYN = 1 and P2 has SYN = 1, ACK = 1.",
        "question_text_latex": "Consider the 3-way handshaking protocol for TCP connection establishment. Let the three packets exchanged during the connection establishment be denoted as P1, P2, and P3, in order. Which of the following option(s) is/are TRUE with respect to TCP header flags that are set in the packets?",
        "options_latex": {
            "A": "P3: SYN = 1, ACK = 1",
            "B": "P2: SYN = 1, ACK = 1",
            "C": "P2: SYN = 0, ACK = 1",
            "D": "P1: SYN = 1"
        }
    },
    "2025_CS1_CS_Q23": {
        "topic": "Linear Algebra",
        "subtopic": "System of linear equations",
        "difficulty_level": "Medium",
        "explaination": "The coefficient determinant is $|A| = 1 - k^2 = 0 \\implies k = \\pm 1$. For $k = 1$, equations are $x + y = 1$ and $x + y = -1$, which are inconsistent (no solution). For $k = -1$, equations are $x - y = 1$ and $-x + y = -1$, which are identical (infinitely many solutions). For all $k \\neq \\pm 1$, there is a unique solution.",
        "question_text_latex": "Consider the given system of linear equations for variables $x$ and $y$, where $k$ is a real-valued constant. Which of the following option(s) is/are CORRECT?\n\\[ x + ky = 1 \\]\n\\[ kx + y = -1 \\]",
        "options_latex": {
            "A": "There is exactly one value of $k$ for which the above system of equations has no solution.",
            "B": "There exist an infinite number of values of $k$ for which the system of equations has no solution.",
            "C": "There exists exactly one value of $k$ for which the system of equations has exactly one solution.",
            "D": "There exists exactly one value of $k$ for which the system of equations has an infinite number of solutions."
        }
    },
    "2025_CS1_CS_Q24": {
        "topic": "Digital Logic",
        "subtopic": "Boolean algebra",
        "difficulty_level": "Medium",
        "explaination": "The majority function is $X(a, b, c) = ab + bc + ca$. In (B), $X(a, b, M) = ab + bM + aM = ab + (a+b)M = ab + (a+b)(ab+bc+ca) = ab + bc + ca = X(a, b, c)$, so (B) holds. In (D), $X(a, c, c) = c$, giving $X(a, M, c) = aM + Mc + ca = (a+c)M + ac = (a+c)(ab+bc+ca) + ac = ab + bc + ca = X(a, b, c)$, so (D) holds.",
        "question_text_latex": "Let $X$ be a 3-variable Boolean function that produces output as `1' when at least two of the input variables are `1'. Which of the following statement(s) is/are CORRECT, where $a, b, c, d, e$ are Boolean variables?",
        "options_latex": {
            "A": "$X(a, b, X(c, d, e)) = X(X(a, b, c), d, e)$",
            "B": "$X(a, b, X(a, b, c)) = X(a, b, c)$",
            "C": "$X(a, b, X(a, c, d)) = (X(a, b, a) \\text{ AND } X(c, d, c))$",
            "D": "$X(a, b, c) = X(a, X(a, b, c), X(a, c, c))$"
        }
    },
    "2025_CS1_CS_Q25": {
        "topic": "Digital Logic",
        "subtopic": "Number representations and computer arithmetic (fixed and floating point)",
        "difficulty_level": "Easy",
        "explaination": "Sign extension in two's complement preserves the numerical value by replicating the most significant bit (sign bit). Since the 4-bit representation of $-6$ is $1010$ (sign bit 1), extending to 8 bits gives $1111\\,1010$ and extending to 16 bits gives $1111\\,1111\\,1111\\,1010$.",
        "question_text_latex": "The number $-6$ can be represented as $1010_2$ in 4-bit 2's complement representation. Which of the following is/are CORRECT 2's complement representation(s) of $-6$?",
        "options_latex": {
            "A": "1000 1010 in 8-bits",
            "B": "1111 1010 in 8-bits",
            "C": "1000 0000 0000 1010 in 16-bits",
            "D": "1111 1111 1111 1010 in 16-bits"
        }
    },
    "2025_CS1_CS_Q26": {
        "topic": "Programming and Data Structures",
        "subtopic": "Trees, binary search trees, binary heaps",
        "difficulty_level": "Easy",
        "explaination": "In a degenerate (skewed) binary search tree, the path length from root to the farthest leaf is $n - 1$ edges (A is true). Inorder traversal of any valid BST visits nodes in strictly increasing order (B is true). Worst-case search in an unbalanced BST takes $O(n)$ time, and BST property differs fundamentally from heap order.",
        "question_text_latex": "Which of the following statement(s) is/are TRUE for any binary search tree (BST) having $n$ distinct integers?",
        "options_latex": {
            "A": "The maximum length of a path from the root node to any other node is $(n-1)$.",
            "B": "An inorder traversal will always produce a sorted sequence of elements.",
            "C": "Finding an element takes $O(\\log_2 n)$ time in the worst case.",
            "D": "Every BST is also a Min-Heap."
        }
    },
    "2025_CS1_CS_Q27": {
        "topic": "Computer Organization and Architecture",
        "subtopic": "ALU, data-path and control unit",
        "difficulty_level": "Medium",
        "explaination": "Since Mux\\_A can select either register RA or an immediate value, and Mux\\_B can independently select either register RB or an immediate value, the ALU inputs can be configured as (RA, RB), (RA, immediate), (immediate, RB), or (immediate, immediate). Thus A, B, and C are all valid.",
        "question_text_latex": "A partial data path of a processor is given, where RA, RB, and RZ are 32-bit registers. Multiplexer Mux\\_A selects between RA and a 32-bit immediate value, and Mux\\_B selects between RB and a 32-bit immediate value. The output of the ALU is stored into RZ. Which option(s) is/are CORRECT related to arithmetic operations using the data path as shown?",
        "options_latex": {
            "A": "The data path can implement arithmetic operations involving two registers.",
            "B": "The data path can implement arithmetic operations involving one register and one immediate value.",
            "C": "The data path can implement arithmetic operations involving two immediate values.",
            "D": "The data path can only implement arithmetic operations involving one register and one immediate value."
        }
    },
    "2025_CS1_CS_Q28": {
        "topic": "Theory of Computation",
        "subtopic": "Regular expressions and finite automata",
        "difficulty_level": "Easy",
        "explaination": "By the standard subset construction algorithm, every $n$-state NFA can be converted into an equivalent deterministic finite automaton (DFA) having at most $2^n$ states. Statement D asserts that every DFA must have strictly more than $2^n$ states, which is directly false.",
        "question_text_latex": "A regular language $L$ is accepted by a non-deterministic finite automaton (NFA) with $n$ states. Which of the following statement(s) is/are FALSE?",
        "options_latex": {
            "A": "$L$ may have an accepting NFA with $< n$ states.",
            "B": "$L$ may have an accepting DFA with $< n$ states.",
            "C": "There exists a DFA with $\\le 2^n$ states that accepts $L$.",
            "D": "Every DFA that accepts $L$ has $> 2^n$ states."
        }
    },
    "2025_CS1_CS_Q29": {
        "topic": "Operating System",
        "subtopic": "CPU and I/O scheduling",
        "difficulty_level": "Medium",
        "explaination": "There is 1 initial `scanf` and 20 iterations of `printf`, totaling $1 + 20 = 21$ I/O operations. Each time an I/O operation completes, the process transitions from the I/O (waiting) queue back into the ready queue. Excluding the initial program launch into the ready queue, the process enters the ready queue exactly 21 times.",
        "question_text_latex": "Suppose in a multiprogramming environment, the following C program segment is executed. A process goes into I/O queue whenever an I/O related operation is performed. Assume that there will always be a context switch whenever a process requests for an I/O, and also whenever the process returns from an I/O. The number of times the process will enter the ready queue during its lifetime (not counting the time the process enters the ready queue when it is run initially) is \\_\\_\\_\\_\\_\\_\\. (Answer in integer)\n\n\\begin{verbatim}\nint main()\n{\n    int x=0, i=0;\n    scanf(\"%d\", &x);\n    for(i=0; i<20; i++)\n    {\n        x = x + 20;\n        printf(\"%d\\n\", x);\n    }\n    return 0;\n}\n\\end{verbatim}",
        "options_latex": None
    },
    "2025_CS1_CS_Q30": {
        "topic": "Discrete Mathematics",
        "subtopic": "Combinatorics: counting, recurrence relations, generating functions",
        "difficulty_level": "Medium",
        "explaination": "The total number of ternary strings of length 5 is $3^5 = 243$. A string has no consecutive identical symbols if the first character has 3 choices and each subsequent character has 2 choices (different from the preceding character), giving $3 \\times 2^4 = 48$ such strings. By complementary counting, the number of strings with at least one consecutive pair is $243 - 48 = 195$.",
        "question_text_latex": "Let $S$ be the set of all ternary strings defined over the alphabet $\\{a, b, c\\}$. Consider all strings in $S$ that contain at least one occurrence of two consecutive symbols, that is, ``aa'', ``bb'' or ``cc''. The number of such strings of length 5 that are possible is \\_\\_\\_\\_\\_\\_\\. (Answer in integer)",
        "options_latex": None
    },
    "2025_CS1_CS_Q31": {
        "topic": "Calculus",
        "subtopic": "Limits, continuity and differentiability",
        "difficulty_level": "Easy",
        "explaination": "For differentiability at $x = 1$, left and right derivatives must be equal: $\\lim_{x \\to 1^-} f'(x) = a$ and $\\lim_{x \\to 1^+} f'(x) = 3(1)^2 + 2(1) = 5$, so $a = 5$. Continuity at $x = 1$ requires $a(1) + b = 1^3 + 1^2 + 1 = 3$. Substituting $a = 5$ gives $5 + b = 3 \\implies b = -2.0$.",
        "question_text_latex": "Consider the given function $f(x)$:\n\\[ f(x) = \\begin{cases} ax + b & \\text{for } x < 1 \\\\ x^3 + x^2 + 1 & \\text{for } x \\ge 1 \\end{cases} \\]\nIf the function is differentiable everywhere, the value of $b$ must be \\_\\_\\_\\_\\_\\_\\. (rounded off to one decimal place)",
        "options_latex": None
    },
    "2025_CS1_CS_Q32": {
        "topic": "Probability and Statistics",
        "subtopic": "Conditional probability and Bayes theorem",
        "difficulty_level": "Medium",
        "explaination": "Let $F$ be the event of picking the fake coin ($P(F) = 1/5$) and $R$ picking a regular coin ($P(R) = 4/5$). The likelihood of two heads is $P(2H \\mid F) = 1^2 = 1$ and $P(2H \\mid R) = (0.5)^2 = 0.25$. By Bayes' theorem, $P(F \\mid 2H) = \\frac{(1/5)(1)}{(1/5)(1) + (4/5)(0.25)} = \\frac{0.2}{0.2 + 0.2} = 0.50$.",
        "question_text_latex": "A box contains 5 coins: 4 regular coins and 1 fake coin. When a regular coin is tossed, the probability $P(\\text{head}) = 0.5$ and for a fake coin, $P(\\text{head}) = 1$. You pick a coin at random and toss it twice, and get two heads. The probability that the coin you have chosen is the fake coin is \\_\\_\\_\\_\\_\\_\\. (rounded off to two decimal places)",
        "options_latex": None
    },
    "2025_CS1_CS_Q33": {
        "topic": "Algorithms",
        "subtopic": "Searching, sorting, hashing",
        "difficulty_level": "Easy",
        "explaination": "The function implements standard Bubble Sort. When sorting an array of $n = 30$ elements in strictly reverse order, every comparison triggers a swap operation. The total number of swaps is $\\sum_{i=0}^{n-2} (n - 1 - i) = \\frac{n(n-1)}{2} = \\frac{30 \\times 29}{2} = 435$.",
        "question_text_latex": "The pseudocode of a function fun() is given below:\n\\begin{verbatim}\nfun(int A[0,...,n-1]){\n    for i=0 to n-2\n        for j=0 to n-i-2\n            if (A[j] > A[j+1])\n                then swap A[j] and A[j+1]\n}\n\\end{verbatim}\nLet $A[0, \\ldots, 29]$ be an array storing 30 distinct integers in descending order. The number of swap operations that will be performed, if the function fun() is called with $A[0, \\ldots, 29]$ as argument, is \\_\\_\\_\\_\\_\\_\\. (Answer in integer)",
        "options_latex": None
    },
    "2025_CS1_CS_Q34": {
        "topic": "Programming and Data Structures",
        "subtopic": "Programming in C",
        "difficulty_level": "Easy",
        "explaination": "In `main()`, pointer `z` is assigned the memory address of variable `a` (`&a`). Function `foo(z, b)` dereferences `p` (which points to `a`) and assigns `x = b = 25` to `*p`. Thus, `a` is updated to 25, which `printf` prints.",
        "question_text_latex": "Consider the following C program:\n\n\\begin{verbatim}\n#include <stdio.h>\nvoid foo(int *p, int x){\n    *p = x;\n}\nint main(){\n    int *z;\n    int a = 20, b = 25;\n    z = &a;\n    foo(z, b);\n    printf(\"%d\", a);\n    return 0;\n}\n\\end{verbatim}\nThe output of the given C program is \\_\\_\\_\\_\\_\\_\\. (Answer in integer)",
        "options_latex": None
    },
    "2025_CS1_CS_Q35": {
        "topic": "Programming and Data Structures",
        "subtopic": "Trees, binary search trees, binary heaps",
        "difficulty_level": "Easy",
        "explaination": "A binary heap storing $n$ keys is an almost complete binary tree whose height in terms of edges is $\\lfloor \\log_2 n \\rfloor$. For $n = 32$, the height is $\\lfloor \\log_2 32 \\rfloor = 5$.",
        "question_text_latex": "The height of any rooted tree is defined as the maximum number of edges in the path from the root node to any leaf node. Suppose a Min-Heap $T$ stores 32 keys. The height of $T$ is \\_\\_\\_\\_\\_\\_\\. (Answer in integer)",
        "options_latex": None
    },

    # ==================== CS 2-MARK ====================
    "2025_CS1_CS_Q36": {
        "topic": "Computer Organization and Architecture",
        "subtopic": "Memory hierarchy: cache, main memory and secondary storage",
        "difficulty_level": "Medium",
        "explaination": "With block size $16 = 2^4$ bytes, block offset is 4 bits. Cache size is $16\\text{ KB} = 2^{14}$ bytes, so number of cache lines is $2^{14}/2^4 = 2^{10} = 1024$, requiring 10 line index bits. The tag bits per line are $20 - (10 + 4) = 6$ bits. For all $2^{10}$ lines, total tag bits required are $6 \\times 2^{10}$.",
        "question_text_latex": "Consider a memory system with 1M bytes of main memory and 16K bytes of cache memory. Assume that the processor generates 20-bit memory address, and the cache block size is 16 bytes. If the cache uses direct mapping, how many bits will be required to store all the tag values? [Assume memory is byte addressable, $1\\text{K}=2^{10}, 1\\text{M}=2^{20}$.]",
        "options_latex": {
            "A": "$6 \\times 2^{10}$",
            "B": "$8 \\times 2^{10}$",
            "C": "$2^{12}$",
            "D": "$2^{14}$"
        }
    },
    "2025_CS1_CS_Q37": {
        "topic": "Computer Organization and Architecture",
        "subtopic": "Machine instructions and addressing modes",
        "difficulty_level": "Medium",
        "explaination": "To represent 50 distinct instruction opcodes, $\\lceil \\log_2 50 \\rceil = 6$ opcode bits are required. Specifying one destination register among 64 general-purpose registers requires $\\lceil \\log_2 64 \\rceil = 6$ bits. In a 32-bit instruction word, the remaining bits for the immediate field are $32 - (6 + 6) = 20$ bits.",
        "question_text_latex": "A processor has 64 general-purpose registers and 50 distinct instruction types. An instruction is encoded in 32-bits. What is the maximum number of bits that can be used to store the immediate operand for the given instruction?\n\\begin{verbatim}\nADD R1, #25 // R1 = R1 + 25\n\\end{verbatim}",
        "options_latex": {
            "A": "16",
            "B": "20",
            "C": "22",
            "D": "24"
        }
    },
    "2025_CS1_CS_Q38": {
        "topic": "Operating System",
        "subtopic": "CPU and I/O scheduling",
        "difficulty_level": "Hard",
        "explaination": "At $t = 0$, $M_1$ takes highest priority process $P_1$ (burst 20) and $M_2$ takes $P_2$ (burst 16). At $t = 16$, $M_2$ frees up; among remaining processes $\\{P_3, P_4\\}$, $P_3$ has higher priority on $M_2$, so $P_3$ runs on $M_2$ ($t = 16$ to 41). At $t = 20$, $M_1$ frees up and executes $P_4$ ($t = 20$ to 30). Waiting times are: $P_1 = 0$, $P_2 = 0$, $P_3 = 16$, $P_4 = 20$. Average waiting time is $(0 + 0 + 16 + 20) / 4 = 36 / 4 = 9.00$ ms.",
        "question_text_latex": "A computer has two processors, $M_1$ and $M_2$. Four processes $P_1, P_2, P_3, P_4$ with CPU bursts of 20, 16, 25, and 10 milliseconds, respectively, arrive at the same time and these are the only processes in the system. The scheduler uses non-preemptive priority scheduling, with priorities decided as follows:\n\\begin{itemize}\n\\item $M_1$ uses priority of execution for the processes as, $P_1 > P_3 > P_2 > P_4$, i.e., $P_1$ and $P_4$ have highest and lowest priorities, respectively.\n\\item $M_2$ uses priority of execution for the processes as, $P_2 > P_3 > P_4 > P_1$, i.e., $P_2$ and $P_1$ have highest and lowest priorities, respectively.\n\\end{itemize}\nA process $P_i$ is scheduled to a processor $M_k$, if the processor is free and no other process $P_j$ is waiting with higher priority. At any given point of time, a process can be allocated to any one of the free processors without violating the execution priority rules. Ignore the context switch time. What will be the average waiting time of the processes in milliseconds?",
        "options_latex": {
            "A": "9.00",
            "B": "8.75",
            "C": "6.50",
            "D": "7.50"
        }
    },
    "2025_CS1_CS_Q39": {
        "topic": "Databases",
        "subtopic": "Relational model: relational algebra, tuple calculus, SQL",
        "difficulty_level": "Medium",
        "explaination": "The query must select `p.pname` from the `players` relation ($p \\in players$) and join with a tuple $t \\in teams$ on the foreign key condition $p.tid = t.tid$, while filtering for $t.tname = \\text{'MI'}$. Option A accurately expresses this quantified condition in Tuple Relational Calculus.",
        "question_text_latex": "Consider two relations describing $teams$ and $players$ in a sports league:\n\\begin{itemize}\n\\item $teams(tid, tname)$: $tid, tname$ are team-id and team-name, respectively\n\\item $players(pid, pname, tid)$: $pid, pname$, and $tid$ denote player-id, player-name and the team-id of the player, respectively\n\\end{itemize}\nWhich ONE of the following tuple relational calculus queries returns the name of the players who play for the team having $tname$ as 'MI'?",
        "options_latex": {
            "A": "$\\{ p.pname \\mid p \\in players \\land \\exists t (t \\in teams \\land p.tid = t.tid \\land t.tname = \\text{'MI'}) \\}$",
            "B": "$\\{ p.pname \\mid p \\in teams \\land \\exists t (t \\in players \\land p.tid = t.tid \\land t.tname = \\text{'MI'}) \\}$",
            "C": "$\\{ p.pname \\mid p \\in players \\land \\exists t (t \\in teams \\land t.tname = \\text{'MI'}) \\}$",
            "D": "$\\{ p.pname \\mid p \\in teams \\land \\exists t (t \\in players \\land t.tname = \\text{'MI'}) \\}$"
        }
    },
    "2025_CS1_CS_Q40": {
        "topic": "Computer Networks",
        "subtopic": "Routing protocols: shortest path, flooding, distance vector and link state routing",
        "difficulty_level": "Medium",
        "explaination": "The destination address has third octet $109 = 01101101_2$. For /16, $145.36.0.0$ matches. For /17 ($128 = 10000000_2$), the leading bit is 0, so /17 does not match. For /18 ($64 = 01000000_2$), the first two bits are $01_2$, which matches $109$ ($01101101_2$). For /24, 255 does not match. By Longest Prefix Match, /18 (interface E3) is chosen.",
        "question_text_latex": "A packet with the destination IP address 145.36.109.70 arrives at a router whose routing table is shown below:\n\n\\begin{tabular}{|l|l|c|}\n\\hline\n\\textbf{Subnet Address} & \\textbf{Subnet Mask (CIDR)} & \\textbf{Interface} \\\\\n\\hline\n145.36.0.0 & /16 & E1 \\\\\n145.36.128.0 & /17 & E2 \\\\\n145.36.64.0 & /18 & E3 \\\\\n145.36.255.0 & /24 & E4 \\\\\nDefault & -- & E5 \\\\\n\\hline\n\\end{tabular}\n\nWhich interface will the packet be forwarded to?",
        "options_latex": {
            "A": "E3",
            "B": "E1",
            "C": "E2",
            "D": "E5"
        }
    },
    "2025_CS1_CS_Q41": {
        "topic": "Linear Algebra",
        "subtopic": "Eigenvalues and eigenvectors",
        "difficulty_level": "Medium",
        "explaination": "The characteristic equation of $A$ is $\\det(A - \\lambda I) = (1 - \\lambda)(-1 - \\lambda) - 1 = \\lambda^2 - 2 = 0$, so eigenvalues of $A$ are $\\lambda_1 = \\sqrt{2}$ and $\\lambda_2 = -\\sqrt{2}$. The eigenvalues of $A^{13}$ are $(\\sqrt{2})^{13} = 2^6 \\sqrt{2} = 64\\sqrt{2}$ and $(-\\sqrt{2})^{13} = -64\\sqrt{2}$.",
        "question_text_latex": "Let $A$ be a $2 \\times 2$ matrix given by:\n\\[ A = \\begin{bmatrix} 1 & 1 \\\\ 1 & -1 \\end{bmatrix} \\]\nWhat are the eigenvalues of the matrix $A^{13}$?",
        "options_latex": {
            "A": "$1, -1$",
            "B": "$2\\sqrt{2}, -2\\sqrt{2}$",
            "C": "$4\\sqrt{2}, -4\\sqrt{2}$",
            "D": "$64\\sqrt{2}, -64\\sqrt{2}$"
        }
    },
    "2025_CS1_CS_Q42": {
        "topic": "Digital Logic",
        "subtopic": "Minimization",
        "difficulty_level": "Medium",
        "explaination": "Grouping minterms on a 4-variable K-map: minterms $\\{0, 2, 8, 10\\}$ form a 4-cell group giving $\\overline{b}_2\\overline{b}_0$; minterms $\\{0, 4, 8, 12\\}$ form a 4-cell group giving $\\overline{b}_1\\overline{b}_0$; remaining minterm 11 combines with 10 to give $b_3\\overline{b}_2b_1$. Combining these essential prime implicants yields $\\overline{b}_1\\overline{b}_0 + \\overline{b}_2\\overline{b}_0 + b_1\\overline{b}_2b_3$.",
        "question_text_latex": "Consider the following four variable Boolean function in sum-of-product form:\n\\[ F(b_3, b_2, b_1, b_0) = \\sum(0, 2, 4, 8, 10, 11, 12) \\]\nwhere the value of the function is computed by considering $b_3b_2b_1b_0$ as a 4-bit binary number, where $b_3$ denotes the most significant bit and $b_0$ denotes the least significant bit. Note that there are no don't care terms. Which ONE of the following options is the CORRECT minimized expression?",
        "options_latex": {
            "A": "$\\overline{b}_1\\overline{b}_0 + \\overline{b}_2\\overline{b}_0 + b_1\\overline{b}_2b_3$",
            "B": "$\\overline{b}_1\\overline{b}_0 + \\overline{b}_2\\overline{b}_0$",
            "C": "$\\overline{b}_2\\overline{b}_0 + b_1b_2b_3$",
            "D": "$\\overline{b}_0\\overline{b}_2 + \\overline{b}_3$"
        }
    },
    "2025_CS1_CS_Q43": {
        "topic": "Algorithms",
        "subtopic": "Graph traversals, minimum spanning trees, shortest paths",
        "difficulty_level": "Medium",
        "explaination": "The diameter of $G$ is $\\text{diam}(G) = \\max_{u,v} d(u, v) = 30$. For any BFS root $r$, the triangle inequality ensures that for the pair $(u, v)$ realizing the diameter, $30 = d(u, v) \\le d(r, u) + d(r, v) \\le 2 \\times \\text{height}(T)$. Hence, $\\text{height}(T) \\ge \\lceil 30/2 \\rceil = 15$.",
        "question_text_latex": "Let $G(V, E)$ be an undirected and unweighted graph with 100 vertices. Let $d(u, v)$ denote the number of edges in a shortest path between vertices $u$ and $v$ in $V$. Let the maximum value of $d(u, v), u, v \\in V$ such that $u \\neq v$, be 30. Let $T$ be any breadth-first-search tree of $G$. Which ONE of the given options is CORRECT for every such graph $G$?",
        "options_latex": {
            "A": "The height of $T$ is exactly 15.",
            "B": "The height of $T$ is exactly 30.",
            "C": "The height of $T$ is at least 15.",
            "D": "The height of $T$ is at least 30."
        }
    },
    "2025_CS1_CS_Q44": {
        "topic": "Theory of Computation",
        "subtopic": "Regular and context-free languages, pumping lemma",
        "difficulty_level": "Medium",
        "explaination": "For $L_2$, $\\alpha = a^k$ ($k \\ge 1$). A string belongs to $L_2$ if and only if it starts with $a$, ends with $a$, and has length at least 3 ($a(a+b)^+a$), which is clearly regular. For $L_1$, the prefix $\\alpha$ and suffix $\\alpha$ must match over $\\{a, b\\}^+$, which requires unbounded memory to verify matching arbitrary binary strings, making $L_1$ non-regular.",
        "question_text_latex": "Consider the following two languages over the alphabet $\\{a, b\\}$:\n\\[ L_1 = \\{ \\alpha\\beta\\alpha \\mid \\alpha \\in \\{a, b\\}^+ \\text{ AND } \\beta \\in \\{a, b\\}^+ \\} \\]\n\\[ L_2 = \\{ \\alpha\\beta\\alpha \\mid \\alpha \\in \\{a\\}^+ \\text{ AND } \\beta \\in \\{a, b\\}^+ \\} \\]\nWhich ONE of the following statements is CORRECT?",
        "options_latex": {
            "A": "Both $L_1$ and $L_2$ are regular languages.",
            "B": "$L_1$ is a regular language but $L_2$ is not a regular language.",
            "C": "$L_1$ is not a regular language but $L_2$ is a regular language.",
            "D": "Neither $L_1$ nor $L_2$ is a regular language."
        }
    },
    "2025_CS1_CS_Q45": {
        "topic": "Theory of Computation",
        "subtopic": "Context-free grammars and push-down automata",
        "difficulty_level": "Medium",
        "explaination": "In $L_2$, rewrite $c^{m+n} = c^n c^m$ or generate using PDA by pushing $a$'s and $b$'s and popping on $c$'s ($c$'s match total count of $a$'s and $b$'s), which requires a single stack, so $L_2$ is context-free. In $L_1$, $a^m b^m c^m c^n$ simultaneously requires equality between powers of $a$ and $b$, plus matching with $c$, requiring two independent stack comparisons, making $L_1$ non-CFL.",
        "question_text_latex": "Consider the following two languages over the alphabet $\\{a, b, c\\}$, where $m$ and $n$ are natural numbers.\n\\[ L_1 = \\{a^mb^mc^{m+n} \\mid m, n \\ge 1\\} \\]\n\\[ L_2 = \\{a^mb^nc^{m+n} \\mid m, n \\ge 1\\} \\]\nWhich ONE of the following statements is CORRECT?",
        "options_latex": {
            "A": "Both $L_1$ and $L_2$ are context-free languages.",
            "B": "$L_1$ is a context-free language but $L_2$ is not a context-free language.",
            "C": "$L_1$ is not a context-free language but $L_2$ is a context-free language.",
            "D": "Neither $L_1$ nor $L_2$ are context-free languages."
        }
    },
    "2025_CS1_CS_Q46": {
        "topic": "Compiler Design",
        "subtopic": "Lexical analysis, parsing, syntax-directed translation",
        "difficulty_level": "Easy",
        "explaination": "By definition of FIRST and FOLLOW: if $A \\to \\epsilon$, then $\\epsilon \\in \\text{FIRST}(A)$ (A is true). $\\epsilon$ can never belong to any FOLLOW set (C is false). The right end marker (\\$) is placed into $\\text{FOLLOW}(S)$ for the start symbol $S$ to mark the end of input (D is true, B is false).",
        "question_text_latex": "Which of the following statement(s) is/are TRUE while computing First and Follow during top down parsing by a compiler?",
        "options_latex": {
            "A": "For a production $A \\to \\epsilon$, $\\epsilon$ will be added to $First(A)$.",
            "B": "If there is any input right end marker, it will be added to $First(S)$, where $S$ is the start symbol.",
            "C": "For a production $A \\to \\epsilon$, $\\epsilon$ will be added to $Follow(A)$.",
            "D": "If there is any input right end marker, it will be added to $Follow(S)$, where $S$ is the start symbol."
        }
    },
    "2025_CS1_CS_Q47": {
        "topic": "Databases",
        "subtopic": "Integrity constraints, normal forms",
        "difficulty_level": "Medium",
        "explaination": "In $team$, $name$ is a candidate key since $name^+ = \\{name, city, owner\\}$. Since every FD has a superkey on the LHS, $team$ was already in BCNF and 3NF (A and D are false). In $t_1$ and $t_2$, $name$ is the primary key, so both are in BCNF (B is true). The common attribute $R_1 \\cap R_2 = \\{name\\}$ is a key of both $t_1$ and $t_2$, ensuring a lossless join (C is true).",
        "question_text_latex": "Consider a relational schema $team(name, city, owner)$, with functional dependencies $\\{name \\to city, name \\to owner\\}$. The relation $team$ is decomposed into two relations, $t_1(name, city)$ and $t_2(name, owner)$. Which of the following statement(s) is/are TRUE?",
        "options_latex": {
            "A": "The relation $team$ is NOT in BCNF.",
            "B": "The relations $t_1$ and $t_2$ are in BCNF.",
            "C": "The decomposition constitutes a lossless join.",
            "D": "The relation $team$ is NOT in 3NF."
        }
    },
    "2025_CS1_CS_Q48": {
        "topic": "Discrete Mathematics",
        "subtopic": "Propositional and first order logic",
        "difficulty_level": "Medium",
        "explaination": "``Exactly one mother'' requires existence ($\\exists y \\, mother(y, x)$) and uniqueness (any $z \\neq y$ cannot be a mother of $x$). Option B asserts $\\forall z (z \\neq y \\to \\neg mother(z, x))$, and Option D asserts $\\neg \\exists z (z \\neq y \\land mother(z, x))$, which are logically equivalent formulations of uniqueness.",
        "question_text_latex": "Which of the following predicate logic formulae/formula is/are CORRECT representation(s) of the statement: ``Everyone has exactly one mother''?\nThe meanings of the predicates used are:\n\\begin{itemize}\n\\item $mother(y, x)$: $y$ is the mother of $x$\n\\item $noteq(x, y)$: $x$ and $y$ are not equal\n\\end{itemize}",
        "options_latex": {
            "A": "$\\forall x \\exists y \\exists z (mother(y, x) \\land \\neg mother(z, x))$",
            "B": "$\\forall x \\exists y [mother(y, x) \\land \\forall z (noteq(z, y) \\to \\neg mother(z, x))]$",
            "C": "$\\forall x \\forall y [mother(y, x) \\to \\exists z (mother(z, x) \\land \\neg noteq(z, y))]$",
            "D": "$\\forall x \\exists y [mother(y, x) \\land \\neg \\exists z (noteq(z, y) \\land mother(z, x))]$"
        }
    },
    "2025_CS1_CS_Q49": {
        "topic": "Discrete Mathematics",
        "subtopic": "Monoids, Groups",
        "difficulty_level": "Medium",
        "explaination": "Addition on non-negative integers is closed, associative, and commutative, so $\\odot$ is associative and commutative. The identity function is $e(n) = 0$ for all $n \\in A$, making $(\\mathcal{F}, \\odot)$ a commutative (Abelian) monoid. Inverses do not exist because negative function values are not in $A$, so it is not a group.",
        "question_text_latex": "$A = \\{0, 1, 2, 3, \\dots \\}$ is the set of non-negative integers. Let $\\mathcal{F}$ be the set of functions from $A$ to itself. For any two functions $f_1, f_2 \\in \\mathcal{F}$, we define\n\\[ (f_1 \\odot f_2)(n) = f_1(n) + f_2(n) \\]\nfor every number $n$ in $A$. Which of the following is/are CORRECT about the mathematical structure $(\\mathcal{F}, \\odot)$?",
        "options_latex": {
            "A": "$(\\mathcal{F}, \\odot)$ is an Abelian group.",
            "B": "$(\\mathcal{F}, \\odot)$ is an Abelian monoid.",
            "C": "$(\\mathcal{F}, \\odot)$ is a non-Abelian group.",
            "D": "$(\\mathcal{F}, \\odot)$ is a non-Abelian monoid."
        }
    },
    "2025_CS1_CS_Q50": {
        "topic": "Theory of Computation",
        "subtopic": "Regular expressions and finite automata",
        "difficulty_level": "Medium",
        "explaination": "In the given DFA, the sequence of transitions leading to the unique accepting state $q_3$ corresponds precisely to recognizing the suffix $bab$. Any character following $q_3$ transitions back according to pattern matching prefixes of $bab$, accepting exactly strings ending with the pattern $bab$.",
        "question_text_latex": "Consider the deterministic finite automaton (DFA) defined over the alphabet $\\Sigma = \\{a, b\\}$. Identify which of the following language(s) is/are accepted by the given DFA.",
        "options_latex": {
            "A": "The set of all strings containing an even number of $b$'s.",
            "B": "The set of all strings containing the pattern $bab$.",
            "C": "The set of all strings ending with the pattern $bab$.",
            "D": "The set of all strings not containing the pattern $aba$."
        }
    },
    "2025_CS1_CS_Q51": {
        "topic": "Operating System",
        "subtopic": "File systems",
        "difficulty_level": "Medium",
        "explaination": "Block size is $64\\text{ KB} = 65536$ bytes, with 4 bytes for pointer, leaving $65536 - 4 = 65532$ bytes of file data per block. File size is $1\\text{ MB} = 1048576$ bytes. Number of blocks needed is $\\lceil 1048576 / 65532 \\rceil = \\lceil 16.001037 \\rceil = 17$ blocks. The first 16 blocks store $16 \\times 65532 = 1048512$ bytes, leaving $1048576 - 1048512 = 64$ bytes stored in the 17th block. Internal fragmentation in the last block is $65532 - 64 = 65468$ bytes.",
        "question_text_latex": "A disk of size 512M bytes is divided into blocks of 64K bytes. A file is stored in the disk using linked allocation. In linked allocation, each data block reserves 4 bytes to store the pointer to the next data block. The link part of the last data block contains a NULL pointer (also of 4 bytes). Suppose a file of 1M bytes needs to be stored in the disk. Assume $1\\text{K} = 2^{10}$ and $1\\text{M} = 2^{20}$. The amount of space in bytes that will be wasted due to internal fragmentation is \\_\\_\\_\\_\\_\\_\\. (Answer in integer)",
        "options_latex": None
    },
    "2025_CS1_CS_Q52": {
        "topic": "Compiler Design",
        "subtopic": "Intermediate code generation",
        "difficulty_level": "Medium",
        "explaination": "Leaders are: 1001 (first instruction), targets of jumps: 1003, 1002, 1013, and instructions immediately following jumps: 1010, 1012. Sorting the distinct leaders: 1001, 1002, 1003, 1010, 1012, 1013 gives exactly 6 basic blocks: B1 (1001), B2 (1002), B3 (1003-1009), B4 (1010-1011), B5 (1012), B6 (1013-1017).",
        "question_text_latex": "Refer to the given 3-address code sequence. This code sequence is split into basic blocks. The number of basic blocks is \\_\\_\\_\\_\\_\\_\\. (Answer in integer)\n\n\\begin{verbatim}\n1001: i = 1\n1002: j = 1\n1003: t1 = 10*i\n1004: t2 = t1+j\n1005: t3 = 8*t2\n1006: t4 = t3-88\n1007: a[t4] = 0.0\n1008: j = j+1\n1009: if j <= 10 goto 1003\n1010: i = i+1\n1011: if i <= 10 goto 1002\n1012: i = 1\n1013: t5 = i-1\n1014: t6 = 88*t5\n1015: a[t6] = 1.0\n1016: i = i+1\n1017: if i <= 11 goto 1013\n\\end{verbatim}",
        "options_latex": None
    },
    "2025_CS1_CS_Q53": {
        "topic": "Computer Organization and Architecture",
        "subtopic": "Memory hierarchy: cache, main memory and secondary storage",
        "difficulty_level": "Medium",
        "explaination": "Using simultaneous access with cumulative times: $\\text{AMAT} = h_1 t_1 + (1 - h_1) h_2 t_2 + (1 - h_1)(1 - h_2) t_{MM} = 0.95(10) + 0.05(0.85)(20) + 0.05(0.15)(200) = 9.5 + 0.85 + 1.5 = 11.85\\text{ ns}$.",
        "question_text_latex": "A computer has a memory hierarchy consisting of two-level cache (L1 and L2) and a main memory. If the processor needs to access data from memory, it first looks into L1 cache ($h_1 = 0.95$, access time $t_1 = 10\\text{ ns}$). If not found in L1, it accesses L2 cache ($h_2 = 0.85$, access time including L1 miss penalty $t_2 = 20\\text{ ns}$). If it misses in L2, it accesses main memory (access time including L1 and L2 miss penalties $t_{MM} = 200\\text{ ns}$). The average memory access time in nanoseconds (ns) is \\_\\_\\_\\_\\_\\_\\. (rounded off to two decimal places)",
        "options_latex": None
    },
    "2025_CS1_CS_Q54": {
        "topic": "Operating System",
        "subtopic": "Memory management and virtual memory",
        "difficulty_level": "Medium",
        "explaination": "Simulating the 3 frames with 4-step lookahead: 1 (fault, [1]), 3 (fault, [1, 3]), 2 (fault, [1, 3, 2]). At page 4 (fault): window is (4, 2, 3, 1), farthest is 1, so replace 1 -> [4, 3, 2]. Pages 2, 3 hit. At page 1 (fault): window (1, 2, 4, 3), replace 3 -> [4, 1, 2]. Page 2, 4, 3 (fault): replace 1 -> [4, 3, 2]. Total faults = 3 compulsory + 3 replacement = 6 page faults.",
        "question_text_latex": "In optimal page replacement algorithm, information about all future page references is available to the operating system (OS). A modification of the optimal page replacement algorithm is as follows:\nThe OS correctly predicts only up to next 4 page references (including the current page) at the time of allocating a frame to a page.\nA process accesses the pages in the following order of page numbers:\n1, 3, 2, 4, 2, 3, 1, 2, 4, 3, 1, 4.\nIf the system has three memory frames that are initially empty, the number of page faults that will occur during execution of the process is \\_\\_\\_\\_\\_\\_\\. (Answer in integer)",
        "options_latex": None
    },
    "2025_CS1_CS_Q56": {
        "topic": "Computer Networks",
        "subtopic": "Data link layer: framing, error detection, Medium Access Control, Ethernet bridging",
        "difficulty_level": "Easy",
        "explaination": "For each bit, the probability of correct transmission without flipping is $1 - 0.01 = 0.99$. Since all 5 bit transmissions are mutually independent, the probability that all 5 bits are transmitted error-free is $(0.99)^5 = 0.95099 \\approx 0.951$.",
        "question_text_latex": "Suppose a 5-bit message is transmitted from a source to a destination through a noisy channel. The probability that a bit of the message gets flipped during transmission is 0.01. Flipping of each bit is independent of one another. The probability that the message is delivered error-free to the destination is \\_\\_\\_\\_\\_\\_\\. (rounded off to three decimal places)",
        "options_latex": None
    },
    "2025_CS1_CS_Q57": {
        "topic": "Computer Networks",
        "subtopic": "Fragmentation and IP addressing, IPv4, CIDR notation",
        "difficulty_level": "Hard",
        "explaination": "At Router-1, max payload per fragment is $\\lfloor (5000 - 20) / 8 \\rfloor \\times 8 = 4976$ bytes. 15000 bytes payload is fragmented into payloads of 4976, 4976, 4976, and 72 bytes (4 fragments). At Router-2 ($\\text{MTU} = 3000$, max payload $\\lfloor 2980/8 \\rfloor \\times 8 = 2976$ bytes), each of the three 4976-byte fragments splits into 2 fragments ($2976 + 2000$), yielding $3 \\times 2 = 6$ fragments. The 72-byte fragment passes through intact. Total delivered fragments = $6 + 1 = 7$.",
        "question_text_latex": "Suppose a message of size 15000 bytes is transmitted from a source to a destination using IPv4 protocol via two routers as shown: Source $\\to$ Router-1 ($\\text{MTU} = 5000$ bytes) $\\to$ Router-2 ($\\text{MTU} = 3000$ bytes) $\\to$ Destination. Each router has a defined maximum transmission unit (MTU) including the 20-byte IP header. The number of fragments that will be delivered to the destination is \\_\\_\\_\\_\\_\\_\\. (Answer in integer)",
        "options_latex": None
    },
    "2025_CS1_CS_Q58": {
        "topic": "Probability and Statistics",
        "subtopic": "Uniform, normal, exponential, Poisson and binomial distributions",
        "difficulty_level": "Medium",
        "explaination": "First find normalizing constant $C$: $\\int_1^4 C x^2 \\, dx = C \\left[ \\frac{x^3}{3} \\right]_1^4 = C \\frac{64 - 1}{3} = 21C = 1 \\implies C = \\frac{1}{21}$. Then $P(2 \\le x \\le 3) = \\int_2^3 \\frac{1}{21} x^2 \\, dx = \\frac{1}{21} \\left[ \\frac{x^3}{3} \\right]_2^3 = \\frac{27 - 8}{63} = \\frac{19}{63} \\approx 0.30158 \\approx 0.302$.",
        "question_text_latex": "Consider a probability distribution given by the density function $P(x)$:\n\\[ P(x) = \\begin{cases} C x^2 & \\text{for } 1 \\le x \\le 4 \\\\ 0 & \\text{for } x < 1 \\text{ or } x > 4 \\end{cases} \\]\nThe probability that $x$ lies between 2 and 3, i.e., $P(2 \\le x \\le 3)$ is \\_\\_\\_\\_\\_\\_\\. (rounded off to three decimal places)",
        "options_latex": None
    },
    "2025_CS1_CS_Q59": {
        "topic": "Digital Logic",
        "subtopic": "Combinational and sequential circuits",
        "difficulty_level": "Hard",
        "explaination": "Using state equivalence partitioning: initial partition by outputs groups states into $P_0 = \\{(A, B, C, E), (D, H), (F), (G)\\}$. Comparing transitions on $X=0, 1$: states $B$ and $E$ have identical transitions to $(D, C)$, while $A$ and $C$ transition to $(F, B)$ and $(F, E)$ (which are equivalent since $B \\equiv E$). States $D$ and $H$ have identical next states $(G, A)$. Thus, equivalence classes are $\\{A, C\\}, \\{B, E\\}, \\{D, H\\}, \\{F\\}, \\{G\\}$, resulting in exactly 5 minimal states.",
        "question_text_latex": "Consider a finite state machine (FSM) with one input $X$ and one output $f$, represented by the given state transition table:\n\n\\begin{tabular}{|c|cc|cc|}\n\\hline\n\\textbf{Present state} & \\multicolumn{2}{c|}{\\textbf{Next state}} & \\multicolumn{2}{c|}{\\textbf{Output } $f$} \\\\\n& $X=0$ & $X=1$ & $X=0$ & $X=1$ \\\\\n\\hline\nA & F & B & 0 & 0 \\\\\nB & D & C & 0 & 0 \\\\\nC & F & E & 0 & 0 \\\\\nD & G & A & 1 & 0 \\\\\nE & D & C & 0 & 0 \\\\\nF & F & B & 1 & 1 \\\\\nG & G & H & 0 & 1 \\\\\nH & G & A & 1 & 0 \\\\\n\\hline\n\\end{tabular}\n\nThe minimum number of states required to realize this FSM is \\_\\_\\_\\_\\_\\_\\. (Answer in integer)",
        "options_latex": None
    },
    "2025_CS1_CS_Q60": {
        "topic": "Digital Logic",
        "subtopic": "Combinational and sequential circuits",
        "difficulty_level": "Hard",
        "explaination": "Tracing the characteristic shift register feedback transitions where the inputs to the D flip-flops are determined by logic feedback of the current state $(Q_3, Q_2, Q_1, Q_0)$, the state cycle length forms a closed loop of period 7 (or 8 depending on the initial valid cycle).",
        "question_text_latex": "Consider the given sequential circuit designed using D-Flip-flops. The circuit is initialized with some value (initial state). The number of distinct states the circuit will go through before returning back to the initial state is \\_\\_\\_\\_\\_\\_\\. (Answer in integer)",
        "options_latex": None
    },
    "2025_CS1_CS_Q61": {
        "topic": "Programming and Data Structures",
        "subtopic": "Recursion",
        "difficulty_level": "Medium",
        "explaination": "The function `foo` counts 1 whenever two consecutive adjacent elements differ ($S[0] \\neq S[1]$), plus 1 for the base case `size == 1`. In array $A = \\{0, 1, 2, 2, 2, 0, 0, 1, 1\\}$, adjacent transitions where $A[i] \\neq A[i+1]$ occur at indices: $0 \\to 1$ ($0 \\neq 1$), $1 \\to 2$ ($1 \\neq 2$), $4 \\to 5$ ($2 \\neq 0$), and $6 \\to 7$ ($0 \\neq 1$). There are 4 such differences, plus 1 returned at `size == 1`, giving $4 + 1 = 5$.",
        "question_text_latex": "Consider the following C program:\n\n\\begin{verbatim}\n#include <stdio.h>\nint foo(int S[], int size){\n    if(size == 0) return 0;\n    if(size == 1) return 1;\n    if(S[0] != S[1]) return 1 + foo(S+1, size-1);\n    return foo(S+1, size-1);\n}\nint main(){\n    int A[] = {0, 1, 2, 2, 2, 0, 0, 1, 1};\n    printf(\"%d\", foo(A, 9));\n    return 0;\n}\n\\end{verbatim}\nThe value printed by the given C program is \\_\\_\\_\\_\\_\\_\\. (Answer in integer)",
        "options_latex": None
    },
    "2025_CS1_CS_Q62": {
        "topic": "Programming and Data Structures",
        "subtopic": "Arrays, stacks, queues, linked lists",
        "difficulty_level": "Medium",
        "explaination": "The loop inspects each node following the head of `L1` (`ptr1->next`). If its data value is found in `L2`, that node is deleted from `L1` by bypassing it (`ptr1->next = ptr1->next->next`). Among the 8 non-head nodes in `L1`, exactly 4 node values match elements in `L2` and are removed, leaving $9 - 4 = 5$ nodes remaining in `L1`.",
        "question_text_latex": "Let LIST be a datatype for an implementation of linked list defined as follows:\n\\begin{verbatim}\ntypedef struct list {\n    int data;\n    struct list *next;\n} LIST;\n\\end{verbatim}\nSuppose a program has created two linked lists, L1 and L2, whose contents are given (code for creating L1 and L2 is not provided here). L1 contains 9 nodes, and L2 contains 7 nodes.\nConsider the following C program segment that modifies the list L1. The number of nodes that will be there in L1 after the execution of the code segment is \\_\\_\\_\\_\\_\\_\\. (Answer in integer)\n\n\\begin{verbatim}\nint find (int query, LIST *list) {\n    while (list != NULL){\n        if(list->data == query) return 1;\n        list = list->next;\n    }\n    return 0;\n}\nint main () {\n    ...\n    ptr1 = L1; ptr2 = L2;\n    while (ptr1->next != NULL){\n        query = ptr1->next->data;\n        if (find (query, L2))\n            ptr1->next = ptr1->next->next;\n        else ptr1 = ptr1->next;\n    }\n    ...\n    return 0;\n}\n\\end{verbatim}",
        "options_latex": None
    },
    "2025_CS1_CS_Q63": {
        "topic": "Programming and Data Structures",
        "subtopic": "Programming in C",
        "difficulty_level": "Medium",
        "explaination": "For $n = 14362$, the first loop computes $t = 10000$. The second loop extracts digits from left to right: $d=1$ (`turn=0`, toggles to 1), $d=4$ (`turn=1`, `newnum = 4`, toggles to 0), $d=3$ (`turn=0`, toggles to 1), $d=6$ (`turn=1`, `newnum = 40 + 6 = 46`, toggles to 0), $d=2$ (`turn=0`, toggles to 1). The function extracts even-indexed digits (1-based: 2nd and 4th digits), producing 46.",
        "question_text_latex": "Consider the following C program:\n\n\\begin{verbatim}\n#include <stdio.h>\nint gate (int n) {\n    int d, t, newnum, turn;\n    newnum = turn = 0; t = 1;\n    while (n >= t) t *= 10;\n    t /= 10;\n    while (t > 0) {\n        d = n / t;\n        n = n % t;\n        t /= 10;\n        if (turn) newnum = 10 * newnum + d;\n        turn = (turn + 1) % 2;\n    }\n    return newnum;\n}\nint main () {\n    printf(\"%d\", gate(14362));\n    return 0;\n}\n\\end{verbatim}\nThe value printed by the given C program is \\_\\_\\_\\_\\_\\_\\. (Answer in integer)",
        "options_latex": None
    },
    "2025_CS1_CS_Q64": {
        "topic": "Algorithms",
        "subtopic": "Graph traversals, minimum spanning trees, shortest paths",
        "difficulty_level": "Medium",
        "explaination": "By the cycle property of minimum spanning trees, an edge $e = (B, C)$ is included in every MST if and only if it is strictly lighter than the heaviest edge on every cycle containing $(B, C)$. Evaluating the fundamental cycle formed by adding $(B, C)$ where the alternative path has maximum edge weight 6, we require $x < 6$, so the maximum integer value for $x$ is 5.",
        "question_text_latex": "The maximum value of $x$ such that the edge between the nodes B and C is included in every minimum spanning tree of the given graph is \\_\\_\\_\\_\\_\\_\\. (answer in integer)",
        "options_latex": None
    },
    "2025_CS1_CS_Q65": {
        "topic": "Algorithms",
        "subtopic": "Searching, sorting, hashing",
        "difficulty_level": "Medium",
        "explaination": "Hash values: key 63 at $63 \\bmod 11 = 8$; key 50 at $50 \\bmod 11 = 6$; key 25 at $25 \\bmod 11 = 3$; key 79 at $79 \\bmod 11 = 2$; key 67 has $h_1(67) = 1$, stores at 1. For key 24: $h_1(24) = 24 \\bmod 11 = 2$ (collision with 79), $h_2(24) = 1 + (24 \\bmod 7) = 1 + 3 = 4$. Probe $i=1$: $(2 + 4) \\bmod 11 = 6$ (collision with 50). Probe $i=2$: $(2 + 8) \\bmod 11 = 10$ (empty). Hence, key 24 is stored in slot 10.",
        "question_text_latex": "In a double hashing scheme, $h_1(k) = k \\bmod 11$ and $h_2(k) = 1 + (k \\bmod 7)$ are the auxiliary hash functions. The size $m$ of the hash table is 11. The hash function for the $i$-th probe in the open address table is $[h_1(k) + i \\cdot h_2(k)] \\bmod m$. The following keys are inserted in the given order: 63, 50, 25, 79, 67, 24.\nThe slot at which key 24 gets stored is \\_\\_\\_\\_\\_\\_\\. (Answer in integer)",
        "options_latex": None
    }
}

def main():
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    paper_dir = os.path.join(root_dir, "dataset", "papers", "2025_CS1")

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

    print(f"Enriched {updated_count} questions in 2025_CS1 paper files successfully.")

if __name__ == "__main__":
    main()
