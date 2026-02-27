html = open('/Users/darknet/dating-site/templates/register.html', 'w', encoding='utf-8')
html.write("""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Регистрация — LoveMatch</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:Arial,sans-serif;background:linear-gradient(135deg,#ff6b6b,#fd79a8);min-height:100vh;display:flex;align-items:center;justify-content:center;padding:20px}
.box{background:#fff;border-radius:30px;padding:40px;max-width:480px;width:100%;box-shadow:0 20px 60px rgba(0,0,0,.3)}
h1{text-align:center;color:#ff6b6b;margin-bottom:5px;font-size:28px}
.sub{text-align:center;color:#aaa;margin-bottom:25px;font-size:14px}
.row{display:grid;grid-template-columns:1fr 1fr;gap:15px}
.group{margin-bottom:15px}
label{display:block;font-size:13px;color:#666;margin-bottom:5px;font-weight:bold}
input,select{width:100%;padding:12px 15px;border:2px solid #eee;border-radius:12px;font-size:15px;outline:none}
input:focus,select:focus{border-color:#ff6b6b}
.btn{width:100%;padding:15px;background:linear-gradient(135deg,#ff6b6b,#fd79a8);color:#fff;border:none;border-radius:50px;font-size:18px;font-weight:bold;cursor:pointer;margin-top:10px}
.login{text-align:center;margin-top:15px;color:#aaa;font-size:14px}
.login a{color:#ff6b6b;text-decoration:none;font-weight:bold}
.error{background:#ffe0e0;color:#ff4444;padding:10px 15px;border-radius:10px;margin-bottom:15px;font-size:14px;display:none}
.success{background:#e0ffe0;color:#44aa44;padding:10px 15px;border-radius:10px;margin-bottom:15px;font-size:14px;display:none}
</style>
</head>
<body>
<div class="box">
<div style="text-align:center;font-size:40px;margin-bottom:10px">💕</div>
<h1>Создать аккаунт</h1>
<p class="sub">Найди свою вторую половинку</p>
<div class="error" id="error"></div>
<div class="success" id="success"></div>
<div class="row">
<div class="group"><label>Имя</label><input type="text" id="name" placeholder="Алия"></div>
<div class="group"><label>Возраст</label><input type="number" id="age" placeholder="25" min="18"></div>
</div>
<div class="group"><label>Email</label><input type="email" id="email" placeholder="email@mail.ru"></div>
<div class="group"><label>Логин</label><input type="text" id="username" placeholder="username"></div>
<div class="group"><label>Пароль</label><input type="password" id="password" placeholder="********"></div>
<div class="row">
<div class="group"><label>Пол</label><select id="gender"><option value="">Выбери</option><option value="male">Мужской</option><option value="female">Женский</option></select></div>
<div class="group"><label>Город</label><input type="text" id="city" placeholder="Алматы"></div>
</div>
<button class="btn" onclick="register()">Зарегистрироваться</button>
<p class="login">Уже есть аккаунт? <a href="/login">Войти</a></p>
</div>
<script>
async function register() {
  const name = document.getElementById('name').value;
  const age = document.getElementById('age').value;
  const email = document.getElementById('email').value;
  const username = document.getElementById('username').value;
  const password = document.getElementById('password').value;
  const gender = document.getElementById('gender').value;
  const city = document.getElementById('city').value;
  if(!name||!age||!email||!username||!password||!gender||!city){
    showError('Заполни все поля'); return;
  }
  try {
    const res = await fetch('/register?email='+email+'&username='+username+'&password='+password+'&name='+name+'&age='+age+'&gender='+gender+'&city='+city, {method:'POST'});
    const data = await res.json();
    if(res.ok){ showSuccess('Аккаунт создан'); setTimeout(()=>window.location.href='/login',1500); }
    else { showError(data.detail||'Ошибка'); }
  } catch(e){ showError('Ошибка сервера'); }
}
function showError(msg){ const el=document.getElementById('error'); el.textContent=msg; el.style.display='block'; }
function showSuccess(msg){ const el=document.getElementById('success'); el.textContent=msg; el.style.display='block'; }
</script>
</body>
</html>""")
html.close()
print('Done')
