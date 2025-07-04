# Orchestrator Worker

A parallel workflow execution framework built with LangGraph for generating structured reports using LLMs.

## Overview

This project demonstrates a parallel task orchestration pattern using LangGraph to generate reports on arbitrary topics. The system breaks down the report generation task into sections that can be processed independently by worker nodes, then synthesizes the final output.

## Architecture

The system consists of several key components:

- **Orchestrator**: Plans the report structure and divides it into sections
- **Workers**: Process individual sections in parallel 
- **Synthesizer**: Combines all processed sections into a cohesive final report

## Core Components

### State Models

- `State`: Tracks the overall workflow state
  - `topic`: The report subject
  - `sections`: List of planned report sections
  - `completed_sections`: Results from all workers
  - `final_report`: The synthesized output

- `WorkerState`: Represents the state for individual worker processes
  - `section`: The specific section being processed
  - `completed_sections`: Output accumulator

- `Section`: Defines the schema for report sections
  - `name`: Section title
  - `description`: Brief overview of section content

### Node Functions

- `orchestrator()`: Generates a structured plan with sections
- `llm_call()`: Processes individual report sections
- `synthesizer()`: Combines all section outputs into a final report
- `assign_workers()`: Creates parallel tasks using the `Send()` API

## Workflow

1. The workflow begins with a topic input
2. The orchestrator uses an LLM to create a structured plan
3. Workers process each section in parallel
4. The synthesizer combines all outputs
5. The final report is returned

## LLM Integration

The project uses OpenAI's GPT-4o-mini model (via LangChain) for:
- Generating the report structure
- Processing individual sections
- Producing coherent content

## Usage

```python
# Import the workflow
from app import orchestrator_worker

# Generate a report on any topic
result = orchestrator_worker.invoke({"topic": "Create a report on LLM scaling laws"})

# Access the final report
print(result["final_report"])
```

## Visualization

The workflow graph can be visualized by uncommenting the `display_graph(orchestrator_worker)` line in app.py.
