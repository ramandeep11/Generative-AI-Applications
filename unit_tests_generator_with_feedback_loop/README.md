# Unit Test Generator with Feedback Loop

AI-powered unit test generator using [crewAI Flows](https://docs.crewai.com/en/guides/flows/first-flow) with iterative feedback loop to refine tests until they compile successfully.

## Flow Diagram

![Unit Test Generator with Feedback Loop](https://github.com/ramandeep11/Generative-AI-Applications/blob/main/unit_tests_generator_with_feedback_loop/Screenshot%202026-01-05%20at%209.26.58%E2%80%AFPM.png)

```
Start → Generate → Build → Checkout & Commit → End
↑                     ↓
└─────(retry)─────────┘
        (with feedback, max 3 times)
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
class UnitTestFlowState(BaseModel):
    clone_path: str = "./Business_Management_Project/"
    service_class_name: str = "OrderServices.java"
    coding_language: str = "Java"
    build_tool: str = "Maven"
    max_retry: int = 3
```

**Note**: Repository must be already cloned at `clone_path`.

## How It Works

1. **Generate Unit Test** - AI generates tests for the service class
2. **Build & Evaluate** - Builds project and captures errors
3. **Router Logic**:
   - Build succeeds → Commit to new branch
   - Build fails → Retry with error feedback
   - Max retries → Log failure and exit

## Crews

- **GenerateUnitTestCrew**: Generates and writes unit tests
- **BuildProjectCrew**: Validates tests through build
- **GitCheckoutAndCommitCrew**: Commits successful tests
