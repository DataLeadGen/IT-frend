/*=========================================
  Main JavaScript - IT FRNDLeads
=========================================*/

document.addEventListener('DOMContentLoaded', function() {
  'use strict';
  
  console.log('DOM fully loaded - initializing components');
  
  // Initialize all components
  initPreloader();
  initNavigation();
  initScrollAnimations();
  initParticles();
  initBackToTop();
  initContactForm();
  initSkeletonLoaders();
  
  // Preloader
  function initPreloader() {
    const preloader = document.querySelector('.loader-wrapper');
    
    if (preloader) {
      // Hide preloader after a short delay
      setTimeout(function() {
        preloader.classList.add('hidden');
        // Enable scrolling after preloader is hidden
        document.body.style.overflow = 'visible';
      }, 800);
      
      // Also bind to window load event as a fallback
      window.addEventListener('load', function() {
        preloader.classList.add('hidden');
        document.body.style.overflow = 'visible';
      });
      
      // Disable scrolling while preloader is visible
      document.body.style.overflow = 'hidden';
    }
  }
  
  // Navigation
  function initNavigation() {
    const header = document.querySelector('.header');
    const navToggle = document.querySelector('.nav-toggle');
    const navMenu = document.querySelector('.nav-menu');
    const navLinks = document.querySelectorAll('.nav-link');
    
    // Handle scroll
    window.addEventListener('scroll', function() {
      if (window.scrollY > 50) {
        header.classList.add('header-scrolled');
      } else {
        header.classList.remove('header-scrolled');
      }
    });
    
    // Mobile menu toggle
    if (navToggle) {
      navToggle.addEventListener('click', function() {
        navMenu.classList.toggle('active');
        
        // Toggle between hamburger and X icon
        const iconElement = this.querySelector('i');
        if (iconElement.classList.contains('feather-menu')) {
          iconElement.classList.remove('feather-menu');
          iconElement.classList.add('feather-x');
        } else {
          iconElement.classList.remove('feather-x');
          iconElement.classList.add('feather-menu');
        }
      });
    }
    
    // Close mobile menu when clicking a nav link
    navLinks.forEach(link => {
      link.addEventListener('click', function() {
        if (navMenu) {
          navMenu.classList.remove('active');
        }
        
        // Reset icon if navToggle exists
        if (navToggle) {
          const iconElement = navToggle.querySelector('i');
          if (iconElement) {
            iconElement.classList.remove('feather-x');
            iconElement.classList.add('feather-menu');
          }
        }
        
        // Update active link
        navLinks.forEach(navLink => navLink.classList.remove('active'));
        this.classList.add('active');
      });
    });
    
    // Set active nav link based on scroll position
    window.addEventListener('scroll', function() {
      if (navLinks.length === 0) return;
      
      let current = '';
      
      const sections = document.querySelectorAll('section[id]');
      
      sections.forEach(section => {
        const sectionTop = section.offsetTop - 100;
        const sectionHeight = section.offsetHeight;
        
        if (window.scrollY >= sectionTop && window.scrollY < sectionTop + sectionHeight) {
          current = section.getAttribute('id');
        }
      });
      
      if (current) {
        navLinks.forEach(link => {
          link.classList.remove('active');
          const href = link.getAttribute('href');
          if (href && href.includes(current)) {
            link.classList.add('active');
          }
        });
      }
    });
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
      anchor.addEventListener('click', function(e) {
        e.preventDefault();
        
        const targetId = this.getAttribute('href');
        if (targetId === '#') return;
        
        const targetElement = document.querySelector(targetId);
        
        if (targetElement) {
          window.scrollTo({
            top: targetElement.offsetTop - 80, // Account for fixed header
            behavior: 'smooth'
          });
        }
      });
    });
  }
  
  // Scroll animations
  function initScrollAnimations() {
    const animatedElements = document.querySelectorAll('.fade-in, .slide-in-left, .slide-in-right');
    
    function checkScroll() {
      animatedElements.forEach(element => {
        const elementTop = element.getBoundingClientRect().top;
        const windowHeight = window.innerHeight;
        
        // When element is in viewport
        if (elementTop < windowHeight * 0.85) {
          element.classList.add('visible');
        }
      });
    }
    
    // Check positions on load
    checkScroll();
    
    // Check positions on scroll
    window.addEventListener('scroll', checkScroll);
  }
  
  // Initialize particles.js
  function initParticles() {
    // Make sure the particles.js container exists
    if (document.getElementById('particles-js')) {
      // Try initialize on DOM ready
      if (typeof particlesJS !== 'undefined') {
        particlesJS('particles-js', particlesConfig);
      } else {
        // Fallback: try again after a delay
        console.log('Waiting for particles.js to load...');
        setTimeout(function() {
          if (typeof particlesJS !== 'undefined') {
            particlesJS('particles-js', particlesConfig);
          } else {
            console.error('Could not initialize particles.js');
          }
        }, 1000);
      }
    }
  }
  
  // Back to top button
  function initBackToTop() {
    const backToTopBtn = document.querySelector('.back-to-top');
    
    if (backToTopBtn) {
      window.addEventListener('scroll', function() {
        if (window.scrollY > 300) {
          backToTopBtn.classList.add('visible');
        } else {
          backToTopBtn.classList.remove('visible');
        }
      });
      
      backToTopBtn.addEventListener('click', function(e) {
        e.preventDefault();
        window.scrollTo({
          top: 0,
          behavior: 'smooth'
        });
      });
    }
  }
  
  // Contact form validation
  function initContactForm() {
    const contactForm = document.getElementById('contactForm');
    
    if (contactForm) {
      contactForm.addEventListener('submit', function(e) {
        let valid = true;
        const nameInput = document.getElementById('name');
        const emailInput = document.getElementById('email');
        const subjectInput = document.getElementById('subject');
        const messageInput = document.getElementById('message');
        
        // Simple client-side validation
        if (!nameInput.value.trim()) {
          showError(nameInput, 'Please enter your name');
          valid = false;
        } else {
          removeError(nameInput);
        }
        
        if (!emailInput.value.trim()) {
          showError(emailInput, 'Please enter your email');
          valid = false;
        } else if (!isValidEmail(emailInput.value.trim())) {
          showError(emailInput, 'Please enter a valid email address');
          valid = false;
        } else {
          removeError(emailInput);
        }
        
        if (!subjectInput.value.trim()) {
          showError(subjectInput, 'Please enter a subject');
          valid = false;
        } else {
          removeError(subjectInput);
        }
        
        if (!messageInput.value.trim() || messageInput.value.trim().length < 10) {
          showError(messageInput, 'Please enter a message (at least 10 characters)');
          valid = false;
        } else {
          removeError(messageInput);
        }
        
        if (!valid) {
          e.preventDefault();
        }
      });
      
      // Function to show error message
      function showError(input, message) {
        const formGroup = input.closest('.form-group');
        formGroup.classList.add('has-error');
        
        let errorElement = formGroup.querySelector('.error-message');
        
        if (!errorElement) {
          errorElement = document.createElement('div');
          errorElement.className = 'error-message';
          errorElement.style.color = 'var(--highlight-yellow)';
          errorElement.style.fontSize = '0.85rem';
          errorElement.style.marginTop = '0.5rem';
          formGroup.appendChild(errorElement);
        }
        
        errorElement.textContent = message;
      }
      
      // Function to remove error message
      function removeError(input) {
        const formGroup = input.closest('.form-group');
        formGroup.classList.remove('has-error');
        
        const errorElement = formGroup.querySelector('.error-message');
        if (errorElement) {
          errorElement.remove();
        }
      }
      
      // Function to validate email format
      function isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
      }
    }
  }
  
  // Animate numbers/counters
  const counterElements = document.querySelectorAll('.stat-number');
  
  if (counterElements.length > 0) {
    const observerOptions = {
      threshold: 0.5
    };
    
    const observer = new IntersectionObserver(function(entries) {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const element = entry.target;
          
          if (!element.classList.contains('counted')) {
            element.classList.add('counted');
            
            const countTo = parseInt(element.getAttribute('data-count'), 10);
            let count = 0;
            const duration = 2000;
            const increment = Math.ceil(countTo / (duration / 30));
            
            const timer = setInterval(function() {
              count += increment;
              
              if (count >= countTo) {
                element.textContent = countTo.toLocaleString();
                clearInterval(timer);
              } else {
                element.textContent = count.toLocaleString();
              }
            }, 30);
          }
        }
      });
    }, observerOptions);
    
    counterElements.forEach(counter => {
      observer.observe(counter);
    });
  }
  

  
  // Skeleton Loading Animation
  function initSkeletonLoaders() {
    // Function to reveal content with skeletons
    function revealContent(containerId) {
      const container = document.getElementById(containerId);
      
      if (container) {
        // Simulate loading delay
        setTimeout(() => {
          // Hide skeleton loaders
          const skeletons = container.querySelectorAll('.skeleton-container');
          skeletons.forEach(skeleton => {
            skeleton.style.display = 'none';
          });
          
          // Show actual content
          container.classList.add('content-loaded');
          const contentElements = container.querySelectorAll('.real-content');
          contentElements.forEach(element => {
            element.classList.remove('content-hidden');
            // Re-initialize Feather icons if needed
            const featherIcons = element.querySelectorAll('[data-feather]');
            if (featherIcons.length > 0) {
              feather.replace(featherIcons);
            }
          });
        }, 1500); // Delay in milliseconds before showing content
      }
    }
    
    // Initialize skeleton loaders for different sections
    if (document.getElementById('specialized-services-container')) {
      revealContent('specialized-services-container');
    }
    
    if (document.getElementById('main-services-container')) {
      revealContent('main-services-container');
    }
  }
});
