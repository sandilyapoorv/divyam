'use client';

import React, { useState } from 'react';
import { BookOpen, ChevronDown, ChevronUp, ShieldCheck, FileText } from 'lucide-react';
import { QuestionCitation } from '@/lib/api-client';

interface CitationViewerProps {
  citation?: QuestionCitation;
}

export default function CitationViewer({ citation }: CitationViewerProps) {
  const [isOpen, setIsOpen] = useState(false);

  if (!citation) {
    return null;
  }

  return (
    <div className="rounded-xl border border-indigo-100 bg-indigo-50/50 overflow-hidden text-xs">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="w-full px-4 py-2.5 flex items-center justify-between text-left hover:bg-indigo-100/50 transition-colors"
      >
        <div className="flex items-center space-x-2">
          <ShieldCheck className="w-4 h-4 text-indigo-600 flex-shrink-0" />
          <span className="font-bold text-indigo-950">
            Source Grounding: {citation.document_title} (Page {citation.page_number})
          </span>
          <span className="hidden sm:inline text-[10px] font-semibold px-2 py-0.5 rounded bg-indigo-200/60 text-indigo-800">
            Zero-Hallucination
          </span>
        </div>
        <div className="flex items-center space-x-1 text-indigo-700 font-semibold">
          <span>{isOpen ? 'Hide Citation' : 'Inspect Source Citation'}</span>
          {isOpen ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
        </div>
      </button>

      {isOpen && (
        <div className="p-4 pt-2 border-t border-indigo-100 space-y-2 bg-white/90">
          <div className="flex items-center justify-between text-slate-500 text-[11px]">
            <span className="font-semibold text-slate-700">
              Official MoSPI Publication: <span className="text-indigo-900">{citation.document_title}</span>
            </span>
            <span className="bg-slate-100 px-2 py-0.5 rounded font-mono font-bold text-slate-800">
              Page {citation.page_number}
            </span>
          </div>

          {citation.section_heading && (
            <p className="text-[11px] font-semibold text-slate-600">
              Section: {citation.section_heading}
            </p>
          )}

          {citation.quote_snippet && (
            <div className="p-3 rounded-lg bg-slate-50 border-l-4 border-indigo-500 font-mono text-[11px] text-slate-700 leading-relaxed italic">
              &ldquo;{citation.quote_snippet}&rdquo;
            </div>
          )}

          <p className="text-[10px] text-slate-400 italic">
            Exact grounding verified by DRIVYAM RAG Engine against MoSPI Official Statistical Manuals.
          </p>
        </div>
      )}
    </div>
  );
}
