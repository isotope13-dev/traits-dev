## Range literal syntax (`[1..9]`)

Considered as a shorthand for constructing a `list of int`
sequence:

```jennifer
# what range literal would let us write
def xs as list of int init [1..9];
for (def i in [1..len($items)]) { ... }
```

Borrowed from Haskell / Kotlin / Ruby's syntactic form.

Rejected because:

- **Parallel API to the `[1, 2, 3]` list literal.** Two syntaxes
  for "construct a `list of int`" - same family as `++`, `+=`,
  and ternary. Stance #1 has rejected every previous instance.
- **Hides materialization cost (stance #2).** `[1..big_number]`
  silently allocates a million-element list. The explicit
  `for (def i init 1; $i <= n; ...)` loop iterates without
  materializing, and the cost shows up at the call site instead
  of being buried in a two-character `..` operator. A library
  function call (`lists.range(...)`) makes the allocation
  visible too; the literal form does not.
- **New single-purpose operator.** Jennifer hasn't introduced an
  operator that works in exactly one context before; every other
  operator (`+ - * / // % & | ^ ~ << >> < > <= >= == and or not`)
  works across multiple types or contexts. `..` only does
  integer ranges. Once it ships we'd have to defend "why doesn't
  `[1.0..9.0]` work? why not `["a".."z"]`?" - each extension
  another design discussion.
- **Pattern set elsewhere.** Jennifer ships `lists.head` /
  `lists.tail` instead of Python `xs[:n]` / `xs[n:]` slicing
  syntax; `strings.substring` instead of `s[i:j]`; index-write
  `$xs[i] = v;` instead of pythonic `$xs[i:i+1] = [v]`. Library
  functions over syntax for collection operations is the
  established Jennifer pattern.

The chosen rule: ship `lists.range(start, end)` (M15.0) as the
canonical way to allocate an integer sequence. Use site reads as
"this allocates a list" instead of hiding behind two characters
of punctuation. See
[milestones.md > M15](../milestones.md#m15---foundational-libraries--first-public-release)
(M15.0).
