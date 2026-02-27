import sys
sys.path.insert(0, '/Users/darknet/dating-site')
from database import SessionLocal
from models import Like

db = SessionLocal()

# Алия, Дана, Асель лайкают Макса (id=1)
likes = [
    Like(liker_id=2, liked_id=1),
    Like(liker_id=3, liked_id=1),
    Like(liker_id=4, liked_id=1),
]

for l in likes:
    db.add(l)
db.commit()
db.close()
print('Done - взаимные лайки добавлены')
