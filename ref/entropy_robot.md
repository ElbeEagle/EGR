

# The Entropy Based Approach to Modeling and Evaluating Autonomy and Intelligence of Robotic Systems

# Abstract

This review paper presents the Entropy approach to modeling and performance evaluation of Intelligent Machines (IMs), which are modeled as hierarchical, multi-level structures. It provides a chronological summary of developments related to intelligent control, from its origins to current advances. It discusses fundamentals of the concept of Entropy as a measure of uncertainty and as a control function, which may be used to control, evaluate and improve through adaptation and learning performance of engineering systems. It describes a multi-level, hierarchical, architecture that is used to model such systems, and it defines autonomy and machine intelligence for engineering systems, with the aim to set foundations necessary to tackle related challenges. The modeling philosophy for the systems under consideration follows the mathematically proven principle of Increasing Precision with Decreasing Intelligence (IPDI). Entropy is also used in the context of $N$-Dimensional Information Theory to model the flow of information throughout such systems and contributes to quantitatively evaluate uncertainty, thus, autonomy and intelligence. It is explained how Entropy qualifies as a unique, single, measure to evaluate autonomy, intelligence and precision of task execution. The main contribution of this review paper is that it brings under one forum research findings from the 1970's and 1980's, and that it supports the argument that even today, given the unprecedented existing computational power, advances in Artificial Intelligence, Deep Learning and Control Theory, the same foundational framework may be followed to study large-scale, distributed Cyber Physical Systems (CPSs), including distributed intelligence and multi-agent systems, with direct applications to the SmartGrid, transportation systems and multi-robot teams, to mention but a few applications.

Keywords Intelligent machines · Entropy · Autonomy · Hierarchical systems

# 1 Introduction

Since the 1960's progress and advances in robotics and automation, despite several challenges and drawbacks, has produced unparalleled results; technology has today, matured to the point of serious discussions to design fully autonomous systems [69]. Chronologically, in parallel to robot design, there have been efforts to develop a theory of intelligent machines building on the foundations of classical control (1950's), adaptive and learning control (1960's), self-organizing control (1970's), and, subsequently, intelligent

