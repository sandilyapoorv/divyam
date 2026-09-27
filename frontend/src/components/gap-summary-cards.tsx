'use client';

import React from 'react';
import { ShieldCheck, AlertTriangle, TrendingUp, CheckCircle2, Layers } from 'lucide-react';
import { GapAnalysisResponse } from '@/lib/api-client';

interface GapSummaryCardsProps {
  gapData: GapAnalysisResponse;
}

export default function GapSummaryCards({ gapData }: GapSummaryCardsProps) {
  const readinessPct = Math.round(gapData.readiness_index * 100);
  const totalCompetencies = gapData.gaps.length;
  const deficitCount = gapData.gaps.filter((g) => g.gap > 0).length;
  const masteredCount = totalCompetencies - deficitCount;
  
  // Top priority competency
  const topPriority = gapData.gaps.length > 0 ? gapData.gaps[0] : null;

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      {/* Card 1: Readiness Index */}
      <div className="bg-white rounded-2xl p-5 border border-slate-200 shadow-sm relative overflow-hidden">
        <div className="flex items-center justify-between">
          <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">
            FRAC Readiness Index (&Omega;)
          </span>
          <div className={`p-2 rounded-xl ${
            readinessPct >= 80 
              ? 'bg-green-50 text-indiaGreen-600' 
              : readinessPct >= 60 
              ? 'bg-amber-50 text-amber-600' 
              : 'bg-red-50 text-red-600'
          }`}>
            <TrendingUp className="w-4 h-4" />
          </div>
        </div>
        <div className="mt-3 flex items-baseline space-x-2">
          <span className="text-3xl font-extrabold text-slate-900">{readinessPct}%</span>
          <span className="text-xs text-slate-500 font-medium">of Role Target</span>
        </div>
        <div className="mt-3 w-full bg-slate-100 rounded-full h-2 overflow-hidden">
          <div
            className={`h-full rounded-full transition-all duration-500 ${
              readinessPct >= 80 ? 'bg-indiaGreen-500' : readinessPct >= 60 ? 'bg-saffron-500' : 'bg-red-500'
            }`}
            style={{ width: `${Math.min(100, readinessPct)}%` }}
          />
        </div>
      </div>

      {/* Card 2: Competency Deficits */}
      <div className="bg-white rounded-2xl p-5 border border-slate-200 shadow-sm">
        <div className="flex items-center justify-between">
          <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">
            Competency Deficits
          </span>
          <div className="p-2 rounded-xl bg-amber-50 text-amber-600">
            <AlertTriangle className="w-4 h-4" />
          </div>
        </div>
        <div className="mt-3 flex items-baseline space-x-2">
          <span className="text-3xl font-extrabold text-slate-900">{deficitCount}</span>
          <span className="text-xs text-slate-500 font-medium">active gaps to close</span>
        </div>
        <p className="mt-3 text-xs text-slate-500 flex items-center space-x-1">
          <span>{masteredCount} of {totalCompetencies} targets currently satisfied</span>
        </p>
      </div>

      {/* Card 3: Top Priority Skill */}
      <div className="bg-white rounded-2xl p-5 border border-slate-200 shadow-sm">
        <div className="flex items-center justify-between">
          <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">
            Highest Priority Deficit
          </span>
          <div className="p-2 rounded-xl bg-blue-50 text-mospi-600">
            <ShieldCheck className="w-4 h-4" />
          </div>
        </div>
        <div className="mt-3">
          <p className="text-sm font-bold text-slate-900 truncate" title={topPriority?.competency_name || 'None'}>
            {topPriority?.competency_name || 'All Targets Met'}
          </p>
          <div className="flex items-center space-x-2 mt-1">
            <span className="text-xs text-red-600 font-semibold">
              Gap: -{topPriority?.gap || 0} Levels
            </span>
            <span className="text-xs text-slate-400">&bull;</span>
            <span className="text-[11px] font-medium text-slate-500 uppercase">
              {topPriority?.competency_type || 'Domain'}
            </span>
          </div>
        </div>
      </div>

      {/* Card 4: Cadre Benchmark Status */}
      <div className="bg-white rounded-2xl p-5 border border-slate-200 shadow-sm">
        <div className="flex items-center justify-between">
          <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">
            FRAC Framework
          </span>
          <div className="p-2 rounded-xl bg-purple-50 text-purple-600">
            <Layers className="w-4 h-4" />
          </div>
        </div>
        <div className="mt-3 flex items-baseline space-x-2">
          <span className="text-2xl font-bold text-slate-900">Level 1 - 5</span>
          <span className="text-xs text-slate-500 font-medium">Standard</span>
        </div>
        <p className="mt-3 text-xs text-slate-500">
          MoSPI Official Cadre Standard (ISS &amp; SSS)
        </p>
      </div>
    </div>
  );
}
