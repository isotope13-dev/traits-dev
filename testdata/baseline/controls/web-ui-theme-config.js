// Static analyzer control. Never execute this fixture.
// A web UI helper that reads theme config paths like `daisyui.themes`.
// Dotted config accessors are not GNOME theme-directory references, so the
// GNOME theme-resource atom must stay silent here (daisyUI tripped it).
function injectThemes(addBase, config, themes) {
  const includedThemesObj = {}
  // add default themes
  Object.entries(themes).forEach(([theme, value]) => {
    includedThemesObj[theme] = value
  })
  // add custom themes
  if (Array.isArray(config("daisyui.themes"))) {
    config("daisyui.themes").forEach((item) => {
      if (typeof item === "object" && item !== null) {
        Object.entries(item).forEach(([theme, value]) => {
          includedThemesObj[theme] = value
        })
      }
    })
  } else if (config("daisyui.themes") === true) {
    Object.entries(themes).forEach(([theme, value]) => {
      includedThemesObj[theme] = value
    })
  }
  return includedThemesObj
}

module.exports = { injectThemes }
