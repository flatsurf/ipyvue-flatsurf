const plugin = require('./plugin');
const base = require('@jupyter-widgets/base');

module.exports = {
  id: 'ipyvue-flatsurf:plugin',
  requires: [base.IJupyterWidgetRegistry],
  activate: function(app, widgets) {
      plugin.activate(app, widgets);
      widgets.registerWidget({
          name: 'ipyvue-flatsurf',
          version: plugin.version,
          exports: plugin
      });
  },
  autoStart: true
};
