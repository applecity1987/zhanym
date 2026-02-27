from pathlib import Path
import re

file_path = Path("templates/chat.html")
content = file_path.read_text()

new_function = """
function renderMatches(matches) {
    const list = document.getElementById("matches-list");

    list.innerHTML = matches.map(m => `
        <div class="match-item" id="match-${m.id}"
            onclick="openChat(${m.id}, '${m.name}', '${m.gender}')">
            <div class="match-avatar">
                ${m.gender === "female" ? "👩" : "👨"}
            </div>
            <div>
                <div class="match-name">${m.name}, ${m.age}</div>
                <div class="match-preview">${m.city}</div>
            </div>
        </div>
    `).join("");
}
"""

content = re.sub(
    r"function renderMatches\(.*?\}",
    new_function,
    content,
    flags=re.DOTALL
)

file_path.write_text(content)

print("renderMatches обновлена успешно")
