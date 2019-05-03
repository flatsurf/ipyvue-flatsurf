const path = require('path');
const version = require('./package.json').version;
const { VueLoaderPlugin } = require('vue-loader');
const webpack = require('webpack');

// Custom webpack rules
const rules = [
  { test: /\.ts$/, loader: 'ts-loader' , options: {
    appendTsSuffixTo: [/\.vue$/],
  } },
  { test: /\.js$/, loader: 'source-map-loader' },
  { test: /\.css$/, use: ['vue-style-loader', 'css-loader']},
  { test: /\.scss$/, use: ['vue-style-loader', 'css-loader' , 'sass-loader']},
  { test: /\.vue$/, use: ['vue-loader']},
  { test: /\.svg$/, use: ['svg-url-loader']},
];

// Packages that shouldn't be bundled but loaded at runtime
const externals = ['@jupyter-widgets/base'];

const plugins = [
  new VueLoaderPlugin(),
];

const resolve = {
  // Add '.ts' and '.tsx' as resolvable extensions.
  extensions: [".webpack.js", ".web.js", ".ts", ".js"],
};

const isHotUpdate = /\.hot-update\.(js|json|js\.map)$/;

const notebookPath = "http://localhost:8889";

module.exports = [
  /**
   * Notebook extension for hot reloading
   */
  {
    entry: './src/extension.ts',
    output: {
      filename: 'nbextensions/flatsurf_widgets/index.js',
      libraryTarget: 'amd'
    },
    module: {
      rules: rules
    },
    devtool: 'source-map',
    externals,
    resolve,
    plugins,
    devServer: {
      port: 9000,
      hot: true,
      public: 'localhost:9000',
      index: '',
      sockPath: '/hot-node',
      proxy: {
	target: notebookPath,
	context: function(path) {
	  let ret = true;
	  if (path.match(/^\/hot-node\//)) {
	    // The dev server handles websocket connections to the hot-reloading machinery
	    ret = false;
	  } else if (path.match(/^\/nbextensions\/flatsurf_widgets\/index\.js/)) {
	    // The dev server handles this extension's bundle
	    ret = false;
	  } else if (path.match(isHotUpdate)) {
	    if (path.match(/.+\//)) {
	      // We proxy hot requests so we can fix their path (strip initial
              // path components such as /notebooks/examples)
	      ret = true;
	    } else {
	      // If the path is already stripped, we want to handle it from the dev server
	      ret = false;
	    }
	  }
	  return ret;
	},
	pathRewrite: function(path) {
	  let ret = path;
	  if (path.match(isHotUpdate)) {
	    ret =  path.replace(/.*\//, '/');
	  }
	  // console.log(`${path} -> ${ret}`);
	  return ret;
	},
	router: function(req) {
	  const path = req.url;
	  if (path.match(isHotUpdate)) {
	    return "http://localhost:9000";
	  } else {
	    return notebookPath;
	  }
	},
	ws: true,
      },
    }
  },
];
