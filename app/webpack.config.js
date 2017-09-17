var webpack = require("webpack");

module.exports = {
  entry: [
    'webpack-dev-server/client?http://localhost:8080',
    'webpack/hot/only-dev-server',
    './js/index.js'
  ],
  plugins: [
    new webpack.ProvidePlugin ({
      ReactDOM: 'react-dom',
      React: 'react',
      $: 'jquery',
      jQuery: 'jquery'
    })
  ],
  module: {
    loaders: [{
      test: /\.jsx?$/,
      exclude: /node_modules/,
      loader: 'react-hot-loader!babel-loader'
      //loader: 'babel-loader'
    }]
  },
  resolve: {
    extensions: ['*', '.js', '.jsx'],
    modules: ["./node_modules"]
  },
  output: {
    path: __dirname + '/static',
    publicPath: '/',
    filename: 'bundle.js'
  },
  devServer: {
    contentBase: './static',
    hot:true
  }
};
