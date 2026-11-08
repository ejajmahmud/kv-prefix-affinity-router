"""Core KV Prefix Affinity Router implementation."""
import hashlib
from typing import Dict, List, Optional, Any


class InferenceNode:
    def __init__(self, node_id: str, capacity: int = 100):
        self.node_id = node_id
        self.capacity = capacity
        self.active_requests = 0
        self.cached_prefixes: set = set()


class KVPrefixAffinityRouter:
    def __init__(self):
        self.nodes: Dict[str, InferenceNode] = {}

    def register_node(self, node_id: str, capacity: int = 100):
        self.nodes[node_id] = InferenceNode(node_id, capacity)

    def compute_prefix_hash(self, prompt_prefix: str) -> str:
        return hashlib.sha256(prompt_prefix.strip().encode("utf-8")).hexdigest()[:16]

    def route(self, prompt_prefix: str) -> str:
        if not self.nodes:
            raise RuntimeError("No inference nodes available")

        p_hash = self.compute_prefix_hash(prompt_prefix)

        # 1. Look for node holding warm cache with available capacity
        warm_nodes = [
            n for n in self.nodes.values()
            if p_hash in n.cached_prefixes and n.active_requests < n.capacity
        ]
        if warm_nodes:
            chosen = min(warm_nodes, key=lambda n: n.active_requests)
            chosen.active_requests += 1
            return chosen.node_id

        # 2. Fall back to least loaded node and seed cache
        available = [n for n in self.nodes.values() if n.active_requests < n.capacity]
        if not available:
            # Overloaded: pick lowest request count
            chosen = min(self.nodes.values(), key=lambda n: n.active_requests)
        else:
            chosen = min(available, key=lambda n: n.active_requests)

        chosen.cached_prefixes.add(p_hash)
        chosen.active_requests += 1
        return chosen.node_id

    def release(self, node_id: str):
        if node_id in self.nodes:
            self.nodes[node_id].active_requests = max(0, self.nodes[node_id].active_requests - 1)
