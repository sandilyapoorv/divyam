import React from 'react';
import Link from 'next/link';
import { 
  BarChart3, 
  ShieldCheck, 
  BookOpen, 
  ArrowRight, 
  FileText, 
  Target, 
  Sparkles, 
  Database,
  Layers
} from 'lucide-react';

export default function HomePage() {
  return (
    <div className="space-y-12 pb-12">
      {/* Hero Section */}
      <section className="relative overflow-hidden rounded-3xl bg-gradient-to-br from-mospi-900 via-mospi-800 to-slate-900 text-white p-8 sm:p-12 lg:p-16 shadow-2xl border border-slate-700/50">
        <div className="absolute top-0 right-0 -mt-10 -mr-10 w-96 h-96 bg-saffron-500/10 rounded-full blur-3xl pointer-events-none"></div>
        <div className="absolute bottom-0 left-0 -mb-10 -ml-10 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl pointer-events-none"></div>

        <div className="relative z-10 max-w-3xl space-y-6">
          <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-saffron-500/20 border border-saffron-500/40 text-saffron-300 text-xs font-semibold tracking-wide uppercase">
            <Sparkles className="w-3.5 h-3.5" />
            <span>SIH26101 &bull; Smart India Hackathon</span>
          </div>

          <h1 className="text-3xl sm:text-5xl font-extrabold tracking-tight leading-tight">
            Empowering India&apos;s Official Statistical System with <span className="text-transparent bg-clip-text bg-gradient-to-r from-saffron-400 via-amber-300 to-saffron-200">AI-Enabled FRAC Learning</span>
          </h1>

          <p className="text-slate-300 text-base sm:text-lg leading-relaxed">
            <strong>DIVYAM</strong> integrates the Government of India FRAC competency framework with the 
            <strong> iGOT Karmayogi</strong> ecosystem and RAG-driven Bloom&apos;s Taxonomy question generation 
            from MoSPI statistical manuals—accelerating capacity building across ISS &amp; SSS cadres.
          </p>

          <div className="flex flex-wrap gap-4 pt-4">
            <Link
              href="/dashboard"
              className="inline-flex items-center space-x-2 px-6 py-3.5 rounded-xl bg-gradient-to-r from-saffron-500 to-amber-500 hover:from-saffron-600 hover:to-amber-600 text-slate-950 font-bold text-sm shadow-lg hover:shadow-saffron-500/20 transition-all hover:scale-[1.02]"
            >
              <span>Cadre Officer Dashboard</span>
              <ArrowRight className="w-4 h-4" />
            </Link>

            <Link
              href="/diagnostic"
              className="inline-flex items-center space-x-2 px-6 py-3.5 rounded-xl bg-mospi-800/80 hover:bg-mospi-700/80 text-white font-semibold text-sm border border-slate-600 transition-all hover:scale-[1.02]"
            >
              <Target className="w-4 h-4 text-saffron-400" />
              <span>Take FRAC Diagnostic</span>
            </Link>

            <Link
              href="/admin"
              className="inline-flex items-center space-x-2 px-6 py-3.5 rounded-xl bg-slate-800/80 hover:bg-slate-700/80 text-white font-semibold text-sm border border-slate-700 transition-all"
            >
              <FileText className="w-4 h-4 text-blue-400" />
              <span>MoSPI Ingestion Studio</span>
            </Link>
          </div>
        </div>
      </section>

      {/* Core Architectural Pillars */}
      <section className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Pillar 1 */}
        <div className="bg-white rounded-2xl p-6 shadow-sm border border-slate-200 hover:border-saffron-400/60 transition-all group">
          <div className="w-12 h-12 rounded-xl bg-saffron-50 text-saffron-600 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
            <BarChart3 className="w-6 h-6" />
          </div>
          <h3 className="text-lg font-bold text-slate-900 mb-2">
            FRAC Competency Gap Radar
          </h3>
          <p className="text-sm text-slate-600 leading-relaxed">
            Evaluates officers across Domain, Functional, and Behavioural competencies (Levels 1–5). Computes mathematically rigorous Gap analysis and Departmental Readiness Index (&Omega;).
          </p>
          <div className="mt-4 pt-4 border-t border-slate-100 flex items-center justify-between text-xs font-medium text-slate-500">
            <span>Dynamic Multi-Axis Radar</span>
            <span className="text-saffron-600 font-semibold">Live Visuals</span>
          </div>
        </div>

        {/* Pillar 2 */}
        <div className="bg-white rounded-2xl p-6 shadow-sm border border-slate-200 hover:border-mospi-500/60 transition-all group">
          <div className="w-12 h-12 rounded-xl bg-blue-50 text-mospi-600 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
            <BookOpen className="w-6 h-6" />
          </div>
          <h3 className="text-lg font-bold text-slate-900 mb-2">
            iGOT Karmayogi Adapter
          </h3>
          <p className="text-sm text-slate-600 leading-relaxed">
            Automatically maps detected competency deficits to authentic MoSPI courses on Karmayogi Bharat, ranked by statutory criticality weights for immediate skill upliftment.
          </p>
          <div className="mt-4 pt-4 border-t border-slate-100 flex items-center justify-between text-xs font-medium text-slate-500">
            <span>DoPT / Karmayogi Schema</span>
            <span className="text-blue-600 font-semibold">Deficit-Matched</span>
          </div>
        </div>

        {/* Pillar 3 */}
        <div className="bg-white rounded-2xl p-6 shadow-sm border border-slate-200 hover:border-indiaGreen-500/60 transition-all group">
          <div className="w-12 h-12 rounded-xl bg-green-50 text-indiaGreen-600 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
            <FileText className="w-6 h-6" />
          </div>
          <h3 className="text-lg font-bold text-slate-900 mb-2">
            RAG Bloom&apos;s Quiz Generator
          </h3>
          <p className="text-sm text-slate-600 leading-relaxed">
            Ingests official MoSPI guidelines &amp; survey manuals (PLFS, CPI, SNA). Generates 4-tier Bloom&apos;s questions with 100% zero-hallucination exact page citations.
          </p>
          <div className="mt-4 pt-4 border-t border-slate-100 flex items-center justify-between text-xs font-medium text-slate-500">
            <span>ChromaDB Vector Store</span>
            <span className="text-indiaGreen-600 font-semibold">Exact Citations</span>
          </div>
        </div>
      </section>

      {/* Cadre Roles Covered */}
      <section className="bg-white rounded-2xl p-8 border border-slate-200 shadow-sm">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-6">
          <div>
            <h2 className="text-xl font-bold text-slate-900">
              National Statistical Cadres &amp; FRAC Benchmarks
            </h2>
            <p className="text-sm text-slate-600">
              Tailored competency targets designed for India&apos;s Central Statistical Apparatus
            </p>
          </div>
          <div className="inline-flex items-center space-x-1.5 px-3 py-1 rounded-md bg-slate-100 text-slate-700 text-xs font-medium">
            <Layers className="w-4 h-4 text-slate-500" />
            <span>MoSPI Cadre Hierarchy</span>
          </div>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="p-4 rounded-xl bg-slate-50 border border-slate-200/80">
            <span className="text-xs font-bold text-saffron-600 uppercase tracking-wider">ISS Cadre</span>
            <h4 className="font-semibold text-slate-800 text-sm mt-1">Director (National Accounts)</h4>
            <p className="text-xs text-slate-500 mt-1">Level 4/5 Mastery in SNA, Macro Modeling &amp; SUT</p>
          </div>
          <div className="p-4 rounded-xl bg-slate-50 border border-slate-200/80">
            <span className="text-xs font-bold text-saffron-600 uppercase tracking-wider">ISS Cadre</span>
            <h4 className="font-semibold text-slate-800 text-sm mt-1">Joint Director (Survey Sampling)</h4>
            <p className="text-xs text-slate-500 mt-1">Level 4 Mastery in Multistage Stratified Sampling</p>
          </div>
          <div className="p-4 rounded-xl bg-slate-50 border border-slate-200/80">
            <span className="text-xs font-bold text-blue-600 uppercase tracking-wider">SSS Cadre</span>
            <h4 className="font-semibold text-slate-800 text-sm mt-1">Senior Statistical Officer (SSO)</h4>
            <p className="text-xs text-slate-500 mt-1">Level 3 in CPI compilation, Data Verification &amp; CAPI</p>
          </div>
          <div className="p-4 rounded-xl bg-slate-50 border border-slate-200/80">
            <span className="text-xs font-bold text-blue-600 uppercase tracking-wider">SSS Cadre</span>
            <h4 className="font-semibold text-slate-800 text-sm mt-1">Junior Statistical Officer (JSO)</h4>
            <p className="text-xs text-slate-500 mt-1">Level 2 in Field Data Ingestion, Schedules &amp; Scrutiny</p>
          </div>
        </div>
      </section>
    </div>
  );
}
