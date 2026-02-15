/**
 * LICHTHARMONIE by Aksu - Ultra-Modern SPA Engine
 */

// --- 0. Configurations ---
const TELEGRAM_TOKEN = 'xxx';
const TELEGRAM_CHAT_ID = '1917004037';

// --- 1. Global Managers (Persistent) ---

class MobileMenuManager {
    constructor() {
        this.overlay = document.getElementById('mobileMenuOverlay');
        this.toggleBtn = document.getElementById('mobileMenuToggle');
        this.closeBtn = document.getElementById('mobileMenuClose');
        this.init();
    }

    init() {
        this.bindEvents();
    }

    bindEvents() {
        this.overlay = document.getElementById('mobileMenuOverlay');
        this.toggleBtn = document.getElementById('mobileMenuToggle');
        this.closeBtn = document.getElementById('mobileMenuClose');

        if (this.toggleBtn) {
            this.toggleBtn.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                this.open();
            });
        }

        if (this.closeBtn) {
            this.closeBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                this.close();
            });
        }

        if (this.overlay) {
            this.overlay.addEventListener('click', (e) => {
                if (e.target === this.overlay) this.close();
            });
        }

        document.querySelectorAll('.mobile-link').forEach(link => {
            link.addEventListener('click', () => {
                this.close();
            });
        });
    }

    open() {
        if (!this.overlay) return;
        this.overlay.classList.add('active');
        document.body.style.overflow = 'hidden';
    }

    close() {
        if (!this.overlay) return;
        this.overlay.classList.remove('active');
        document.body.style.overflow = '';
    }
}

class ThemeManager {
    constructor() {
        this.themeToggle = document.getElementById('themeToggle');
        this.init();
    }
    init() {
        if (localStorage.getItem('theme') === 'dark') this.enable();
        this.bindEvents();
    }
    bindEvents() {
        this.themeToggle = document.getElementById('themeToggle');
        if (this.themeToggle) {
            this.themeToggle.onclick = () => {
                document.body.classList.contains('dark-mode') ? this.disable() : this.enable();
            };
        }
    }
    enable() {
        document.body.classList.add('dark-mode');
        localStorage.setItem('theme', 'dark');
        if (this.themeToggle) this.themeToggle.innerHTML = '<i class="fas fa-sun"></i>';
    }
    disable() {
        document.body.classList.remove('dark-mode');
        localStorage.setItem('theme', 'light');
        if (this.themeToggle) this.themeToggle.innerHTML = '<i class="fas fa-moon"></i>';
    }
}

class ZenAudioPlayer {
    constructor() {
        this.playlist = ['audio/zen1.mp3', 'audio/zen2.mp3', 'audio/zen3.mp3', 'audio/zen4.mp3'];
        this.currentIndex = 0;
        this.audio = new Audio(this.playlist[this.currentIndex]);
        this.isPlaying = false;
        this.init();
    }
    init() {
        this.bindEvents();
        this.audio.addEventListener('ended', () => this.playNext());
        this.audio.addEventListener('error', () => {
            if (this.isPlaying) this.playNext();
        });
    }
    bindEvents() {
        this.toggleBtn = document.getElementById('zenToggle');
        if (this.toggleBtn) {
            this.toggleBtn.onclick = () => this.toggle();
            this.updateUI();
        }
    }
    toggle() { this.isPlaying ? this.pause() : this.play(); }
    play() {
        this.audio.play().then(() => {
            this.isPlaying = true;
            this.updateUI();
        }).catch(err => console.warn('Audio waiting for user interaction'));
    }
    pause() {
        this.audio.pause();
        this.isPlaying = false;
        this.updateUI();
    }
    playNext() {
        this.currentIndex = (this.currentIndex + 1) % this.playlist.length;
        this.audio.src = this.playlist[this.currentIndex];
        if (this.isPlaying) this.play();
    }
    updateUI() {
        this.toggleBtn = document.getElementById('zenToggle');
        if (!this.toggleBtn) return;
        this.toggleBtn.classList.toggle('playing', this.isPlaying);
        this.toggleBtn.innerHTML = this.isPlaying ? '<i class="fas fa-pause"></i>' : '<i class="fas fa-play"></i>';
    }
}

