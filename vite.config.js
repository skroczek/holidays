import { defineConfig } from 'vite'
import tailwindcss from '@tailwindcss/vite'
import { createHtmlPlugin } from 'vite-plugin-html';

export default defineConfig({
    base: './',
    plugins: [
        tailwindcss(),
        createHtmlPlugin({
            inject: {
                data: {
                    buildYear: `${new Date().getFullYear()}`
                }
            }
        })
    ],
});