(() => {
  const lessonKey = document.body.dataset.lesson || "lesson";
  const state = JSON.parse(localStorage.getItem(`teach:${lessonKey}`) || "{}");

  const save = () => localStorage.setItem(`teach:${lessonKey}`, JSON.stringify(state));

  document.querySelectorAll(".question").forEach((question, questionIndex) => {
    const feedback = question.querySelector(".feedback");
    question.querySelectorAll(".choice").forEach((button) => {
      button.addEventListener("click", () => {
        question.querySelectorAll(".choice").forEach((choice) => {
          choice.classList.remove("correct", "wrong");
        });
        const isCorrect = button.dataset.correct === "true";
        button.classList.add(isCorrect ? "correct" : "wrong");
        feedback.textContent = isCorrect
          ? button.dataset.feedback
          : `Not yet. ${button.dataset.feedback}`;
        state[`question${questionIndex}`] = isCorrect;
        save();
      });
    });
  });

  const editor = document.querySelector("#refactor-editor");
  const checkButton = document.querySelector("#check-refactor");
  const resetButton = document.querySelector("#reset-refactor");
  const checklist = document.querySelector("#refactor-checklist");

  if (editor && checkButton && checklist) {
    const initialCode = editor.value;
    if (state.code) editor.value = state.code;

    const checks = [
      {
        label: "The function says it selects or filters a result.",
        test: (code) => /def\s+(select|filter|find|choose)_[a-z_]+\s*\(/i.test(code),
      },
      {
        label: "The inputs name documents or records, not xs.",
        test: (code) => /(documents|records|texts)/i.test(code) && !/\bxs\b/.test(code),
      },
      {
        label: "The model role is explicit, not m.",
        test: (code) => /(classifier|classification_model|model)/i.test(code) && !/\bm\b/.test(code),
      },
      {
        label: "The threshold names confidence and its meaning.",
        test: (code) => /(confidence_threshold|minimum_confidence|min_confidence)/i.test(code),
      },
      {
        label: "Predictions or probabilities replace r and p.",
        test: (code) => /(probabilities|predictions|class_scores)/i.test(code) && !/\br\b/.test(code),
      },
    ];

    const renderChecks = (code) => {
      checklist.innerHTML = "";
      let score = 0;
      checks.forEach((check) => {
        const passed = check.test(code);
        score += Number(passed);
        const item = document.createElement("li");
        item.className = passed ? "pass" : "";
        item.textContent = check.label;
        checklist.appendChild(item);
      });
      const feedback = document.querySelector("#refactor-feedback");
      feedback.textContent = score === checks.length
        ? "All five signals are explicit. Your code now carries its own context."
        : `${score}/5 signals are explicit. Keep the behaviour unchanged and improve only the names.`;
      state.refactorScore = score;
      state.code = code;
      save();
    };

    checkButton.addEventListener("click", () => renderChecks(editor.value));
    resetButton.addEventListener("click", () => {
      editor.value = initialCode;
      delete state.code;
      state.refactorScore = 0;
      save();
      renderChecks(initialCode);
    });

    if (state.code) renderChecks(state.code);
  }

  const contractBuilder = document.querySelector("#contract-builder");
  if (contractBuilder) {
    const options = [...contractBuilder.querySelectorAll(".contract-option")];
    const checkContract = contractBuilder.querySelector("#check-contract");
    const resetContract = contractBuilder.querySelector("#reset-contract");
    const contractFeedback = contractBuilder.querySelector("#contract-feedback");
    const selected = new Set(state.contractSelections || []);

    const renderSelections = () => {
      options.forEach((option, index) => {
        const isSelected = selected.has(index);
        option.classList.toggle("selected", isSelected);
        option.setAttribute("aria-pressed", String(isSelected));
      });
      state.contractSelections = [...selected];
      save();
    };

    options.forEach((option, index) => {
      option.setAttribute("aria-pressed", "false");
      option.addEventListener("click", () => {
        if (selected.has(index)) selected.delete(index);
        else selected.add(index);
        options.forEach((item) => item.classList.remove("correct", "wrong", "excluded"));
        contractFeedback.textContent = "Selection updated. Check when the contract contains only caller-visible promises.";
        renderSelections();
      });
    });

    checkContract.addEventListener("click", () => {
      let score = 0;
      options.forEach((option, index) => {
        const shouldSelect = option.dataset.contract === "true";
        const matches = selected.has(index) === shouldSelect;
        score += Number(matches);
        option.classList.toggle("correct", matches && shouldSelect);
        option.classList.toggle("excluded", matches && !shouldSelect);
        option.classList.toggle("wrong", !matches);
      });
      contractFeedback.textContent = score === options.length
        ? "5/5. The contract is complete without exposing replaceable machinery."
        : `${score}/5 facts are classified correctly. Keep caller-visible promises; remove replaceable machinery.`;
      state.contractScore = score;
      save();
    });

    resetContract.addEventListener("click", () => {
      selected.clear();
      options.forEach((option) => option.classList.remove("correct", "wrong", "excluded"));
      contractFeedback.textContent = "Three promises and two implementation details are mixed together.";
      state.contractScore = 0;
      renderSelections();
    });

    renderSelections();
  }

  const progressBar = document.querySelector(".progress span");
  const updateProgress = () => {
    const root = document.documentElement;
    const max = root.scrollHeight - root.clientHeight;
    const progress = max > 0 ? (root.scrollTop / max) * 100 : 100;
    if (progressBar) progressBar.style.width = `${progress}%`;
  };
  document.addEventListener("scroll", updateProgress, { passive: true });
  updateProgress();
})();
