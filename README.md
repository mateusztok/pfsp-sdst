# PFSP-SDST Optimizer

A high-performance solver for the **Permutation Flow Shop Problem with Sequence-Dependent Setup Times (PFSP-SDST)**. 

This project features a two-layer architecture: a blazing-fast C++ algorithmic engine for complex combinatorial optimization, and a modern, dark-mode Python GUI for real-time visualization and parameter management.

## Architecture

The system is divided into two decoupled layers communicating via standard output streams (IPC):
* **Low-Layer (C++):** A highly optimized computational engine implementing scheduling heuristics and metaheuristics. It evaluates makespan (Cmax) and emits structured execution frames (`SLOT;...`).
* **High-Layer (Python):** A responsive graphical user interface built with `customtkinter`. It spawns the C++ solver as a subprocess, strictly validates input data sets, and renders interactive Gantt charts on the fly using `matplotlib`.

## Key Features

* **Advanced Algorithms:** 
  * **NEH Heuristic:** Fast, constructive algorithm for establishing a strong initial job sequence.
  * **Simulated Annealing (SA):** Powerful metaheuristic for deep optimization.
* **Dynamic GUI:** Real-time logging, live updating of the best sequence, and interactive Cmax tracking.
* **Gantt Chart Visualization:** Automated, color-coded scheduling visualization including setup times, job IDs, and machine timelines.
* **Strict Data Validation:** Comprehensive dataset parser that catches matrix dimension mismatches and syntax errors before the solver runs.
* **Configurable Parameters:** Easily adjust SA parameters (Iterations, Initial Temperature, Cooling Factor) directly from the UI..

## Tech Stack

* **Backend:** C++17 (Standard Library, Chrono, Random)
* **Frontend:** Python 3, CustomTkinter, Tkinter
* **Visualization:** Matplotlib
* **Integration:** Subprocess routing, custom stdout protocol

## Build & Run

```bash
# 1. Compile the C++ backend engine
cd low_layer
mkdir build && cd build
cmake ..
cmake --build .

# 2. Install dependencies
pip install customtkinter matplotlib

# 3. Launch the Python GUI
python high_layer/src/app_gui.py
