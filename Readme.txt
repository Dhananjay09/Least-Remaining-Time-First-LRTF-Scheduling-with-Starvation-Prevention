# Least Remaining Time First (LRTF) Scheduling with Starvation Prevention

This project implements a **Least Remaining Time First (LRTF)** scheduling algorithm for handling multiple PDF page processing requests using multiple threads.  
It ensures:
- **Collaborative processing**: Multiple threads can work on a single request at the same time.
- **Starvation prevention**: If a request has been waiting too long, the scheduler assigns extra threads to it.
- **Gantt chart visualization**: The execution timeline is plotted for better understanding.

---

## Project Structure

project/
│
├── scheduler.py # Core scheduling logic
├── plot_gantt.py # Reads schedule output & plots Gantt chart
├── requirements.txt # Python dependencies
└── README.md # Documentation

---

## Requirements

Python **3.7+**  
Install dependencies:
```bash
To install the requirements
    pip install -r requirements.txt
To run scheduler 
    python scheduler.py
To plot the output in the graph
    python plot_gantt.py