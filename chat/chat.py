from flask import Flask, request, jsonify, send_from_directory, session
import bcrypt, os, time, threading, uuid
import uuid

BANS_FILE = "bans.txt"
COOKIE_NAME = "chat_id"

banned_cookies = set()

app = Flask(__name__)
app.secret_key = os.urandom(32)

BASE = os.path.dirname(__file__)
MSG_DIR = os.path.join(BASE,"messages")
ROOM_DIR = os.path.join(MSG_DIR,"rooms")
USERS_FILE = os.path.join(BASE,"users.txt")
BANS_FILE = os.path.join(BASE,"bans.txt")

os.makedirs(ROOM_DIR, exist_ok=True)

RATE_LIMIT = 5
RATE_WINDOW = 5
MESSAGE_EXPIRY = 60*60*24*180  # 6 months

online_users = {}
muted_users = set()
msg_times = {}

def get_cookie_id():
    if COOKIE_NAME not in session:
        session[COOKIE_NAME] = uuid.uuid4().hex
    return session[COOKIE_NAME]
def get_room():
    return session.get("room", "public")

# ---------------- Users ----------------
def load_users():
    users = {}
    if os.path.exists(USERS_FILE):
        for l in open(USERS_FILE):
            if ":" not in l: continue
            u, h, r = l.strip().split(":")
            users[u] = {"hash":h.encode(), "role":r}
    return users

def save_user(username, password, role="user"):
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    with open(USERS_FILE,"a") as f:
        f.write(f"{username}:{hashed}:{role}\n")

# ---------------- Auth ----------------
def auth():
    get_cookie_id()

    if is_banned():
        session.clear()
        return None

    u = session.get("user")
    if u:
        online_users[u] = time.time()
    return u
def is_banned():
    if not os.path.exists(BANS_FILE):
        return False

    bans = open(BANS_FILE).read().splitlines()
    cid = session.get(COOKIE_NAME)
    ip = request.remote_addr

    return f"cookie:{cid}" in bans or f"ip:{ip}" in bans


# ---------------- Rate Limit ----------------
def ratelimit(user):
    now = time.time()
    lst = [t for t in msg_times.get(user, []) if now - t < RATE_WINDOW]
    lst.append(now)
    msg_times[user] = lst
    return len(lst) > RATE_LIMIT

# ---------------- Message Storage ----------------
def msg_path(room):
    return os.path.join(MSG_DIR, "public.txt" if room=="public" else f"{room}.txt")

def write_msg(path, user, msg):
    ts = time.strftime("[%H:%M:%S]", time.localtime())
    mid = uuid.uuid4().hex[:8]
    with open(path,"a") as f:
        f.write(f"{ts}|{user}: {msg}|{mid}\n")

def read_msgs(path):
    msgs = []
    if not os.path.exists(path): return msgs
    with open(path) as f:
        for l in f:
            try:
                ts_user_msg, mid = l.rsplit("|",1)
                ts, rest = ts_user_msg.split("|",1)
                msgs.append({"id":mid.strip(), "text":ts+"|"+rest})
            except:
                continue
    return msgs

# ---------------- Cleanup ----------------
def cleanup():
    while True:
        now = time.time()
        for f in os.listdir(MSG_DIR):
            p = os.path.join(MSG_DIR,f)
            if not os.path.isfile(p): continue
            kept=[]
            for l in open(p):
                kept.append(l)
            with open(p,"w") as fw:
                fw.writelines(kept)
        time.sleep(3600)

def prune():
    while True:
        now = time.time()
        for u in list(online_users):
            if now - online_users[u] > 15: del online_users[u]
        time.sleep(5)

threading.Thread(target=cleanup,daemon=True).start()
threading.Thread(target=prune,daemon=True).start()

# ---------------- Routes ----------------
@app.route("/")
def index(): return send_from_directory("templates","chat.html")

