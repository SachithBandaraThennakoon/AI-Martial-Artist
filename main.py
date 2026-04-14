from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from jose import JWTError, jwt
import json
import time

# core
from core.database import engine, Base, SessionLocal
from core.security import SECRET_KEY, ALGORITHM

# memory
from brain.memory.semantic_memory.target_angle import TargetAngle

# routes
from brain.action.api_routes.auth_routes import router as auth_router
from brain.action.api_routes.technique_routes import router as technique_router

# brain
from brain.consciousness.orchestrator import run_brain


# -----------------------------
# INIT APP
# -----------------------------
app = FastAPI(title="AI Martial Brain")

Base.metadata.create_all(bind=engine)


# -----------------------------
# CORS
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------
# ROUTERS
# -----------------------------
app.include_router(auth_router)
app.include_router(technique_router)


# -----------------------------
# AUTH
# -----------------------------
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -----------------------------
# ROOT
# -----------------------------
@app.get("/")
def root():
    return {"message": "AI Martial Brain Running 🧠"}


# -----------------------------
# PROTECTED TEST
# -----------------------------
@app.get("/protected")
def protected_route(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return {"message": f"Hello {payload.get('sub')}"}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


# -----------------------------
# 🧠 WEBSOCKET TRAINING PIPELINE
# -----------------------------
@app.websocket("/ws/train")
async def train(websocket: WebSocket):

    token = websocket.query_params.get("token")

    if not token:
        await websocket.close()
        return

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        print("✅ Connected:", email)
    except JWTError:
        await websocket.close()
        return

    await websocket.accept()

    db = SessionLocal()

    # 🧠 TEMPORAL MEMORY
    angle_history = []
    history_duration = 5  # seconds

    last_feedback_time = 0
    feedback_interval = 2

    try:
        while True:
            data = await websocket.receive_text()
            parsed = json.loads(data)

            step_id = parsed.get("step_id")
            live_angles = parsed.get("angles", {})

            current_time = time.time()

            # -----------------------------
            # STORE TEMPORAL MEMORY
            # -----------------------------
            angle_history.append({
                "time": current_time,
                "angles": live_angles
            })

            angle_history = [
                x for x in angle_history
                if current_time - x["time"] <= history_duration
            ]

            history_angles = [x["angles"] for x in angle_history]

            # -----------------------------
            # GET REQUIRED PARTS (MEMORY)
            # -----------------------------
            required_parts = db.query(TargetAngle).filter(
                TargetAngle.step_id == step_id
            ).all()

            # -----------------------------
            # 🧠 RUN FULL BRAIN
            # -----------------------------
            if current_time - last_feedback_time > feedback_interval:

                brain_output = run_brain(
                    required_parts,
                    live_angles,
                    history_angles
                )

                last_feedback_time = current_time
            else:
                brain_output = {
                    "analysis": [],
                    "feedback": [],
                    "summary": "..."
                }

            # -----------------------------
            # SIMPLE ACCURACY (FAST UI)
            # -----------------------------
            correct = sum(
                1 for part in required_parts
                if part.body_part in live_angles and
                part.min_angle <= live_angles[part.body_part] <= part.max_angle
            )

            total = len(required_parts)
            accuracy = int((correct / total) * 100) if total > 0 else 0

            # -----------------------------
            # SEND RESPONSE
            # -----------------------------
            await websocket.send_text(json.dumps({
                "accuracy": accuracy,
                "feedback": brain_output["feedback"],
                "summary": brain_output["summary"]
            }))

    except WebSocketDisconnect:
        print(f"{email} disconnected")

    finally:
        db.close()


# -----------------------------
# GET ANGLES
# -----------------------------
@app.get("/steps/{step_id}/angles")
def get_angles(step_id: int, db: Session = Depends(get_db)):
    angles = db.query(TargetAngle).filter(
        TargetAngle.step_id == step_id
    ).all()

    return [
        {
            "body_part": a.body_part,
            "min": a.min_angle,
            "max": a.max_angle
        }
        for a in angles
    ]