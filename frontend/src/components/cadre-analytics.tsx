'use client';

import React from 'react';
import { 
  Users, 
  TrendingUp, 
  Building2, 
  CheckCircle2, 
  AlertTriangle,
  ArrowUpRight,
  ShieldCheck
} from 'lucide-react';

export default function CadreAnalytics() {
  const divisions = [
    {
      name: 'National Accounts Division (NAD)',
      code: 'NAD',
      officers: 112,
      currentAvg: 3.4,
      targetAvg: 4.8,
      readiness: 71,
      topDeficit: 'SNA 2008 & Supply-Use Tables',
    },
    {
      name: 'Field Operations Division (FOD / NSSO)',
      code: 'FOD',
      officers: 215,
      currentAvg: 2.9,
      targetAvg: 4.0,
      readiness: 73,
      topDeficit: 'Multistage Stratified Sampling & CAPI',
    },
    {
      name: 'Price Statistics Division (PSD - CPI/IIP)',
      code: 'PSD',
      officers: 78,
      currentAvg: 3.5,
      targetAvg: 4.2,
      readiness: 83,
      topDeficit: 'Geometric Aggregation & Substitution Bias',
    },
    {
      name: 'Economic Statistics Division (ESD - ASI)',
      code: 'ESD',
      officers: 95,
      currentAvg: 3.2,
      targetAvg: 4.1,
      readiness: 78,
      topDeficit: 'Factory Census Non-Response Imputation',
    },
  ];

  return (
    <div className="space-y-6">
      {/* Top Ministry KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-white rounded-2xl p-5 border border-slate-200 shadow-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-500 uppercase">
              Total Cadre Officers
            </span>
            <div className="p-2 rounded-xl bg-blue-50 text-mospi-600">
              <Users className="w-4 h-4" />
            </div>
          </div>
          <div className="mt-3 flex items-baseline space-x-2">
            <span className="text-3xl font-extrabold text-slate-900">500</span>
            <span className="text-xs text-slate-500">ISS &amp; SSS Cadres</span>
          </div>
          <p className="mt-2 text-xs text-slate-500">100% mapped to FRAC Framework</p>
        </div>

        <div className="bg-white rounded-2xl p-5 border border-slate-200 shadow-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-500 uppercase">
              Ministry Readiness Index
            </span>
            <div className="p-2 rounded-xl bg-green-50 text-indiaGreen-600">
              <TrendingUp className="w-4 h-4" />
            </div>
          </div>
          <div className="mt-3 flex items-baseline space-x-2">
            <span className="text-3xl font-extrabold text-slate-900">76.3%</span>
            <span className="text-xs text-indiaGreen-600 font-bold">+5.2% MoM</span>
          </div>
          <p className="mt-2 text-xs text-slate-500">Target Benchmark: 85% by Q4</p>
        </div>

        <div className="bg-white rounded-2xl p-5 border border-slate-200 shadow-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-500 uppercase">
              iGOT Course Enrolments
            </span>
            <div className="p-2 rounded-xl bg-purple-50 text-purple-600">
              <ShieldCheck className="w-4 h-4" />
            </div>
          </div>
          <div className="mt-3 flex items-baseline space-x-2">
            <span className="text-3xl font-extrabold text-slate-900">1,240</span>
            <span className="text-xs text-slate-500">Active Lessons</span>
          </div>
          <p className="mt-2 text-xs text-slate-500">Deficit-driven automated allocations</p>
        </div>

        <div className="bg-white rounded-2xl p-5 border border-slate-200 shadow-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-500 uppercase">
              Bloom&apos;s Quizzes Taken
            </span>
            <div className="p-2 rounded-xl bg-amber-50 text-amber-600">
              <CheckCircle2 className="w-4 h-4" />
            </div>
          </div>
          <div className="mt-3 flex items-baseline space-x-2">
            <span className="text-3xl font-extrabold text-slate-900">3,890</span>
            <span className="text-xs text-slate-500">Assessments</span>
          </div>
          <p className="mt-2 text-xs text-slate-500">100% cited from MoSPI manuals</p>
        </div>
      </div>

      {/* Divisional Breakdown Table */}
      <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm">
        <h3 className="text-base font-bold text-slate-900 mb-1">
          MoSPI Operational Division Readiness &amp; Gap Matrix
        </h3>
        <p className="text-xs text-slate-500 mb-4">
          Tracking capability benchmarks across key central statistical directorates.
        </p>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-slate-200 text-slate-500 font-semibold uppercase">
                <th className="pb-3">Directorate / Division</th>
                <th className="pb-3 text-center">Cadre Strength</th>
                <th className="pb-3 text-center">Assessed vs Target</th>
                <th className="pb-3">Readiness Index (&Omega;)</th>
                <th className="pb-3">Key Deficit Area</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {divisions.map((div) => (
                <tr key={div.code} className="hover:bg-slate-50/70">
                  <td className="py-4 font-bold text-slate-800">
                    <div>{div.name}</div>
                    <span className="text-[10px] font-semibold text-slate-400 font-mono">
                      Division ID: {div.code}
                    </span>
                  </td>
                  <td className="py-4 text-center font-semibold text-slate-700">
                    {div.officers} Officers
                  </td>
                  <td className="py-4 text-center font-bold text-mospi-900">
                    L{div.currentAvg} / L{div.targetAvg}
                  </td>
                  <td className="py-4 w-48">
                    <div className="flex items-center space-x-2">
                      <span className="font-extrabold text-slate-900 text-xs w-8">{div.readiness}%</span>
                      <div className="flex-1 bg-slate-100 rounded-full h-2">
                        <div
                          className={`h-full rounded-full ${
                            div.readiness >= 80 ? 'bg-indiaGreen-500' : 'bg-saffron-500'
                          }`}
                          style={{ width: `${div.readiness}%` }}
                        />
                      </div>
                    </div>
                  </td>
                  <td className="py-4">
                    <span className="px-2 py-1 rounded bg-red-50 text-red-700 font-medium text-[11px] border border-red-200">
                      {div.topDeficit}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
