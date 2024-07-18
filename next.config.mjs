/** @type {import('next').NextConfig} */
const nextConfig = {};

export default {
  ...nextConfig,
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'https://face-recognition-server-jade.vercel.app/:path*', // Ensure this points to your Flask server
      },
    ];
  },
};
