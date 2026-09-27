'use client';

import React from 'react';
import { ExternalLink, Clock, Award, Shield, CheckCircle } from 'lucide-react';
import { RecommendationItem } from '@/lib/api-client';

interface IgotCourseCardProps {
  recommendation: RecommendationItem;
}

export default function IgotCourseCard({ recommendation }: IgotCourseCardProps) {
  const { course, competency_name, gap, priority_level } = recommendation;

  const priorityStyles: Record<string, { bg: string; text: string; border: string }> = {
    HIGH: { bg: 'bg-red-50', text: 'text-red-700', border: 'border-red-200' },
    MEDIUM: { bg: 'bg-amber-50', text: 'text-amber-700', border: 'border-amber-200' },
    LOW: { bg: 'bg-blue-50', text: 'text-blue-700', border: 'border-blue-200' },
  };

  const currentPriorityStyle = priorityStyles[priority_level] || priorityStyles.MEDIUM;

  return (
    <div className="bg-white rounded-2xl p-5 border border-slate-200 shadow-sm hover:shadow-md hover:border-mospi-500/50 transition-all flex flex-col justify-between group">
      <div>
        {/* Top Badges */}
        <div className="flex items-center justify-between gap-2 mb-3">
          <span
            className={`text-[11px] font-bold px-2.5 py-0.5 rounded-full border ${currentPriorityStyle.bg} ${currentPriorityStyle.text} ${currentPriorityStyle.border}`}
          >
            {priority_level} PRIORITY GAP
          </span>
          <div className="flex items-center space-x-1 text-slate-500 text-xs">
            <Clock className="w-3.5 h-3.5 text-slate-400" />
            <span>{course.duration_hours} hrs</span>
          </div>
        </div>

        {/* Course Title */}
        <h4 className="font-bold text-slate-900 text-base leading-snug group-hover:text-mospi-700 transition-colors">
          {course.title}
        </h4>

        {/* Competency Gap Resolution Badge */}
        <div className="mt-2.5 p-2 rounded-lg bg-slate-50 border border-slate-200/70 text-xs text-slate-600 space-y-1">
          <div className="flex items-center justify-between font-medium">
            <span className="text-slate-700">Target Competency:</span>
            <span className="text-red-600 font-semibold">Deficit: -{gap} Level</span>
          </div>
          <p className="font-semibold text-mospi-900 truncate">
            {competency_name}
          </p>
        </div>

        {/* Course Description */}
        <p className="mt-3 text-xs text-slate-500 line-clamp-2 leading-relaxed">
          {course.description}
        </p>
      </div>

      {/* Footer Info & Karmayogi Direct Action */}
      <div className="mt-5 pt-4 border-t border-slate-100 flex items-center justify-between gap-3">
        <div>
          <span className="text-[11px] text-slate-400 block">Accreditation</span>
          <span className="text-xs font-semibold text-slate-700 flex items-center space-x-1">
            <Shield className="w-3.5 h-3.5 text-saffron-500" />
            <span className="truncate max-w-[150px]">{course.provider}</span>
          </span>
        </div>

        <a
          href={course.course_url}
          target="_blank"
          rel="noopener noreferrer"
          className="inline-flex items-center space-x-1.5 px-3.5 py-2 rounded-xl bg-mospi-900 hover:bg-mospi-800 text-white text-xs font-semibold shadow-sm transition-all hover:scale-[1.02]"
        >
          <span>Enroll on iGOT</span>
          <ExternalLink className="w-3.5 h-3.5 text-saffron-400" />
        </a>
      </div>
    </div>
  );
}
