import type { Metadata } from 'next';
import './globals.css';
import Navbar from '@/components/navbar';

export const metadata: Metadata = {
  title: 'DIVYAM | AI-Enabled Capacity Building for Official Statistical System',
  description: 'SIH26101 - FRAC Competency Gap Analysis, iGOT Karmayogi Integration & RAG-Powered Bloom\'s Assessment Generator for MoSPI, Indian Statistical Service (ISS) & Subordinate Statistical Service (SSS).',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="h-full">
      <body className="h-full flex flex-col antialiased bg-slate-50 text-slate-900 font-sans">
        <Navbar />
        <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {children}
        </main>
        <footer className="bg-slate-900 text-slate-400 py-6 border-t border-slate-800 text-xs">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row justify-between items-center gap-4">
            <div className="flex items-center space-x-2">
              <span className="font-bold text-white tracking-wide">DIVYAM</span>
              <span>&bull;</span>
              <span>Smart India Hackathon 2024 (Problem Statement SIH26101)</span>
            </div>
            <div>
              Ministry of Statistics & Programme Implementation (MoSPI) &bull; Karmayogi Bharat Aligned
            </div>
          </div>
        </footer>
      </body>
    </html>
  );
}
