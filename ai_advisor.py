import sys
from google import genai
from decouple import config


def make_client():
    try:
        api_key = config("GEMINI_API_KEY")
        return genai.Client(api_key=api_key)
    except Exception as e:
        print(f"🚨 Configuration Error: {e}")
        sys.exit(1)


client = make_client()


def get_ai_advice(device_name, model_type, status):
    prompt = (
        f"Analyze failure for {device_name} ({model_type}). "
        f"Status: {status}. "
        "Provide 3 technical troubleshooting steps."
    )

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash", contents=prompt
        )
        return response.text
    except Exception as e:
        return f"🚨 AI Analysis Failed: {str(e)}"


def main():
    device = {
        "name": "LON-BDR-02",
        "model": "Juniper MX",
        "status": "OFFLINE (Timeout)",
    }
    print(f"🤖 AI Advisor is analyzing {device['name']}...")
    print(get_ai_advice(device["name"], device["model"], device["status"]))


if __name__ == "__main__":
    main()
