'use client';

import React from 'react';
import Link from 'next/link';
import { ArrowLeft, Clock, Sparkles } from 'lucide-react';

interface ComingSoonProps {
  title: string;
  description: string;
  expectedLaunch?: string;
  features?: string[];
  icon?: React.ReactNode;
}

export default function ComingSoon({
  title,
  description,
  expectedLaunch = 'November 2025',
  features = [],
  icon
}: ComingSoonProps) {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800 flex items-center justify-center px-4">
      <div className="max-w-2xl w-full">
        {/* Card */}
        <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8 md:p-12">
          {/* Icon */}
          <div className="flex justify-center mb-6">
            <div className="w-20 h-20 bg-blue-100 dark:bg-blue-900/30 rounded-full flex items-center justify-center">
              {icon || <Sparkles className="w-10 h-10 text-blue-600 dark:text-blue-400" />}
            </div>
          </div>

          {/* Title */}
          <h1 className="text-3xl md:text-4xl font-bold text-center text-gray-900 dark:text-white mb-4">
            {title}
          </h1>

          {/* Description */}
          <p className="text-lg text-center text-gray-600 dark:text-gray-400 mb-8">
            {description}
          </p>

          {/* Expected Launch */}
          <div className="flex items-center justify-center gap-2 mb-8">
            <Clock className="w-5 h-5 text-blue-600 dark:text-blue-400" />
            <span className="text-sm font-medium text-blue-600 dark:text-blue-400">
              Expected Launch: {expectedLaunch}
            </span>
          </div>

          {/* Features (if provided) */}
          {features.length > 0 && (
            <div className="mb-8">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4 text-center">
                Planned Features
              </h3>
              <ul className="space-y-2">
                {features.map((feature, index) => (
                  <li
                    key={index}
                    className="flex items-start gap-2 text-gray-700 dark:text-gray-300"
                  >
                    <span className="text-blue-600 dark:text-blue-400 mt-1">✓</span>
                    <span>{feature}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Status Badge */}
          <div className="flex justify-center mb-8">
            <span className="px-4 py-2 bg-yellow-100 dark:bg-yellow-900/30 text-yellow-800 dark:text-yellow-300 rounded-full text-sm font-medium">
              🚧 Under Active Development
            </span>
          </div>

          {/* Back Button */}
          <div className="flex justify-center">
            <Link
              href="/"
              className="inline-flex items-center gap-2 px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-colors"
            >
              <ArrowLeft className="w-4 h-4" />
              Back to Home
            </Link>
          </div>
        </div>

        {/* Footer Note */}
        <p className="text-center text-sm text-gray-500 dark:text-gray-400 mt-6">
          Want to be notified when this feature launches? Stay tuned for updates!
        </p>
      </div>
    </div>
  );
}
