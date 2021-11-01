**Changed:**

* Cleaned up the implementation quite a bit. Mostly, by properly separating
  different visualizations. They are all still available as `Widget` but this
  then dispatches to the actual implementation classes.
  Note that the old `FlatSurface` class is gone.

* Upgrade to vue-flatsurf 0.8.1 which brings lots of new features. However,
  some features such as setting a glueing from the outside have not been
  migrated yet.

* We now depend on ipyvue-async to make blocking asynchronous calls into the
  Widget in Jupyter Notebooks.
