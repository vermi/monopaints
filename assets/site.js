// Full-screen viewer for the portfolio, and the copy-email button.

(function () {
  const dialog = document.querySelector(".lightbox");
  const triggers = Array.from(document.querySelectorAll("[data-full]"));

  if (dialog && triggers.length) {
    const img = dialog.querySelector(".lightbox-stage img");
    const caption = dialog.querySelector(".lightbox-foot .caption");
    const count = dialog.querySelector(".lightbox-count");
    let current = 0;

    function show(index) {
      current = (index + triggers.length) % triggers.length;
      const trigger = triggers[current];
      const thumb = trigger.querySelector("img");
      img.src = trigger.dataset.full;
      img.alt = thumb.alt;
      caption.innerHTML = trigger.closest("li").querySelector(".caption").innerHTML;
      count.textContent = `${current + 1} of ${triggers.length}`;
      // Warm up the neighbors so stepping through feels instant.
      [current - 1, current + 1].forEach((i) => {
        const next = triggers[(i + triggers.length) % triggers.length];
        new Image().src = next.dataset.full;
      });
    }

    triggers.forEach((trigger, index) => {
      trigger.addEventListener("click", () => {
        show(index);
        dialog.showModal();
      });
    });

    dialog.querySelector("[data-close]").addEventListener("click", () => dialog.close());
    dialog.querySelector("[data-prev]").addEventListener("click", () => show(current - 1));
    dialog.querySelector("[data-next]").addEventListener("click", () => show(current + 1));

    dialog.addEventListener("keydown", (event) => {
      if (event.key === "ArrowLeft") show(current - 1);
      if (event.key === "ArrowRight") show(current + 1);
    });

    // Clicking the dark area around the painting closes the viewer.
    dialog.querySelector(".lightbox-stage").addEventListener("click", (event) => {
      if (event.target !== img) dialog.close();
    });

    let touchX = null;
    dialog.addEventListener("touchstart", (event) => {
      touchX = event.touches[0].clientX;
    }, { passive: true });
    dialog.addEventListener("touchend", (event) => {
      if (touchX === null) return;
      const dx = event.changedTouches[0].clientX - touchX;
      if (Math.abs(dx) > 50) show(current + (dx < 0 ? 1 : -1));
      touchX = null;
    });
  }

  const copy = document.querySelector(".copy-email");
  if (copy && navigator.clipboard) {
    copy.hidden = false;
    copy.addEventListener("click", async () => {
      try {
        await navigator.clipboard.writeText(copy.dataset.email);
        copy.textContent = "Email address copied";
      } catch {
        copy.textContent = "Couldn't copy. Select the address above instead.";
      }
    });
  }
})();
