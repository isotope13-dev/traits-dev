// Static analyzer control. Never execute this fixture.
// A browser UI helper that manages theme cards via DOM class selectors.
// The `.themes` string is a jQuery class selector, not a GNOME theme
// directory, so the GNOME theme-resource atom must stay silent here
// (WordPress admin theme.js tripped it).
function renderThemes( view ) {
  view.$el.find( '.themes' ).remove();
  const panel = document.createElement( 'div' );
  view.$el.find( '.theme-browser' ).append( panel );
  return panel;
}

module.exports = { renderThemes };
