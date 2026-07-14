# IEEE Editing Mathematics — rules digest

Repo-side documentation; not installed with the skill. This digest records the math-editing rules
from *Editing Mathematics* (IEEE Publication Operations) that inform the skill, so their
provenance survives independently of the source document.

- Source: IEEE Publication Operations, *Editing Mathematics*, V 10.27.2023, © 2023 IEEE.
  Accessed 14 July 2026 via a published copy supplied by the maintainer.
- Encoded in the skill: "Mathematical notation and equation editing" in
  [`manuscript-structure-style.md`](../../skills/ieee-acm-paper-writing/references/manuscript-structure-style.md).
- Precedence: the current edition of the guide and venue-specific author instructions override
  everything below.
- Fidelity note: the source renders many equations as embedded images; those did not survive
  text export and are marked `[equation image]` or `[image]` below. Rules whose meaning depends
  on a lost image are reconstructed in the distilled skill reference, not here.

## A. The Language of Math

When editing technical publications it is important to remember that the mathematics often
carries as much if not more meaning than the body of text itself. Therefore, it is critical that
the grammar of an equation be taken into account when editing.

Most equations should read like a sentence. They should contain a noun and a verb and often
contain adjectives, prepositional phrases, conjunctions, and conditions. Equations also contain
punctuation. When math occurs along with text it shares the grammatical characteristics of the
text. A displayed expression may be a main or subordinate clause, an expression in apposition, a
direct object, an item in a list, or the object of a preposition. **Use a comma at the end of
introductory sentences after: i.e., e.g., "Hence" or "That is." Use a colon after words such as
"following" or "as follows."** There should be no punctuation after forms of the verb *to be*, or
between a verb and its object or a preposition and its object. IEEE style dictates that the only
punctuation used at the end of an equation is a period. There is, however, other punctuation
permitted in the equation itself and between an equation and its condition. This interior
punctuation contains mathematical meaning and must not be changed.

Some examples of interior punctuation are as follows.

*Mathematical ellipses:*

> *I* = 1, 2, 3, … , *n*

**NOTE:** *Only three dots* are used and they are enclosed by commas and are on the baseline.

*Matrix:* `[equation image]`

**NOTE:** There is a centered operator, equation number, and period.

*Parenthetic statement:*

> *v*(*t*) = *u*(*t*),  *t* = 1, 2, …, *m*.

**NOTE:** There is a 2em space after the comma and before the condition *t* = 1, 2, …, *m*.
Multiple conditions should be separated with a semicolon, with a comma at the end of the
equation, a 2em space, and the condition aligned on the operator.

## B. In-Line Equations and Expressions

An inline equation is an equation within text or part of a paragraph. It is not displayed.

- *Rule 1:* Equations appearing in text should be broken after a verb or an operator, meaning,
  if at all possible, the verb or operator should remain on the top line of text.
- *Rule 2:* Fractions should not appear stacked in line. `[stacked fraction image]` should be
  written with a solidus or negative exponent.
- *Rule 3:* Collective signs should not appear with limits to top and bottom, but to the side
  instead.
- *Rule 4:* Use Roman function exp instead of *e* followed by a lengthy superscript.
  `[image]` should be written as exp[(*zx*² + *y*)(α − 2*yx*) + *zx*].
- *Rule 5 (optional):* Avoid square roots (radical signs) having long bars. `[image]` should be
  rewritten as (*x* + α)^½.

## C. Break/Alignment Rules

- *Rule 1:* Break equations at verbs and align on same when possible for a displayed equation.

  ```text
  A = (5α + x) + (10y + β)²
    ≥ (5x − α + y + x²)
    ≡ B²
  ```

- *Rule 2:* In equations with one verb, break at operators and align to the right of the verb.

  ```text
  A = (5α + x)
      + (10y + β)²
      − (5x − α + y + x²)
  ```

- *Rule 3:* Separate all equations with 1) an em quad if they fit on one line or 2) stack and
  align on the verb.
- *Rule 4:* An equation that will fit conveniently on two lines without further breaks should be
  broken at the verb and aligned flush left/flush right over the column width.
- *Rule 5:* When breaking an equation within fences, break at an operator and align inside the
  left-hand fence. **NOTE:** Pairs of fences should match in size and be proportional to the math
  within.
- *Rule 6:* A period is placed at the end of a fraction, case equation, or closed delimiters.
  **NOTE:** Pairs of fences should match in size and be proportional to the math within.

## D. Exceptions and Oddities

- *Right-to-left equations:* Equations in which the verb appears in the right half of the
  statement are broken before an operator and aligned to the left of the verb.

  ```text
  5α + x + 10y
  + β² + z = x
  ```

