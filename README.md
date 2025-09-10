# Chain-of-Experts: When LLMs Meet Complex Operation Research Problems

## Overview

Chain-of-Experts is a novel framework that leverages Large Language Models (LLMs) to solve complex Operations Research (OR) problems by orchestrating multiple specialized AI experts in a collaborative manner. The system breaks down complex OR problems into manageable components and assigns them to different expert agents, each specializing in a specific aspect of the problem-solving process.

## Architecture

The framework consists of several key components working together:

### Core Components

1. **Conductor**: Acts as the central orchestrator that decides which expert to consult next based on the current state of problem-solving and available expert capabilities.

2. **Experts**: A collection of specialized AI agents, each focusing on a specific aspect:
   - **TerminologyInterpreter**: Interprets and explains domain-specific terminology
   - **ParameterExtractor**: Extracts key parameters and constraints from problem descriptions
   - **ModelingExpert**: Constructs mathematical optimization models (MIP/LP)
   - **ProgrammingExampleProvider**: Provides relevant code examples and patterns
   - **ProgrammingExpert**: Implements the optimization solution in Python code
   - **ModelingKnowledgeSupplementExpert**: Provides additional modeling knowledge and insights
   - **CodeReviewer**: Reviews and validates generated code for correctness

3. **CommentPool**: A communication system that manages comments and insights exchanged between experts, ensuring proper information flow.

4. **Reducer**: Synthesizes all expert contributions into a final, coherent solution.

5. **Evaluator**: Generates test cases and validates the correctness of generated solutions, providing feedback for reflection and improvement.

### Workflow

1. **Problem Input**: The system receives an OR problem description and code template
2. **Expert Collaboration**: The Conductor selects experts sequentially (up to `max_collaborate_nums`)
3. **Forward Pass**: Each selected expert contributes insights based on the problem and previous comments
4. **Solution Synthesis**: The Reducer combines all expert inputs to generate final code
5. **Testing & Reflection** (optional): The Evaluator tests the solution and provides feedback
6. **Backward Pass** (if reflection enabled): Experts refine their contributions based on test feedback
7. **Iteration**: Process repeats for up to `max_trials` iterations until convergence

## Data Storage and Results

### Input Data Structure
Problems are stored in the `dataset/` directory with the following structure:
```
dataset/
├── LPWP/                    # Linear Programming Word Problems dataset
│   ├── prob_0/
│   │   ├── description.txt  # Problem description
│   │   ├── code_example.py  # Code template
│   │   └── sample.json      # Test samples
│   └── prob_1/
│       └── ...
└── ComplexOR/               # Complex Operations Research problems
    └── ...
```

### Output and Logging
All results are stored in the `log/` directory (configurable via `--log_dir`):

```
log/
├── run_coe_LPWP_[timestamp]/    # Experiment-specific directory
│   ├── prob_0_original_answer.txt    # Raw LLM response
│   ├── prob_0_generated_code.py      # Extracted code
│   └── prob_0_test_log.txt           # Test execution results
└── LOG_FILE_GENERATED_HERE          # General log file
```

### Temporary Files
- `generated_code.py`: Contains the most recently generated solution code
- Various log files track execution progress and results

## Requirements

1. Clone the repository
```bash
git clone https://github.com/xzymustbexzy/Chain-of-Experts.git
```

2. Install the necessary dependencies provided in the requirements.txt.
```bash
pip install -r requirements.txt
```

## Run the experiments
Firstly, set the environment variable `OPENAI_API_KEY`

```bash
export OPENAI_API_KEY=[Your API key here]
```

Run the experimental script

```bash
python run_exp.py --dataset LPWP --problem "prob_.*" --algorithm coe
```

## Key Files and Modules

### Main Entry Points
- `main.py`: Contains the core `chain_of_experts()` function that orchestrates the entire process
- `run_exp.py`: Command-line interface for running experiments on datasets

### Expert System Components
- `conductor.py`: Implements the Conductor class that selects next experts
- `experts/`: Directory containing all expert implementations
  - `base_expert.py`: Base class for all experts
  - Individual expert files (modeling_expert.py, programming_expert.py, etc.)
