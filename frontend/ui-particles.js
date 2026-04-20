class ParticleBackground {
    constructor(containerId = 'particles-canvas', options = {}) {
        this.containerId = containerId;
        this.options = {
            particleColor: options.particleColor || '0, 210, 255',
            particleCount: options.particleCount || 80,
            lineDistance: options.lineDistance || 180,
            particleRadius: options.particleRadius || 2,
            speed: options.speed || 0.8,
            lineOpacity: options.lineOpacity || 0.25,
            particleOpacity: options.particleOpacity || 0.9,
            flowSpeed: options.flowSpeed || 2,
            ...options
        };

        this.canvas = null;
        this.ctx = null;
        this.particles = [];
        this.flowLines = [];
        this.width = 0;
        this.height = 0;
        this.animationId = null;
        this.time = 0;
    }

    init() {
        this.canvas = document.getElementById(this.containerId);
        if (!this.canvas) {
            console.error(`Canvas element with id "${this.containerId}" not found`);
            return;
        }

        this.ctx = this.canvas.getContext('2d');
        this.resize();
        this.createParticles();
        this.createFlowLines();
        this.bindEvents();
        this.animate();
    }

    resize() {
        this.width = this.canvas.width = window.innerWidth;
        this.height = this.canvas.height = window.innerHeight;
    }

    createParticles() {
        this.particles = [];
        const count = Math.min(
            this.options.particleCount,
            Math.floor((this.width * this.height) / 12000)
        );

        for (let i = 0; i < count; i++) {
            this.particles.push({
                x: Math.random() * this.width,
                y: Math.random() * this.height,
                vx: (Math.random() - 0.5) * this.options.speed,
                vy: (Math.random() - 0.5) * this.options.speed,
                radius: Math.random() * this.options.particleRadius * 0.8 + this.options.particleRadius * 0.5,
                opacity: Math.random() * 0.4 + this.options.particleOpacity * 0.6,
                pulseSpeed: Math.random() * 0.02 + 0.01,
                pulsePhase: Math.random() * Math.PI * 2,
                trail: []
            });
        }
    }

    createFlowLines() {
        this.flowLines = [];
        const lineCount = 12;

        for (let i = 0; i < lineCount; i++) {
            const isHorizontal = Math.random() > 0.5;
            this.flowLines.push({
                x: isHorizontal ? -200 : Math.random() * this.width,
                y: isHorizontal ? Math.random() * this.height : -200,
                length: Math.random() * 200 + 100,
                width: isHorizontal ? 1 : 0,
                height: isHorizontal ? 0 : 1,
                speed: (Math.random() * 1.5 + 1) * this.options.flowSpeed,
                direction: isHorizontal ? 1 : (Math.random() > 0.5 ? 1 : -1),
                isHorizontal: isHorizontal,
                hue: Math.random() * 20 - 10,
                alpha: Math.random() * 0.15 + 0.08,
                waveAmp: Math.random() * 30 + 10,
                waveFreq: Math.random() * 0.02 + 0.01
            });
        }
    }

    bindEvents() {
        window.addEventListener('resize', () => {
            this.resize();
            this.createParticles();
            this.createFlowLines();
        });
    }

    drawFlowLines() {
        this.flowLines.forEach((line, index) => {
            const timeOffset = this.time * line.waveFreq;

            if (line.isHorizontal) {
                line.x += line.speed;
                if (line.x > this.width + line.length) {
                    line.x = -line.length;
                    line.y = Math.random() * this.height;
                }

                const gradient = this.ctx.createLinearGradient(line.x, line.y, line.x + line.length, line.y);
                gradient.addColorStop(0, `hsla(${190 + line.hue}, 100%, 60%, 0)`);
                gradient.addColorStop(0.2, `hsla(${190 + line.hue}, 100%, 70%, ${line.alpha})`);
                gradient.addColorStop(0.5, `hsla(${190 + line.hue}, 100%, 80%, ${line.alpha * 1.5})`);
                gradient.addColorStop(0.8, `hsla(${190 + line.hue}, 100%, 70%, ${line.alpha})`);
                gradient.addColorStop(1, `hsla(${190 + line.hue}, 100%, 60%, 0)`);

                this.ctx.beginPath();
                this.ctx.strokeStyle = gradient;
                this.ctx.lineWidth = 1.5;
                this.ctx.lineCap = 'round';

                this.ctx.moveTo(line.x, line.y);
                for (let px = 0; px <= line.length; px += 5) {
                    const wave = Math.sin(timeOffset + px * 0.02) * line.waveAmp * 0.3;
                    this.ctx.lineTo(line.x + px, line.y + wave);
                }
                this.ctx.stroke();

                const dotX = line.x + (Math.sin(timeOffset * 2) * 0.5 + 0.5) * line.length;
                const dotY = line.y + Math.sin(timeOffset + line.length * 0.02) * line.waveAmp * 0.3;

                const glowGradient = this.ctx.createRadialGradient(dotX, dotY, 0, dotX, dotY, 15);
                glowGradient.addColorStop(0, `hsla(${195 + line.hue}, 100%, 80%, ${line.alpha * 2})`);
                glowGradient.addColorStop(0.3, `hsla(${195 + line.hue}, 100%, 70%, ${line.alpha})`);
                glowGradient.addColorStop(1, `hsla(${195 + line.hue}, 100%, 60%, 0)`);

                this.ctx.beginPath();
                this.ctx.fillStyle = glowGradient;
                this.ctx.arc(dotX, dotY, 15, 0, Math.PI * 2);
                this.ctx.fill();

                this.ctx.beginPath();
                this.ctx.fillStyle = `hsla(${195 + line.hue}, 100%, 90%, ${line.alpha * 3})`;
                this.ctx.arc(dotX, dotY, 3, 0, Math.PI * 2);
                this.ctx.fill();

            } else {
                line.y += line.speed * line.direction;
                if (line.y > this.height + line.length) {
                    line.y = -line.length;
                    line.x = Math.random() * this.width;
                }
                if (line.y < -line.length && line.direction < 0) {
                    line.y = this.height + line.length;
                    line.x = Math.random() * this.width;
                }

                const gradient = this.ctx.createLinearGradient(line.x, line.y, line.x, line.y + line.length);
                gradient.addColorStop(0, `hsla(${190 + line.hue}, 100%, 60%, 0)`);
                gradient.addColorStop(0.2, `hsla(${190 + line.hue}, 100%, 70%, ${line.alpha})`);
                gradient.addColorStop(0.5, `hsla(${190 + line.hue}, 100%, 80%, ${line.alpha * 1.5})`);
                gradient.addColorStop(0.8, `hsla(${190 + line.hue}, 100%, 70%, ${line.alpha})`);
                gradient.addColorStop(1, `hsla(${190 + line.hue}, 100%, 60%, 0)`);

                this.ctx.beginPath();
                this.ctx.strokeStyle = gradient;
                this.ctx.lineWidth = 1.5;
                this.ctx.lineCap = 'round';

                this.ctx.moveTo(line.x, line.y);
                for (let py = 0; py <= line.length; py += 5) {
                    const wave = Math.sin(timeOffset + py * 0.02) * line.waveAmp * 0.3;
                    this.ctx.lineTo(line.x + wave, line.y + py);
                }
                this.ctx.stroke();

                const dotX = line.x + Math.sin(timeOffset + line.length * 0.02) * line.waveAmp * 0.3;
                const dotY = line.y + (Math.cos(timeOffset * 2) * 0.5 + 0.5) * line.length;

                const glowGradient = this.ctx.createRadialGradient(dotX, dotY, 0, dotX, dotY, 15);
                glowGradient.addColorStop(0, `hsla(${195 + line.hue}, 100%, 80%, ${line.alpha * 2})`);
                glowGradient.addColorStop(0.3, `hsla(${195 + line.hue}, 100%, 70%, ${line.alpha})`);
                glowGradient.addColorStop(1, `hsla(${195 + line.hue}, 100%, 60%, 0)`);

                this.ctx.beginPath();
                this.ctx.fillStyle = glowGradient;
                this.ctx.arc(dotX, dotY, 15, 0, Math.PI * 2);
                this.ctx.fill();

                this.ctx.beginPath();
                this.ctx.fillStyle = `hsla(${195 + line.hue}, 100%, 90%, ${line.alpha * 3})`;
                this.ctx.arc(dotX, dotY, 3, 0, Math.PI * 2);
                this.ctx.fill();
            }
        });
    }

    drawParticles() {
        this.particles.forEach(p => {
            p.trail.push({ x: p.x, y: p.y, opacity: p.opacity });
            if (p.trail.length > 8) {
                p.trail.shift();
            }

            p.trail.forEach((t, i) => {
                const trailOpacity = (i / p.trail.length) * t.opacity * 0.3;
                const trailRadius = p.radius * (i / p.trail.length) * 0.8;

                this.ctx.beginPath();
                this.ctx.arc(t.x, t.y, trailRadius, 0, Math.PI * 2);
                this.ctx.fillStyle = `rgba(${this.options.particleColor}, ${trailOpacity})`;
                this.ctx.fill();
            });

            const pulse = Math.sin(this.time * p.pulseSpeed + p.pulsePhase) * 0.3 + 0.7;
            const finalOpacity = p.opacity * pulse;

            const glowGradient = this.ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, p.radius * 4);
            glowGradient.addColorStop(0, `rgba(${this.options.particleColor}, ${finalOpacity})`);
            glowGradient.addColorStop(0.4, `rgba(${this.options.particleColor}, ${finalOpacity * 0.4})`);
            glowGradient.addColorStop(1, `rgba(${this.options.particleColor}, 0)`);

            this.ctx.beginPath();
            this.ctx.fillStyle = glowGradient;
            this.ctx.arc(p.x, p.y, p.radius * 4, 0, Math.PI * 2);
            this.ctx.fill();

            this.ctx.beginPath();
            this.ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
            this.ctx.fillStyle = `rgba(${this.options.particleColor}, ${finalOpacity})`;
            this.ctx.fill();

            this.ctx.beginPath();
            this.ctx.arc(p.x, p.y, p.radius * 0.5, 0, Math.PI * 2);
            this.ctx.fillStyle = `rgba(255, 255, 255, ${finalOpacity * 0.8})`;
            this.ctx.fill();
        });
    }

    drawConnections() {
        for (let i = 0; i < this.particles.length; i++) {
            for (let j = i + 1; j < this.particles.length; j++) {
                const dx = this.particles[i].x - this.particles[j].x;
                const dy = this.particles[i].y - this.particles[j].y;
                const distance = Math.sqrt(dx * dx + dy * dy);

                if (distance < this.options.lineDistance) {
                    const opacity = (1 - distance / this.options.lineDistance) * this.options.lineOpacity;

                    const gradient = this.ctx.createLinearGradient(
                        this.particles[i].x, this.particles[i].y,
                        this.particles[j].x, this.particles[j].y
                    );
                    gradient.addColorStop(0, `rgba(${this.options.particleColor}, ${opacity})`);
                    gradient.addColorStop(0.5, `rgba(${this.options.particleColor}, ${opacity * 1.3})`);
                    gradient.addColorStop(1, `rgba(${this.options.particleColor}, ${opacity})`);

                    this.ctx.beginPath();
                    this.ctx.moveTo(this.particles[i].x, this.particles[i].y);
                    this.ctx.lineTo(this.particles[j].x, this.particles[j].y);
                    this.ctx.strokeStyle = gradient;
                    this.ctx.lineWidth = 0.8;
                    this.ctx.stroke();
                }
            }
        }
    }

    updateParticles() {
        this.particles.forEach(p => {
            p.x += p.vx;
            p.y += p.vy;

            if (p.x < 0) p.x = this.width;
            if (p.x > this.width) p.x = 0;
            if (p.y < 0) p.y = this.height;
            if (p.y > this.height) p.y = 0;
        });
    }

    animate() {
        this.ctx.clearRect(0, 0, this.width, this.height);
        this.time += 1;

        this.drawFlowLines();
        this.updateParticles();
        this.drawConnections();
        this.drawParticles();

        this.animationId = requestAnimationFrame(() => this.animate());
    }

    destroy() {
        if (this.animationId) {
            cancelAnimationFrame(this.animationId);
        }
    }
}

function initParticleBackground(containerId = 'particles-canvas', options = {}) {
    const particles = new ParticleBackground(containerId, options);
    particles.init();
    return particles;
}
