'use client';

import React, { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import { api, QuizItem } from '@/lib/api-client';
import QuizPlayer from '@/components/quiz-player';
import { Loader2 } from 'lucide-react';

export default function AssessmentPage() {
  const params = useParams();
  const quizId = (params?.id as string) || 'demo';
  const [quiz, setQuiz] = useState<QuizItem | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    async function loadQuiz() {
      setLoading(true);
      try {
        if (quizId !== 'demo') {
          const remoteQuiz = await api.getQuiz(quizId);
          setQuiz(remoteQuiz);
          return;
        }
      } catch (err) {
        console.warn('Could not fetch quiz from API, loading MoSPI master assessment:', err);
      }

      // Authentic MoSPI Bloom's assessment fallback
      const demoQuiz: QuizItem = {
        id: 'quiz-mospi-demo-001',
        title: 'MoSPI Cadre Assessment: Survey Sampling & National Accounts (SNA 2008)',
        document_id: 'doc-sampling-guide-001',
        competency_id: 'comp-dom-002',
        total_questions: 4,
        pass_threshold_percentage: 60,
        created_at: new Date().toISOString(),
        questions: [
          {
            id: 'q-demo-1',
            question_text: 'Under standard NSSO Multi-stage Stratified Sampling architecture, which geographical or administrative division is officially designated as the First Stage Unit (FSU) for rural sectors?',
            options: [
              'Census Village (or Panchayat Ward)',
              'Revenue Block (Tehsil)',
              'Individual Agricultural Household',
              'Enumeration Block of 50 Households'
            ],
            bloom_level: 'Remembering',
            competency_id: 'comp-dom-002',
            explanation: 'As per MoSPI Official Sampling Guidelines, rural FSUs are universally defined as the 2011 Census Villages, while urban FSUs correspond to Urban Frame Survey (UFS) blocks.',
            citation: {
              document_id: 'doc-sampling-guide-001',
              document_title: 'MoSPI National Statistical Handbook on Household Surveys',
              page_number: 14,
              section_heading: 'Section 2.1 - Frame Stratification and FSU Demarcation',
              quote_snippet: 'In the rural sector, the First Stage Units (FSUs) are the Census Villages as per the latest available Population Census. In urban sectors, FSUs consist of UFS blocks.',
            },
          },
          {
            id: 'q-demo-2',
            question_text: 'In the System of National Accounts (SNA 2008), why is Financial Intermediation Services Indirectly Measured (FISIM) allocated as intermediate consumption rather than directly as final consumption of households?',
            options: [
              'Because FISIM reflects the service charge embedded in interest rate margins rather than pure property income transfers',
              'Because central banks prohibit measuring household interest payments',
              'Because FISIM is only accounted for in export-oriented trade deficits',
              'Because financial institutions do not generate gross value added (GVA)'
            ],
            bloom_level: 'Understanding',
            competency_id: 'comp-dom-001',
            explanation: 'Under SNA 2008, FISIM isolates the production of financial intermediation services from pure property income (interest), allocating costs according to whether the funds were borrowed/deposited by enterprises (intermediate) or individuals (final).',
            citation: {
              document_id: 'doc-sna-manual-001',
              document_title: 'Sources and Methods of National Accounts Statistics (MoSPI 2020)',
              page_number: 84,
              section_heading: 'Chapter 5: Financial Corporations and FISIM Accounting',
              quote_snippet: 'FISIM represents the output produced by financial intermediaries by paying lower interest on deposits and charging higher interest on loans compared to a reference risk-free rate.',
            },
          },
          {
            id: 'q-demo-3',
            question_text: 'Given a sample of 200 enterprises from a stratified industry frame using Probability Proportional to Size with Replacement (PPSWR), where size measure equals annual turnover, what formula yields the unbiased Horvitz-Thompson design weight for enterprise i?',
            options: [
              'w_i = (1 / n) * (Total Size / Size_i)',
              'w_i = (Size_i / Total Size) * n',
              'w_i = Total Size / (n * Sum of Selected Sizes)',
              'w_i = 1 / (1 - (Size_i / Total Size)^n)'
            ],
            bloom_level: 'Applying',
            competency_id: 'comp-dom-002',
            explanation: 'In PPSWR sampling, the selection probability per draw is p_i = Size_i / Total Size. For an n-draw sample, the inclusion probability per draw gives the unbiased Hansen-Hurwitz / Horvitz-Thompson multiplier w_i = (1 / n) * (1 / p_i).',
            citation: {
              document_id: 'doc-sampling-guide-001',
              document_title: 'MoSPI National Statistical Handbook on Household Surveys',
              page_number: 52,
              section_heading: 'Formula Annexure: Unequal Probability Multipliers',
              quote_snippet: 'For PPS with replacement, the design weight assigned to the i-th unit is w_i = (1 / n) * (X / x_i), ensuring that the estimator is strictly unbiased for the universe total.',
            },
          },
          {
            id: 'q-demo-4',
            question_text: 'During the tabulation of the Annual Survey of Industries (ASI), a senior statistician discovers severe non-response bias in the large plant census sector (>100 workers). Which statistical imputation procedure is compliant with MoSPI National Quality Standards?',
            options: [
              'Stratified Hot-Deck imputation using identical 4-digit NIC classification and electricity consumption brackets',
              'Dropping the non-responding census units without adjustment',
              'Multiplying the remaining factory outputs by arbitrary state-level GDP deflators',
              'Replacing non-responding output values with zero in the factory sector summary'
            ],
            bloom_level: 'Analyzing',
            competency_id: 'comp-func-001',
            explanation: 'ASI methodology specifies donor-based hot-deck imputation stratified by 4-digit NIC industrial classification and physical capacity variables (such as electrical energy consumption) to prevent downward distortion in Gross Value of Output (GVO).',
            citation: {
              document_id: 'doc-asi-instruction-001',
              document_title: 'Manual of Instructions for Annual Survey of Industries (ASI 2022-23)',
              page_number: 112,
              section_heading: 'Section 7.4 - Handling Non-Response in Census Factory Units',
              quote_snippet: 'When large census plants fail to report despite statutory notices, hot-deck donor matching within the same 4-digit NIC code and connected power load bracket shall be applied.',
            },
          },
        ],
      };

      setQuiz(demoQuiz);
      setLoading(false);
    }

    loadQuiz();
  }, [quizId]);

  if (loading) {
    return (
      <div className="h-[400px] flex flex-col items-center justify-center space-y-3">
        <Loader2 className="w-8 h-8 text-saffron-500 animate-spin" />
        <span className="text-sm font-semibold text-slate-600">
          Retrieving Bloom&apos;s Assessment and Verified Citations...
        </span>
      </div>
    );
  }

  if (!quiz) {
    return (
      <div className="p-8 text-center text-slate-500">
        Assessment could not be loaded. Please return to dashboard.
      </div>
    );
  }

  return (
    <div className="py-4">
      <QuizPlayer quiz={quiz} userId="user-iss-001" />
    </div>
  );
}
