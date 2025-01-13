## What is a function?
Given two sets $A$ and $B$, a **function** from $A$ to $B$ is a rule or mapping that takes each element $x \in A$ and associates with it a single element of $B$. In this case, we write $f : A \to B$. Given an element $x \in A$, the expression $f(x)$ is used to represent the element of $B$ associated with $x$ by $f$. The set $A$ is called the **domain** of $f$. The **range** of $f$ is not necessarily equal to $B$ but refers to the subset of $B$ given by $\{ y \in B : y = f(x) \text{ for some } x \in A \}$.

## Two numbers are equal if and only if?
Two real numbers $a$ and $b$ are equal if and only if for every real number $\epsilon > 0$ it follows that $|a - b| < \epsilon$.

## What is the Axiom of Completeness?
Every nonempty set of real numbers that is bounded above has a least upper bound.

## What do bounded above and bounded below mean?
A set $A \subseteq \mathbb{R}$ is **bounded above** if there exists a number $b \in \mathbb{R}$ such that $a \leq b$ for all $a \in A$. The number $b$ is called an **upper bound** for $A$. Similarly, the set $A$ is **bounded below** if there exists a lower bound $l \in \mathbb{R}$ satisfying $l \leq a$ for every $a \in A$.

## What is the least upper bound for a set?
A real number $s$ is the **least upper bound** for a set $A \subseteq \mathbb{R}$ if it meets the following two criteria:
1. $s$ is an upper bound for $A$.
2. If $b$ is any upper bound for $A$, then $s \leq b$.

## What are the maximum and minimum of a set?
A real number $a_0$ is a **maximum** of the set $A$ if $a_0$ is an element of $A$ and $a_0 \geq a$ for all $a \in A$. Similarly, a number $a_1$ is a **minimum** of $A$ if $a_1 \in A$ and $a_1 \leq a$ for every $a \in A$.

## Lemma 1.3.8
Assume $s \in \mathbb{R}$ is an upper bound for a set $A \subseteq \mathbb{R}$. Then, $s = \sup A$ if and only if, for every choice of $\epsilon > 0$, there exists an element $a \in A$ satisfying $s - \epsilon < a$.

## What is the Nested Interval Property?
For each $n \in \mathbb{N}$, assume we are given a closed interval $I_n = [a_n, b_n] = \{x \in \mathbb{R} : a_n \leq x \leq b_n \}$. Assume also that each $I_n$ contains $I_{n+1}$. Then, the resulting nested sequence of closed intervals
$$
I_1 \supseteq I_2 \supseteq I_3 \supseteq I_4 \supseteq \cdots
$$
has a nonempty intersection; that is, $\bigcap_{n=1}^\infty I_n \neq \emptyset$.
