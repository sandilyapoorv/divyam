'use client';

import React, { useState, useEffect } from 'react';
import { 
  api, 
  DocumentItem, 
  QuizItem 
} from '@/lib/api-client';
import DocumentUploader from '@/components/document-uploader';
import QuestionCurator from '@/components/question-curator';
import CadreAnalytics from '@/components/cadre-analytics';
import { 
  FileText, 
  Sparkles, 
  BarChart3, 
  ShieldCheck, 
  BookOpen, 
  CheckCircle2, 
  Clock, 
  Database 
} from 'lucide-react';

export default function AdminStudioPage() {
  const [activeTab, setActiveTab] = useState<'upload' | 'curate' | 'analytics'>('upload');
  const [documents, setDocuments] = useState<DocumentItem[]>([]);
  const [quizzes, setQuizzes] = useState<QuizItem[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  const loadData = async () => {
    setLoading(true);
    try {
      const [docs, qList] = await Promise.all([
        api.getDocuments(),
        api.getQuizzes(),
      ]);
      setDocuments(docs);
      setQuizzes(qList);
    } catch (err) {
      console.warn('Backend fetch error, using default MoSPI manual library:', err);
      // Demo library
      const fallbackDocs: DocumentItem[] = [
        {
          id: 'doc-sampling-guide-001',
          title: 'MoSPI National Statistical Handbook on Household Surveys',
          file_name: 'mospi_sampling_handbook_2023.pdf',
          file_type: 'pdf',
          file_size_bytes: 4820000,
          description: 'Official methodology for multistage stratified sampling, FSU frames, and design weights.',
          competency_id: 'comp-dom-002',
          is_indexed: true,
          total_chunks: 148,
          created_at: new Date().toISOString(),
        },
        {
          id: 'doc-sna-manual-001',
          title: 'Sources and Methods of National Accounts Statistics (MoSPI 2020)',
          file_name: 'sources_and_methods_sna_2020.pdf',
          file_type: 'pdf',
          file_size_bytes: 9240000,
          description: 'Guidelines on GDP compilation, FISIM allocation, and Supply-Use Tables under SNA 2008.',
          competency_id: 'comp-dom-001',
          is_indexed: true,
          total_chunks: 312,
          created_at: new Date().toISOString(),
        },
        {
          id: 'doc-asi-instruction-001',
          title: 'Manual of Instructions for Annual Survey of Industries (ASI 2022-23)',
          file_name: 'asi_manual_instructions_2022.pdf',
          file_type: 'pdf',
          file_size_bytes: 3100000,
          description: 'Field scrutiny, census sector validation, and non-response handling instructions.',
          competency_id: 'comp-func-001',
          is_indexed: true,
          total_chunks: 96,
          created_at: new Date().toISOString(),
        },
      ];
      setDocuments(fallbackDocs);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleDocumentAdded = (newDoc: DocumentItem) => {
    setDocuments((prev) => [newDoc, ...prev]);
  };

  const handleQuizPublished = (newQuiz: QuizItem) => {
    setQuizzes((prev) => [newQuiz, ...prev]);
  };

  return (
    <div className="space-y-8 pb-12">
      {/* Studio Header */}
      <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2">
            <span className="text-xs font-bold text-saffron-600 uppercase tracking-wider">
              MoSPI Administrator &amp; Trainer Portal
            </span>
            <span className="text-slate-300">&bull;</span>
            <span className="text-xs text-slate-500">Official Cadre Studio</span>
          </div>
          <h1 className="text-xl font-extrabold text-slate-900 mt-1">
            Statistical Guidelines Ingestion &amp; Assessment Studio
          </h1>
        </div>

        {/* Tab Navigation */}
        <div className="flex items-center space-x-1 bg-slate-100 p-1 rounded-xl text-xs font-semibold">
          <button
            onClick={() => setActiveTab('upload')}
            className={`flex items-center space-x-1.5 px-3.5 py-2 rounded-lg transition-all ${
              activeTab === 'upload'
                ? 'bg-white text-mospi-900 shadow-sm font-bold'
                : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            <FileText className="w-4 h-4 text-mospi-700" />
            <span>Document Ingestion</span>
          </button>

          <button
            onClick={() => setActiveTab('curate')}
            className={`flex items-center space-x-1.5 px-3.5 py-2 rounded-lg transition-all ${
              activeTab === 'curate'
                ? 'bg-white text-mospi-900 shadow-sm font-bold'
                : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            <Sparkles className="w-4 h-4 text-saffron-500" />
            <span>Bloom&apos;s Generator</span>
          </button>

          <button
            onClick={() => setActiveTab('analytics')}
            className={`flex items-center space-x-1.5 px-3.5 py-2 rounded-lg transition-all ${
              activeTab === 'analytics'
                ? 'bg-white text-mospi-900 shadow-sm font-bold'
                : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            <BarChart3 className="w-4 h-4 text-indiaGreen-600" />
            <span>Cadre Analytics</span>
          </button>
        </div>
      </div>

      {/* Tab 1: Ingestion & Document Repository */}
      {activeTab === 'upload' && (
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          <div className="lg:col-span-5">
            <DocumentUploader onUploadSuccess={handleDocumentAdded} />
          </div>

          <div className="lg:col-span-7 space-y-4">
            <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm">
              <div className="flex items-center justify-between mb-4">
                <div>
                  <h3 className="text-base font-bold text-slate-900">
                    Indexed MoSPI Statistical Manuals ({documents.length})
                  </h3>
                  <p className="text-xs text-slate-500">
                    Chunked, embedded, and stored in local ChromaDB for semantic retrieval.
                  </p>
                </div>
                <div className="flex items-center space-x-1 px-2.5 py-1 rounded bg-green-50 text-indiaGreen-700 text-xs font-semibold">
                  <Database className="w-3.5 h-3.5" />
                  <span>ChromaDB Active</span>
                </div>
              </div>

              <div className="divide-y divide-slate-100">
                {documents.map((doc) => (
                  <div key={doc.id} className="py-4 space-y-2">
                    <div className="flex items-start justify-between">
                      <div className="space-y-1">
                        <h4 className="font-bold text-slate-900 text-sm">
                          {doc.title}
                        </h4>
                        <p className="text-xs text-slate-500">
                          {doc.description || 'Official guidelines for Indian statistical capacity building.'}
                        </p>
                      </div>
                      <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-green-100 text-indiaGreen-800 flex-shrink-0">
                        Indexed
                      </span>
                    </div>

                    <div className="flex items-center space-x-4 text-[11px] text-slate-500 font-medium">
                      <span>File: <strong className="text-slate-700">{doc.file_name}</strong></span>
                      <span>&bull;</span>
                      <span>Chunks: <strong className="text-mospi-800">{doc.total_chunks} Vectors</strong></span>
                      <span>&bull;</span>
                      <span>Size: {Math.round(doc.file_size_bytes / 1024)} KB</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Tab 2: Bloom's Question Generation & Question Bank */}
      {activeTab === 'curate' && (
        <div className="space-y-6">
          <QuestionCurator documents={documents} onQuizPublished={handleQuizPublished} />
        </div>
      )}

      {/* Tab 3: Cadre-wide Readiness Analytics */}
      {activeTab === 'analytics' && (
        <CadreAnalytics />
      )}
    </div>
  );
}
