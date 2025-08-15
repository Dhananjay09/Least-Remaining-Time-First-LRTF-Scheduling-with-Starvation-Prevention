from dataclasses import dataclass, field
from typing import List, Optional, Dict
import math

@dataclass
class Request:
    rid: str
    arrival: int
    total_pages: int
    remaining: int = field(init=False)
    waiting_time: int = 0
    completion: Optional[int] = None

    def __post_init__(self):
        self.remaining = self.total_pages


class CollaborativeLRTF:
    def __init__(self, threads: int, starvation_threshold: int = 5):
        self.threads = threads
        self.starvation_threshold = starvation_threshold
        self.time = 0
        self.requests: Dict[str, Request] = {}
        self.arrivals: Dict[int, List[str]] = {}
        self.timeline: List[List[Optional[str]]] = []

    def add_request(self, rid: str, arrival: int, total_pages: int):
        req = Request(rid, arrival, total_pages)
        self.requests[rid] = req
        self.arrivals.setdefault(arrival, []).append(rid)

    def _ready_requests(self):
        return [r for r in self.requests.values() if r.arrival <= self.time and r.remaining > 0]

    def run(self):
        while True:
            unfinished = [r for r in self.requests.values() if r.remaining > 0]
            if not unfinished:
                break

            # Add new arrivals in the queue
            for rid in self.arrivals.get(self.time, []):
                self.requests[rid].waiting_time = 0

            ready = self._ready_requests() # ready requests are requests that have arrived and have remaining pages
            if not ready:
                self.timeline.append([None] * self.threads)
                self.time += 1
                continue

            # Update waiting times
            for r in ready:
                r.waiting_time += 1

            # Sort by remaining time (LRTF priority)
            ready.sort(key=lambda r: r.remaining)

            tick_assignments: List[Optional[str]] = []

            # Step 1: Check for starving requests
            starving = [r for r in ready if r.waiting_time >= self.starvation_threshold]
            if starving:
                # Pick the most starving one (longest waiting time)
                starving.sort(key=lambda r: (-r.waiting_time, r.remaining))
                chosen = starving[0]
                # Give it as many threads as possible (but not more than pages left)
                threads_for_starving = min(self.threads, chosen.remaining)
                tick_assignments.extend([chosen.rid] * threads_for_starving)
                chosen.remaining -= threads_for_starving
                chosen.waiting_time = 0
                if chosen.remaining == 0:
                    chosen.completion = self.time + 1

                threads_left = self.threads - threads_for_starving
            else:
                threads_left = self.threads

            # Step 2: Allocate remaining threads to smallest remaining jobs
            for r in ready:
                if threads_left <= 0 or r.remaining == 0:
                    continue
                needed = min(r.remaining, threads_left)
                tick_assignments.extend([r.rid] * needed)
                r.remaining -= needed
                r.waiting_time = 0
                if r.remaining == 0:
                    r.completion = self.time + 1
                threads_left -= needed

            # Fill idle slots if any
            while len(tick_assignments) < self.threads:
                tick_assignments.append(None)

            self.timeline.append(tick_assignments)
            self.time += 1

    def gantt(self):
        print("Time | " + " | ".join(f"T{i}" for i in range(self.threads)))
        print("-" * (7 + 4 * self.threads))
        for t, slots in enumerate(self.timeline):
            row = f"{t:>4} | " + " | ".join(s if s else "." for s in slots)
            print(row)

    def stats(self):
        for r in sorted(self.requests.values(), key=lambda x: x.rid):
            turnaround = (r.completion - r.arrival) if r.completion else None
            print({
                "Request": r.rid,
                "arrival": r.arrival,
                "pages": r.total_pages,
                "completion": r.completion,
                "turnaround": turnaround
            })

    def get_timeline(self):
        """Return timeline for Gantt plotting."""
        return self.timeline


# ---------------- Example usage ----------------
if __name__ == "__main__":
    sched = CollaborativeLRTF(threads=4, starvation_threshold=5)
    sched.add_request("A", arrival=0, total_pages=100)
    sched.add_request("B", arrival=1, total_pages=30)
    sched.add_request("C", arrival=2, total_pages=8)
    sched.add_request("D", arrival=4, total_pages=20)  # big job

    sched.run()

    print("\n--- GANTT ---")
    sched.gantt()

    print("\n--- Stats ---")
    sched.stats()
