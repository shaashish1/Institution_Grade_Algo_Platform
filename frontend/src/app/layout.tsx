import { Inter } from 'next/font/google'
import { Providers } from '@/components/providers'
import { MegaMenu } from '@/components/layout/mega-menu'
import '@/styles/globals.css'
import { Metadata } from 'next'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'AlgoProject - Advanced Trading Platform',
  description: 'Professional algorithmic trading platform for crypto and stocks',
  keywords: 'trading, crypto, stocks, algorithms, portfolio, investment',
  authors: [{ name: 'AlgoProject Team' }],
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className={inter.className}>
      <body className="antialiased bg-slate-950 text-white">
        <Providers>
          <MegaMenu />
          {children}
        </Providers>
      </body>
    </html>
  )
}