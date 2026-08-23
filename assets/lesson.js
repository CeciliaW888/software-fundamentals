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
    if (state[`question${questionIndex}`] === true) {
      const correctChoice = question.querySelector('.choice[data-correct="true"]');
      if (correctChoice) {
        correctChoice.classList.add("correct");
        feedback.textContent = correctChoice.dataset.feedback;
      }
    }
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
        label: "The input names About-page text or customer records.",
        test: (code) => /(about_page_texts|customer_records|industry_suggestions)/i.test(code) && !/\bxs\b/.test(code),
      },
      {
        label: "The model’s industry-classifier job is explicit.",
        test: (code) => /(industry_classifier|classification_model|classifier)/i.test(code) && !/\bm\b/.test(code),
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
        ? "All five pieces of meaning are visible. The code explains its own job."
        : `${score}/5 pieces of meaning are visible. Keep the behaviour unchanged and improve only the names.`;
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

  const promiseBuilder = document.querySelector("#promise-builder");
  if (promiseBuilder) {
    const options = [...promiseBuilder.querySelectorAll(".promise-option")];
    const checkPromises = promiseBuilder.querySelector("#check-promises");
    const resetPromises = promiseBuilder.querySelector("#reset-promises");
    const promiseFeedback = promiseBuilder.querySelector("#promise-feedback");
    const selected = new Set(state.promiseSelections || state.contractSelections || []);

    const renderSelections = () => {
      options.forEach((option, index) => {
        const isSelected = selected.has(index);
        option.classList.toggle("selected", isSelected);
        option.setAttribute("aria-pressed", String(isSelected));
      });
      state.promiseSelections = [...selected];
      delete state.contractSelections;
      save();
    };

    options.forEach((option, index) => {
      option.setAttribute("aria-pressed", "false");
      option.addEventListener("click", () => {
        if (selected.has(index)) selected.delete(index);
        else selected.add(index);
        options.forEach((item) => item.classList.remove("correct", "wrong", "excluded"));
        promiseFeedback.textContent = "Selection updated. Check when you have kept only facts that other code needs.";
        renderSelections();
      });
    });

    checkPromises.addEventListener("click", () => {
      let score = 0;
      options.forEach((option, index) => {
        const shouldSelect = option.dataset.promise === "true";
        const matches = selected.has(index) === shouldSelect;
        score += Number(matches);
        option.classList.toggle("correct", matches && shouldSelect);
        option.classList.toggle("excluded", matches && !shouldSelect);
        option.classList.toggle("wrong", !matches);
      });
      promiseFeedback.textContent = score === options.length
        ? "5/5. You kept every promise and left out both temporary details."
        : `${score}/5 choices are correct. Keep promised behaviour and remove temporary details.`;
      state.promiseScore = score;
      delete state.contractScore;
      save();
    });

    resetPromises.addEventListener("click", () => {
      selected.clear();
      options.forEach((option) => option.classList.remove("correct", "wrong", "excluded"));
      promiseFeedback.textContent = "Three promises and two temporary details are mixed together.";
      state.promiseScore = 0;
      delete state.contractScore;
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
