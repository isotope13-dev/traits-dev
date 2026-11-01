# SEO evidence review

The legacy SEO-spam rules included observations that do not establish spam:
repeated `rel="dofollow"` attributes, a sitemap closing tag, `strstr` text,
a regular expression for a double-hash prefix, and a WordPress theme name.
These now live under their observed subjects. The former sitemap-and-search
combination is a sitemap profile, not a search-engine cloaking claim.

The hosts-file sinkhole rule previously selected these through the dropper
ancestor. It now names the moved observations explicitly to preserve the
existing selection. The remaining rules are now migrated: response-based
redirects, encoded resource reads, backlink endpoint references and remote
markup insertion live with those operations, while SEO spam combinations
live under `objectives/impact/spam`. The broad sitemap/offscreen/redirect or
curl combinations are suspicious clues rather than conclusive hostile spam;
the WordPress backlink-feed combination retains its hostile assessment. The
former ancestor consumer explicitly retains the moved positive alternatives.

The near-cap markup insertion leaf also included record-field and HTML
construction observations. These moved to assignment/conditional syntax and
markup subjects, retaining explicit references to the insertion facts they use.
