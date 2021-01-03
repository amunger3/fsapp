---
page_type: meta
languages:
- python
description: "CHANGELOG"
urlFragment: changelog
---
# Elo Football App

## Release Notes

Changelog labels are any of the following:

- [BUGFIX], [CHANGE], [CODEQUALITY], [DEPENDENCY], [ENHANCEMENT], [OTHER], [TRANSLATION]

### Version 0.9.2 (2021-01-02)

- [ENHANCEMENT] Added area flag SVG and current matchday to card titles.
- [CODEQUALITY] `npm run update` now also updates the `\comps` table for current matchday info.

### Version 0.9.1 (2020-12-30)

- [CHANGE] Switched to backend table sortings (pandas), sacrificing speed for greater flexibility
- [ENHANCEMENT] Some cosmetic UI changes

### Version 0.9.0 (2020-12-23)

#### Minor Release 0.9

- [OTHER] Successful deployment to heroku with Python 3.9.1.

### Version 0.8.0 (2020-11-17)

#### Minor Release 0.8

- [ENHANCEMENT] Added Teams tab, for future graphing capabilities.

### Version 0.7.0 (2020-11-13)

#### Minor Release 0.7

- [OTHER] Updated to 2020-2021 Season.
- [OTHER] New runtime: Python 3.9.0.

### Version 0.6.0 (2020-08-13)

#### Minor Release 0.6

- [ENHANCEMENT] Standings API incorporated into DataTable.

### Version 0.5.2 (2020-08-13)

- [CODEQUALITY] Updated 'comps' DataFrame to remove Pandas warning.
- [ENHANCEMENT] Customized app title and icon.

### Version 0.5.1 (2020-08-13)

- [DEPENDENCY] Updated UIKit to 3.5.6.

### Version 0.5.0 (2020-08-09)

#### Minor Release 0.5

- [BUGFIX] Bundesliga now working, all query filters are functional.
- [DEPENDENCY] Added PyTest, to implement in future release.
- [DEPENDENCY] Pandas upgraded to 1.1.0, throwing a deprecation warning — to keep in mind.
- [DEPENDENCY] Dash upgraded to 1.14. No significant effects.
- [OTHER] All 2019-2020 season Elo ratings finalized.
- [CODEQUALITY] Rework of class responsibilities; will be easier to expand to multi-year/multi-stage.

### Version 0.4.2 (2020-07-26)

- [OTHER] Updated runtime to Python 3.8.5.

### Version 0.4.1 (2020-07-26)

- [ENHANCEMENT] Added Elo Rank column to DataTable.
- [CODEQUALITY] Uninstalled unused Python packages.
- [DEPENDENCY] Updated to Plotly 4.9.

### Version 0.4.0 (2020-07-16)

#### Minor Release 0.4

- [ENHANCEMENT] Added last match results to data table.
- [ENHANCEMENT] Lots of UI improvements.

### Version 0.3.0 (2020-07-16)

#### Minor Release 0.3

- [ENHANCEMENT] Added custom UIKit theme and built from Sass.
- [DEPENDENCY] Grunt-contrib-sass, Ruby, Ruby-sass

### Version 0.2.1 (2020-07-15)

- [ENHANCEMENT] Edited conditional styles for readability and color contrast.
- [BUGFIX] Conditional styles and their legend now update with table selection.

### Version 0.2.0 (2020-07-15)

#### Minor Release 0.2

- [CODEQUALITY] Pandas backend now stores HDF5; no more JSON I/O.
- [CODEQUALITY] Grunt used to copy static web assets from UIKit.
- [DEPENDENCY] Grunt (dev) (NPM).
- [DEPENDENCY] UIKit upgraded to v3.5.5.

### Version 0.1.9 (2020-07-11)

- [ENHANCEMENT] Dash app is fully functional. 0.2 will release when integrated into heroku.

### Version 0.1.1 (2020-07-11)

- [CHANGE] Beginning transition to [Dash DataTable](https://dash.plotly.com/datatable) app.
- [DEPENDENCY] [Dash](https://dash.plotly.com), [Dash_DAQ](https://dash.plotly.com/dash-daq), [NumPy](https://numpy.org/doc/stable/reference/index.html), [Pandas](https://pandas.pydata.org/pandas-docs/stable/index.html)

### Version 0.1.0 (2020-07-11)

- [ENHANCEMENT] First working version with all competition routes and tables.
- [DEPENDENCY] [MPMath](http://mpmath.org/doc/current/)

### Version 0.0.3 (2020-07-03)

- [ENHANCEMENT] Now using [UIKit](https://getuikit.com/docs).
- [DEPENDENCY] UIKit (NPM)

### Version 0.0.2 (2020-07-03)

- [CHANGE] Migrated files from other reopsitory.

### Version 0.0.1 (2020-07-03)

- [ENHANCEMENT] [Deployed on Heroku](https://fs-mir-pro.herokuapp.com/).
- [CODEQUALITY] Changelog and SemVer initialized.
