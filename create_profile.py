html = open('/Users/darknet/dating-site/templates/profile.html', 'w', encoding='utf-8')
html.write("""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Профиль — Zhanym</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:Arial,sans-serif;background:#f5f5f5;min-height:100vh}
.header{background:white;padding:15px 20px;display:flex;justify-content:space-between;align-items:center;box-shadow:0 2px 10px rgba(0,0,0,.1)}
.logo{font-size:24px;font-weight:bold;color:#ff6b6b}
.nav a{margin-left:15px;text-decoration:none;color:#666;font-size:14px}
.nav a:hover{color:#ff6b6b}
.container{max-width:500px;margin:30px auto;padding:0 20px}
.card{background:white;border-radius:20px;padding:30px;box-shadow:0 5px 20px rgba(0,0,0,.1);margin-bottom:20px}
.avatar{width:120px;height:120px;border-radius:50%;background:linear-gradient(135deg,#ff6b6b,#fd79a8);display:flex;align-items:center;justify-content:center;font-size:50px;margin:0 auto 20px;cursor:pointer;position:relative;overflow:hidden}
.avatar img{width:100%;height:100%;object-fit:cover}
.avatar-edit{position:absolute;bottom:0;width:100%;background:rgba(0,0,0,.5);color:white;text-align:center;font-size:12px;padding:5px}
.name{text-align:center;font-size:24px;font-weight:bold;color:#333;margin-bottom:5px}
.city{text-align:center;color:#aaa;font-size:14px;margin-bottom:20px}
.group{margin-bottom:15px}
label{display:block;font-size:13px;color:#666;margin-bottom:5px;font-weight:bold}
input,select,textarea{width:100%;padding:12px 15px;border:2px solid #eee;border-radius:12px;font-size:15px;outline:none;transition:.3s}
input:focus,select:focus,textarea:focus{border-color:#ff6b6b}
textarea{height:100px;resize:none}
.btn{width:100%;padding:15px;background:linear-gradient(135deg,#ff6b6b,#fd79a8);color:#fff;border:none;border-radius:50px;font-size:18px;font-weight:bold;cursor:pointer;margin-top:10px}
.btn:hover{opacity:.9}
.btn-logout{width:100%;padding:12px;background:#f5f5f5;color:#666;border:none;border-radius:50px;font-size:16px;cursor:pointer;margin-top:10px}
.success{background:#e0ffe0;color:#44aa44;padding:10px 15px;border-radius:10px;margin-bottom:15px;font-size:14px;display:none}
.stats{display:flex;justify-content:space-around;padding:15px 0;border-top:1px solid #eee;margin-top:15px}
.stat{text-align:center}
.stat h3{font-size:22px;color:#ff6b6b;font-weight:bold}
.stat p{font-size:12px;color:#aaa}
</style>
</head>
<body>
<div class="header">
  <div class="logo">🌹 Zhanym</div>
  <div class="nav">
    <a href="/dashboard">Лента</a>
    <a href="/profile">Профиль</a>
    <a href="#" onclick="logout()">Выйти</a>
  </div>
</div>
<div class="container">
  <div class="card">
    <div class="avatar" id="avatarDiv" onclick="document.getElementById('photoInput').click()">
      <span id="avatarEmoji">👤</span>
      <div class="avatar-edit">Изменить фото</div>
    </div>
    <input type="file" id="photoInput" accept="image/*" style="display:none" onchange="uploadPhoto(this)">
    <div class="name" id="profileName">Загрузка...</div>
    <div class="city" id="profileCity"></div>
    <div class="stats">
      <div class="stat"><h3 id="likesCount">0</h3><p>Лайков</p></div>
      <div class="stat"><h3 id="matchesCount">0</h3><p>Матчей</p></div>
    </div>
  </div>
  <div class="card">
    <div class="success" id="success">Профиль обновлён!</div>
    <div class="group"><label>Имя</label><input type="text" id="name" placeholder="Твоё имя"></div>
    <div class="group"><label>Возраст</label><input type="number" id="age" placeholder="25" min="18" max="99"></div>
    <div class="group"><label>Город</label><input type="text" id="city" placeholder="Алматы"></div>
    <div class="group"><label>О себе</label><textarea id="bio" placeholder="Расскажи о себе..."></textarea></div>
    <div class="group">
      <label>Пол</label>
      <select id="gender">
        <option value="male">Мужской</option>
        <option value="female">Женский</option>
      </select>
    </div>
    <button class="btn" onclick="saveProfile()">Сохранить</button>
    <button class="btn-logout" onclick="logout()">Выйти из аккаунта</button>
  </div>
</div>
<script>
const token = localStorage.getItem('token');
if(!token) window.location.href = '/login';

async function loadProfile() {
  try {
    const res = await fetch('/users/me', {headers:{'Authorization':'Bearer '+token}});
    if(res.status===401){ window.location.href='/login'; return; }
    const user = await res.json();
    document.getElementById('profileName').textContent = user.name + ', ' + user.age;
    document.getElementById('profileCity').textContent = user.city;
    document.getElementById('name').value = user.name || '';
    document.getElementById('age').value = user.age || '';
    document.getElementById('city').value = user.city || '';
    document.getElementById('bio').value = user.bio || '';
    document.getElementById('gender').value = user.gender || 'male';
    document.getElementById('avatarEmoji').textContent = user.gender === 'female' ? '👩' : '👨';
    if(user.photo && user.photo !== 'default.jpg'){
      document.getElementById('avatarDiv').innerHTML = '<img src="/static/uploads/'+user.photo+'" alt="фото"><div class="avatar-edit">Изменить фото</div>';
    }
  } catch(e){ console.log(e); }
}

async function saveProfile() {
  const name = document.getElementById('name').value;
  const age = document.getElementById('age').value;
  const city = document.getElementById('city').value;
  const bio = document.getElementById('bio').value;
  try {
    const res = await fetch('/users/me?name='+encodeURIComponent(name)+'&age='+age+'&city='+encodeURIComponent(city)+'&bio='+encodeURIComponent(bio), {
      method:'PUT', headers:{'Authorization':'Bearer '+token}
    });
    if(res.ok){
      const el = document.getElementById('success');
      el.style.display = 'block';
      setTimeout(()=>el.style.display='none', 3000);
      loadProfile();
    }
  } catch(e){ console.log(e); }
}

async function uploadPhoto(input) {
  const file = input.files[0];
  if(!file) return;
  const formData = new FormData();
  formData.append('file', file);
  try {
    const res = await fetch('/users/me/photo', {
      method:'POST',
      headers:{'Authorization':'Bearer '+token},
      body: formData
    });
    if(res.ok){ loadProfile(); }
  } catch(e){ console.log(e); }
}

function logout(){ localStorage.removeItem('token'); window.location.href='/'; }

loadProfile();
</script>
</body>
</html>""")
html.close()
print('Done')