- *Solidus as operator:* Break after a solidus and align the next line to the right of the verb.
- *Implied product:* When a set of fences is followed directly by another set of fences, the
  equation may be broken between them, provided a multiplication sign (×, ·) is inserted.
  Alignment is to the right of the verb as for other operators.

  ```text
  x = (−b + 4ac)(a − 2bc)
      × (−c + 3ab)
  ```

- *Integrals and differentials:* If an equation containing an integral must be broken before the
  differential expression, break at an operator and align to the right of the integral. It is
  preferential not to break this type of equation until a differential occurs, then break after
  the differential expression.

## E. Headings for Theorems, Proofs, and Postulates

Some articles do not conform to an outline style for theorems and proofs that is easily
transformed into the normal heading sequence. The preferred style is to set the head giving the
theorem number as a tertiary heading (no Arabic numeral preceding) and the proof head as a
quaternary head. This rule also applies to Lemmas, Hypotheses, Propositions, Definitions,
Conditions, etc.

## F. Numbered Display Equations

- *Consecutive numbering:* Equations within an article are numbered consecutively from the
  beginning of the article to the end. There are some Transactions in which an author's own
  numbering system such as numbering by section, e.g., (1.1), (1.2.1), (A1), is permitted.
- *Appendix equations:* Continued consecutive numbering of equations is best in the Appendix,
  but if an author starts equation numbering over with (A1), (A2), etc., for Appendix equations,
  it is permissible to leave the copy as is.
- *Hyphens and periods:* Hyphens and periods are usually removed from equation numbers, i.e.,
  (1a) rather than (1-a) and (2a) rather than (2.a). This should be done consistently throughout
  the article.

## G. Reminders

