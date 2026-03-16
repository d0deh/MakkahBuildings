"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { UploadZone } from "@/components/upload-zone";
import { LoadingState } from "@/components/loading-state";
import { uploadExcel } from "@/lib/api";

export default function HomePage() {
  const router = useRouter();
  const [file, setFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleAnalyze = async () => {
    if (!file) return;
    setIsUploading(true);
    setError(null);

    try {
      const result = await uploadExcel(file);
      router.push(`/dashboard/${result.session_id}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : "حدث خطأ غير متوقع");
      setIsUploading(false);
    }
  };

  if (isUploading) {
    return (
      <main className="min-h-screen flex items-center justify-center">
        <LoadingState message="جاري تحميل وتحليل البيانات..." />
      </main>
    );
  }

  return (
    <main className="min-h-screen flex items-center justify-center p-6">
      <div className="w-full max-w-2xl space-y-8">
        <div className="text-center space-y-2">
          <h1 className="text-[28px] font-bold text-foreground">
            مولد التقارير العمرانية
          </h1>
          <p className="text-sm text-muted-foreground">
            تحليل بيانات المسح العمراني وإنشاء التقارير تلقائياً
          </p>
        </div>

        <UploadZone onFileSelected={setFile} isLoading={isUploading} />

        {error && (
          <div className="bg-status-danger/10 border border-status-danger/20 text-status-danger rounded-lg p-4 text-center">
            {error}
          </div>
        )}

        <Button
          onClick={handleAnalyze}
          disabled={!file || isUploading}
          className="w-full bg-gold hover:bg-gold-dark text-background font-bold text-lg py-6 rounded-lg disabled:bg-muted disabled:text-muted-foreground disabled:opacity-100"
          size="lg"
        >
          تحليل البيانات
        </Button>
      </div>
    </main>
  );
}
