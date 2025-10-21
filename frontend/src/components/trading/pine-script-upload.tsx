'use client';

import React, { useState, useRef, useCallback } from 'react';
import { 
  Upload, FileCode, CheckCircle, AlertCircle, X, Eye, 
  Download, Play, Settings, Code, Zap, Brain
} from 'lucide-react';

interface PineScriptFile {
  id: string;
  name: string;
  content: string;
  size: number;
  uploadDate: Date;
  status: 'uploading' | 'validating' | 'valid' | 'invalid' | 'deployed';
  errors?: string[];
  metadata?: {
    version?: string;
    title?: string;
    description?: string;
    author?: string;
    timeframe?: string;
    indicators?: string[];
  };
}

interface PineScriptUploadProps {
  onFileUpload?: (file: PineScriptFile) => void;
  onFileDelete?: (id: string) => void;
  onFileValidate?: (id: string) => void;
  onFileDeploy?: (id: string) => void;
}

export function PineScriptUpload({
  onFileUpload,
  onFileDelete,
  onFileValidate,
  onFileDeploy
}: PineScriptUploadProps) {
  const [files, setFiles] = useState<PineScriptFile[]>([]);
  const [isDragging, setIsDragging] = useState(false);
  const [uploadProgress, setUploadProgress] = useState<{ [key: string]: number }>({});
  const fileInputRef = useRef<HTMLInputElement>(null);

  const validatePineScript = (content: string): { isValid: boolean; errors: string[]; metadata: any } => {
    const errors: string[] = [];
    const metadata: any = {};

    // Basic Pine Script validation
    if (!content.includes('//@version=')) {
      errors.push('Missing @version directive');
    }

    if (!content.includes('study(') && !content.includes('strategy(') && !content.includes('indicator(')) {
      errors.push('Missing study(), strategy(), or indicator() declaration');
    }

    // Extract metadata
    const versionMatch = content.match(/\/\/@version=(\d+)/);
    if (versionMatch) {
      metadata.version = versionMatch[1];
    }

    const titleMatch = content.match(/(?:study|strategy|indicator)\s*\(\s*["']([^"']+)["']/);
    if (titleMatch) {
      metadata.title = titleMatch[1];
    }

    // Check for common indicators
    const indicators = [];
    if (content.includes('sma(')) indicators.push('SMA');
    if (content.includes('ema(')) indicators.push('EMA');
    if (content.includes('rsi(')) indicators.push('RSI');
    if (content.includes('macd(')) indicators.push('MACD');
    if (content.includes('stoch(')) indicators.push('Stochastic');
    if (content.includes('bb(')) indicators.push('Bollinger Bands');
    
    metadata.indicators = indicators;

    return {
      isValid: errors.length === 0,
      errors,
      metadata
    };
  };

  const handleFileUpload = useCallback(async (uploadedFiles: FileList) => {
    const newFiles: PineScriptFile[] = [];

    for (let i = 0; i < uploadedFiles.length; i++) {
      const file = uploadedFiles[i];
      
      // Validate file type
      if (!file.name.endsWith('.pine') && !file.name.endsWith('.pinescript') && !file.name.endsWith('.txt')) {
        alert(`Invalid file type: ${file.name}. Please upload .pine, .pinescript, or .txt files.`);
        continue;
      }

      const fileId = Date.now().toString() + i;
      const content = await file.text();
      
      const newFile: PineScriptFile = {
        id: fileId,
        name: file.name,
        content,
        size: file.size,
        uploadDate: new Date(),
        status: 'uploading'
      };

      newFiles.push(newFile);
      setUploadProgress(prev => ({ ...prev, [fileId]: 0 }));

      // Simulate upload progress
      const progressInterval = setInterval(() => {
        setUploadProgress(prev => {
          const currentProgress = prev[fileId] || 0;
          if (currentProgress >= 100) {
            clearInterval(progressInterval);
            return prev;
          }
          return { ...prev, [fileId]: currentProgress + 10 };
        });
      }, 100);

      // Validate after upload simulation
      setTimeout(() => {
        const validation = validatePineScript(content);
        newFile.status = validation.isValid ? 'valid' : 'invalid';
        newFile.errors = validation.errors;
        newFile.metadata = validation.metadata;
        
        setFiles(prev => [...prev.filter(f => f.id !== fileId), newFile]);
        
        if (onFileUpload) {
          onFileUpload(newFile);
        }
      }, 1500);
    }

    setFiles(prev => [...prev, ...newFiles]);
  }, [onFileUpload]);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    
    const droppedFiles = e.dataTransfer.files;
    handleFileUpload(droppedFiles);
  }, [handleFileUpload]);

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
  }, []);

  const handleFileSelect = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFiles = e.target.files;
    if (selectedFiles) {
      handleFileUpload(selectedFiles);
    }
  }, [handleFileUpload]);

  const handleDeleteFile = (id: string) => {
    setFiles(prev => prev.filter(f => f.id !== id));
    setUploadProgress(prev => {
      const newProgress = { ...prev };
      delete newProgress[id];
      return newProgress;
    });
    
    if (onFileDelete) {
      onFileDelete(id);
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'uploading':
      case 'validating':
        return <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-blue-400" />;
      case 'valid':
        return <CheckCircle className="h-5 w-5 text-green-400" />;
      case 'invalid':
        return <AlertCircle className="h-5 w-5 text-red-400" />;
      case 'deployed':
        return <Zap className="h-5 w-5 text-yellow-400" />;
      default:
        return <FileCode className="h-5 w-5 text-slate-400" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'valid':
        return 'text-green-400 bg-green-400/10';
      case 'invalid':
        return 'text-red-400 bg-red-400/10';
      case 'deployed':
        return 'text-yellow-400 bg-yellow-400/10';
      default:
        return 'text-blue-400 bg-blue-400/10';
    }
  };

  return (
    <div className="space-y-6">
      {/* Upload Area */}
      <div
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        className={`
          relative border-2 border-dashed rounded-xl p-8 text-center transition-all duration-200
          ${isDragging 
            ? 'border-blue-400 bg-blue-500/10' 
            : 'border-slate-600 hover:border-slate-500'
          }
        `}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept=".pine,.pinescript,.txt"
          multiple
          onChange={handleFileSelect}
          className="hidden"
        />
        
        <div className="space-y-4">
          <div className="flex justify-center">
            <Upload className={`h-12 w-12 ${isDragging ? 'text-blue-400' : 'text-slate-400'}`} />
          </div>
          
          <div>
            <h3 className="text-lg font-medium text-white mb-2">Upload Pine Script Files</h3>
            <p className="text-slate-400 mb-4">
              Drag and drop your .pine, .pinescript, or .txt files here, or click to browse
            </p>
          </div>
          
          <button
            onClick={() => fileInputRef.current?.click()}
            className="px-6 py-3 bg-blue-500 hover:bg-blue-600 text-white rounded-lg transition-colors"
          >
            Choose Files
          </button>
          
          <div className="text-sm text-slate-500">
            Supported formats: .pine, .pinescript, .txt
          </div>
        </div>
      </div>

      {/* Uploaded Files List */}
      {files.length > 0 && (
        <div className="space-y-4">
          <h3 className="text-lg font-semibold text-white">Uploaded Pine Scripts</h3>
          
          {files.map((file) => (
            <div key={file.id} className="bg-slate-800 rounded-lg p-4 border border-slate-700">
              <div className="flex items-start justify-between mb-3">
                <div className="flex items-center space-x-3">
                  {getStatusIcon(file.status)}
                  <div>
                    <h4 className="font-medium text-white">{file.name}</h4>
                    <div className="flex items-center space-x-4 text-sm text-slate-400">
                      <span>{(file.size / 1024).toFixed(1)} KB</span>
                      <span>{file.uploadDate.toLocaleDateString()}</span>
                      <span className={`px-2 py-1 rounded text-xs ${getStatusColor(file.status)}`}>
                        {file.status}
                      </span>
                    </div>
                  </div>
                </div>
                
                <div className="flex items-center space-x-2">
                  <button
                    onClick={() => {/* View file logic */}}
                    className="p-2 text-slate-400 hover:text-white transition-colors"
                    title="View file"
                  >
                    <Eye className="h-4 w-4" />
                  </button>
                  
                  {file.status === 'valid' && (
                    <button
                      onClick={() => onFileDeploy?.(file.id)}
                      className="p-2 text-green-400 hover:text-green-300 transition-colors"
                      title="Deploy strategy"
                    >
                      <Play className="h-4 w-4" />
                    </button>
                  )}
                  
                  <button
                    onClick={() => handleDeleteFile(file.id)}
                    className="p-2 text-red-400 hover:text-red-300 transition-colors"
                    title="Delete file"
                  >
                    <X className="h-4 w-4" />
                  </button>
                </div>
              </div>

              {/* Upload Progress */}
              {file.status === 'uploading' && uploadProgress[file.id] !== undefined && (
                <div className="mb-3">
                  <div className="flex justify-between text-sm text-slate-400 mb-1">
                    <span>Uploading...</span>
                    <span>{uploadProgress[file.id]}%</span>
                  </div>
                  <div className="w-full bg-slate-700 rounded-full h-2">
                    <div 
                      className="bg-blue-500 h-2 rounded-full transition-all duration-200"
                      style={{ width: `${uploadProgress[file.id]}%` }}
                    />
                  </div>
                </div>
              )}

              {/* File Metadata */}
              {file.metadata && (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-3">
                  {file.metadata.title && (
                    <div>
                      <span className="text-sm text-slate-400">Title:</span>
                      <span className="ml-2 text-sm text-white">{file.metadata.title}</span>
                    </div>
                  )}
                  {file.metadata.version && (
                    <div>
                      <span className="text-sm text-slate-400">Version:</span>
                      <span className="ml-2 text-sm text-white">v{file.metadata.version}</span>
                    </div>
                  )}
                  {file.metadata.indicators && file.metadata.indicators.length > 0 && (
                    <div className="md:col-span-2">
                      <span className="text-sm text-slate-400">Indicators:</span>
                      <div className="flex flex-wrap gap-1 mt-1">
                        {file.metadata.indicators.map((indicator, index) => (
                          <span key={index} className="px-2 py-1 bg-blue-500/20 text-blue-400 text-xs rounded">
                            {indicator}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}

              {/* Validation Errors */}
              {file.errors && file.errors.length > 0 && (
                <div className="bg-red-500/10 border border-red-500/20 rounded p-3">
                  <div className="flex items-center space-x-2 mb-2">
                    <AlertCircle className="h-4 w-4 text-red-400" />
                    <span className="text-sm font-medium text-red-400">Validation Errors:</span>
                  </div>
                  <ul className="text-sm text-red-300 space-y-1">
                    {file.errors.map((error, index) => (
                      <li key={index} className="flex items-center space-x-2">
                        <span className="w-1 h-1 bg-red-400 rounded-full"></span>
                        <span>{error}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      {/* Quick Actions */}
      <div className="bg-slate-800 rounded-lg p-4 border border-slate-700">
        <h4 className="font-medium text-white mb-3">Quick Actions</h4>
        <div className="flex flex-wrap gap-3">
          <button className="px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-lg text-sm transition-colors">
            <Code className="h-4 w-4 inline mr-2" />
            Create New Script
          </button>
          <button className="px-4 py-2 bg-purple-500 hover:bg-purple-600 text-white rounded-lg text-sm transition-colors">
            <Brain className="h-4 w-4 inline mr-2" />
            AI Script Generator
          </button>
          <button className="px-4 py-2 bg-green-500 hover:bg-green-600 text-white rounded-lg text-sm transition-colors">
            <Download className="h-4 w-4 inline mr-2" />
            Download Templates
          </button>
          <button className="px-4 py-2 bg-slate-600 hover:bg-slate-500 text-white rounded-lg text-sm transition-colors">
            <Settings className="h-4 w-4 inline mr-2" />
            Upload Settings
          </button>
        </div>
      </div>
    </div>
  );
}