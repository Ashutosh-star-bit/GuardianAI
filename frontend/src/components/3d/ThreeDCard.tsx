import React, { useState } from 'react';

interface ThreeDCardProps {
  children: React.ReactNode;
  className?: string;
  intensity?: number;
  glowColor?: 'cyan' | 'purple' | 'emerald' | 'amber';
}

export const ThreeDCard: React.FC<ThreeDCardProps> = ({
  children,
  className = '',
  intensity = 3, // Ultra-smooth, subtle 3-degree tilt
  glowColor = 'cyan',
}) => {
  const [rotateX, setRotateX] = useState(0);
  const [rotateY, setRotateY] = useState(0);
  const [glarePosition, setGlarePosition] = useState({ x: 50, y: 50, opacity: 0 });

  const handleMouseMove = (e: React.MouseEvent<HTMLDivElement>) => {
    const rect = e.currentTarget.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    const centerX = rect.width / 2;
    const centerY = rect.height / 2;

    const rX = ((y - centerY) / centerY) * -intensity;
    const rY = ((x - centerX) / centerX) * intensity;

    setRotateX(rX);
    setRotateY(rY);

    const glareX = (x / rect.width) * 100;
    const glareY = (y / rect.height) * 100;
    setGlarePosition({ x: glareX, y: glareY, opacity: 0.12 });
  };

  const handleMouseLeave = () => {
    setRotateX(0);
    setRotateY(0);
    setGlarePosition((prev) => ({ ...prev, opacity: 0 }));
  };

  const glowShadowMap = {
    cyan: 'hover:shadow-[0_12px_32px_rgba(56,189,248,0.18)] hover:border-sky-500/40',
    purple: 'hover:shadow-[0_12px_32px_rgba(168,85,247,0.18)] hover:border-purple-500/40',
    emerald: 'hover:shadow-[0_12px_32px_rgba(16,185,129,0.18)] hover:border-emerald-500/40',
    amber: 'hover:shadow-[0_12px_32px_rgba(245,158,11,0.18)] hover:border-amber-500/40',
  };

  return (
    <div className="perspective-1000 w-full">
      <div
        onMouseMove={handleMouseMove}
        onMouseLeave={handleMouseLeave}
        style={{
          transform: `rotateX(${rotateX}deg) rotateY(${rotateY}deg)`,
          transformStyle: 'preserve-3d',
          transition: 'transform 0.4s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.4s ease',
        }}
        className={`relative rounded-2xl ${glowShadowMap[glowColor]} ${className}`}
      >
        {/* Soft Glare Highlight */}
        <div
          className="absolute inset-0 rounded-2xl pointer-events-none z-10 transition-opacity duration-400 overflow-hidden"
          style={{
            opacity: glarePosition.opacity,
            background: `radial-gradient(circle at ${glarePosition.x}% ${glarePosition.y}%, rgba(255,255,255,0.2) 0%, rgba(255,255,255,0) 60%)`,
          }}
        />

        {/* Stable Micro Depth Content */}
        <div style={{ transform: 'translateZ(2px)' }} className="w-full h-full">
          {children}
        </div>
      </div>
    </div>
  );
};
