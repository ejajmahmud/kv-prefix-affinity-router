"""Unit tests for kv-prefix-affinity-router."""
import unittest
from kv_prefix_affinity_router.router import KVPrefixAffinityRouter


class TestKVPrefixAffinityRouter(unittest.TestCase):
    def test_prefix_affinity_sticky(self):
        router = KVPrefixAffinityRouter()
        router.register_node("n1")
        router.register_node("n2")

        target = router.route("prefix_common")
        router.release(target)

        # Subsequent call with same prefix should route to same node
        target2 = router.route("prefix_common")
        self.assertEqual(target, target2)

    def test_fallback_least_loaded(self):
        router = KVPrefixAffinityRouter()
        router.register_node("n1", capacity=1)
        router.register_node("n2", capacity=5)

        _ = router.route("prefix_a")  # fills n1
        # n1 is full, next different prefix should go to n2
        target_b = router.route("prefix_b")
        self.assertEqual(target_b, "n2")