class GlitterBackground {
    constructor() {
        this.canvas = document.getElementById('glitterCanvas');
        if (!this.canvas) return;
        this.ctx = this.canvas.getContext('2d');
        this.particles = [];
        this.mouse = { x: null, y: null, radius: 180 };
        this.init();
    }
    init() {
        window.addEventListener('resize', () => this.resize());
        window.addEventListener('mousemove', (e) => { this.mouse.x = e.x; this.mouse.y = e.y; });
        this.resize();
        this.animate();
    }
    resize() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
        this.particles = Array.from({ length: 180 }, () => new Particle(this.canvas));
    }
    animate() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        this.particles.forEach(p => { p.update(this.mouse); p.draw(this.ctx); });
        requestAnimationFrame(() => this.animate());
    }
}

class Particle {
    constructor(canvas) {
        this.canvas = canvas;
        this.init();
    }
    init() {
        this.x = Math.random() * this.canvas.width;
        this.y = Math.random() * this.canvas.height;
        this.vx = (Math.random() - 0.5) * 0.3;
        this.vy = (Math.random() - 0.5) * 0.3;
        this.size = Math.random() * 3 + 0.5;
        this.color = `rgba(${180 + Math.random() * 50}, ${110 + Math.random() * 60}, ${40 + Math.random() * 40}, ${Math.random() * 0.5 + 0.3})`;
    }
    update(mouse) {
        this.x += this.vx; this.y += this.vy;
        if (mouse.x) {
            const dx = mouse.x - this.x; const dy = mouse.y - this.y;
            const dist = Math.sqrt(dx * dx + dy * dy);
            if (dist < mouse.radius) {
                const force = (mouse.radius - dist) / mouse.radius;
                this.x -= (dx / dist) * force * 3; this.y -= (dy / dist) * force * 3;
            }
        }
        if (this.x < 0) this.x = this.canvas.width; if (this.x > this.canvas.width) this.x = 0;
        if (this.y < 0) this.y = this.canvas.height; if (this.y > this.canvas.height) this.y = 0;
    }
    draw(ctx) {
        ctx.beginPath();
        for (let i = 0; i < 5; i++) {
            ctx.lineTo(this.x + Math.cos((18 + i * 72) / 180 * Math.PI) * this.size, this.y + Math.sin((18 + i * 72) / 180 * Math.PI) * this.size);
            ctx.lineTo(this.x + Math.cos((54 + i * 72) / 180 * Math.PI) * (this.size / 2), this.y + Math.sin((54 + i * 72) / 180 * Math.PI) * (this.size / 2));
        }
        ctx.closePath();
        ctx.fillStyle = this.color;
        ctx.fill();
    }
}

class ButterflyFollower {
    constructor() {
        this.el = document.getElementById('butterfly-follower');
        this.mouse = { x: window.innerWidth / 2, y: window.innerHeight / 2 };
        this.pos = { x: window.innerWidth / 2, y: window.innerHeight / 2 };
        this.init();
    }
    init() {
        this.bindEvents();
        this.animate();
    }
    bindEvents() {
        this.el = document.getElementById('butterfly-follower');
        if (!this.el) return;
        window.addEventListener('mousemove', (e) => {
            this.mouse.x = e.clientX; this.mouse.y = e.clientY;
            this.el.style.opacity = '1';
        });
    }
    animate() {
        this.pos.x += (this.mouse.x - this.pos.x) * 0.05;
        this.pos.y += (this.mouse.y - this.pos.y) * 0.05;
        const angle = Math.atan2(this.mouse.y - this.pos.y, this.mouse.x - this.pos.x) * (180 / Math.PI) + 90;
        if (this.el) this.el.style.transform = `translate3d(${this.pos.x - 20}px, ${this.pos.y - 20}px, 0) rotate(${angle}deg)`;
        requestAnimationFrame(() => this.animate());
    }
}

class SoundTherapy {
    constructor() {
        this.card = document.getElementById('sound-therapy-card');
        // if (!this.card) return; // Don't return early; we might need to bind later if content changes
        // Actually, for simplicity, let's keep it safe.
        // But since SPA re-runs initPageFeatures, we should be careful about duplicate listeners if we didn't use a class instance.
        // The SPA logic seems to re-run initPageFeatures.
        this.audio = new Audio('audio/klang.mp3');
        this.audio.volume = 0.5; // Subtle volume
        this.init();
    }

    init() {
        this.card = document.getElementById('sound-therapy-card');
        if (this.card) this.bindEvents();
    }

