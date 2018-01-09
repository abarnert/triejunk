# triejunk
A simple trie implementation

This is probably useless, except to test whether I remember how a trie works
well enough to build one in under half an hour. But if someone else finds a
use for it, more power to you. (But I'm sure there are a variety of good trie 
classes on PyPI.)

# Interface

`Trie` is a MutableMapping (with the usual `dict` constructor API), but only 
strings can be used as keys (although there's no type checking).

The only additional method is `_dump`, which can be used to get a graphical 
representation of the trie structure.

In particular, there's no prefix-find method, or anything for manipulating
subtries, that you'd want to use for typical trie applications like 
autocomplete suggestions.

## Example

You use a `Trie` the same way as a `dict`; the only visible interesting
difference is the `_dump` method:

    >>> Trie({'A': 15, 'i': 11, 'inn': 9, 'toe': 7, 'tea': 3, 'ted': 4, 'ten': 12})._dump()
    {'A': (15, {}),
     'i': (11, {'n': {'n': (9, {})}}),
     't': {'e': {'a': (3, {}), 'd': (4, {}), 'n': (12, {})}, 'o': {'e': (7, {})}}}

The head contains three nodes. The `A` and `i` nodes have values, but the `t`
doesn't; the `i` and `t` have children, but the `A` doesn't. And so on recursively.

## Implementation

A `Trie` object is just a node, not a wrapper around a head node. This
allows easy tail sharing, which is important for many trie applications,
although since there's no usable interface to get at the tails, it's not as
useful as it sounds. (The no-wrapper implementation also allows every method
to be quickly implemented recursively and then converted to iterative 
implementations at leisure.)

Each node just contains children (mapped by char) and value. For nodes with
no value, there's still a `_value` attribute; it's just set to a special
value. Which of those is better depends on what you're trying to optimize,
and there's no attempt at optimization here.

Iterating large tries is probably particularly inefficient. Besides being
recursive, the `__iter__` method also concatenates the keys by quadratically 
adding each char on the left (which also means each prefix is built over and
over instead of just once).

The only thing that prevents this from being used for `bytes`-like keys is
that `''` is hardcoded as the empty key. That's easily fixable. Using it
for keys that are arbitrary sequences would require a bit more change, but
still not much.

A (space-)optimized trie would use `__slots__`, and possibly something more 
compact than a general-purpose `dict` for the children.

The `test` function tests details of the internal structure, not just the API.
