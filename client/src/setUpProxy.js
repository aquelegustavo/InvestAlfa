const { createProxyMiddleware } = require("http-proxy-middleware");

console.log(process.env.NODE_ENV);

if (process.env.NODE_ENV == "development") {
  module.exports = function (app) {
    app.use(
      "/api",
      createProxyMiddleware({
        target: process.env.PROXY_TARGET,
        changeOrigin: true,
      })
    );
  };
}
