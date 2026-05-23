/* =============================================================================
   ST. XAVIER'S SCHOOL, HARMUTTY — MAIN JAVASCRIPT
   =============================================================================
   Clean, well-commented vanilla JavaScript for:
   1.  Hero Carousel (auto-play, arrows, dots, touch/swipe)
   2.  Mobile Navigation (hamburger toggle)
   3.  Scroll Animations (Intersection Observer)
   4.  Counter Animation (animated number count-up)
   5.  Sticky Header Shadow
   6.  Active Navigation Link Highlighting
   7.  Smooth Scroll for Anchor Links
   ============================================================================= */

document.addEventListener('DOMContentLoaded', () => {
  'use strict';

  /* =========================================================================
     1. HERO CAROUSEL
     =========================================================================
     Features:
     - Auto-advances every 5 seconds
     - Fade transitions between slides
     - Previous / Next arrow controls
     - Indicator dot controls
     - Pauses on hover, resumes on mouse leave
     - Touch / swipe support for mobile devices
     ========================================================================= */

  const carousel = document.querySelector('.hero-carousel');

  if (carousel) {
    const slides       = carousel.querySelectorAll('.carousel-slide');
    const prevBtn      = carousel.querySelector('.carousel-prev');
    const nextBtn      = carousel.querySelector('.carousel-next');
    const dotsContainer = carousel.querySelector('.carousel-indicators');
    const dots         = dotsContainer ? dotsContainer.querySelectorAll('.dot') : [];
    let currentSlide   = 0;
    let autoPlayTimer  = null;
    const INTERVAL     = 5000; // 5 seconds

    /**
     * Show a specific slide by index.
     * Removes .active from the current slide and dot, adds it to the target.
     */
    function goToSlide(index) {
      // Wrap around
      if (index < 0) index = slides.length - 1;
      if (index >= slides.length) index = 0;

      // Deactivate current
      slides[currentSlide].classList.remove('active');
      if (dots[currentSlide]) dots[currentSlide].classList.remove('active');

      // Activate target
      currentSlide = index;
      slides[currentSlide].classList.add('active');
      if (dots[currentSlide]) dots[currentSlide].classList.add('active');
    }

    /** Advance to the next slide */
    function nextSlide() {
      goToSlide(currentSlide + 1);
    }

    /** Go back to the previous slide */
    function prevSlide() {
      goToSlide(currentSlide - 1);
    }

    /** Start the auto-play timer */
    function startAutoPlay() {
      stopAutoPlay(); // prevent duplicate timers
      autoPlayTimer = setInterval(nextSlide, INTERVAL);
    }

    /** Stop the auto-play timer */
    function stopAutoPlay() {
      if (autoPlayTimer) {
        clearInterval(autoPlayTimer);
        autoPlayTimer = null;
      }
    }

    // ── Arrow Controls ──────────────────────────────────────────────────
    if (prevBtn) {
      prevBtn.addEventListener('click', () => {
        prevSlide();
        startAutoPlay(); // reset timer on manual interaction
      });
    }

    if (nextBtn) {
      nextBtn.addEventListener('click', () => {
        nextSlide();
        startAutoPlay();
      });
    }

    // ── Dot Controls ────────────────────────────────────────────────────
    dots.forEach((dot, i) => {
      dot.addEventListener('click', () => {
        goToSlide(i);
        startAutoPlay();
      });
    });

    // ── Pause on Hover ──────────────────────────────────────────────────
    carousel.addEventListener('mouseenter', stopAutoPlay);
    carousel.addEventListener('mouseleave', startAutoPlay);

    // ── Touch / Swipe Support ───────────────────────────────────────────
    let touchStartX = 0;
    let touchEndX   = 0;
    const SWIPE_THRESHOLD = 50; // minimum px distance to register a swipe

    carousel.addEventListener('touchstart', (e) => {
      touchStartX = e.changedTouches[0].screenX;
      stopAutoPlay();
    }, { passive: true });

    carousel.addEventListener('touchend', (e) => {
      touchEndX = e.changedTouches[0].screenX;
      const diff = touchStartX - touchEndX;

      if (Math.abs(diff) > SWIPE_THRESHOLD) {
        if (diff > 0) {
          nextSlide();  // swiped left → next
        } else {
          prevSlide();  // swiped right → prev
        }
      }

      startAutoPlay();
    }, { passive: true });

    // ── Keyboard support (arrow keys) ───────────────────────────────────
    document.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowLeft') { prevSlide(); startAutoPlay(); }
      if (e.key === 'ArrowRight') { nextSlide(); startAutoPlay(); }
    });

    // Initialise: show first slide, start auto-play
    goToSlide(0);
    startAutoPlay();
  }


  /* =========================================================================
     2. MOBILE NAVIGATION
     =========================================================================
     - Toggles the .active class on .nav-links when the hamburger is clicked
     - Closes the menu when a navigation link is clicked
     - Closes the menu when clicking outside of it
     ========================================================================= */

  const navToggle = document.querySelector('.nav-toggle');
  const navLinks  = document.querySelector('.nav-links');

  if (navToggle && navLinks) {
    // Toggle menu open / close
    navToggle.addEventListener('click', (e) => {
      e.stopPropagation();
      navToggle.classList.toggle('active');
      navLinks.classList.toggle('active');
    });

    // Close menu when a link is clicked (for single-page smooth scrolling)
    navLinks.querySelectorAll('a').forEach((link) => {
      link.addEventListener('click', () => {
        navToggle.classList.remove('active');
        navLinks.classList.remove('active');
      });
    });

    // Close menu when clicking anywhere outside the nav
    document.addEventListener('click', (e) => {
      if (!navLinks.contains(e.target) && !navToggle.contains(e.target)) {
        navToggle.classList.remove('active');
        navLinks.classList.remove('active');
      }
    });
  }


  /* =========================================================================
     3. SCROLL ANIMATIONS (Intersection Observer)
     =========================================================================
     - Observes all elements with .animate-on-scroll
     - Adds .animated when 15 % of the element enters the viewport
     - Unobserves once animated (fires only once)
     ========================================================================= */

  const scrollElements = document.querySelectorAll('.animate-on-scroll');

  if (scrollElements.length > 0 && 'IntersectionObserver' in window) {
    const scrollObserver = new IntersectionObserver(
      (entries, observer) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('animated');
            observer.unobserve(entry.target); // animate only once
          }
        });
      },
      {
        threshold: 0.15,      // trigger when 15 % visible
        rootMargin: '0px 0px -50px 0px' // slight offset so it triggers a bit after scroll
      }
    );

    scrollElements.forEach((el) => scrollObserver.observe(el));
  } else {
    // Fallback for browsers without Intersection Observer
    scrollElements.forEach((el) => el.classList.add('animated'));
  }


  /* =========================================================================
     4. COUNTER ANIMATION
     =========================================================================
     - Targets elements with .counter-number and a data-target attribute
     - Animates the displayed number from 0 → data-target over ~2 seconds
     - Uses an ease-out function for smooth deceleration
     - Triggered via Intersection Observer (fires only when visible)
     ========================================================================= */

  const counters = document.querySelectorAll('.counter-number[data-target]');

  if (counters.length > 0 && 'IntersectionObserver' in window) {
    /**
     * Animate a counter element from 0 to its target value.
     * @param {HTMLElement} el - The counter element
     */
    function animateCounter(el) {
      const target   = parseInt(el.getAttribute('data-target'), 10);
      const duration = 2000;   // 2 seconds
      const startTime = performance.now();

      /**
       * Ease-out cubic: decelerates towards the end
       * @param {number} t - progress (0 → 1)
       * @returns {number}
       */
      function easeOutCubic(t) {
        return 1 - Math.pow(1 - t, 3);
      }

      function updateCounter(currentTime) {
        const elapsed  = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        const eased    = easeOutCubic(progress);
        const current  = Math.floor(eased * target);

        el.textContent = current.toLocaleString();

        if (progress < 1) {
          requestAnimationFrame(updateCounter);
        } else {
          // Ensure final value is exact
          el.textContent = target.toLocaleString();
        }
      }

      requestAnimationFrame(updateCounter);
    }

    const counterObserver = new IntersectionObserver(
      (entries, observer) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            animateCounter(entry.target);
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.3 }
    );

    counters.forEach((counter) => counterObserver.observe(counter));
  }


  /* =========================================================================
     5. STICKY HEADER SHADOW
     =========================================================================
     - Adds a .scrolled class to the header when page is scrolled past 100px
     - CSS uses .scrolled to enhance the box-shadow
     ========================================================================= */

  const siteHeader = document.querySelector('.site-header');

  if (siteHeader) {
    let lastScrollY = 0;
    let ticking     = false;

    function updateHeaderShadow() {
      if (window.scrollY > 100) {
        siteHeader.classList.add('scrolled');
      } else {
        siteHeader.classList.remove('scrolled');
      }
      ticking = false;
    }

    window.addEventListener('scroll', () => {
      lastScrollY = window.scrollY;
      if (!ticking) {
        window.requestAnimationFrame(updateHeaderShadow);
        ticking = true;
      }
    }, { passive: true });

    // Run once on load in case page is already scrolled
    updateHeaderShadow();
  }


  /* =========================================================================
     6. ACTIVE NAVIGATION LINK HIGHLIGHTING
     =========================================================================
     - Compares each nav link's href with window.location.pathname
     - Adds .active class to the matching link
     - Handles both exact matches and partial path matches
     ========================================================================= */

  const navLinksAll = document.querySelectorAll('.nav-links a');

  if (navLinksAll.length > 0) {
    const currentPath = window.location.pathname;

    navLinksAll.forEach((link) => {
      const linkPath = new URL(link.href, window.location.origin).pathname;

      // Exact match, or match for root path
      if (linkPath === currentPath) {
        link.classList.add('active');
      }
      // Partial match for sub-pages (e.g. /about/ matches /about/history/)
      // But avoid matching '/' to everything
      else if (linkPath !== '/' && currentPath.startsWith(linkPath)) {
        link.classList.add('active');
      }
    });
  }


  /* =========================================================================
     7. SMOOTH SCROLL FOR ANCHOR LINKS
     =========================================================================
     - Intercepts clicks on links that start with #
     - Smoothly scrolls to the target element
     - Accounts for the sticky header height offset
     ========================================================================= */

  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener('click', function (e) {
      const targetId = this.getAttribute('href');

      // Ignore empty hash links
      if (targetId === '#' || targetId === '') return;

      const targetEl = document.querySelector(targetId);
      if (targetEl) {
        e.preventDefault();

        // Calculate header offset for sticky header
        const header       = document.querySelector('.site-header');
        const headerHeight = header ? header.offsetHeight : 0;
        const navBar       = document.querySelector('.main-nav');
        const navHeight    = navBar ? navBar.offsetHeight : 0;
        const totalOffset  = headerHeight + navHeight + 20; // 20px breathing room

        const targetPosition = targetEl.getBoundingClientRect().top
                             + window.pageYOffset
                             - totalOffset;

        window.scrollTo({
          top: targetPosition,
          behavior: 'smooth'
        });
      }
    });
  });


  /* =========================================================================
     UTILITIES — CONSOLE GREETING
     ========================================================================= */

  console.log(
    '%c✦ St. Xavier\'s School, Harmutty — Website Loaded Successfully ✦',
    'color: #d4a745; font-size: 14px; font-weight: bold; background: #0a1628; padding: 8px 16px; border-radius: 4px;'
  );
});
