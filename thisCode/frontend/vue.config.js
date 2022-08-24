const BundleTracker = require('webpack-bundle-tracker');

module.exports = {
    publicPath: '',
    outputDir: './dist/',
    chainWebpack: (config) => {
        config.optimization.splitChunks(false);

        config
            .plugin('BundleTracker')
            .use(BundleTracker, [
                { filename: '../frontend/webpack-stats.json' },
            ]);

        config.resolve.alias.set('__STATIC__', 'static');

        config.devServer
            .public('static/')
            .host('127.0.0.1')
            .port(8080)
            .hotOnly(true)
            .watchOptions({ poll: 1000 })
            .https(false)
            .headers({ 'Access-Control-Allow-Origin': ['*'] });

        config.module
            .rule('pdf')
            .test(/\.pdf$/)
            .use('file-loader')
            .loader('file-loader')
            .options({
                name: '[name].[ext]',
            });
    },
    transpileDependencies: ['vuetify'],
    devServer: {
        proxy: 'http://127.0.0.1:8000',
    },
};
