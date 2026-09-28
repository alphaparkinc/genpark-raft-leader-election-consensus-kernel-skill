from typing import List, Dict, Any, Optional

class RaftLeaderElectionKernel:
    FOLLOWER = "Follower"
    CANDIDATE = "Candidate"
    LEADER = "Leader"

    def __init__(self, node_id: str = "node-alpha", peers: Optional[List[str]] = None):
        self.node_id = node_id
        self.peers = peers or ["node-beta", "node-gamma", "node-delta", "node-epsilon"]
        self.current_term = 0
        self.voted_for: Optional[str] = None
        self.state = self.FOLLOWER
        self.votes_received = 0

    def start_election(self) -> Dict[str, Any]:
        self.state = self.CANDIDATE
        self.current_term += 1
        self.voted_for = self.node_id
        self.votes_received = 1
        total = len(self.peers) + 1
        return {
            "node_id": self.node_id,
            "term": self.current_term,
            "state": self.state,
            "votes_received": self.votes_received,
            "quorum_required": total // 2 + 1,
            "is_leader": False
        }

    def receive_vote_response(self, from_node: str, term: int, vote_granted: bool) -> Dict[str, Any]:
        if term > self.current_term:
            self.current_term = term
            self.state = self.FOLLOWER
            self.voted_for = None
            return {"node_id": self.node_id, "state": self.state, "stepped_down": True}
        if self.state == self.CANDIDATE and vote_granted and term == self.current_term:
            self.votes_received += 1
            if self.votes_received >= (len(self.peers) + 1) // 2 + 1:
                self.state = self.LEADER
        return {"node_id": self.node_id, "state": self.state, "term": self.current_term, "is_leader": self.state == self.LEADER}

    def benchmark_election(self) -> Dict[str, Any]:
        start = self.start_election()
        r1 = self.receive_vote_response("node-beta", self.current_term, True)
        r2 = self.receive_vote_response("node-gamma", self.current_term, True)
        return {"election_start": start, "vote_1": r1, "vote_2_final": r2}
