from modreg import db, create_app

app = create_app()

with app.app_context():
    db.engine.execute("""
    INSERT INTO webusers VALUES ('A001','password',True);
    INSERT INTO webusers VALUES ('A002','password',False);
    INSERT INTO webusers VALUES ('A003','password',False);
    INSERT INTO webusers VALUES ('A004','password',False);
    INSERT INTO webusers VALUES ('A005','password',False);

    INSERT INTO webadmins VALUES ('A001', 'Mr Toh', '09/05/2000');
    INSERT INTO students VALUES ('A002', 'Adi', '09/05/2000');
    INSERT INTO students VALUES ('A003', 'Bdi', '09/05/2000');
    INSERT INTO students VALUES ('A004', 'Cdee', '09/05/2000');
    INSERT INTO students VALUES ('A005', 'Edd', '09/05/2000');

    INSERT INTO faculties VALUES ('School Of Computing');
    INSERT INTO faculties VALUES ('Faculty Of Science');
    INSERT INTO faculties VALUES ('Faculty Of Engineering');

    INSERT INTO majors VALUES ('Computer Science','School Of Computing');
    INSERT INTO majors VALUES ('Computer Engineering','School Of Computing');
    INSERT INTO majors VALUES ('Software Engineering','School Of Computing');

    INSERT INTO majoring VALUES ('A002','Computer Science');
    INSERT INTO majoring VALUES ('A003','Computer Engineering');
    INSERT INTO majoring VALUES ('A004','Software Engineering');
    INSERT INTO majoring VALUES ('A005','Computer Science');

    INSERT INTO modules VALUES ('CS1010','Programming Methodology I', 'This module introduces the fundamental concepts of problem solving by computing and programming using an imperative programming language. It is the first and foremost introductory course to computing. Topics covered include computational thinking and computational problem solving, designing and specifying an algorithm, basic problem formulation and problem solving approaches, program development, coding, testing and debugging, fundamental programming constructs (variables, types, expressions, assignments, functions, control structures, etc.), fundamental data structures (arrays, strings, composite data types), basic sorting, and recursion.', 'School Of Computing', 4);
    INSERT INTO modules VALUES ('CS2030', 'Programming Methodology II', 'This module is a follow up to CS1010. It explores two modern programming paradigms, object-oriented programming and functional programming. Through a series of integrated assignments, students will learn to develop medium-scale software programs in the order of thousands of lines of code and tens of classes using objectoriented design principles and advanced programming constructs available in the two paradigms. Topics include objects and classes, composition, association, inheritance, interface, polymorphism, abstract classes, dynamic binding, lambda expression, effect-free programming, first class functions, closures, continuations, monad, etc.', 'School Of Computing', 4);
    INSERT INTO modules VALUES ('CS2040', 'Data Structures and Algorithms', 'This module introduces students to the design and implementation of fundamental data structures and algorithms. The module covers basic data structures (linked lists, stacks, queues, hash tables, binary heaps, trees, and graphs), searching and sorting algorithms, and basic analysis of algorithms.', 'School Of Computing', 4);
    INSERT INTO modules VALUES ('CS2103', 'Software Engineering', 'This module introduces the necessary conceptual and analytical tools for systematic and rigorous development of software systems. It covers four main areas of software development, namely object-oriented system analysis, object-oriented system modelling and design, implementation, and testing, with emphasis on system modelling and design and implementation of software modules that work cooperatively to fulfill the requirements of the system. Tools and techniques for software development, such as Unified Modelling Language (UML), program specification, and testing methods, will be taught. Major software engineering issues such as modularisation criteria, program correctness, and software quality will also be covered.', 'School Of Computing', 4);
    INSERT INTO modules VALUES ('CS2100', 'Computer Organisation', 'The objective of this module is to familiarise students with the fundamentals of computing devices. Through this module students will understand the basics of data representation, and how the various parts of a computer work, separately and with each other. This allows students to understand the issues in computing devices, and how these issues affect the implementation of solutions. Topics covered include data representation systems, combinational and sequential circuit design techniques, assembly language, processor execution cycles, pipelining, memory hierarchy and input/output systems.', 'School Of Computing', 4);
    INSERT INTO modules VALUES ('MA1101R', 'Linear Algebra I', 'This module is a first course in linear algebra. Fundamental concepts of linear algebra will be introduced and investigated in the context of the Euclidean spaces R^n. Proofs of results will be presented in the concrete setting. Students are expected to acquire computational facilities and geometric intuition with regard to vectors and matrices. Some applications will be presented. Major topics: Systems of linear equations, matrices, determinants, Euclidean spaces, linear combinations and linear span, subspaces, linear independence, bases and dimension, rank of a matrix, inner products, eigenvalues and eigenvectors, diagonalization, linear transformations between Euclidean spaces, applications.', 'Faculty Of Science', 4);    
    INSERT INTO modules VALUES ('CS1231', 'Discrete Structure', 'This module introduces mathematical tools required in the study of computer science. Topics include: (1) Logic and proof techniques: propositions, conditionals, quantifications. (2) Relations and Functions: Equivalence relations and partitions. Partially ordered sets. Well-Ordering Principle. Function equality. Boolean/identity/inverse functions. Bijection. (3) Mathematical formulation of data models (linear model, trees, graphs). (4) Counting and Combinatoric: Pigeonhole Principle. Inclusion-Exclusion Principle. Number of relations on a set, number of injections from one finite set to another, Diagonalisation proof: An infinite countable set has an uncountable power set; Algorithmic proof: An infinite set has a countably infinite subset. Subsets of countable sets are countable.', 'School Of Computing',4);
    INSERT INTO modules VALUES ('CS3243', 'Introduction to Artificial Intelligence', 'The module introduces the basic concepts in search and knowledge representation as well as to a number of sub-areas of artificial intelligence. It focuses on covering the essential concepts in AI. The module covers Turing test, blind search, iterative deepening, production systems, heuristic search, A* algorithm, minimax and alpha-beta procedures, predicate and first-order logic, resolution refutation, non-monotonic reasoning, assumption-based truth maintenance systems, inheritance hierarchies, the frame problem, certainly factors, Bayes rule, frames and semantic nets, planning, learning, natural language, vision, and expert systems and LISP.', 'School Of Computing', 4);
    INSERT INTO modules VALUES ('CG2028', 'Computer Organisation', 'This module teaches students computer organization concepts and how to write efficient microprocessor programs using assembly language. The course covers computer microarchitecture and memory system fundamentals, and the ARM microprocessor instruction set. The course culminates in an assignment in which students design and implement an efficient assembly language solution to an engineering problem.', 'Faculty Of Engineering', 4);
    INSERT INTO modules VALUES ('CS3210', 'Parallel Computing', 'The aim of this module is to provide an introduction to the field of parallel computing with hands-on parallel programming experience on real parallel machines. The module is divided into four parts: parallel computation models and parallelism, parallel architectures, parallel algorithm design and programming, and new parallel computing models. Topics includes: theory of parallelism and models; shared-memory architectures; distributed-memory architectures; data parallel architectures; interconnection networks, topologies and basic of communication operations; principles of parallel algorithm design; performance and scalability of parallel programs, overview of new parallel computing models such as grid, cloud, GPGPU.', 'School Of Computing', 4);
    INSERT INTO modules VALUES ('CS3223', 'Database Systems Implementation', 'This module provides an in-depth study of the concepts and implementation issues related to database management systems. It first covers the physical implementation of relational data model, which includes storage management, access methods, query processing, and optimisation. Then it covers issues and techniques dealing with multi-user application environments, namely, transactions, concurrency control and recovery. The third part covers object-database systems that are useful extension of relational databases to deal with complex data types. The last part covers database technologies required for modern decision support systems, including data warehousing, data mining and knowledge discovery and on-line analytical processing.', 'School Of Computing', 4);
    INSERT INTO modules VALUES ('CS2102', 'Database Systems', 'The aim of this module is to introduce the fundamental concepts and techniques necessary for the understanding and practice of design and implementation of database applications and of the management of data with relational database management systems. The module covers practical and theoretical aspects of design with entity-relationship model, theory of functional dependencies and normalisation by decomposition in second, third and Boyce-Codd normal forms. The module covers practical and theoretical aspects of programming with SQL data definition and manipulation sublanguages, relational tuple calculus, relational domain calculus and relational algebra.', 'School Of Computing', 4);
    INSERT INTO modules VALUES ('MA2214', 'Combinatorics and Graphs I', 'The main objective of this module is to introduce to students fundamental principles and techniques in combinatorics as well as the basics of graph theory, which have practical applications in such areas as computer science and operations research. The major topics from combinatorics are: Permutations and Combinations, Binomial and Multinomial Coefficients, The Principle of Inclusion and Exclusion, Generating Functions, Recurrence Relations, Special Numbers including Fibonacci Numbers, Stirling Numbers, Catalan Numbers, Harmonic Numbers and Bernoulli Numbers. The major topics from graph theory are: Basic Concepts and Results, Bipartite graphs and trees.', 'Faculty Of Science', 4);
    INSERT INTO modules VALUES ('MA1100', 'Basic Discrete Mathematics', 'This is the entry-level module for a sound education in modern mathematics, to prepare students for higher level mathematics courses. The first goal is to build the necessary mathematical foundation by introducing the basic language, concepts, and methods of contemporary mathematics, with focus on discrete and algebraic notions. The second goal is to develop student’s ability to construct rigorous arguments and formal proofs based on logical reasoning. Main topics: logic, sets, maps, equivalence relations, natural numbers, integers, rational numbers, congruences, counting and cardinality. Major results include: binomial theorem, fundamental theorem of arithmetic, infinitude of primes, Chinese remainder theorem, Fermat-Euler theorem.', 'Faculty Of Science', 4);

    INSERT INTO lectures VALUES  ('1','CS1010','11/11/2019 10:00:00',50);
    INSERT INTO slots VALUES ('1','CS1010','Monday','10:00:00','12:00:00');
    INSERT INTO slots VALUES ('1','CS1010','Friday','10:00:00','12:00:00');
    INSERT INTO lectures VALUES  ('2','CS1010','11/11/2019 10:00:00',50);
    INSERT INTO slots VALUES ('2','CS1010','Tuesday','08:00:00','10:00:00');
    INSERT INTO slots VALUES ('2','CS1010','Thursday','14:00:00','16:00:00');

    INSERT INTO lectures VALUES  ('1','CS1231','11/11/2019 10:00:00',50);
    INSERT INTO slots VALUES ('1','CS1231','Monday','08:00:00','10:00:00');
    INSERT INTO slots VALUES ('1','CS1231','Thursday','14:00:00','16:00:00');
    INSERT INTO lectures VALUES  ('2','CS1231','11/20/2019 10:00:00',50);
    INSERT INTO slots VALUES ('2','CS1231','Wednesday','08:00:00','10:00:00');
    INSERT INTO slots VALUES ('2','CS1231','Friday','14:00:00','16:00:00');

    INSERT INTO completions VALUES ('A002','CS1010');
    INSERT INTO completions VALUES ('A003','CS1010');
    INSERT INTO completions VALUES ('A003','CS1231');
    INSERT INTO completions VALUES ('A003','CS2030');

    INSERT INTO prerequisites VALUES ('CS2030','CS1010');
    INSERT INTO prerequisites VALUES ('CS2040','CS1010');
    INSERT INTO prerequisites VALUES ('CS2040','CS1231');
    INSERT INTO prerequisites VALUES ('CS2103','CS2030');
    INSERT INTO prerequisites VALUES ('MA2214','CS1231');
    INSERT INTO prerequisites VALUES ('CS3210','CS2100');
    INSERT INTO prerequisites VALUES ('CS3223','CS2102');
    INSERT INTO prerequisites VALUES ('CS3243','CS1231');
    INSERT INTO prerequisites VALUES ('CS3243','CS2040');
    

    INSERT INTO preclusions VALUES ('CG2028','CS2100');
    INSERT INTO preclusions VALUES ('MA1100','CS1231');
    """)
