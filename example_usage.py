from client import RaftLeaderElectionKernel

def run_example():
    print("=== GenPark Raft Leader Election Example ===")
    raft = RaftLeaderElectionKernel(node_id="worker-01", peers=["worker-02", "worker-03"])
    print("Election Start:", raft.start_election())
    vote = raft.receive_vote_response("worker-02", 1, True)
    print("Leader Confirmed:", vote["is_leader"])

if __name__ == "__main__":
    run_example()