    bindEvents() {
        if (!this.card) return;

        // Remove old listeners if any (by replacing the element is one way, but here it breaks observers).
        // Since SPA replaces the whole DOM, we don't need to worry about stacking listeners 
        // on the SAME element instance, because this runs on NEW elements.

        this.card.addEventListener('mouseenter', () => {
            this.audio.currentTime = 0;
            this.audio.play().catch(e => console.log('Audio play failed:', e));
        });

        this.card.addEventListener('mouseleave', () => {
            this.audio.pause();
            this.audio.currentTime = 0;
        });
    }
}

// --- 2. Page Specific Initializer ---

function initPageFeatures() {
    // Navbar Scroll
    const navbar = document.getElementById('navbar');
    window.onscroll = () => {
        navbar?.classList.toggle('scrolled', window.scrollY > 50);
    };

    // Mobile Menu - Delegates to Global Manager now
    if (window.mobileMenu) window.mobileMenu.bindEvents();


    // Reveal Animations
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, { threshold: 0.1 });

    document.querySelectorAll('.bento-item, .hero-content, .glass, .reveal').forEach((el, i) => {
        el.style.opacity = '0'; el.style.transform = 'translateY(30px)';
        el.style.transition = `all 0.6s cubic-bezier(0.16, 1, 0.3, 1) ${i * 0.05}s`;
        observer.observe(el);
    });

    // Glass Shine
    document.querySelectorAll('.glass').forEach(card => {
        if (card.classList.contains('no-tilt')) return;
        card.onmousemove = (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left; const y = e.clientY - rect.top;
            card.style.setProperty('--mouse-x', `${x}px`);
            card.style.setProperty('--mouse-y', `${y}px`);

            // Subtler rotation (minimalist feel)
            const divisor = card.classList.contains('soft-tilt') ? 400 : 100;
            const rotateX = (y - rect.height / 2) / divisor;
            const rotateY = (rect.width / 2 - x) / divisor;

            card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale(1.002)`;
        };
        card.onmouseleave = () => card.style.transform = 'none';
    });

    // FAQ Accordion (Unified)
    document.querySelectorAll('.faq-item').forEach(item => {
        item.onclick = () => {
            const isActive = item.classList.contains('active');
            document.querySelectorAll('.faq-item').forEach(i => i.classList.remove('active'));
            if (!isActive) item.classList.add('active');
        };
    });

    // Telegram Form
    const bookingForm = document.getElementById('bookingForm');
    if (bookingForm) {
        bookingForm.onsubmit = async (e) => {
            e.preventDefault();
            const status = document.getElementById('formStatus');
            const fd = new FormData(bookingForm);
            const msg = `✨ *Neue Terminanfrage:*\n\n👤 *Name:* ${fd.get('name')}\n📞 *Telefon:* ${fd.get('phone')}\n💆 *Service:* ${fd.get('service')}\n📅 *Datum:* ${fd.get('date')}`;
            if (status) { status.style.display = 'block'; status.innerHTML = 'Sende Lichtsignale...'; }
            try {
                const res = await fetch(`https://api.telegram.org/bot${TELEGRAM_TOKEN}/sendMessage`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ chat_id: TELEGRAM_CHAT_ID, text: msg, parse_mode: 'Markdown' })
                });
                if (res.ok && status) { status.innerHTML = 'Lichtvoll empfangen!'; bookingForm.reset(); }
            } catch (e) { if (status) status.innerHTML = 'Fehler.'; }
            setTimeout(() => { if (status) status.style.display = 'none'; }, 5000);
        };
    }

    // Mobile Menu Cleanup: Close after navigation
    const cleanupMenuOverlay = document.getElementById('mobileMenuOverlay');
    const cleanupToggle = document.getElementById('mobileMenuToggle');
    if (cleanupMenuOverlay) cleanupMenuOverlay.classList.remove('active');
    if (cleanupToggle) {
        const icon = cleanupToggle.querySelector('i');
        icon?.classList.add('fa-bars');
        icon?.classList.remove('fa-times');
    }

    // Initialize Sound Therapy
    new SoundTherapy();
}

// --- 3. SPA Transition Engine ---

