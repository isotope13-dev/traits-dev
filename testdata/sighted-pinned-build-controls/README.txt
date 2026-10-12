Focused controls are staged outside testdata before scanning, because
the production rules exclude inert test-corpus paths. cases.json paths
are relative to this directory; stage each basename in one scratch folder.
The Gradle fixture substitutes an inert .invalid URL and a different
character-stripped decoder name to test generalization.
