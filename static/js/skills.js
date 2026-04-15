// Profile skills UI logic for variant 2 (user skills)
(function () {
  document.addEventListener("DOMContentLoaded", () => {
    const container = document.getElementById("skills-container");
    if (!container) return;

    const userId = container.dataset.userId;
    const addBtn = document.getElementById("add-skill-btn");
    const inputWrapper = document.getElementById("skill-input-wrapper");
    const input = document.getElementById("skill-input");
    const suggestions = document.getElementById("skill-suggestions");

    const ownerMode = Boolean(addBtn && inputWrapper && input && suggestions && userId);
    if (!ownerMode) return;

    addBtn.addEventListener("click", () => {
      addBtn.classList.add("hidden");
      inputWrapper.classList.remove("hidden");
      input.value = "";
      suggestions.innerHTML = "";
      suggestions.classList.add("hidden");
      input.focus();
    });

    let debounceTimer = null;
    input.addEventListener("input", () => {
      const q = input.value.trim();
      clearTimeout(debounceTimer);
      if (!q) {
        suggestions.classList.add("hidden");
        suggestions.innerHTML = "";
        return;
      }

      debounceTimer = setTimeout(async () => {
        try {
          const response = await fetch(`/users/skills/?q=${encodeURIComponent(q)}`);
          if (!response.ok) return;
          const data = await response.json();

          suggestions.innerHTML = "";
          data.forEach((skill) => {
            const li = document.createElement("li");
            li.textContent = skill.name;
            li.dataset.id = skill.id;
            li.className = "suggestion-item";
            suggestions.appendChild(li);
          });

          const exact = data.some((s) => s.name.toLowerCase() === q.toLowerCase());
          if (!exact) {
            const liNew = document.createElement("li");
            liNew.textContent = `Создать «${q}»`;
            liNew.dataset.name = q;
            liNew.className = "create-new";
            suggestions.appendChild(liNew);
          }

          suggestions.classList.remove("hidden");
        } catch (error) {
          console.error("Ошибка автодополнения навыков:", error);
        }
      }, 220);
    });

    suggestions.addEventListener("mousedown", async (event) => {
      const li = event.target.closest("li");
      if (!li) return;

      if (li.classList.contains("create-new")) {
        await addSkillByName(li.dataset.name);
      } else if (li.dataset.id) {
        await addSkillById(li.dataset.id);
      }
      hideInput();
    });

    input.addEventListener("keydown", async (event) => {
      if (event.key === "Enter") {
        event.preventDefault();
        const q = input.value.trim();
        if (!q) return;

        const first = suggestions.querySelector("li");
        if (first && first.dataset.id) {
          await addSkillById(first.dataset.id);
        } else {
          await addSkillByName(q);
        }
        hideInput();
      }

      if (event.key === "Escape") {
        hideInput();
      }
    });

    input.addEventListener("blur", () => setTimeout(hideInput, 120));

    function hideInput() {
      inputWrapper.classList.add("hidden");
      suggestions.classList.add("hidden");
      addBtn.classList.remove("hidden");
    }

    container.addEventListener("click", async (event) => {
      if (!event.target.classList.contains("remove-skill-btn")) return;

      const chip = event.target.closest(".skill-chip");
      if (!chip) return;

      const skillId = chip.dataset.id;
      try {
        const response = await fetch(`/users/${userId}/skills/${skillId}/remove/`, {
          method: "POST",
          headers: {
            "X-CSRFToken": window.getCookie ? window.getCookie("csrftoken") : "",
          },
        });
        if (response.ok) {
          chip.remove();
          ensureEmptyText();
        }
      } catch (error) {
        console.error("Ошибка удаления навыка:", error);
      }
    });

    async function addSkillById(skillId) {
      await addSkill({ skill_id: skillId });
    }

    async function addSkillByName(name) {
      await addSkill({ name });
    }

    async function addSkill(payload) {
      try {
        const response = await fetch(`/users/${userId}/skills/add/`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": window.getCookie ? window.getCookie("csrftoken") : "",
          },
          body: JSON.stringify(payload),
        });

        if (!response.ok) return;
        const skill = await response.json();
        const id = skill.id ?? skill.skill_id;
        const name = skill.name;
        if (!id || !name) return;
        appendChip(id, name);
      } catch (error) {
        console.error("Ошибка добавления навыка:", error);
      }
    }

    function appendChip(id, name) {
      if (container.querySelector(`.skill-chip[data-id="${id}"]`)) return;

      const chip = document.createElement("span");
      chip.className = "skill-chip";
      chip.dataset.id = id;
      chip.innerHTML = `${name} <button type="button" class="remove-skill-btn" aria-label="Удалить" title="Удалить">×</button>`;

      container.insertBefore(chip, addBtn);

      const empty = container.querySelector(".skill-empty");
      if (empty) empty.remove();
    }

    function ensureEmptyText() {
      if (container.querySelector(".skill-chip")) return;
      if (container.querySelector(".skill-empty")) return;

      const empty = document.createElement("span");
      empty.className = "skill-empty";
      empty.textContent = "Пока навыков нет.";
      container.insertBefore(empty, addBtn);
    }
  });
})();
