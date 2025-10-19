// ========================================
// KOITA_STORE - Script d'interactivité
// ========================================

document.addEventListener('DOMContentLoaded', function() {
    
    // ========================================
    // BARRE DE RECHERCHE AMÉLIORÉE
    // ========================================
    
    const searchInput = document.querySelector('.search-field-improved');
    const searchForm = document.querySelector('.search-form-improved');
    
    if (searchInput) {
        // Afficher ce qu'on tape en temps réel
        searchInput.addEventListener('input', function(e) {
            const query = e.target.value;
            console.log('Recherche:', query);
            
            // Ajouter un indicateur visuel
            if (query.length > 0) {
                searchInput.style.fontWeight = '600';
                searchInput.style.color = 'var(--primary-orange)';
            } else {
                searchInput.style.fontWeight = 'normal';
                searchInput.style.color = 'var(--dark-gray)';
            }
        });
        
        // Auto-focus sur "/" key
        document.addEventListener('keydown', function(e) {
            if (e.key === '/' && !searchInput.matches(':focus')) {
                e.preventDefault();
                searchInput.focus();
            }
        });
    }
    
    // ========================================
    // PROGRESS BAR DE SCROLL
    // ========================================
    
    function createScrollProgressBar() {
        const progressBar = document.createElement('div');
        progressBar.className = 'scroll-progress';
        document.body.appendChild(progressBar);
        
        window.addEventListener('scroll', function() {
            const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
            const scrollHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
            const scrollPercentage = (scrollTop / scrollHeight) * 100;
            progressBar.style.width = scrollPercentage + '%';
        });
    }
    
    createScrollProgressBar();
    
    // ========================================
    // ANIMATION D'AJOUT AU PANIER
    // ========================================
    
    const addToCartButtons = document.querySelectorAll('.add-cart-btn');
    
    addToCartButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            // Effet confetti
            createConfetti(e.clientX, e.clientY);
            
            // Animation du bouton
            const originalText = button.innerHTML;
            button.innerHTML = '<i class="fas fa-check"></i> Ajouté !';
            button.style.background = 'linear-gradient(135deg, #2ecc71, #27ae60)';
            
            // Reset après 2 secondes
            setTimeout(() => {
                button.innerHTML = originalText;
                button.style.background = '';
            }, 2000);
        });
    });
    
    // ========================================
    // FONCTION CONFETTI
    // ========================================
    
    function createConfetti(x, y) {
        const colors = ['#ff6b35', '#38b6ff', '#f39c12', '#e74c3c', '#2ecc71'];
        const confettiCount = 30;
        
        for (let i = 0; i < confettiCount; i++) {
            const confetti = document.createElement('div');
            confetti.className = 'confetti';
            confetti.style.left = x + 'px';
            confetti.style.top = y + 'px';
            confetti.style.background = colors[Math.floor(Math.random() * colors.length)];
            confetti.style.animationDelay = (Math.random() * 0.5) + 's';
            confetti.style.transform = `translateX(${(Math.random() - 0.5) * 200}px)`;
            
            document.body.appendChild(confetti);
            
            setTimeout(() => {
                confetti.remove();
            }, 3000);
        }
    }
    
    // ========================================
    // LAZY LOADING DES IMAGES
    // ========================================
    
    const images = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.removeAttribute('data-src');
                observer.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
    
    // ========================================
    // ANIMATION DES COMPTEURS
    // ========================================
    
    function animateCounter(element, target) {
        let current = 0;
        const increment = target / 50;
        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                current = target;
                clearInterval(timer);
            }
            element.textContent = Math.floor(current);
        }, 20);
    }
    
    const counters = document.querySelectorAll('.animated-count');
    const counterObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const target = parseInt(entry.target.dataset.count);
                animateCounter(entry.target, target);
                counterObserver.unobserve(entry.target);
            }
        });
    });
    
    counters.forEach(counter => counterObserver.observe(counter));
    
    // ========================================
    // EFFET DE PARTICULES SUR HOVER
    // ========================================
    
    const productCards = document.querySelectorAll('.modern-product-card');
    
    productCards.forEach(card => {
        card.addEventListener('mouseenter', function(e) {
            createParticles(card);
        });
    });
    
    function createParticles(element) {
        const particleCount = 5;
        const rect = element.getBoundingClientRect();
        
        for (let i = 0; i < particleCount; i++) {
            const particle = document.createElement('div');
            particle.className = 'product-card-hover-particle';
            particle.style.left = (Math.random() * rect.width) + 'px';
            particle.style.top = (Math.random() * rect.height) + 'px';
            element.appendChild(particle);
            
            setTimeout(() => {
                particle.remove();
            }, 1000);
        }
    }
    
    // ========================================
    // FILTRAGE INSTANTANÉ DES PRODUITS
    // ========================================
    
    if (searchInput) {
        let searchTimeout;
        
        searchInput.addEventListener('input', function(e) {
            clearTimeout(searchTimeout);
            
            searchTimeout = setTimeout(() => {
                const query = e.target.value.toLowerCase();
                const products = document.querySelectorAll('.modern-product-card');
                let visibleCount = 0;
                
                products.forEach(product => {
                    const title = product.querySelector('.product-title').textContent.toLowerCase();
                    const description = product.querySelector('.product-desc').textContent.toLowerCase();
                    
                    if (title.includes(query) || description.includes(query)) {
                        product.style.display = 'block';
                        product.style.animation = 'fadeInUp 0.5s ease';
                        visibleCount++;
                    } else {
                        product.style.display = 'none';
                    }
                });
                
                // Mettre à jour le compteur de résultats
                updateResultCount(visibleCount);
            }, 300);
        });
    }
    
    function updateResultCount(count) {
        const resultCountElement = document.querySelector('.result-count');
        if (resultCountElement) {
            resultCountElement.textContent = `${count} article${count > 1 ? 's' : ''} trouvé${count > 1 ? 's' : ''}`;
            resultCountElement.classList.add('animated-count');
        }
    }
    
    // ========================================
    // TOOLTIP DYNAMIQUE
    // ========================================
    
    function createTooltip(element, text) {
        element.setAttribute('data-tooltip', text);
    }
    
    // Ajouter des tooltips aux icônes
    const icons = document.querySelectorAll('.category-icon-large, .product-category-badge i');
    icons.forEach(icon => {
        const categoryName = icon.closest('.category-card-image, .product-content')?.querySelector('h3, h4')?.textContent;
        if (categoryName) {
            createTooltip(icon, categoryName);
        }
    });
    
    // ========================================
    // SMOOTH SCROLL VERS LES SECTIONS
    // ========================================
    
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // ========================================
    // SAUVEGARDE AUTOMATIQUE DE LA RECHERCHE
    // ========================================
    
    if (searchInput) {
        // Charger la dernière recherche
        const lastSearch = localStorage.getItem('lastSearch');
        if (lastSearch) {
            searchInput.value = lastSearch;
        }
        
        // Sauvegarder à chaque changement
        searchInput.addEventListener('input', function(e) {
            localStorage.setItem('lastSearch', e.target.value);
        });
        
        // Effacer au reset
        const clearButton = document.querySelector('.clear-search');
        if (clearButton) {
            clearButton.addEventListener('click', function() {
                localStorage.removeItem('lastSearch');
            });
        }
    }
    
    // ========================================
    // ANIMATION AU SCROLL (REVEAL)
    // ========================================
    
    const revealElements = document.querySelectorAll('.modern-product-card, .category-card-image');
    
    const revealObserver = new IntersectionObserver((entries) => {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                setTimeout(() => {
                    entry.target.classList.add('reveal-on-scroll');
                }, index * 100);
                revealObserver.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1
    });
    
    revealElements.forEach(element => {
        revealObserver.observe(element);
    });
    
    // ========================================
    // GESTION DES FAVORIS (LOCAL STORAGE)
    // ========================================
    
    function initFavorites() {
        const favoriteButtons = document.querySelectorAll('.favorite-btn');
        
        favoriteButtons.forEach(button => {
            const productId = button.dataset.productId;
            const favorites = JSON.parse(localStorage.getItem('favorites') || '[]');
            
            if (favorites.includes(productId)) {
                button.classList.add('active');
                button.innerHTML = '<i class="fas fa-heart"></i>';
            }
            
            button.addEventListener('click', function(e) {
                e.preventDefault();
                toggleFavorite(productId, button);
            });
        });
    }
    
    function toggleFavorite(productId, button) {
        let favorites = JSON.parse(localStorage.getItem('favorites') || '[]');
        
        if (favorites.includes(productId)) {
            favorites = favorites.filter(id => id !== productId);
            button.classList.remove('active');
            button.innerHTML = '<i class="far fa-heart"></i>';
            showNotification('Retiré des favoris', 'info');
        } else {
            favorites.push(productId);
            button.classList.add('active');
            button.innerHTML = '<i class="fas fa-heart"></i>';
            showNotification('Ajouté aux favoris', 'success');
        }
        
        localStorage.setItem('favorites', JSON.stringify(favorites));
    }
    
    initFavorites();
    
    // ========================================
    // SYSTÈME DE NOTIFICATIONS
    // ========================================
    
    function showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <i class="fas fa-${getNotificationIcon(type)}"></i>
            <span>${message}</span>
        `;
        
        notification.style.cssText = `
            position: fixed;
            top: 100px;
            right: 20px;
            padding: 1rem 1.5rem;
            background: var(--white);
            border-radius: 12px;
            box-shadow: 0 10px 40px var(--shadow-medium);
            z-index: 10000;
            display: flex;
            align-items: center;
            gap: 1rem;
            animation: slideInRight 0.5s ease;
            border-left: 4px solid ${getNotificationColor(type)};
        `;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.style.animation = 'slideOutRight 0.5s ease';
            setTimeout(() => notification.remove(), 500);
        }, 3000);
    }
    
    function getNotificationIcon(type) {
        const icons = {
            success: 'check-circle',
            error: 'exclamation-circle',
            warning: 'exclamation-triangle',
            info: 'info-circle'
        };
        return icons[type] || 'info-circle';
    }
    
    function getNotificationColor(type) {
        const colors = {
            success: '#2ecc71',
            error: '#e74c3c',
            warning: '#f39c12',
            info: '#38b6ff'
        };
        return colors[type] || '#38b6ff';
    }
    
    // ========================================
    // GESTION DU PANIER (MISE À JOUR BADGE)
    // ========================================
    
    function updateCartBadge() {
        const cartBadge = document.getElementById('cartBadge');
        const cartCount = localStorage.getItem('cartCount') || 0;
        
        if (cartBadge) {
            cartBadge.textContent = cartCount;
            
            if (cartCount > 0) {
                cartBadge.style.display = 'flex';
                cartBadge.classList.add('badge-pulse');
            } else {
                cartBadge.style.display = 'none';
            }
        }
    }
    
    // Écouter les événements d'ajout au panier
    addToCartButtons.forEach(button => {
        button.addEventListener('click', function() {
            let cartCount = parseInt(localStorage.getItem('cartCount') || 0);
            cartCount++;
            localStorage.setItem('cartCount', cartCount);
            updateCartBadge();
            showNotification('Produit ajouté au panier !', 'success');
        });
    });
    
    updateCartBadge();
    
    // ========================================
    // COMPARAISON DE PRODUITS
    // ========================================
    
    let compareList = [];
    
    function initCompare() {
        const compareButtons = document.querySelectorAll('.compare-btn');
        
        compareButtons.forEach(button => {
            button.addEventListener('click', function(e) {
                e.preventDefault();
                const productId = this.dataset.productId;
                toggleCompare(productId);
            });
        });
    }
    
    function toggleCompare(productId) {
        if (compareList.includes(productId)) {
            compareList = compareList.filter(id => id !== productId);
            showNotification('Retiré de la comparaison', 'info');
        } else {
            if (compareList.length >= 3) {
                showNotification('Maximum 3 produits à comparer', 'warning');
                return;
            }
            compareList.push(productId);
            showNotification('Ajouté à la comparaison', 'success');
        }
        
        updateCompareButton();
    }
    
    function updateCompareButton() {
        const compareButton = document.getElementById('compareButton');
        if (compareButton) {
            compareButton.textContent = `Comparer (${compareList.length})`;
            compareButton.style.display = compareList.length > 0 ? 'block' : 'none';
        }
    }
    
    initCompare();
    
    // ========================================
    // FILTRAGE AVANCÉ PAR PRIX
    // ========================================
    
    function initPriceFilter() {
        const priceMin = document.getElementById('priceMin');
        const priceMax = document.getElementById('priceMax');
        const priceFilterBtn = document.getElementById('applyPriceFilter');
        
        if (priceFilterBtn) {
            priceFilterBtn.addEventListener('click', function() {
                const min = parseFloat(priceMin.value) || 0;
                const max = parseFloat(priceMax.value) || Infinity;
                
                filterByPrice(min, max);
            });
        }
    }
    
    function filterByPrice(min, max) {
        const products = document.querySelectorAll('.modern-product-card');
        let visibleCount = 0;
        
        products.forEach(product => {
            const priceText = product.querySelector('.price-amount').textContent;
            const price = parseFloat(priceText.replace(/\s/g, ''));
            
            if (price >= min && price <= max) {
                product.style.display = 'block';
                visibleCount++;
            } else {
                product.style.display = 'none';
            }
        });
        
        showNotification(`${visibleCount} produits trouvés`, 'info');
    }
    
    initPriceFilter();
    
    // ========================================
    // DÉTECTION DE LA VITESSE DE SCROLL
    // ========================================
    
    let lastScrollTop = 0;
    let scrollSpeed = 0;
    
    window.addEventListener('scroll', function() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        scrollSpeed = Math.abs(scrollTop - lastScrollTop);
        lastScrollTop = scrollTop;
        
        // Si scroll rapide, masquer certains éléments pour performance
        if (scrollSpeed > 50) {
            document.body.classList.add('fast-scrolling');
        } else {
            document.body.classList.remove('fast-scrolling');
        }
    });
    
    // ========================================
    // RACCOURCIS CLAVIER
    // ========================================
    
    document.addEventListener('keydown', function(e) {
        // Ctrl + K : Focus sur la recherche
        if (e.ctrlKey && e.key === 'k') {
            e.preventDefault();
            searchInput?.focus();
        }
        
        // Escape : Fermer les modals
        if (e.key === 'Escape') {
            closeAllModals();
        }
        
        // F : Ouvrir/fermer filtres
        if (e.key === 'f' && !searchInput?.matches(':focus')) {
            toggleFilters();
        }
    });
    
    function closeAllModals() {
        document.querySelectorAll('.modal, .overlay').forEach(el => {
            el.classList.remove('active');
        });
    }
    
    function toggleFilters() {
        const filtersPanel = document.querySelector('.filters-panel');
        if (filtersPanel) {
            filtersPanel.classList.toggle('open');
        }
    }
    
    // ========================================
    // PRÉCHARGEMENT DES IMAGES
    // ========================================
    
    function preloadImages() {
        const images = document.querySelectorAll('img[data-preload]');
        images.forEach(img => {
            const tempImg = new Image();
            tempImg.src = img.dataset.preload;
        });
    }
    
    preloadImages();
    
    // ========================================
    // DÉTECTION DE LA CONNEXION INTERNET
    // ========================================
    
    window.addEventListener('online', function() {
        showNotification('Connexion rétablie', 'success');
    });
    
    window.addEventListener('offline', function() {
        showNotification('Connexion perdue', 'error');
    });
    
    // ========================================
    // ANALYTICS (TRACKING)
    // ========================================
    
    function trackEvent(category, action, label) {
        console.log('Event:', category, action, label);
        // Intégrer Google Analytics ou autre ici
        // gtag('event', action, { category, label });
    }
    
    // Tracker les clics sur les produits
    productCards.forEach(card => {
        card.addEventListener('click', function() {
            const productName = this.querySelector('.product-title').textContent;
            trackEvent('Product', 'Click', productName);
        });
    });
    
    // Tracker les recherches
    if (searchForm) {
        searchForm.addEventListener('submit', function() {
            const query = searchInput.value;
            trackEvent('Search', 'Submit', query);
        });
    }
    
    // ========================================
    // INITIALISATION FINALE
    // ========================================
    
    console.log('🎮 KOITA_STORE initialisé avec succès!');
    showNotification('Bienvenue sur KOITA_STORE !', 'success');
    
    // Charger les préférences utilisateur
    loadUserPreferences();
    
    function loadUserPreferences() {
        const darkMode = localStorage.getItem('darkMode') === 'true';
        if (darkMode) {
            document.body.classList.add('dark-mode');
        }
    }
});

// ========================================
// ANIMATIONS CSS SUPPLÉMENTAIRES
// ========================================

const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .badge-pulse {
        animation: badgePulse 2s infinite;
    }
    
    @keyframes badgePulse {
        0%, 100% {
            transform: scale(1);
        }
        50% {
            transform: scale(1.1);
        }
    }
    
    .fast-scrolling .product-card-hover-particle,
    .fast-scrolling .smoke-effect {
        display: none !important;
    }
    
    .notification {
        font-family: "Montserrat", sans-serif;
        font-weight: 600;
    }
    
    .notification i {
        font-size: 1.5rem;
    }
    
    .favorite-btn.active {
        color: #e74c3c;
    }
    
    .filters-panel {
        transform: translateX(-100%);
        transition: transform 0.3s ease;
    }
    
    .filters-panel.open {
        transform: translateX(0);
    }
`;
document.head.appendChild(style);