// ========================================
// KOITA_STORE - Script d'interactivité
// ========================================

document.addEventListener('DOMContentLoaded', function() {
    
    // ========================================
    // CARROUSEL AUTOMATIQUE
    // ========================================
    
    function initCarousel() {
        const carousel = document.querySelector('.carousel-container');
        if (!carousel) return;

        const slides = carousel.querySelector('.carousel-slides');
        const slidesCount = carousel.querySelectorAll('.slide').length;
        const prevBtn = carousel.querySelector('.prev-btn');
        const nextBtn = carousel.querySelector('.next-btn');
        const dots = carousel.querySelectorAll('.dot');
        let currentIndex = 0;
        let autoPlayInterval;

        function goToSlide(index) {
            if (index < 0) {
                currentIndex = slidesCount - 1;
            } else if (index >= slidesCount) {
                currentIndex = 0;
            } else {
                currentIndex = index;
            }
            slides.style.transform = `translateX(-${currentIndex * 100}%)`;
            updateDots();
        }

        function updateDots() {
            dots.forEach((dot, index) => {
                dot.classList.toggle('active', index === currentIndex);
            });
        }

        function startAutoPlay() {
            autoPlayInterval = setInterval(() => {
                goToSlide(currentIndex + 1);
            }, 5000);
        }

        function stopAutoPlay() {
            clearInterval(autoPlayInterval);
        }

        if (prevBtn) {
            prevBtn.addEventListener('click', () => {
                stopAutoPlay();
                goToSlide(currentIndex - 1);
                startAutoPlay();
            });
        }

        if (nextBtn) {
            nextBtn.addEventListener('click', () => {
                stopAutoPlay();
                goToSlide(currentIndex + 1);
                startAutoPlay();
            });
        }

        dots.forEach(dot => {
            dot.addEventListener('click', function() {
                stopAutoPlay();
                const slideIndex = parseInt(this.getAttribute('data-slide'));
                goToSlide(slideIndex);
                startAutoPlay();
            });
        });

        // Démarrer l'auto-play
        startAutoPlay();

        // Pause au survol
        carousel.addEventListener('mouseenter', stopAutoPlay);
        carousel.addEventListener('mouseleave', startAutoPlay);
    }

    initCarousel();
    
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
    
    const addToCartButtons = document.querySelectorAll('.add-cart-btn, .btn-primary');
    
    addToCartButtons.forEach(button => {
        // Vérifier que c'est bien un bouton d'ajout au panier
        if (button.textContent.includes('Ajouter au panier') || button.classList.contains('add-cart-btn')) {
            button.addEventListener('click', function(e) {
                // Empêcher le comportement par défaut si c'est un formulaire
                if (button.type !== 'submit') {
                    e.preventDefault();
                }
                
                // Effet confetti
                const rect = button.getBoundingClientRect();
                createConfetti(rect.left + rect.width/2, rect.top + rect.height/2);
                
                // Animation du bouton
                const originalText = button.innerHTML;
                const originalBackground = button.style.background;
                button.innerHTML = '<i class="fas fa-check"></i> Ajouté !';
                button.style.background = 'linear-gradient(135deg, #2ecc71, #27ae60)';
                
                // Reset après 2 secondes
                setTimeout(() => {
                    button.innerHTML = originalText;
                    button.style.background = originalBackground;
                }, 2000);
                
                // Mettre à jour le badge du panier
                updateCartBadge(true);
                showNotification('Produit ajouté au panier !', 'success');
            });
        }
    });
    
    // ========================================
    // FONCTION CONFETTI
    // ========================================
    
    function createConfetti(x, y) {
        const colors = ['#ff6b35', '#38b6ff', '#f39c12', '#e74c3c', '#2ecc71'];
        const confettiCount = 20;
        
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
                if (confetti.parentNode) {
                    confetti.remove();
                }
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
            element.textContent = Math.floor(current).toLocaleString();
        }, 20);
    }
    
    const counters = document.querySelectorAll('.animated-count');
    const counterObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const target = parseInt(entry.target.dataset.count) || 0;
                animateCounter(entry.target, target);
                counterObserver.unobserve(entry.target);
            }
        });
    });
    
    counters.forEach(counter => counterObserver.observe(counter));
    
    // ========================================
    // EFFET DE PARTICULES SUR HOVER
    // ========================================
    
    const productCards = document.querySelectorAll('.product-card, .modern-product-card');
    
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
                if (particle.parentNode) {
                    particle.remove();
                }
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
                const products = document.querySelectorAll('.product-card, .modern-product-card');
                let visibleCount = 0;
                
                products.forEach(product => {
                    const title = product.querySelector('h3')?.textContent.toLowerCase() || '';
                    const description = product.querySelector('.product-description')?.textContent.toLowerCase() || '';
                    
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
    const icons = document.querySelectorAll('.category-icon-large, .product-category-badge i, .feature-box i');
    icons.forEach(icon => {
        const categoryName = icon.closest('.category-card-image, .product-content, .feature-box')?.querySelector('h3, h4')?.textContent;
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
                searchInput.value = '';
            });
        }
    }
    
    // ========================================
    // ANIMATION AU SCROLL (REVEAL)
    // ========================================
    
    const revealElements = document.querySelectorAll('.product-card, .category-card-image, .feature-box');
    
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
        // Supprimer les notifications existantes
        document.querySelectorAll('.custom-notification').forEach(notif => notif.remove());
        
        const notification = document.createElement('div');
        notification.className = `custom-notification notification-${type}`;
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
            font-family: "Montserrat", sans-serif;
            font-weight: 600;
        `;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.style.animation = 'slideOutRight 0.5s ease';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.remove();
                }
            }, 500);
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
    
    function updateCartBadge(increment = false) {
        const cartBadge = document.getElementById('cartBadge');
        let cartCount = parseInt(localStorage.getItem('cartCount') || '0');
        
        if (increment) {
            cartCount++;
            localStorage.setItem('cartCount', cartCount.toString());
        }
        
        if (cartBadge) {
            cartBadge.textContent = cartCount;
            
            if (cartCount > 0) {
                cartBadge.style.display = 'flex';
                cartBadge.classList.add('badge-pulse');
            } else {
                cartBadge.style.display = 'none';
                cartBadge.classList.remove('badge-pulse');
            }
        }
    }
    
    // Initialiser le badge du panier
    updateCartBadge();
    
    // ========================================
    // COMPARAISON DE PRODUITS
    // ========================================
    
    let compareList = JSON.parse(localStorage.getItem('compareList') || '[]');
    
    function initCompare() {
        const compareButtons = document.querySelectorAll('.compare-btn');
        
        compareButtons.forEach(button => {
            button.addEventListener('click', function(e) {
                e.preventDefault();
                const productId = this.dataset.productId;
                toggleCompare(productId);
            });
        });
        
        updateCompareButton();
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
        
        localStorage.setItem('compareList', JSON.stringify(compareList));
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
        
        if (priceFilterBtn && priceMin && priceMax) {
            priceFilterBtn.addEventListener('click', function() {
                const min = parseFloat(priceMin.value) || 0;
                const max = parseFloat(priceMax.value) || Infinity;
                
                filterByPrice(min, max);
            });
        }
    }
    
    function filterByPrice(min, max) {
        const products = document.querySelectorAll('.product-card, .modern-product-card');
        let visibleCount = 0;
        
        products.forEach(product => {
            const priceElement = product.querySelector('.price');
            if (priceElement) {
                const priceText = priceElement.textContent.replace(/[^\d,]/g, '').replace(',', '.');
                const price = parseFloat(priceText);
                
                if (!isNaN(price) && price >= min && price <= max) {
                    product.style.display = 'block';
                    visibleCount++;
                } else {
                    product.style.display = 'none';
                }
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
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            if (searchInput) {
                searchInput.focus();
            }
        }
        
        // Escape : Fermer les modals
        if (e.key === 'Escape') {
            closeAllModals();
        }
        
        // F : Ouvrir/fermer filtres
        if (e.key === 'f' && !(searchInput && searchInput.matches(':focus'))) {
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
            const productName = this.querySelector('h3')?.textContent || 'Produit sans nom';
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
    // GESTION DU DROPDOWN PROFIL
    // ========================================
    
    const profileToggle = document.getElementById('profileToggle');
    const profileDropdown = document.getElementById('profileDropdown');
    
    if (profileToggle && profileDropdown) {
        profileToggle.addEventListener('click', function(e) {
            e.preventDefault();
            profileDropdown.classList.toggle('show');
        });
        
        // Fermer le dropdown si on clique ailleurs
        window.addEventListener('click', function(e) {
            if (!e.target.matches('.profile-icon') && !e.target.closest('.profile-icon')) {
                if (profileDropdown && profileDropdown.classList.contains('show')) {
                    profileDropdown.classList.remove('show');
                }
            }
        });
    }
    
    // ========================================
    // INITIALISATION FINALE
    // ========================================
    
    console.log('🎮 KOITA_STORE initialisé avec succès!');
    
    // Charger les préférences utilisateur
    loadUserPreferences();
    
    function loadUserPreferences() {
        const darkMode = localStorage.getItem('darkMode') === 'true';
        if (darkMode) {
            document.body.classList.add('dark-mode');
        }
        
        // Charger d'autres préférences si nécessaire
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme) {
            document.documentElement.setAttribute('data-theme', savedTheme);
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
    
    .custom-notification {
        font-family: "Montserrat", sans-serif;
        font-weight: 600;
    }
    
    .custom-notification i {
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
    
    .confetti {
        position: fixed;
        width: 10px;
        height: 10px;
        background: var(--primary-orange);
        animation: confetti-fall 3s linear forwards;
        z-index: 9999;
        pointer-events: none;
    }
    
    @keyframes confetti-fall {
        0% {
            transform: translateY(-100%) rotate(0deg);
            opacity: 1;
        }
        100% {
            transform: translateY(100vh) rotate(720deg);
            opacity: 0;
        }
    }
    
    .product-card-hover-particle {
        position: absolute;
        width: 5px;
        height: 5px;
        background: var(--primary-orange);
        border-radius: 50%;
        pointer-events: none;
        animation: particles 1s ease-out forwards;
    }
    
    @keyframes particles {
        0% {
            opacity: 0;
            transform: translateY(0) scale(0);
        }
        50% {
            opacity: 1;
        }
        100% {
            opacity: 0;
            transform: translateY(-20px) scale(1);
        }
    }
    
    .reveal-on-scroll {
        opacity: 0;
        animation: reveal 0.8s ease forwards;
    }
    
    @keyframes reveal {
        from {
            opacity: 0;
            transform: translateY(50px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .scroll-progress {
        position: fixed;
        top: 0;
        left: 0;
        width: 0%;
        height: 4px;
        background: linear-gradient(90deg, var(--primary-orange), var(--secondary-blue));
        z-index: 9999;
        transition: width 0.1s ease;
    }
`;
document.head.appendChild(style);

