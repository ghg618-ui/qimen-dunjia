import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
    title: '奇门遁甲 | 元始版 - 智能云端推演系统',
    description: '专业的奇门遁甲云端排盘与大数据解析平台',
}

export default function RootLayout({
    children,
}: {
    children: React.ReactNode
}) {
    return (
        <html lang="zh-CN">
            <body>{children}</body>
        </html>
    )
}