@app.route("/room/join", methods=["POST"])
def join_room():
    if is_banned(): return "banned", 403

    data = request.json
    room = data.get("room")

    if not room or not room.isalnum():
        return "bad room", 400

    path = msg_path(room)
    if not os.path.exists(path):
        return "no room", 404

    session["room"] = room
    return "ok"

@app.route("/register",methods=["POST"])
def register():
    d = request.json
    users = load_users()
    if d["username"] in users: return "exists",409
    save_user(d["username"], d["password"])
    return "ok"

@app.route("/login",methods=["POST"])
def login():
    if is_banned(): return jsonify(status="banned"),403
    d = request.json
    users = load_users()
    u = d.get("username")
    p = d.get("password")
    if u in users and bcrypt.checkpw(p.encode(), users[u]["hash"]):
        session["user"] = u
        return jsonify(status="ok")
    return jsonify(status="fail"),403

@app.route("/logout")
def logout():
    session.clear()
    return "ok"

@app.route("/whoami")
def whoami():
    u = session.get("user")
    if u:
        online_users[u] = time.time()
        return jsonify(user=u)
    return jsonify(user=None)

@app.route("/ping",methods=["POST"])
def ping():
    if auth(): return "ok"
    return "fail",403

@app.route("/send",methods=["POST"])
def send():
    u = auth()
    if not u: return "no",403
    if ratelimit(u): return "rate",429
    if is_banned(): return jsonify(status="banned"),403
    d = request.json
    room = d.get("room","public")
    p = msg_path(room)
    os.makedirs(MSG_DIR, exist_ok=True)
    write_msg(p,u,d["message"])
    return "ok"

@app.route("/messages")
def messages():
    room = request.args.get("room","public")
    return jsonify(read_msgs(msg_path(room)))

@app.route("/users")
def users():
    return jsonify(sorted(online_users.keys()))

@app.route("/room/new")
def new_room():
    r = uuid.uuid4().hex[:6]
    open(msg_path(r),"a").close()
    return r

@app.route("/command",methods=["POST"])
def command():
    data = request.json
    user = session.get("user")
    users = load_users()

    # Admin check for frontend
    if data.get("cmd") == "/checkrole":
        role = users.get(user, {}).get("role","user")
        return jsonify(role=role)

    # Only admins for other commands
    if not user or users.get(user,{}).get("role") != "admin":
        return "forbidden",403

    parts = data["cmd"].split(maxsplit=1)
    if not parts: return "bad",400
    cmd = parts[0]
    arg = parts[1] if len(parts)>1 else ""

    if cmd=="/mute": muted_users.add(arg)
    elif cmd=="/unmute": muted_users.discard(arg)
    elif cmd == "/ban":
        cid = session.get(COOKIE_NAME)
        with open(BANS_FILE, "a") as f:
            f.write(f"cookie:{cid}\n")
    elif cmd == "/ipban":
        ip = request.remote_addr
        with open(BANS_FILE, "a") as f:
            f.write(f"ip:{ip}\n")
    elif cmd == "/unban":
        cid = session.get(COOKIE_NAME)
        ip = request.remote_addr

        if not os.path.exists(BANS_FILE):
            return "ok"

        with open(BANS_FILE) as f:
            lines = f.readlines()

        with open(BANS_FILE, "w") as f:
            for l in lines:
                if l.strip() not in (f"cookie:{cid}", f"ip:{ip}"):
                    f.write(l)
    elif cmd=="/delete":
        # delete by message ID
        for file in [msg_path("public")]+[os.path.join(ROOM_DIR,f) for f in os.listdir(ROOM_DIR)]:
            if not os.path.exists(file): continue
            with open(file) as fr:
                lines = fr.readlines()
            with open(file,"w") as fw:
                for l in lines:
                    if not l.strip().endswith(arg):
                        fw.write(l)
    return "ok"

# ---------------- Start ----------------
if __name__=="__main__":
    app.run(host="0.0.0.0", port=5000)
