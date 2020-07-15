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

### Version 0.2.1 (2020-07-15)

- [ENHANCEMENT] Edited conditional styles for readability and color contrast.
- [BUGFIX] conditional styles and their legend now update with table selection.

### Version 0.2.0 (2020-07-15)

#### Minor Release

- [CODEQUALITY] Pandas backend now stores HDF5; no more JSON I/O.
- [CODEQUALITY] grunt used to copy static web assets from UIKit.
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
