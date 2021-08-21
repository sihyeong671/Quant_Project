const webpack = require('webpack');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const ForkTsCheckerWebpackPlugin = require('fork-ts-checker-webpack-plugin');

const port = 3000;

module.exports = {
    mode: 'development',
    entry: [
        'babel-polyfill',
        // './src/index.tsx',
        './src/index.jsx'
    ],
    output: {
        path: __dirname + '/build',
        filename: 'app.js',
        publicPath: '/'
    },
    resolve: {
        alias: {
            components: __dirname + 'src/components'
        },
        extensions: ['.js', '.jsx', '.tsx'],
    },
    module: {
        rules: [
            // { // BABEL LOADER
            //     test: /\.(js)$/,
            //     exclude: /node_modules/,
            //     use: ['babel-loader']
            // },
            { // BABEL & TS LOADER
                test: /\.(ts|tsx|js|jsx)$/,
                use: [
                    'babel-loader',
                    {
                        loader: 'ts-loader',
                        options: {
                            transpileOnly: true,
                        },
                    },
                ],
                exclude: /node_modules/,
            },
            { // CSS LOADER
                test: /\.(css|scss)$/,
                // use: ['style-loader', 'css-loader'],
                use: [
                    MiniCssExtractPlugin.loader, 
                    'css-loader',
                    'sass-loader'  
                ],
            },
            { // URL LOADER
                test: /\.(ico|png|jpg|jpeg|gif|svg|woff|woff2|ttf|eot)?$/,
                loader: 'url-loader',
                options: {
                    name: 'src/[name].[ext]',
                    fallback: 'file-loader',
                    limit: 10000,
                },
            }
        ]
    },
    plugins: [
        new webpack.HotModuleReplacementPlugin(),
        new MiniCssExtractPlugin({
            filename: 'app.css'
        }),
        new HtmlWebpackPlugin({
            template: 'public/index.html',
        }),
        new ForkTsCheckerWebpackPlugin({}),
    ],
    devServer: {
        host: 'localhost',
        port: port,
        open: true,
        historyApiFallback: true,
        hot: true
    }
};