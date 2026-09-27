'use client';

import React, { useEffect, useState } from 'react';
import {
  Radar,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  ResponsiveContainer,
  Legend,
  Tooltip,
} from 'recharts';
import { RadarDataPoint } from '@/lib/api-client';

interface CompetencyRadarProps {
  data: RadarDataPoint[];
}

export default function CompetencyRadar({ data }: CompetencyRadarProps) {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) {
    return (
      <div className="h-[380px] w-full flex items-center justify-center bg-slate-50/50 rounded-2xl animate-pulse">
        <span className="text-sm text-slate-400 font-medium">Loading FRAC Radar Visualizer...</span>
      </div>
    );
  }

  if (!data || data.length === 0) {
    return (
      <div className="h-[380px] w-full flex items-center justify-center bg-slate-50 rounded-2xl border border-dashed border-slate-300">
        <span className="text-sm text-slate-400">No competency data available for radar mapping.</span>
      </div>
    );
  }

  return (
    <div className="w-full h-[400px]">
      <ResponsiveContainer width="100%" height="100%">
        <RadarChart cx="50%" cy="50%" outerRadius="75%" data={data}>
          <PolarGrid stroke="#cbd5e1" strokeDasharray="3 3" />
          <PolarAngleAxis
            dataKey="subject"
            tick={{ fill: '#334155', fontSize: 12, fontWeight: 500 }}
          />
          <PolarRadiusAxis angle={30} domain={[0, 5]} tick={{ fill: '#64748b', fontSize: 10 }} />
          
          <Tooltip
            content={({ active, payload }) => {
              if (active && payload && payload.length) {
                const item = payload[0].payload as RadarDataPoint;
                const gap = Math.max(0, item.target - item.current);
                return (
                  <div className="bg-slate-900 text-white p-3 rounded-xl shadow-xl text-xs space-y-1 border border-slate-700">
                    <p className="font-bold text-saffron-400 text-sm">{item.subject}</p>
                    <p className="text-slate-300">Target Benchmark: <span className="font-semibold text-white">{item.target} / 5</span></p>
                    <p className="text-slate-300">Assessed Level: <span className="font-semibold text-white">{item.current} / 5</span></p>
                    <p className="pt-1 border-t border-slate-800 text-amber-300 font-medium">
                      Deficit Gap: <span className={gap > 0 ? "text-red-400 font-bold" : "text-green-400 font-bold"}>{gap > 0 ? `-${gap} Level` : 'Target Achieved'}</span>
                    </p>
                  </div>
                );
              }
              return null;
            }}
          />

          <Legend 
            wrapperStyle={{ paddingTop: '10px' }}
            formatter={(value) => <span className="text-xs font-semibold text-slate-700">{value}</span>}
          />

          {/* Benchmark Target (Saffron Outline) */}
          <Radar
            name="Target Benchmark (FRAC)"
            dataKey="target"
            stroke="#ff9933"
            strokeWidth={2.5}
            fill="#ff9933"
            fillOpacity={0.15}
          />

          {/* Assessed Score (MoSPI Navy Solid Fill) */}
          <Radar
            name="Officer Assessed Score"
            dataKey="current"
            stroke="#0f2b5c"
            strokeWidth={2.5}
            fill="#0f2b5c"
            fillOpacity={0.4}
          />
        </RadarChart>
      </ResponsiveContainer>
    </div>
  );
}
