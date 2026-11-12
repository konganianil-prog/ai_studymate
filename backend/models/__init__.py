from backend.extensions import db
from backend.models.user import User
from backend.models.subject import Subject, Unit
from backend.models.document import Document, ExtractedQuestion
from backend.models.answer import GeneratedAnswer, GeneratedVisual
from backend.models.quiz import Quiz, QuizQuestion, QuizAttempt, Flashcard
from backend.models.note import StudyNote

DEFAULT_SUBJECTS = [
    {
        "name": "Artificial Intelligence",
        "code": "CS-AI-401",
        "icon": "bi-cpu",
        "description": "Foundations of AI, search algorithms, knowledge representation, problem solving and modern AI applications.",
        "units": [
            {"unit_number": 1, "title": "Introduction to AI & Problem Solving", "description": "State spaces, heuristic search, A* algorithm, hill climbing"},
            {"unit_number": 2, "title": "Knowledge Representation & Reasoning", "description": "Propositional logic, predicate calculus, inference rules, semantic nets"},
            {"unit_number": 3, "title": "Probabilistic Reasoning & Planning", "description": "Bayesian networks, Markov decision processes, STRIPS planning"},
            {"unit_number": 4, "title": "Learning & Expert Systems", "description": "Supervised learning overview, decision trees, rule-based systems"}
        ]
    },
    {
        "name": "Machine Learning",
        "code": "CS-ML-501",
        "icon": "bi-graph-up-arrow",
        "description": "Statistical learning, regression, classification, clustering, ensemble learning and model evaluation.",
        "units": [
            {"unit_number": 1, "title": "Supervised Learning Fundamentals", "description": "Linear regression, logistic regression, cost functions, gradient descent"},
            {"unit_number": 2, "title": "Classification Algorithms", "description": "Decision trees, Random Forest, Support Vector Machines, k-Nearest Neighbors"},
            {"unit_number": 3, "title": "Unsupervised Learning & Clustering", "description": "k-Means, Hierarchical clustering, PCA, Dimensionality reduction"},
            {"unit_number": 4, "title": "Model Evaluation & Neural Networks intro", "description": "Cross-validation, precision, recall, ROC-AUC, perceptron"}
        ]
    },
    {
        "name": "Deep Learning",
        "code": "CS-DL-601",
        "icon": "bi-diagram-3",
        "description": "Deep artificial neural networks, CNNs, RNNs, Transformers and deep generative models.",
        "units": [
            {"unit_number": 1, "title": "Deep Neural Network Architecture", "description": "Backpropagation, activation functions, regularization, optimizers"},
            {"unit_number": 2, "title": "Convolutional Neural Networks (CNN)", "description": "Convolutions, pooling, ResNet, VGG, image classification"},
            {"unit_number": 3, "title": "Sequence Models & RNNs", "description": "Recurrent neural nets, LSTM, GRU, sequence-to-sequence"},
            {"unit_number": 4, "title": "Attention & Transformers", "description": "Self-attention mechanism, transformer encoder-decoder, LLM foundations"}
        ]
    },
    {
        "name": "Python Programming",
        "code": "CS-PY-201",
        "icon": "bi-code-slash",
        "description": "Core Python language, OOP, data structures, file handling and standard libraries.",
        "units": [
            {"unit_number": 1, "title": "Python Basics & Control Flow", "description": "Variables, data types, loops, conditionals, functions"},
            {"unit_number": 2, "title": "Data Structures & Collections", "description": "Lists, tuples, dictionaries, sets, comprehensions"},
            {"unit_number": 3, "title": "Object-Oriented Programming (OOP)", "description": "Classes, inheritance, polymorphism, encapsulation, dunder methods"},
            {"unit_number": 4, "title": "File I/O, Exceptions & Modules", "description": "File handling, custom exceptions, package management"}
        ]
    },
    {
        "name": "Database Management Systems (DBMS)",
        "code": "CS-DB-301",
        "icon": "bi-database",
        "description": "Relational data modeling, SQL, normalization, transactions, concurrency control and indexing.",
        "units": [
            {"unit_number": 1, "title": "ER Modeling & Relational Algebra", "description": "Entity-Relationship model, relational integrity constraints, algebra"},
            {"unit_number": 2, "title": "SQL & Query Optimization", "description": "DDL, DML, joins, subqueries, group by, indexing strategies"},
            {"unit_number": 3, "title": "Normalization & Schema Refinement", "description": "1NF, 2NF, 3NF, BCNF, functional dependencies, loss-less decomposition"},
            {"unit_number": 4, "title": "Transactions & Concurrency Control", "description": "ACID properties, serializability, two-phase locking, recovery systems"}
        ]
    },
    {
        "name": "Blockchain Technology",
        "code": "CS-BC-602",
        "icon": "bi-link-45deg",
        "description": "Decentralized ledgers, cryptographic primitives, consensus mechanisms, smart contracts and Ethereum.",
        "units": [
            {"unit_number": 1, "title": "Cryptography & Distributed Ledgers", "description": "Hash functions, public-key cryptography, Merkle trees, P2P networks"},
            {"unit_number": 2, "title": "Consensus Mechanisms", "description": "Proof of Work (PoW), Proof of Stake (PoS), Byzantine Fault Tolerance"},
            {"unit_number": 3, "title": "Smart Contracts & Ethereum", "description": "Solidity overview, EVM, gas mechanics, decentralized applications (DApps)"},
            {"unit_number": 4, "title": "Blockchain Use Cases & Scalability", "description": "DeFi, supply chain, Layer 2 rollups, sharding, security vulnerabilities"}
        ]
    },
    {
        "name": "Operating Systems",
        "code": "CS-OS-302",
        "icon": "bi-terminal",
        "description": "Process management, CPU scheduling, memory virtualization, synchronization, deadlock and file systems.",
        "units": [
            {"unit_number": 1, "title": "Processes & Threads", "description": "Process states, PCB, context switching, inter-process communication, multithreading"},
            {"unit_number": 2, "title": "CPU Scheduling & Synchronization", "description": "FCFS, SJF, Round Robin, semaphores, mutex, critical section problem"},
            {"unit_number": 3, "title": "Deadlocks & Memory Management", "description": "Deadlock conditions, Banker's algorithm, paging, segmentation, virtual memory"},
            {"unit_number": 4, "title": "Storage & File Systems", "description": "Disk scheduling, file allocation methods, directory structures, protection"}
        ]
    },
    {
        "name": "Computer Networks",
        "code": "CS-CN-402",
        "icon": "bi-hdd-network",
        "description": "OSI & TCP/IP models, routing protocols, transport layer flow/congestion control, socket programming.",
        "units": [
            {"unit_number": 1, "title": "Network Architecture & Physical Layer", "description": "OSI 7-layer stack, TCP/IP reference model, network topologies, transmission media"},
            {"unit_number": 2, "title": "Data Link Layer & MAC", "description": "Framing, error detection (CRC), sliding window protocols, Ethernet, CSMA/CD"},
            {"unit_number": 3, "title": "Network Layer & Routing", "description": "IPv4/IPv6 addressing, subnetting, Dijkstra shortest path, distance vector, BGP"},
            {"unit_number": 4, "title": "Transport & Application Layers", "description": "TCP three-way handshake, UDP, congestion control, HTTP, DNS, socket concepts"}
        ]
    }
]

def seed_default_subjects():
    """Populates default academic subjects and their units if empty."""
    if Subject.query.count() == 0:
        for subj_data in DEFAULT_SUBJECTS:
            subject = Subject(
                name=subj_data["name"],
                code=subj_data["code"],
                icon=subj_data["icon"],
                description=subj_data["description"],
                user_id=None
            )
            db.session.add(subject)
            db.session.flush()  # get subject.id
            
            for u in subj_data["units"]:
                unit = Unit(
                    subject_id=subject.id,
                    unit_number=u["unit_number"],
                    title=u["title"],
                    description=u["description"]
                )
                db.session.add(unit)
        db.session.commit()
