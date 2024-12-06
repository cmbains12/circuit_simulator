# Circuit Simulator (in development)

A Python-based circuit simulation tool for analyzing and visualizing electrical circuits.

## Table of Contents

- [Features](#features)
- [Setup](#setup)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Setup

1. Ensure you have Python 3.6+ installed on your system.
2. Install virtualenv if you don't have it:
    ```bash
    pip install virtualenv
    ```

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/your_project_name.git
    ```
2. Navigate to the project directory:
    ```bash
    cd CircuitSimulator
    ```

## Getting Started

1. Ensure you have Python installed on your system.
2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Planned Features

- Simulate various electrical components like resistors, capacitors, and inductors.
- Visualize circuit diagrams.
- Perform AC/DC analysis.
- Export simulation results.

## Current Features

- Draw conductor segments and chain them together to form 'nets'
- Track component, node, and net ids
- Perform a merge function when linking two nets with a component and consistently apply the change of net arrangement to the components

## To-Do

- create method to select components or nodes and highlight them on the canvas
- click and drag function
- create undo/redo functions that operate on mesh/net changes as well as component/node creation 
(easy/medium)
- method to delete selected item and refactor remaining components appropriately into remaining 
meshes, nets, and branches
- create mesh class and integrate it into the canvas object id tracking similar to "nets" (easy)
- create a method to check for and identify complete loops (called "meshes") in the arrangement of 
components on the canvas (hard)

- create a method create new branches from the remnents of the original branch that was bisected 
by the creation of a mesh (think about it like identifiying the branches on a btex molecule) 
(medium)



- Reorganize and rename code to comply with standard network analysis terms and heirarchies 
(like treating the diagram and the component arrangements as seperate objects ('Netlist'))
- Create methods to verify Kirchoff's laws on nodes and meshes


## Usage

1. Run the main script to start the simulator:
    ```bash
    python main.py
    ```
2. Follow the on-screen instructions to create and simulate your circuit.