control (1980's). The foundational framework for designing intelligent machines (IMs) is based on integration of concepts and ideas from Science, Engineering and Mathematics, under one common cover connecting several diverse methodologies that are used to define machine intelligence [29, 42, 67, 68, 70–75, 88, 94, 96–98, 114]. An intelligent robotic system (IRS), is a specific application of an IM. It is defined as a complex, spatio-temporal, computer-controlled system (multi-manipulators, homogeneous or heterogeneous multi-robot teams, unmanned vehicle teams, etc.) equipped with diverse sensors, with (perhaps limited) situation awareness, decision-making and problem/mission solving capabilities under dynamic (environment and/or system) uncertainties, also possessing adaptation and learning attributes. Modeling, control and performance evaluation of IRSs may be accomplished via an ensemble of analytical and heuristic methodologies and techniques pertaining to generalized system theory, soft computing, artificial intelligence (AI), learning, operations research, game theory, complexity theory, cased based reasoning, and a plethora of other approaches [1, 43].

When designing IMs, IRSs, and other unmanned robotic systems in general, autonomy (or autonomous functionality) is the objective, and intelligent controllers are one way to achieve it [8, 9, 91]. However, 'intelligent control', which tends to encompass everything that is not characterized as 'conventional control', has shifting boundaries, since the precise definition of 'intelligence' has been eluding mankind for thousands of years.¹ The issue or concept of 'intelligence' has been widely addressed by disciplines such as psychology, philosophy, biology and AI. No consensus has emerged of what constitutes 'intelligence'. The controversy surrounding the widely-used IQ tests, adds to the fact that scientists and engineers may be well away from having understood these issues, let alone implement them in real complex systems. Despite the challenge, in a hierarchical system, or, hierarchically intelligent system, intelligent control uses conventional control methods to solve 'lower level' control problems as explained in [4, 6, 8, 9, 17, 23, 43, 56, 91]. At a minimum, intelligent control is at the intersection of AI. Operations Research and Control Systems [23, 43, 56] with Computer Science providing the backbone for the accompanied software architecture, aiming to use and implement a blend of concepts, ideas, methodologies, tools and techniques used in each of the constituent areas with the objective to build (human-made) IMs, IRSs and unmanned robotic systems.

Autonomy has shifting boundaries, too. It has been argued that autonomy is a set of capabilities, and that autonomy is evaluated with respect to a set of desirable goals and capabilities. If this is accepted (and from the engineering point of view, it should), then, one may also argue that levels of autonomy may be used to characterize and evaluate the (corresponding level of) autonomous functionality of an IM or IRS, or, according to P. J. Antsaklis, the autonomicity of the system [1, 17, 80]. Under this consideration, full autonomicity implies full autonomy or complete autonomy or fully autonomous operation without intervention of and interaction with a human operator. The 'shifting boundaries of autonomy' may be easier understood when the set of desired goals changes, or when the system is faced with unforeseen situations in its workspace environment, which may subsequently affect autonomous system functionality – this limitation may be overcome over time via enhanced situation awareness, resilient resign, advanced adaptation and learning.

From the modeling and control point of view, IMs/IRSs behave as multi-level hybrid, but also time-based and event-based systems [36-41, 80]. Time-based attributes relate to the (lowest level) actual and precise execution of specific tasks using well-established and widely used control algorithms. Event-based attributes relate to higher level reasoning, planning, decision-making and coordination functionalities, which occur on- or off- line. IMs/IRSs also operate in different time-scales that span the range from strict real-time task execution (hard timing constraints) to quasi-real-time scheduling, task allocation and coordination, and off-line mission planning and re-planning. In further detail, top-down consideration of such systems entails general mission decomposition from complex activities (formed as strings of ordered primitive events that define the capabilities of the IM/IRS) to primitive events or primitive tasks that are executed in real-time, while bottom-up consideration includes primitive event synthesis and concatenation to form complex (ordered) activities that constitute a complete mission. Inherent in this framework is how a task / multiple tasks are executed, how activities are ranked to best execute an assigned mission, but also how the ranking changes based on adaptation and learning [23, 35, 43, 44].

The central goal when developing intelligent systems and machines, is to demonstrate and evaluate progression of automation attributes, eventually resulting in high-confidence and trusted systems, which a human operator can trust and work with, in unison. Stated differently, delegation of authority and decision-making will shift gradually, over time, from the human operator to the machine. It is this delegation of authority that requires adaptation and learning to make the system trustworthy for autonomous functionality. Autonomy and autonomous functionality allows for transition from the 'human-in-the-loop' to the 'human-on-the-loop' concept, which, when achieved, will close the loop of a 40+ years argument to build intelligent machines that function with minimum human supervision.

Entropy is a convenient global measure of performance [43] because of its wide applicability to a variety of systems of diverse disciplines. It is the duality of the concept of Entropy as a measure of uncertainty and as energy function that makes it a viable candidate to evaluate autonomy/intelligence of complex engineering systems [54, 55, 90, 91]. For a multi-level, hierarchical system, Entropy may be used as an overall system, inter-level and intra-level (vertical and horizontal) measure of uncertainty and precision of task allocation and execution. Under this consideration, intelligent control is cast as the mathematical problem offinding the right sequence of reasoning, planning and decision-making actions and controls for a hierarchical multi-level system such that it minimizes its total Entropy [23, 50, 55]. The design constraint is the principle of increasing precision with decreasing intelligence (IPDI), first introduced and proven by Saridis [90, 91].

The rest of the paper is organized as follows: Section $2$ provides related literature review, which sets the tone for subsequent sections. Section $3$ is devoted to fundamentals of Entropy, as well as Entropy definitions and methods pertaining to intelligent control, while Section $4$ discusses the multi-level architecture, details its functionality and connects it with the Entropy formulation. The last Section concludes the paper.

# 2 Literature Review

Research in intelligent control, intelligent robotic systems, intelligent machines, and hierarchically intelligent control systems finds its origins in the pioneering work on 'learning control' of Fu [30, 31], Sklansky [32], Tsykin [33, 34], Mesarovic's theory of hierarchical multilevel systems [61], R. C. Conant's laws of information that govern systems [59], and Findeisen's et al. work on control and coordination in hierarchical systems [60], while, in parallel, Sheridan and his group were working on man-machine systems see [79] and references therein. Historically, the term 'hierarchical control' was introduced by K. S. Fu in the very early 1970's, while the first attempts to study it are found in Saridis and Stephanou and Saridis and Graham [23, 77, 78, 102]. The 1980's and 1990's witnessed major and coordinated efforts by specific groups (led by J. Albus, P. J. Antsaklis, A. Meystel, U. Ozguner, G. N. Saridis) to define intelligent control and hierarchical architectures as applied to engineering systems, robotic systems, robotic assemblies and intelligent machines [1-22, 26-28, 35-37], [23, 43-56], [24, 57], [25, 63, 64], [65, 66]. J. Albus proposed a theory of intelligence for biological and artificial systems [24]; Passino and Antsaklis studied autonomous control systems designed to perform well under uncertainties in the system and environment for long periods of time and compensated for system failures without external intervention. Path panning was put under an AI context, while conditions for strong and weal controllability, observability and stability were defined [2, 5, 7, 17, 18, 35, 36]. Acar and Ozguner adopted an axiomatic approach to derive a unified hierarchical control strategy utilizing mathematical and functional system representations [64, 65]; reliability analysis and the issue of structural formulation for plan generation were investigated in [113], while other approaches may be found in [51-53, 62, 63]. At the same time, expert control, and command and control [57, 58] were introduced as additional challenges to control science, followed by efforts in hybrid systems and their applications [20-22, 38-41]. There were also attempts to tackle similarities and differences between

expert systems and intelligent machines [45, 46, 49, 53, 54]. In summary, the NASREM architecture [56], the levels of autonomicity in hierarchical systems, the principle of increasing precision with decreasing intelligence, the idea of nested hierarchical structures, and the design of knowledge-rich hierarchical controllers for large-scale systems were some of the concepts that found their way in the literature until the early 2000's. The objective of minimum interaction and supervision by a human operator, although discussed, was not actually implemented and demonstrated in real systems; one explanation may be the lack of computer and computational power that limited implementation to only simulation studies for simple systems, while a second explanation may be the lack of agreement on what constituted intelligent control.

However, efforts to define the meaning of intelligent control continued, and the IEEE Control Systems Society established a Task Force to investigate intelligent control. In its report, the Task Force pointed out quite clearly that autonomy is the goal and intelligent methods are necessary for high degrees of autonomy. Antsaklis has played a leading and pioneering role in this major task; several reports and publications resulted from this effort, for example, see [4, 8, 9, 14, 16, 80] and references therein, which provided rationale on what may be considered as intelligent control.

Focusing on Entropy, the Entropy consideration to modeling and evaluation of modern engineering systems finds its origin in Conant [59] who was the first to use it as an information theoretic measure to study and establish laws that govern the behavior of deterministic systems, deriving the total rate of information flow in terms of throughput, blockage, coordination and noise rates. This law was generalized by Valavanis and Saridis [54] who used $N$-dimensional information theory to derive a generalized law of information rates to study stochastic systems taking into consideration interdependences of their internal components.

Despite other considerations of team theoretic decision problems, it was A. Levis and his group (Boettcher, Hall, Stabile) [98, 103, 114 and references therein] who really pioneered the decision-making process by synthesizing qualitative notions of decision-making with the analytic framework of information theory. Motivated by theories of organization developed by Galbraith and Drenick [100, 101], the first model that was introduced was a simple two-stage model of situation assessment (SA) and response selection (RS), which was used to characterize the process of executing a well-defined decision-making task. This model was memoryless; subsequently, functions of storage and memory as occurred in a rate decision-making system were modeled in an information theoretic framework. The initial two-stage model was enhanced to a four-stage model with information fusion (IF) and command interpretation (CI) components between SA and RS, with an additional enhancement that included a fifth sensor component. Research conducted by the Saridis' group until the middle 2000's, and specifically by Valavanis, has been influenced by the research findings of the Levis' group.

Moreover, Broekstra [99] examined the applicability of information theory to the problem of structure identification, while Koomen [110] argued that information is linked with the structural complexity of the system. Jaynes [104, 105] showed that information theory provides a criterion to set up worst case probability distributions based on partial knowledge, leading to a type of statistical inference called maximum Entropy estimate (that is maximally non-committal regarding missing information). Kalata and Priemer used information theoretic concepts in a series of four papers [106–109] to: obtain conditions for a minimax error Entropy stochastic approximation algorithm to estimate the state of a nonlinear discrete time system; analyze the smoothing problem for linear discrete time systems; derive a procedure for identifying a parameter of a stochastic linear discrete time scalar system; derive fundamental principles for the general estimation problem.

Despite these major efforts and continued research in robotics, automation, and control systems with unprecedented developments and accomplishments, and although it may be argued that systems, in general, may follow a (loose or strict) hierarchical multi-level structure [61, 62], there appears to be a drawback when attempting to study, model, develop, and formalize design of systems that operate in uncertain/dynamic environments and exhibit attributes of autonomous performance. This drawback may be re-phrased as: Lack of a widely acceptable, proven, detailed, unified and hierarchical (multi-level) methodology that addresses autonomous functionality of real robotic systems, from mission planning/replanning, to task assignment and coordination, to actual mission execution, to improving performance based on fault-tolerance, adaptation and learning, subsequently resulting in autonomous robotic systems. One may find several justifiable reasons for such a 'gap' or 'vacuum', one of which may be that it is preferred to focus on specific components (layers or levels) of a complex system, i.e., controller design, as opposed to developing and validating overall methodologies – which is hard, to say the least.

Despite challenges, a candidate methodology is offered with the hope to re-ignite discussions on multi-level systems, based on what we know and understand now, and to pave the way for an acceptable foundation towards measuring and evaluating autonomy and intelligence of engineering systems.

The next Section centers on the concept of Entropy and how it may be applied to facilitate studying engineering systems.

# 3 Fundamentals of Entropy

Entropy is introduced from different points of view, with the aim to pave the way and establish synergies and equivalences to show that the concept of Entropy may be used as one, unified measure of autonomy, intelligence and autonomous functionality, being a measure of uncertainty of information, as well as of precision of task execution from a control theory perspective. Discussion follows a logical progression in a step-by-step way that also shows how Saridis was inspired to use Entropy in intelligent control and to formulate control problems in terms of Entropy performance measures.$^{2}$ Comments are also offered, which could be considered to develop an enhanced foundation for multi-level hierarchical systems.

Historically, the concept of Entropy was introduced by Clausius in thermodynamics in 1867 to define the low-quality energy resulting from the second law of thermodynamics. But, it was Boltzmann who in 1872 used this concept to create the theory of statistical thermodynamics to express the uncertainty of the state of the molecules of a perfect gas [85, 89–91, 93]. Boltzmann defined the Entropy, $S$, of a perfect gas changing states isothermally at temperature $T$ in terms of the Gibbs energy $\psi$, the total energy of the system $H$ and Boltzmann's universal constant $k$, as

$$
S = - k \int _ { x } \{ ( \psi - H ) / k T \} \mathrm { e } ^{( \psi - H ) / k T} d x
$$

However, due to the size of the problem and related uncertainties when trying to describe the dynamic behavior of a perfect gas, a probabilistic model was derived, in which the Entropy was defined in terms of the molecular probabilistic distribution $p(x)$ that indicates the probability of a molecule being in state $x$, under the assumption that $p(x)$ satisfies the incompressibility property over time in the state-space $X$ in which $x$ is defined, i.e., $dp/dt=0$. When this is the case, the Entropy $S$ is defined as

$$
S = - k \int _ { X } p ( x ) l n p ( x ) d x
$$

where the integral is defined over the whole state-space $X$, and

$$
p ( x ) = \mathrm { e } ^{( \psi - H ) / k T}
$$



The key observation is to realize that in an isothermal process, heat may be considered as the result of the kinetic and potential energies of molecular motion! Thus, when applying the dynamical theory of thermodynamics on the aggregate of the molecules of a perfect gas, an average Lagrangian, $I$, may be defined to describe the performance over time of the state $x$ of the gas

$$
I = \int L ( x , t ) d t
$$

where the Lagrangian $L(x,t)dt$ is the difference between the kinetic and potential energy, and the integral is defined over the interval $[t_o,t_f]$. The average Lagrangian, when minimized, satisfies the second law of thermodynamics. Under this consideration, the expressions $S=-k\int_x\{(\psi-H)/kT\}\mathbf{e}^{(\psi-H)/kT}dx$, $I=\int L(x,t)dt$ are equivalent, which leads to

$$
S = I / T
$$

with $T$ the constant temperature of the isothermal process of a perfect gas.

It is this equivalence of formulations that inspired Saridis to express the performance measure of a control problem in terms of Entropy [90, 91], building a whole theory on "...establishing Entropy measures equivalent to the performance criteria of the optimal control problem, while providing a physical meaning to the latter." In further detail, for example, consider the optimal feedback deterministic control problem with accessible states for the $n$-dimensional dynamic system with state vector $x(t)$, $dx/dt = f(x, u, t)$, with initial conditions $x(t_o) = x_o$, and cost function $V(u, x_o, t_o) = \int L(x, u, t)dt$, where the integral is defined over $[t_o, T]$, and with $u(x, t)$ the $m$-dimensional control law. An optimal control $u^*(x, t)$minimizes the cost $V(u^*; x_o, t_o) = min_u \int L(x, u, t)dt$ with the integral defined over $[t_o, T]$. Saridis proposed to define the differential Entropy for some $u(x, t)$ as

$$
\begin{array}{rl} & { H ( x _ { o } , u ( x , t ) , p ( u ) )  =  H ( u ) } \\& {   = - \int _ { \Omega u } \int _ { \Omega x } p ( x _ { o } , u ) l n p ( x _ { o } , u ) d x _ { o } d u } \end{array}
$$

where the integrals are defined over $\Omega_{u}$ and $\Omega_{x}$, and found necessary and sufficient conditions to minimize $V(u(x, t)$, $x_{o}, t_{o})$ by minimizing the differential Entropy $H(u, p(u))$ where $p(u)$ is the worst Entropy density as defined by Jayne's Maximum Entropy Principle [104, 105]. Therefore [113], "...by selecting the worst-case distribution satisfying Jaynes' Maximum Entropy Principle, the performance criterion of the control is associated with the Entropy of selecting a certain control law." Minimization of the differential Entropy results in the optimal control solution. The adaptive control and stochastic optimal control problems were derived as special cases of the optimal control formulation.

Note that Jaynes' Maximum Entropy Principle was formulated to be applied in theoretical mechanics. It states that "the uncertainty of an unspecified relation of the function of a system is expressed by an exponential density function of a known energy relation associated with the system." It is this statement that Saridis used in a modified version following the calculus of variations, to derive the Entropy formulation of control problems either for deterministic or stochastic systems and for optimal and non-optimal solutions.

In addition, it has been shown that Entropy has invariant features, for example, it is invariant to transformations between coordinate frames. This makes it an even stronger candidate to evaluate performance of engineering and robotic systems (multi-robot teams, UAVs, etc.) as it is often required to transform sensor readings between coordinate frames – to make a point, covariance does change when subjected to coordinate frame transformations. Application-wise, any sensor-based navigation control algorithm for a single robot manipulator, a robotic vehicle, a (homogeneous or heterogeneous) team of such vehicles, or a dynamic system in general, and/or a controller design may be derived and evaluated using Entropy measures as performance criteria; Lagrangian formulations and the generalized Hamilton-Jacobi-Bellman equation may be derived accordingly based on probability distributions and the incompressibility condition. Viewed from this perspective, Entropy minimization relates to 'how well' or 'how precise' the algorithm/controller performs, and, by analogy, to how precisely a task is executed, i.e., trajectory tracking, end-point control, move(A, B), collision avoidance, etc. Entropy as performance criterion in a control theoretic setting reveals (lower- or lowest- level time-based attributes of a multi-level system and is linked directly to precision of task execution.

Again, and this supports (the strong argument of) using Entropy as a unique measure, the Entropy connection is that a probability density function is assigned over the space of admissible controls and the problem is solved by finding the control law that has maximum probability of attaining the optimal value.

Entropy is also a measure of uncertainty as defined in information theory, which was first introduced by Shannon [86, 87, 95]. Information theory studies communication of messages from one point to another, answering how the constraint between two variables $X$ and $Y$ that represent a message sent and a message received, respectively, can be measured and maximized in a channel with limited total capacity $C$. The basic measure is the Entropy of a (continuous, discrete or discretized) random variable, say $X$, defined as (in the discrete case)

$$
H ( X ) = - \sum _ { x } p ( x ) l o g p ( x )
$$

where the summation is over all values $x$ taken by $X$, $p(x)$ is the probability density function of $X$, and the uncertainty is defined by $-logp(x)$. The logarithmic base may be $log$ or $ln$. Accordingly, the differential Entropy of a continuous random variable $X$ with density function $f(x)$ with respect to Lebesgue measure, may be defined according to Van Campenhout and Cover [43] over the interval $(-\infty, +\infty)$ as

$$
H ( X ) = \int f ( x ) l n f ( x ) d x
$$

Conditional Entropies are defined based on joint and/or conditional probability distributions for $X$, $Y$

$$
\begin{array}{rl} & { H _ { Y } ( X ) = - \sum _ { x , y } p ( x , y ) l o g p ( x / y ) } \\& { = - \sum _ { y } p ( y ) \sum _ { x } p ( x / y ) l o g p ( x / y ) } \end{array}
$$

Transmission of information indicates the amount by which two random variables $X$, $Y$ are related, or, the amount by which knowledge of one variable reduces the uncertainty about the other, and it is defined either through individual and joint Entropies or through conditional Entropies as

$$
\begin{array}{rl} & { T ( X : Y ) = H ( X ) + H ( Y ) - H ( X , Y ) = H ( X ) - H _ { Y } ( X ) } \\& {  = H ( Y ) - - H _ { X } ( Y ) } \end{array}  ( 10 )
$$

It was Shannon's Entropy formulation that motivated Conant to define the Entropy rate as the information carried per observation in a long sequence {X(t), X(t+1), ..., X(T+m-1)} as

$$
\begin{array}{r} { \dot { H } ( x ) = l i m _ { m \rightarrow \infty } ( 1 / m ) H ( X ( t ) , X ( t + 1 ) , \dots , } \\{ X ( T + m - 1 ) ) } \end{array}
$$

while Hall and Levis and Papoulis [103, 111] defined the Entropy rate for statistically independent inputs generated every $\tau$units/seconds as

$$
\dot { H } ( x ) = ( 1 / \tau ) H ( x )
$$

Conant's Partition Law of Information Rates (PLIR) states that for a system $G$ modeled as an ordered set of variables $G = (G_1, G_2, G_3, \ldots, G_{|G|})$ that are divided into internal variables $G_{int}$ and output variables $G_{out}$ that are observable from its environment, i.e., $G = (G_{int}, G_{out})$, which receives a vector input $E$ from the environment, and is partitioned into $N$ disjoint subsystems $G_i, i = l, 2, 3, \ldots |G|$, of variables $G_{ij}$, the total non-deterministic activity $F$, ignoring intervariable relationships, may be defined as the sum of the throughput, blockage, coordination and noise rates

$$
F = F _ { l } + F _ { b } + F _ { c } + F _ { n }
$$

$F = -\sum_{j} \dot{H}(G_{j})$ the total rate of information flow

$$
F _ { t } = \tilde { T } ( E : G _ { o u t } )  \mathrm { t h e ~ t r o u g h p u t ~ r a t e }
$$

$$
F _ { b } = \tilde { T } _ { G o u t } ( E : G _ { i n t } )  \mathrm { t h e ~ b l o c k a g e ~ r a t e }
$$

$$
F _ { c } = \tilde { T } ( G _ { 1 } : G _ { 2 } ; . . . : G _ { | G | } )  \mathrm { t h e ~ c o o r d i n a t i o n ~ r a t e }
$$

$$
F _ { n } = \dot { H } _ { E } ( G )
$$

$$
\mathrm { t h e ~ n o i s e ~ r a t e }
$$

The $PLIR$ 'exposes' the additive properties of Entropy and indicates that in a system of fixed total capacity ($F$) there are tradeoffs and competition for resources as indicated by relations (14)-(18). Careful observation 'beyond' Eqs. (13) to (18) suggests that if estimates for blockage, coordination and output are available and if capacities of system components are known, $PLIR$ provides a lower bound of the number of components needed to execute a task.

It is the additive properties of Entropy as measure of uncertainty under the information theory consideration, and the ability to consider component dependencies and interactions within a complex dynamic system, as well as to 'quantify' such uncertainties that motivated Valavanis to generalize Conant's PLIR to include the stochastic nature of engineering systems and to follow a probabilistic approach to mission planning and decision-making. This generalized law, GPLIR, may be derived for the whole hierarchy (multi-level system), but also for each level, separately [4, 54].

It is postulated that the system's intelligence, machine intelligence, is related to its corresponding level of uncertainty; minimum uncertainty refers to maximum intelligence, thus, maximum autonomous functionality or autonomicity as defined by Antsaklis. Moreover, the very same concept or measure, Entropy, offers the needed glue to connect machine intelligence to robust intelligence. Robust intelligence may be evaluated by measuring the distance or divergence or discrepancy from maximum/minimum uncertainty (worst/best plan to execute a mission) or any measured uncertainty (any admissible plan between the best and the worst one) within the Entropy Interval = $H_{max}$ - $-H_{min}$, using the Kullback-Leibler (K-L) measure of cross-Entropy (1951) and Kullback's (1959) minimum directed divergence or minimum cross-Entropy principle, MinxEnt [92].

Possible human intervention is accounted for in terms of (probabilistic) constraints that affect/alter the $H_{max} - -H_{min}$ interval. To be specific, in the case of probabilistic uncertainty, when there are $n$ possible outcomes with probability $p_i$, $i = 1$, $2$, $3$, ..., $n$, and $\sum p_i = 1$, then, $H_{max}$ corresponds to the uniform distribution ($p_i = 1/n$) that has the maximum uncertainty out of all probability distributions for $n$ outcomes – this is Laplace's principle of insufficient reason. Any other distribution results in $H < H_{max}$, and one distribution results in $H_{min}$, which is the achievable lower bound of uncertainty. The human intervention, which characterizes the level of human-machine interaction, is introduced mathematically via additional probabilistic constraints, for example $p_i$, $i = I$, 2, 3..., $n$, $\sum p_i = 1$, and $\sum c_i p_i = c$, $c_i'$s are weights and $c$ a bound, which are imposed on (unconstraint) probability distributions and influence/alter the $H_{max} - -H_{min}$ interval. That is, uncertainty maximization/minimization is now subject to all constraints that must be satisfied. In this case the choice of distributions is restricted as it must satisfy all constraints.

Whether following the 'human-in-the-loop' or the 'human-on-the-loop' approach, uncertainty (may be) is reduced due to human intervention, and this is reflected in the $H_{max} - H_{min}$ interval. The $H_{max} - H_{min}$ interval provides robustness bounds related to calculated uncertainty. In detail, the distance between two probability distributions $\boldsymbol{p} = (p_1, p_2, \ldots, p_n)$ and $\boldsymbol{q} = (q_1, q_2, \ldots, q_n)$ may be measured (and evaluated) via the K-L measure $D(\boldsymbol{p};\boldsymbol{q}) = \sum p_i \ln(p_i/q_i)$. For example, when $\boldsymbol{q}$ is the uniform distribution (indicating maximum uncertainty), then $D(\boldsymbol{p};\boldsymbol{q}) = \ln n - H(\boldsymbol{p})$ where $H(\boldsymbol{p})$ is Shannon's Entropy. Therefore, the 'distance' among any two formulated plans may be calculated regardless of whether the human imposes constraints or not, as well as the best plan with the minimum uncertainty, the next to the best plan, etc., all the way to the worst plan with the maximum uncertainty. Therefore, after missions are issued by the human operator as input commands, the IM or IRS, through reasoning, planning and decision-making, formulates candidate plans in terms of ordered sequences of events. Probability distributions are defined or estimated for each candidate plan, and Entropy provides measures of how good or how bad a candidate plan is. In cases where the system's desired performance is a-priori defined, the 'distance' from this performance, also expressed as a probability distribution, and, thus, Entropy, may be measured. Under this information theory related approach, which connects Entropy with the event-based attributes of multi-level systems, the system starts from a state of maximum uncertainty and through adaptation and learning, uncertainty is reduced as a function of accumulated and acquired knowledge and information over time.

To summarize, the duality of Entropy, as measure of uncertainty and as energy function has been presented. Entropy has additive properties that allow for partitioning the overall uncertainty of several variables into the uncertainty of the first plus the uncertainty of the second remaining after knowledge of the first, etc. Entropy may be used to measure uncertainty of a single variable or (primitive) event, a group of variables (i.e., a sequence of ordered events that formulate a plan to execute a mission), or evaluate several alternative plans (in a probabilistic way) that are suitable to complete a task/mission. It is these properties that support the argument that Entropy may be used to evaluate the overall (vertical) autonomy and intelligence of a multi-level system, as well as individual level autonomy (horizontal), and precision of individual task or plan execution.

The proposed multi-level hierarchical architecture that has been introduced by the Saridis' [43, 77, 78, 89] and Antsaklis' [1, 2, 17, 18] groups is shown in Figs. 1 and 2, respectively. The choice of (somehow, arbitrarily) using three levels is leveraged by the fact that a system architecture may be conceptually combined to follow a

# 4 A Hierarchical Architecture

<div style="display: block; width: 100%"><img src="https://storage.simpletex.cn/view/m12f04d32a029341a367d5e1768c0a490" style="width: 40%; max-width: 40%" /></div> Fig. 1 The Saridis et al. hierarchical architecture that is based on the principle of IPDI



<div style="display: block; width: 100%"><img src="https://storage.simpletex.cn/view/m758b855bacf831371904b0c770e66d93" style="width: 27%; max-width: 27%" /></div> Fig. 2 The Antsaklis et al hierarchical architecture that centers on autonomicity

three-level representation [60, 61].$^{3}$ This representation is applicable to most autonomous systems based on grouping together sublevels of the architecture, if necessary. The lowest level involves conventional control algorithms (real-time), while the highest level involves reasoning, planning, decision-making and adaptation/learning. The middle level uses a combination of conventional and intelligent decision-making methods, completing the hierarchy. Commands are issued top-down by higher levels to lower levels, while response data flows bottom-up from lower levels, upwards. Parameters of subsystems and components at a specific level can be altered by subsystems/components at the immediately higher level of the hierarchy. There is a delegation and distribution of tasks from higher to lower levels and a layered distribution of decision-making authority. At each level, preprocessing occurs before information is sent to adjacent levels. All subsystems provide status and health information to higher levels. Human intervention may be allowed with commands passing down from the upper levels of the hierarchy. Under the Entropy formulation, human intervention is modeled in terms of imposed constraints in probability distributions.

The key functions of the Management/Organization level are reasoning, planning and decision-making (top-down), feedback, adaptation/learning and update of the knowledge base (bottom-up). In unison with the coordination level, this requires decomposing the high-level mission into conflict-free specifications for the candidate system in response to uncertainties or changes, create alternative plans and evaluate performance. The coordination level formulates the control problem associated with the decomposed plan with task specifications (received from the higher level), and oversees execution in real-time. This may require selection of one among alternative plan scripts that accomplish the same job in different ways per the specifications/constraints imposed by the assigned mission and/or environment.

The coordination level has no reasoning capabilities; its intelligence is related to its ability on how to execute the assigned plan in the best possible way based on accrued experience. Interfaces among the different levels 'convert' commands to the format (i.e., strings of symbols, events) understood by the lower/upper level [43].

Figure 3 illustrates the three-level hierarchical architecture in terms of inputs, outputs, internal variables and feedback information. This configuration serves as the backbone to plan formulation and execution, adaptation and learning.

Although there exist several architectures in the literature, this configuration is a functional architecture; it is hardware and software agnostic, applicable to a wide range of systems from engineering to socio-economic

<div style="display: block; width: 100%"><img src="https://storage.simpletex.cn/view/m96cdbb1f93c8afd3f63211a11d67735b" style="width: 40%; max-width: 40%" /></div> Fig.3 General structure of the three-level functional architecture ones and financial organizations. The only requirement is to define functionality of each level and overall system objectives. The IPDI principle dictates that the Organization/Management level (event-based) is the most intelligent one, while the execution level (time-based) is the most precise. Entropy brings under one ensemble uncertainty and performance criteria, which, when optimized, provide a quantitative evaluation of the system's intelligence and autonomicity.

For any system that is represented by the hierarchical architecture of Figs. 11-3 the following may be defined [43]:

Machine Knowledge ($\mathbf{K}$) is the structured information acquired/applied to remove ignorance/uncertainty about a specific task pertaining to the intelligent machine.

The Rate of Machine Knowledge ($\mathbf{R}$) is the flow of knowledge through the intelligent machine.

Machine Intelligence ($\mathbf{MI}$), where machine is used as a general term, is defined as the process of analyzing, organizing and converting data into knowledge. It is the set of actions or rules that operates on a Data Base ($\mathbf{DB}$) of events or activities to produce flow of knowledge ($\mathbf{R}$). This definition relates to the mathematically proven principle of increasing precision with decreasing intelligence, IPDI [55].

An intelligent system, is characterized by its ability to dynamically assign sub-goals and control actions in an internal or autonomous fashion; this relates to the system's attempt to organize or order the 'knowledge' of its own dynamical behavior to meet a control objective. If knowledge organization is done autonomously by the system, then, intelligence becomes a property of the system, rather than of the system's designer. This implies that systems that autonomously (self)-organize controllers with respect to an internally realized organizational principle are intelligent control systems. Any intelligent system is a control system, as it has desirable behavior and goals to achieve, and intelligence is necessary to provide desirable functionality under changing conditions. An intelligent control system is designed so that it can autonomously achieve a high-level goal, while its components, control goals, plant models and control laws may not be completely defined, either because they were not known at the time of the system design, or because of unexpected changes. The term "intelligent control system" simply stresses the control aspect of the intelligent system. Consequently, there are degrees or levels of intelligence that can be measured along the various dimensions of intelligence.

Adaptation and Learning are both essential attributes of an IM/IRS. The ability to adapt to changing conditions is a necessary (but not sufficient) requirement of an intelligent system, because adaptation does not necessarily require the ability to learn. Learning is also a necessary (but not sufficient) requirement of an intelligent system and includes the ability to adapt to a wide range of unforeseen situations / changes in the workspace environment. Learning leads to autonomous functionality. Subsequently, adaptation and learning, together, are necessary functions of a high autonomy system.

Autonomy and Intelligence: Autonomy refers to the ability/property of the system in setting and achieving goals and in acting appropriately in an uncertain environment for extended periods of time without external intervention/interaction with a human operator. Intelligence relates to autonomy, as higher intelligence is necessary for higher autonomy.

Human-in/on-the-Loop and Adaptive Autonomy: Adaptive autonomy is achieved when the human operator interacts or inserts herself/himself and dictates actions or takes over functions (i.e., planning) assisting the system. (Self-) Autonomy is the progression from adaptive autonomy, and it is obtained over time; in an ideal situation, adaptive autonomy leads to full autonomy.

As such, overall system autonomy/intelligence may be evaluated as follows: Machine knowledge $\mathbf{K}$, which represents accrued information, is represented as $\mathbf{K} = -\alpha - \ln p(\mathbf{K})$ where $p(\mathbf{K})$ is the probability density of knowledge and $\alpha$ is an appropriately chosen constant. $p(\mathbf{K})$ satisfies the expression in agreement with Jaynes Principle of Maximum Entropy, $p(\mathbf{K}) = e^{-\alpha - \mathbf{K}}$ and $\alpha = \int e^{-\mathbf{K}}ds$ where the integral is over the space of the system knowledge, $\Omega_s$. The state space of knowledge $\Omega_s$ is defined in terms of states $s_i$ that represent events at the nodes of the system network defining the stages of a task to be executed. Knowledge between two states is expressed as $K_{ij} = /2w_{ij}s_{i}s_j$ with the $w$'s serving as state transition coefficients, being zero ($0$) in case of inactive transition (no association). Knowledge at state $s_i$ is the association of that state with all other active states $s_j$. The total knowledge of the system may be defined as $\mathbf{K} = \frac{1}{2}\Sigma_i \Sigma_j w_{ij}s_{ij}s_j$. This expression has the form of energy of all underlying events. Subsequently, $R_{ij} = K_{ij}/T$, $R_i = K_i/T$ and $\mathbf{R} = \mathbf{K}/T$.

The rate of knowledge $\boldsymbol{R}$ may be chosen as the main variable of the IM/IRS with discrete states, defined over a fixed interval of time $T$. Based on this rationale, and given the design constraint of IPDI, the rate of knowledge must satisfy the relation (MI): (DB) to (R).

This relation may be expressed probabilistically as Prob(MI,DB)=Prob(R) where DB is the data base associated with the specific task to be executed and represents the complexity of the task that is proportional to the precision of execution. By conditioning, taking natural logarithms and then expected values, the following Entropy equation is obtained $H(MI/DB) + H(DB) = H(R)$. A special case arises when $MI$ is independent of the $DB$, captured by $H(MI) + H(DB) = H(R)$.

This formulation and approach may be followed for the overall three-level system, and for each level, separately. Thus, autonomy and intelligence may be evaluated vertically and horizontally, for the overall system, for each component, etc. This Entropy formulation is independent of system configuration and independent of specific tools/techniques used for mission planning and execution, which makes it a desirable and suitable metric for any complex engineering system.

# 4.1 The Organization/Management Level

The top-down functions of the Management/Organization level are reasoning, planning and decision-making. The result of these functions is candidate plan generation and evaluation to find the best possible plan based on historical data and evidence, to execute an assigned mission. The bottom-up functions are feedback, adaptation/learning and update of the knowledge base. Bottom-up feedback mechanisms evaluate plan execution using a smart knowledge-base for adaptation/learning. The former may be accomplished via a general purpose stochastic approximation learning algorithm that satisfies Dvoketcky's condition for convergence [76], while the latter may be accomplished through a Dynamic Case Based Reasoning (DCBR) paradigm that stores previous cases, retrieves new ones and reasons about the health state of the system's critical components [81–84]. Figure 4 illustrates how the Organization/Management level operates, and the interactions among its components.

<div style="display: block; width: 100%"><img src="https://storage.simpletex.cn/view/m1f9dca8fd278b01494a07b8ada7f6e01" style="width: 40%; max-width: 40%" /></div> Fig. 4 Components of the Organization/Management level

Observing Fig. 3, user commands $c$ are issued (perhaps remotely), which denote the set of admissible inputs to the system $c_i$, $i=1, 2, 3, \ldots |c|$. They may be linguistic or text commands, and they represent general missions the IM/IRS is tasked to execute, i.e., <survey area $A$>. User commands are classified and translated into a format understandable by the system. The actual inputs to the system (IM, IRS) are the classified input commands $\mathbf{u}$, $u_j$, $j=1, 2, 3, \ldots |u|$. Without loss of generality, it is considered that the number of user and compiled commands is finite, that is, $|c|=|u|=M$. Commands may be corrupted by noise, $\zeta$, which may result in misclassification, i.e., $c_i \rightarrow u_i$ under correct classification, or $c_i \rightarrow u_j$, $i \neq j$ in misclassification. Complexity-wise, the classifier must choose among $M^2$ alternative decisions, $M$ of which are correct, and $M^2 - M = M(M-1)$ are misclassifications. Possible human interference $\xi$, imposes additional information in terms of constraints to the assigned mission.

The Organization/Management level is modeled via a set of internal variables $^{0}$S$_{\text{int}}$ represented as primitive events $e$. They define the task domain of the IM/IRS and they are divided into disjoint subsets of repetitive and non-repetitive primitive events. Primitive events $e$, in a probabilistic setting,$^{4}$ are either active or inactive, thus, they are represented in terms of a binary random variable $\boldsymbol{x}$, $\{e_{i} \longleftrightarrow x_{i}\}$, $i=1$, $0$, that takes as values either $0$ or $1$.

The Organization/Management level, formulates plans based on cumulative, acquired knowledge in its knowledge base (reflected and updated through feedback $f_{\mathrm{CO}}$, which is off-line feedback information) received from the lower level, the coordination level. Plans are formulated as sets of primitive events that form activities $\mathbf{A}$, ordered activities $\mathbf{O}\mathbf{A}$ in which primitive events are ordered in sequence based on precedence relations, and augmented ordered activities $\mathbf{O}\mathbf{A}_{\mathbf{A}}$ if/when (human) imposed constraints dictate 'adding' primitives to facilitate mission execution. Thus, given a mission command, machine reasoning deals with the generation of all ordered augmented activities (strings) that qualify as candidate plans.

Machine planning deals with assigning probabilities (pdfs), calculating Entropies and cross-Entropies of valid augmented and ordered strings that formulate candidate plans. That is, each plan is evaluated and ranked probabilistically; the corresponding Entropy is calculated; the best plan $Y_{|O|}$ is communicated to the coordination level. $Y_{|O|}$ is the output of the Organization/Management level, which serves as input to the coordination level (along with the feedback from the execution level,$f_{\mathrm{EC}}$). Note that inherent in this formulation is the ability to also evaluate performance against a-priori defined capabilities. This is accomplished via cross-Entropies; plans are ranked based on the distance from the best, and the one with the smallest distance, from the ideal, is chosen.

Machine decision-making deals with choosing the most probable plan (minimum Entropy), as well as the minimum distance from the best plan alternative. Consequently, all candidate plans are ranked from the best (minimum uncertainty) to the worst (maximum uncertainty). Human intervention may be imposed in terms of probabilistic constraints on the frequency of occurrence of events, which alters probability distributions and Entropy levels. For example, if there is no human-machine interaction, maximum uncertainty corresponds to the uniform distribution – the system starts from a state of maximum uncertainty; if there is human intervention in terms of imposed constraints, the distribution that corresponds to maximum uncertainty may not/will not be the uniform distribution.

The best plan candidate to execute an assigned mission formulated top-down, is passed through the coordination level that decides how the specific plan will be executed, to the execution level. Feedback is received by the Organization/Management level after actual execution.

# 4.1.1 Feedback, Adaptation and Learning Mechanisms

Following (actual) plan execution, feedback to the Organization/Management level is crucial to evaluate plan validity and to update the knowledge base. This bottom-up feedback information relates to whether the chosen plan was successfully (or not) executed. To provide a metric for success (or failure), the overall accrued cost $J_{c}$ that is associated with the specific plan execution is defined; the form of $J_{c}$ depends on the specific application problem. Then, a general stochastic approximation learning algorithm of the form

$$
p ( k + 1 / u _ { i } ) = p ( k / u _ { i } ) + \beta _ { i + 1 } [ \xi - p ( t / u _ { i } ) ]
$$

is derived and implemented, where $k$ is the iteration number, $u_i$ is the received command/input based on which a plan is formulated/chosen, $\beta_{i+1}$ is a sequence satisfying Dvoketcky's condition for convergence [76], $\xi$ is either 1 when $J'=\min J_{c}$, or, otherwise 0, and $J'$ is the actual cost of execution of the formulated plan.

However, it is more realistic to consider that the performance index is corrupted by system uncertainties. In this case, performance estimates are first updated, followed by updating the $p(k/u_i)$. Thus,

$$
J ( k + 1 / u _ { i } ) = J ( k / u _ { i } ) + \gamma _ { i + 1 } [ J _ { o b s } ( k + 1 / u _ { i } ) - J ( k / u _ { i } ) ]
$$

where $J$ is the performance estimate, $J_{obs}$ is the observed performance value, and $\gamma$ must satisfy Dvoketcky's condition for convergence. The obtained $J$'s are then used in the $\xi$ equation, subsequently calculating $p(k+1/u_i)$. By following this feedback mechanism, information and knowledge is continuously updated; a library of plans is related to each received command; and, a continuously updated metric (probability, Entropy) of success/failure during execution is associated with each plan. The Entropy equations for feedback and learning are derived from the above equations, in a similar way as shown in [90, 91]. This feedback mechanism is effective and efficient, and independent of the way plans are generated.

In parallel with the feedback mechanism, a Dynamic Case Based Reasoning (DCBR) software infrastructure is / may be considered$^{5}$ [81–84], which resides in the Organization/Management level, to house information about system requirements, performance, potential failures, etc., allowing for adaptation/learning of cases, configurations and other situations under which the system exhibits similar behaviors. The DCBR stores data and decision support tools to assist in the development and implementation of plans. It functions as the central repository of cases/algorithms to ascertain that pertinent strategies are executed effectively, robustly and efficiently. Cases from historical evidence are stored, and new cases are compared with stored ones to determine the current system (IM, IRS) state. This is crucial because machine reasoning determines similarity between strategies (stored in memory) and potential new ones that may also be applied.

A generalized similarity by proximity expression may be used to evaluate the similarity between a new case (new plan) and cases previously presented and stored (previous plans), which may be calculated based on the scoring function:

$sim(Ent e , Ent j ) = \frac{\sum_{k=1}^{n} \alpha \times sim(Ent i,k , Ent j,k ) + \sum_{k=1}^{n} n k,i , pred i × n i , pert × sim(Ent i,k , Ent j,k )}{\alpha \times n + \sum_{k=1}^{n} n k,i , pred i × n i , pert$

$Ent_{t}$ is a new case presented to the system; $Ent_{j}$ represents cases previously presented; $El_{i}$ is a feature or an attribute or value pair; $n_{i, pert}$ is a pertinence weighted variable



<div style="display: block; width: 100%"><img src="https://storage.simpletex.cn/view/mcd6698e0cd6f5e0bf95232beea38f9d6" style="width: 40%; max-width: 40%" /></div> Fig. 5 Structure of the coordination level. General configuration in terms of different coordinators

associated with the description element $E_{l}$; $n_{i, pred}$ is a predictive weighted variable associated with each case in memory, which is increased as the corresponding element (feature) is favorably selecting a case, and decreased as this selection leads to a failure; $\alpha$ is an adjustable parameter. The similarity expression returns a number in the $[0, 1]$ interval, thus, the scoring function provides supplemental information (in addition to the feedback mechanism) related to how close (or not) plans may be. Further, incremental learning may occur whenever a new case is processed and its results are identified. The knowledge base (memory) keeps track of each of its experiences/cases, whether labeled as success or failure in a declarative way being ready to take advantage of future experiences.6 Combined, the feedback mechanism and the DCBR provide the dynamically updated knowledge base that stores all cases faced by the IM/IRS. Each plan is associated with metrics of success/failure and similarity indices with other plans. This information is updated every time a plan is executed. In a similar way, information about a simple task is also be stored/updated.

# 4.2 Coordination Level

The coordination level is an intermediate structure that dispatches organizational information to the execution level. Its objective is the actual formulation of the control problem associated with the most probable plan that will be executed in real-time. Figure 5 depicts the most general configuration of the coordination level. It is composed of a set of individual coordinators with fixed structure (i.e., vision coordinator). Their intelligence is related to how to execute the plan in the best possible way.

The coordination level involves decision-making associated with specific knowledge/information processing based on the best-chosen plan. The flexibility of the coordination level and its ability to formulate alternate real-time scenarios is influenced by the specific structure of the dispatcher (for example, automata and Petri Nets may be used [89]). It is logical to assume that each task (event) specifics are stored (and updated) in the dispatcher memory, and this information is passed to the specific coordinators that are needed to execute the task. Different coordinators may not communicate directly with each other, but through the dispatcher; however, task decomposition is both temporal and spatial. Temporal decomposition corresponds to sequential execution and spatial decomposition corresponds to tasks executed by more than one coordinator.

A specific configuration of the coordination level of a robotic vehicle system is depicted in Fig. 6. The uncertainty related to each coordinator is calculated in terms of Entropy. For example, when the vision coordinator is tasked to recognize (and avoid) an object, the uncertainty of the recognition process may be determined in terms of the object's positional and orientational Entropy, $H_v = H_P + H_O$ [43, 89–91, 112, 113]. The same approach holds true for the other coordinators, too [43]. The motion control coordinator problem is formulated using Entropy, as well as the path planning coordinator problem (finding the most probable path to be followed). The sensor coordinator has similar properties with the vision coordinator. Thus, the total horizontal Entropy of the formulation of the specific execution scenario of the best plan formulated by the organizer is the sum of the corresponding Entropies. Minimization is performed in the uncertainty associated

<div style="display: block; width: 100%"><img src="https://storage.simpletex.cn/view/m04fe666c23727adc6abfe75f5cb1cd39" style="width: 40%; max-width: 40%" /></div> Fig. 6 Robotic vehicle system coordination level with four different coordinators with each coordinator, as each coordinator has different characteristics.

# 4.3 Execution Level

When it comes to the execution level, precision/accuracy of task/plan execution requires minimization of a cost function (or performance index) [43]. Details of the Entropy approach to the actual control problem were presented in Section 3. To summarize, starting with a performance index defined in classical control theory as $J_P = J\{V(q(t), u(t), t)\}$, where $J_P$ denotes the specific plan/task to be executed and $V$ is a function of system states, control action and time, and by defining this performance index as an Entropy function $H(x_o, u, p(u)) = E\{V(x_o, u, t)\}$, minimization leads to maximum precision execution. Details may be found in [90, 91].

# 4.4 The Generalized Partition Law of Information Rates (GPLIR)

The GPLIR is presented in detail in [43, 44, 54]. It is summarized here because of its generality and ability to capture component dependences within a system, and its implementation flexibility to quantify uncertainty and flow of information i.) throughout the overall system, ii.) within each level of the system. Considering Fig. 3, any three-level hierarchical system is modeled as a dynamic system ($DS$) composed of three subsystems, $S_O$, $S_C$, $S_E$

$$
D S = \{ S _ { O } , S _ { C } , S _ { E } \}
$$

A model is defined for each level (subsystem) based on its corresponding inputs, outputs and internal variables (See Fig. 3) as

$$
S _ { O } = \{ u , \zeta , \xi , f _ { \mathrm { C O } } , ^{0} S _ { \mathrm { i n t } } , Y _ { | O | } \}
$$

$$
S _ { C } = \{ Y _ { | O | } , f _ { \mathrm { E C } } , ^{\mathrm { ~ C ~} } S _ { \mathrm { i n t } } , F _ { | C | } \}
$$

$$
S _ { E } = \{ F _ { | C | } , ^{\mathrm { ~ E ~} } S _ { \mathrm { i n t } } , Z _ { | E | } \}
$$

Alternatively, when looking at the overall multi-level (three-level) system from the input-output point of view, the combined model is derived as

$$
D S = \{ \, S _ { O } , \, S _ { C } , \, S _ { E } \} = \{ u , \, \zeta , \, \xi , f _ { \mathrm { C O } } . f _ { \mathrm { E C } } , \, ^{\mathrm { o} } S _ { \mathrm { i n t } } , \, ^{\mathrm { c} } S _ { \mathrm { i n t } } , \, ^{\mathrm { E} } S _ { \mathrm { i n t } } . Z _ { | E | } \}  ( 26 )
$$

where the augmented input is $U = \{\boldsymbol{u}, \ \zeta, \ \xi\}$, internal variables are $S_i = \{\boldsymbol{f}_{\mathrm{CO}}, \boldsymbol{f}_{\mathrm{EC}}, \ \mathrm{^oS_{\mathrm{int}}}, \ \mathrm{^cS_{\mathrm{int}}}, \ \mathrm{^eS_{\mathrm{int}}}\}$ and the output is $\mathbf{Z}_{|E|}$.

The main differences between the GPLIR and the original PLIR are: i.) the GPLIR considers external and internal noise, as well as internal control strategies and internal coordination of the levels and between the levels to execute the requested mission; ii.) a corresponding GPLIR may be derived for each top-down and bottom-up function of the organizer; iii.) the GPLIR is also derived for the coordination and execution levels.

