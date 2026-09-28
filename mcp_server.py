import sys, json
from client import RaftLeaderElectionKernel

raft = RaftLeaderElectionKernel()

def handle_jsonrpc(line):
    global raft
    try:
        req = json.loads(line)
        req_id = req.get("id")
        method = req.get("method")
        if method == "initialize":
            return {"jsonrpc": "2.0", "id": req_id, "result": {"protocolVersion": "2024-11-05", "serverInfo": {"name": "genpark-raft-leader-election-consensus-kernel-skill", "version": "1.0.0"}, "capabilities": {"tools": {}}}}
        elif method == "tools/list":
            return {"jsonrpc": "2.0", "id": req_id, "result": {"tools": [
                {"name": "start_election", "description": "Trigger Raft election.", "inputSchema": {"type": "object", "properties": {}}},
                {"name": "process_vote", "description": "Process peer vote response.", "inputSchema": {"type": "object", "properties": {"from_node": {"type": "string"}, "term": {"type": "integer"}, "vote_granted": {"type": "boolean"}}, "required": ["from_node", "term", "vote_granted"]}},
                {"name": "benchmark_election", "description": "Run Raft benchmark election.", "inputSchema": {"type": "object", "properties": {}}}
            ]}}
        elif method == "tools/call":
            params = req.get("params", {})
            tool = params.get("name")
            args = params.get("arguments", {})
            if tool == "start_election":
                res = raft.start_election()
            elif tool == "process_vote":
                res = raft.receive_vote_response(args.get("from_node"), args.get("term"), args.get("vote_granted"))
            elif tool == "benchmark_election":
                res = raft.benchmark_election()
            else:
                return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        return {"jsonrpc": "2.0", "id": req_id, "result": {}}
    except Exception as e:
        return {"jsonrpc": "2.0", "id": None, "error": {"code": -32603, "message": str(e)}}

def main():
    for line in sys.stdin:
        if line.strip():
            print(json.dumps(handle_jsonrpc(line.strip())), flush=True)

if __name__ == "__main__":
    main()
