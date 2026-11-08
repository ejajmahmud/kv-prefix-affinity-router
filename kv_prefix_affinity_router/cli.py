"""CLI for kv-prefix-affinity-router."""
import sys
import argparse
from .router import KVPrefixAffinityRouter


def main():
    parser = argparse.ArgumentParser(description="KV Prefix Affinity Router CLI")
    parser.add_argument("--demo", action="store_true", help="Run KV prefix affinity router demo")
    args = parser.parse_args()

    if args.demo:
        router = KVPrefixAffinityRouter()
        router.register_node("gpu-node-01")
        router.register_node("gpu-node-02")

        prefix = "SYSTEM: You are an autonomous coding assistant with tools [read, write, bash]"
        n1 = router.route(prefix)
        print(f"[+] Initial query with prefix routed to: {n1}")
        n2 = router.route(prefix)
        print(f"[+] Subsequent identical prefix query routed to: {n2} (Affinity cache hit!)")
    else:
        parser.print_help()
    sys.exit(0)


if __name__ == "__main__":
    main()