- *Algorithms:* Algorithms should not be edited. Keep title, formatting, punctuation, and
  placement as provided by the author. When positioning is unclear, an algorithm may be placed
  in-line within text or at the end of a paragraph if an introductory sentence or phrase
  precedes it (e.g., "as shown in the following"; "in the process below"; or "as follows in
  Algorithm 1"). Otherwise, float an algorithm to the top of the page when it is cited by only
  its number or title.
- *Angle brackets:* Angle brackets are not the same as greater-than and less-than signs.
- *Vectors:* Vectors are usually made boldface (if distinguished by the author).
- *Thin spaces and Roman functions and differentials:* Thin spaces occur on either side of both
  functions and differentials.

  > Incorrect: sin*t* = log*μr*  Correct: sin *t* = log *μr*

  However, a thin space is not necessary when functions and differentials are preceded or
  followed by verbs or an operator.

## H. Short Reference List of Italics, Roman, and Small Capitals

| Italics | Roman | Small caps |
| --- | --- | --- |
| *RC* | p-n, p-i-n, p⁺-n-p⁺⁺ and variations thereof (do not forget the hyphen) | A.M., P.M. |
| *RL* | NOR | |
| *I-V* | OR | |
| *LC* | ORing | |
| *S/N* | ORed | |
| *f/22* | SNR | AND |
| | O ring | NAND |
| | T junction | ADD |
| | Y-connected circuit | DIFFER |
| | class-A amplifier | EXTRACT |
| | 2N5090 transistor | XOR |
| | e.g., | EXCLUSIVE OR |
| | i.e., | DIMENSION |
| | viz., | GO TO |
| | Fortran IV | DO |
| | Algol 60 | READ |
| | Cobol | WRITE |
| | Atlas Autocode | PRINT |
| | PL/1 | CONTINUE |
| | BAL | PAUSE |
| | cf., | FORMAT |
| | Tr | END |
| | Ke | ON |
| | Im | OFF |
| | et al. | IGFET |
| | in situ | IMPATT |
| | inter alia | TRAPATT |
| | in toto | ONE |
| | in vivo | ZERO |
| | in vitro | BARITT |
| | a priori | |
| | a posteriori | |

## I. Functions and Operators Always Set in Roman Font

| Function | Meaning |
| --- | --- |
| ad | adjoint |
| arg | argument |
| cos | cosine |
| cosh | hyperbolic cosine |
| cot | cotangent (do not use ctg) |
| coth | hyperbolic cotangent |
| csc | cosecant (do not use cosec) |
| csch | hyperbolic cosecant |
| curl | curl |
| det | determinant |
| diag | diagonal |
| dim | dimension |
| div | divergence |
| exp | exponential |
| hom | homology |
| Im | imaginary |
| inf | inferior (infimum) |
| ker | kernel |
| lim | limit |
| liminf | limit inferior |
| limsup | limit superior |
| ln | natural logarithm |
| log | logarithm |
| lub | least upper bound |
| max | maximum |
| min | minimum |
| mod | modulus |
| Pr | probability |
| Re | real |
| sec | secant |
| sin | sine |
| sinh | hyperbolic sine |
| tan | tangent |
| tanh | hyperbolic tangent |
| tr | trace |
| Tr | transpose |
| wr | wreath |

## J. Glossary

- *Base line:* The imaginary line connecting the bottoms of capital letters.
- *Collective signs:* Term used to describe a certain group of mathematical symbols including
  sums, products, unions, and integrals.
- *Differential:* Identifiable as being *d* or delta (Δ, δ) combinations.
- *Em quad:* Unit of linear measurement equal to the point size of the type font being used.
- *En quad:* Half an em quad.
- *Fences:* Any one of several signs of aggregation such as parens ( ), brackets [ ], or angle
  brackets ⟨ ⟩, having the following hierarchy when nested: {[( )]}.
- *Indices:* Subscripts and superscripts which are inferior and superior, respectively, to the
  symbols on the base line. First-order indices attach to base-line symbols; subscripts and
  superscripts on first-order indices are second-order indices. *Note:* Plural of index is
  indices in math.
- *Matrix:* A rectangular array of mathematical terms written between fences.
- *Operator:* A mathematical symbol that indicates an operation to be performed, e.g., +, −, /, ×.
- *Roman functions:* Functions and operators typically set in Roman font.
- *Solidus:* A slanted line used between the parts of a fraction such as 3/4. Also known as
  "shilled."
- *Stacked fraction:* A fraction in which the numerator is set above a rule and the denominator
  is set below, in contrast to a fraction set with a solidus. Also known as "built up."
- *Thick space:* Not usually used but approximately one-third of an em space.
- *Thin space:* Approximately one-fifth of an em space. Used around Roman functions.
- *Verb:* A mathematical symbol indicating a relationship, e.g., =, ≥, ≤, >, <.

Near-equality symbols:

- ≈ (`\approx`) — usually to indicate approximation between numbers.
- ≃ (`\simeq`) — usually to indicate asymptotic equivalence between functions; using ≈ for this
  would be wrong, despite being widely used.
- ∼ (`\sim`) — usually to indicate proportionality between functions.
- ≅ (`\cong`) — usually to indicate congruence between figures.

## K. The Greek Alphabet

| Name | Uppercase | Lowercase |
| --- | --- | --- |
| Alpha | Α | *α* |
| Beta | Β | *β* |
| Gamma | Γ | *γ* |
| Delta | Δ | *δ* |
| Epsilon | Ε | *ε* |
| Zeta | Ζ | *ζ* |
| Eta | Η | *η* |
| Theta | Θ | *θ* |
| Iota | Ι | *ι* |
| Kappa | Κ | *κ* |
| Lambda | Λ | *λ* |
| Mu | Μ | *μ* |
| Nu | Ν | *ν* |
| Xi | Ξ | *ξ* |
| Omicron | Ο | ο |
| Pi | Π | *π* |
| Rho | Ρ | *ρ* |
| Sigma | Σ | *σ* |
| Tau | Τ | *τ* |
| Upsilon | Υ | *υ* |
| Phi | Φ | *φ* |
| Chi | Χ | *χ* |
| Psi | Ψ | *ψ* |
| Omega | Ω | *ω* |

## L. Common Mathematical Function Name Abbreviations and Symbols (use Roman for these symbols)

| Notation | Meaning |
| --- | --- |
| *ℓ* | Script ell, used to distinguish ell from one; set as italic ell. |
| exp (*x*) | Exponential function of *x*; = *e*^*x*. |
| *e* | Base of natural logarithms. |
| ln *x* | Natural logarithm of *x*. |
| log₂ *x* | Logarithm, base 2, of *x*. |
| log *x*, log₁₀ *x* | Common logarithm of *x*. |
| Δ*x* | Finite increase of *x*. |
| δ*x* | Variation of *x*. |
| *dx* | Total differential of *x*. |
| ∂*x* | Partial differential of *x*. |
| *f*(*x*) | Function of *x*. |
| lim *f*(*x*) | Limit of *f*(*x*). |
| lim(*x*→*a*) *f*(*x*) | Limit of *f*(*x*) as *x* approaches *a*. |
| l.i.m. *f*(*x*) | Limit in the mean. |
| min *f*(*x*) | Minimum of *f*(*x*). |
| maxᵢ *f*(*x*) | Maximum of *f*(*x*) over *i*. |
| inf | Infimum (greatest lower bound). |
| supₓ | Supremum over *x* (least upper bound). |
| Pr (*a*) | Probability of *a* (do not use Prob., *P_r*). |
| Re *z* | Real part of *z* (use Re). |
| Im *z* | Imaginary part of *z*. |
| arg *z* | Argument of *z*. |
| det | Determinant. |
| diag | Diagonal. |
| int | Integer value. |
| cov | Covariance. |
| var | Variance. |
| sgn *x* | Signum function of *x*. |
| sinc *x* | (sin *x*)/*x*. |
| sn, cn, dn, an | (Sinus) Jacobian elliptical functions. |
| grad | Gradient. |
| div *V* | Divergence of *V*; ∇ · *V*. |
| curl *V*, Rot *V* | Curl of *V*; ∇ × *V*. |
| tr | Trace. |
| Tr | Transpose. |
| \|*A*\| | Absolute value of *A*. |
| *A*ᵀ | Transpose of matrix *A*. |
| *A*\* | Complex conjugate of *A*. |
| *A*† | Hermitian conjugate of *A*. |
| Si (*z*) | Sine integral. |
| Ci (*z*) | Cosine integral. |
| Cin (*z*) | Cosine integral, Cin (*z*) = −Ci (*z*) + ln *z* + γ. |
| Shi (*z*) | Hyperbolic sine integral. |
| Chi (*z*) | Hyperbolic cosine integral. |
| Ei (*z*) | Exponential integral. |
| li (*z*) | Logarithmic integral. |
| Ai (*z*) | Airy integral. |
| erf *z* | Error function. |
| erfc *z* | 1 − erf *z*. |

### Trigonometric functions

| Notation | Meaning |
| --- | --- |
| sin | sine |
| cos | cosine |
| tan | tangent (not tg) |
| cot | cotangent (not ctn or ctg) |
| sec | secant |
| csc | cosecant (not cosec) |
| arcsin/sin⁻¹, arccos/cos⁻¹, arctan/tan⁻¹, arccot/cot⁻¹, arcsec/sec⁻¹, arccsc/csc⁻¹ | Inverse trigonometric functions. |

### Hyperbolic and related functions

| Notation | Meaning |
| --- | --- |
| sinh, cosh, tanh, coth, csch | Hyperbolic functions. |
| ver *A* | versine *A*; 1 − cos *A*. |
| covers *A* | coversine *A*; 1 − sin *A*. |
| havers *A* | haversine *A*; ½ vers *A*. |
| exsec *A* | exsecant *A*; sec *A* − 1. |
| *p*! | *p* factorial; 1 · 2 · 3 ⋯ *p*. |
| gaf | Gaussian distribution function. |
| gafc | 1 − gaf. |

### Selected symbols

| Symbol | Meaning |
| --- | --- |
| ′ ″ ‴ | Prime, double prime, triple prime. |
| ° | Degree. |
| ∵ | Because or since. |
| ∴ | Therefore. |
| ∝ | Varies as, proportional to. |
| ∞ | Infinity. |
| ± ∓ | Plus or minus; minus or plus. |
| ≠ | Is not equal to. |
| ≈ | 1) Approximately equal to. 2) Asymptotic to. 3) Equal to in the mean. |
| ≃ | 1) Similar to. 2) Geometrically equivalent, congruent to. 3) Equal or nearly equal to. |
| ∼ | 1) Difference between. 2) Is equivalent to. 3) Asymptotic to. 4) Similar to. 5) On the order of. 6) The complement of. 7) Negation sign (math. logic). |
| ≳ ≲ | Greater/less than or equivalent to. |
| ≪ ≫ | Much less than; much greater than. |
| ≤ ≥ | Less/greater than or equal to. |
| ≐ | 1) Approaches the limit. 2) Approaches in value to. |
| ⊂ ⊃ ⊆ ⊇ | Set containment (proper subclass / subclass variants). |
| ∩ ∪ | Intersection ("cap"); union ("cup"). |
| ∀ ∃ ∍ | For all; there exists; such that. |
| ∈ ∉ | Is / is not an element of. |
| ≡ ≢ | Is / is not congruent (or identical, or definitionally identical) to. |
| ∤ | Does not divide. |
| → ← ↑ ↓ | Limit/implication arrows; tends up/down to the limit. |
| ⇔ | Implies and is implied by; if and only if. |
| ↔ | 1) Mutually implies. 2) One-to-one correspondence. 3) Corresponds reciprocally. 4) Asymptotically equivalent to. |
| ∫ ∮ | Integral; contour integral. |
| ∂ | Partial differentiation sign. |
| Γ | Gamma function. |
| Σ Π | Summation sign; product sign. |
| ℘ | Weierstrass elliptic function. |
| א | Aleph (transfinite cardinals). |
| O, *o* | Of order [O(*x*)]; of lower order than [o(*x*)]. |
| \| | 1) Modulus (\|*x*\|). 2) Joint denial (math. logic). 3) Divides (number theory). |
| ‖ | Parallel to. |
| / | Divided by (solidus). |
| √ ∛ ∜ | Square, cube, fourth root. |
