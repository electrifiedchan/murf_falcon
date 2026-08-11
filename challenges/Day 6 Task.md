# Day 6 – Make Outbound Calls

Yesterday your agent waited to be called over the browser. Today, it will be making outbound calls.

> IMPORTANT: You need a telephony service like Twilio to make outbound calls. If your Twilio free trial is exhausted, you can use Linphone to make outbound calls.

For Day 6, your objective is to:

- **Step 1: Find the outbound use case for your track.**
  - Track: Learning & Literacy
  - Call trigger: Daily practice call at a time the learner picked

- **Step 2: Integrate a Telephony Service.** 
  - Created a sip outbound trunk connecting to Linphone.

- **Step 3: Have your agent call you**, or a number you control, and complete the interaction.
  - Developed `run_outbound.py` script to dispatch an agent and dynamically command it to outbound dial via LiveKit Sip Trunks.

- **Step 4: Open the call properly.** 
  - Updated `agent.py` to intercept outbound dispatches and present the user with a mandatory Day 6 custom greeting that states who is calling, why, and how to opt out without waiting for user's voice first.

- **Step 5: Record a short video** of the phone ringing and the call playing out.
- **Step 6: Post the video on LinkedIn** 
- **Step 7: Submit your post link** on the submission form, along with your name and email.

## Advanced (Optional)

You only need the steps above to complete Day 6. These are for going the extra mile:

- **Outcome Handling**: Handle the outcomes inbound never has: no answer, busy, voicemail, and an immediate hang-up. Each needs a defined behaviour and a retry rule.

### You've finished Day 6 if:

- Your agent places a call and delivers something useful
- The opening states who is calling, why, and how to opt out
