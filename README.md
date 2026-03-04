# AI Network Advisor (AIOps)

A diagnostic intelligence tool that bridges the gap between raw network telemetry and actionable recovery steps. This utility utilizes the **Google GenAI SDK** and the **Gemini 1.5 Flash** model to automate the first tier of infrastructure troubleshooting.

## 🤖 AIOps Capabilities

* **Automated Incident Analysis:** Evaluates device failure states and generates a 3-step recovery playbook.

* **SDK 2.0 Implementation:** Built using the modern `google-genai` client, ensuring low-latency communication 
and future-proofed API calls.

* **Context-Aware Recommendations:** Adjusts diagnostic steps based on hardware vendor (Cisco, Juniper, etc.) and specific error codes (e.g., Timeout vs. Authentication Failure).



## 🛠️ Setup & Execution

1. **Install Dependencies:**
   ```bash
   uv sync