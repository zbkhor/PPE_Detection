const BundleTracker = require('webpack-bundle-tracker');

module.exports = {
    publicPath: '',
    outputDir: './dist/',
    chainWebpack: config => {
        config.optimization.splitChunks(false);

        config
            .plugin('BundleTracker')
            .use(BundleTracker, [
                { filename: '../frontend_visitor/webpack-stats-visitor.json' }
            ]);

        config.resolve.alias.set('__STATIC__', 'static');

        config.devServer
            .public('static/')
            .host('127.0.0.1')
            .port(8081)
            .hotOnly(true)
            .watchOptions({ poll: 1000 })
            .https(false)
            .headers({ 'Access-Control-Allow-Origin': ['*'] });
    },
    transpileDependencies: ['vuetify']
};