The advantage of this formulation is that it allows for single level-optimization (horizontal), as well as overall system optimization (vertical). Depending on specific mission requirements corresponding to total rate of information flow $F$, tradeoffs may be considered and evaluated with respect to how system intelligence is influenced. It is because of the additive properties of Entropy that this is possible.

# 5 Conclusions

The aim of this review paper is to register research findings related to intelligent control as applied to hierarchical multi-level systems, and, in particular, intelligent machines and intelligent robotic systems. The objective is to show how and why Entropy may be used as one, unified measure to evaluate intelligence, autonomy and precision of task execution in such systems. When focusing on IMs or IRSs, it is shown how the Entropy approach to control and evaluation of such systems is implemented level-wise and overall system-wise.

Functionality-wise, an IN or IRS functions as follows: After receiving commands from human operators, the organizer (a) reasons about the received command and formulates conflict-free augmented ordered activities as strings of primitive events that formulate admissible plans; (b) evaluates admissible plans based on accrued information that is reflected through probability distributions and calculated Entropies; (c) ranks all admissible plans from best to worst, and, (d) after execution, updates though adaptation/learning the DCBR. The output from the organizer is a sequence of events (binary string), such as "Survey Area Z", "Create a map of area Z", etc., which is passed to the coordination level.

Events at the coordination level are translated into specific sequences of basic actions (i.e., maneuvers, trajectories, specific control algorithms) that are used by the execution level for actual plan execution. There is information flow (signal flow) from the execution level to the coordination level, such as sensor readings. This information is abstracted into events such as "Help Request to Survey Area Z" that are understood by the organization and/or coordination levels. In this way, the upper levels get feedback and are aware of the status of the overall system.

If the environment changes, the mission fails, or mission requirements change, the process is repeated to generate alternative plans. Human involvement is in terms of imposed constraints.

In conclusion, the organization level deals with the uncertainty of choosing the best plan before executing an assigned mission. The coordination level deals with the uncertainty of deciding how to execute a specific plan. The execution level is cast as a control problem with objective maximum precision. Intelligence is measured in terms of Entropy. Robust intelligence is demonstrated in terms of the $H_{max} - H_{min}$ interval and cross-Entropy. Autonomy is defined with respect to a set of goals. A system is autonomous regarding a set of goals, with respect to a set of measures of intervention. A perhaps more useful working definition of an autonomous system is that a system has high or low degree or level of autonomy regarding a goal. By high degree/level of autonomy it is meant that the degree/level of human intervention (or perhaps intervention by other engineered systems) is low, while by low degree/level of autonomy, a high degree/level of human intervention is implied. Under this consideration, the proposed formulation is suitable to measure system autonomy.