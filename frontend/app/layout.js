import './globals.css'

export const metadata = {
  title: 'XHS Workflow Review Console',
  description: 'AI content workflow review console for Xiaohongshu',
}

export default function RootLayout({ children }) {
  return (
    <html lang="zh-CN">
      <body>{children}</body>
    </html>
  )
}
