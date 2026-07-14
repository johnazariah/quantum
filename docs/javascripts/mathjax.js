window.MathJax = {
  tex: {
    inlineMath: [["\\(", "\\)"]],
    displayMath: [["\\[", "\\]"]],
    processEscapes: true,
    processEnvironments: true,
    macros: {
      ket: ["{\\left|#1\\right\\rangle}", 1],
      bra: ["{\\left\\langle#1\\right|}", 1],
      braket: ["{\\left\\langle#1\\middle|#2\\right\\rangle}", 2],
      melem: ["{\\left\\langle#1\\middle|#2\\middle|#3\\right\\rangle}", 3],
      expval: ["{\\left\\langle#1\\right\\rangle}", 1]
    }
  },
  options: {
    ignoreHtmlClass: ".*|",
    processHtmlClass: "arithmatex"
  }
};

document$.subscribe(() => {
  MathJax.typesetPromise()
})