// ========================================
// FONCTIONS GLOBALES
// ========================================

// Fonction pour formater les prix
function formatPrice(price) {
    return new Intl.NumberFormat('fr-FR', {
        style: 'currency',
        currency: 'XOF'
    }).format(price).replace('XOF', 'FCFA');
}

// Fonction pour obtenir le token CSRF (utile pour les requêtes AJAX)
function getCSRFToken() {
    const name = 'csrftoken';
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Fonction pour faire des requêtes AJAX
function makeRequest(url, options = {}) {
    const defaultOptions = {
        headers: {
            'X-CSRFToken': getCSRFToken(),
            'Content-Type': 'application/json',
        }
    };
    
    return fetch(url, { ...defaultOptions, ...options })
        .then(response => {
            if (!response.ok) {
                throw new Error('Erreur réseau');
            }
            return response.json();
        });
}

// Export des fonctions globales si nécessaire (pour les modules)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        formatPrice,
        getCSRFToken,
        makeRequest
    };
}
// Validation de l'ID joueur
function validatePlayerId(input) {
    const playerId = input.value.trim();
    const productRequiresId = document.getElementById('player_id') !== null;
    
    if (productRequiresId && !playerId) {
        showNotification('❌ ID joueur requis pour ce produit!', 'error');
        return false;
    }
    
    if (playerId && !/^\d+$/.test(playerId)) {
        showNotification('❌ L\'ID joueur doit contenir uniquement des chiffres!', 'error');
        return false;
    }
    
    return true;
}

// Écouter la soumission du formulaire d'ajout au panier
document.addEventListener('DOMContentLoaded', function() {
    const addToCartForm = document.querySelector('form[action*="add_to_cart"]');
    if (addToCartForm) {
        addToCartForm.addEventListener('submit', function(e) {
            const playerIdInput = document.getElementById('player_id');
            if (playerIdInput && !validatePlayerId(playerIdInput)) {
                e.preventDefault();
                playerIdInput.focus();
            }
        });
    }
});