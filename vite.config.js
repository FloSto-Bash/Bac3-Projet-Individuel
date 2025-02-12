import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

// source : https://github.com/sveltejs/kit/issues/11293

function crossOriginIsolationMiddleware(_, response, next) {
    response.setHeader('Cross-Origin-Opener-Policy', 'same-origin');
	response.setHeader('Cross-Origin-Embedder-Policy', 'require-corp');
	response.setHeader('Cross-Origin-Resource-Policy', 'cross-origin');
	response.setHeader('Access-Control-Allow-Origin', '*');
    next();
}

const crossOriginIsolation = {
    name: 'cross-origin-isolation',
    configureServer: server => { server.middlewares.use(crossOriginIsolationMiddleware); },
    configurePreviewServer: server => { server.middlewares.use(crossOriginIsolationMiddleware); },
};

/** @type {import('vite').UserConfig} */
export default defineConfig({
	plugins: [
		sveltekit(), 
		crossOriginIsolation
	]
});