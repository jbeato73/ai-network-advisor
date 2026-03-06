# AI Network Advisor (AIOps)

A diagnostic intelligence tool that bridges the gap between raw network telemetry and actionable recovery steps. This utility utilizes the **Google GenAI SDK** and the **Gemini 1.5 Flash** model to automate the first tier of infrastructure troubleshooting.

AIOps Reporting: Includes a specialized query engine that filters the inventory database for assets with active AI-generated recovery playbooks, enabling a "Diagnostics-First" maintenance workflow.

## 🤖 AIOps Capabilities

* **Automated Incident Analysis:** Evaluates device failure states and generates a 3-step recovery playbook.

* **SDK 2.0 Implementation:** Built using the modern `google-genai` client, ensuring low-latency communication 
and future-proofed API calls.

* **Context-Aware Recommendations:** Adjusts diagnostic steps based on hardware vendor (Cisco, Juniper, etc.) and specific error codes (e.g., Timeout vs. Authentication Failure).

## 🛠️ Setup & Execution

1. ## Install Dependencies:
   ```bash
      uv sync

2. ## Configure Environment:
   Add your Gemini API Key to a .env file:
   ```bash 
      GEMINI_API_KEY=your_actual_key_here

3. ## Run the Advisor:
   ```Bash
      uv run python ai_advisor.py

## 📋 Technical Stack: 

   LLM: Google Gemini 1.5 Flash
   
   SDK: google-genai (v2.0)
   
   Environment: UV & Python-Decouple

---

## 🏁 Final Execution Check:

   Run the command one last time to see the AI report: 
   
    ```bash
       uv run python ai_advisor.py
