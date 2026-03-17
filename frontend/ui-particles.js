class ParticleBackground {
    constructor(containerId = 'particles-canvas', options = {}) {
        this.containerId = containerId;
        this.options = {
            particleColor: options.particleColor || '0, 210, 255',
            particleCount: options.particleCount || 80,
            lineDistance: options.lineDistance || 150,
            particleRadius: options.particleRadius || 2,
            speed: options.speed || 0.5,
            ...options
        };
        
        this.canvas = null;
        this.ctx = null;
        this.particles = [];
        this.width = 0;
        this.height = 0;
        this.animationId = null;
        this.mouseX = null;
        this.mouseY = null;
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
            Math.floor((this.width * this.height) / 10000)
        );
        
        for (let i = 0; i < count; i++) {
            this.particles.push({
                x: Math.random() * this.width,
                y: Math.random() * this.height,
                vx: (Math.random() - 0.5) * this.options.speed,
                vy: (Math.random() - 0.5) * this.options.speed,
                radius: Math.random() * this.options.particleRadius + 1,
                opacity: Math.random() * 0.5 + 0.2
            });
        }
    }

    bindEvents() {
        window.addEventListener('resize', () => {
            this.resize();
            this.createParticles();
        });

        window.addEventListener('mousemove', (e) => {
            this.mouseX = e.clientX;
            this.mouseY = e.clientY;
        });

        window.addEventListener('mouseout', () => {
            this.mouseX = null;
            this.mouseY = null;
        });
    }

    drawParticles() {
        this.particles.forEach(p => {
            this.ctx.beginPath();
            this.ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
            this.ctx.fillStyle = `rgba(${this.options.particleColor}, ${p.opacity})`;
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
                    const opacity = 1 - distance / this.options.lineDistance;
                    this.ctx.beginPath();
                    this.ctx.moveTo(this.particles[i].x, this.particles[i].y);
                    this.ctx.lineTo(this.particles[j].x, this.particles[j].y);
                    this.ctx.strokeStyle = `rgba(${this.options.particleColor}, ${opacity * 0.3})`;
                    this.ctx.lineWidth = 1;
                    this.ctx.stroke();
                }
            }
        }
    }

    updateParticles() {
        this.particles.forEach(p => {
            p.x += p.vx;
            p.y += p.vy;

            if (p.x < 0 || p.x > this.width) p.vx *= -1;
            if (p.y < 0 || p.y > this.height) p.vy *= -1;

            if (this.mouseX !== null && this.mouseY !== null) {
                const dx = p.x - this.mouseX;
                const dy = p.y - this.mouseY;
                const distance = Math.sqrt(dx * dx + dy * dy);
                if (distance < 100) {
                    const force = (100 - distance) / 100;
                    p.vx += (dx / distance) * force * 0.02;
                    p.vy += (dy / distance) * force * 0.02;
                }
            }
        });
    }

    animate() {
        this.ctx.clearRect(0, 0, this.width, this.height);
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
