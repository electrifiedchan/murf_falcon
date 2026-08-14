# Day 9 – Hand Off to a Specialist Agent

Today we demonstrated advanced multi-agent architecture using the LiveKit SDK, transitioning from a single monolithic AI to a system where specialized agents take over specific domains.

For Day 9, the objective was to:

- **Step 1: Choose a specialist.**
  - Added a **Maths Practice Specialist** for the Learning & Literacy track.
- **Step 2: Create the specialist as a separate agent.**
  - Created `MathsSpecialistAgent` in Python, powered by a distinct voice (`Samar`) so the transition is obvious to the user.
- **Step 3: Add a handoff tool to the main agent.**
  - Defined the `transfer_to_maths_specialist` `@function_tool` inside our primary `Assistant` (Shiksha AI).
- **Step 4: Pass the conversation context.**
  - Carried over the `chat_ctx` from the main agent to the specialist so the history remains intact.
- **Step 5: Make the handoff clear to the user.**
  - The main agent verbally announces: "I will transfer you to our Maths Practice Specialist now. Hold on a moment please."
- **Bonus Step: UI Telemetry for Handoff.**
  - Implemented real-time `DataChannel` payloads (`tool_results`) so the frontend explicitly renders a visual "Transferring to Maths Specialist..." toast while the audio swap occurs.

### You've finished Day 9 if:

- The agent properly identifies requests for "math", "numbers", or "arithmetic".
- The UI triggers the handoff loading screen.
- A new voice answers and contextually continues the math topic with the learner.
