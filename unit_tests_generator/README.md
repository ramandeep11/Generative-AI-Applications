# Unit Test Generator

Complete workflow for automated unit test generation using [crewAI Flows](https://docs.crewai.com/en/guides/flows/first-flow). Clones repositories, generates unit tests, validates through build with feedback loop, and commits to a new branch.

## Flow Diagram

![Unit Test Generator Flow](https://github.com/ramandeep11/Generative-AI-Applications/blob/main/unit_tests_generator/Screenshot%202026-01-05%20at%209.28.01%E2%80%AFPM.png)

```
Start → Git Clone → Generate/Build/Validate → Checkout & Commit → End
                            ↑         ↓
                            └─(failed)┘
                    (retry with feedback, max 3 iterations)
```

## Installation

Ensure you have Python >=3.10 <3.14 installed.

```bash
pip install uv
crewai install
```

**Add your `OPENAI_API_KEY` to `.env`:**
```bash
OPENAI_API_KEY=your_api_key_here
```

## Running the Flow

Execute the flow:
```bash
crewai flow kickoff
```

Visualize the flow:
```bash
crewai flow plot
```

## Configuration

Edit `main.py` to customize the flow state:

```python
class State(BaseModel):
    git_url: str = "https://github.com/SuhasKamate/Business_Management_Project.git"
    git_branch: str = "master"
    service_class_name: str = "OrderServices.java"
    coding_language: str = "Java"
    build_tool: str = "Maven"
    max_iterations: int = 3
```

## How It Works

1. **Git Clone** - Clones repository and builds the project (once)
2. **Generate/Build/Validate** - Generates tests, writes files, and builds
   - Uses router to evaluate build success
   - On failure: retries with build error feedback
   - On success: proceeds to commit
3. **Checkout & Commit** - Creates new branch and commits successful tests

## Crews

- **GitCloneCrew**: Clones repository and builds project
- **GenerateUnitTestCrew**: Generates, writes, and validates unit tests (with retry logic)
- **GitCheckoutAndCommitCrew**: Commits successful tests
