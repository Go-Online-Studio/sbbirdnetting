// Debounce function to limit how often functions execute on resize/scroll
function debounce(func, delay) {
  let timeout;
  return function (...args) {
    clearTimeout(timeout);
    timeout = setTimeout(() => func.apply(this, args), delay);
  };
}

$(document).ready(function () {
  const phoneNumber = "919081062820";

  // Function to initialize dynamic WhatsApp links on page load and resize
  function initializeWhatsAppLinks() {
    const isMobile = $(window).width() <= 767.98;

    // Target all anchors that reference whatsapp or wa.me
    $('a[href*="whatsapp.com/send"], a[href*="wa.me"]').each(function () {
      const currentUrl = $(this).attr("href");
      let textParam = "";

      try {
        // Try parsing URL query parameter
        if (currentUrl.includes("?")) {
          const urlObj = new URL(currentUrl);
          textParam = urlObj.searchParams.get("text") || "";
        }
      } catch (e) {
        // Regex fallback if parsing fails (e.g. invalid base url)
        const textMatch = currentUrl.match(/[?&]text=([^&#]*)/);
        if (textMatch) {
          textParam = decodeURIComponent(textMatch[1]);
        }
      }

      let newHref = "";
      const encodedText = textParam ? encodeURIComponent(textParam) : "";

      if (isMobile) {
        // Mobile Link
        newHref = `https://api.whatsapp.com/send?phone=${phoneNumber}${encodedText ? "&text=" + encodedText : ""}`;
      } else {
        // Desktop Link
        newHref = `https://web.whatsapp.com/send?phone=${phoneNumber}${encodedText ? "&text=" + encodedText : ""}`;
      }

      $(this).attr("href", newHref);
    });
  }

  // Initial call
  initializeWhatsAppLinks();

  // Reinitialize on window resize with debounce
  $(window).on(
    "resize",
    debounce(function () {
      initializeWhatsAppLinks();
    }, 200)
  );

  // --- Contact Form Submission Logic ---
  const contactForm = document.querySelector("#contactPageForm");
  if (contactForm) {
    $(contactForm).on("submit", function (event) {
      event.preventDefault(); // Stop default form redirect

      // Validate Bootstrap Form
      if (!contactForm.checkValidity()) {
        event.stopPropagation();
        contactForm.classList.add("was-validated");
        return;
      }

      const name = $("#validationCustom01").val();
      const phone = $("#validationNumber").val();
      const email = $("#validationCustomUsername").val();
      const message = $("#validationMessage").val();

      // Construct the WhatsApp message
      const formattedMessage = `Hello, I want to query about your services:\n\nName: ${name}\nEmail: ${email}\nPhone: ${phone || "Not provided"}\nMessage: ${message}`;
      const encodedMessage = encodeURIComponent(formattedMessage);

      const isMobile = $(window).width() <= 767.98;

      if (isMobile) {
        const userAgent = navigator.userAgent || navigator.vendor || window.opera;
        // Check if Android device
        if (/android/i.test(userAgent)) {
          window.location.href = `intent://send?phone=${phoneNumber}&text=${encodedMessage}#Intent;scheme=whatsapp;package=com.whatsapp;end`;
        } else {
          // Fallback for iOS and other mobile platforms
          window.location.href = `https://wa.me/${phoneNumber}?text=${encodedMessage}`;
        }
      } else {
        // Use WhatsApp Web URL for desktop
        const whatsappWebUrl = `https://web.whatsapp.com/send?phone=${phoneNumber}&text=${encodedMessage}`;
        window.open(whatsappWebUrl, "_blank");
      }

      // Reset form and clear validation styling
      contactForm.reset();
      contactForm.classList.remove("was-validated");
    });
  }
});
