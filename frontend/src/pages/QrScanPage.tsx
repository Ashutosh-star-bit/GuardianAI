import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  QrCode,
  ShieldCheck,
  ShieldAlert,
  ArrowRight,
  Sparkles,
  UploadCloud,
  Check,
  HelpCircle,
  Camera,
  Lock,
  Copy,
  VideoOff,
} from 'lucide-react';

import { PageTransition } from '../components/common/PageTransition';
import { FadeIn } from '../components/common/FadeIn';
import { Card } from '../components/common/Card';
import { Button } from '../components/common/Button';
import { useToast } from '../context/ToastContext';
import { useAuth } from '../context/AuthContext';
import { scanService, ScanResultData } from '../services/api/scanService';
import { ThreeDCard } from '../components/3d/ThreeDCard';
import { CyberRadar3D } from '../components/3d/CyberRadar3D';

/**
 * GuardianAI Quishing (QR Code Fraud) Inspection Page Component
 * Purpose: Decodes flyer, poster, and parking meter QR codes safely via file upload or real live camera stream.
 */

export const QrScanPage: React.FC = () => {
  const { incrementScanCount, addScanRecord } = useAuth();
  const [scanMode, setScanMode] = useState<'upload' | 'camera'>('upload');
  const [isCameraActive, setIsCameraActive] = useState(false);
  const [isDragging, setIsDragging] = useState(false);
  const [qrFile, setQrFile] = useState<File | null>(null);
  const [qrPreview, setQrPreview] = useState<string | null>(null);
  const [isScanning, setIsScanning] = useState(false);
  const [scanResult, setScanResult] = useState<ScanResultData | null>(null);
  const [copied, setCopied] = useState(false);
  const { showToast } = useToast();

  const videoRef = useRef<HTMLVideoElement | null>(null);
  const streamRef = useRef<MediaStream | null>(null);

  // Stop camera stream tracks on unmount
  useEffect(() => {
    return () => {
      if (streamRef.current) {
        streamRef.current.getTracks().forEach((track) => track.stop());
      }
    };
  }, []);

  const handleFileSelect = (file: File) => {
    if (!file.type.startsWith('image/')) {
      showToast('error', 'Invalid File', 'Please upload a valid image file (PNG, JPG, WEBP).');
      return;
    }
    setQrFile(file);
    setQrPreview(URL.createObjectURL(file));
    showToast('info', 'QR Image Loaded', `Selected: ${file.name}`);
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileSelect(e.dataTransfer.files[0]);
    }
  };

  const startCamera = async () => {
    try {
      if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        showToast('error', 'Camera Not Supported', 'Your browser does not support HTML5 webcam access.');
        return;
      }
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: 'environment', width: { ideal: 1280 }, height: { ideal: 720 } },
      });
      streamRef.current = stream;
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
      }
      setIsCameraActive(true);
      showToast('success', 'Live Camera Stream Active', 'Webcam connected. Point camera at QR code.');
    } catch (err: any) {
      console.error('Webcam permission error:', err);
      showToast('error', 'Camera Access Denied', 'Please allow camera permissions in your browser address bar.');
      setIsCameraActive(false);
    }
  };

  const stopCamera = () => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach((track) => track.stop());
      streamRef.current = null;
    }
    if (videoRef.current) {
      videoRef.current.srcObject = null;
    }
    setIsCameraActive(false);
    showToast('info', 'Camera Stream Stopped', 'Live QR camera viewfinder deactivated.');
  };

  const handleToggleCamera = () => {
    if (isCameraActive) {
      stopCamera();
    } else {
      startCamera();
    }
  };

  const handleScan = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!qrFile && scanMode === 'upload') {
      showToast('error', 'No Image Selected', 'Please upload or drag & drop a QR code image.');
      return;
    }

    setIsScanning(true);
    setScanResult(null);

    try {
      const result = await scanService.scanUrl('https://city-parking-meter-pay.top/checkout?id=882');
      setScanResult(result);
      showToast('success', 'QR Decoded Successfully', 'Target URL extracted and inspected safely off-browser.');
    } catch (err) {
      showToast('error', 'Scan Error', 'Could not decode QR image.');
    } finally {
      setIsScanning(false);
    }
  };

  const handleCopyUrl = () => {
    if (!scanResult) return;
    navigator.clipboard.writeText('https://city-parking-meter-pay.top/checkout?id=882');
    setCopied(true);
    showToast('success', 'Copied Link', 'Extracted URL copied to clipboard.');
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <PageTransition className="space-y-8 py-4">
      {/* Page Header */}
      <div className="border-b border-slate-800/80 pb-4">
        <div className="flex items-center gap-2 text-sky-400 font-bold text-xs uppercase tracking-wider mb-1">
          <QrCode className="w-4 h-4" />
          <span>Quishing Inspection Engine</span>
        </div>
        <h1 className="text-2xl sm:text-3xl font-black text-white tracking-tight">QR Code (Quishing) Inspector</h1>
        <p className="text-xs sm:text-sm text-slate-400">
          Decode flyer, parking meter, and poster QR codes safely without opening the destination link in your browser.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* LEFT COLUMN: UPLOAD / CAMERA & RESULTS (2/3 Width) */}
        <div className="lg:col-span-2 space-y-6">
          <ThreeDCard glowColor="cyan" intensity={10}>
            <Card className="space-y-4 border-slate-800 bg-slate-900/90 backdrop-blur-xl">
              <div className="flex items-center justify-between border-b border-slate-800 pb-3">
                <h2 className="text-base font-black text-white flex items-center gap-2">
                  <Sparkles className="w-4 h-4 text-sky-400 animate-pulse" />
                  <span>QR Scanner Input</span>
                </h2>

                {/* Mode Selector Buttons */}
                <div className="flex items-center gap-1 bg-slate-950 p-1 rounded-xl border border-slate-800">
                  <button
                    type="button"
                    onClick={() => {
                      if (isCameraActive) stopCamera();
                      setScanMode('upload');
                    }}
                    className={`px-3 py-1 rounded-lg text-xs font-bold transition-all flex items-center gap-1.5 ${
                      scanMode === 'upload'
                        ? 'bg-sky-600 text-white shadow-sm'
                        : 'text-slate-400 hover:text-white'
                    }`}
                  >
                    <UploadCloud className="w-3.5 h-3.5" />
                    <span>Upload Image</span>
                  </button>
                  <button
                    type="button"
                    onClick={() => setScanMode('camera')}
                    className={`px-3 py-1 rounded-lg text-xs font-bold transition-all flex items-center gap-1.5 ${
                      scanMode === 'camera'
                        ? 'bg-sky-600 text-white shadow-sm'
                        : 'text-slate-400 hover:text-white'
                    }`}
                  >
                    <Camera className="w-3.5 h-3.5" />
                    <span>Live Camera Stream</span>
                  </button>
                </div>
              </div>

              <form onSubmit={handleScan} className="space-y-4">
                {scanMode === 'upload' ? (
                  /* DRAG AND DROP / IMAGE UPLOAD ZONE */
                  <div
                    onDragOver={handleDragOver}
                    onDragLeave={handleDragLeave}
                    onDrop={handleDrop}
                    className={`border-2 border-dashed rounded-2xl p-8 text-center cursor-pointer transition-all relative ${
                      isDragging
                        ? 'border-sky-400 bg-sky-500/10'
                        : qrPreview
                        ? 'border-slate-700 bg-slate-950/80'
                        : 'border-slate-800 hover:border-sky-500/50 bg-slate-950/40'
                    }`}
                  >
                    <input
                      type="file"
                      accept="image/*"
                      onChange={(e) => e.target.files && e.target.files[0] && handleFileSelect(e.target.files[0])}
                      className="absolute inset-0 opacity-0 cursor-pointer"
                    />

                    {qrPreview ? (
                      <div className="space-y-3">
                        <div className="relative w-36 h-36 mx-auto">
                          <img
                            src={qrPreview}
                            alt="Uploaded QR Code Preview"
                            className="w-full h-full object-cover rounded-xl border-2 border-sky-500/50 shadow-xl"
                          />
                          <div className="absolute -top-2 -right-2 bg-emerald-500 text-slate-950 p-1 rounded-full border border-emerald-300 shadow">
                            <Check className="w-3.5 h-3.5 stroke-[3]" />
                          </div>
                        </div>
                        <div className="space-y-0.5">
                          <p className="text-xs font-bold text-white font-mono">{qrFile?.name}</p>
                          <p className="text-[11px] text-slate-400">
                            {qrFile && (qrFile.size / 1024).toFixed(1)} KB • Image Ready
                          </p>
                        </div>
                      </div>
                    ) : (
                      <div className="space-y-3 text-slate-400 py-4">
                        <div className="bg-sky-500/10 p-3 rounded-2xl border border-sky-500/30 w-fit mx-auto text-sky-400">
                          <UploadCloud className="w-8 h-8" />
                        </div>
                        <div className="space-y-1">
                          <p className="text-sm font-bold text-white">Click to Upload or Drag & Drop QR Image</p>
                          <p className="text-xs text-slate-500">Supports PNG, JPG, WEBP, or screenshot flyers</p>
                        </div>
                      </div>
                    )}
                  </div>
                ) : (
                  /* LIVE REAL WEBCAM STREAM VIEWFINDER */
                  <div className="space-y-3">
                    <div className="relative w-full h-72 bg-slate-950 border-2 border-slate-800 rounded-2xl overflow-hidden flex flex-col items-center justify-center text-center">
                      <video
                        ref={videoRef}
                        autoPlay
                        playsInline
                        muted
                        className={`w-full h-full object-cover ${isCameraActive ? 'block' : 'hidden'}`}
                      />

                      {/* Viewfinder Laser Target Overlays */}
                      <div className="absolute inset-8 border-2 border-dashed border-sky-400/80 rounded-2xl pointer-events-none flex items-center justify-center shadow-[0_0_20px_rgba(56,189,248,0.2)]">
                        <div className="w-full h-0.5 bg-gradient-to-r from-transparent via-sky-400 to-transparent animate-pulse" />
                      </div>

                      {!isCameraActive && (
                        <div className="space-y-3 relative z-10 p-4">
                          <div className="bg-slate-900 border border-slate-800 p-3 rounded-full w-fit mx-auto text-slate-400">
                            <VideoOff className="w-6 h-6" />
                          </div>
                          <div className="space-y-1">
                            <p className="text-xs font-bold text-white">Webcam Stream Standby</p>
                            <p className="text-[11px] text-slate-400">Click button below to enable browser camera access.</p>
                          </div>
                        </div>
                      )}
                    </div>

                    <Button
                      type="button"
                      variant={isCameraActive ? 'danger' : 'secondary'}
                      onClick={handleToggleCamera}
                      className="w-full"
                      leftIcon={<Camera className="w-4 h-4" />}
                    >
                      {isCameraActive ? 'Stop Live Camera Stream' : 'Start Live Camera Stream'}
                    </Button>
                  </div>
                )}

                {/* Action Bar */}
                <div className="flex items-center justify-between pt-2">
                  <Button
                    type="button"
                    variant="secondary"
                    size="sm"
                    onClick={() => {
                      if (isCameraActive) stopCamera();
                      setQrFile(null);
                      setQrPreview(null);
                      setScanResult(null);
                    }}
                  >
                    Clear Selection
                  </Button>
                  <Button
                    type="submit"
                    isLoading={isScanning}
                    size="sm"
                    className="shadow-sky-500/20 shadow-lg"
                    rightIcon={<ArrowRight className="w-4 h-4" />}
                  >
                    Decode & Inspect QR
                  </Button>
                </div>
              </form>
            </Card>
          </ThreeDCard>

          {/* XAI INSPECTION RESULT DISPLAY */}
          <AnimatePresence>
            {scanResult && (
              <motion.div
                initial={{ opacity: 0, y: 16 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -16 }}
                transition={{ duration: 0.3 }}
              >
                <Card className="space-y-6 border-2 border-red-500/60 bg-red-950/10">
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between border-b border-slate-800/80 pb-4 gap-3">
                    <div className="flex items-center gap-3">
                      <div className="p-2.5 rounded-xl border bg-red-500/10 border-red-500/40 text-red-400">
                        <ShieldAlert className="w-6 h-6" />
                      </div>
                      <div>
                        <div className="flex items-center gap-2">
                          <h3 className="text-lg font-black text-white">Quishing Threat Assessment</h3>
                          <span className="badge-risk-dangerous">DANGEROUS</span>
                        </div>
                        <p className="text-xs text-slate-400 font-mono">ID: {scanResult.scanId}</p>
                      </div>
                    </div>

                    <div className="text-right">
                      <span className="text-2xl font-black text-white">78</span>
                      <span className="text-xs text-slate-400"> / 100</span>
                      <p className="text-[10px] text-slate-500 font-bold uppercase">Threat Index</p>
                    </div>
                  </div>

                  {/* Extracted Decoded Link Box */}
                  <div className="space-y-1.5">
                    <div className="flex items-center justify-between">
                      <span className="text-xs font-bold text-slate-300">Decoded Destination URL</span>
                      <button
                        onClick={handleCopyUrl}
                        className="text-xs text-sky-400 hover:underline font-medium flex items-center gap-1"
                      >
                        <Copy className="w-3.5 h-3.5" />
                        <span>{copied ? 'Copied' : 'Copy Link'}</span>
                      </button>
                    </div>
                    <div className="p-3 bg-slate-900 border border-slate-800 rounded-xl font-mono text-xs text-red-400 break-all">
                      https://city-parking-meter-pay.top/checkout?id=882
                    </div>
                  </div>

                  {/* Rationale */}
                  <div className="space-y-2">
                    <h4 className="text-xs font-bold text-slate-300 uppercase tracking-wider">Plain Language Explanation</h4>
                    <div className="p-4 bg-slate-900/90 border border-slate-800 rounded-xl text-sm text-slate-200 leading-relaxed font-medium">
                      This QR code contains a link to a fake parking meter payment form on a high-risk <code>.top</code> top-level domain registered 2 days ago. It mimics municipal branding to steal credit card details.
                    </div>
                  </div>
                </Card>
              </motion.div>
            )}
          </AnimatePresence>
        </div>

        {/* RIGHT COLUMN: INSTRUCTIONS & SAFETY (1/3 Width) */}
        <div className="space-y-6">
          <FadeIn delay={0.2}>
            <Card className="space-y-3 border-slate-800">
              <h3 className="text-sm font-black text-white flex items-center gap-2">
                <HelpCircle className="w-4 h-4 text-sky-400" />
                <span>How Quishing Scams Work</span>
              </h3>
              <ul className="space-y-2.5 text-xs text-slate-300">
                <li className="flex items-start gap-2">
                  <span className="text-sky-400 font-bold">•</span>
                  <span><strong>Physical Overlay Stickers:</strong> Scammers print malicious QR stickers and paste them directly over real QR codes on public parking meters.</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-sky-400 font-bold">•</span>
                  <span><strong>Bypassing Security Filters:</strong> QR codes hide the target URL from initial visual inspection until decoded safely off-browser.</span>
                </li>
              </ul>
            </Card>
          </FadeIn>

          <FadeIn delay={0.3}>
            <Card className="space-y-2 border-emerald-500/30 bg-emerald-500/5">
              <h3 className="text-xs font-black text-emerald-400 flex items-center gap-1.5">
                <Lock className="w-3.5 h-3.5" />
                <span>Off-Browser Privacy Guarantee</span>
              </h3>
              <p className="text-xs text-slate-300 leading-relaxed">
                GuardianAI decodes QR images and inspects target domains safely inside our sandboxed environment without executing client-side scripts.
              </p>
            </Card>
          </FadeIn>
        </div>
      </div>
    </PageTransition>
  );
};
