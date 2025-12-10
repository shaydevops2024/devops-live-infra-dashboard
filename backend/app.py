from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
import redis
import pika
import docker
from datetime import datetime

# ----------------------------------------------------
# FastAPI app + CORS
# ----------------------------------------------------
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

docker_client = docker.from_env()

# ----------------------------------------------------
# DATABASE CONNECTION FOR LOGS
# ----------------------------------------------------
def get_db_conn():
    return psycopg2.connect(
        dbname="example",
        user="example",
        password="example",
        host="db",
        port=5432
    )

def save_log(service, message):
    try:
        conn = get_db_conn()
        cur = conn.cursor()
        cur.execute(
            "CREATE TABLE IF NOT EXISTS service_logs ("
            "id SERIAL PRIMARY KEY, "
            "service VARCHAR(50), "
            "message TEXT, "
            "created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"
        )
        cur.execute(
            "INSERT INTO service_logs (service, message) VALUES (%s, %s)",
            (service, message)
        )
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print("Error saving log:", e)

# ----------------------------------------------------
# SERVICE CHECK FUNCTIONS
# ----------------------------------------------------
def check_db():
    try:
        conn = psycopg2.connect(
            dbname="example",
            user="example",
            password="example",
            host="db",
            port=5432,
            connect_timeout=2
        )
        conn.close()
        return True
    except:
        return False

def check_redis():
    try:
        r = redis.Redis(host="redis", port=6379)
        r.ping()
        return True
    except:
        return False

def check_rabbit():
    try:
        conn = pika.BlockingConnection(
            pika.ConnectionParameters(host="rabbit", blocked_connection_timeout=1)
        )
        conn.close()
        return True
    except:
        return False

# ----------------------------------------------------
# ROUTES
# ----------------------------------------------------
@app.get("/status")
def status():
    return {
        "db": check_db(),
        "redis": check_redis(),
        "rabbit": check_rabbit()
    }

@app.post("/stop/{service}")
def stop_service(service: str):
    try:
        container = docker_client.containers.get(service)
        container.stop()
        return {"success": True, "message": f"{service} stopped"}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.post("/start/{service}")
def start_service(service: str):
    try:
        container = docker_client.containers.get(service)
        container.start()
        return {"success": True, "message": f"{service} started"}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.post("/ping/{service}")
def ping_service(service: str):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        if service == "db":
            conn = psycopg2.connect(
                dbname="example",
                user="example",
                password="example",
                host="db",
                port=5432,
                connect_timeout=2
            )
            conn.close()
        elif service == "redis":
            r = redis.Redis(host="redis", port=6379)
            r.ping()
        elif service == "rabbit":
            conn = pika.BlockingConnection(
                pika.ConnectionParameters(host="rabbit", blocked_connection_timeout=1)
            )
            conn.close()
        else:
            raise ValueError("Unknown service")
        message = f"Ping OK at {now}"
    except Exception as e:
        message = f"Ping FAILED at {now} ({str(e)})"

    save_log(service, message)
    return {"success": True, "message": message}

@app.get("/logs/{service}")
def get_logs(service: str):
    try:
        conn = get_db_conn()
        cur = conn.cursor()
        cur.execute(
            "SELECT message, created_at FROM service_logs WHERE service=%s ORDER BY id ASC",
            (service,)
        )
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return [{"message": row[0], "created_at": row[1].strftime("%Y-%m-%d %H:%M:%S")} for row in rows]
    except Exception as e:
        return {"error": str(e)}
