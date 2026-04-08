from fastapi import FastAPI
from env.env import EmailEnv
import uvicorn

app = FastAPI()
env = EmailEnv()
from fastapi.responses import HTMLResponse

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
    <head>
        <title>Email Env Demo</title>
    </head>
    <body style="font-family: Arial; padding: 20px;">
        <h1>📧 Email Environment (OpenEnv)</h1>
        <p>This simulates email classification by an AI agent.</p>

        <h3>Try Demo:</h3>
        <button onclick="fetchEmail()">Get Email</button>

        <pre id="output"></pre>

        <script>
        async function fetchEmail() {
            const res = await fetch('/reset');
            const data = await res.json();
            document.getElementById('output').innerText = JSON.stringify(data, null, 2);
        }
        </script>
    </body>
    </html>
    """
@app.get("/reset")
def reset():
    obs = env.reset()
    return obs.dict()

@app.post("/step")
def step(action: dict):
    obs, reward, done, info = env.step(action)
    return {
        "observation": obs.dict(),
        "reward": reward,
        "done": done,
        "info": info
    }
@app.get("/state")
def get_state():
    return env.state().dict()
# ✅ THIS IS WHAT VALIDATOR WANTS
def main():
    uvicorn.run(app, host="0.0.0.0", port=7860)

# ✅ REQUIRED for execution
if __name__ == "__main__":
    main()