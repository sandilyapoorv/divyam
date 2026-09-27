'use client';

import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { 
  BarChart3, 
  BookOpen, 
  Award, 
  ShieldCheck, 
  FileText, 
  User as UserIcon,
  Sparkles
} from 'lucide-react';

export default function Navbar() {
  const pathname = usePathname();

  const navLinks = [
    { href: '/dashboard', label: 'Cadre Dashboard', icon: BarChart3 },
    { href: '/diagnostic', label: 'FRAC Diagnostic', icon: ShieldCheck },
    { href: '/assessment/demo', label: 'Bloom\'s Assessment', icon: Award },
    { href: '/admin', label: 'MoSPI Admin Studio', icon: FileText },
  ];

  return (
    <header className="bg-mospi-900 text-white shadow-lg sticky top-0 z-50">
      {/* Top Tiranga Accent Line */}
      <div className="h-1 w-full flex">
        <div className="h-full w-1/3 bg-saffron-500"></div>
        <div className="h-full w-1/3 bg-white"></div>
        <div className="h-full w-1/3 bg-indiaGreen-500"></div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Brand Logo & Title */}
          <div className="flex items-center space-x-3">
            <Link href="/" className="flex items-center space-x-3 group">
              <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-saffron-500 to-amber-600 flex items-center justify-center font-bold text-white shadow-md group-hover:scale-105 transition-transform">
                <span className="text-xl tracking-tighter">दि</span>
              </div>
              <div>
                <div className="flex items-center space-x-2">
                  <span className="font-extrabold text-xl tracking-tight text-white">DIVYAM</span>
                  <span className="text-[10px] font-semibold tracking-wider uppercase px-1.5 py-0.5 rounded bg-saffron-500/20 text-saffron-400 border border-saffron-500/30">
                    SIH26101
                  </span>
                </div>
                <p className="text-xs text-slate-300 tracking-wide font-normal">
                  MoSPI Statistical Capacity Building &bull; iGOT Karmayogi
                </p>
              </div>
            </Link>
          </div>

          {/* Desktop Navigation Links */}
          <nav className="hidden md:flex items-center space-x-1">
            {navLinks.map((link) => {
              const Icon = link.icon;
              const isActive = pathname.startsWith(link.href) && link.href !== '/';
              return (
                <Link
                  key={link.href}
                  href={link.href}
                  className={`flex items-center space-x-2 px-3.5 py-2 rounded-md text-sm font-medium transition-colors ${
                    isActive
                      ? 'bg-mospi-800 text-white border-b-2 border-saffron-500'
                      : 'text-slate-200 hover:bg-mospi-800/60 hover:text-white'
                  }`}
                >
                  <Icon className="w-4 h-4 text-saffron-400" />
                  <span>{link.label}</span>
                </Link>
              );
            })}
          </nav>

          {/* User Profile Pill */}
          <div className="flex items-center space-x-3">
            <div className="hidden lg:flex flex-col text-right">
              <span className="text-xs font-semibold text-white">Dr. Rajesh Sharma, ISS</span>
              <span className="text-[11px] text-slate-300">Director, National Accounts</span>
            </div>
            <div className="w-9 h-9 rounded-full bg-slate-800 border-2 border-saffron-500 flex items-center justify-center text-white shadow-inner">
              <UserIcon className="w-5 h-5 text-saffron-400" />
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}
