/** @type {import('next').NextConfig} */
const nextConfig = {};

export default {
  ...nextConfig,
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://localhost:5000/:path*', // Ensure this points to your Flask server
      },
    ];
  },
};