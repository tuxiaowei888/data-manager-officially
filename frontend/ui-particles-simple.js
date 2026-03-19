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
            ...options
        };

        this.canvas = null;
        this.ctx = null;
        this.particles = [];
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
                pulsePhase: Math.random() * Math.PI * 2
            });
        }
    }

    bindEvents() {
        window.addEventListener('resize', () => {
            this.resize();
            this.createParticles();
        });
    }

    drawParticles() {
        this.particles.forEach(p => {
            const pulse = Math.sin(this.time * p.pulseSpeed + p.pulsePhase) * 0.3 + 0.7;
            const finalOpacity = p.opacity * pulse;

            // 外层光晕
            const glowGradient = this.ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, p.radius * 4);
            glowGradient.addColorStop(0, `rgba(${this.options.particleColor}, ${finalOpacity * 0.5})`);
            glowGradient.addColorStop(0.4, `rgba(${this.options.particleColor}, ${finalOpacity * 0.2})`);
            glowGradient.addColorStop(1, `rgba(${this.options.particleColor}, 0)`);

            this.ctx.beginPath();
            this.ctx.fillStyle = glowGradient;
            this.ctx.arc(p.x, p.y, p.radius * 4, 0, Math.PI * 2);
            this.ctx.fill();

            // 核心粒子
            this.ctx.beginPath();
            this.ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
            this.ctx.fillStyle = `rgba(${this.options.particleColor}, ${finalOpacity})`;
            this.ctx.fill();

            // 中心高光
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
                    gradient.addColorStop(0.5, `rgba(${this.options.particleColor}, ${opacity * 1.5})`);
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
