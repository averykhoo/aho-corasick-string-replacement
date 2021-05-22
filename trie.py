from abc import ABC
from abc import abstractmethod
from typing import Optional
from typing import Tuple
from typing import Type
from typing import Union


class Match:
    """
    match result (similar to re.Match)

    todo: find some way to normalize to char index instead of token index?
    but because the input is already tokenized, there's no way to tell the actual char index
    so we need our tokenizer to emit `tokenizer.Token`

    todo: frozen class (maybe dataclass?)
    dataclasses will support slots in python 3.10
    and it comes with sortable and hashable traits for free

    todo: mimic as much as possible of this
    https://docs.python.org/3/library/re.html#match-objects
    # '__class__':         type
    # '__copy__':          method_descriptor
    # '__deepcopy__':      method_descriptor
    # '__delattr__':       wrapper_descriptor
    # '__dir__':           method_descriptor
    # '__doc__':           str
    '__eq__':            wrapper_descriptor
    # '__format__':        method_descriptor
    '__ge__':            wrapper_descriptor
    # '__getattribute__':  wrapper_descriptor
    '__getitem__':       wrapper_descriptor
    '__gt__':            wrapper_descriptor
    '__hash__':          wrapper_descriptor
    '__init__':          wrapper_descriptor
    # '__init_subclass__': builtin_function_or_method
    '__le__':            wrapper_descriptor
    '__lt__':            wrapper_descriptor
    '__ne__':            wrapper_descriptor
    '__new__':           builtin_function_or_method
    # '__reduce__':        method_descriptor
    # '__reduce_ex__':     method_descriptor
    '__repr__':          wrapper_descriptor
    # '__setattr__':       wrapper_descriptor
    # '__sizeof__':        method_descriptor
    '__str__':           wrapper_descriptor
    # '__subclasshook__':  builtin_function_or_method
    'end':               method_descriptor
    'endpos':            member_descriptor
    'expand':            method_descriptor
    'group':             method_descriptor
    'groupdict':         method_descriptor
    'groups':            method_descriptor
    'lastgroup':         getset_descriptor
    'lastindex':         getset_descriptor
    'pos':               member_descriptor
    're':                member_descriptor
    'regs':              getset_descriptor
    'span':              method_descriptor
    'start':             method_descriptor
    'string':            member_descriptor

    todo: subclass string
    https://stackoverflow.com/a/33272874

    :param start: index of start TOKEN (not char)
    :param end: index after end token
    :param match: string matched
    """

    __slots__ = ('regs', 'str')

    def __init__(self, start, end, match):
        self.regs: Tuple[Tuple[int, int]] = ((start, end),)  # mimic the re.Match object

        # re.Match references the original string to save space
        # but we might match a char iterator, which is ephemeral
        # and we can't gave a 1gb string lying around in memory to be used as a reference
        # so this is just going to be the match
        self.str: str = match

    def __getitem__(self, group_index: int) -> str:
        if group_index != 0:
            raise IndexError('no such group')
        return self.str

    def __repr__(self):
        return f'<Match object; span={self.regs[0]}, match={repr(self.str)}>'

    def __len__(self):
        return self.regs[0][1] - self.regs[0][0]

    def __str__(self) -> str:
        return self.str

    def group(self, group_index: int = 0) -> str:
        return self[group_index]

    def start(self, group_index: int = 0) -> int:
        if group_index != 0:
            raise IndexError('no such group')
        return self.regs[0][0]

    def end(self, group_index: int = 0) -> int:
        if group_index != 0:
            raise IndexError('no such group')
        return self.regs[0][1]

    def span(self, group_index: int = 0) -> Tuple[int, int]:
        if group_index != 0:
            raise IndexError('no such group')
        return self.regs[0]


class Sentinel:
    __slots__ = ()  # keeps size to 16 bytes, same as an object()


NULL = Sentinel()  # means that the value is undefined, ie. the node is not a leaf
NOTHING = Sentinel()  # means that the value is empty, ie. the node is a leaf with no value


class Node(dict):
    __slots__ = ('value', 'length', 'fail', 'match')

    # noinspection PyMissingConstructor
    def __init__(self):
        # todo: maybe use dataclass?
        self.value: Union[Sentinel, str] = NULL
        self.length: int = 0  # to determine how much of the buffer to release
        self.fail: Optional[Type['Node']] = None  # for aho-corasick failure jumps
        self.match: Optional[Type['Node']] = None  # to return matches in prefix on failure


class Trie(ABC):
    root: Node

    __slots__ = ('root',)

    @abstractmethod
    def __contains__(self, key):
        ...

    @abstractmethod
    def __len__(self):
        ...

    @abstractmethod
    def keys(self):
        ...

    @abstractmethod
    def values(self):
        ...

    @abstractmethod
    def __getitem__(self, key):
        ...

    @abstractmethod
    def pop(self, key=None):
        ...

    @abstractmethod
    def get(self, key, default=None):
        ...

    @abstractmethod
    def __set__(self, key, value):
        ...

    @abstractmethod
    def __delitem__(self, key):
        ...

    @abstractmethod
    def setdefault(self, key, value):
        ...

    @abstractmethod
    def finditer(self, text):
        ...

    @abstractmethod
    def findall(self, text):
        ...

    @abstractmethod
    def sub(self, text):
        ...

    @abstractmethod
    def items(self):
        ...
