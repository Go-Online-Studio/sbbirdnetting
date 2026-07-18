
/* Preloader logic */
(function() {
  function dismissPreloader() {
    const preloader = document.getElementById("preloader");
    if (!preloader) return;
    preloader.style.opacity = '0';
    preloader.style.transition = 'opacity 0.5s ease';
    setTimeout(() => {
      if (preloader.parentNode) preloader.parentNode.removeChild(preloader);
      document.body.classList.remove("loading");
    }, 500);
  }

  function checkCriticalAssets() {
    // Nav
    const nav = document.querySelector("header[role='banner']");
    // First section after header
    const firstSection = document.querySelector("header[role='banner'] + *");
    
    let images = [];
    if (nav) images = images.concat(Array.from(nav.querySelectorAll("img")));
    if (firstSection) images = images.concat(Array.from(firstSection.querySelectorAll("img")));

    // Filter out already loaded
    images = images.filter(img => !img.complete);

    if (images.length === 0) {
      dismissPreloader();
    } else {
      let loadedCount = 0;
      const onImageLoad = () => {
        loadedCount++;
        if (loadedCount === images.length) dismissPreloader();
      };
      images.forEach(img => {
        img.addEventListener("load", onImageLoad);
        img.addEventListener("error", onImageLoad);
      });
    }
  }

  document.addEventListener("DOMContentLoaded", () => {
    checkCriticalAssets();
    // Fallback
    setTimeout(dismissPreloader, 3000);
  });
})();

function debounce(t,e){let n;return function(...o){clearTimeout(n),n=setTimeout(()=>t.apply(this,o),e)}}$(document).ready(function(){const t="919081062820",e=document.getElementById("current-year");function n(){const e=$(window).width()<=767.98;$('a[href*="whatsapp.com/send"], a[href*="wa.me"]').each(function(){const n=$(this).attr("href");let o="";try{if(n.includes("?")){o=new URL(n).searchParams.get("text")||""}}catch(t){const e=n.match(/[?&]text=([^&#]*)/);e&&(o=decodeURIComponent(e[1]))}let a="";const s=o?encodeURIComponent(o):"";a=e?`https://api.whatsapp.com/send?phone=${t}${s?"&text="+s:""}`:`https://web.whatsapp.com/send?phone=${t}${s?"&text="+s:""}`,$(this).attr("href",a)})}e&&(e.textContent=(new Date).getFullYear()),n(),$(window).on("resize",debounce(function(){n()},200));const o=document.querySelector("#contactPageForm");o&&$(o).on("submit",function(e){if(e.preventDefault(),!o.checkValidity())return e.stopPropagation(),void o.classList.add("was-validated");const n=$("#validationCustom01").val(),a=$("#validationNumber").val(),s=$("#validationCustomUsername").val(),i=$("#validationMessage").val(),c=encodeURIComponent(`Hello, I want to query about your services:\n\nName: ${n}\nEmail: ${s}\nPhone: ${a||"Not provided"}\nMessage: ${i}`);if($(window).width()<=767.98){const e=navigator.userAgent||navigator.vendor||window.opera;/android/i.test(e)?window.location.href=`intent://send?phone=${t}&text=${c}#Intent;scheme=whatsapp;package=com.whatsapp;end`:window.location.href=`https://wa.me/${t}?text=${c}`}else{const e=`https://web.whatsapp.com/send?phone=${t}&text=${c}`;window.open(e,"_blank")}o.reset(),o.classList.remove("was-validated")})});