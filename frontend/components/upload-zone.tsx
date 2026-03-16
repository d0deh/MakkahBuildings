"use client";

import { useCallback, useState } from "react";

interface UploadZoneProps {
  onFileSelected: (file: File) => void;
  isLoading: boolean;
}

export function UploadZone({ onFileSelected, isLoading }: UploadZoneProps) {
  const [isDragOver, setIsDragOver] = useState(false);
  const [fileName, setFileName] = useState<string | null>(null);

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault();
      setIsDragOver(false);
      const file = e.dataTransfer.files[0];
      if (file && (file.name.endsWith(".xlsx") || file.name.endsWith(".xls"))) {
        setFileName(file.name);
        onFileSelected(file);
      }
    },
    [onFileSelected]
  );

  const handleFileInput = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      const file = e.target.files?.[0];
      if (file) {
        setFileName(file.name);
        onFileSelected(file);
      }
    },
    [onFileSelected]
  );

  return (
    <div
      className={`border rounded-lg p-12 text-center transition-colors cursor-pointer ${
        isDragOver
          ? "border-gold bg-gold/5"
          : "border-[hsl(var(--border))] hover:border-gold/50"
      } bg-[hsl(var(--surface))] ${isLoading ? "opacity-50 pointer-events-none" : ""}`}
      onDragOver={(e) => {
        e.preventDefault();
        setIsDragOver(true);
      }}
      onDragLeave={() => setIsDragOver(false)}
      onDrop={handleDrop}
      onClick={() => document.getElementById("file-input")?.click()}
    >
      <input
        id="file-input"
        type="file"
        accept=".xlsx,.xls"
        className="hidden"
        onChange={handleFileInput}
      />
      <div className="flex flex-col items-center gap-4">
        <div className="w-16 h-16 rounded-full bg-[hsl(var(--muted))] flex items-center justify-center">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className="h-8 w-8 text-muted-foreground"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
            />
          </svg>
        </div>
        {fileName ? (
          <p className="text-lg font-bold text-foreground">{fileName}</p>
        ) : (
          <>
            <p className="text-lg text-muted-foreground">
              اسحب ملف Excel هنا أو انقر للاختيار
            </p>
            <p className="text-sm text-[hsl(var(--text-muted))]">.xlsx أو .xls</p>
          </>
        )}
      </div>
    </div>
  );
}