- `reducer.py`: Implements the Reducer that synthesizes final solutions
- `evaluator.py`: Handles test case generation and solution validation

### Utilities and Data Management
- `comment_pool.py`: Manages communication between experts
- `comment.py`: Defines the Comment data structure
- `utils.py`: Helper functions for code extraction and problem loading
- `result.py`: Defines result enumeration for test outcomes

### Baseline Algorithms
- `baseline/standard.py`: Standard prompting approach
- `baseline/chain_of_thought.py`: Chain-of-thought reasoning
- `baseline/progressive_hint.py`: Progressive hint prompting

## Usage
- `--dataset`: Specifies the dataset name. Currently supports "LPWP" or "ComplexOR". This argument is required.

- `--problem`: Specifies the name of the problem to solve. This argument is required.

- `--algorithm`: Specifies the algorithm to use. Supported algorithms include:
  - `coe` or `chain_of_experts`: The main Chain-of-Experts approach
  - `standard`: Basic prompting without expert collaboration
  - `cot` or `chain_of_thought`: Chain-of-thought reasoning
  - `php` or `progressive_hint`: Progressive hint prompting
  - `ssp` or `solo_performance_prompting`: Solo performance prompting
  - `reflexion`: Reflexion-based approach

- `--enable_reflection`: Adds reflection capabilities to the selected algorithm. This is optional and is disabled by default.
- `--log_dir`: Specifies the directory where logs will be stored. The default is 'log'.
- `--model`: Specifies the base large language model to use. The default is 'gpt-3.5-turbo'.
- `--max_collaborate_nums`: Sets the maximum number of collaborations allowed. The default value is 3.
- `--max_trials`: Sets the maximum number of forward-backward trials allowed. The default value is 3.

### Customizing Expert Instructions
Each expert in the `experts/` directory has predefined prompts that guide their behavior. To modify the instructions for a specific expert:

1. Locate the expert's file in the `experts/` directory (e.g., `modeling_expert.py`).
2. Edit the `ROLE_DESCRIPTION`, `FORWARD_TASK`, or `BACKWARD_TASK` class variables to update the prompts.
3. Restart the system to apply changes.

For example, to change the ModelingExpert's forward task, modify the `FORWARD_TASK` string in `experts/modeling_expert.py`.

### Using Your Own Datasets
To integrate custom datasets:

1. Create a new directory under `dataset/` (e.g., `dataset/MyDataset/`).
2. For each problem, create a subdirectory (e.g., `dataset/MyDataset/prob_0/`).
3. In each problem directory, include:
   - `description.txt`: A text file containing the problem description.
   - `code_example.py`: A Python file with a code template (can be empty or minimal).
   - `sample.json`: A JSON file with test samples, structured as an array of objects with input/output pairs.
4. Update the `--dataset` argument to point to your new dataset name (e.g., `--dataset MyDataset`).
5. Ensure the problem names match the regex pattern in `--problem` (e.g., `--problem "prob_.*"` for all problems starting with "prob_").

Example `sample.json` structure:
```json
[
  {
    "input": {"param1": 10, "param2": 20},
    "output": {"result": 30}
  }
]
```

## Dataset
The LPWP dataset is uploaded in this repo.

Please note that the ComplexOR dataset is still in the review stage, and we have uploaded a raw version of the ComplexOR dataset. The formal 37 datasets mentioned in the paper will be released soon.

## Citation
```
@inproceedings{
xiao2024chainofexperts,
title={Chain-of-Experts: When {LLM}s Meet Complex Operations Research Problems},
author={Ziyang Xiao and Dongxiang Zhang and Yangjun Wu and Lilin Xu and Yuan Jessica Wang and Xiongwei Han and Xiaojin Fu and Tao Zhong and Jia Zeng and Mingli Song and Gang Chen},
booktitle={The Twelfth International Conference on Learning Representations},
year={2024},
url={https://openreview.net/forum?id=HobyL1B9CZ}
}
```
