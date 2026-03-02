// ===== SerNest Main JS =====
console.log("MAIN JS WORKING");
// Navbar scroll behavior
const navbar = document.querySelector('.navbar');
window.addEventListener('scroll', () => {
  if (window.scrollY > 30) {
    navbar.classList.add('scrolled');
  } else {
    navbar.classList.remove('scrolled');
  }
});

// Active nav link
const navLinks = document.querySelectorAll('.nav-links a');
navLinks.forEach(link => {
  if (link.href === window.location.href) {
    link.classList.add('active');
  }
});

// Scroll animations
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
    }
  });
}, { threshold: 0.08, rootMargin: '0px 0px -40px 0px' });

document.querySelectorAll('.animate-on-scroll').forEach(el => observer.observe(el));

// Fade-in animation on scroll
const cards = document.querySelectorAll(".workflow-card");

window.addEventListener("scroll", () => {
    cards.forEach(card => {
        const cardTop = card.getBoundingClientRect().top;
        if (cardTop < window.innerHeight - 50) {
            card.style.opacity = "1";
            card.style.transform = "translateY(0)";
        }
    });
});


// Mobile menu
const mobileToggle = document.querySelector('.nav-mobile-toggle');
const mobileMenu = document.querySelector('.mobile-menu');
if (mobileToggle && mobileMenu) {
  mobileToggle.addEventListener('click', () => {
    mobileMenu.classList.toggle('open');
  });
}

// Smooth count-up for hero stats
function countUp(el, target, duration = 1800) {
  let start = 0;
  const step = target / (duration / 16);
  const timer = setInterval(() => {
    start += step;
    if (start >= target) {
      el.textContent = target.toLocaleString() + '+';
      clearInterval(timer);
    } else {
      el.textContent = Math.floor(start).toLocaleString() + '+';
    }
  }, 16);
}

const statObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const nums = entry.target.querySelectorAll('[data-count]');
      nums.forEach(el => {
        const target = parseInt(el.dataset.count);
        countUp(el, target);
      });
      statObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.5 });

const statsSection = document.querySelector('.hero-stats');
if (statsSection) statObserver.observe(statsSection);



document.addEventListener("DOMContentLoaded", function () {

    const track = document.querySelector(".slider-track");
    const cards = document.querySelectorAll(".service-card");

    if (!track || cards.length === 0) {
        return;
    }

    let index = 0;

    function moveSlider() {
        index++;

        if (index >= cards.length) {
            index = 0;
        }

        const slideWidth = track.clientWidth;
        track.style.transform = `translateX(-${index * slideWidth}px)`;
    }

    setInterval(moveSlider, 3000);
});