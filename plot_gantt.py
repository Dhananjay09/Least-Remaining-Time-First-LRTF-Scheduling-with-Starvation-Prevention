# plot_gantt.py
import matplotlib.pyplot as plt
from scheduling import CollaborativeLRTF

def plot_gantt(timeline):
    fig, ax = plt.subplots(figsize=(10, 5))

    colors = {}
    y_labels = []
    for thread_id in range(len(timeline[0])):
        y_labels.append(f"Thread {thread_id}")

    for t, slots in enumerate(timeline):
        for thread_id, req in enumerate(slots):
            if req is None:
                continue
            if req not in colors:
                colors[req] = plt.cm.tab20(len(colors))
            ax.barh(thread_id, 1, left=t, color=colors[req], edgecolor="black")
            ax.text(t + 0.5, thread_id, req, ha='center', va='center', fontsize=8)

    ax.set_yticks(range(len(timeline[0])))
    ax.set_yticklabels(y_labels)
    ax.set_xlabel("Time Units")
    ax.set_title("Gantt Chart for Collaborative LRTF Scheduling")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # Example run
    sched = CollaborativeLRTF(threads=4, starvation_threshold=5)
    sched.add_request("A", arrival=0, total_pages=10)
    sched.add_request("B", arrival=1, total_pages=3)
    sched.add_request("C", arrival=2, total_pages=8)
    sched.add_request("D", arrival=4, total_pages=20)

    sched.run()
    timeline = sched.get_timeline()
    plot_gantt(timeline)
