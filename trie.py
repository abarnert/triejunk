#!/usr/bin/env python3

# TODO: Comments

import collections
import collections.abc

class Trie(collections.abc.MutableMapping):
    _empty = object()
    def __init__(self, iterable_or_mapping=None, **kv):
        self._children = {}
        self._value = Trie._empty
        self._len = 0
        if isinstance(iterable_or_mapping, collections.abc.Mapping):
            for k in iterable_or_mapping:
                self[k] = iterable_or_mapping[k]
        elif iterable_or_mapping is not None:
            for k, v in iterable_or_mapping:
                self[k] = v
        for k, v in kv.items():
            self[k] = v
    def __repr__(self):
        return '{}({})'.format(type(self).__name__, dict(self))
    def _dump(self):
        d = {char: child._dump() for char, child in self._children.items()}
        if self._value is Trie._empty:
            return d
        else:
            return self._value, d
    def __getitem__(self, key):
        node = self
        for char in key:
            try:
                node = node._children[char]
            except KeyError:
                raise KeyError(key)
        if node._value is Trie._empty:
            raise KeyError(key)
        return node._value
    def __setitem__(self, key, value):
        node = self
        ikey = iter(key)
        try:
            for char in ikey:
                node = node._children[char]
        except KeyError:
            node._children[char] = Trie()
            node = node._children[char]
            for char in ikey:
                node._children[char] = Trie()
                node = node._children[char]
        if node._value is Trie._empty:
            self._len += 1
        node._value = value
    def _delitem(self, key):
        # TODO: non-recursive implementation
        if not key:
            if self._value is Trie._empty:
                raise KeyError(key)
            self._value = Trie._empty
            return len(self._children) == 0
        # let KeyError pass through
        child = self._children[key[0]]
        if child._delitem(key[1:]):
            del self._children[key[0]]
        return self._value is Trie._empty and len(self._children) == 0
    def __delitem__(self, key):
        try:
            self._delitem(key)
        except KeyError:
            raise KeyError(key)
        else:
            self._len -= 1
    def __iter__(self):
        # TODO: non-recursive implementation
        if self._value is not Trie._empty:
            yield ''
        yield from (char+key for char, child in self._children.items()
                    for key in child)
    def __len__(self):
        return self._len

def test():
    d = {'A': 15, 'i': 11, 'inn': 9, 'toe': 7, 'tea': 3, 'ted': 4, 'ten': 12}
    def _test(t):
        for k, v in d.items():
            assert t[k] == v
        try:
            t['in']
        except KeyError:
            pass
        else:
            assert False
        assert len(t) == len(d)            
        node = t._children['i']._children['n']
        assert node._value is Trie._empty
        assert len(node._children) == 1
        t['in'] = 3
        del t['inn']
        del t['i']
        assert node is t._children['i']._children['n']
        assert node._value == 3
        assert len(node._children) == 0
        t['inn'] = 8
        assert node is t._children['i']._children['n']
        assert len(node._children) == 1
    _test(Trie(d))
    _test(Trie(**d))
    t1 = Trie(d)
    t2 = Trie()
    for k in sorted(d, reverse=True):
        t2[k] = d[k]
    assert t1 == t2
    _test(t2)
    
