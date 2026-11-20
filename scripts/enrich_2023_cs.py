#!/usr/bin/env python3
"""
enrich_2023_cs.py

Fills the AI metadata fields for 2023 CS questions based on syllabus/cs_2026_syllabus.json:
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
    "2023_CS_GA_Q01": {
        "topic": "Verbal Aptitude",
        "subtopic": "Basic English grammar: tenses, articles, adjectives, prepositions, conjunctions, verb-noun agreement",
        "difficulty_level": "Easy",
        "explaination": "The adverb 'nearly' means 'almost' and correctly modifies the past-tense verb 'missed'. 'Near' is an adjective/preposition, while 'utterly' and 'mostly' do not fit the intended semantic meaning of narrowly missing a train.",
        "question_text_latex": "We reached the station late, and \\_\\_\\_\\_\\_\\_\\_ missed the train.",
        "options_latex": {
            "A": "near",
            "B": "nearly",
            "C": "utterly",
            "D": "mostly"
        }
    },
    "2023_CS_GA_Q02": {
        "topic": "Verbal Aptitude",
        "subtopic": "Vocabulary: words, idioms, and phrases in context",
        "difficulty_level": "Easy",
        "explaination": "'Often' and 'Frequently' are direct synonyms. 'Kind' can be a noun meaning 'Type' (category) or an adjective meaning benevolent/caring. Because of multiple ambiguous interpretations of 'Kind', GATE awarded Marks to All (MTA) for this question.",
        "question_text_latex": "Kind : \\_\\_\\_\\_\\_\\_\\_ : : Often : Frequently\n(By word meaning)",
        "options_latex": {
            "A": "Mean",
            "B": "Type",
            "C": "Cruel",
            "D": "Kindly"
        }
    },
    "2023_CS_GA_Q03": {
        "topic": "Quantitative Aptitude",
        "subtopic": "Numerical computation and estimation: ratios, percentages, powers, exponents and logarithms, permutations and combinations, series",
        "difficulty_level": "Easy",
        "explaination": "The recurrence relation is $F_{n+1} = F_n + F_{n-1} \\implies F_{n-1} = F_{n+1} - F_n$. Working backward from $F_7 = 60$ and $F_6 = 37$: $F_5 = 60 - 37 = 23$; $F_4 = 37 - 23 = 14$; $F_3 = 23 - 14 = 9$; $F_2 = 14 - 9 = 5$; and $F_1 = 9 - 5 = 4$.",
        "question_text_latex": "A series of natural numbers $F_1, F_2, F_3, F_4, F_5, F_6, F_7, \\dots$ obeys $F_{n+1} = F_n + F_{n-1}$ for all integers $n \\ge 2$.\nIf $F_6 = 37$, and $F_7 = 60$, then what is $F_1$?",
        "options_latex": {
            "A": "4",
            "B": "5",
            "C": "8",
            "D": "9"
        }
    },
    "2023_CS_GA_Q04": {
        "topic": "Quantitative Aptitude",
        "subtopic": "Numerical computation and estimation: ratios, percentages, powers, exponents and logarithms, permutations and combinations, series",
        "difficulty_level": "Easy",
        "explaination": "Out of all pregnant women, 90% received medical care at least once. Among those who received medical care, 60% received care from doctors. The percentage of all pregnant women who received care at least once from a doctor is $90\\% \\times 60\\% = 54\\%$, which is strictly greater than half ($> 50\\%$).",
        "question_text_latex": "A survey for a certain year found that 90\\% of pregnant women received medical care at least once before giving birth. Of these women, 60\\% received medical care from doctors, while 40\\% received medical care from other healthcare providers.\nGiven this information, which one of the following statements can be inferred with certainty?",
        "options_latex": {
            "A": "More than half of the pregnant women received medical care at least once from a doctor.",
            "B": "Less than half of the pregnant women received medical care at least once from a doctor.",
            "C": "More than half of the pregnant women received medical care at most once from a doctor.",
            "D": "Less than half of the pregnant women received medical care at most once from a doctor."
        }
    },
    "2023_CS_GA_Q05": {
        "topic": "Spatial Aptitude",
        "subtopic": "Transformation of shapes: translation, rotation, scaling, mirroring, assembling, and grouping",
        "difficulty_level": "Easy",
        "explaination": "A smooth 3-dimensional object (such as a torus or a dumbbell shape) can possess regions of positive Gaussian curvature where it is locally convex, as well as regions of negative curvature (saddle-like regions) where it is locally concave. Hence, its surface may be concave in some places and convex in others.",
        "question_text_latex": "Looking at the surface of a smooth 3-dimensional object from the outside, which one of the following options is TRUE?",
        "options_latex": {
            "A": "The surface of the object must be concave everywhere.",
            "B": "The surface of the object must be convex everywhere.",
            "C": "The surface of the object may be concave in some places and convex in other places.",
            "D": "The object can have edges, but no corners."
        }
    },

    # ==================== GA 2-MARK ====================
    "2023_CS_GA_Q06": {
        "topic": "Verbal Aptitude",
        "subtopic": "Reading and comprehension",
        "difficulty_level": "Easy",
        "explaination": "The passage establishes that a complete lack of physical exercise is a primary cause of health issues, and in response, the government provides financial incentives to ride bicycles to work. This direct causal measure logically implies that the government views bicycle riding as a form of physical exercise.",
        "question_text_latex": "The country of Zombieland is in distress since more than 75\\% of its working population is suffering from serious health issues. Studies conducted by competent health experts concluded that a complete lack of physical exercise among its working population was one of the leading causes of their health issues. As one of the measures to address the problem, the Government of Zombieland has decided to provide monetary incentives to those who ride bicycles to work.\n\nBased only on the information provided above, which one of the following statements can be logically inferred with certainty?",
        "options_latex": {
            "A": "All the working population of Zombieland will henceforth ride bicycles to work.",
            "B": "Riding bicycles will ensure that all of the working population of Zombieland is free of health issues.",
            "C": "The health experts suggested to the Government of Zombieland to declare riding bicycles as mandatory.",
            "D": "The Government of Zombieland believes that riding bicycles is a form of physical exercise."
        }
    },
    "2023_CS_GA_Q07": {
        "topic": "Quantitative Aptitude",
        "subtopic": "Numerical computation and estimation: ratios, percentages, powers, exponents and logarithms, permutations and combinations, series",
        "difficulty_level": "Easy",
        "explaination": "Setting $f(t) = g(t) \\implies 0.01 t^2 = 4t \\implies t = 400$. For any $0 < t < 400$ (e.g., $t = 10$), $g(10) = 40 > f(10) = 1$, making statement (i) correct. For all $t > 400$, the quadratic growth of $f(t)$ strictly dominates the linear growth of $g(t)$, so choosing $T = 400$ satisfies statement (ii). Hence, both statements are correct.",
        "question_text_latex": "Consider two functions of time ($t$),\n\\[ f(t) = 0.01 t^2, \\quad g(t) = 4 t \\]\nwhere $0 < t < \\infty$.\nNow consider the following two statements:\n\\begin{enumerate}[label=(\\roman*),itemsep=0pt,topsep=2pt]\n\\item For some $t > 0$, $g(t) > f(t)$.\n\\item There exists a $T$, such that $f(t) > g(t)$ for all $t > T$.\n\\end{enumerate}\nWhich one of the following options is TRUE?",
        "options_latex": {
            "A": "only (i) is correct",
            "B": "only (ii) is correct",
            "C": "both (i) and (ii) are correct",
            "D": "neither (i) nor (ii) is correct"
        }
    },
    "2023_CS_GA_Q08": {
        "topic": "Verbal Aptitude",
        "subtopic": "Narrative sequencing",
        "difficulty_level": "Easy",
        "explaination": "Sentence (iii) introduces the protagonist Mina carrying heavy market purchases. Sentence (ii) describes the resulting exertion as she climbs the stairs. Sentence (i) brings her onto the terrace where she spots a man. Sentence (iv) details the man's posture against the parapet. Thus, the coherent sequence is (iii), (ii), (i), (iv).",
        "question_text_latex": "Which one of the following sentence sequences creates a coherent narrative?\n\\begin{enumerate}[label=(\\roman*),itemsep=0pt,topsep=2pt]\n\\item Once on the terrace, on her way to her small room in the corner, she notices the man right away.\n\\item She begins to pant by the time she has climbed all the stairs.\n\\item Mina has bought vegetables and rice at the market, so her bags are heavy.\n\\item He was leaning against the parapet, watching the traffic below.\n\\end{enumerate}",
        "options_latex": {
            "A": "(i), (ii), (iv), (iii)",
            "B": "(ii), (iii), (i), (iv)",
            "C": "(iv), (ii), (i), (iii)",
            "D": "(iii), (ii), (i), (iv)"
        }
    },
    "2023_CS_GA_Q09": {
        "topic": "Quantitative Aptitude",
        "subtopic": "Numerical computation and estimation: ratios, percentages, powers, exponents and logarithms, permutations and combinations, series",
        "difficulty_level": "Easy",
        "explaination": "We are given $f(x) = g(y)$ for all independent real variables $x$ and $y$. If $x$ varies while $y$ remains constant, $f(x)$ cannot change because $g(y)$ is fixed, meaning $f(x)$ must be a constant. Symmetrically, $g(y)$ must be identical to that same constant. Therefore, $f(x) = g(y) = \\text{constant}$.",
        "question_text_latex": "$f(x)$ and $g(y)$ are functions of $x$ and $y$, respectively, and $f(x) = g(y)$ for all real values of $x$ and $y$. Which one of the following options is necessarily TRUE for all $x$ and $y$?",
        "options_latex": {
            "A": "$f(x) = 0$ and $g(y) = 0$",
            "B": "$f(x) = g(y) = \\text{constant}$",
            "C": "$f(x) \\neq \\text{constant}$ and $g(y) \\neq \\text{constant}$",
            "D": "$f(x) + g(y) = f(x) - g(y)$"
        }
    },
    "2023_CS_GA_Q10": {
        "topic": "Spatial Aptitude",
        "subtopic": "Transformation of shapes: translation, rotation, scaling, mirroring, assembling, and grouping",
        "difficulty_level": "Medium",
        "explaination": "Analyzing the rigid 2D planar transformations from figure P to Q and Q to R shows that statement S1 accurately describes the sequence of planar rotation and reflection, while statements S2 and S3 fail to match the observed geometric orientations. Hence, only S1 is TRUE.",
        "question_text_latex": "Which one of the options best describes the transformation of the 2-dimensional figure P to Q, and then to R, as shown?",
        "options_latex": {
            "A": "Only S1 is TRUE.",
            "B": "Only S1 and S2 are TRUE.",
            "C": "S1, S2, and S3 are all TRUE.",
            "D": "Only S1 and S3 are TRUE."
        }
    },

    # ==================== CS 1-MARK ====================
    "2023_CS_CS_Q12": {
        "topic": "Programming and Data Structures",
        "subtopic": "Trees, binary search trees, binary heaps",
        "difficulty_level": "Easy",
        "explaination": "In a 1-indexed max-heap, every node at index $i$ must satisfy $A[i] \\ge A[2i]$ and $A[i] \\ge A[2i+1]$. For sequence B $[23, 17, 14, 7, 13, 10, 1, 5, 6, 12]$: $A[1]=23 \\ge A[2]=17, A[3]=14$; $A[2]=17 \\ge A[4]=7, A[5]=13$; $A[3]=14 \\ge A[6]=10, A[7]=1$; $A[4]=7 \\ge A[8]=5, A[9]=6$; $A[5]=13 \\ge A[10]=12$. Every parent is greater than or equal to its children, forming a valid max-heap.",
        "question_text_latex": "Which one of the following sequences when stored in an array at locations $A[1], \\dots, A[10]$ forms a max-heap?",
        "options_latex": {
            "A": "23, 17, 10, 6, 13, 14, 1, 5, 7, 12",
            "B": "23, 17, 14, 7, 13, 10, 1, 5, 6, 12",
            "C": "23, 17, 14, 6, 13, 10, 1, 5, 7, 15",
            "D": "23, 14, 17, 1, 10, 13, 16, 12, 7, 5"
        }
    },
    "2023_CS_CS_Q13": {
        "topic": "Programming and Data Structures",
        "subtopic": "Arrays, stacks, queues, linked lists",
        "difficulty_level": "Easy",
        "explaination": "In a singly-linked list, deleting a given node requires finding its predecessor node to bypass it, requiring an $\\mathcal{O}(n)$ traversal from the head in the worst case. In a doubly-linked list, each node directly points to its predecessor (`node->prev`), allowing immediate pointer adjustments in $\\mathcal{O}(1)$ time.",
        "question_text_latex": "Let `SLLdel` be a function that deletes a node in a singly-linked list given a pointer to the node and a pointer to the head of the list. Similarly, let `DLLdel` be another function that deletes a node in a doubly-linked list given a pointer to the node and a pointer to the head of the list.\nLet $n$ denote the number of nodes in each of the linked lists. Which one of the following choices is TRUE about the worst-case time complexity of `SLLdel` and `DLLdel`?",
        "options_latex": {
            "A": "`SLLdel` is $\\mathcal{O}(1)$ and `DLLdel` is $\\mathcal{O}(n)$",
            "B": "Both `SLLdel` and `DLLdel` are $\\mathcal{O}(\\log n)$",
            "C": "Both `SLLdel` and `DLLdel` are $\\mathcal{O}(1)$",
            "D": "`SLLdel` is $\\mathcal{O}(n)$ and `DLLdel` is $\\mathcal{O}(1)$"
        }
    },
    "2023_CS_CS_Q15": {
        "topic": "Discrete Mathematics",
        "subtopic": "Combinatorics: counting, recurrence relations, generating functions",
        "difficulty_level": "Medium",
        "explaination": "The recurrence $L_n = L_{n-1} + L_{n-2}$ has characteristic equation $r^2 - r - 1 = 0$, giving roots $r_1, r_2 = \\frac{1 \\pm \\sqrt{5}}{2}$. The general solution is $L_n = c_1 \\left(\\frac{1+\\sqrt{5}}{2}\\right)^n + c_2 \\left(\\frac{1-\\sqrt{5}}{2}\\right)^n$. Substituting initial conditions $L_1 = 1$ and $L_2 = 3$ yields $c_1 = 1$ and $c_2 = 1$.",
        "question_text_latex": "The Lucas sequence $L_n$ is defined by the recurrence relation:\n\\[ L_n = L_{n-1} + L_{n-2}, \\quad \\text{for } n \\ge 3, \\]\nwith $L_1 = 1$ and $L_2 = 3$.\nWhich one of the options given is TRUE?",
        "options_latex": {
            "A": "$L_n = \\left(\\frac{1+\\sqrt{5}}{2}\\right)^n + \\left(\\frac{1-\\sqrt{5}}{2}\\right)^n$",
            "B": "$L_n = \\left(\\frac{1+\\sqrt{5}}{2}\\right)^n - \\left(\\frac{1-\\sqrt{5}}{3}\\right)^n$",
            "C": "$L_n = \\left(\\frac{1+\\sqrt{5}}{2}\\right)^n + \\left(\\frac{1-\\sqrt{5}}{3}\\right)^n$",
            "D": "$L_n = \\left(\\frac{1+\\sqrt{5}}{2}\\right)^n - \\left(\\frac{1-\\sqrt{5}}{2}\\right)^n$"
        }
    },
    "2023_CS_CS_Q16": {
        "topic": "Databases",
        "subtopic": "Relational model: relational algebra, tuple calculus, SQL",
        "difficulty_level": "Easy",
        "explaination": "In relational database theory, the degree (or arity) of a relation is defined as the number of attributes (columns) in its relation schema, whereas the cardinality of a relation is the number of tuples (rows).",
        "question_text_latex": "Which one of the options given below refers to the degree (or arity) of a relation in relational database systems?",
        "options_latex": {
            "A": "Number of attributes of its relation schema.",
            "B": "Number of tuples stored in the relation.",
            "C": "Number of entries in the relation.",
            "D": "Number of distinct domains of its relation schema."
        }
    },
    "2023_CS_CS_Q17": {
        "topic": "Computer Networks",
        "subtopic": "Transport layer: flow control and congestion control, UDP, TCP, sockets",
        "difficulty_level": "Medium",
        "explaination": "Link utilization in Stop-and-Wait is $\\eta = \\frac{1}{1 + 2a}$, where $a = \\frac{T_{\\text{prop}}}{T_{\\text{trans}}} = \\frac{d/v}{L/B} = \\frac{d \\cdot B}{v \\cdot L}$. Utilization $\\eta$ is lowest when parameter $a$ is maximized, which occurs when the link length $d$ is longer (increasing propagation delay) and the transmission rate $B$ is higher (decreasing packet transmission time).",
        "question_text_latex": "Suppose two hosts are connected by a point-to-point link and they are configured to use Stop-and-Wait protocol for reliable data transfer. Identify in which one of the following scenarios, the utilization of the link is the lowest.",
        "options_latex": {
            "A": "Longer link length and lower transmission rate",
            "B": "Longer link length and higher transmission rate",
            "C": "Shorter link length and lower transmission rate",
            "D": "Shorter link length and higher transmission rate"
        }
    },
    "2023_CS_CS_Q18": {
        "topic": "Linear Algebra",
        "subtopic": "Matrices, determinants",
        "difficulty_level": "Easy",
        "explaination": "Matrix $B$ is obtained from matrix $A$ by interchanging row 1 and row 3 ($R_1 \\leftrightarrow R_3$), leaving all other rows unchanged. By the elementary row operation property of determinants, swapping any two rows of a square matrix negates its determinant: $\\det(B) = -\\det(A)$.",
        "question_text_latex": "Let\n\\[ A = \\begin{bmatrix} 1 & 2 & 3 & 4 \\\\ 4 & 1 & 2 & 3 \\\\ 3 & 4 & 1 & 2 \\\\ 2 & 3 & 4 & 1 \\end{bmatrix} \\quad \\text{and} \\quad B = \\begin{bmatrix} 3 & 4 & 1 & 2 \\\\ 4 & 1 & 2 & 3 \\\\ 1 & 2 & 3 & 4 \\\\ 2 & 3 & 4 & 1 \\end{bmatrix}. \\]\nLet $\\det(A)$ and $\\det(B)$ denote the determinants of the matrices $A$ and $B$, respectively.\nWhich one of the options given below is TRUE?",
        "options_latex": {
            "A": "$\\det(A) = \\det(B)$",
            "B": "$\\det(B) = -\\det(A)$",
            "C": "$\\det(A) = 0$",
            "D": "$\\det(AB) = \\det(A) + \\det(B)$"
        }
    },
    "2023_CS_CS_Q20": {
        "topic": "Algorithms",
        "subtopic": "Searching, sorting, hashing",
        "difficulty_level": "Easy",
        "explaination": "In universal hashing, the hash function is chosen uniformly at random from a carefully designed universal collection of hash functions independently of the keys. Because the adversary cannot predict which function will be selected at runtime, any fixed choice of malicious keys cannot guarantee worst-case collision behavior.",
        "question_text_latex": "An algorithm has to store several keys generated by an adversary in a hash table. The adversary is malicious who tries to maximize the number of collisions. Let $k$ be the number of keys, $m$ be the number of slots in the hash table, and $k > m$.\nWhich one of the following is the best hashing strategy to counteract the adversary?",
        "options_latex": {
            "A": "Division method, i.e., use the hash function $h(k) = k \\bmod m$.",
            "B": "Multiplication method, i.e., use the hash function $h(k) = \\lfloor m(kA - \\lfloor kA \\rfloor)\\rfloor$, where $A$ is a carefully chosen constant.",
            "C": "Universal hashing method.",
            "D": "If $k$ is a prime number, use Division method. Otherwise, use Multiplication method."
        }
    },
    "2023_CS_CS_Q22": {
        "topic": "Operating System",
        "subtopic": "System calls, processes, threads, inter-process communication",
        "difficulty_level": "Easy",
        "explaination": "Threads of the same process share the process address space, open files, and the page table base register (PTBR is not switched). However, each thread has its own private thread control block (TCB) maintaining its program counter, stack pointer, and general purpose CPU registers, which must be saved during a thread context switch.",
        "question_text_latex": "Which one or more of the following need to be saved on a context switch from one thread (T1) of a process to another thread (T2) of the same process?",
        "options_latex": {
            "A": "Page table base register",
            "B": "Stack pointer",
            "C": "Program counter",
            "D": "General purpose registers"
        }
    },
    "2023_CS_CS_Q23": {
        "topic": "Operating System",
        "subtopic": "System calls, processes, threads, inter-process communication",
        "difficulty_level": "Easy",
        "explaination": "A transition to kernel mode is triggered by traps, exceptions, or hardware interrupts. A Page Fault is a hardware exception handled exclusively by the OS kernel (C is true). A System Call issues an explicit software trap instruction switching the CPU to kernel mode (D is true). Standard user-space function calls and `malloc` execute in user mode without inherently causing a mode transition.",
        "question_text_latex": "Which one or more of the following options guarantee that a computer system will transition from user mode to kernel mode?",
        "options_latex": {
            "A": "Function Call",
            "B": "`malloc` Call",
            "C": "Page Fault",
            "D": "System Call"
        }
    },
    "2023_CS_CS_Q24": {
        "topic": "Theory of Computation",
        "subtopic": "Regular and context-free languages, pumping lemma",
        "difficulty_level": "Easy",
        "explaination": "Regular languages, recursive languages, and recursively enumerable languages are all closed under intersection (A, C, and D are CORRECT). Context-free languages are not closed under intersection; for example, $L_1 = \\{a^n b^n c^m\\}$ and $L_2 = \\{a^m b^n c^n\\}$ are both CFLs, but $L_1 \\cap L_2 = \\{a^n b^n c^n\\}$ is not context-free.",
        "question_text_latex": "Which of the following statements is/are CORRECT?",
        "options_latex": {
            "A": "The intersection of two regular languages is regular.",
            "B": "The intersection of two context-free languages is context-free.",
            "C": "The intersection of two recursive languages is recursive.",
            "D": "The intersection of two recursively enumerable languages is recursively enumerable."
        }
    },
    "2023_CS_CS_Q25": {
        "topic": "Computer Networks",
        "subtopic": "Routing protocols: shortest path, flooding, distance vector and link state routing",
        "difficulty_level": "Easy",
        "explaination": "OSPF is an intra-domain (Interior Gateway) routing protocol that uses Dijkstra's link-state algorithm (not Bellman-Ford, which is used by distance-vector protocols like RIP). Therefore, statement A (implements Bellman-Ford) and statement C (used as inter-domain) are INCORRECT, which are the required answers.",
        "question_text_latex": "Which of the following statements is/are INCORRECT about the OSPF (Open Shortest Path First) routing protocol used in the Internet?",
        "options_latex": {
            "A": "OSPF implements Bellman-Ford algorithm to find shortest paths.",
            "B": "OSPF uses Dijkstra's shortest path algorithm to implement least-cost path routing.",
            "C": "OSPF is used as an inter-domain routing protocol.",
            "D": "OSPF implements hierarchical routing."
        }
    },
    "2023_CS_CS_Q26": {
        "topic": "Discrete Mathematics",
        "subtopic": "Propositional and first order logic",
        "difficulty_level": "Medium",
        "explaination": "Geetha's conjecture states $\\forall x [P(x) \\implies \\exists y Q(x, y)]$. Statement B ($\\forall x \\forall y Q(x, y)$) asserts $Q(x, y)$ holds for every pair, directly implying $\\exists y Q(x, y)$ and therefore making the implication true for all $x$. Statement C ($\\exists y \\forall x [P(x) \\implies Q(x, y)]$) provides a single $y$ that satisfies the implication for every $x$, which immediately implies that such a $y$ exists for each $x$.",
        "question_text_latex": "Geetha has a conjecture about integers, which is of the form\n\\[ \\forall x \\, [P(x) \\implies \\exists y \\, Q(x, y)], \\]\nwhere $P$ is a statement about integers, and $Q$ is a statement about pairs of integers. Which of the following (one or more) option(s) would imply Geetha's conjecture?",
        "options_latex": {
            "A": "$\\exists x \\, [P(x) \\land \\forall y \\, Q(x, y)]$",
            "B": "$\\forall x \\forall y \\, Q(x, y)$",
            "C": "$\\exists y \\forall x \\, [P(x) \\implies Q(x, y)]$",
            "D": "$\\exists x \\, [P(x) \\land \\exists y \\, Q(x, y)]$"
        }
    },
    "2023_CS_CS_Q27": {
        "topic": "Operating System",
        "subtopic": "CPU and I/O scheduling",
        "difficulty_level": "Easy",
        "explaination": "Priority Scheduling can cause starvation for low-priority processes if higher-priority processes arrive continuously (C). Shortest Job First (SJF) starves long burst jobs when short jobs arrive continuously (D). Under certain interpretations where FIFO queues suffer convoy effects or indefinitely waiting jobs in specific priority variants, FIFO was also credited, hence GATE accepted {C, D} or {A, C, D}. Round Robin provides bounded waiting and prevents starvation.",
        "question_text_latex": "Which one or more of the following CPU scheduling algorithms can potentially cause starvation?",
        "options_latex": {
            "A": "First-in First-Out",
            "B": "Round Robin",
            "C": "Priority Scheduling",
            "D": "Shortest Job First"
        }
    },
    "2023_CS_CS_Q28": {
        "topic": "Calculus",
        "subtopic": "Maxima and minima",
        "difficulty_level": "Easy",
        "explaination": "Setting $f'(x) = 3x^2 + 30x - 33 = 3(x+11)(x-1) = 0$ yields critical points $x = -11$ and $x = 1$. The second derivative is $f''(x) = 6x + 30$. Since $f''(-11) = -36 < 0$, $x = -11$ is a local maximum (B is TRUE). Since $f''(1) = 36 > 0$, $x = 1$ is a local minimum (D is TRUE).",
        "question_text_latex": "Let\n\\[ f(x) = x^3 + 15x^2 - 33x - 36 \\]\nbe a real-valued function.\nWhich of the following statements is/are TRUE?",
        "options_latex": {
            "A": "$f(x)$ does not have a local maximum.",
            "B": "$f(x)$ has a local maximum.",
            "C": "$f(x)$ does not have a local minimum.",
            "D": "$f(x)$ has a local minimum."
        }
    },
    "2023_CS_CS_Q29": {
        "topic": "Algorithms",
        "subtopic": "Asymptotic worst case time and space complexity",
        "difficulty_level": "Easy",
        "explaination": "For $f(n) = n$ and $g(n) = n^2$, we evaluate $\\lim_{n \\to \\infty} \\frac{f(n)}{g(n)} = \\lim_{n \\to \\infty} \\frac{1}{n} = 0$. By definition, if the limit is 0, $f(n) \\in o(g(n))$, which strictly implies $f(n) \\in \\mathcal{O}(g(n))$. Hence, both A and C are TRUE.",
        "question_text_latex": "Let $f$ and $g$ be functions of natural numbers given by $f(n) = n$ and $g(n) = n^2$.\nWhich of the following statements is/are TRUE?",
        "options_latex": {
            "A": "$f \\in \\mathcal{O}(g)$",
            "B": "$f \\in \\Omega(g)$",
            "C": "$f \\in o(g)$",
            "D": "$f \\in \\Theta(g)$"
        }
    },
    "2023_CS_CS_Q31": {
        "topic": "Calculus",
        "subtopic": "Integration",
        "difficulty_level": "Easy",
        "explaination": "The integral splits into $\\int_{-3}^3 \\int_{-2}^2 \\int_{-1}^1 4x^2 y \\, dz \\, dy \\, dx - \\int_{-3}^3 \\int_{-2}^2 \\int_{-1}^1 z^3 \\, dz \\, dy \\, dx$. The first integral is zero because $y$ is an odd function integrated over symmetric limits $[-2, 2]$. The second integral is zero because $z^3$ is an odd function integrated over symmetric limits $[-1, 1]$. Thus, the total value is $0 - 0 = 0$.",
        "question_text_latex": "The value of the definite integral\n\\[ \\int_{-3}^3 \\int_{-2}^2 \\int_{-1}^1 (4x^2 y - z^3) \\, dz \\, dy \\, dx \\]\nis \\_\\_\\_\\_\\_\\_\\_\\_\\. (Rounded off to the nearest integer)",
        "options_latex": None
    },
    "2023_CS_CS_Q32": {
        "topic": "Digital Logic",
        "subtopic": "Number representations and computer arithmetic (fixed and floating point)",
        "difficulty_level": "Easy",
        "explaination": "Converting $132_4$ to base 10: $1 \\times 4^2 + 3 \\times 4^1 + 2 \\times 4^0 = 16 + 12 + 2 = 30_{10}$. Converting $30_{10}$ to radix 5: $30 = 6 \\times 5 + 0$, $6 = 1 \\times 5 + 1$, $1 = 0 \\times 5 + 1$. Reading remainders from bottom to top yields $110_5$.",
        "question_text_latex": "A particular number is written as 132 in radix-4 representation. The same number in radix-5 representation is \\_\\_\\_\\_\\_\\_\\_\\_\\. (Answer in integer)",
        "options_latex": None
    },
    "2023_CS_CS_Q33": {
        "topic": "Computer Organization and Architecture",
        "subtopic": "Instruction pipelining, pipeline hazards",
        "difficulty_level": "Easy",
        "explaination": "The clock period of the pipeline is governed by the longest stage delay: $T = \\max(10, 20, 14) = 20\\text{ ns}$. For an ideal $k$-stage pipeline executing $n$ instructions, the total execution time is $(k + n - 1) \\times T$. For $k = 3$ and $n = 100$: $(3 + 100 - 1) \\times 20 = 102 \\times 20 = 2040\\text{ ns}$.",
        "question_text_latex": "Consider a 3-stage pipelined processor having a delay of 10 ns (nanoseconds), 20 ns, and 14 ns, for the first, second, and the third stages, respectively. Assume that there is no other delay and the processor does not suffer from any pipeline hazards. Also assume that one instruction is fetched every cycle.\nThe total execution time for executing 100 instructions on this processor is \\_\\_\\_\\_\\_\\_\\_\\_\\_ ns. (Answer in integer)",
        "options_latex": None
    },
    "2023_CS_CS_Q34": {
        "topic": "Computer Organization and Architecture",
        "subtopic": "I/O interface: interrupt and DMA mode",
        "difficulty_level": "Medium",
        "explaination": "With polling every $10\\text{ ms}$, there are 100 polls per second. Polling overhead is $100 \\times 100\\ \\mu\\text{s} = 10000\\ \\mu\\text{s} = 10\\text{ ms}$. With 1 keystroke/s, processing takes $200\\ \\mu\\text{s} = 0.2\\text{ ms}$, giving $T_1 = 10 + 0.2 = 10.2\\text{ ms}$. In interrupt-driven mode, 1 interrupt per second takes $1\\text{ ms}$, giving $T_2 = 1\\text{ ms}$. The ratio is $\\frac{T_1}{T_2} = \\frac{10.2}{1.0} = 10.2$.",
        "question_text_latex": "A keyboard connected to a computer is used at a rate of 1 keystroke per second. The computer system polls the keyboard every 10 ms (milli seconds) to check for a keystroke and consumes 100 $\\mu$s (micro seconds) for each poll. If it is determined after polling that a key has been pressed, the system consumes an additional 200 $\\mu$s to process the keystroke. Let $T_1$ denote the fraction of a second spent in polling and processing a keystroke.\nIn an alternative implementation, the system uses interrupts instead of polling. An interrupt is raised for every keystroke. It takes a total of 1 ms for servicing an interrupt and processing a keystroke. Let $T_2$ denote the fraction of a second spent in servicing the interrupt and processing a keystroke.\nThe ratio $\\frac{T_1}{T_2}$ is \\_\\_\\_\\_\\_\\_\\_\\_\\. (Rounded off to one decimal place)",
        "options_latex": None
    },
    "2023_CS_CS_Q35": {
        "topic": "Programming and Data Structures",
        "subtopic": "Programming in C",
        "difficulty_level": "Easy",
        "explaination": "In `funcp()`, the static variable $x$ persists across invocations. On first call `x = funcp()`, static $x$ increments from 1 to 2 and returns 2, setting local $x = 2$. In `y = funcp() + x`, `funcp()` increments static $x$ from 2 to 3 and returns 3, so $y = 3 + 2 = 5$. Finally, `printf` prints $x + y = 2 + 5 = 7$.",
        "question_text_latex": "The integer value printed by the ANSI-C program given below is \\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\. (Answer in integer)\n\\begin{lstlisting}[language=C]\n#include <stdio.h>\nint funcp() {\n    static int x = 1;\n    x++;\n    return x;\n}\nint main() {\n    int x, y;\n    x = funcp();\n    y = funcp() + x;\n    printf(\"%d\\n\", (x + y));\n    return 0;\n}\n\\end{lstlisting}",
        "options_latex": None
    },
    "2023_CS_CS_Q36": {
        "topic": "Compiler Design",
        "subtopic": "Runtime environments",
        "difficulty_level": "Medium",
        "explaination": "In `main()`, the calls are `f1()`, `f2(2)`, and `f3()` as direct children. Inside `f2(2)`, it invokes `f3()` first, then because $X=2 \\neq 1$, recursively invokes `f2(1)`. Inside `f2(1)`, it invokes `f3()` first, and then since $X=1$, invokes `f1()`. This call sequence maps directly to the tree structure in option A.",
        "question_text_latex": "Consider the following program:\n\\begin{lstlisting}[language=C]\nint main() {\n    f1();\n    f2(2);\n    f3();\n    return(0);\n}\nint f1() {\n    return(1);\n}\nint f2(int X) {\n    f3();\n    if (X == 1)\n        return f1();\n    else\n        return (X * f2(X - 1));\n}\nint f3() {\n    return(5);\n}\n\\end{lstlisting}\nWhich one of the following options represents the activation tree corresponding to the main function?",
        "options_latex": {
            "A": "main -> [f1, f2, f3]; where f2(2) -> [f3, f2(1)]; and f2(1) -> [f3, f1]",
            "B": "main -> [f2, f3]; where f2 -> [f1, f1, f3]",
            "C": "main -> [f2]; where f2 -> [f1, f3, f1]",
            "D": "main -> [f1, f2, f3]; where f2 -> [f3, f2, f1]"
        }
    },

    # ==================== CS 2-MARK ====================
    "2023_CS_CS_Q38": {
        "topic": "Operating System",
        "subtopic": "Concurrency and synchronization",
        "difficulty_level": "Medium",
        "explaination": "With binary semaphore $s=1$ (I-1), mutual exclusion guarantees serialized critical section access, yielding net change $+5 - 3 = +2 \\implies V_1 = 10 + 2 = 12$. With counting semaphore $s=2$ (I-2), two threads can enter simultaneously; a decrement thread can read $X=10$, be preempted while all 5 increments and 2 decrements complete, and then write back $10-1 = 9$, repeatedly clobbering increments to achieve minimum $V_2 = 10 - 3 = 7$.",
        "question_text_latex": "Consider the two functions `incr` and `decr` shown below:\n\\begin{lstlisting}[language=C]\nincr() {\n    wait(s);\n    X = X + 1;\n    signal(s);\n}\ndecr() {\n    wait(s);\n    X = X - 1;\n    signal(s);\n}\n\\end{lstlisting}\nThere are 5 threads each invoking `incr` once, and 3 threads each invoking `decr` once, on the same shared variable $X$. The initial value of $X$ is 10.\nSuppose there are two implementations of the semaphore $s$, as follows:\n\\begin{itemize}[itemsep=0pt,topsep=2pt]\n\\item I-1: $s$ is a binary semaphore initialized to 1.\n\\item I-2: $s$ is a counting semaphore initialized to 2.\n\\end{itemize}\nLet $V_1, V_2$ be the values of $X$ at the end of execution of all the threads with implementations I-1, I-2, respectively.\nWhich one of the following choices corresponds to the minimum possible values of $V_1, V_2$, respectively?",
        "options_latex": {
            "A": "15, 7",
            "B": "7, 7",
            "C": "12, 7",
            "D": "12, 8"
        }
    },
    "2023_CS_CS_Q39": {
        "topic": "Theory of Computation",
        "subtopic": "Context-free grammars and push-down automata",
        "difficulty_level": "Medium",
        "explaination": "The subgrammar $X \\to aX \\mid Xb \\mid a \\mid b$ derives all non-empty strings with any number of $a$'s followed by any number of $b$'s having at least one $a$ or $b$, described by $a^*(a+b)b^*$. Rule $S \\to aSb \\mid X$ prefixes $k$ $a$'s and suffixes $k$ $b$'s ($k \\ge 0$), yielding $a^k a^*(a+b)b^* b^k = a^*(a+b)b^*$. Because this language is represented by a regular expression, it is a regular language.",
        "question_text_latex": "Consider the context-free grammar $G$ below:\n\\begin{align*}\nS &\\to aSb \\mid X \\\\\nX &\\to aX \\mid Xb \\mid a \\mid b,\n\\end{align*}\nwhere $S$ and $X$ are non-terminals, and $a$ and $b$ are terminal symbols. The starting non-terminal is $S$.\nWhich one of the following statements is CORRECT?",
        "options_latex": {
            "A": "The language generated by $G$ is $(a + b)^*$",
            "B": "The language generated by $G$ is $a^*(a + b)b^*$",
            "C": "The language generated by $G$ is $a^*b^*(a + b)$",
            "D": "The language generated by $G$ is not a regular language"
        }
    },
    "2023_CS_CS_Q41": {
        "topic": "Computer Organization and Architecture",
        "subtopic": "Machine instructions and addressing modes",
        "difficulty_level": "Medium",
        "explaination": "Multiplying by 8 corresponds to shifting left by 3 bits ($2^3 = 8$), so $U_1 = 3$. Since elements are 32-bit (4-byte) integers in byte-addressable memory, the pointers in registers `r3` and `r4` must advance by 4 bytes each iteration, so $U_2 = 4$ and $U_3 = 4$. Finally, the loop branches back to the condition check at label $L_{01}$, so $U_4 = L_{01}$.",
        "question_text_latex": "Consider the given C-code and its corresponding assembly code, with a few operands U1--U4 being unknown. Some useful information as well as the semantics of each unique assembly instruction is annotated as inline comments in the code. The memory is byte-addressable.\n\\begin{lstlisting}[language=C]\n// C-code\nint a[10], b[10], i;    // int is 32-bit\nfor (i = 0; i < 10; i++)\n    a[i] = b[i] * 8;\n\\end{lstlisting}\n\\begin{lstlisting}\n; assembly-code (; indicates comments)\n; r1-r5 are 32-bit integer registers\n; initialize r1=0, r2=10\n; initialize r3, r4 with base address of a, b\nL01: jeq r1, r2, end    ; if(r1==r2) goto end\nL02: lw  r5, 0(r4)      ; r5 <- Memory[r4+0]\nL03: shl r5, r5, U1     ; r5 <- r5 << U1\nL04: sw  r5, 0(r3)      ; Memory[r3+0] <- r5\nL05: add r3, r3, U2     ; r3 <- r3+U2\nL06: add r4, r4, U3\nL07: add r1, r1, 1\nL08: jmp U4             ; goto U4\nL09: end\n\\end{lstlisting}\nWhich one of the following options is a CORRECT replacement for operands in the position (U1, U2, U3, U4) in the above assembly code?",
        "options_latex": {
            "A": "(8, 4, 1, L02)",
            "B": "(3, 4, 4, L01)",
            "C": "(8, 1, 1, L02)",
            "D": "(3, 1, 1, L01)"
        }
    },
    "2023_CS_CS_Q45": {
        "topic": "Digital Logic",
        "subtopic": "Number representations and computer arithmetic (fixed and floating point)",
        "difficulty_level": "Medium",
        "explaination": "Number $P = \\text{0xC1800000}$ has sign bit 1, biased exponent $131$, actual exponent $131 - 127 = 4$, and mantissa $1.0$, so $P = -16.0 = -2^4$. Number $Q = \\text{0x3F5C2EF4}$ is positive with biased exponent $126$ (exponent $-1$) and mantissa fraction `5C2EF4`. Multiplying $P \\times Q$ flips the sign to negative (1), adds 4 to the exponent (biased exponent becomes $126 + 4 = 130 = \\text{0x82}$), and retains the mantissa fraction, resulting in `0xC15C2EF4`.",
        "question_text_latex": "Consider the IEEE-754 single precision floating point numbers $P = \\text{0xC1800000}$ and $Q = \\text{0x3F5C2EF4}$.\nWhich one of the following corresponds to the product of these numbers (i.e., $P \\times Q$), represented in the IEEE-754 single precision format?",
        "options_latex": {
            "A": "0x404C2EF4",
            "B": "0x405C2EF4",
            "C": "0xC15C2EF4",
            "D": "0xC14C2EF4"
        }
    },
    "2023_CS_CS_Q46": {
        "topic": "Programming and Data Structures",
        "subtopic": "Trees, binary search trees, binary heaps",
        "difficulty_level": "Easy",
        "explaination": "In a binary max-heap of $n$ elements, `Extract-Max` replaces the root with the last element and performs `maxHeapify` downward along the height $\\lfloor \\log_2 n \\rfloor$, running in $\\mathcal{O}(\\log n)$ worst-case time. `Insert` places the new key at the next leaf position and sifts upward along the height, also running in $\\mathcal{O}(\\log n)$ worst-case time.",
        "question_text_latex": "Let $A$ be a priority queue for maintaining a set of elements. Suppose $A$ is implemented using a max-heap data structure. The operation $\\text{Extract-Max}(A)$ extracts and deletes the maximum element from $A$. The operation $\\text{Insert}(A, \\text{key})$ inserts a new element $\\text{key}$ in $A$. The properties of a max-heap are preserved at the end of each of these operations.\nWhen $A$ contains $n$ elements, which one of the following statements about the worst case running time of these two operations is TRUE?",
        "options_latex": {
            "A": "Both `Extract-Max(A)` and `Insert(A,key)` run in $\\mathcal{O}(1)$.",
            "B": "Both `Extract-Max(A)` and `Insert(A,key)` run in $\\mathcal{O}(\\log n)$.",
            "C": "`Extract-Max(A)` runs in $\\mathcal{O}(1)$ whereas `Insert(A,key)` runs in $\\mathcal{O}(n)$.",
            "D": "`Extract-Max(A)` runs in $\\mathcal{O}(1)$ whereas `Insert(A,key)` runs in $\\mathcal{O}(\\log n)$."
        }
    },
    "2023_CS_CS_Q47": {
        "topic": "Programming and Data Structures",
        "subtopic": "Recursion",
        "difficulty_level": "Medium",
        "explaination": "Function `foo` performs post-order traversal, recursively summing `p->val + foo(p->left) + foo(p->right)` and printing each subtree sum. Leaf 3 prints 3; leaf 8 prints 8; node 5 sums $5 + 3 + 8 = 16$ (prints 16); leaf 13 prints 13; node 11 sums $11 + 0 + 13 = 24$ (prints 24); root 10 sums $10 + 16 + 24 = 50$ (prints 50). The printed output sequence is 3 8 16 13 24 50.",
        "question_text_latex": "Consider the C function `foo` and the binary tree shown:\n\\begin{lstlisting}[language=C]\ntypedef struct node {\n    int val;\n    struct node *left, *right;\n} node;\nint foo(node *p) {\n    int retval;\n    if (p == NULL)\n        return 0;\n    else {\n        retval = p->val + foo(p->left) + foo(p->right);\n        printf(\"%d \", retval);\n        return retval;\n    }\n}\n\\end{lstlisting}\nIn the binary tree, root is 10; its left child is 5 with children 3 and 8; its right child is 11 with right child 13.\nWhen `foo` is called with a pointer to the root node of the given binary tree, what will it print?",
        "options_latex": {
            "A": "3 8 5 13 11 10",
            "B": "3 5 8 10 11 13",
            "C": "3 8 16 13 24 50",
            "D": "3 16 8 50 24 13"
        }
    },
    "2023_CS_CS_Q48": {
        "topic": "Discrete Mathematics",
        "subtopic": "Combinatorics: counting, recurrence relations, generating functions",
        "difficulty_level": "Hard",
        "explaination": "There are 2 orderings for which block appears first ($A$ before $B$ or $B$ before $A$). There are $\\binom{n}{2k}$ ways to choose the positions in the permutation for elements of $A \\cup B$. The first $k$ chosen positions must contain elements of the first set ($k!$ permutations) and the next $k$ positions contain elements of the second set ($k!$ permutations). The remaining $n - 2k$ elements can be arranged in any of the $(n - 2k)!$ remaining positions. Total valid permutations $= 2 \\binom{n}{2k} (n - 2k)! (k!)^2$.",
        "question_text_latex": "Let $U = \\{1, 2, \\dots, n\\}$, where $n$ is a large positive integer greater than 1000. Let $k$ be a positive integer less than $n$. Let $A, B$ be subsets of $U$ with $|A| = |B| = k$ and $A \\cap B = \\emptyset$. We say that a permutation of $U$ separates $A$ from $B$ if one of the following is true:\n\\begin{itemize}[itemsep=0pt,topsep=2pt]\n\\item All members of $A$ appear in the permutation before any of the members of $B$.\n\\item All members of $B$ appear in the permutation before any of the members of $A$.\n\\end{itemize}\nHow many permutations of $U$ separate $A$ from $B$?",
        "options_latex": {
            "A": "$n!$",
            "B": "$\\binom{n}{2k} (n - 2k)!$",
            "C": "$\\binom{n}{2k} (n - 2k)! (k!)^2$",
            "D": "$2 \\binom{n}{2k} (n - 2k)! (k!)^2$"
        }
    },
    "2023_CS_CS_Q49": {
        "topic": "Discrete Mathematics",
        "subtopic": "Sets, relations, functions, partial orders and lattices",
        "difficulty_level": "Medium",
        "explaination": "By the fundamental theorem of equivalence relations and canonical function decomposition, $F([x]) = f(x)$ is well-defined and injective because $[x_1] = [x_2] \\iff f(x_1) = f(x_2)$ (C is TRUE). Because $f: A \\to B$ is surjective (onto), for every $b \\in B$, there exists $x \\in A$ such that $F([x]) = f(x) = b$, making $F$ surjective (B is TRUE). Since $F$ is both injective and surjective, it is a bijective function (D is TRUE).",
        "question_text_latex": "Let $f : A \\to B$ be an onto (or surjective) function, where $A$ and $B$ are nonempty sets. Define an equivalence relation $\\sim$ on the set $A$ as\n\\[ a_1 \\sim a_2 \\quad \\text{if } f(a_1) = f(a_2), \\]\nwhere $a_1, a_2 \\in A$. Let $E = \\{[x] : x \\in A\\}$ be the set of all the equivalence classes under $\\sim$. Define a new mapping $F : E \\to B$ as\n\\[ F([x]) = f(x), \\]\nfor all the equivalence classes $[x]$ in $E$.\nWhich of the following statements is/are TRUE?",
        "options_latex": {
            "A": "$F$ is NOT well-defined.",
            "B": "$F$ is an onto (or surjective) function.",
            "C": "$F$ is a one-to-one (or injective) function.",
            "D": "$F$ is a bijective function."
        }
    },
    "2023_CS_CS_Q50": {
        "topic": "Computer Networks",
        "subtopic": "Transport layer: flow control and congestion control, UDP, TCP, sockets",
        "difficulty_level": "Hard",
        "explaination": "To prevent sequence number wraparound within the Maximum Segment Lifetime ($MSL = 2\\text{ min} = 120\\text{ s}$), the sequence number space $2^k$ must be at least the data bytes transmitted at line rate during MSL: $2^k \\ge \\frac{100 \\times 10^6\\text{ bps}}{8} \\times 120\\text{ s} = 1.5 \\times 10^9\\text{ bytes}$. Since $2^{30} \\approx 1.07 \\times 10^9 < 1.5 \\times 10^9$ and $2^{31} \\approx 2.15 \\times 10^9 > 1.5 \\times 10^9$, at least 31 bits are required. Thus, 32 bits, 34 bits, and 36 bits are all valid lengths.",
        "question_text_latex": "Suppose you are asked to design a new reliable byte-stream transport protocol like TCP. This protocol, named myTCP, runs over a 100 Mbps network with Round Trip Time of 150 milliseconds and the maximum segment lifetime of 2 minutes.\nWhich of the following is/are valid lengths of the Sequence Number field in the myTCP header?",
        "options_latex": {
            "A": "30 bits",
            "B": "32 bits",
            "C": "34 bits",
            "D": "36 bits"
        }
    },
    "2023_CS_CS_Q51": {
        "topic": "Discrete Mathematics",
        "subtopic": "Monoids, Groups",
        "difficulty_level": "Medium",
        "explaination": "Symmetric difference $\\Delta$ is associative on $2^X$. The identity element is the empty set $\\emptyset$, since $A \\Delta \\emptyset = A$. Every subset $A$ is its own inverse because $A \\Delta A = (A - A) \\cup (A - A) = \\emptyset$ (D is TRUE). Consequently, $(2^X, \\Delta)$ satisfies all group axioms, forming an abelian group where every element is self-inverse (A is TRUE).",
        "question_text_latex": "Let $X$ be a set and $2^X$ denote the powerset of $X$.\nDefine a binary operation $\\Delta$ on $2^X$ as follows:\n\\[ A \\Delta B = (A - B) \\cup (B - A). \\]\nLet $H = (2^X, \\Delta)$. Which of the following statements about $H$ is/are correct?",
        "options_latex": {
            "A": "$H$ is a group.",
            "B": "Every element in $H$ has an inverse, but $H$ is NOT a group.",
            "C": "For every $A \\in 2^X$, the inverse of $A$ is the complement of $A$.",
            "D": "For every $A \\in 2^X$, the inverse of $A$ is $A$."
        }
    },
    "2023_CS_CS_Q52": {
        "topic": "Computer Networks",
        "subtopic": "Application layer protocols: DNS, SMTP, HTTP, FTP, Email",
        "difficulty_level": "Hard",
        "explaination": "Resolving the URL via 3-tier iterative DNS requires $3\\text{ RTT}$. Initiating TCP connection and requesting the base HTML page requires $1 + 1 = 2\\text{ RTT}$, so the base HTML is received after $3 + 2 = 5\\text{ RTT}$. With persistent HTTP pipelining, all 10 objects are fetched in 1 round trip over the established connection, giving $5 + 1 = 6\\text{ RTT}$ (D is TRUE). With non-persistent HTTP and 5 parallel connections, fetching 10 objects takes 2 sequential batches; each batch takes $1\\text{ RTT (TCP)} + 1\\text{ RTT (HTTP)} = 2\\text{ RTT}$, adding $2 \\times 2 = 4\\text{ RTT}$, giving $5 + 4 = 9\\text{ RTT}$ (C is TRUE).",
        "question_text_latex": "Suppose in a web browser, you click on the `www.gate-2023.in` URL. The browser cache is empty. The IP address for this URL is not cached in your local host, so a DNS lookup is triggered (by the local DNS server deployed on your local host) over the 3-tier DNS hierarchy in an iterative mode. No resource records are cached anywhere across all DNS servers.\nLet RTT denote the round trip time between your local host and DNS servers in the DNS hierarchy. The round trip time between the local host and the web server hosting `www.gate-2023.in` is also equal to RTT. The HTML file associated with the URL is small enough to have negligible transmission time and negligible rendering time by your web browser, which references 10 equally small objects on the same web server.\nWhich of the following statements is/are CORRECT about the minimum elapsed time between clicking on the URL and your browser fully rendering it?",
        "options_latex": {
            "A": "7 RTTs, in case of non-persistent HTTP with 5 parallel TCP connections.",
            "B": "5 RTTs, in case of persistent HTTP with pipelining.",
            "C": "9 RTTs, in case of non-persistent HTTP with 5 parallel TCP connections.",
            "D": "6 RTTs, in case of persistent HTTP with pipelining."
        }
    },
    "2023_CS_CS_Q53": {
        "topic": "Probability and Statistics",
        "subtopic": "Conditional probability and Bayes theorem",
        "difficulty_level": "Easy",
        "explaination": "Sample space $S = \\{HH, HT, TH, TT\\}$. Events are $A = \\{HH\\}$, $B = \\{HH, HT\\}$, $C = \\{HH, TH\\}$. We have $P(B) = 1/2$, $P(C) = 1/2$, and $P(B \\cap C) = P(\\{HH\\}) = 1/4 = P(B)P(C)$, confirming $B$ and $C$ are independent (C is TRUE). By independence, $\\text{Prob}(B|C) = \\text{Prob}(B)$ (D is TRUE). $P(A \\cap B) = 1/4 \\neq P(A)P(B) = 1/8$, so $A$ and $B$ are dependent.",
        "question_text_latex": "Consider a random experiment where two fair coins are tossed. Let $A$ be the event that denotes HEAD on both the throws, $B$ be the event that denotes HEAD on the first throw, and $C$ be the event that denotes HEAD on the second throw.\nWhich of the following statements is/are TRUE?",
        "options_latex": {
            "A": "$A$ and $B$ are independent.",
            "B": "$A$ and $C$ are independent.",
            "C": "$B$ and $C$ are independent.",
            "D": "$\\text{Prob}(B|C) = \\text{Prob}(B)$"
        }
    },
    "2023_CS_CS_Q54": {
        "topic": "Algorithms",
        "subtopic": "Asymptotic worst case time and space complexity",
        "difficulty_level": "Easy",
        "explaination": "In Function 1, the inner loop executes $n + \\lfloor n/2 \\rfloor + \\lfloor n/4 \\rfloor + \\dots \\approx 2n$ times, which gives $f_1(n) = \\Theta(n)$. In Function 2, the loop runs $100n$ times, which gives $f_2(n) = \\Theta(n)$. Because both functions have exact linear asymptotic growth, $f_1(n) \\in \\Theta(f_2(n))$ (A is TRUE) and $f_1(n) \\in \\mathcal{O}(n)$ (D is TRUE).",
        "question_text_latex": "Consider functions Function 1 and Function 2 expressed in pseudocode as follows:\n\\begin{lstlisting}\n// Function 1\nwhile n > 1 do\n    for i = 1 to n do\n        x = x + 1;\n    end for\n    n = floor(n / 2);\nend while\n\n// Function 2\nfor i = 1 to 100 * n do\n    x = x + 1;\nend for\n\\end{lstlisting}\nLet $f_1(n)$ and $f_2(n)$ denote the number of times the statement ``$x = x + 1$'' is executed in Function 1 and Function 2, respectively.\nWhich of the following statements is/are TRUE?",
        "options_latex": {
            "A": "$f_1(n) \\in \\Theta(f_2(n))$",
            "B": "$f_1(n) \\in o(f_2(n))$",
            "C": "$f_1(n) \\in \\omega(f_2(n))$",
            "D": "$f_1(n) \\in \\mathcal{O}(n)$"
        }
    },
    "2023_CS_CS_Q55": {
        "topic": "Discrete Mathematics",
        "subtopic": "Graphs: connectivity, matching, colouring",
        "difficulty_level": "Medium",
        "explaination": "The greedy coloring strategy assigns to each vertex the lowest index color not used by any already-colored neighbor, guaranteeing that adjacent vertices receive distinct colors (proper coloring, so A is TRUE). Because any vertex has degree at most $\\Delta(G)$, at most $\\Delta(G)$ colors are forbidden at any step, ensuring that at most $\\Delta(G) + 1$ colors are ever needed (B is TRUE). Greedy coloring does not guarantee finding the minimum chromatic number.",
        "question_text_latex": "Let $G$ be a simple, finite, undirected graph with vertex set $\\{v_1, \\dots, v_n\\}$. Let $\\Delta(G)$ denote the maximum degree of $G$ and let $\\mathbb{N} = \\{1, 2, \\dots\\}$ denote the set of all possible colors. Color the vertices of $G$ using the following greedy strategy:\n\\begin{lstlisting}\nfor i = 1, ..., n\n    color(vi) <- min{j in N : no neighbour of vi is colored j}\n\\end{lstlisting}\nWhich of the following statements is/are TRUE?",
        "options_latex": {
            "A": "This procedure results in a proper vertex coloring of $G$.",
            "B": "The number of colors used is at most $\\Delta(G) + 1$.",
            "C": "The number of colors used is at most $\\Delta(G)$.",
            "D": "The number of colors used is equal to the chromatic number of $G$."
        }
    },
    "2023_CS_CS_Q56": {
        "topic": "Algorithms",
        "subtopic": "Graph traversals, minimum spanning trees, shortest paths",
        "difficulty_level": "Hard",
        "explaination": "The vertex set has $2^3 = 8$ vertices. An edge connects $A$ and $B$ iff $A \\subsetneq B$ or $B \\subsetneq A$. For the empty set $\\emptyset$, every non-empty subset $S \\subseteq U$ satisfies $\\emptyset \\subsetneq S$, meaning all 7 non-empty subsets are direct neighbors of $\\emptyset$ at BFS depth 1. A BFS starting at $\\emptyset$ must visit $\\emptyset$ first, and can then visit the 7 distance-1 neighbors in any of the $7! = 5040$ possible orderings.",
        "question_text_latex": "Let $U = \\{1, 2, 3\\}$. Let $2^U$ denote the powerset of $U$. Consider an undirected graph $G$ whose vertex set is $2^U$. For any $A, B \\in 2^U$, $(A, B)$ is an edge in $G$ if and only if (i) $A \\neq B$, and (ii) either $A \\subsetneq B$ or $B \\subsetneq A$. For any vertex $A$ in $G$, the set of all possible orderings in which the vertices of $G$ can be visited in a Breadth First Search (BFS) starting from $A$ is denoted by $B(A)$.\nIf $\\emptyset$ denotes the empty set, then the cardinality of $B(\\emptyset)$ is \\_\\_\\_\\_\\_\\_\\_\\_\\. (Answer in integer)",
        "options_latex": None
    },
    "2023_CS_CS_Q57": {
        "topic": "Operating System",
        "subtopic": "Memory management and virtual memory",
        "difficulty_level": "Hard",
        "explaination": "Array $D[128][128]$ has 16384 elements stored in row-major order. Each page holds 512 elements, so the array is partitioned into $16384 / 512 = 32$ pages. The nested loop accesses the array column by column ($j$ changes faster in $D[j][i]$), referencing all 32 pages sequentially in every column iteration. Because only 30 physical frames are available, LRU replaces the earliest page before a column pass finishes. Consequently, every page access across all 128 column passes causes a page fault: $128 \\times 32 = 4096$ page faults.",
        "question_text_latex": "Consider the following two-dimensional array $D$ in the C programming language, which is stored in row-major order:\n\\begin{lstlisting}[language=C]\nint D[128][128];\n\\end{lstlisting}\nDemand paging is used for allocating memory and each physical page frame holds 512 elements of the array $D$. The Least Recently Used (LRU) page-replacement policy is used by the operating system. A total of 30 physical page frames are allocated to a process which executes the following code snippet:\n\\begin{lstlisting}[language=C]\nfor (int i = 0; i < 128; i++)\n    for (int j = 0; j < 128; j++)\n        D[j][i] *= 10;\n\\end{lstlisting}\nThe number of page faults generated during the execution of this code snippet is \\_\\_\\_\\_\\_\\_\\_\\_\\. (Answer in integer)",
        "options_latex": None
    },
    "2023_CS_CS_Q58": {
        "topic": "Operating System",
        "subtopic": "Memory management and virtual memory",
        "difficulty_level": "Medium",
        "explaination": "Page size is $4\\text{ KB} = 2^{12}\\text{ bytes}$, which leaves $57 - 12 = 45\\text{ bits}$ for the page table hierarchy. Each page table holds $\\frac{4\\text{ KB}}{8\\text{ bytes}} = 512 = 2^9$ entries, so each level indexes 9 bits. The number of levels required to cover the 45 virtual page bits is $L = \\frac{45}{9} = 5$.",
        "question_text_latex": "Consider a computer system with 57-bit virtual addressing using multi-level tree-structured page tables with $L$ levels for virtual to physical address translation. The page size is 4 KB (1 KB = 1024 B) and a page table entry at any of the levels occupies 8 bytes.\nThe value of $L$ is \\_\\_\\_\\_\\_\\_\\_\\_\\. (Answer in integer)",
        "options_latex": None
    },
    "2023_CS_CS_Q59": {
        "topic": "Programming and Data Structures",
        "subtopic": "Arrays, stacks, queues, linked lists",
        "difficulty_level": "Medium",
        "explaination": "Operations trace: Push $[1, 5, 7, 8, 9, 2]$ to $S$ (top=2); enqueue $[1, 5, 7, 8, 9, 2]$ to $Q$ (front=1). Pop 2 from $S$ ($S=[1,5,7,8,9]$), dequeue 1 from $Q$ ($Q=[5,7,8,9,2]$); pop 9 from $S$ ($S=[1,5,7,8]$), dequeue 5 from $Q$ ($Q=[7,8,9,2]$). Repeating dequeue from $Q$ and push to $S$ 4 times moves $7, 8, 9, 2$ into $S$, making $S=[1,5,7,8,7,8,9,2]$. Finally, two pops remove 2 and 9, leaving 8 at the top of $S$.",
        "question_text_latex": "Consider a sequence $a$ of elements $a_0 = 1, a_1 = 5, a_2 = 7, a_3 = 8, a_4 = 9$, and $a_5 = 2$. The following operations are performed on a stack $S$ and a queue $Q$, both of which are initially empty:\n\\begin{enumerate}[label=\\Roman*.,itemsep=0pt,topsep=2pt]\n\\item push the elements of $a$ from $a_0$ to $a_5$ in that order into $S$.\n\\item enqueue the elements of $a$ from $a_0$ to $a_5$ in that order into $Q$.\n\\item pop an element from $S$.\n\\item dequeue an element from $Q$.\n\\item pop an element from $S$.\n\\item dequeue an element from $Q$.\n\\item dequeue an element from $Q$ and push the same element into $S$.\n\\item Repeat operation VII three times.\n\\item pop an element from $S$.\n\\item pop an element from $S$.\n\\end{enumerate}\nThe top element of $S$ after executing the above operations is \\_\\_\\_\\_\\_\\_\\_\\_\\. (Answer in integer)",
        "options_latex": None
    },
    "2023_CS_CS_Q60": {
        "topic": "Compiler Design",
        "subtopic": "Lexical analysis, parsing, syntax-directed translation",
        "difficulty_level": "Medium",
        "explaination": "For `10#011`: integer part `10` evaluates as $I.val = 2(1) + 0 = 2$. Fraction part `011` with right-recursive rules: lowest $F_3 \\to B(1) \\implies F_3.val = 0.5$; middle $F_2 \\to B(1) F_3 \\implies F_2.val = \\frac{1}{2}(1 + 0.5) = 0.75$; top $F \\to B(0) F_2 \\implies F.val = \\frac{1}{2}(0 + 0.75) = 0.375$. Total value $N.val = I.val + F.val = 2 + 0.375 = 2.375$.",
        "question_text_latex": "Consider the syntax directed translation given by the following grammar and semantic rules. Here $N, I, F$ and $B$ are non-terminals. $N$ is the starting non-terminal, and $\\#, 0$ and $1$ are lexical tokens corresponding to input letters ``\\#'', ``0'' and ``1'', respectively. $X.val$ denotes the synthesized attribute (a numeric value) associated with a non-terminal $X$. $I_1$ and $F_1$ denote occurrences of $I$ and $F$ on the right hand side of a production, respectively. For the tokens 0 and 1, $0.val = 0$ and $1.val = 1$.\n\\begin{align*}\nN &\\to I \\,\\#\\, F & N.val &= I.val + F.val \\\\\nI &\\to I_1 B & I.val &= (2 \\cdot I_1.val) + B.val \\\\\nI &\\to B & I.val &= B.val \\\\\nF &\\to B F_1 & F.val &= \\frac{1}{2}(B.val + F_1.val) \\\\\nF &\\to B & F.val &= \\frac{1}{2}B.val \\\\\nB &\\to 0 & B.val &= 0.val \\\\\nB &\\to 1 & B.val &= 1.val\n\\end{align*}\nThe value computed by the translation scheme for the input string `10#011` is \\_\\_\\_\\_\\_\\_\\_\\_\\. (Rounded off to three decimal places)",
        "options_latex": None
    },
    "2023_CS_CS_Q61": {
        "topic": "Databases",
        "subtopic": "Relational model: relational algebra, tuple calculus, SQL",
        "difficulty_level": "Easy",
        "explaination": "The query evaluates the WHERE clause condition `gender = 'F' AND marks > 65`. Among female students: Aliya (rollNum 2, marks 70) and Aliya (rollNum 3, marks 80) satisfy both conditions, whereas Swati (rollNum 5, marks 65) fails the strict inequality. Thus, exactly 2 rows are returned.",
        "question_text_latex": "Consider the following table named `Student` in a relational database. The primary key of this table is `rollNum`.\n\\begin{center}\n\\begin{tabular}{|c|c|c|c|}\n\\hline\n\\textbf{rollNum} & \\textbf{name} & \\textbf{gender} & \\textbf{marks} \\\\\n\\hline\n1 & Naman & M & 62 \\\\\n2 & Aliya & F & 70 \\\\\n3 & Aliya & F & 80 \\\\\n4 & James & M & 82 \\\\\n5 & Swati & F & 65 \\\\\n\\hline\n\\end{tabular}\n\\end{center}\nThe SQL query below is executed on this database:\n\\begin{lstlisting}[language=SQL]\nSELECT *\nFROM Student\nWHERE gender = 'F' AND marks > 65;\n\\end{lstlisting}\nThe number of rows returned by the query is \\_\\_\\_\\_\\_\\_\\_\\_\\. (Answer in integer)",
        "options_latex": None
    },
    "2023_CS_CS_Q63": {
        "topic": "Theory of Computation",
        "subtopic": "Regular expressions and finite automata",
        "difficulty_level": "Easy",
        "explaination": "The language contains all binary strings not containing `111`. The minimal DFA tracks consecutive 1s: state $q_0$ (0 consecutive 1s, start), state $q_1$ (1 consecutive 1), state $q_2$ (2 consecutive 1s), and state $q_3$ (trap state reached on 3rd consecutive 1). States $q_0, q_1, q_2$ are accepting states. Thus, exactly 4 states are required.",
        "question_text_latex": "Consider the language $L$ over the alphabet $\\{0, 1\\}$, given below:\n\\[ L = \\{w \\in \\{0, 1\\}^* \\mid w \\text{ does not contain three or more consecutive 1's}\\}. \\]\nThe minimum number of states in a Deterministic Finite-State Automaton (DFA) for $L$ is \\_\\_\\_\\_\\_\\_\\_\\_\\. (Answer in integer)",
        "options_latex": None
    },
    "2023_CS_CS_Q64": {
        "topic": "Computer Organization and Architecture",
        "subtopic": "Memory hierarchy: cache, main memory and secondary storage",
        "difficulty_level": "Easy",
        "explaination": "Address size $= 32\\text{ bits}$. Cache size $= 64\\text{ KB} = 2^{16}\\text{ bytes}$. For an 8-way set-associative cache, the combined capacity of index and offset is $\\frac{\\text{Cache Size}}{\\text{Associativity}} = \\frac{64\\text{ KB}}{8} = 8\\text{ KB} = 2^{13}\\text{ bytes}$, requiring $13\\text{ bits}$ for INDEX + BLOCK OFFSET. Therefore, the number of TAG bits is $32 - 13 = 19\\text{ bits}$.",
        "question_text_latex": "An 8-way set associative cache of size 64 KB (1 KB = 1024 bytes) is used in a system with 32-bit address. The address is sub-divided into TAG, INDEX, and BLOCK OFFSET.\nThe number of bits in the TAG is \\_\\_\\_\\_\\_\\_\\_\\_\\. (Answer in integer)",
        "options_latex": None
    },
    "2023_CS_CS_Q65": {
        "topic": "Computer Networks",
        "subtopic": "Routing protocols: shortest path, flooding, distance vector and link state routing",
        "difficulty_level": "Medium",
        "explaination": "For destination 200.150.68.118: subnet /16 (prefix length 16) matches. Subnet 200.150.64.0/19 (mask 255.255.224.0) matches since $68 \\& 224 = 64$. Subnet 200.150.68.0/24 (mask 255.255.255.0) matches since $68 = 68$. Subnet 200.150.68.64/27 (mask 255.255.255.224) does not match since $118 \\& 224 = 96 \\neq 64$. By the Longest Prefix Match rule, the /24 route (interface 3) is selected.",
        "question_text_latex": "The forwarding table of a router is shown below:\n\\begin{center}\n\\begin{tabular}{|l|l|c|}\n\\hline\n\\textbf{Subnet Number} & \\textbf{Subnet Mask} & \\textbf{Interface ID} \\\\\n\\hline\n200.150.0.0 & 255.255.0.0 & 1 \\\\\n200.150.64.0 & 255.255.224.0 & 2 \\\\\n200.150.68.0 & 255.255.255.0 & 3 \\\\\n200.150.68.64 & 255.255.255.224 & 4 \\\\\nDefault & & 0 \\\\\n\\hline\n\\end{tabular}\n\\end{center}\nA packet addressed to a destination address 200.150.68.118 arrives at the router. It will be forwarded to the interface with ID \\_\\_\\_\\_\\_\\_\\_\\_\\. (Answer in integer)",
        "options_latex": None
    }
}

def main():
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    paper_dir = os.path.join(root_dir, "dataset", "papers", "2023_CS")

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

    print(f"Enriched {updated_count} questions in 2023_CS paper files successfully.")

if __name__ == "__main__":
    main()

