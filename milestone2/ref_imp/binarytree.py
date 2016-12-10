from rbtree.binarynode import BinaryNode
from rbtree.binarynoderef import BinaryNodeRef
from rbtree.valueref import ValueRef

class BinaryTree(object):
    "Immutable Binary Tree class. Constructs new tree on changes"

    def __init__(self, storage):
        self._storage = storage
        self._refresh_tree_ref()

    def commit(self):
        "changes are final only when committed"
        # triggers BinaryNodeRef.store
        self._tree_ref.store(self._storage)
        # make sure address of new tree is stored
        self._storage.commit_root_address(self._tree_ref.address)

    def _refresh_tree_ref(self):
        "get reference to new tree if it has changed"
        self._tree_ref = BinaryNodeRef(
            address=self._storage.get_root_address())

    def get(self, key):
        "get value for a key"
        # your code here
        # if tree is not locked by another writer
        # refresh the references and get new tree if needed
        if not self._storage.locked:
            self._refresh_tree_ref()
        # get the top level node
        node = self._follow(self._tree_ref)
        # traverse until you find appropriate node
        while node is not None:
            if key < node.key:
                node = self._follow(node.left_ref)
            elif key < node.key:
                node = self._follow(node.right_ref)
            else:
                return self._follow(node.value_ref)
        raise KeyError

    def set(self, key, value):
        "set a new value in the tree. will cause a new tree"
        # try to lock the tree. If we succeed make sure
        # we dont lose updates from any other process
        if self._storage.lock():
            self._refresh_tree_ref()
        # get current top-level node and make a value-ref
        node = self._follow(self._tree_ref)
        value_ref = ValueRef(value)
        # insert and get new tree ref
        self._tree_ref = self._insert(node, key, value_ref)

    def _insert(self, node, key, value_ref):
        "insert a new node creating a new path from root"
        # create a tree ifnthere was none so far
        if node is None:
            new_node = BinaryNode(
                BinaryNodeRef(), key, value_ref, BinaryNodeRef())
        elif key < node.key:
            new_node = BinaryNode.from_node(
                node,
                left_ref=self._insert(
                    self._follow(node.left_ref), key, value_ref))
        elif key > node.key:
            new_node = BinaryNode.from_node(
                node,
                right_ref=self._insert(
                    self._follow(node.right_ref), key, value_ref))
        else:  # create a new node to represent this data
            new_node = BinaryNode.from_node(node, value_ref=value_ref)
        return BinaryNodeRef(referent=new_node)

    def delete(self, key):
        "delete node with key, creating new tree and path"
        if self._storage.lock():
            self._refresh_tree_ref()
        node = self._follow(self._tree_ref)
        self._tree_ref = self._delete(node, key)

    def _delete(self, node, key):
        "underlying delete implementation"
        if node is None:
            raise KeyError
        elif key < node.key:
            new_node = BinaryNode.from_node(
                node,
                left_ref=self._delete(
                    self._follow(node.left_ref), key))
        elif key > node.key:
            new_node = BinaryNode.from_node(
                node,
                right_ref=self._delete(
                    self._follow(node.right_ref), key))
        else:
            left = self._follow(node.left_ref)
            right = self._follow(node.right_ref)
            if left and right:
                replacement = self._find_max(left)
                left_ref = self._delete(
                    self._follow(node.left_ref), replacement.key)
                new_node = BinaryNode(
                    left_ref,
                    replacement.key,
                    replacement.value_ref,
                    node.right_ref,
                )
            elif left:
                return node.left_ref
            else:
                return node.right_ref
        return BinaryNodeRef(referent=new_node)

    def _follow(self, ref):
        "get a node from a reference"
        # calls BinaryNodeRef.get
        return ref.get(self._storage)

    def _find_max(self, node):
        while True:
            next_node = self._follow(node.right_ref)
            if next_node is None:
                return node
            node = next_node