class SPAEngine {
    constructor() {
        this.content = document.getElementById('main-content');
        this.init();
    }
    init() {
        window.onpopstate = () => this.loadPage(window.location.pathname, false);
        this.bindLinks(document);
    }
    bindLinks(scope) {
        scope.querySelectorAll('a').forEach(link => {
            const href = link.getAttribute('href');
            // Skip external links, tel/mail, or empty
            if (!href || href.startsWith('http') || href.startsWith('tel:') || href.startsWith('mailto:')) return;
            // Skip social media follow buttons etc. (handled by their href)
            if (link.getAttribute('target') === '_blank') return;

            link.addEventListener('click', (e) => {
                const [path, hash] = href.split('#');
                const currentPath = window.location.pathname;
                const isHomePage = currentPath === '/' || currentPath.endsWith('index.html');
                const targetIsHome = path === '' || path === 'index.html';

                // Scenario A: Anchor link on the Home page (from the home page)
                if (targetIsHome && isHomePage && hash) {
                    const target = document.getElementById(hash);
                    if (target) {
                        e.preventDefault();
                        window.scrollTo({ top: target.offsetTop - 35, behavior: 'smooth' });
                        return;
                    }
                }

                // Scenario B: Link to current page with hash
                if (path !== '' && currentPath.endsWith(path) && hash) {
                    const target = document.getElementById(hash);
                    if (target) {
                        e.preventDefault();
                        window.scrollTo({ top: target.offsetTop - 35, behavior: 'smooth' });
                        return;
                    }
                }

                // Scenario C: Anchor link to home but NOT on home
                if (targetIsHome && !isHomePage) {
                    e.preventDefault();
                    this.loadPage('index.html' + (hash ? '#' + hash : ''), true);
                    return;
                }

                // Scenario D: Page transition
                if (href.includes('.html')) {
                    e.preventDefault();
                    if (currentPath.endsWith(path)) return; // Already here, do nothing
                    this.loadPage(href, true);
                }
            });
        });
        this.refreshActiveLinks();
    }

    refreshActiveLinks() {
        const currentPath = window.location.pathname;
        const isHomePage = currentPath === '/' || currentPath.endsWith('index.html');

        document.querySelectorAll('.nav-links a, .mobile-links a').forEach(link => {
            const href = link.getAttribute('href');
            if (!href) return;

            const [path, hash] = href.split('#');
            const targetIsHome = path === '' || path === 'index.html';

            let isActive = false;
            // Only highlight if it's the main page link (no hash)
            if (targetIsHome && isHomePage && !hash) {
                isActive = true;
            } else if (path !== '' && currentPath.endsWith(path) && !hash) {
                isActive = true;
            }

            if (isActive) {
                link.classList.add('active');
            } else {
                link.classList.remove('active');
            }
        });
    }
    async loadPage(url, push = true) {
        this.content = document.getElementById('main-content');
        if (!this.content) return;
        this.content.classList.add('loading');
        try {
            const fetchUrl = url.split('#')[0];
            const res = await fetch(fetchUrl);
            const html = await res.text();
            const doc = new DOMParser().parseFromString(html, 'text/html');
            const newMain = doc.getElementById('main-content');

            setTimeout(() => {
                this.content.innerHTML = newMain.innerHTML;
                document.title = doc.title;
                if (push) window.history.pushState({}, '', url);

                // Scroll to top IMMEDIATELY before initializing animations
                // This ensures IntersectionObserver sees elements in their correct viewport position
                const hash = url.split('#')[1];
                if (!hash) {
                    window.scrollTo(0, 0);
                }

                initPageFeatures();
                // Re-bind links only inside content; navbar is persistent and bound once
                this.bindLinks(this.content);

                window.audioPlayer?.bindEvents();
                window.themeManager?.bindEvents();
                window.butterfly?.bindEvents();
                this.content.classList.remove('loading');

                // Handle Scroll to Hash after load
                if (hash) {
                    setTimeout(() => {
                        const target = document.getElementById(hash);
                        if (target) window.scrollTo({ top: target.offsetTop - 35, behavior: 'smooth' });
                    }, 100);
                }
            }, 500);
        } catch (e) { window.location.href = url.split('#')[0]; }
    }
}

// --- 4. Bootstrapping ---

window.onload = () => {
    window.themeManager = new ThemeManager();
    window.mobileMenu = new MobileMenuManager();
    window.glitter = new GlitterBackground();

    window.audioPlayer = new ZenAudioPlayer();
    window.butterfly = new ButterflyFollower();
    initPageFeatures();
    window.spa = new SPAEngine();
};



