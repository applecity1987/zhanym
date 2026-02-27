html = open('/Users/darknet/dating-site/templates/about.html', 'w', encoding='utf-8')
html.write("""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>О нас — Zhanym</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:Arial,sans-serif;background:#f9f9f9;color:#333}
.header{background:#1a1a2e;padding:20px 40px;display:flex;justify-content:space-between;align-items:center}
.logo{font-size:24px;font-weight:900;color:white;text-decoration:none}
.nav a{color:rgba(255,255,255,.8);text-decoration:none;margin-left:20px;font-size:15px}
.hero{background:linear-gradient(135deg,#1a1a2e,#ff4458);padding:80px 40px;text-align:center;color:white}
.hero h1{font-size:52px;font-weight:900;margin-bottom:15px}
.hero p{font-size:20px;opacity:.9;max-width:650px;margin:0 auto}
.content{max-width:900px;margin:60px auto;padding:0 40px}
.section{background:white;border-radius:20px;padding:40px;margin-bottom:30px;box-shadow:0 5px 20px rgba(0,0,0,.08)}
.section h2{font-size:28px;font-weight:900;color:#1a1a2e;margin-bottom:20px}
.section p{color:#666;font-size:17px;line-height:1.9;margin-bottom:15px}
.section p:last-child{margin-bottom:0}
.highlight{background:linear-gradient(135deg,#ff4458,#fd79a8);color:white;border-radius:20px;padding:40px;margin-bottom:30px;text-align:center}
.highlight h2{font-size:32px;font-weight:900;margin-bottom:15px}
.highlight p{font-size:18px;opacity:.9;line-height:1.8}
.values{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin-top:20px}
.value{background:#f9f9f9;border-radius:15px;padding:25px;text-align:center}
.value-icon{font-size:40px;margin-bottom:12px}
.value h3{font-size:18px;font-weight:bold;color:#1a1a2e;margin-bottom:8px}
.value p{color:#888;font-size:14px}
.cta{text-align:center;padding:60px 40px}
.cta h2{font-size:38px;font-weight:900;color:#1a1a2e;margin-bottom:15px}
.cta p{color:#888;font-size:18px;margin-bottom:30px}
.btn{background:linear-gradient(135deg,#ff4458,#fd79a8);color:white;padding:16px 45px;border-radius:50px;font-size:18px;font-weight:bold;text-decoration:none;display:inline-block}
.footer{background:#1a1a2e;padding:40px;text-align:center;color:rgba(255,255,255,.5)}
.footer-logo{font-size:22px;font-weight:900;color:white;margin-bottom:10px}
</style>
</head>
<body>
<div class="header">
  <a href="/" class="logo">🌹 Zhanym</a>
  <div class="nav">
    <a href="/">Главная</a>
    <a href="/safety">Безопасность</a>
    <a href="/register">Регистрация</a>
    <a href="/login">Войти</a>
  </div>
</div>

<div class="hero">
  <h1>🌹 О нас</h1>
  <p>Zhanym — это казахстанская платформа знакомств, созданная для тех, кто ищет настоящую связь</p>
</div>

<div class="content">

  <div class="section">
    <h2>Почему стоит знакомиться именно в Zhanym?</h2>
    <p>Выбор платформ для знакомств огромен: Tinder, Bumble, Badoo, Mamba и многие другие. Если ты хочешь найти любовь, сходить на свидание или просто поболтать — тебе нужна платформа, на которую можно положиться.</p>
    <p>В знакомствах не всегда всё однозначно. Если ты стремишься встретить новых людей, в Zhanym ты найдёшь всё необходимое для этого. Мы создали платформу специально для казахстанцев — здесь ты встретишь людей из своего города, которые говорят на твоём языке и разделяют твою культуру.</p>
    <p>Знакомиться онлайн — это просто. Не будем просто говорить, что мы лучше — лучше убедись сам, попробовав Zhanym! 🌹</p>
  </div>

  <div class="highlight">
    <h2>💞 Наша миссия</h2>
    <p>Мы верим, что каждый человек заслуживает найти свою вторую половинку. Zhanym создан чтобы сделать знакомства простыми, безопасными и приятными для каждого казахстанца.</p>
  </div>

  <div class="section">
    <h2>Наши ценности</h2>
    <div class="values">
      <div class="value">
        <div class="value-icon">❤️</div>
        <h3>Искренность</h3>
        <p>Мы верим в настоящие чувства и помогаем людям находить друг друга</p>
      </div>
      <div class="value">
        <div class="value-icon">🔒</div>
        <h3>Безопасность</h3>
        <p>Защита данных и безопасность каждого пользователя — наш главный приоритет</p>
      </div>
      <div class="value">
        <div class="value-icon">🌍</div>
        <h3>Для Казахстана</h3>
        <p>Мы создали платформу для казахстанцев — с учётом нашей культуры и ценностей</p>
      </div>
    </div>
  </div>

  <div class="section">
    <h2>Как это работает?</h2>
    <p>Зарегистрируйся бесплатно и заполни свой профиль. Укажи своё имя, возраст, город и немного о себе. Загрузи фото чтобы другие пользователи могли тебя увидеть.</p>
    <p>Просматривай анкеты людей рядом с тобой. Понравился кто-то — поставь лайк ❤️. Если симпатия взаимна — это пара! Теперь вы можете общаться в чате.</p>
    <p>Всё просто, быстро и бесплатно. Начни прямо сейчас!</p>
  </div>

</div>

<div class="cta">
  <h2>Готов найти свою пару? 🌹</h2>
  <p>Присоединяйся к тысячам людей которые уже нашли своё счастье в Zhanym</p>
  <a href="/register" class="btn">🚀 Создать аккаунт бесплатно</a>
</div>

<div class="footer">
  <div class="footer-logo">🌹 Zhanym</div>
  <p>© 2026 Zhanym. Все права защищены.</p>
</div>
</body>
</html>""")
html.close()
print('Done')
