(() => {
  const TERMS = {
    function: {
      label: "Function",
      definition: "A named block of code that performs a job and can be used from other code.",
      source: "Official Python terminology, explained in the Python tutorial",
      url: "https://docs.python.org/3/tutorial/controlflow.html#defining-functions",
    },
    module: {
      label: "Module",
      definition: "A unit of code with an interface and an implementation. It can be a function, class, subsystem, or service.",
      source: "Paraphrased from John Ousterhout, A Philosophy of Software Design, 2nd ed., Chapter 4",
    },
    service: {
      label: "Service",
      definition: "A higher-level unit of software with an interface and an implementation.",
      source: "Paraphrased from John Ousterhout, A Philosophy of Software Design, 2nd ed., Chapter 4",
    },
    interface: {
      label: "Interface",
      definition: "Everything someone working elsewhere must know to use the module. It describes what the module does, not how it does it.",
      source: "Paraphrased from John Ousterhout, A Philosophy of Software Design, 2nd ed., Chapter 4",
    },
    implementation: {
      label: "Implementation",
      definition: "The code that carries out the promises made by the interface.",
      source: "John Ousterhout, A Philosophy of Software Design, 2nd ed., Chapter 4",
    },
    abstraction: {
      label: "Abstraction",
      definition: "A simplified view of something that leaves out unimportant details.",
      source: "Paraphrased from John Ousterhout, A Philosophy of Software Design, 2nd ed., Chapter 4",
    },
    docstring: {
      label: "Docstring",
      definition: "Text placed as the first statement inside a function, class, or module to explain it.",
      source: "Paraphrased from Python PEP 257",
      url: "https://peps.python.org/pep-0257/#what-is-a-docstring",
    },
    none: {
      label: "None",
      definition: "Python’s built-in object for representing the absence of a value.",
      source: "Official Python documentation",
      url: "https://docs.python.org/3/library/constants.html#None",
    },
    callable: {
      label: "Callable",
      definition: "Any Python object that can be used with function-call syntax, including functions, classes, and some other objects.",
      source: "Official Python glossary",
      url: "https://docs.python.org/3/glossary.html#term-callable",
    },
    classifier: {
      label: "Classifier",
      definition: "A component that assigns an input to a category. In this course it proposes an ANZSIC category from website evidence.",
      source: "Standard data and machine-learning term, specialised for this course",
    },
    confidence: {
      label: "Confidence",
      definition: "A score used here to show how strongly the chosen model supports a suggestion. Its exact meaning depends on that model.",
      source: "Course domain definition, not a definition taken from the books",
    },
    anzsic: {
      label: "ANZSIC",
      definition: "The Australian and New Zealand Standard Industrial Classification, used to group organisations by their main business activity.",
      source: "Australian Bureau of Statistics, ANZSIC 2006, Revision 2.0",
      url: "https://www.abs.gov.au/statistics/classifications/australian-and-new-zealand-standard-industrial-classification-anzsic/latest-release",
    },
    "anzsic-suggestion": {
      label: "ANZSIC suggestion",
      definition: "A proposed ANZSIC code and label that still carries its evidence, confidence, and review status.",
      source: "Course domain term, not a definition taken from the books",
    },
    "ubiquitous-language": {
      label: "Ubiquitous Language",
      definition: "Language built around one domain model and used consistently by the people who build and discuss that domain.",
      source: "Paraphrased from Eric Evans, Domain-Driven Design, Chapter 2",
    },
    domain: {
      label: "Domain",
      definition: "The subject area in which the software is used and the knowledge needed to work in that area.",
      source: "Paraphrased from Eric Evans, Domain-Driven Design",
    },
    stage: {
      label: "Stage",
      definition: "Where a value currently sits in a sequence of work, such as candidate, verified, or classified.",
      source: "Course-authored teaching term, not a definition taken from the books",
    },
    boundary: {
      label: "Boundary",
      definition: "The point where this code meets another system, team, or responsibility.",
      source: "Standard software term; this plain definition is course-authored",
    },
    "side-effect": {
      label: "Side effect",
      definition: "A change outside the returned value, such as saving data, sending a message, or modifying an input.",
      source: "Standard software term; PEP 257 says function documentation should describe side effects",
      url: "https://peps.python.org/pep-0257/#multi-line-docstrings",
    },
    contract: {
      label: "Contract",
      definition: "Shorthand used in broader software engineering for behaviour that other code is allowed to rely on.",
      source: "Not used in the reviewed Ousterhout chapters; optional course terminology",
    },
  };

  const triggers = [...document.querySelectorAll(".term[data-term]")];
  if (!triggers.length) return;

  const tooltip = document.createElement("aside");
  tooltip.className = "term-tooltip";
  tooltip.id = "term-tooltip";
  tooltip.setAttribute("role", "tooltip");
  tooltip.hidden = true;
  document.body.append(tooltip);

  let activeTrigger = null;
  let pinned = false;
  let closeTimer = null;

  const clearCloseTimer = () => {
    if (closeTimer) window.clearTimeout(closeTimer);
    closeTimer = null;
  };

  const positionTooltip = () => {
    if (!activeTrigger || tooltip.hidden) return;
    const triggerRect = activeTrigger.getBoundingClientRect();
    const tooltipRect = tooltip.getBoundingClientRect();
    const margin = 12;
    let left = triggerRect.left + triggerRect.width / 2 - tooltipRect.width / 2;
    left = Math.max(margin, Math.min(left, window.innerWidth - tooltipRect.width - margin));
    let top = triggerRect.bottom + 9;
    if (top + tooltipRect.height > window.innerHeight - margin) {
      top = triggerRect.top - tooltipRect.height - 9;
    }
    tooltip.style.left = `${Math.max(margin, left)}px`;
    tooltip.style.top = `${Math.max(margin, top)}px`;
  };

  const renderTooltip = (trigger) => {
    const entry = TERMS[trigger.dataset.term];
    if (!entry) return false;
    tooltip.replaceChildren();

    const heading = document.createElement("strong");
    heading.className = "term-tooltip__heading";
    heading.textContent = entry.label;

    const definition = document.createElement("span");
    definition.className = "term-tooltip__definition";
    definition.textContent = entry.definition;

    const source = entry.url ? document.createElement("a") : document.createElement("span");
    source.className = "term-tooltip__source";
    source.textContent = `Source: ${entry.source}`;
    if (entry.url) {
      source.href = entry.url;
      source.target = "_blank";
      source.rel = "noreferrer";
    }

    tooltip.append(heading, definition, source);
    return true;
  };

  const openTooltip = (trigger, shouldPin = false) => {
    clearCloseTimer();
    if (!renderTooltip(trigger)) return;
    if (activeTrigger && activeTrigger !== trigger) activeTrigger.setAttribute("aria-expanded", "false");
    activeTrigger = trigger;
    pinned = shouldPin;
    trigger.setAttribute("aria-expanded", "true");
    tooltip.hidden = false;
    positionTooltip();
  };

  const closeTooltip = () => {
    clearCloseTimer();
    if (activeTrigger) activeTrigger.setAttribute("aria-expanded", "false");
    activeTrigger = null;
    pinned = false;
    tooltip.hidden = true;
  };

  const scheduleClose = () => {
    clearCloseTimer();
    closeTimer = window.setTimeout(() => {
      if (!pinned) closeTooltip();
    }, 140);
  };

  triggers.forEach((trigger) => {
    if (!TERMS[trigger.dataset.term]) return;
    trigger.dataset.registered = "true";
    trigger.setAttribute("tabindex", "0");
    trigger.setAttribute("role", "button");
    trigger.setAttribute("aria-expanded", "false");
    trigger.setAttribute("aria-describedby", tooltip.id);

    trigger.addEventListener("mouseenter", () => openTooltip(trigger));
    trigger.addEventListener("mouseleave", scheduleClose);
    trigger.addEventListener("focus", () => openTooltip(trigger));
    trigger.addEventListener("blur", (event) => {
      if (!tooltip.contains(event.relatedTarget)) scheduleClose();
    });
    trigger.addEventListener("click", (event) => {
      event.preventDefault();
      if (activeTrigger === trigger && pinned) closeTooltip();
      else openTooltip(trigger, true);
    });
    trigger.addEventListener("keydown", (event) => {
      if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        openTooltip(trigger, true);
      }
      if (event.key === "Escape") closeTooltip();
    });
  });

  tooltip.addEventListener("mouseenter", clearCloseTimer);
  tooltip.addEventListener("mouseleave", scheduleClose);
  tooltip.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
      const triggerToRestore = activeTrigger;
      closeTooltip();
      triggerToRestore?.focus();
    }
  });
  document.addEventListener("click", (event) => {
    if (activeTrigger && !activeTrigger.contains(event.target) && !tooltip.contains(event.target)) closeTooltip();
  });
  window.addEventListener("scroll", positionTooltip, { passive: true });
  window.addEventListener("resize", positionTooltip);
})();
