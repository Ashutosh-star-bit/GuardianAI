import React, { useEffect, useRef } from 'react';

export const CinematicMatrix3DCanvas: React.FC = () => {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    let animationFrameId: number;
    let width = (canvas.width = window.innerWidth);
    let height = (canvas.height = window.innerHeight);

    const handleResize = () => {
      if (!canvas) return;
      width = canvas.width = window.innerWidth;
      height = canvas.height = window.innerHeight;
    };

    window.addEventListener('resize', handleResize);

    // 3D Floating Particle Nodes
    const numNodes = 45;
    const nodes: Array<{
      x: number;
      y: number;
      z: number;
      vx: number;
      vy: number;
      vz: number;
      radius: number;
      color: string;
    }> = [];

    const colors = ['rgba(56, 189, 248, 0.6)', 'rgba(168, 85, 247, 0.5)', 'rgba(14, 165, 233, 0.4)'];

    for (let i = 0; i < numNodes; i++) {
      nodes.push({
        x: (Math.random() - 0.5) * width,
        y: (Math.random() - 0.5) * height,
        z: Math.random() * 800 + 100,
        vx: (Math.random() - 0.5) * 0.4,
        vy: (Math.random() - 0.5) * 0.4,
        vz: (Math.random() - 0.5) * 0.5,
        radius: Math.random() * 2 + 1,
        color: colors[Math.floor(Math.random() * colors.length)],
      });
    }

    const focalLength = 400;

    const render = () => {
      ctx.clearRect(0, 0, width, height);

      const cx = width / 2;
      const cy = height / 2;

      // Draw faint connections between nearby 3D nodes
      for (let i = 0; i < nodes.length; i++) {
        const nodeA = nodes[i];

        // Move node
        nodeA.x += nodeA.vx;
        nodeA.y += nodeA.vy;
        nodeA.z += nodeA.vz;

        if (nodeA.x < -width) nodeA.x = width;
        if (nodeA.x > width) nodeA.x = -width;
        if (nodeA.y < -height) nodeA.y = height;
        if (nodeA.y > height) nodeA.y = -height;
        if (nodeA.z < 50) nodeA.z = 900;
        if (nodeA.z > 900) nodeA.z = 50;

        // Project 3D to 2D
        const scale = focalLength / nodeA.z;
        const px = nodeA.x * scale + cx;
        const py = nodeA.y * scale + cy;

        if (px < 0 || px > width || py < 0 || py > height) continue;

        // Draw particle
        ctx.beginPath();
        ctx.arc(px, py, nodeA.radius * scale, 0, Math.PI * 2);
        ctx.fillStyle = nodeA.color;
        ctx.shadowBlur = 12 * scale;
        ctx.shadowColor = '#38bdf8';
        ctx.fill();

        // Connect lines
        for (let j = i + 1; j < nodes.length; j++) {
          const nodeB = nodes[j];
          const dx = nodeA.x - nodeB.x;
          const dy = nodeA.y - nodeB.y;
          const dz = nodeA.z - nodeB.z;
          const dist = Math.sqrt(dx * dx + dy * dy + dz * dz);

          if (dist < 220) {
            const scaleB = focalLength / nodeB.z;
            const pxB = nodeB.x * scaleB + cx;
            const pyB = nodeB.y * scaleB + cy;

            const alpha = (1 - dist / 220) * 0.25;
            ctx.beginPath();
            ctx.moveTo(px, py);
            ctx.lineTo(pxB, pyB);
            ctx.strokeStyle = `rgba(56, 189, 248, ${alpha})`;
            ctx.lineWidth = 0.6 * scale;
            ctx.stroke();
          }
        }
      }

      animationFrameId = requestAnimationFrame(render);
    };

    render();

    return () => {
      window.removeEventListener('resize', handleResize);
      cancelAnimationFrame(animationFrameId);
    };
  }, []);

  return (
    <canvas
      ref={canvasRef}
      className="fixed inset-0 pointer-events-none z-0 opacity-40 mix-blend-screen"
    />
  );
};
