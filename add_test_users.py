import sys
sys.path.insert(0, '/Users/darknet/dating-site')
from database import SessionLocal
from models import User
import bcrypt

def hash_pw(p):
    return bcrypt.hashpw(p.encode(), bcrypt.gensalt()).decode()

db = SessionLocal()

users = [
    User(email='aliya@mail.ru', username='aliya25', hashed_password=hash_pw('12345678'), name='Алия', age=25, gender='female', city='Алматы', bio='Люблю путешествия и кофе'),
    User(email='dana@mail.ru', username='dana22', hashed_password=hash_pw('12345678'), name='Дана', age=22, gender='female', city='Алматы', bio='Студентка, люблю музыку'),
    User(email='asel@mail.ru', username='asel28', hashed_password=hash_pw('12345678'), name='Асель', age=28, gender='female', city='Астана', bio='Врач, спортсменка'),
    User(email='arman@mail.ru', username='arman30', hashed_password=hash_pw('12345678'), name='Арман', age=30, gender='male', city='Алматы', bio='Программист, люблю горы'),
    User(email='dias@mail.ru', username='dias27', hashed_password=hash_pw('12345678'), name='Диас', age=27, gender='male', city='Астана', bio='Бизнесмен'),
]

for u in users:
    db.add(u)
db.commit()
db.close()
print('Done - добавлено 5 пользователей')
